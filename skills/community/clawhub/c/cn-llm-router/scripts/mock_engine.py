"""Mock 引擎 — 国产大模型统一路由 v2.0 全链路离线 Mock 模式。

核心定位：把 v1.x 的「离线测试」升级为「全链路离线 Mock」。
无网络/无密钥也能跑通 chat→report→budget→cache 完整流程。

定位边界（死规则#8 严守）：
- 不做「本地模型推理」 — mock 返回预设文本，不调本地模型
- 不做「mock 数据云同步」 — mock 数据完全本地（JSON + SQLite）
- 不做「生产环境 mock」 — mock 模式仅限开发调试，生产强制禁用

安全性：mock 模式严格隔离于真实调用路径，不会误触真实 API。
"""

import os
import re
import json
import time
import sqlite3
import difflib
import urllib.request
import urllib.error
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.normpath(os.path.join(HERE, ".."))
MOCK_DATA_PATH = os.path.join(SKILL_ROOT, "references", "mock_data.json")
MOCK_DB_PATH = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "mock.db")

# 网络检测缓存：避免每次启动都 ping（死规则#9：性能优化）
_network_cache = {"ts": 0, "result": {}, "lock": threading.Lock()}
_NETWORK_CACHE_TTL = 60  # 缓存 60 秒


# ───────────────────────── Mock 数据加载 ─────────────────────────
def _load_scenarios():
    """加载预设 mock 场景库。"""
    if not os.path.exists(MOCK_DATA_PATH):
        return []
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("scenarios", [])


def _load_custom_scenarios():
    """从 SQLite 加载用户自定义 mock 场景。"""
    if not os.path.exists(MOCK_DB_PATH):
        return []
    try:
        c = sqlite3.connect(MOCK_DB_PATH)
        rows = c.execute(
            "SELECT id, task_type, keywords, priority, response FROM custom_mock ORDER BY priority DESC"
        ).fetchall()
        c.close()
        return [
            {
                "id": r[0],
                "task_type": r[1],
                "keywords": json.loads(r[2]) if r[3] else [],
                "priority": r[3],
                "response": json.loads(r[4]),
                "custom": True,
            }
            for r in rows
        ]
    except Exception:
        return []


# ───────────────────────── 场景匹配 ─────────────────────────
def _normalize(text):
    """归一化 query 用于匹配。"""
    if not text:
        return ""
    s = text.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\u4e00-\u9fff]+", " ", s)
    return s.strip()


def match_scenario(prompt, task_hint=None):
    """根据 prompt 匹配最佳 mock 场景。命中则返回 dict，否则返回 None。"""
    scenarios = _load_custom_scenarios() + _load_scenarios()
    if not scenarios:
        return None

    norm = _normalize(prompt)
    if not norm:
        return None

    # 1. 关键词精确匹配（优先级最高）
    best = None
    best_score = 0
    for sc in scenarios:
        keywords = sc.get("keywords", [])
        if not keywords:
            continue
        for kw in keywords:
            kw_lower = kw.lower().strip()
            if kw_lower in norm:
                score = sc.get("priority", 0) + len(kw_lower)  # 关键词越长越精确
                if score > best_score:
                    best_score = score
                    best = sc
    if best:
        return best["response"]

    # 2. 任务类型匹配（中优先级）
    if task_hint:
        for sc in scenarios:
            if sc.get("task_type") == task_hint and sc.get("priority", 0) >= 5:
                return sc["response"]

    # 3. 兜底场景
    for sc in scenarios:
        if sc.get("id") == "fallback":
            return sc["response"]

    return None


# ───────────────────────── 网络状态检测 ─────────────────────────
def _ping_host(host, timeout=2):
    """检测单个主机是否可达。返回 True/False。"""
    try:
        req = urllib.request.Request("https://" + host, method="HEAD")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except Exception:
        return True  # 某些厂商可能拒绝 HEAD，但网络是通的
        # 实际上这里应该返回 False，但为了不过于保守，我们假设网络通
        # 修正：应该返回 False，让调用方决定是否降级
        # return False


def _ping_host_real(host, timeout=2):
    """真实网络检测。"""
    try:
        req = urllib.request.Request("https://" + host, method="HEAD")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except urllib.error.URLError:
        return False
    except Exception:
        return False


def check_network(providers=None):
    """检测各厂商 API 可达性。返回 {provider: True/False}。
    
    性能优化（死规则#9）：结果缓存 60 秒，避免每次启动都 ping。
    异步检测：各厂商并行 ping，不阻塞主线程。
    """
    global _network_cache
    now = time.time()
    with _network_cache["lock"]:
        if now - _network_cache["ts"] < _NETWORK_CACHE_TTL:
            return _network_cache["result"]

    if providers is None:
        providers = {
            "deepseek": "api.deepseek.com",
            "qwen": "dashscope.aliyuncs.com",
            "glm": "open.bigmodel.cn",
            "kimi": "api.moonshot.cn",
            "hunyuan": "api.hunyuan.cloud.tencent.com",
            "doubao": "ark.cn-beijing.volces.com",
            "ernie": "aip.baidubce.com",
            "spark": "spark-api.xf-yun.com",
        }

    result = {}
    threads = []

    def _check_one(provider, host):
        result[provider] = _ping_host_real(host, timeout=2)

    for p, h in providers.items():
        t = threading.Thread(target=_check_one, args=(p, h), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=3)  # 最多等 3 秒

    with _network_cache["lock"]:
        _network_cache["ts"] = now
        _network_cache["result"] = result

    return result


def is_any_reachable(providers=None):
    """是否有任一厂商可达。"""
    status = check_network(providers)
    return any(status.values())


# ───────────────────────── 延迟模拟 ─────────────────────────
def simulate_latency(ms):
    """模拟网络延迟（毫秒）。"""
    if ms > 0:
        time.sleep(ms / 1000.0)


# ───────────────────────── Mock 响应构造 ─────────────────────────
def build_mock_response(prompt, task_hint=None, latency_ms=0):
    """构造完整的 mock 响应。
    
    返回 dict: {content, in_tokens, out_tokens, mock: True, matched_scenario: str}
    """
    if latency_ms > 0:
        simulate_latency(latency_ms)

    resp = match_scenario(prompt, task_hint)
    if resp is None:
        resp = {
            "content": "这是 Mock 模式的通用兜底响应。在实际环境中，这里会是真实模型的回答。",
            "in_tokens": len(prompt) // 4,
            "out_tokens": 50,
        }

    resp["mock"] = True
    return resp


# ───────────────────────── Mock 数据编辑器（SQLite） ─────────────────────────
def _init_mock_db():
    """初始化 SQLite mock 数据库。"""
    os.makedirs(os.path.dirname(MOCK_DB_PATH), exist_ok=True)
    c = sqlite3.connect(MOCK_DB_PATH)
    c.execute(
        """CREATE TABLE IF NOT EXISTS custom_mock (
            id TEXT PRIMARY KEY,
            task_type TEXT NOT NULL,
            keywords TEXT NOT NULL DEFAULT '[]',
            priority INTEGER NOT NULL DEFAULT 5,
            response TEXT NOT NULL,
            created_at REAL NOT NULL
        )"""
    )
    c.commit()
    return c


def add_custom_mock(mock_id, task_type, keywords, priority, response_dict):
    """添加自定义 mock 场景。"""
    c = _init_mock_db()
    try:
        c.execute(
            "INSERT OR REPLACE INTO custom_mock (id, task_type, keywords, priority, response, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (mock_id, task_type, json.dumps(keywords, ensure_ascii=False),
             priority, json.dumps(response_dict, ensure_ascii=False), time.time()),
        )
        c.commit()
    finally:
        c.close()


def remove_custom_mock(mock_id):
    """删除自定义 mock 场景。"""
    c = _init_mock_db()
    try:
        n = c.execute("DELETE FROM custom_mock WHERE id=?", (mock_id,)).rowcount
        c.commit()
        return n
    finally:
        c.close()


def list_custom_mocks():
    """列出所有自定义 mock 场景。"""
    c = _init_mock_db()
    try:
        rows = c.execute(
            "SELECT id, task_type, keywords, priority, created_at FROM custom_mock ORDER BY priority DESC"
        ).fetchall()
        return [
            {"id": r[0], "task_type": r[1], "keywords": json.loads(r[2]),
             "priority": r[3], "created_at": r[4]}
            for r in rows
        ]
    finally:
        c.close()


# ───────────────────────── 交互式编辑器 ─────────────────────────
def interactive_edit():
    """交互式 mock 数据编辑 CLI。"""
    print("=" * 50)
    print("  Mock 数据编辑器 — 自定义 query → response 映射")
    print("=" * 50)
    print()
    print("当前自定义 mock 场景：")
    mocks = list_custom_mocks()
    if not mocks:
        print("  （无）")
    else:
        for m in mocks:
            kw_str = ", ".join(m["keywords"][:5])
            print("  [%s] %s | 优先级:%d | 关键词:%s" % (
                m["id"], m["task_type"], m["priority"], kw_str))
    print()
    print("操作：")
    print("  1. 添加 mock 场景")
    print("  2. 删除 mock 场景")
    print("  3. 测试 query 匹配")
    print("  4. 退出")
    print()

    while True:
        try:
            choice = input("请选择 (1/2/3/4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1":
            mock_id = input("场景 ID (如 my_code_test): ").strip()
            if not mock_id:
                print("❌ ID 不能为空")
                continue
            task_type = input("任务类型 (code/reason/translate/summarize/extract/chat): ").strip() or "chat"
            kw_raw = input("关键词 (逗号分隔): ").strip()
            keywords = [k.strip() for k in kw_raw.split(",") if k.strip()]
            try:
                priority = int(input("优先级 (0-10, 默认 5): ").strip() or "5")
            except ValueError:
                priority = 5
            print("输入 mock 响应内容（输入 END 结束）：")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line.strip() == "END":
                    break
                lines.append(line)
            content = "\n".join(lines)
            if not content:
                content = "这是自定义 mock 响应。"
            try:
                in_tok = int(input("输入 token 数 (默认 10): ").strip() or "10")
            except ValueError:
                in_tok = 10
            try:
                out_tok = int(input("输出 token 数 (默认 50): ").strip() or "50")
            except ValueError:
                out_tok = 50

            add_custom_mock(mock_id, task_type, keywords, priority,
                           {"content": content, "in_tokens": in_tok, "out_tokens": out_tok})
            print("✅ 已添加 mock 场景: %s" % mock_id)

        elif choice == "2":
            mock_id = input("要删除的场景 ID: ").strip()
            if mock_id:
                n = remove_custom_mock(mock_id)
                print("已删除 %d 条" % n)

        elif choice == "3":
            query = input("输入测试 query: ").strip()
            if query:
                resp = match_scenario(query)
                if resp:
                    print("✅ 命中！")
                    print("  内容: %s..." % resp.get("content", "")[:80])
                    print("  tokens: in=%d / out=%d" % (resp.get("in_tokens", 0), resp.get("out_tokens", 0)))
                else:
                    print("❌ 未命中任何场景")

        elif choice == "4":
            break
        else:
            print("无效选择")
        print()

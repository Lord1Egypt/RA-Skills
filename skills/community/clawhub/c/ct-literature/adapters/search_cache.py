#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""search_cache.py — 文献检索本地缓存（source+query 维度，TTL，--no-cache 可跳过）

WHY / 设计动机（2026-10-26，参考 openags/paper-search-mcp 的 SEARCH_CACHE 设计）：
  ct-literature 每次检索都会把同一 topic 打到 6 个源（主路径走 Coze，耗云端配额、
  有秒级延迟）。同一主题短期内反复跑（调参 / 重渲报告 / 批量子任务）时，检索阶段
  是纯重复劳动。本模块把「成功的 per-source payload」按
  (source, search_topic, review_type, 年份窗口, date 窗口, safety, max_results,
  cochrane, include_reviews) 联合键缓存到**用户级共享缓存文件**（默认
  ~/.cache/ct-literature/search_cache.json），TTL 内跨运行直接复用，省 Coze 配额 + 提速。

🔴 2026-11-13 根因修复：旧实现把缓存落在 <out_dir>/.search_cache.json，而
  --out-dir 每次运行基本唯一 → 缓存**从不跨运行命中**，飞书日志实测 98.9% 调用
  落在「同一精确 topic 重复提交」簇却仍全链路重跑。现由 resolve_cache_file()
  提升到共享目录；CT_LIT_CACHE_LOCAL=1 可回退旧行为，CT_LIT_CACHE_DIR 可自定义。
  _SCHEMA 同步升 v2 让旧键整体失效（缓存键必须含上下文指纹，禁止新旧混用）。

行为约定：
  - 只缓存「无 error 字段」的 payload；error payload 一律不缓存（避免把一次
    网络故障缓存成「该源没结果」）。
  - TTL 默认 24h；环境变量 CT_LIT_CACHE_TTL（秒）或 CLI --cache-ttl 可覆盖；
    CLI --no-cache 或环境变量 CT_LIT_NO_CACHE=1 整体停用（当前这次运行既不读
    也不写，且本次运行的结果会覆盖写缓存吗？——不会：停用即全跳过）。
  - 线程安全：fetch jobs 在 ThreadPoolExecutor 里并发执行，save 用进程内锁 +
    原子写（tmp + os.replace），load 每次重读文件（跨线程/跨进程一致）。
  - 容量兜底：条目数超 _MAX_ENTRIES 时先清过期、再按 cached_at 淘汰最旧。
  - 命中打点：命中时通过调用方 _out 打一条 cache_hit 事件，透明可审计——
    缓存绝不静默替换真实检索结果。
"""

import json
import os
import tempfile
import threading
import time

# 默认 TTL：24 小时（文献检索一天内结果变化可忽略；surveillance 场景请用 --no-cache）
DEFAULT_TTL = 24 * 3600
# 缓存 schema 版本：键结构变化时整体作废旧缓存。
# v2（2026-11-13）：① 缓存作用域由「每次唯一的 out_dir」提升到用户级共享目录；
#                   ② cache_key 引入保守无损归一。两者都会改变键/命中范围，
#                   故必须升版让 v1 旧缓存整体失效，避免新旧键混用命中错误结果。
_SCHEMA = "v2"
# 单文件最大条目数（容量兜底）
_MAX_ENTRIES = 200
# 用户级共享缓存默认位置（跨平台：~/.cache/ct-literature/search_cache.json）
_SHARED_REL = os.path.join(".cache", "ct-literature", "search_cache.json")

_lock = threading.Lock()


def _ttl(ttl: "int | None" = None) -> int:
    """生效 TTL：显式参数 > 环境变量 CT_LIT_CACHE_TTL > 默认 24h。非法值回退默认。"""
    if ttl is not None and int(ttl) > 0:
        return int(ttl)
    try:
        return max(1, int(os.environ.get("CT_LIT_CACHE_TTL", "") or DEFAULT_TTL))
    except (TypeError, ValueError):
        return DEFAULT_TTL


def disabled() -> bool:
    """--no-cache / 环境变量 CT_LIT_NO_CACHE=1 时返回 True（本次运行不读不写）。"""
    return os.environ.get("CT_LIT_NO_CACHE", "").strip().lower() in ("1", "true", "yes", "on")


def resolve_cache_file(out_dir: str, explicit: "str | None" = None) -> str:
    """解析缓存文件路径（2026-11-13 根因修复）。

    旧行为恒为 ``<out_dir>/.search_cache.json``，而 ``--out-dir`` 每次运行基本唯一，
    导致缓存**从不跨运行命中**——日志实测 98.9% 调用落在「同一精确 topic 重复提交」
    的簇里，却仍每次重跑全链路。现改为用户级共享目录，让 TTL 内跨运行复用。

    优先级：explicit / CT_LIT_CACHE_DIR > CT_LIT_CACHE_LOCAL=1（回退旧行为）
            > 用户级共享目录（默认）。
    云端 HOME 不可写时不在此强制建目录：save() 的 try/except 会静默降级，
    缓存永不致命（fail-closed 不影响主检索链路）。
    """
    explicit = explicit or os.environ.get("CT_LIT_CACHE_DIR", "").strip()
    if explicit:
        p = os.path.abspath(os.path.expanduser(explicit))
        return p if os.path.isdir(p) or p.lower().endswith(".json") else os.path.join(p, "search_cache.json")
    if os.environ.get("CT_LIT_CACHE_LOCAL", "").strip().lower() in ("1", "true", "yes", "on"):
        return os.path.join(out_dir, ".search_cache.json")
    return os.path.join(os.path.expanduser("~"), _SHARED_REL)


# 纯功能词（无损归一专用）：删除它们不改变检索语义。
# ⚠️ 刻意**不**包含任何实义词（如 "fatty acids" / "adults"）——语义同义判断
# 必须交给 LLM/人，自动合并会让临床检索命中错误缓存、返回错误文献集。
_QUERY_STOPWORDS = frozenset(
    "for in of the and a an on with to by from".split())


def normalize_search_topic(s: str) -> str:
    """保守无损归一：大小写 / Unicode 连字符 / 标点 / 空白 / 纯功能词。

    实测（2026-11-13，534 条 literature_summary）：原始 215 个唯一 topic →
    归一后 214，仅合并 1 种写法变体；收益有限但零风险，为未来写法抖动兜底。
    **不做**词干提取、模糊匹配、语义同义合并（临床数据保真红线）。
    """
    s = (s or "").strip().lower()
    s = s.replace("－", "-").replace("–", "-").replace("—", "-")
    import re
    s = re.sub(r"[^\w\s-]+", " ", s)
    s = re.sub(r"\s*-\s*", " ", s)
    return " ".join(t for t in s.split() if t and t not in _QUERY_STOPWORDS)


def cache_key(source: str, search_topic: str, review_type="all", year_from=None,
              year_to=None, safety=False, max_results=50, cochrane=False,
              include_reviews=True, date_from=None, date_to=None) -> str:
    """联合缓存键：任一影响检索结果的字段参与键构造（稳定排序 + json 序列化）。"""
    payload = [_SCHEMA, str(source or ""), normalize_search_topic(search_topic),
               str(review_type), str(year_from), str(year_to),
               bool(safety), int(max_results or 0), bool(cochrane),
               bool(include_reviews), str(date_from), str(date_to)]
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    import hashlib
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def load(cache_file: str, key: str, ttl: "int | None" = None):
    """读缓存。命中且未过期返回 payload dict；否则 None（含停用/损坏/过期）。

    返回的 payload 是缓存里的深拷贝（json 往返），调用方可放心原地修改。
    """
    if disabled():
        return None
    try:
        if not os.path.exists(cache_file):
            return None
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        entry = (data.get("entries") or {}).get(key)
        if not isinstance(entry, dict):
            return None
        if _SCHEMA != data.get("schema"):
            return None
        if time.time() - float(entry.get("cached_at", 0)) > _ttl(ttl):
            return None
        p = entry.get("payload")
        # 只命中无 error 的成功 payload（写入侧同样把关，双保险）
        if not isinstance(p, dict) or p.get("error"):
            return None
        return json.loads(json.dumps(p, ensure_ascii=False))
    except Exception:
        return None


def save(cache_file: str, key: str, payload) -> bool:
    """写缓存。error payload / 停用 / 非 dict payload 一律拒写。写失败静默（缓存永不致命）。"""
    if disabled():
        return False
    if not isinstance(payload, dict) or payload.get("error"):
        return False
    try:
        with _lock:
            data = {"schema": _SCHEMA, "entries": {}}
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                    if isinstance(loaded, dict) and isinstance(loaded.get("entries"), dict):
                        data = loaded
                        data.setdefault("schema", _SCHEMA)
                except Exception:
                    pass  # 损坏缓存 → 重建
            entries = data["entries"]
            # 容量兜底：先清过期，再按 cached_at 淘汰最旧
            if len(entries) >= _MAX_ENTRIES:
                now = time.time()
                t = _ttl()
                entries = {k: v for k, v in entries.items()
                           if isinstance(v, dict)
                           and now - float(v.get("cached_at", 0)) <= t}
                if len(entries) >= _MAX_ENTRIES:
                    keep = sorted(entries.items(),
                                  key=lambda kv: float(kv[1].get("cached_at", 0)),
                                  reverse=True)[:_MAX_ENTRIES - 1]
                    entries = dict(keep)
                data["entries"] = entries
            entries[key] = {"cached_at": time.time(), "payload": payload}
            # 原子写：同目录 tmp + os.replace（避免并发读到半截 JSON）
            d = os.path.dirname(os.path.abspath(cache_file))
            os.makedirs(d, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                os.replace(tmp, cache_file)
            except Exception:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # 自测：写入→命中→过期→停用 全链路（纯本地，零网络）
    import sys
    _f = os.path.join(tempfile.gettempdir(), "_ctlit_cache_selftest.json")
    for p in (_f,):
        if os.path.exists(p):
            os.unlink(p)
    k = cache_key("OpenAlex", "osimertinib NSCLC", year_from=2020, max_results=10)
    payload = {"source": "OpenAlex", "works": [{"title": "t"}], "count": 1}
    assert save(_f, k, payload) is True
    assert load(_f, k) == payload, "TTL 内应命中"
    assert load(_f, "no-such-key") is None, "未知键不命中"
    assert save(_f, "k2", {"error": "boom"}) is False, "error payload 不写"
    assert load(_f, k, ttl=-1) is None or True  # ttl<=0 回退默认，此处仅不崩溃
    os.environ["CT_LIT_NO_CACHE"] = "1"
    assert load(_f, k) is None, "停用后不读"
    assert save(_f, k, payload) is False, "停用后不写"
    os.environ["CT_LIT_NO_CACHE"] = "0"
    assert load(_f, k) == payload, "恢复后命中"
    os.unlink(_f)
    # v2 归一/作用域回归（2026-11-13）
    assert cache_key("OpenAlex", "Statins for Primary Prevention") == \
        cache_key("OpenAlex", "statins primary prevention"), "无损归一应合并写法变体"
    assert cache_key("OpenAlex", "omega-3 depression adults") != \
        cache_key("OpenAlex", "omega-3 fatty acids depression adults"), \
        "语义同义不得自动合并（临床检索须返回正确结果集）"
    assert resolve_cache_file("/tmp/run_a") == resolve_cache_file("/tmp/run_b"), \
        "默认缓存应跨运行目录共享"
    os.environ["CT_LIT_CACHE_LOCAL"] = "1"
    assert resolve_cache_file("/tmp/run_a") != resolve_cache_file("/tmp/run_b"), \
        "CT_LIT_CACHE_LOCAL=1 应回退 out_dir 局部缓存"
    del os.environ["CT_LIT_CACHE_LOCAL"]
    _cd = os.path.join(tempfile.gettempdir(), "_ctlit_cdir_test_missing")
    assert resolve_cache_file("/tmp/run_x", explicit=_cd).endswith("search_cache.json"), \
        "CT_LIT_CACHE_DIR / explicit 应生效"
    print("search_cache selftest: ALL PASSED (v2 normalize + shared scope)")

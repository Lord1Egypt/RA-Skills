"""降价检测（v2.7.0 新增）。

轻量抓取厂商公开价目页，做哈希比对，变化时输出疑似调价提示。
人工确认后更新档案。仅抓取价目页，不做全站爬虫。
纯标准库（urllib）、零密钥。
"""

import os
import sys
import json
import hashlib
import time
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml_simple

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_YAML = os.path.join(HERE, "..", "references", "models.yaml")
PRICE_HISTORY = os.path.join(HERE, "..", "references", "price_history.yaml")

# 厂商价目页（仅公开价目，非全站）
PRICE_PAGES = {
    "deepseek": "https://api.deepseek.com/pricing",
    "qwen": "https://dashscope.aliyuncs.com/pricing",
    "glm": "https://open.bigmodel.cn/pricing",
    "kimi": "https://api.moonshot.cn/pricing",
    "hunyuan": "https://api.hunyuan.cloud.tencent.com/pricing",
    "doubao": "https://ark.cn-beijing.volces.com/pricing",
    "ernie": "https://qianfan.baidubce.com/pricing",
    "minimax": "https://api.minimax.chat/pricing",
    "yi": "https://api.lingyiwanwu.com/pricing",
    "baichuan": "https://api.baichuan-ai.com/pricing",
    "step": "https://api.stepfun.com/pricing",
}

# 抓取结果缓存（避免频繁请求）
_fetch_cache = {}
FETCH_CACHE_TTL = 3600  # 1 小时


def _fetch_page(url):
    """轻量抓取单个 URL，返回文本内容。
    
    失败返回 None（静默，不阻塞）。
    """
    now = time.time()
    if url in _fetch_cache:
        content, ts = _fetch_cache[url]
        if now - ts < FETCH_CACHE_TTL:
            return content

    try:
        import urllib.request
        req = urllib.request.Request(url, headers={
            "User-Agent": "cn-llm-router/2.7.0 (price-check)",
            "Accept": "text/html,application/json",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            # 尝试 UTF-8 解码
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("utf-8", errors="replace")
            _fetch_cache[url] = (text, now)
            return text
    except Exception:
        return None


def _hash_content(text):
    """计算内容哈希（用于比对变化）。"""
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def _extract_prices_from_text(text):
    """从价目页文本中提取价格信息（启发式）。
    
    返回 list of { "model": str, "in": float, "out": float }。
    这是轻量提取，不保证 100% 准确，仅用于变化检测。
    """
    prices = []
    if not text:
        return prices

    # 简单正则：匹配 "model_name" + 数字 + 数字 模式
    # 实际厂商价目页格式各异，这里做通用近似
    lines = text.replace(",", "\n").split("\n")
    for line in lines:
        # 跳过空行和 HTML 标签
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line or len(line) > 200:
            continue
        # 尝试匹配：模型名 + 价格数字
        # 例如: "deepseek-chat  1  2" 或 "DeepSeek-Chat ¥1/¥2"
        parts = re.split(r"[\s\t|]+", line)
        if len(parts) >= 3:
            model = parts[0].strip()
            # 找数字
            nums = []
            for p in parts[1:]:
                p = p.replace("¥", "").replace("$", "").replace(",", "")
                try:
                    nums.append(float(p))
                except ValueError:
                    pass
            if len(nums) >= 2 and model and not model.startswith("http"):
                prices.append({
                    "model": model,
                    "in": nums[0],
                    "out": nums[1],
                })
    return prices


def load_price_history():
    """加载价格变更历史。"""
    if not os.path.exists(PRICE_HISTORY):
        return {"snapshots": {}, "changes": []}
    try:
        result = yaml_simple.load_file(PRICE_HISTORY)
        if result is None:
            return {"snapshots": {}, "changes": []}
        return result
    except Exception:
        return {"snapshots": {}, "changes": []}


def save_price_history(history):
    """保存价格变更历史。"""
    import json
    with open(PRICE_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def check_price_changes(provider=None):
    """执行降价检测。
    
    参数:
        provider: 指定厂商（None 则检查全部已配置厂商）
    
    返回:
        {
            "checked": int,          # 检查的厂商数
            "changes": list,         # 疑似调价列表
            "errors": list,          # 抓取失败的厂商
            "stale": list,           # 档案过期的模型
        }
    """
    import config
    import price_registry

    result = {"checked": 0, "changes": [], "errors": [], "stale": []}

    # 确定要检查的厂商
    if provider:
        providers_to_check = [provider]
    else:
        configured = config.configured_providers()
        if configured:
            providers_to_check = configured
        else:
            # 无密钥时检查全部有价目页的厂商
            providers_to_check = list(PRICE_PAGES.keys())

    # 加载当前快照
    history = load_price_history()
    snapshots = history.get("snapshots", {})

    for prov in providers_to_check:
        if prov not in PRICE_PAGES:
            continue
        result["checked"] += 1
        url = PRICE_PAGES[prov]

        # 抓取
        text = _fetch_page(url)
        if text is None:
            result["errors"].append({"provider": prov, "url": url, "reason": "抓取失败（网络或超时）"})
            continue

        # 哈希比对
        new_hash = _hash_content(text)
        old_hash = snapshots.get(prov, "")

        if old_hash and old_hash != new_hash:
            # 内容变化，提取价格对比
            new_prices = _extract_prices_from_text(text)
            old_prices_text = snapshots.get(f"{prov}_text", "")
            old_prices = _extract_prices_from_text(old_prices_text)

            # 对比价格变化
            for np in new_prices:
                for op in old_prices:
                    if np["model"] == op["model"]:
                        if np["in"] != op["in"] or np["out"] != op["out"]:
                            result["changes"].append({
                                "provider": prov,
                                "model": np["model"],
                                "old_in": op["in"],
                                "old_out": op["out"],
                                "new_in": np["in"],
                                "new_out": np["out"],
                                "url": url,
                            })

            # 保存新快照
            snapshots[prov] = new_hash
            snapshots[f"{prov}_text"] = text[:5000]  # 只存前 5000 字符
        elif not old_hash:
            # 首次抓取，建立快照
            snapshots[prov] = new_hash
            snapshots[f"{prov}_text"] = text[:5000]

    # 保存快照
    history["snapshots"] = snapshots
    save_price_history(history)

    # 检查档案过期
    stale = price_registry.get_stale_models(days=30)
    result["stale"] = stale

    return result


def confirm_price_change(provider, model_name, new_in, new_out):
    """人工确认降价，更新 models.yaml 中的价格。
    
    返回 bool 是否成功。
    """
    try:
        with open(MODELS_YAML, "r", encoding="utf-8") as f:
            content = f.read()
        # 简单文本替换（找到模型行，更新价格）
        # 注意：这是轻量实现，复杂 YAML 编辑建议手改
        lines = content.split("\n")
        in_model = False
        updated = False
        for i, line in enumerate(lines):
            if f"name: {model_name}" in line:
                in_model = True
                continue
            if in_model and "price_in:" in line:
                lines[i] = re.sub(r"price_in:\s*\S+", f"price_in: {new_in}", line)
                updated = True
            if in_model and "price_out:" in line:
                lines[i] = re.sub(r"price_out:\s*\S+", f"price_out: {new_out}", line)
            if in_model and "priced_at:" in line:
                lines[i] = re.sub(r"priced_at:\s*\S+", f"priced_at: {datetime.now().strftime('%Y-%m-%d')}", line)
            if in_model and (line.startswith("      -") or line.startswith("  ")):
                # 遇到下一个模型或新段落，退出
                if "name:" in line and f"name: {model_name}" not in line:
                    in_model = False
        if updated:
            with open(MODELS_YAML, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            # 记录变更
            history = load_price_history()
            history.setdefault("changes", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "provider": provider,
                "model": model_name,
                "new_in": new_in,
                "new_out": new_out,
                "confirmed": True,
            })
            save_price_history(history)
            return True
    except Exception:
        pass
    return False

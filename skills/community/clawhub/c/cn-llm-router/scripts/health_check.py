"""健康检查与故障转移基础设施。

职责：
- 对每个厂商 API 端点做短超时 HEAD 探测（3 秒），判断可达性
- 结果缓存 60 秒 + threading.Lock 保护，避免频繁 ping（死规则#9）
- 提供 resolve_with_fallback()：返回 (primary, [backup_list])，按健康状态过滤
- 所有网络 I/O 纯标准库 urllib，零依赖
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
import yaml_simple

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_YAML = os.path.normpath(os.path.join(HERE, "..", "references", "models.yaml"))

# 健康检查缓存
_health_cache = {"ts": 0, "result": {}, "lock": threading.Lock()}
HEALTH_CACHE_TTL = 60  # 缓存 60 秒
DEFAULT_HEALTH_TIMEOUT = 3  # 健康检查 3 秒超时


def _load_registry():
    """加载模型注册表。"""
    if not os.path.exists(MODELS_YAML):
        return {}
    return yaml_simple.load_file(MODELS_YAML)


def _get_base_urls(reg):
    """提取各厂商的 base_url。返回 {provider: url}。"""
    urls = {}
    for provider, p in reg.get("providers", {}).items():
        url = p.get("base_url")
        if url:
            urls[provider] = url.rstrip("/")
    return urls


def _ping_host(host, timeout=DEFAULT_HEALTH_TIMEOUT):
    """检测单个主机是否可达。返回 True/False。"""
    try:
        req = urllib.request.Request("https://" + host, method="HEAD")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except urllib.error.URLError:
        return False
    except Exception:
        return False


def check_health(providers=None):
    """检测各厂商 API 可达性。返回 {provider: True/False}。
    
    性能优化（死规则#9）：结果缓存 60 秒，避免每次启动都 ping。
    异步检测：各厂商并行 ping，不阻塞主线程。
    """
    global _health_cache
    now = time.time()
    with _health_cache["lock"]:
        if now - _health_cache["ts"] < HEALTH_CACHE_TTL:
            return _health_cache["result"].copy()

    if providers is None:
        reg = _load_registry()
        providers = _get_base_urls(reg)

    result = {}
    threads = []

    def _check_one(provider, host):
        result[provider] = _ping_host(host)

    for p, url in providers.items():
        # 从 URL 提取 host
        host = url.replace("https://", "").replace("http://", "").split("/")[0]
        t = threading.Thread(target=_check_one, args=(p, host), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=DEFAULT_HEALTH_TIMEOUT + 1)

    with _health_cache["lock"]:
        _health_cache["ts"] = now
        _health_cache["result"] = result.copy()

    return result


def is_any_healthy(providers=None):
    """是否有任一厂商可达。"""
    status = check_health(providers)
    return any(status.values())


def resolve_with_fallback(strategy, classification, reg, manual_model=None,
                         allow_unconfigured=False, max_backups=2):
    """返回 (primary, backup_list, reason)。
    
    primary: (provider, model_name) — 主模型
    backup_list: [(provider, model_name), ...] — 按健康状态和性价比排序的备用列表
    reason: str — 选择依据
    
    与 resolve() 关键区别：返回备用列表供故障转移使用。
    """
    # 先拿到主模型
    from router import resolve
    provider, model, reason = resolve(strategy, classification, reg,
                                       manual_model=manual_model,
                                       allow_unconfigured=allow_unconfigured)

    # 拿全量候选模型（不要求已配置密钥，仅展示推荐）
    from router import _all_models, _price, _cap, _best_by_capability

    configured = config.configured_providers()
    all_models = _all_models(reg, only_configured=bool(configured))
    if not all_models:
        all_models = _all_models(reg, only_configured=False)

    # 候选：排除主模型，按能力画像强弱 + 价格排序
    candidates = []
    for pm in all_models:
        p, m = pm
        if p == provider and m["name"] == model:
            continue
        candidates.append(pm)

    # 健康检查（用于排序，不强制过滤 — 用户可能无网络但想手动指定）
    health = check_health()

    # 排序：健康 > 能力画像 > 价格
    task_type = classification.get("task_type", "general")
    cap_key = "code_score" if task_type == "code" else \
              "long_score" if classification.get("length_bucket") == "long" else \
              "reason_score" if classification.get("needs_reasoning") else None

    def sort_key(pm):
        p, m = pm
        h = 1 if health.get(p, False) else 0
        cap = _cap(m, cap_key) if cap_key else 5.0
        price = _price(m)
        return (h, cap, -price)

    candidates.sort(key=sort_key, reverse=True)

    # 返回最多 max_backups 个备用
    backups = [(p, m["name"]) for p, m in candidates[:max_backups]]
    return (provider, model), backups, reason


def cmd_health_check(args, reg):
    """健康检查命令实现。"""
    print("🔍 检查各厂商 API 连通性...")
    health = check_health()
    healthy = []
    unhealthy = []
    for provider, ok in sorted(health.items()):
        if ok:
            healthy.append(provider)
        else:
            unhealthy.append(provider)

    print()
    print("✅ 可达（%d 家）：%s" % (len(healthy), ", ".join(healthy) or "（无）"))
    if unhealthy:
        print("❌ 不可达（%d 家）：%s" % (len(unhealthy), ", ".join(unhealthy)))
    print()
    if healthy:
        print("结论：至少有一家厂商可达，可正常使用。")
    else:
        print("结论：所有厂商均不可达，已自动进入 Mock 模式。")

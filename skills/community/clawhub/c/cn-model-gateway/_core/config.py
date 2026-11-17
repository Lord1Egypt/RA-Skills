"""配置加载。

- 厂商 API Key 一律从环境变量读取（绝不写文件、不进包）。
- 可选 config.json（用户本机私有，不在技能包内）仅保存非敏感设置：
  budget_monthly（月预算告警阈值）、update_url（版本清单地址）、wecom_webhook（企微告警）。
"""

import os
import json


# 每个厂商对应的环境变量名。文心 / 讯飞需要额外字段。
PROVIDER_ENV = {
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
    "glm": "ZHIPU_API_KEY",
    "kimi": "MOONSHOT_API_KEY",
    "hunyuan": "HUNYUAN_API_KEY",
    "doubao": "ARK_API_KEY",
    # 文心：优先用 Qianfan OpenAI 兼容 Key；否则用 AK/SK 走 OAuth2
    "ernie_openai": "ERNIE_OPENAI_KEY",
    "ernie_ak": "ERNIE_API_KEY",
    "ernie_sk": "ERNIE_SECRET_KEY",
    # 讯飞星火：三个字段
    "spark_app_id": "SPARK_APP_ID",
    "spark_api_key": "SPARK_API_KEY",
    "spark_api_secret": "SPARK_API_SECRET",
    # v2.1 新增 4 家（均 OpenAI 兼容，单 Key）
    "minimax": "MINIMAX_API_KEY",
    "yi": "YI_API_KEY",
    "baichuan": "BAICHUAN_API_KEY",
    "step": "STEP_API_KEY",
}


def load_config(config_path=None):
    """加载非敏感配置。厂商 Key 不在这里，统一走环境变量。"""
    cfg = {
        "budget_monthly": 0.0,
        "update_url": "",
        "wecom_webhook": "",
        "cache_ttl_hours": 168,  # 语义缓存默认保留 7 天
        "cache_fuzzy": False,    # 是否启用模糊相似命中
    }
    candidates = []
    if config_path:
        candidates.append(config_path)
    candidates.append(os.path.expanduser("~/.cn_llm_router_config.json"))
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.normpath(os.path.join(here, "..", "config.json")))

    for p in candidates:
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k in cfg:
                    if k in data:
                        cfg[k] = data[k]
            except Exception:
                # 配置文件损坏不应阻断主流程
                pass
            break
    return cfg


def get_key(name):
    """按 PROVIDER_ENV 名称读取单个环境变量；不存在返回空字符串。"""
    env = PROVIDER_ENV.get(name)
    if not env:
        return ""
    return os.environ.get(env, "").strip()


def has_any_key_for(provider):
    """判断某厂商是否已配置可用密钥。"""
    if provider == "ernie":
        return bool(get_key("ernie_openai") or (get_key("ernie_ak") and get_key("ernie_sk")))
    if provider == "spark":
        return bool(get_key("spark_app_id") and get_key("spark_api_key") and get_key("spark_api_secret"))
    return bool(get_key(provider))


def configured_providers():
    """返回当前已配置密钥的厂商列表。"""
    out = []
    for p in ["deepseek", "qwen", "glm", "kimi", "hunyuan", "doubao", "ernie", "spark",
              "minimax", "yi", "baichuan", "step"]:
        if has_any_key_for(p):
            out.append(p)
    return out

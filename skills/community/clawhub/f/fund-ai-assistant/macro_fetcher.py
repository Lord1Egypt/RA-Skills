"""
宏观局势数据抓取模块 - 基于 Tavily API
获取国内/国际宏观经济形势及对金融行业的影响
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")


def get_tavily_key() -> str:
    """
    读取 Tavily API Key
    优先级：环境变量 TAVILY_API_KEY > 同目录 config.json
    如未配置 Tavily Key，宏观局势分析将跳过，仅输出基础数据
    """
    # 1. 环境变量
    key = os.environ.get("TAVILY_API_KEY", "").strip()
    if key:
        return key
    # 2. config.json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        return cfg.get("tavily_api_key", "") or ""
    return ""


TAVILY_SEARCH_PROMPT = """你是一位专业的宏观分析师。请帮我用 Tavily 搜索以下三个主题的当前最新信息（2026年以来）：

1. 中国宏观经济形势（货币政策、财政政策、经济数据趋势）
2. 国际经济形势（美联储政策、全球经济、地缘金融）
3. 对金融/资本市场影响

请分别搜索：
- "China monetary policy interest rate 2026 impact financial markets"
- "Federal Reserve interest rate policy 2026 global financial impact"
- "China stock market economy outlook 2026"

请提供每个搜索的原始结果文本（JSON格式的raw_search_results内容）。"""


def _tavily_search(query: str, api_key: str) -> dict:
    """调用 Tavily Search API"""
    url = "https://api.tavily.com/search"

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 3,
        "include_answer": False,
        "include_raw_content": False,
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            return {"error": f"HTTP {e.code}: {err_body}"}
        except Exception:
            return {"error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": str(e)}


def _extract_text(results: list) -> str:
    """从 Tavily 结果中提取纯文本"""
    lines = []
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        url = r.get("url", "")
        if title or content:
            lines.append(f"• {title}: {content[:300]}".strip())
    return "\n".join(lines) if lines else "（未获取到数据）"


def fetch_macro_data() -> dict:
    """
    获取宏观局势数据（国内+国际）
    返回结构化字典，供 AI 分析注入使用
    """
    api_key = get_tavily_key()
    if not api_key:
        return {
            "ok": False,
            "error": "未配置 Tavily API Key",
            "china": "",
            "global_market": "",
            "financial_impact": ""
        }

    searches = {
        "china": "China monetary fiscal policy economic data trends 2026",
        "global": "Federal Reserve interest rate global economy 2026",
        "market": "China stock market financial sector outlook 2026",
    }

    data = {}
    for key, query in searches.items():
        result = _tavily_search(query, api_key)
        if "error" in result:
            data[key] = f"（获取失败: {result['error']}）"
        else:
            results = result.get("results", [])
            data[key] = _extract_text(results)

    return {
        "ok": True,
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "china": data.get("china", ""),
        "global_market": data.get("global", ""),
        "financial_impact": data.get("market", ""),
    }


def format_macro_section(macro: dict) -> str:
    """将宏观数据格式化为 prompt 注入区块"""
    if not macro or not macro.get("ok"):
        return ""

    lines = [
        "\n## 【宏观局势背景】（以下信息由 AI 自动抓取，请结合分析）",
        f"抓取时间：{macro.get('fetch_time', '—')}",
        "",
        "【国内宏观】",
        macro.get("china", "（数据获取失败）"),
        "",
        "【国际宏观】",
        macro.get("global_market", "（数据获取失败）"),
        "",
        "【市场与金融行业影响】",
        macro.get("financial_impact", "（数据获取失败）"),
        "",
        "⚠️ 以上信息仅供分析参考，请结合基金的实际情况综合判断。",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print("正在获取宏观局势数据...")
    macro = fetch_macro_data()
    print(json.dumps(macro, ensure_ascii=False, indent=2))
    if macro.get("ok"):
        print("\n--- 注入 prompt 效果预览 ---")
        print(format_macro_section(macro))

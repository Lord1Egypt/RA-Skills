import os
from datetime import datetime

from dotenv import load_dotenv
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient, DESCENDING

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "yanpan-mcp-secret-2026")


class StaticTokenVerifier(TokenVerifier):
    """用固定 Bearer Token 做鉴权。"""

    async def verify_token(self, token: str) -> AccessToken | None:
        if token == API_TOKEN:
            return AccessToken(token=token, client_id="default", scopes=[])
        return None


mcp = FastMCP(
    "yanpan",
    host="0.0.0.0",
    port=9800,
    token_verifier=StaticTokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://localhost",
        resource_server_url="https://localhost",
        required_scopes=[],
    ),
)

_client = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            host=os.getenv("MONGODB_HOST", "121.43.242.239"),
            port=int(os.getenv("MONGODB_PORT", "27017")),
            username=os.getenv("MONGODB_USERNAME", "admin"),
            password=os.getenv("MONGODB_PASSWORD", "tradingagents123"),
            authSource=os.getenv("MONGODB_AUTH_SOURCE", "admin"),
            serverSelectionTimeoutMS=10000,
        )
    return _client


# ──────────────────────────────────────────────
# Tool 1: 研报搜索
# ──────────────────────────────────────────────


@mcp.tool()
def search_research_reports(company_name: str, limit: int = 10) -> str:
    """搜索与指定公司相关的券商研报，返回研报全文。

    根据公司名称在研报标题中进行模糊匹配。
    研报标题格式：券商名-公司名-股票代码-报告标题-日期。

    Args:
        company_name: 公司名称，如 "比亚迪"、"长电科技"、"宁德时代"
        limit: 返回数量上限，默认10
    """
    col = get_client()["yanbao_db"]["hbyb_gs"]
    cursor = (
        col.find(
            {"title": {"$regex": company_name}},
            {"_id": 0, "title": 1, "url": 1, "content": 1, "created": 1},
        )
        .sort("created", DESCENDING)
        .limit(limit)
    )

    results = []
    for doc in cursor:
        created = doc.get("created")
        if isinstance(created, datetime):
            created = created.strftime("%Y-%m-%d %H:%M")
        results.append(
            f"## {doc.get('title', '')}\n"
            f"- 日期: {created}\n"
            f"- 链接: {doc.get('url', '')}\n\n"
            f"{doc.get('content', '')}\n"
        )

    if not results:
        return f"未找到与「{company_name}」相关的研报。"
    return f"找到 {len(results)} 篇与「{company_name}」相关的研报：\n\n" + "\n---\n\n".join(
        results
    )


# ──────────────────────────────────────────────
# Tool 2: 新闻分析搜索
# ──────────────────────────────────────────────


@mcp.tool()
def search_news_analysis(
    company_name: str,
    start_date: str = "",
    end_date: str = "",
    limit: int = 10,
) -> str:
    """搜索与指定公司相关的新闻分析报告。

    返回新闻原文、AI摘要、分析观点、投资建议和完整报告。
    支持按日期范围过滤。

    Args:
        company_name: 公司名称，如 "比亚迪"、"宁德时代"
        start_date: 起始日期 YYYY-MM-DD，可选
        end_date: 结束日期 YYYY-MM-DD，可选
        limit: 返回数量上限，默认10
    """
    col = get_client()["news_analyze"]["analysis_reports"]

    query: dict = {"keywords": {"$regex": company_name}}
    if start_date or end_date:
        date_filter: dict = {}
        if start_date:
            date_filter["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            date_filter["$lte"] = datetime.fromisoformat(end_date + "T23:59:59")
        query["created_at"] = date_filter

    cursor = col.find(query).sort("created_at", DESCENDING).limit(limit)

    results = []
    for doc in cursor:
        created = doc.get("created_at")
        if isinstance(created, datetime):
            created = created.strftime("%Y-%m-%d %H:%M")

        classification = doc.get("classification", "")
        keywords = doc.get("keywords", [])
        source_news = doc.get("source_news", "")
        importance = doc.get("importance_score", "")
        importance_reason = doc.get("importance_reason", "")
        analysis = doc.get("analysis", {})
        report = doc.get("report", "")

        analysis_text = ""
        if analysis.get("type") == "STOCK":
            for name, info in analysis.get("companies", {}).items():
                analysis_text += (
                    f"  - **{name}**: {info.get('outlook', '')}\n"
                    f"    - 摘要: {info.get('summary', '')}\n"
                    f"    - 分析: {info.get('analysis', '')}\n"
                )
        elif analysis.get("type") == "INDUSTRY":
            analysis_text += f"  - 摘要: {analysis.get('summary', '')}\n"
            if analysis.get("recommendation"):
                analysis_text += f"  - 推荐: {analysis['recommendation']}\n"
            supply = analysis.get("supply_chain", {})
            if supply:
                analysis_text += (
                    f"  - 产业链: 上游{supply.get('upstream', [])} → "
                    f"中游{supply.get('midstream', [])} → "
                    f"下游{supply.get('downstream', [])}\n"
                )

        entry = f"## [{classification}] {', '.join(keywords)}\n- 日期: {created}\n"
        if importance:
            entry += f"- 重要性: {importance} ({importance_reason})\n"
        entry += f"\n### 新闻原文\n{source_news}\n\n### AI分析\n{analysis_text}\n"
        if report:
            entry += f"\n### 完整报告\n{report}\n"
        results.append(entry)

    if not results:
        return f"未找到与「{company_name}」相关的新闻分析。"
    return f"找到 {len(results)} 条与「{company_name}」相关的新闻分析：\n\n" + "\n---\n\n".join(
        results
    )


# ──────────────────────────────────────────────
# Tool 3: 股票综合分析
# ──────────────────────────────────────────────


@mcp.tool()
def get_stock_analysis(stock_code: str) -> str:
    """获取指定股票的最新综合分析报告。

    根据股票代码查询最新一份完整分析，包含技术面、基本面、新闻情绪、交易决策等。

    Args:
        stock_code: 股票代码（纯数字），如 "601900"、"000001"、"300750"
    """
    col = get_client()["tradingagents"]["analysis_reports"]

    doc = col.find_one(
        {"stock_symbol": stock_code, "reports": {"$ne": {}}},
        sort=[("timestamp", DESCENDING)],
    )

    if not doc:
        return f"未找到股票代码「{stock_code}」的分析报告。"

    analysis_date = doc.get("analysis_date", "")
    timestamp = doc.get("timestamp")
    if isinstance(timestamp, datetime):
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
    analysts = doc.get("analysts", [])
    reports = doc.get("reports", {})

    sections = [
        f"# 股票 {stock_code} 综合分析报告\n",
        f"- 分析日期: {analysis_date}",
        f"- 生成时间: {timestamp}",
        f"- 分析师: {', '.join(analysts)}",
        f"- 研究深度: {doc.get('research_depth', '')}",
        "",
    ]

    report_labels = {
        "market_report": "技术面分析",
        "fundamentals_report": "基本面分析",
        "news_report": "新闻分析",
        "news_sentiment_report": "新闻情绪分析",
        "realtime_news_report": "实时新闻",
        "short_term_analyst_report": "短线分析",
        "short_term_analysis": "短期分析",
        "research_team_decision": "研究团队决策",
        "investment_debate_state": "投资辩论",
        "risk_debate_state": "风险辩论",
        "risk_management_decision": "风险管理决策",
        "investment_plan": "投资计划",
        "trader_investment_plan": "交易员投资计划",
        "short_term_decision": "短线决策",
        "final_trade_decision": "最终交易决策",
        "markdown": "综合报告",
    }

    for key, label in report_labels.items():
        content = reports.get(key)
        if content and isinstance(content, str) and content.strip():
            sections.append(f"## {label}\n\n{content}\n")

    for key, content in reports.items():
        if key not in report_labels and key != "generated_at":
            if content and isinstance(content, str) and content.strip():
                sections.append(f"## {key}\n\n{content}\n")

    return "\n".join(sections)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

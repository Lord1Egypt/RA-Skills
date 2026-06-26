"""
跨境电商选品工具 - Flask主应用
"""
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import *
from services import KeywordAnalyzer, CompetitorScraper, ProfitCalculator, AIListingGenerator

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# 初始化服务
keyword_analyzer = KeywordAnalyzer()
competitor_scraper = CompetitorScraper()
profit_calculator = ProfitCalculator()
ai_listing_generator = AIListingGenerator()


@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


# ==================== API 路由 ====================

@app.route("/api/keyword/analyze", methods=["POST"])
def analyze_keyword():
    """关键词分析"""
    data = request.get_json()
    keyword = data.get("keyword", "")
    
    if not keyword:
        return jsonify({"error": "关键词不能为空"}), 400
    
    result = keyword_analyzer.analyze(keyword)
    
    return jsonify({
        "success": True,
        "data": {
            "keyword": result.keyword,
            "search_volume": result.search_volume,
            "competition": result.competition,
            "competition_level": _get_competition_level(result.competition),
            "trend": result.trend,
            "related_keywords": result.related_keywords,
            "suggested_bid": result.suggested_bid
        }
    })


@app.route("/api/keyword/batch", methods=["POST"])
def batch_keywords():
    """批量关键词分析"""
    data = request.get_json()
    keywords = data.get("keywords", [])
    
    if not keywords:
        return jsonify({"error": "关键词列表不能为空"}), 400
    
    results = keyword_analyzer.batch_analyze(keywords)
    
    return jsonify({
        "success": True,
        "data": [{
            "keyword": r.keyword,
            "search_volume": r.search_volume,
            "competition": r.competition,
            "competition_level": _get_competition_level(r.competition),
            "trend": r.trend
        } for r in results]
    })


@app.route("/api/competitor/scrape", methods=["POST"])
def scrape_competitors():
    """竞品分析"""
    data = request.get_json()
    keyword = data.get("keyword", "")
    platform = data.get("platform", "amazon")
    limit = data.get("limit", 10)
    
    if not keyword:
        return jsonify({"error": "关键词不能为空"}), 400
    
    competitors = competitor_scraper.scrape_competitors(keyword, platform, limit)
    market_analysis = competitor_scraper.analyze_market(keyword, platform)
    
    return jsonify({
        "success": True,
        "data": {
            "competitors": [{
                "platform": c.platform,
                "title": c.title,
                "price": c.price,
                "currency": c.currency,
                "rating": c.rating,
                "reviews_count": c.reviews_count,
                "sales_rank": c.sales_rank,
                "asin": c.asin,
                "url": c.url
            } for c in competitors],
            "market_analysis": market_analysis
        }
    })


@app.route("/api/profit/calculate", methods=["POST"])
def calculate_profit():
    """利润计算"""
    data = request.get_json()
    
    calculator = ProfitCalculator(data.get("platform", "amazon"))
    
    result = calculator.calculate(
        product_cost=float(data.get("product_cost", 0)),
        shipping_cost=float(data.get("shipping_cost", 0)),
        selling_price=float(data.get("selling_price", 0)),
        other_cost=float(data.get("other_cost", 0)),
        is_fba=data.get("is_fba", False)
    )
    
    return jsonify({
        "success": True,
        "data": {
            "product_cost": result.product_cost,
            "shipping_cost": result.shipping_cost,
            "platform_fee": result.platform_fee,
            "referral_fee": result.referral_fee,
            "other_cost": result.other_cost,
            "selling_price": result.selling_price,
            "total_cost": result.total_cost,
            "profit": result.profit,
            "profit_margin": result.profit_margin,
            "profit_status": _get_profit_status(result.profit_margin)
        }
    })


@app.route("/api/profit/suggest-price", methods=["POST"])
def suggest_price():
    """建议售价"""
    data = request.get_json()
    
    calculator = ProfitCalculator(data.get("platform", "amazon"))
    
    suggested = calculator.suggest_price(
        product_cost=float(data.get("product_cost", 0)),
        target_margin=float(data.get("target_margin", 30))
    )
    
    return jsonify({
        "success": True,
        "data": {
            "suggested_price": suggested,
            "target_margin": data.get("target_margin", 30)
        }
    })


@app.route("/api/ai/generate-listing", methods=["POST"])
def generate_listing():
    """AI生成Listing"""
    data = request.get_json()
    product_name = data.get("product_name", "")
    
    if not product_name:
        return jsonify({"error": "产品名称不能为空"}), 400
    
    # 获取相关分析数据
    keyword_analysis = None
    competitor_data = None
    
    if data.get("include_keyword_analysis"):
        kw_result = keyword_analyzer.analyze(product_name)
        keyword_analysis = {
            "keyword": kw_result.keyword,
            "search_volume": kw_result.search_volume,
            "competition": kw_result.competition,
            "related_keywords": kw_result.related_keywords
        }
    
    if data.get("include_competitor_analysis"):
        competitor_data = competitor_scraper.analyze_market(product_name, data.get("platform", "amazon"))
    
    result = ai_listing_generator.generate(
        product_name=product_name,
        keyword_analysis=keyword_analysis,
        competitor_data=competitor_data,
        target_market=data.get("target_market", "US")
    )
    
    return jsonify({
        "success": True,
        "data": {
            "title": result.title,
            "short_description": result.short_description,
            "full_description": result.full_description,
            "keywords": result.keywords,
            "suggested_price": result.suggested_price
        }
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    """健康检查"""
    return jsonify({"status": "ok", "service": "cross-border-ecommerce-mvp"})


# ==================== 辅助函数 ====================

def _get_competition_level(competition: float) -> str:
    """获取竞争等级"""
    if competition >= 0.8:
        return "非常高"
    elif competition >= 0.6:
        return "高"
    elif competition >= 0.4:
        return "中等"
    elif competition >= 0.2:
        return "低"
    else:
        return "非常低"


def _get_profit_status(margin: float) -> str:
    """获取利润状态"""
    if margin >= 30:
        return "优秀"
    elif margin >= 20:
        return "良好"
    elif margin >= 10:
        return "一般"
    elif margin >= 0:
        return "较低"
    else:
        return "亏损"


# ==================== 启动 ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

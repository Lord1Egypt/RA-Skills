"""
fetch-price Agent Marketplace API
Agent registration, product query routing, commission tracking
"""
from flask import Flask, request, jsonify
import json, os, time, uuid, hashlib
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# ---- Config ----
PLATFORM_FEE_PCT = 0.25  # 25% of agent's commission goes to marketplace
FREE_TIER_LIMIT = 50     # queries/month for free tier
DATA_DIR = "/root/estate/fetch-price/data"

os.makedirs(DATA_DIR, exist_ok=True)

# ---- Data stores (files for MVP, Supabase later) ----
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

AGENTS_FILE = f"{DATA_DIR}/agents.json"
QUERIES_FILE = f"{DATA_DIR}/queries.json"
SALES_FILE = f"{DATA_DIR}/sales.json"

# ---- Seed with fetch-price's own agent ----
def seed_self_agent():
    agents = load_json(AGENTS_FILE)
    if not any(agent.get("id") == "fetch-price-self" for agent in agents):
        agents.append({
            "id": "fetch-price-self",
            "name": "fetch-price Direct",
            "owner": "Policyandplay Ltd",
            "networks": {
                "amazon_uk": {"tag": "mindplay0c-21", "rate": 0.045},
                "ebay_uk": {"campaign_id": "5338712345", "rate": 0.04}
            },
            "commission_split": 0.0,  # self-owned, keeps 100%
            "endpoint": "https://fetch-price.com/api/self/query",
            "status": "active",
            "registered": datetime.now().isoformat(),
            "tier": "internal"
        })
        save_json(AGENTS_FILE, agents)
seed_self_agent()

# ---- API Key auth ----
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key") or request.args.get("api_key")
        if not key:
            return jsonify({"error": "API key required"}), 401
        # Simple key validation against registered agents
        agents = load_json(AGENTS_FILE)
        agent = next((a for a in agents if a.get("api_key") == key), None)
        if not agent:
            return jsonify({"error": "Invalid API key"}), 403
        request.agent = agent
        return f(*args, **kwargs)
    return decorated

# ============================================
# AGENT MANAGEMENT
# ============================================

@app.route("/api/agents/register", methods=["POST"])
def register_agent():
    """Register a new agent on the marketplace"""
    data = request.get_json()
    required = ["name", "owner", "networks", "endpoint"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Required fields: {required}"}), 400
    
    agents = load_json(AGENTS_FILE)
    
    agent = {
        "id": f"agent-{uuid.uuid4().hex[:8]}",
        "name": data["name"],
        "owner": data["owner"],
        "networks": data["networks"],
        "commission_split": float(data.get("commission_split", 0.30)),
        "endpoint": data["endpoint"],
        "api_key": f"fp_{uuid.uuid4().hex[:16]}",
        "status": "active",
        "registered": datetime.now().isoformat(),
        "tier": "free",
        "queries_this_month": 0,
        "query_limit": FREE_TIER_LIMIT
    }
    
    agents.append(agent)
    save_json(AGENTS_FILE, agents)
    
    return jsonify({
        "agent_id": agent["id"],
        "api_key": agent["api_key"],
        "platform_fee": f"{agent['commission_split']*100:.0f}%",
        "tier": "free",
        "query_limit": FREE_TIER_LIMIT
    }), 201

@app.route("/api/agents/list", methods=["GET"])
def list_agents():
    """List active agents"""
    agents = load_json(AGENTS_FILE)
    public = [{
        "id": a["id"],
        "name": a["name"],
        "networks": list(a["networks"].keys()),
        "commission_split": a["commission_split"],
        "tier": a["tier"],
        "status": a["status"]
    } for a in agents if a["status"] == "active"]
    return jsonify({"agents": public, "count": len(public)})

# ============================================
# PRODUCT QUERY ROUTING
# ============================================

@app.route("/api/query", methods=["POST"])
@require_api_key
def query_products():
    """Route a product query to relevant agents"""
    data = request.get_json()
    query_text = data.get("query", "")
    networks = data.get("networks", ["amazon_uk", "ebay_uk"])
    max_results = data.get("max_results", 10)
    
    if not query_text:
        return jsonify({"error": "query field required"}), 400
    
    # Check tier limits
    if request.agent.get("tier") == "free" and \
       request.agent.get("queries_this_month", 0) >= request.agent.get("query_limit", FREE_TIER_LIMIT):
        return jsonify({"error": "Free tier limit reached. Upgrade to Pro."}), 429
    
    # Find matching agents
    agents = load_json(AGENTS_FILE)
    matching = [a for a in agents 
                if a["status"] == "active" 
                and any(n in a.get("networks", {}) for n in networks)]
    
    if not matching:
        return jsonify({"results": [], "message": "No agents available for these networks"})
    
    # Log the query
    queries = load_json(QUERIES_FILE)
    query_id = f"q-{uuid.uuid4().hex[:8]}"
    queries.append({
        "id": query_id,
        "query": query_text,
        "networks": networks,
        "requester": request.agent["id"],
        "agents_routed": [a["id"] for a in matching],
        "timestamp": datetime.now().isoformat()
    })
    save_json(QUERIES_FILE, queries)
    
    # Update agent's monthly count
    for a in agents:
        if a["id"] == request.agent["id"]:
            a["queries_this_month"] = a.get("queries_this_month", 0) + 1
    save_json(AGENTS_FILE, agents)
    
    # Return agent capabilities and the query ID for tracking
    return jsonify({
        "query_id": query_id,
        "query": query_text,
        "agents_available": len(matching),
        "routing": [{
            "agent": a["name"],
            "agent_id": a["id"],
            "networks": {n: d for n, d in a["networks"].items() if n in networks},
            "commission_split": a["commission_split"],
            "endpoint": a["endpoint"],
            "estimated_earnings": estimate_earnings(a, query_text)
        } for a in sorted(matching, key=lambda x: x["commission_split"], reverse=True)]
    })


@app.route("/api/query/self", methods=["POST"])
def self_query():
    """Internal endpoint for fetch-price's own affiliate matching"""
    data = request.get_json()
    query_text = data.get("query", "")
    networks = data.get("networks", ["amazon_uk"])
    
    # Use SearXNG for price research
    results = []
    for network in networks:
        if network == "amazon_uk":
            # Build affiliate link with existing tag
            results.append({
                "network": "amazon_uk",
                "tag": "mindplay0c-21",
                "search_url": f"https://www.amazon.co.uk/s?k={query_text.replace(' ', '+')}&tag=mindplay0c-21",
                "commission_rate": "1-20% depending on category",
                "note": "Direct Amazon search. User clicks through with affiliate tag."
            })
        elif network == "ebay_uk":
            results.append({
                "network": "ebay_uk",
                "campaign_id": "5338712345",
                "search_url": f"https://www.ebay.co.uk/sch/i.html?_nkw={query_text.replace(' ', '+')}&campid=5338712345",
                "commission_rate": "1-6% depending on category"
            })
    
    return jsonify({"results": results, "query": query_text})

# ============================================
# COMMISSION TRACKING
# ============================================

@app.route("/api/sales/report", methods=["POST"])
@require_api_key
def report_sale():
    """Agent reports a sale that came through the marketplace"""
    data = request.get_json()
    
    sale = {
        "id": f"s-{uuid.uuid4().hex[:8]}",
        "query_id": data.get("query_id"),
        "agent_id": request.agent["id"],
        "network": data.get("network"),
        "product": data.get("product"),
        "sale_amount": float(data.get("sale_amount", 0)),
        "commission_rate": float(data.get("commission_rate", 0)),
        "commission_earned": float(data.get("commission_earned", 0)),
        "platform_fee": float(data.get("commission_earned", 0)) * PLATFORM_FEE_PCT,
        "reported": datetime.now().isoformat(),
        "status": "pending_verification"
    }
    
    sales = load_json(SALES_FILE)
    sales.append(sale)
    save_json(SALES_FILE, sales)
    
    return jsonify({
        "sale_id": sale["id"],
        "commission_earned": sale["commission_earned"],
        "platform_fee": round(sale["platform_fee"], 2),
        "your_cut": round(sale["commission_earned"] - sale["platform_fee"], 2)
    }), 201


@app.route("/api/stats", methods=["GET"])
def marketplace_stats():
    """Public stats for the marketplace"""
    agents = load_json(AGENTS_FILE)
    queries = load_json(QUERIES_FILE)
    sales = load_json(SALES_FILE)
    
    return jsonify({
        "agents_active": len([a for a in agents if a["status"] == "active"]),
        "networks_available": list(set(
            net for a in agents if a["status"] == "active"
            for net in a.get("networks", {}).keys()
        )),
        "queries_total": len(queries),
        "sales_total": len(sales),
        "total_commission_tracked": round(sum(s["commission_earned"] for s in sales), 2),
        "platform_version": "1.0.0"
    })

# ---- Helpers ----
def estimate_earnings(agent, query):
    """Estimate potential commission based on agent's networks"""
    total = 0
    for network, cfg in agent.get("networks", {}).items():
        if network.startswith("amazon"):
            total += 0.03  # avg 3% of avg £100 purchase = £3
        elif network.startswith("ebay"):
            total += 0.02
        elif "booking" in network or "travel" in network:
            total += 0.04
    return round(total, 2)

if __name__ == "__main__":
    app.run(port=5100, debug=True)

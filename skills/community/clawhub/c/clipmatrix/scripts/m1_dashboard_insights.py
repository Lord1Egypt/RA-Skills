#!/usr/bin/env python3
"""
M1 Metricool AI Dashboard Insights — 为每个账号获取AI洞察
用法:
  from m1_dashboard_insights import get_all_insights
  insights = get_all_insights(token, uid, accounts)  # {aid: insight_data}
"""

import json, urllib.request, time, logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

API_BASE = "https://app.metricool.com/api"
_BRANDS_CACHE = None  # 缓存Brands API结果


def _req(url, token, method="GET", body=None, timeout=30):
    """封装请求"""
    headers = {"X-Mc-Auth": token, "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read())


def list_dashboards(token: str, uid: str, blog_id: str) -> list:
    """列出某个blog的活跃dashboard"""
    try:
        url = f"{API_BASE}/v2/reporting/campaigns-dashboard?blogId={blog_id}&userId={uid}"
        data = _req(url, token)
        return data.get("data", [])
    except Exception as e:
        logger.warning(f"list_dashboards blog={blog_id}: {e}")
        return []


def get_brand_networks(token: str, uid: str, blog_id: str) -> list:
    """从Brands API获取某个blog的实际连接平台（带缓存）"""
    global _BRANDS_CACHE
    if _BRANDS_CACHE is None:
        url = f"{API_BASE}/v2/settings/brands?userId={uid}"
        data = _req(url, token)
        _BRANDS_CACHE = data.get("data", [])
    
    for b in _BRANDS_CACHE:
        if str(b.get("id")) == str(blog_id):
            nw = b.get("networksData", {})
            nets = []
            if (nw.get("tiktokData") or "").strip():
                nets.append("tiktok")
            if (nw.get("instagramData") or "").strip():
                nets.append("instagram_business")
            return nets
    return ["tiktok"]  # fallback


def create_dashboard(token: str, uid: str, blog_id: str, title: str = None,
                     from_date: str = None, to_date: str = None,
                     networks: list = None) -> dict:
    """创建新的Performance Dashboard"""
    from_dt = from_date or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00")
    to_dt = to_date or datetime.now().strftime("%Y-%m-%dT23:59:59")
    nets = networks or ["tiktok", "instagram_business"]
    
    body = {
        "title": title or "Pandajourneys Auto Dashboard",
        "description": "Auto-generated for AI insights",
        "networks": nets,
        "from": {"dateTime": from_dt, "timezone": "Asia/Shanghai"},
        "to": {"dateTime": to_dt, "timezone": "Asia/Shanghai"},
        "autoCategorize": True,
    }
    
    url = f"{API_BASE}/v2/reporting/campaigns-dashboard?blogId={blog_id}&userId={uid}"
    data = _req(url, token, method="POST", body=body)
    return data.get("data", data)


def get_available_content(token: str, uid: str, blog_id: str, dashboard_id: int) -> list:
    """获取dashboard可用内容"""
    url = f"{API_BASE}/v2/reporting/campaigns-dashboard/{dashboard_id}/available-content?blogId={blog_id}&userId={uid}"
    data = _req(url, token)
    return data.get("data", {}).get("contentItems", [])


def add_content(token: str, uid: str, blog_id: str, dashboard_id: int,
                content_items: list) -> bool:
    """添加内容到dashboard"""
    contents = []
    for item in content_items:
        pub_date = item.get("publicationDate", {})
        contents.append({
            "contentId": item["id"],
            "network": item["network"],
            "type": item.get("type", "VIDEO"),
            "contentDate": {
                "dateTime": pub_date.get("dateTime", ""),
                "timezone": pub_date.get("timezone", "Europe/Madrid"),
            },
            "status": item.get("status", "PUBLISHED"),
        })
    
    body = {"contents": contents, "campaigns": []}
    url = f"{API_BASE}/v2/reporting/campaigns-dashboard/{dashboard_id}/content?blogId={blog_id}&userId={uid}"
    _req(url, token, method="POST", body=body)
    return True


def sync_dashboard(token: str, uid: str, blog_id: str, dashboard_id: int) -> bool:
    """同步dashboard"""
    url = f"{API_BASE}/v2/reporting/campaigns-dashboard/{dashboard_id}/sync?blogId={blog_id}&userId={uid}"
    _req(url, token, method="POST", body={})
    return True


def get_insights(token: str, uid: str, blog_id: str, dashboard_id: int) -> dict:
    """获取AI洞察"""
    url = f"{API_BASE}/v2/reporting/campaigns-dashboard/{dashboard_id}/insights?blogId={blog_id}&userId={uid}"
    data = _req(url, token)
    info = data.get("data", {})
    
    result = {
        "dashboard_id": dashboard_id,
        "status": info.get("status", "UNKNOWN"),
        "insights": None,
    }
    
    if info.get("status") == "COMPLETED" and info.get("content"):
        try:
            result["insights"] = json.loads(info["content"])
        except json.JSONDecodeError:
            result["insights"] = {"raw": info["content"]}
    
    return result


def get_or_create_dashboard(token: str, uid: str, blog_id: str,
                            force_recreate: bool = False) -> dict:
    """
    为一个blog获取或创建dashboard，添加Pandajourneys内容，sync，返回insights
    
    优先策略：
    1. 检查所有已有dashboard，有COMPLETED洞察就直接返回
    2. 尝试复用已有dashboard加内容+sync+等待洞察生成
    3. 都没有才新建
    
    Returns: {"dashboard_id": int, "status": str, "insights": dict|None}
    """
    if force_recreate:
        return _create_new_dashboard(token, uid, blog_id)
    
    dashboards = list_dashboards(token, uid, blog_id)
    
    # ── 第1轮：找已有COMPLETED洞察的dashboard ──
    for d in dashboards:
        title = (d.get("title", "") + d.get("description", "")).lower()
        if "pandajourney" not in title and "panda" not in title:
            continue
        did = d["id"]
        insights = get_insights(token, uid, blog_id, did)
        if insights["status"] == "COMPLETED":
            logger.info(f"  已找到COMPLETED洞察 dashboard={did} blog={blog_id}")
            return insights
    
    # ── 第2轮：复用已有dashboard，sync后等待生成 ──
    for d in dashboards:
        title = (d.get("title", "") + d.get("description", "")).lower()
        if "pandajourney" not in title and "panda" not in title:
            continue
        did = d["id"]
        logger.info(f"  复用dashboard={did}，添加内容+sync...")
        items = get_available_content(token, uid, blog_id, did)
        pj_items = _filter_pandajourneys(items) if items else []
        if pj_items:
            add_content(token, uid, blog_id, did, pj_items)
        sync_dashboard(token, uid, blog_id, did)
        # 轮询等待洞察生成（最多等60秒）
        for _ in range(12):
            time.sleep(5)
            insights = get_insights(token, uid, blog_id, did)
            if insights["status"] == "COMPLETED":
                return insights
            if insights["status"] == "FAILED":
                logger.warning(f"  dashboard={did} 洞察生成失败")
                return insights
        logger.warning(f"  dashboard={did} 洞察生成超时(60s)，status={insights.get('status')}")
        return insights
    
    # ── 第3轮：没有可复用的，新建 ──
    return _create_new_dashboard(token, uid, blog_id)


def _create_new_dashboard(token: str, uid: str, blog_id: str) -> dict:
    """创建新dashboard + 加内容 + sync + 等待洞察"""
    nets = get_brand_networks(token, uid, blog_id)
    logger.info(f"  新建dashboard for blog={blog_id} networks={nets}")
    
    if not nets:
        logger.warning(f"  blog={blog_id} 无可用网络")
        return {"dashboard_id": None, "status": "NO_NETWORKS", "insights": None}
    
    d = create_dashboard(token, uid, blog_id, networks=nets)
    did = d.get("id")
    if not did:
        logger.error(f"  创建dashboard失败: {d}")
        return {"dashboard_id": None, "status": "FAILED", "insights": None}
    
    items = get_available_content(token, uid, blog_id, did)
    pj_items = _filter_pandajourneys(items) if items else []
    if pj_items:
        add_content(token, uid, blog_id, did, pj_items)
    sync_dashboard(token, uid, blog_id, did)
    
    # 轮询等待（最多60秒）
    for _ in range(12):
        time.sleep(5)
        insights = get_insights(token, uid, blog_id, did)
        if insights["status"] in ("COMPLETED", "FAILED"):
            return insights
    
    logger.warning(f"  新建dashboard={did} 洞察超时，返回partial")
    return get_insights(token, uid, blog_id, did)


def _filter_pandajourneys(items: list) -> list:
    """筛选Pandajourneys相关内容"""
    result = []
    for item in items:
        text = (item.get("text", "") or "").lower()
        net = item.get("network", "")
        # IG: #pandajourneys hashtag, TK: 旅游相关
        if "#pandajourneys" in text:
            result.append(item)
        elif net == "tiktok" and any(kw in text for kw in
                                      ["china", "sichuan", "chengdu", "chongqing",
                                       "temple", "mountain", "travel", "trip",
                                       "hik", "lake", "valley"]):
            result.append(item)
    return result


def get_all_insights(token: str, uid: str, accounts: dict,
                     force_recreate: bool = False) -> dict:
    """
    为所有账号获取AI洞察
    
    Args:
        token: Metricool API token
        uid: user_id
        accounts: {aid: {"blog_id": int, "name": str}, ...}
        force_recreate: 是否强制重建dashboard
    
    Returns:
        {aid: {"dashboard_id": int, "status": str, "insights": dict|None}, ...}
    """
    results = {}
    for aid, acc in accounts.items():
        bid = acc.get("blog_id") or acc.get("id")
        if not bid:
            logger.warning(f"  {aid}号 无blog_id, 跳过")
            results[aid] = {"dashboard_id": None, "status": "NO_BLOG_ID", "insights": None}
            continue
        
        try:
            logger.info(f"📊 {aid}号 {acc.get('name','?')} (blog={bid})")
            results[aid] = get_or_create_dashboard(token, uid, str(bid),
                                                   force_recreate=force_recreate)
        except Exception as e:
            logger.warning(f"  {aid}号 失败: {e}")
            results[aid] = {"dashboard_id": None, "status": f"ERROR: {e}", "insights": None}
    
    return results


def format_insights_html(aid: str, account_name: str, insights_data: dict) -> str:
    """将单账号AI洞察格式化为HTML片段"""
    if not insights_data or insights_data.get("status") != "COMPLETED":
        status = (insights_data or {}).get("status", "无数据")
        return f'<p style="color:#888">⏳ {account_name}: AI洞察未生成 ({status})</p>'
    
    content = insights_data.get("insights", {})
    if not content:
        return f'<p style="color:#888">⏳ {account_name}: 洞察内容为空</p>'
    
    html = f'<div style="margin-bottom:16px;padding:12px;background:#1a1a2e;border-radius:8px;border-left:3px solid #FFD700">'
    html += f'<h4 style="margin:0 0 8px;color:#FFD700">🤖 AI洞察 — {account_name}</h4>'
    
    # Executive summary
    exec_sum = content.get("executiveSummary", {})
    if exec_sum.get("summary"):
        html += f'<p style="color:#ccc;font-size:13px;margin:0 0 8px">📋 {exec_sum["summary"][:300]}</p>'
    
    # Per-network insights
    for net, items in content.get("organicNetworks", {}).items():
        net_label = {"tiktok": "📱 TikTok", "instagram_business": "📸 Instagram"}.get(net, net)
        html += f'<p style="color:#888;font-size:12px;margin:8px 0 4px"><b>{net_label}</b></p>'
        for item in items[:3]:
            title = item.get("title", "")
            text = item.get("text", "")[:200]
            html += f'<p style="color:#aaa;font-size:11px;margin:2px 0 2px 8px">• <b>{title}</b>: {text}</p>'
    
    # Best posts patterns
    best = content.get("bestPosts", [])
    if best:
        html += '<p style="color:#888;font-size:12px;margin:8px 0 4px"><b>🏆 爆款模式</b></p>'
        for item in best[:2]:
            text = item.get("text", "")[:200]
            html += f'<p style="color:#aaa;font-size:11px;margin:2px 0 2px 8px">• {text}</p>'
    
    html += '</div>'
    return html


def format_insights_text(aid: str, account_name: str, insights_data: dict) -> str:
    """将单账号AI洞察格式化为纯文本"""
    if not insights_data or insights_data.get("status") != "COMPLETED":
        return f"  {account_name}: 无AI洞察"
    
    content = insights_data.get("insights", {})
    if not content:
        return f"  {account_name}: 空"
    
    lines = [f"🤖 {account_name} AI洞察:"]
    
    exec_sum = content.get("executiveSummary", {}).get("summary", "")
    if exec_sum:
        lines.append(f"  📋 {exec_sum[:200]}")
    
    for net, items in content.get("organicNetworks", {}).items():
        for item in items[:2]:
            lines.append(f"  • [{net}] {item.get('title','')}: {item.get('text','')[:150]}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    # 加载配置
    config_file = os.path.join(os.path.dirname(__file__), "..", "config", "metricool.json")
    with open(config_file) as f:
        cfg = json.load(f)
    
    token = cfg["api_token"]
    uid = str(cfg["user_id"])
    accounts = {aid: {"blog_id": acc["id"], "name": acc.get("label", aid)}
                for aid, acc in cfg["accounts"].items()}
    
    # 测试单个
    test_aid = list(accounts.keys())[0]
    result = get_or_create_dashboard(token, uid, str(accounts[test_aid]["blog_id"]))
    print(json.dumps(result, indent=2, ensure_ascii=False)[:1500])

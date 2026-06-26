# -*- coding: utf-8 -*-
"""酒店比价 v2.3 - 两步式交互（途牛MCP原生搜索 + 5源并发精确比价）
第一步：途牛MCP原生搜索（自动2页合并约16家）→ 代码层评分过滤 → 展示酒店列表 + 智能换条件提示
第二步：用户选定酒店 → 5源并发比价（飞猪+RG detail+途牛多策略+同程+美团）→ 展示各平台价格
v2.3更新：新增美团源（proxy v3.2支持按酒店名搜索），比价改为并发执行提升速度
"""
import argparse, json, re, urllib.request, urllib.error, concurrent.futures
from datetime import datetime, timedelta

PROXY_URL = "https://1439498936-4wdncmn2oj.ap-guangzhou.tencentscf.com"
def _token():
    """代理认证令牌（用于请求OTA平台的代理服务鉴权）"""
    return "tp_8k2mX9vQ4z"

PNAME = {"rg":"RollingGo","tuniu":"途牛","tongcheng":"同程","fliggy":"飞猪","meituan":"美团"}
PORDER = ["rg","fliggy","tuniu","tongcheng","meituan"]
# 佣金优先级：RG(5%) > 飞猪(推广者计划) > 途牛 > 同程 > 美团
COMMISSION_PRIORITY = {"rg": 0, "fliggy": 1, "tuniu": 2, "tongcheng": 3, "meituan": 4}

AREA_HINTS = {
    "上海": ["外滩","陆家嘴","南京路","人民广场","虹桥","徐家汇","迪士尼","静安寺","新天地"],
    "北京": ["三里屯","国贸","王府井","西单","望京","中关村","前门","天安门","鸟巢"],
    "杭州": ["西湖","武林广场","钱江新城","萧山","滨江","灵隐寺","千岛湖"],
    "成都": ["春熙路","天府广场","宽窄巷子","武侯祠","锦里","太古里"],
    "广州": ["天河","珠江新城","北京路","越秀","白云","番禺"],
    "深圳": ["福田","南山","罗湖","华侨城","蛇口","宝安"],
    "三亚": ["亚龙湾","海棠湾","大东海","三亚湾","天涯海角"],
    "南京": ["新街口","夫子庙","玄武湖","中山陵","河西","仙林"],
}

# ===== 代理调用 =====
def _proxy(source, params, timeout=30):
    body = json.dumps({"source": source, "params": params}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": _token()},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"code": 500, "error": str(e)}

def _mcp_result(result):
    if "error" in result:
        return {"error": str(result.get("error", ""))[:200]}
    content = result.get("result", {}).get("content", [])
    if content and isinstance(content, list) and len(content) > 0:
        f = content[0]
        if isinstance(f, dict) and f.get("type") == "text":
            t = f.get("text", "")
            if "Error executing tool" in t:
                return {"error": t[:200]}
            try:
                return json.loads(t)
            except:
                return {"raw_text": t}
    sc = result.get("result", {}).get("structuredContent")
    if sc:
        return sc
    return {"error": "无法解析响应"}

def _parse(resp):
    if resp.get("code") != 0:
        return {"error": resp.get("error", "代理请求失败")[:200]}
    data = resp.get("data", "")
    ct = resp.get("content_type", "")
    err = resp.get("error")
    if err:
        return {"error": str(err)[:200]}
    if not data:
        return {"error": "数据为空"}
    try:
        if isinstance(data, dict):
            return data
        parsed = json.loads(data) if isinstance(data, str) else data
        if "text/event-stream" in ct:
            if isinstance(parsed, str):
                for line in parsed.split("\n"):
                    if line.startswith("data:"):
                        return _mcp_result(json.loads(line[5:].strip()))
            return _mcp_result(parsed)
        if isinstance(parsed, dict):
            if "result" in parsed or "error" in parsed:
                return _mcp_result(parsed)
            return parsed
        return {"error": "解析失败"}
    except:
        return {"error": "JSON解析失败"}

def _clean(name):
    """清理酒店名：去英文括号内容，保留中文括号和·"""
    name = re.sub(r'\s*\([A-Za-z][^)]*\)', '', name).strip()
    while name and name[-1] in ')）':
        if (name.count('(') + name.count('（')) < (name.count(')') + name.count('）')):
            name = name[:-1].rstrip()
        else:
            break
    return name.strip()

# ===== 第一步：途牛MCP原生搜索（自动2页） =====
def _tuniu_browse(city, ci, co, kw, max_price, poi_name, min_score):
    """途牛MCP原生酒店搜索，自动查2页合并，代码层过滤评分"""
    params = {"city": city, "check_in": ci, "check_out": co}
    if kw and kw != "None": params["keyword"] = kw
    if poi_name and poi_name != "None": params["poiName"] = poi_name
    if max_price and max_price > 0: params["prices"] = f"0-{max_price}"

    # 第1页
    resp1 = _proxy("tuniu", params)
    data1 = _parse(resp1)
    if "error" in data1:
        return [], 0
    qid1 = data1.get("queryId", "")
    hl1 = data1.get("hotels") or data1.get("hotelList") or (data1 if isinstance(data1, list) else [])
    if not isinstance(hl1, list):
        hl1 = []

    # 第2页
    hl2 = []
    if qid1 and len(hl1) >= 6:
        params2 = dict(params)
        params2["pageNum"] = "2"
        params2["queryId"] = qid1
        resp2 = _proxy("tuniu", params2)
        data2 = _parse(resp2)
        if "hotels" in data2 or "hotelList" in data2:
            hl2 = data2.get("hotels") or data2.get("hotelList") or []
            if not isinstance(hl2, list):
                hl2 = []

    # 合并去重
    all_raw = hl1 + hl2
    seen_ids = set()
    hotels = []
    total_before_filter = 0
    for h in all_raw[:40]:
        hotel_id = str(h.get("hotelId", ""))
        if hotel_id and hotel_id in seen_ids:
            continue
        if hotel_id:
            seen_ids.add(hotel_id)
        name = _clean(h.get("hotelName") or h.get("name", ""))
        if not name:
            continue
        try:
            p = float(re.sub(r"[^\d.]", "", str(h.get("lowestPrice") or h.get("price") or "0")))
        except:
            p = 0
        if p <= 0:
            continue
        score = h.get("commentScore")
        try:
            score = float(score) if score else 0
        except:
            score = 0
        total_before_filter += 1
        # 评分过滤
        if min_score and min_score > 0 and score > 0 and score < min_score:
            continue
        url = h.get("detailUrl") or h.get("url", "")
        if not url and hotel_id:
            url = f"https://hotel.tuniu.com/detail/{hotel_id}"
        hotels.append({
            "name": name, "price": p,
            "address": h.get("address") or h.get("hotelAddress", ""),
            "star": h.get("starName") or h.get("star", ""),
            "source": "tuniu", "url": url,
            "brand": h.get("brandName") or "",
            "score": score,
            "distance": h.get("distance") or "",
            "meal": h.get("meal") or "",
            "room_name": h.get("roomName") or "",
            "room_window": h.get("roomWindow") or "",
            "refund": h.get("refund") or "",
            "comment_digest": h.get("commentDigest") or "",
            "pic": h.get("firstPic") or "",
            "hotel_id": hotel_id,
        })
    return hotels, total_before_filter

# ===== 第二步：5源并发精确比价 =====
def _call_fg(city, ci, co, kw):
    """飞猪：keyword精准过滤，搜酒店名最稳"""
    resp = _proxy("fliggy", {"city": city, "check_in": ci, "check_out": co, "keyword": kw or ""})
    data = _parse(resp)
    if "error" in data:
        return []
    hl = data if isinstance(data, list) else data.get("hotels") or data.get("hotelList") or []
    if not isinstance(hl, list):
        return []
    hotels = []
    for h in hl[:20]:
        name = _clean(h.get("name") or h.get("hotelName", ""))
        if not name:
            continue
        try:
            p = float(re.sub(r"[^\d.]", "", str(h.get("price") or h.get("lowestPrice") or "0")))
        except:
            p = 0
        if p <= 0:
            continue
        hotels.append({
            "name": name, "price": p,
            "address": h.get("address", ""),
            "star": h.get("star", ""),
            "source": "fliggy",
            "url": h.get("detailUrl") or h.get("url", ""),
            "brand": h.get("brandName") or "",
        })
    return hotels

def _call_rg_detail(name, ci, co):
    """RG：hotel_detail按名查，比价首选"""
    resp = _proxy("rg_detail", {"name": name, "check_in": ci, "check_out": co})
    data = _parse(resp)
    if "error" in data or "roomRatePlans" not in data:
        return None
    plans = data.get("roomRatePlans", [])
    prices = []
    for plan in plans:
        tp = plan.get("totalPrice")
        if tp:
            try:
                prices.append(float(tp))
            except:
                pass
    if not prices:
        return None
    booking_url = data.get("bookingUrl", "")
    hotel_id = data.get("hotelId", "")
    if not booking_url and hotel_id:
        booking_url = f"https://rollinggo.cn/pages/hotel/detail/index?id={hotel_id}"
    return {"name": _clean(data.get("name", name)), "price": min(prices),
            "url": booking_url, "source": "rg"}

def _call_tn_compare(city, ci, co, target_name, target_brand):
    """途牛比价：多策略（酒店名→品牌→地址路名）"""
    strategies = []
    strategies.append({"keyword": target_name})
    if target_brand and len(target_brand) >= 2:
        strategies.append({"keyword": target_brand})
    # 地址路名
    road = re.search(r'[\u4e00-\u9fff]{2,4}[路街道]', target_name)
    if road:
        strategies.append({"keyword": road.group()})

    for s in strategies:
        resp = _proxy("tuniu", {"city": city, "check_in": ci, "check_out": co, **s})
        data = _parse(resp)
        if "error" in data:
            continue
        hl = data.get("hotels") or data.get("hotelList") or (data if isinstance(data, list) else [])
        if not isinstance(hl, list):
            continue
        for h in hl[:15]:
            hname = _clean(h.get("hotelName") or h.get("name", ""))
            if not hname:
                continue
            # 名字相似度判断
            if _name_match(target_name, hname):
                try:
                    p = float(re.sub(r"[^\d.]", "", str(h.get("lowestPrice") or h.get("price") or "0")))
                except:
                    p = 0
                if p <= 0:
                    continue
                hotel_id = str(h.get("hotelId", ""))
                url = h.get("detailUrl") or h.get("url", "")
                if not url and hotel_id:
                    url = f"https://hotel.tuniu.com/detail/{hotel_id}"
                return {"name": hname, "price": p, "source": "tuniu", "url": url}
    return None

def _call_tc_compare(city, ci, co, target_name):
    """同程比价：keyword搜酒店名"""
    resp = _proxy("tongcheng", {"city": city, "check_in": ci, "check_out": co, "keyword": target_name})
    data = _parse(resp)
    raw = resp.get("data", "")
    ct = resp.get("content_type", "")
    if isinstance(raw, str) and raw:
        try:
            result = json.loads(raw)
            if result.get("code") == "0":
                text = result.get("data", {}).get("text", "")
                links = result.get("data", {}).get("产品跳转链接", {})
                pats = [
                    re.compile(r'^([^，。\n]+?)\s+距[\u4e00-\u9fff]+直线\d+[米公里]*，\s*评分[\s：:]*(\d+\.?\d*)[，,]?\s*价格[\s：:]*(\d+[\d,.]*)\s*元', re.M),
                    re.compile(r'^([^，。\n]+?)\s+.*?评分[\s：:]*(\d+\.?\d*).*?价格[\s：:]*(\d+[\d,.]*)\s*元', re.M),
                    re.compile(r'^([^，。\n]+?)\s+.*?价格[\s：:]*(\d+[\d,.]*)\s*元', re.M),
                ]
                for para in text.split("\n\n"):
                    para = para.strip()
                    if not para or any(s in para for s in ["出行建议", "客服电话", "建议入住"]):
                        continue
                    for pat in pats:
                        m = pat.match(para)
                        if m:
                            hname = _clean(m.group(1).strip())
                            if _name_match(target_name, hname):
                                try:
                                    pv = float(m.group(m.lastindex).replace(",", ""))
                                except:
                                    pv = 0
                                if pv > 0:
                                    url = ""
                                    for lk, ld in links.items():
                                        if hname in lk or lk in hname:
                                            url = (ld.get("手机链接") or ld.get("PC链接", "")) if isinstance(ld, dict) else ""
                                            break
                                    return {"name": hname, "price": pv, "source": "tongcheng", "url": url}
            # JSON-RPC MCP格式
            result_obj = json.loads(raw) if isinstance(raw, str) else raw
            content = result_obj.get("result", {}).get("content", [])
            if content:
                text = content[0].get("text", "")
                parsed = json.loads(text) if text else {}
                if isinstance(parsed, list):
                    for h in parsed:
                        hname = h.get("name") or h.get("hotelName", "")
                        if _name_match(target_name, _clean(hname)):
                            p = h.get("price") or h.get("lowestPrice", 0)
                            try:
                                p = float(re.sub(r"[^\d.]", "", str(p)))
                            except:
                                p = 0
                            if p > 0:
                                return {"name": _clean(hname), "price": p, "source": "tongcheng", "url": h.get("url", "")}
        except:
            pass
    return None

def _call_mt_compare(city, target_name):
    """美团比价：按酒店名+城市搜索，proxy端内置重试"""
    resp = _proxy("meituan", {"city": city, "query": target_name}, timeout=60)
    if resp.get("code") != 0:
        return None
    data = resp.get("data", "")
    # proxy返回 {"code":0,"data":{"code":0,"msg":"success","data":"...markdown..."},...}
    if isinstance(data, dict):
        inner = data.get("data", "")
        if isinstance(inner, str) and inner:
            text = inner
        elif isinstance(data, str):
            text = data
        else:
            return None
    elif isinstance(data, str):
        text = data
    else:
        return None

    # 从markdown文本中提取酒店名+价格+链接
    # 格式：[**酒店名**](url) ... ￥XXX起
    p1 = re.compile(r'\[\*\*(.+?)\*\*\]\(([^)]+)\).*?￥(\d{3,}[\d,.]*)\s*(?:起|/晚|共)', re.DOTALL)
    for m in p1.finditer(text):
        hname = _clean(m.group(1).replace("\\(", "(").replace("\\)", ")"))
        if not hname:
            continue
        if _name_match(target_name, hname):
            try:
                p = float(m.group(3).replace(",", ""))
            except:
                continue
            if p > 0:
                return {"name": hname, "price": p, "source": "meituan", "url": m.group(2).strip()}

    # 备用正则：没有链接的格式 **酒店名** ... ￥XXX起
    p2 = re.compile(r'\*\*(.+?)\*\*[^￥]*?￥(\d{3,}[\d,.]*)\s*(?:起|/晚|共)', re.DOTALL)
    for m in p2.finditer(text):
        hname = _clean(m.group(1).replace("\\(", "(").replace("\\)", ")"))
        if not hname:
            continue
        if _name_match(target_name, hname):
            try:
                p = float(m.group(2).replace(",", ""))
            except:
                continue
            if p > 0:
                # 尝试提取dpurl链接
                url = ""
                url_m = re.search(r'(https?://dpurl\.cn/[^\s)）]+)', text)
                if url_m:
                    url = url_m.group(1)
                return {"name": hname, "price": p, "source": "meituan", "url": url}

    return None

def _name_match(target, candidate, threshold=0.4):
    """简单名字匹配"""
    t, c = target.lower(), candidate.lower()
    if t == c or t in c or c in t:
        return True
    # 去括号后比较
    t_clean = re.sub(r'[\(（][^)）]*[\)）]', '', t).strip()
    c_clean = re.sub(r'[\(（][^)）]*[\)）]', '', c).strip()
    if t_clean and c_clean and (t_clean in c_clean or c_clean in t_clean):
        return True
    # 品牌匹配
    brand_list = ["华尔道夫","威斯汀","丽思卡尔顿","索菲特","全季","亚朵","桔子","如家","汉庭","丽枫","希尔顿","万豪","喜来登","洲际","皇冠假日","JW万豪","W酒店","半岛","四季","凯悦","铂尔曼"]
    for b in brand_list:
        if b in t and b in c:
            return True
    return False

# ===== 智能提示 =====
def _smart_tips(hotels, city, kw, max_price, poi_name, min_score, total_before_filter):
    """根据搜索结果数量，给出调主轴（换区域）或调筛子（价格/评分）的建议"""
    tips = []
    n = len(hotels)
    areas = AREA_HINTS.get(city, [])
    nearby = [a for a in areas if a != (kw or "") and a != (poi_name or "")][:2]

    if n == 0:
        if min_score and min_score > 0:
            tips.append(f"💡 去掉评分限制，或降低评分要求（当前≥{min_score}分）")
        if max_price and max_price > 0:
            tips.append(f"💡 提高价格上限（当前≤¥{max_price}），或去掉价格限制")
        if not min_score and not max_price:
            tips.append("💡 去掉筛选条件，扩大搜索范围")
        if nearby:
            tips.append(f"💡 换个区域试试：{nearby[0]}、{nearby[1]}")
        if kw and len(kw) <= 3:
            tips.append(f"💡 关键词范围放大：\"{kw}\"→\"{city}\"")
    elif n <= 3:
        if min_score and min_score > 0:
            tips.append(f"💡 降低评分要求（当前≥{min_score}分）")
        if max_price and max_price > 0:
            tips.append(f"💡 提高价格上限（当前≤¥{max_price}）")
        if not min_score and not max_price:
            tips.append("💡 可以加价格或评分要求，缩小范围精选")
        if nearby:
            tips.append(f"💡 换个区域：{nearby[0]}、{nearby[1]}")
    else:
        if not max_price and not min_score:
            tips.append("📌 没找到心仪的？可以：限价（告诉我预算，如\"1000以内\"）、限评分（如\"4.5分以上\"）、或换个区域")
        elif nearby:
            tips.append(f"📌 没找到心仪的？可以换个区域：{nearby[0]}、{nearby[1]}")

    return tips

# ===== 展示格式 =====
def _safe_score(h):
    try:
        return float(h.get("score", 0) or 0)
    except:
        return 0

def _price_overview(hotels):
    if not hotels:
        return ""
    prices = [h["price"] for h in hotels if h["price"] > 0]
    if not prices:
        return ""
    lo, hi = int(min(prices)), int(max(prices))
    avg = int(sum(prices) / len(prices))
    scores = [_safe_score(h) for h in hotels if _safe_score(h) >= 4.5]
    parts = [f"💰 ¥{lo}~¥{hi} | 均价¥{avg}"]
    if scores:
        parts.append(f"4.5分以上{len(scores)}家")
    return " | ".join(parts)

def _format_browse(hotels, city, ci, co, kw, max_price, poi_name, min_score, total_before_filter):
    """第一步：浏览模式，展示途牛酒店列表"""
    dest = f"{city}{kw}" if kw else city
    lines = [f"🏨 **{dest}** 酒店浏览（{ci}~{co}）"]
    lines.append("")
    lines.append("⚠️ **以上为浏览价格，尚未比价！选定酒店后告诉我酒店名（如\"第2家\"或酒店全名），立刻启动多旅游平台比价，帮您找到全网最低价！**")
    lines.append("")
    if min_score and min_score > 0 and len(hotels) < total_before_filter:
        lines.append(f"📊 途牛为您找到{total_before_filter}家酒店，评分≥{min_score}分筛选后{len(hotels)}家")
    else:
        lines.append(f"📊 途牛为您找到{len(hotels)}家酒店")
    lines.append(_price_overview(hotels))
    lines.append("")
    for i, h in enumerate(hotels[:16], 1):
        star_str = f" · {h['star']}" if h.get("star") else ""
        score_str = f" · {h['score']}分" if _safe_score(h) > 0 else ""
        brand_str = f" · {h['brand']}" if h.get("brand") else ""
        dist_str = f" · {h['distance']}" if h.get("distance") else ""
        meal_str = ""
        if h.get("meal") and "无" not in str(h["meal"]):
            meal_str = f" · 🍽️{h['meal']}"
        window_str = ""
        if h.get("room_window") and "无" not in str(h["room_window"]):
            window_str = f" · 🪟{h['room_window']}"
        refund_str = ""
        if h.get("refund") and "不可" not in str(h["refund"]):
            refund_str = f" · ↩️可取消"

        url = h.get("url", "")
        link = f" [查看→]({url})" if url else ""
        lines.append(f"**{i}. {h['name']}**{star_str}{score_str}")
        detail_parts = [f"¥{int(h['price'])}起"]
        if brand_str:
            detail_parts.append(brand_str.strip(" · "))
        if dist_str:
            detail_parts.append(dist_str.strip(" · "))
        if meal_str:
            detail_parts.append(meal_str.strip(" · "))
        if window_str:
            detail_parts.append(window_str.strip(" · "))
        if refund_str:
            detail_parts.append(refund_str.strip(" · "))
        lines.append(f"   途牛 {' | '.join(detail_parts)}{link}")
        if h.get("comment_digest"):
            lines.append(f"   💬 {h['comment_digest'][:40]}")
        lines.append("")

    # 智能换条件提示
    tips = _smart_tips(hotels, city, kw, max_price, poi_name, min_score, total_before_filter)
    for tip in tips:
        lines.append(tip)
    if tips:
        lines.append("")

    lines.append('⚠️ **尚未比价！告诉我酒店名（如"第3家"或酒店全名），立刻启动5源比价！**')
    return "\n".join(lines)

def _format_compare(target_name, results, city, ci, co):
    """第二步：比价模式，展示5源比价结果"""
    lines = [f"💰 **{target_name}** 多旅游平台比价（{ci}~{co}）"]
    lines.append("")

    # results: {"rg": result, "fliggy": result, "tuniu": result, "tongcheng": result, "meituan": result}
    found = []
    for src in PORDER:
        r = results.get(src)
        if r:
            found.append((src, r))

    if not found:
        lines.append("❌ 所有平台均未找到该酒店，建议换关键词重试")
        return "\n".join(lines)

    # 按价格排序，同价按佣金优先级
    found.sort(key=lambda x: (x[1]["price"] if x[1]["price"] > 0 else 99999, COMMISSION_PRIORITY.get(x[0], 99)))

    lines.append(f"📊 {len(found)}家平台有报价，价格从低到高：")
    lines.append("")

    min_price = found[0][1]["price"] if found else 0
    for i, (src, h) in enumerate(found):
        p = int(h["price"])
        name_str = PNAME.get(src, src)
        url = h.get("url", "")
        diff_str = ""
        if p > min_price:
            diff_str = f"（贵¥{p - int(min_price)}）"
        if i == 0:
            label = f"💰 **{name_str} ¥{p}最低价**"
            link = f" [去预订→]({url})" if url else ""
            if len(found) > 1:
                second_p = found[1][1]["price"]
                label += f"（比次低省¥{int(second_p) - p}）"
            lines.append(f"{label}{link}")
        else:
            link = f" [去预订→]({url})" if url else ""
            lines.append(f" {name_str} ¥{p}{diff_str}{link}")

    lines.append("")
    lines.append("💡 价格实时变动，以实际预订为准")
    return "\n".join(lines)

# ===== 主入口 =====
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--check-in", default="")
    parser.add_argument("--check-out", default="")
    parser.add_argument("--keyword", default="")
    parser.add_argument("--hotel-name", default="")
    parser.add_argument("--max-price", type=int, default=0)
    parser.add_argument("--poi-name", default="")
    parser.add_argument("--min-score", type=float, default=0)
    args = parser.parse_args()

    city = args.city
    ci = args.check_in
    co = args.check_out
    kw = args.keyword if args.keyword and args.keyword != "None" else ""
    hotel_name = args.hotel_name if args.hotel_name and args.hotel_name != "None" else ""
    mp = args.max_price or 0
    poi_name = args.poi_name if args.poi_name and args.poi_name != "None" else ""
    ms = args.min_score or 0

    # 默认日期
    if not ci or ci == "None":
        ci = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not co or co == "None":
        co = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    try:
        d1 = datetime.strptime(ci, "%Y-%m-%d")
        d2 = datetime.strptime(co, "%Y-%m-%d")
        if d1 < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            print(f"❌ 入住日期{ci}已过期"); return
        if d2 <= d1:
            print(f"❌ 离店日期({co})必须晚于入住日期({ci})"); return
    except ValueError:
        print("❌ 日期格式不正确，请使用YYYY-MM-DD格式"); return

    if hotel_name:
        # ========== 第二步：5源并发比价 ==========
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            fut_rg = ex.submit(_call_rg_detail, hotel_name, ci, co)
            fut_tn = ex.submit(_call_tn_compare, city, ci, co, hotel_name, "")
            fut_fg = ex.submit(_call_fg, city, ci, co, hotel_name)
            fut_tc = ex.submit(_call_tc_compare, city, ci, co, hotel_name)
            fut_mt = ex.submit(_call_mt_compare, city, hotel_name)

            try: results["rg"] = fut_rg.result(timeout=40)
            except: pass
            try: results["tuniu"] = fut_tn.result(timeout=40)
            except: pass
            try:
                fg_list = fut_fg.result(timeout=40)
                for h in fg_list:
                    if _name_match(hotel_name, h["name"]):
                        results["fliggy"] = h
                        break
            except: pass
            try: results["tongcheng"] = fut_tc.result(timeout=40)
            except: pass
            try: results["meituan"] = fut_mt.result(timeout=70)
            except: pass

        print(_format_compare(hotel_name, results, city, ci, co))
    else:
        # ========== 第一步：途牛MCP原生浏览（自动2页） ==========
        hotels, total_before_filter = _tuniu_browse(city, ci, co, kw, mp, poi_name, ms)
        if not hotels:
            tips = _smart_tips([], city, kw, mp, poi_name, ms, total_before_filter)
            lines = [f"❌ 未找到{city}{kw}的酒店"]
            for tip in tips:
                lines.append(tip)
            print("\n".join(lines))
        else:
            print(_format_browse(hotels, city, ci, co, kw, mp, poi_name, ms, total_before_filter))

if __name__ == "__main__":
    main()

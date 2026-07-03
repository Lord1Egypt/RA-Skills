# -*- coding: utf-8 -*-
"""
酒店比价 v3.6-final - CH平台独立脚本
融合v3.5搜索策略 + v3.3展示策略

搜索层：途牛多轮区域搜索（纯城市→区域关键词补充）+ 搜索层价格过滤（prices参数）
展示层：按价格三等分 + 图片 + 每档5家 + 智能引导
比价层：5源并发（飞猪+RG+途牛+美团+同程），同程传keyword精确匹配
数据解析：纯dict模式（代理返回application/json，无需MCP/SSE解析）
"""
import argparse, json, re, concurrent.futures, urllib.request, urllib.error
from datetime import datetime, timedelta

PROXY_URL = "https://1439498936-4wdncmn2oj.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

PNAME = {"rg": "RollingGo", "tuniu": "途牛", "tongcheng": "同程", "fliggy": "飞猪", "meituan": "美团"}
PORDER = ["rg", "fliggy", "tuniu", "meituan", "tongcheng"]
COMMISSION_PRIORITY = {"rg": 0, "fliggy": 1, "tuniu": 2, "meituan": 3, "tongcheng": 4}

AREA_HINTS = {
    "上海": ["外滩", "陆家嘴", "南京路", "人民广场", "虹桥", "徐家汇", "迪士尼", "静安寺", "新天地"],
    "北京": ["三里屯", "国贸", "王府井", "西单", "望京", "中关村", "前门", "天安门", "鸟巢"],
    "杭州": ["西湖", "武林广场", "钱江新城", "萧山", "滨江", "灵隐寺", "千岛湖"],
    "成都": ["春熙路", "天府广场", "宽窄巷子", "武侯祠", "锦里", "太古里"],
    "广州": ["天河", "珠江新城", "北京路", "越秀", "白云", "番禺"],
    "深圳": ["福田", "南山", "罗湖", "华侨城", "蛇口", "宝安"],
    "三亚": ["亚龙湾", "海棠湾", "大东海", "三亚湾", "天涯海角"],
    "南京": ["新街口", "夫子庙", "玄武湖", "中山陵", "河西", "仙林"],
}

MIN_HOTEL_COUNT = 15


# ===== 代理调用与数据解析 =====
def _proxy(source, params, timeout=30):
    body = json.dumps({"source": source, "params": params}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"code": 500, "error": str(e)}


def _get_data(resp):
    """纯dict解析——代理返回application/json，data直接是dict"""
    if resp.get("code") != 0:
        return {"error": resp.get("error", "代理请求失败")[:200]}
    if resp.get("error"):
        return {"error": str(resp["error"])[:200]}
    data = resp.get("data")
    if data is None:
        return {"error": "数据为空"}
    # data可能是str或dict，兼容两种
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            return {"error": "JSON解析失败"}
    return data


def _clean(name):
    """清理酒店名：去英文括号内容，保留中文括号和·"""
    name = re.sub(r'\s*\([^)]*\)', '', name).strip()
    while name and name[-1] in ')）':
        if (name.count('(') + name.count('（')) < (name.count(')') + name.count('）')):
            name = name[:-1].rstrip()
        else:
            break
    return name.strip()


def _clean_tc_url(raw_url):
    """精简同程链接：去掉无用的 a=b 参数和重复的小写 refid"""
    if not raw_url:
        return ""
    url = raw_url.replace("a=b&", "")
    # 去掉重复的小写 &refid=（保留大写的 &refId=）
    url = re.sub(r'&refid=\d+$', '', url)
    return url


# ===== 第一步：途牛多轮区域搜索 =====
def _tuniu_single_search(city, ci, co, kw="", poi_name="", max_price=0):
    """单次途牛搜索（含2页翻页），返回原始酒店列表"""
    params = {"city": city, "check_in": ci, "check_out": co}
    if kw:
        params["keyword"] = kw
    if poi_name:
        params["poiName"] = poi_name
    if max_price and max_price > 0:
        params["prices"] = f"0-{max_price}"

    all_raw = []
    query_id = ""

    for page in range(1, 3):  # 最多2页
        if page > 1:
            if not query_id:
                break
            params["pageNum"] = str(page)
            params["queryId"] = query_id

        resp = _proxy("tuniu", params)
        data = _get_data(resp)
        if "error" in data:
            break

        if page == 1:
            query_id = data.get("queryId", "")

        hl = data.get("hotels") or data.get("hotelList") or []
        if not isinstance(hl, list) or not hl:
            break

        all_raw.extend(hl)
        if len(hl) < 4:
            break

    return all_raw


def _structurize(raw_list):
    """将途牛原始数据转为结构化酒店列表"""
    hotels = []
    for h in raw_list:
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
        # 途牛H5详情页链接：m.tuniu.com/hotel/detail/{hotelId}
        hotel_id = h.get("hotelId", "")
        url = f"https://m.tuniu.com/hotel/detail/{hotel_id}" if hotel_id else ""
        hotels.append({
            "name": name, "price": p,
            "address": h.get("address") or h.get("hotelAddress", ""),
            "star": h.get("starName") or h.get("star", ""),
            "source": "tuniu", "url": url,
            "brand": h.get("brandName") or "",
            "score": score,
            "business": h.get("business") or "",
            "meal": h.get("meal") or "",
            "room_window": h.get("roomWindow") or "",
            "refund": h.get("refund") or "",
            "comment_digest": h.get("commentDigest") or "",
            "image": h.get("firstPic") or "",
            "hotel_id": hotel_id,
        })
    return hotels


def _tuniu_browse(city, ci, co, kw, max_price, poi_name):
    """途牛多轮区域搜索：纯城市→区域补充，凑够15家"""
    # 用户有明确搜索意图（kw/poi_name），只搜一次
    if kw or poi_name:
        raw = _tuniu_single_search(city, ci, co, kw, poi_name, max_price)
        hotels = _structurize(raw)
        return hotels, len(hotels)

    # 无明确意图：纯城市搜索 + 区域关键词补充
    all_raw = _tuniu_single_search(city, ci, co, "", "", max_price)
    areas_tried = []

    if len(all_raw) < MIN_HOTEL_COUNT:
        areas = AREA_HINTS.get(city, [])
        for area in areas:
            if len(all_raw) >= MIN_HOTEL_COUNT * 1.5:
                break
            extra_raw = _tuniu_single_search(city, ci, co, area, "", max_price)
            all_raw.extend(extra_raw)
            areas_tried.append(area)

    # 去重（按名称相似度）+ 结构化
    seen_names = []
    unique_raw = []
    for h in all_raw:
        name = _clean(h.get("hotelName") or h.get("name", ""))
        if not name:
            continue
        is_dup = False
        for sn in seen_names:
            if _name_sim(name, sn) >= 0.7:
                is_dup = True
                break
        if not is_dup:
            seen_names.append(name)
            unique_raw.append(h)

    hotels = _structurize(unique_raw)
    return hotels, len(hotels)


def _classify_by_price(hotels):
    """按价格三等分，返回(低价档, 中价档, 高价档)
    先去掉最高/最低各5%的极端值再分档，避免异常价格拉偏"""
    if not hotels:
        return [], [], []
    sorted_hotels = sorted(hotels, key=lambda h: h["price"])
    n = len(sorted_hotels)
    # 去掉极端值（最少保留10家才去，否则不去）
    if n >= 10:
        trim = max(1, n // 20)  # 5%
        core = sorted_hotels[trim:n - trim]
    else:
        core = sorted_hotels
    n2 = len(core)
    idx1 = n2 // 3
    idx2 = 2 * n2 // 3
    return core[:idx1], core[idx1:idx2], core[idx2:]


def _limit_brand(tier_hotels, max_count=5, max_per_brand=2):
    """从分档酒店中取最多max_count家，同品牌不超过max_per_brand家
    如果限制后不够max_count，放宽品牌限制补位"""
    result = []
    skipped = []
    brand_count = {}
    for h in tier_hotels:
        if len(result) >= max_count:
            break
        brand = h.get("brand", "") or _extract_brand(h.get("name", ""))
        if not brand:
            result.append(h)
            continue
        cnt = brand_count.get(brand, 0)
        if cnt < max_per_brand:
            result.append(h)
            brand_count[brand] = cnt + 1
        else:
            skipped.append(h)
    # 不够的话用被限制的品牌补位
    for h in skipped:
        if len(result) >= max_count:
            break
        result.append(h)
    return result


# ===== 智能引导语 =====
def _smart_tips(keyword, max_price, min_score, city, poi_name=""):
    has_budget = max_price and max_price > 0
    has_score = min_score and min_score > 0
    has_area = False
    areas = AREA_HINTS.get(city, [])
    if keyword:
        for area in areas:
            if area in keyword:
                has_area = True
                break
    if poi_name:
        for area in areas:
            if area in poi_name:
                has_area = True
                break
    suggestions = []
    if not has_area and areas:
        nearby = [a for a in areas if a != (keyword or "") and a != (poi_name or "")][:2]
        if nearby:
            suggestions.append(f"区域/地标（如{'、'.join(nearby)}）")
    if not has_budget:
        suggestions.append("预算（如500以内）")
    if not has_score:
        suggestions.append("评分（如4.8分以上）")
    tips = []
    if suggestions:
        tips.append("💡 告诉我更具体的" + "、".join(suggestions) + "，帮你精确筛选")
    return tips


# ===== 浏览展示（价格分档+图片） =====
def _format_browse(hotels, city, ci, co, kw, max_price, min_score, poi_name, total_before_filter):
    dest = f"{city}{kw}" if kw else city

    low, mid, high = _classify_by_price(hotels)
    for tier in [low, mid, high]:
        tier.sort(key=lambda h: h.get("score", 0), reverse=True)
    low_display = _limit_brand(low, 5, 2)
    mid_display = _limit_brand(mid, 5, 2)
    high_display = _limit_brand(high, 5, 2)

    total = len(hotels)
    if total == 0:
        tips = _smart_tips(kw, max_price, min_score, city, poi_name)
        msg = f"❌ 未找到{dest}的酒店"
        if tips:
            msg += "\n\n" + "\n".join(tips)
        return msg

    all_prices = [h["price"] for h in hotels]
    min_p, max_p = int(min(all_prices)), int(max(all_prices))

    filter_parts = []
    if max_price and max_price > 0:
        filter_parts.append(f"¥{int(max_price)}以内")
    if min_score and min_score > 0:
        filter_parts.append(f"评分{min_score}+")
    if kw:
        filter_parts.append(kw)
    if poi_name:
        filter_parts.append(f"附近{poi_name}")
    filter_str = " · ".join(filter_parts) if filter_parts else ""

    lines = [f"🏨 **{dest}** 酒店浏览（{ci}~{co}）"]
    if filter_str:
        lines.append(f"🔍 筛选条件：{filter_str}")
    display_count = len(low_display) + len(mid_display) + len(high_display)
    if min_score and min_score > 0 and total < total_before_filter:
        lines.append(f"📊 途牛为您找到{total_before_filter}家酒店，评分≥{min_score}分筛选后{total}家，精选{display_count}家推荐 | 💰 ¥{min_p}~¥{max_p}")
    elif display_count < total:
        lines.append(f"📊 途牛为您找到{total}家酒店，精选{display_count}家推荐 | 💰 ¥{min_p}~¥{max_p}")
    else:
        lines.append(f"📊 途牛为您找到{total}家酒店 | 💰 ¥{min_p}~¥{max_p}")
    lines.append("")

    lines.append("⚠️ **以上为浏览价格，尚未比价！选定酒店后告诉我酒店名或序号，立刻启动5大平台比价！**")
    lines.append("")

    global_idx = 0
    tiers_display = [
        ("💰 经济实惠", low_display),
        ("💎 舒适优选", mid_display),
        ("🏆 高端品质", high_display),
    ]

    for tier_label, tier_hotels in tiers_display:
        if not tier_hotels:
            continue
        tier_count = len(tier_hotels)
        tier_prices = [h["price"] for h in tier_hotels]
        tier_min = int(min(tier_prices)) if tier_prices else 0
        tier_max = int(max(tier_prices)) if tier_prices else 0
        price_range = f"¥{tier_min}~¥{tier_max}" if tier_prices else ""

        lines.append(f"━━━━━━ {tier_label}（{tier_count}家）{price_range} ━━━━━━")
        lines.append("")

        for h in tier_hotels:
            global_idx += 1

            img_str = ""
            if h.get("image"):
                img_str = f"![{h['name'][:10]}]({h['image']})"

            score_str = f"⭐{h['score']}分" if h.get("score", 0) > 0 else ""
            brand_str = h.get("brand", "")
            business_str = h.get("business", "")
            price_str = f"¥{int(h['price'])}起"

            info_parts = [p for p in [price_str, score_str, business_str, brand_str] if p]
            info_line = " | ".join(info_parts)

            lines.append(f"**{global_idx}. {h['name']}**")
            lines.append(f"   {info_line}")

            detail_parts = []
            if h.get("comment_digest"):
                detail_parts.append(f"💬 {h['comment_digest']}")
            refund = h.get("refund", "")
            if refund and "不可" not in refund and refund != "不可取消":
                detail_parts.append(f"↩️{refund}")
            meal = h.get("meal", "")
            if meal and "无" not in str(meal):
                detail_parts.append(f"🍽️{meal}")
            if detail_parts:
                lines.append(f"   {' · '.join(detail_parts)}")

            if img_str:
                lines.append(f"   {img_str}")
            lines.append("")

    lines.append("---")
    lines.append("⚠️ **尚未比价！告诉我酒店名或序号，立刻启动5大旅游平台比价！**")

    tips = _smart_tips(kw, max_price, min_score, city, poi_name)
    for tip in tips:
        lines.append(tip)

    return "\n".join(lines)


# ===== 第二步：5源精确比价 =====
def _call_fg(city, ci, co, kw):
    """飞猪：keyword精准过滤"""
    resp = _proxy("fliggy", {"city": city, "check_in": ci, "check_out": co, "keyword": kw or ""})
    data = _get_data(resp)
    if "error" in data:
        return []
    d2 = data.get("data") or data
    if not isinstance(d2, dict):
        return []
    il = d2.get("itemList", []) or []
    hotels = []
    for h in il[:30]:
        name = _clean(h.get("name", ""))
        if not name:
            continue
        try:
            p = float(re.sub(r"[^\d.]", "", str(h.get("price", "0"))))
        except:
            p = 0
        if p <= 0:
            continue
        # 使用FlyAI推广者短链，含佣金追踪参数
        url = h.get("detailUrl", "")
        hotels.append({
            "name": name, "price": p,
            "address": h.get("address", ""),
            "star": h.get("star", ""),
            "source": "fliggy",
            "url": url,
            "brand": h.get("brandName") or "",
        })
    return hotels


def _call_rg_detail(city, ci, co, hotel_name):
    """RG：多策略搜索（原名→品牌+地标→品牌+城市），校验分店一致性"""
    # 构建多个搜索关键词
    keywords = [hotel_name]
    brand = _extract_brand(hotel_name)
    # 从括号提取分店地标
    m_branch = re.search(r'[（(]([^）)]+)[）)]', hotel_name)
    branch = m_branch.group(1) if m_branch else ""
    if brand and branch:
        # 去掉城市名避免"南京路"被识别为城市
        branch_short = re.sub(r'^' + city, '', branch) if city else branch
        keywords.append(brand + branch_short)
        keywords.append(brand + city + branch_short)
    elif brand:
        keywords.append(brand + city)

    for kw in keywords:
        resp = _proxy("rg_detail", {"name": kw, "check_in": ci, "check_out": co, "city": city})
        data = _get_data(resp)
        if "error" in data or not data.get("success"):
            continue
        plans = data.get("roomRatePlans", [])
        min_price = None
        for p in plans:
            tp = p.get("totalPrice") or p.get("averagePrice")
            if tp and isinstance(tp, (int, float)) and tp > 0:
                if min_price is None or tp < min_price:
                    min_price = tp
        if min_price is None:
            continue
        rg_name = data.get("name", hotel_name)
        # 校验分店：两者都有分店信息时，必须包含共同地标字符
        if branch:
            m_rg = re.search(r'[（(]([^）)]+)[）)]', rg_name)
            if m_rg:
                rg_branch = m_rg.group(1)
                common = set(branch) & set(rg_branch)
                if len(common) < 2:
                    continue  # 分店不匹配，试下一个关键词
        # 修正RG链接日期（API返回的日期可能与查询不一致）
        url = data.get("bookingUrl", "")
        if url and ci and co:
            url = re.sub(r'checkInDate=\d{4}-\d{2}-\d{2}', f'checkInDate={ci}', url)
            url = re.sub(r'checkOutDate=\d{4}-\d{2}-\d{2}', f'checkOutDate={co}', url)
        return {
            "name": _clean(rg_name),
            "price": float(min_price),
            "source": "rg",
            "url": url,
        }
    return None


def _call_tuniu_compare(city, ci, co, hotel_name, address=""):
    """途牛比价：多策略搜索（先酒店名→再品牌→再地址路名），选sim最高的结果"""
    brand = _extract_brand(hotel_name)
    road = _extract_road(address)
    strategies = [hotel_name]
    if brand and brand != hotel_name:
        strategies.append(brand)
    if road:
        strategies.append(road)
    best = None
    best_sim = 0.5
    for kw in strategies:
        resp = _proxy("tuniu", {"city": city, "check_in": ci, "check_out": co, "keyword": kw})
        data = _get_data(resp)
        if "error" in data:
            continue
        hl = data.get("hotels") or data.get("hotelList") or []
        if not isinstance(hl, list):
            continue
        for h in hl[:20]:
            name = _clean(h.get("hotelName") or h.get("name", ""))
            if not name:
                continue
            sim = _name_sim(hotel_name, name)
            if sim > best_sim:
                try:
                    p = float(re.sub(r"[^\d.]", "", str(h.get("lowestPrice") or h.get("price") or "0")))
                except:
                    p = 0
                if p <= 0:
                    continue
                best_sim = sim
                hotel_id = h.get("hotelId", "")
                tuniu_url = f"https://m.tuniu.com/hotel/detail/{hotel_id}" if hotel_id else ""
                best = {
                    "name": name, "price": p,
                    "address": h.get("address", ""),
                    "source": "tuniu", "url": tuniu_url,
                    "score": h.get("commentScore", ""),
                    "strategy": kw,
                }
    return best


def _call_tc(city, ci, co, kw):
    """同程：AI聊天接口，传keyword精确匹配（超时重试一次）"""
    # 第一次尝试
    resp = _proxy("tongcheng", {"city": city, "check_in": ci, "check_out": co, "keyword": kw or ""}, timeout=90)
    data = _get_data(resp)
    # 如果失败，重试一次
    if "error" in data:
        resp = _proxy("tongcheng", {"city": city, "check_in": ci, "check_out": co, "keyword": kw or ""}, timeout=90)
        data = _get_data(resp)
        if "error" in data:
            return []
    text = ""
    links = {}
    if isinstance(data, dict):
        if data.get("data") and isinstance(data["data"], dict):
            text = data["data"].get("text", "")
            links = data["data"].get("产品跳转链接", {})
        else:
            text = data.get("text", "")
    hotels = []
    # 优先方案：从产品跳转链接key获取酒店名，从text提取价格
    if links:
        # 提取所有价格（多房型），不只是最低价
        all_prices_map = {}  # {link_name: [price1, price2, ...]}
        # 过滤关键词：跳过钟点房、小时房等非标准房型
        skip_keywords = ["钟点", "小时房", "白天房", "计时房", "短租"]
        for para in text.split("\n\n")[:8]:
            # 检查是否包含需要跳过的关键词
            is_hourly = any(kw in para for kw in skip_keywords)
            for link_name in links:
                if link_name in para:
                    m_price = re.search(r'(\d+[\d,.]*)\s*元', para)
                    if m_price:
                        try:
                            p = float(re.sub(r"[^\d.]", "", m_price.group(1)))
                        except:
                            p = 0
                        if p > 0:
                            if link_name not in all_prices_map:
                                all_prices_map[link_name] = {"all": [], "filtered": []}
                            all_prices_map[link_name]["all"].append(p)
                            if not is_hourly:
                                all_prices_map[link_name]["filtered"].append(p)
                    break
        for link_name, info in links.items():
            if link_name not in all_prices_map:
                continue
            prices_data = all_prices_map[link_name]
            # 优先使用过滤后的价格（排除钟点房），否则使用所有价格
            valid_prices = prices_data["filtered"] if prices_data["filtered"] else prices_data["all"]
            if not valid_prices:
                continue
            # 默认使用过滤后的最低价
            price = min(valid_prices)
            name = _clean(link_name)
            # 从text提取地址
            addr = ""
            for para in text.split("\n"):
                if link_name in para:
                    am = re.search(r'位于([\u4e00-\u9fff\d]+号)', para)
                    if am:
                        addr = am.group(1)
                    break
            hotels.append({
                "name": name, "price": price,
                "all_prices": sorted(set(prices_data["all"])),  # 所有房型价格，用于异常恢复
                "address": addr,
                "source": "tongcheng",
                "url": _clean_tc_url(info.get("手机链接", "") or info.get("PC链接", "")),
            })
        if hotels:
            return hotels
    # 兜底方案：纯正则提取
    for para in text.split("\n\n")[:8]:
        m = re.match(r'^(.+?)\s+(?:位于|坐落|紧邻|靠近|距|临近|毗邻|周边|地处|坐落于).*?(\d+[\d,.]*)\s*元', para, re.M)
        if m:
            name = _clean(m.group(1).strip())
            if name:
                try:
                    p = float(re.sub(r"[^\d.]", "", m.group(2)))
                except:
                    p = 0
                if p > 0:
                    h = {"name": name, "price": p, "source": "tongcheng"}
                    if name in links:
                        h["url"] = _clean_tc_url(links[name].get("手机链接", "") or links[name].get("PC链接", ""))
                    hotels.append(h)
    return hotels


def _call_mt(city, hotel_name):
    """美团：从markdown文本提取价格和预订链接"""
    resp = _proxy("meituan", {"city": city, "query": hotel_name}, timeout=60)
    data = _get_data(resp)
    if "error" in data:
        return None
    text = data.get("data", "")
    if not isinstance(text, str) or not text:
        return None
    m_price = re.search(r'￥(\d+(?:\.\d+)?)\s*起', text)
    if not m_price:
        return None
    price = float(m_price.group(1))
    links = re.findall(r'\[([^\]]*)\]\((https?://[^\)]+)\)', text)
    url = ""
    for label, link_url in links:
        if 'dpurl.cn' in link_url:
            url = link_url
            break
    m_score = re.search(r'美团真实评分([\d.]+)', text)
    score = float(m_score.group(1)) if m_score else 0
    return {
        "name": _clean(hotel_name),
        "price": price,
        "source": "meituan",
        "url": url,
        "score": score,
    }


# ===== 匹配工具 =====
BRAND_LIST = [
    "华尔道夫", "丽思卡尔顿", "瑞吉", "宝格丽", "文华东方", "瑰丽", "半岛", "四季", "悦榕庄", "费尔蒙", "柏悦", "康莱德",
    "洲际", "JW万豪", "W酒店", "威斯汀", "喜来登", "万丽", "皇冠假日", "凯悦", "君悦", "索菲特", "铂尔曼", "诺富特",
    "香格里拉", "丽笙", "万达文华", "万达嘉华",
    "万豪", "希尔顿", "凯宾斯基", "金陵", "开元名都", "锦江",
    "亚朵", "全季", "桔子水晶", "桔子", "丽枫", "喆啡", "美居", "宜必思", "智选假日", "假日",
    "希尔顿欢朋", "希尔顿逸林", "希尔顿花园", "维也纳", "如家", "汉庭", "7天", "莫泰", "速8",
    "格林豪泰", "尚客优", "城市便捷",
]


def _extract_brand(hotel_name):
    for b in BRAND_LIST:
        if b in hotel_name:
            return b
    return ""


def _extract_road(address):
    if not address:
        return ""
    # 先去掉行政区划前缀（省/市/区/县），只保留路名部分
    addr = re.sub(r'^.*[省市区县]', '', address)
    if not addr:
        addr = address
    m = re.search(r'([\u4e00-\u9fff]{1,6}[路街道巷弄])', addr)
    return m.group(1) if m else ""


def _name_sim(q, r):
    # 分店校验：如果两者括号内的分店信息完全不同，最高只给0.4
    m_q = re.search(r'[（(]([^）)]+)[）)]', q)
    m_r = re.search(r'[（(]([^）)]+)[）)]', r)
    branch_mismatch = False
    if m_q and m_r and m_q.group(1) != m_r.group(1):
        # 检查是否在同一城市（有共同字符）
        b_q, b_r = m_q.group(1), m_r.group(1)
        common_chars = set(b_q) & set(b_r)
        if len(common_chars) < 2:
            branch_mismatch = True
    q, r = _clean(q), _clean(r)
    if q == r:
        return 0.4 if branch_mismatch else 1.0
    if not q or not r:
        return 0.0
    if q in r or r in q:
        return 0.85
    q_brand = _extract_brand(q)
    r_brand = _extract_brand(r)
    if q_brand and r_brand and q_brand == r_brand:
        q_loc = q.replace(q_brand, "", 1).replace("酒店", "").replace("大酒店", "").strip()
        r_loc = r.replace(r_brand, "", 1).replace("酒店", "").replace("大酒店", "").strip()
        if q_loc and r_loc and (q_loc in r_loc or r_loc in q_loc):
            return 0.85
        if q_loc and r_loc:
            # 用bigram分词解决中文地址无空格分词问题
            q_tokens = set(q_loc[i:i+2] for i in range(len(q_loc) - 1))
            r_tokens = set(r_loc[i:i+2] for i in range(len(r_loc) - 1))
            if q_tokens & r_tokens:
                overlap = len(q_tokens & r_tokens)
                union = len(q_tokens | r_tokens)
                if union > 0:
                    ratio = overlap / union
                    return 0.65 + 0.2 * ratio
        return 0.3
    q_tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}', q))
    r_tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}', r))
    if q_tokens and r_tokens:
        overlap = len(q_tokens & r_tokens)
        union = len(q_tokens | r_tokens)
        if union > 0:
            return overlap / union
    return 0.0


def _find_target(hotel_name, results, threshold=0.5):
    best = None
    best_score = threshold
    q_brand = _extract_brand(hotel_name)
    for h in results:
        sim = _name_sim(hotel_name, h["name"])
        # 品牌感知：同品牌时降低阈值到0.25，分数额外+0.25
        if q_brand and _extract_brand(h["name"]) == q_brand:
            score = sim + 0.25
        else:
            score = sim
        if score > best_score:
            best_score = score
            best = h
    return best


# ===== 比价结果格式化 =====
def _format_compare(target_name, rg_result, tn_result, fg_result, tc_result, mt_result, city, ci, co):
    lines = [f"💰 **{target_name}** 多旅游平台比价（{ci}~{co}）", ""]
    found = []
    if rg_result:
        if _name_sim(target_name, rg_result["name"]) >= 0.5:
            found.append(("rg", rg_result))
    if fg_result:
        target = _find_target(target_name, fg_result, threshold=0.5)
        if target:
            found.append(("fliggy", target))
    if tn_result:
        found.append(("tuniu", tn_result))
    if mt_result:
        found.append(("meituan", mt_result))
    if tc_result:
        target = _find_target(target_name, tc_result, threshold=0.5)
        if target:
            found.append(("tongcheng", target))
    if not found:
        lines.append("❌ 所有平台均未找到该酒店，建议换关键词重试")
        return "\n".join(lines)

    # ===== 异常价格检测与恢复 =====
    if len(found) >= 3:
        prices = sorted([h["price"] for _, h in found if h["price"] > 0])
        if len(prices) >= 3:
            # 计算中位数
            mid = len(prices) // 2
            median = prices[mid] if len(prices) % 2 == 1 else (prices[mid-1] + prices[mid]) / 2
            threshold = median * 0.5
            # 检测并尝试恢复异常价格
            recovered = []
            for i, (src, h) in enumerate(found):
                if h["price"] > 0 and h["price"] < threshold:
                    # 价格异常，尝试从 all_prices 中恢复
                    all_p = h.get("all_prices", [])
                    if len(all_p) > 1:
                        # 从所有价格中选择一个接近中位数的
                        valid_alternatives = [p for p in all_p if p >= threshold]
                        if valid_alternatives:
                            # 选择最接近中位数的价格
                            best_alt = min(valid_alternatives, key=lambda p: abs(p - median))
                            old_price = h["price"]
                            h["price"] = best_alt
                            recovered.append((src, old_price, best_alt))
                            found[i] = (src, h)
            if recovered:
                # 有价格被恢复
                for src, old_p, new_p in recovered:
                    lines.append(f"⚠️ {PNAME[src]}原价¥{int(old_p)}疑似钟点房，已修正为¥{int(new_p)}")
                lines.append("")

    lines.append(f"📊 {len(found)}家平台有报价，价格从低到高：")
    lines.append("")

    found.sort(key=lambda x: (x[1]["price"] if x[1]["price"] > 0 else 99999, COMMISSION_PRIORITY.get(x[0], 99)))
    lowest_price = found[0][1]["price"]
    lowest_url = found[0][1].get("url", "")
    lowest_label = f"💰 **{PNAME[found[0][0]]} ¥{int(lowest_price)}最低价**"
    if lowest_url:
        lowest_label += f" [去预订→]({lowest_url})"
    if len(found) > 1:
        second_price = found[1][1]["price"]
        savings = second_price - lowest_price
        if savings > 0:
            lowest_label += f"（比次低省¥{int(savings)}）"

    lines.append(lowest_label)
    for i, (s, h) in enumerate(found):
        if i == 0:
            continue
        p = h["price"]
        ps = f"¥{int(p)}"
        diff = p - lowest_price
        diff_str = f"（贵¥{int(diff)}）" if diff > 0 else "（同最低价）"
        url = h.get("url", "")
        url_str = f" [去预订→]({url})" if url else ""
        lines.append(f" {PNAME[s]} {ps}{diff_str}{url_str}")

    if len(found) >= 2:
        prices = [h["price"] for _, h in found if h["price"] > 0]
        max_p, min_p = max(prices), min(prices)
        if max_p / min_p > 1.5:
            lines.append("")
            lines.append(f"📊 各平台价差 ¥{int(min_p)}~¥{int(max_p)}，建议选最低价平台预订")

    not_found = [PNAME[s] for s in PORDER if s not in [x[0] for x in found]]
    if not_found:
        lines.append("")
        lines.append(f"📌 {','.join(not_found)}暂无该酒店报价")

    lines.append("")
    lines.append("💡 价格实时变动，以实际预订为准")
    return "\n".join(lines)


# ===== 主入口 =====
def compare_hotels(city, check_in="", check_out="", keyword="", hotel_name="", max_price=0, poi_name="", min_score=0):
    """酒店比价主函数"""
    # 清理参数
    if not keyword or keyword == "None": keyword = ""
    if not hotel_name or hotel_name == "None": hotel_name = ""
    if not poi_name or poi_name == "None": poi_name = ""
    if not max_price or max_price == "None":
        max_price = 0
    else:
        try: max_price = int(re.sub(r'[^\d]', '', str(max_price)))
        except: max_price = 0
    if not min_score or min_score == "None":
        min_score = 0
    else:
        try: min_score = float(str(min_score))
        except: min_score = 0

    # 日期处理
    if not check_in or check_in == "None":
        check_in = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not check_out or check_out == "None":
        check_out = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    try:
        d1 = datetime.strptime(check_in, "%Y-%m-%d")
        d2 = datetime.strptime(check_out, "%Y-%m-%d")
        if d1 < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return f"❌ 入住日期{check_in}已过期"
        if d2 <= d1:
            return f"❌ 离店日期({check_out})必须晚于入住日期({check_in})"
    except ValueError:
        return "❌ 日期格式不正确，请使用YYYY-MM-DD格式"

    # ========== 用户已选定酒店，5源精确比价 ==========
    if hotel_name:
        rg_result = None
        fg_result = None
        tn_result = None
        tc_result = None
        mt_result = None

        # 第一轮：用酒店名搜索所有平台
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            futs = {}
            futs[ex.submit(_call_rg_detail, city, check_in, check_out, hotel_name)] = "rg"
            futs[ex.submit(_call_fg, city, check_in, check_out, hotel_name)] = "fliggy"
            futs[ex.submit(_call_tuniu_compare, city, check_in, check_out, hotel_name, "")] = "tuniu"
            futs[ex.submit(_call_mt, city, hotel_name)] = "meituan"
            futs[ex.submit(_call_tc, city, check_in, check_out, hotel_name)] = "tongcheng"
            for f in concurrent.futures.as_completed(futs, timeout=90):
                src = futs[f]
                try:
                    r = f.result(timeout=60)
                    if src == "rg": rg_result = r
                    elif src == "fliggy": fg_result = r
                    elif src == "tuniu": tn_result = r
                    elif src == "meituan": mt_result = r
                    elif src == "tongcheng": tc_result = r
                except:
                    pass

        # 第二轮：对未搜到的平台，用品牌名重搜
        brand = _extract_brand(hotel_name)
        if not brand:
            brand = re.sub(r'[（(][^）)]*[）)]', '', hotel_name)
            brand = brand.replace("酒店", "").replace("大酒店", "").strip()

        if brand and brand != hotel_name:
            missing = [s for s, r in [("rg", rg_result), ("fliggy", fg_result),
                ("tuniu", tn_result), ("meituan", mt_result), ("tongcheng", tc_result)] if not r]
            if missing:
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
                    futs2 = {}
                    if "fliggy" in missing:
                        futs2[ex.submit(_call_fg, city, check_in, check_out, brand)] = "fliggy"
                    if "tuniu" in missing:
                        futs2[ex.submit(_call_tuniu_compare, city, check_in, check_out, brand, "")] = "tuniu"
                    if "tongcheng" in missing:
                        futs2[ex.submit(_call_tc, city, check_in, check_out, brand)] = "tongcheng"
                    if "meituan" in missing:
                        futs2[ex.submit(_call_mt, city, brand)] = "meituan"
                    if "rg" in missing:
                        futs2[ex.submit(_call_rg_detail, city, check_in, check_out, brand)] = "rg"
                    for f in concurrent.futures.as_completed(futs2, timeout=90):
                        src = futs2[f]
                        try:
                            r = f.result(timeout=60)
                            if src == "rg" and not rg_result: rg_result = r
                            elif src == "fliggy" and not fg_result: fg_result = r
                            elif src == "tuniu" and not tn_result: tn_result = r
                            elif src == "meituan" and not mt_result: mt_result = r
                            elif src == "tongcheng" and not tc_result: tc_result = r
                        except:
                            pass

        return _format_compare(hotel_name, rg_result, tn_result, fg_result, tc_result, mt_result, city, check_in, check_out)

    # ========== 途牛多页翻页搜索 ==========
    hotels, total_before_filter = _tuniu_browse(city, check_in, check_out, keyword, max_price, poi_name)

    # 评分过滤
    if min_score and min_score > 0:
        hotels = [h for h in hotels if h.get("score", 0) == 0 or h["score"] >= min_score]

    if not hotels:
        tips = _smart_tips(keyword, max_price, min_score, city, poi_name)
        msg = f"未找到{city}符合条件的酒店"
        if max_price: msg += f"（预算¥{int(max_price)}以内）"
        if min_score: msg += f"（评分≥{min_score}）"
        if tips:
            msg += "\n\n" + "\n".join(tips)
        return msg

    return _format_browse(hotels, city, check_in, check_out, keyword, max_price, min_score, poi_name, total_before_filter)


def main():
    parser = argparse.ArgumentParser(description="跨平台酒店比价 - 5大旅游平台酒店价格对比")
    parser.add_argument("--city", required=True, help="城市名，如上海、北京、三亚")
    parser.add_argument("--check_in", default="", help="入住日期，如2026-07-01")
    parser.add_argument("--check_out", default="", help="退房日期，如2026-07-03")
    parser.add_argument("--keyword", default="", help="搜索关键词，如外滩、迪士尼")
    parser.add_argument("--hotel_name", default="", help="酒店名称，用于精确比价模式")
    parser.add_argument("--max_price", type=int, default=0, help="最高价格过滤")
    parser.add_argument("--poi_name", default="", help="附近地标/POI名称")
    parser.add_argument("--min_score", type=float, default=0, help="最低评分过滤")
    args = parser.parse_args()

    result = compare_hotels(
        city=args.city,
        check_in=args.check_in,
        check_out=args.check_out,
        keyword=args.keyword,
        hotel_name=args.hotel_name,
        max_price=args.max_price,
        poi_name=args.poi_name,
        min_score=args.min_score,
    )
    print(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""亲子出行助手 - 儿童票政策查询+亲子景点推荐+出行贴士，帮带娃家庭轻松出行"""

import sys
import json
import urllib.request
import re

# ==================== 代理配置 ====================

SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://gaode-proxy-jerspxcked.cn-hangzhou.fcapp.run"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# ==================== 网络请求 ====================

def http_post(url, data):
    """发送POST请求"""
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def gaode_call(api, params):
    """调用高德代理API"""
    data = json.dumps({"api": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(GAODE_PROXY, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ==================== 儿童票政策规则 ====================

# 机票儿童/婴儿票政策
FLIGHT_CHILD_POLICY = {
    "婴儿票": {
        "age": "出生14天-2周岁(不含)",
        "price_rule": "成人全价票的10%，免收燃油附加费和机场建设费",
        "seat": "不提供座位，需成人抱乘",
        "baggage": "无免费行李额",
        "tips": "需携带出生证明或户口本；起飞/降落时可喂奶缓解耳压"
    },
    "儿童票": {
        "age": "2周岁(含)-12周岁(不含)",
        "price_rule": "成人全价票的50%，免收机场建设费，燃油附加费减半",
        "seat": "提供独立座位",
        "baggage": "部分航司提供儿童免费行李额",
        "tips": "5岁以上儿童可单独乘机(无陪儿童服务)；儿童票可能比成人折扣票贵，建议先查成人折扣票对比"
    },
    "无陪儿童": {
        "age": "5-12周岁",
        "price_rule": "按儿童票标准收费，另收无陪服务费(各航司不同)",
        "seat": "提供独立座位，有专人接送机",
        "tips": "需提前48小时申请；仅限直飞航班"
    },
}

# 火车票儿童票政策
TRAIN_CHILD_POLICY = {
    "免费": {
        "condition": "一名成年人可免费携带一名6周岁(不含)以下儿童",
        "seat": "不提供座位，与成人共用",
        "tips": "6周岁以下如需单独座位应买儿童票"
    },
    "儿童票": {
        "condition": "6周岁(含)-14周岁(不含)",
        "price_rule": "客票、加快票、空调票均为成人票价的50%",
        "seat": "提供独立座位",
        "tips": "14周岁以上买全价票"
    },
}

# 景点儿童票通用规则
SCENIC_CHILD_POLICY = {
    "免票": "1.2米(不含)以下儿童免票(部分景区为1.1米)",
    "半价票": "1.2米-1.5米(不含)儿童半价(部分景区1.2米-1.4米)",
    "全价票": "1.5米(含)以上需购全价票",
    "注意": "各景区标准不同，以景区实际规定为准；部分景区按年龄(如6岁以下/6-18岁)而非身高"
}

# 亲子出行年龄段注意事项
AGE_TIPS = {
    "0-1岁": [
        "🍼 出行必备：奶粉/母乳、奶瓶、尿不湿(日均8-10片)、婴儿湿巾",
        "🛏 住宿建议选婴儿床可借的酒店，或自带便携床围",
        "🚗 交通：飞机需出生14天后才可乘机；火车无年龄限制",
        "💊 随身带退烧药(布洛芬/对乙酰氨基酚)、体温计、创可贴",
        "🌡️ 注意室内外温差，婴儿体温调节能力弱",
    ],
    "1-3岁": [
        "🧸 出行必备：推车(轻便伞车)、零食、水杯、换洗衣物(多备2套)",
        "🚼 景区推车通行性要提前确认，部分景区路面不适合推车",
        "🍽️ 餐饮：自备儿童餐具，选择有儿童餐的餐厅",
        "😴 午睡安排：行程中预留午睡时间，避免过度疲劳哭闹",
        "🏥 近期疫苗接种记录随身带，异地就医可能需要",
    ],
    "3-6岁": [
        "🎢 适合主题乐园/动物园/海洋馆等互动性强的景点",
        "🎨 出行必备：画本/贴纸等安静玩具(排队/乘车用)",
        "📱 教孩子记住父母手机号，或写卡片放口袋",
        "🧴 防晒霜SPF50+，3岁以上可用儿童专用款",
        "💡 行程节奏放缓，每天2-3个景点为宜",
    ],
    "6-12岁": [
        "🎒 可让孩子自己背小包(水杯+零食+玩具)，培养独立性",
        "📚 出行前一起看目的地纪录片/绘本，增加兴趣",
        "🚂 火车儿童票6-14岁半价，注意携带户口本/身份证",
        "🎒 6岁以上可体验研学类景点(科技馆/博物馆/自然保护区)",
        "📱 可考虑给孩子配电话手表，方便联络",
    ],
}

# 亲子友好景点类型
FAMILY_FRIENDLY_TYPES = {
    "主题乐园": {"飞猪category": "主题乐园", "适合年龄": "3岁+", "特点": "互动性强，适合全家"},
    "动物园/海洋馆": {"飞猪category": "动物园", "适合年龄": "1岁+", "特点": "观赏性强，教育意义"},
    "自然公园": {"飞猪category": "公园园林", "适合年龄": "0岁+", "特点": "空间大，推车友好"},
    "科技馆/博物馆": {"飞猪category": "博物馆", "适合年龄": "5岁+", "特点": "寓教于乐，室内不受天气影响"},
    "水上乐园": {"飞猪category": "水上乐园", "适合年龄": "3岁+", "特点": "夏日首选，注意防晒"},
    "农庄/采摘": {"飞猪category": "农家乐", "适合年龄": "2岁+", "特点": "亲近自然，体验式"},
}


# ==================== 命令实现 ====================

def cmd_policy(params):
    """查询儿童票政策"""
    policy_type = params.get("type", "all")  # flight/train/scenic/all
    child_age = int(params.get("age", 0))  # 孩子年龄(岁)

    result = {"child_age": child_age}

    if policy_type in ("all", "flight"):
        result["flight"] = FLIGHT_CHILD_POLICY.copy()
        if child_age > 0:
            if child_age < 2:
                result["flight_recommendation"] = "建议购买婴儿票(成人全价10%)"
            elif child_age < 12:
                result["flight_recommendation"] = "建议购买儿童票(成人全价50%)，但注意对比成人折扣票价格"
            else:
                result["flight_recommendation"] = "需购买成人票"

    if policy_type in ("all", "train"):
        result["train"] = TRAIN_CHILD_POLICY.copy()
        if child_age > 0:
            if child_age < 6:
                result["train_recommendation"] = "可免费随成人乘车(不占座)，如需座位请购儿童票"
            elif child_age < 14:
                result["train_recommendation"] = "购买儿童票(成人票价50%)"
            else:
                result["train_recommendation"] = "需购买全价票"

    if policy_type in ("all", "scenic"):
        result["scenic"] = SCENIC_CHILD_POLICY.copy()

    # 年龄段贴士
    if child_age > 0:
        for age_range, tips in AGE_TIPS.items():
            parts = age_range.split("-")
            low = int(re.sub(r'\D', '', parts[0]) or '0')
            high = int(re.sub(r'\D', '', parts[1]) or '18')
            if low <= child_age <= high:
                result["age_tips"] = tips
                result["age_range"] = age_range
                break
        else:
            result["age_tips"] = AGE_TIPS.get("6-12岁", [])
            result["age_range"] = "6-12岁"

    return result


def cmd_attractions(params):
    """亲子景点推荐"""
    city = params.get("city", "")
    child_age = int(params.get("age", 3))  # 孩子年龄
    attraction_type = params.get("type", "")  # 主题乐园/动物园/水上乐园/...
    keyword = params.get("keyword", "")  # 自定义搜索词

    if not city:
        return {"error": "请提供城市名称"}

    # 构建搜索关键词
    if keyword:
        search_keyword = keyword
    elif attraction_type and attraction_type in FAMILY_FRIENDLY_TYPES:
        search_keyword = f"{city}{attraction_type}"
    else:
        # 根据年龄推荐类型
        if child_age < 3:
            search_keyword = f"{city}动物园"
        elif child_age < 6:
            search_keyword = f"{city}主题乐园"
        else:
            search_keyword = f"{city}主题乐园"

    # 飞猪POI搜索
    fliggy_data = http_post(SCF_FLIGGY_URL, {
        "type": "search_poi",
        "params": {"keyword": search_keyword, "city": city}
    })

    pois = fliggy_data.get("data", {}).get("itemList", [])

    # 如果默认搜索结果少，补充搜索
    if len(pois) < 3 and not keyword:
        extra_keywords = ["海洋馆", "动物园", "儿童乐园"]
        for ek in extra_keywords:
            extra_data = http_post(SCF_FLIGGY_URL, {
                "type": "search_poi",
                "params": {"keyword": f"{city}{ek}", "city": city}
            })
            extra_pois = extra_data.get("data", {}).get("itemList", [])
            pois.extend(extra_pois)
            if len(pois) >= 10:
                break

    # 去重+筛选亲子友好
    seen_ids = set()
    results = []
    for p in pois:
        pid = p.get("id", "")
        if pid in seen_ids:
            continue
        seen_ids.add(pid)

        category = p.get("category", "")
        ti = p.get("ticketInfo", {}) or {}

        # 亲子友好度评分
        family_score = 0
        cat_lower = category.lower() if category else ""
        if any(k in cat_lower for k in ["主题乐园", "乐园"]):
            family_score = 5
        elif any(k in cat_lower for k in ["动物园", "海洋", "水族"]):
            family_score = 5
        elif any(k in cat_lower for k in ["公园", "植物园"]):
            family_score = 3
        elif any(k in cat_lower for k in ["博物馆", "科技馆", "展览"]):
            family_score = 4
        elif any(k in cat_lower for k in ["水上", "温泉"]):
            family_score = 4

        # 如果搜索词包含亲子相关关键词，基础分+1
        name = p.get("name", "")
        desc = p.get("description", "")
        if any(k in name + desc for k in ["亲子", "儿童", "家庭", "宝贝", "少年"]):
            family_score += 1

        results.append({
            "name": name,
            "category": category,
            "address": p.get("address", ""),
            "price": ti.get("price", "未知"),
            "ticket_name": ti.get("ticketName", ""),
            "free": p.get("freePoiStatus", "") == "FREE",
            "family_score": min(family_score, 5),
            "age_suitability": _age_suitability(category, child_age),
            "jump_url": p.get("jumpUrl", ""),
        })

    # 按亲子友好度排序
    results.sort(key=lambda x: (-x["family_score"], x["price"] if isinstance(x["price"], (int, float)) else 999))

    # 查途牛儿童票/亲子票详情（对前3个景点）
    detailed = []
    for r in results[:3]:
        tuniu_info = _query_tuniu_child_tickets(r["name"])
        if tuniu_info:
            r["child_tickets"] = tuniu_info
        detailed.append(r)

    # 天气
    weather = _get_weather_brief(city)

    return {
        "city": city,
        "child_age": child_age,
        "weather": weather,
        "attractions": detailed + results[3:],
        "total_found": len(results),
        "recommended_types": _recommend_types(child_age),
    }


def _age_suitability(category, age):
    """根据景点类型和儿童年龄判断适合度"""
    if not category:
        return "未知"
    cat = category.lower()
    if age < 1:
        if any(k in cat for k in ["公园", "植物园"]):
            return "适合(推车可通行)"
        return "不太适合(婴儿不宜久留)"
    elif age < 3:
        if any(k in cat for k in ["动物园", "海洋", "公园", "乐园"]):
            return "适合"
        return "可能不适合(孩子太小)"
    elif age < 6:
        if any(k in cat for k in ["主题乐园", "动物园", "海洋", "水上", "乐园"]):
            return "非常适合"
        if any(k in cat for k in ["博物馆", "科技馆"]):
            return "部分适合(需有互动展区)"
        return "适合"
    else:
        return "适合"


def _recommend_types(age):
    """根据年龄推荐景点类型"""
    if age < 1:
        return ["自然公园(推车散步)", "室内商场(有母婴室)"]
    elif age < 3:
        return ["动物园/海洋馆(观赏)", "自然公园(亲近自然)", "室内游乐场"]
    elif age < 6:
        return ["主题乐园(互动体验)", "动物园/海洋馆", "水上乐园(夏季)", "农庄采摘"]
    else:
        return ["主题乐园", "科技馆/博物馆(研学)", "水上乐园(夏季)", "自然探索", "历史景点(文化学习)"]


def _query_tuniu_child_tickets(scenic_name):
    """查询途牛儿童票/亲子票"""
    try:
        # 先精确查询
        data = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_ticket_query",
            "params": {"scenic_name": scenic_name}
        })
        tickets = data.get("data", {}).get("tickets", [])

        # 如果无结果，去掉后缀重试
        if not tickets:
            for suffix in ["度假区", "风景名胜区", "旅游景区", "风景区", "景区", "旅游区"]:
                if scenic_name.endswith(suffix):
                    short_name = scenic_name[:-len(suffix)]
                    data = http_post(SCF_TUNIU_URL, {
                        "type": "tuniu_ticket_query",
                        "params": {"scenic_name": short_name}
                    })
                    tickets = data.get("data", {}).get("tickets", [])
                    if tickets:
                        break

        # 筛选儿童票/亲子票
        child_tickets = []
        for t in tickets:
            person = t.get("personTypeName", "")
            if "儿童" in person or "亲子" in person or "家庭" in person or "1大1小" in person or "2大1小" in person:
                child_tickets.append({
                    "type": person,
                    "ticket_type": t.get("ticketTypeName", ""),
                    "price": t.get("startPrice", ""),
                    "market_price": t.get("priceMarket", ""),
                    "satisfaction": t.get("satisfaction", ""),
                })

        return child_tickets if child_tickets else None

    except Exception:
        return None


def _get_weather_brief(city):
    """获取天气简报"""
    try:
        # 先获取adcode
        geo_data = gaode_call("geocode/geo", {"address": city})
        geocodes = geo_data.get("geocodes", [])
        if not geocodes:
            return None
        adcode = geocodes[0].get("adcode", "")

        # 查实况
        weather_data = gaode_call("weather/weatherInfo", {"city": adcode})
        lives = weather_data.get("lives", [])
        if lives:
            l = lives[0]
            return {
                "city": l.get("city", city),
                "weather": l.get("weather", ""),
                "temperature": l.get("temperature", ""),
                "humidity": l.get("humidity", ""),
            }
    except Exception:
        pass
    return None


def cmd_checklist(params):
    """亲子出行打包清单"""
    child_age = int(params.get("age", 3))
    destination = params.get("destination", "")
    days = int(params.get("days", 3))

    checklist = {
        "儿童证件": [
            {"item": "户口本/身份证", "essential": True, "note": "乘机/火车/景点买票都需要"},
            {"item": "出生证明(3岁以下)", "essential": child_age < 3, "note": "乘机必备"},
            {"item": "儿童预防接种证", "essential": False, "note": "异地就医可能需要"},
        ],
        "儿童衣物": [],
        "儿童护理": [],
        "儿童娱乐": [],
        "儿童饮食": [],
    }

    # 按年龄段细化
    if child_age < 1:
        checklist["儿童衣物"].extend([
            {"item": "连体衣×(天数+2)", "essential": True},
            {"item": "薄外套", "essential": True},
            {"item": "口水巾×5", "essential": True},
        ])
        checklist["儿童护理"].extend([
            {"item": "尿不湿(日均8-10片)", "essential": True},
            {"item": "婴儿湿巾", "essential": True},
            {"item": "护臀霜", "essential": True},
            {"item": "婴儿洗衣液(旅行装)", "essential": False},
            {"item": "婴儿沐浴露", "essential": False},
        ])
        checklist["儿童饮食"].extend([
            {"item": "奶粉+奶瓶", "essential": True},
            {"item": "保温杯(冲奶用)", "essential": True},
            {"item": "辅食/果泥", "essential": True},
            {"item": "围兜", "essential": True},
        ])
        checklist["儿童娱乐"].extend([
            {"item": "安抚奶嘴", "essential": False},
            {"item": "牙胶/咬咬乐", "essential": False},
        ])
    elif child_age < 3:
        checklist["儿童衣物"].extend([
            {"item": "儿童换洗衣物×(天数+2)", "essential": True, "note": "小孩容易弄脏，多备"},
            {"item": "薄外套", "essential": True},
            {"item": "防滑袜/软底鞋", "essential": True},
        ])
        checklist["儿童护理"].extend([
            {"item": "尿不湿/拉拉裤", "essential": True},
            {"item": "湿巾+纸巾", "essential": True},
            {"item": "儿童防晒霜", "essential": True},
            {"item": "儿童退烧药+体温计", "essential": True},
            {"item": "创可贴+碘伏棉签", "essential": True},
        ])
        checklist["儿童饮食"].extend([
            {"item": "儿童水杯", "essential": True},
            {"item": "零食(果泥/饼干/奶酪)", "essential": True, "note": "安抚+充饥"},
            {"item": "儿童餐具(便携套装)", "essential": False},
        ])
        checklist["儿童娱乐"].extend([
            {"item": "轻便推车", "essential": True, "note": "午睡+代步"},
            {"item": "2-3个小玩具", "essential": True, "note": "乘车/排队安抚用"},
            {"item": "绘本2-3本", "essential": False},
        ])
    elif child_age < 6:
        checklist["儿童衣物"].extend([
            {"item": "儿童换洗衣物×(天数+1)", "essential": True},
            {"item": "运动鞋(舒适)", "essential": True},
            {"item": "薄外套/防风衣", "essential": True},
        ])
        checklist["儿童护理"].extend([
            {"item": "儿童防晒霜SPF50+", "essential": True},
            {"item": "儿童常用药(退烧/止泻/创可贴)", "essential": True},
            {"item": "湿巾+纸巾", "essential": True},
        ])
        checklist["儿童饮食"].extend([
            {"item": "儿童水杯", "essential": True},
            {"item": "零食", "essential": True},
        ])
        checklist["儿童娱乐"].extend([
            {"item": "画本+彩色笔", "essential": False, "note": "安静活动"},
            {"item": "贴纸书/拼图", "essential": False},
            {"item": "小背包(自己背)", "essential": False},
        ])
    else:
        checklist["儿童衣物"].extend([
            {"item": "儿童换洗衣物×天数", "essential": True},
            {"item": "运动鞋", "essential": True},
        ])
        checklist["儿童护理"].extend([
            {"item": "儿童防晒霜", "essential": True},
            {"item": "常用药", "essential": True},
        ])
        checklist["儿童饮食"].extend([
            {"item": "水杯", "essential": True},
        ])
        checklist["儿童娱乐"].extend([
            {"item": "电话手表", "essential": False, "note": "防走失"},
            {"item": "小背包", "essential": False},
        ])

    # 天气适配追加
    weather_note = ""
    if destination:
        weather = _get_weather_brief(destination)
        if weather:
            temp = int(weather.get("temperature", "20")) if weather.get("temperature", "").isdigit() else 20
            if temp >= 30:
                checklist["儿童护理"].append({"item": "清凉油/防痱子粉", "essential": True})
                checklist["儿童衣物"].append({"item": "防晒帽/遮阳帽", "essential": True})
                weather_note = f"目的地{destination}当前{temp}°C，注意防暑"
            elif temp <= 10:
                checklist["儿童衣物"].append({"item": "厚外套/羽绒服", "essential": True})
                checklist["儿童衣物"].append({"item": "保暖帽+手套", "essential": True})
                weather_note = f"目的地{destination}当前{temp}°C，注意保暖"

    # 去重
    final = {}
    global_seen = set()
    for cat, items in checklist.items():
        unique = []
        for it in items:
            if it["item"] not in global_seen:
                global_seen.add(it["item"])
                unique.append(it)
        if unique:
            final[cat] = unique

    total = sum(len(v) for v in final.values())
    essential = sum(1 for v in final.values() for it in v if it.get("essential"))

    return {
        "destination": destination,
        "child_age": child_age,
        "days": days,
        "checklist": final,
        "stats": {"total_items": total, "essential_items": essential},
        "weather_note": weather_note,
        "pro_tips": _pro_tips(child_age, destination),
    }


def _pro_tips(age, destination):
    """亲子出行专业贴士"""
    tips = []

    if age < 2:
        tips.append("✈️ 2岁以下婴儿机票=成人全价10%，但无座位；建议选靠走道座位方便走动")
        tips.append("🍼 起飞降落时喂奶/喝水，帮助宝宝缓解耳压")
        tips.append("🏨 订酒店确认可否提供婴儿床，部分酒店免费提供")
    elif age < 6:
        tips.append("🎢 主题乐园很多项目有身高限制(如1.1米/1.2米/1.4米)，提前查好避免白跑")
        tips.append("⏰ 带娃行程建议每天不超过2-3个景点，预留午睡/休息时间")
        tips.append("📱 给孩子拍一张当天穿着的照片，万一走失方便描述")
    else:
        tips.append("🎒 让孩子自己整理小背包，培养独立性和参与感")
        tips.append("🗺️ 出发前一起看地图/纪录片，让孩子有期待感")
        tips.append("🚂 6-14岁火车半价票，记得带户口本或身份证")

    tips.append("💊 必备药品：退烧药+止泻药+创可贴+碘伏，儿童剂量与成人不同")
    tips.append("📋 紧急联系卡：写上父母电话+孩子血型+过敏史，放孩子口袋")

    return tips


# ==================== 主入口 ====================

COMMANDS = {
    "policy": cmd_policy,
    "attractions": cmd_attractions,
    "checklist": cmd_checklist,
}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "用法: python3 family.py <command> '<json_params>'",
            "commands": {
                "policy": "查询儿童票政策 (type: flight/train/scenic/all, age: 孩子年龄)",
                "attractions": "亲子景点推荐 (city, age, type, keyword)",
                "checklist": "亲子出行打包清单 (age, destination, days)",
            }
        }, ensure_ascii=False))
        sys.exit(1)

    command = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if command not in COMMANDS:
        print(json.dumps({"error": f"未知命令: {command}，可用: {list(COMMANDS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = COMMANDS[command](params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"执行失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)

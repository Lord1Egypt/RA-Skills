#!/usr/bin/env python3
"""邮轮查询预订 - 全球邮轮航线查询与预订助手"""

import json


# 邮轮公司数据
CRUISE_LINES = {
    "royal_caribbean": {
        "name": "皇家加勒比国际游轮",
        "name_en": "Royal Caribbean International",
        "rating": 4.5,
        "style": "大众/家庭",
        "highlights": ["北极星观景舱", "模拟冲浪", "攀岩墙", "百老汇演出"],
        "fleet_size": 26,
        "price_range": "3000-15000元/人"
    },
    "msc": {
        "name": "地中海邮轮",
        "name_en": "MSC Cruises",
        "rating": 4.3,
        "style": "欧式优雅",
        "highlights": ["地中海美食", "私人阳台房", "水上乐园", "施华洛世奇楼梯"],
        "fleet_size": 22,
        "price_range": "2500-12000元/人"
    },
    "costa": {
        "name": "歌诗达邮轮",
        "name_en": "Costa Crociere",
        "rating": 4.0,
        "style": "意式热情",
        "highlights": ["意式餐饮", "派对文化", "家庭活动", "免税购物"],
        "fleet_size": 14,
        "price_range": "2000-8000元/人"
    },
    "norwegian": {
        "name": "诺唯真游轮",
        "name_en": "Norwegian Cruise Line",
        "rating": 4.4,
        "style": "自由随性",
        "highlights": ["自由就餐", "海上卡丁车", "激光镭射", "百老汇秀"],
        "fleet_size": 19,
        "price_range": "3000-13000元/人"
    },
    "princess": {
        "name": "公主邮轮",
        "name_en": "Princess Cruises",
        "rating": 4.5,
        "style": "经典优雅",
        "highlights": ["海景电影院", "正式晚宴", "学苑课程", "中餐选项"],
        "fleet_size": 15,
        "price_range": "3500-15000元/人"
    },
    "celebrity": {
        "name": "精致邮轮",
        "name_en": "Celebrity Cruises",
        "rating": 4.6,
        "style": "现代奢华",
        "highlights": ["米其林主厨", "SPA水疗", "艺术收藏", "阳台客房"],
        "fleet_size": 16,
        "price_range": "5000-20000元/人"
    },
    "disney": {
        "name": "迪士尼邮轮",
        "name_en": "Disney Cruise Line",
        "rating": 4.8,
        "style": "亲子魔法",
        "highlights": ["迪士尼角色", "海上烟火", "私人岛屿", "主题餐厅"],
        "fleet_size": 5,
        "price_range": "6000-25000元/人"
    },
    "viking": {
        "name": "维京游轮",
        "name_en": "Viking Cruises",
        "rating": 4.7,
        "style": "文化深度",
        "highlights": ["全阳台房", "文化讲座", "目的地深度", "含岸上观光"],
        "fleet_size": 9,
        "price_range": "8000-30000元/人"
    }
}

# 热门航线数据
ROUTES = {
    "caribbean": {
        "name": "加勒比海",
        "regions": ["东加勒比", "西加勒比", "南加勒比"],
        "ports": ["迈阿密", "劳德代尔堡", "圣胡安", "科苏梅尔", "大开曼", "拿骚"],
        "duration": "4-14晚",
        "best_season": "11月-次年4月",
        "price_from": 2500,
        "highlights": ["碧蓝海水", "私人岛屿", "浮潜天堂", "免税购物"],
        "cruise_lines": ["royal_caribbean", "norwegian", "disney", "celebrity", "msc"]
    },
    "mediterranean": {
        "name": "地中海",
        "regions": ["西地中海", "东地中海", "爱琴海"],
        "ports": ["巴塞罗那", "罗马(奇维塔韦基亚)", "威尼斯", "雅典", "伊斯坦布尔", "圣托里尼"],
        "duration": "5-14晚",
        "best_season": "5月-10月",
        "price_from": 3000,
        "highlights": ["历史古迹", "美食天堂", "浪漫海岛", "艺术博物馆"],
        "cruise_lines": ["msc", "costa", "royal_caribbean", "celebrity", "viking"]
    },
    "alaska": {
        "name": "阿拉斯加",
        "regions": ["内湾航道", "冰河湾"],
        "ports": ["西雅图", "温哥华", "朱诺", "史凯威", "凯奇坎"],
        "duration": "7-14晚",
        "best_season": "5月-9月",
        "price_from": 4000,
        "highlights": ["冰川奇观", "极光观赏", "观鲸", "野生动物"],
        "cruise_lines": ["royal_caribbean", "princess", "norwegian", "celebrity", "viking"]
    },
    "japan": {
        "name": "日本",
        "regions": ["本州环线", "冲绳/琉球", "北海道"],
        "ports": ["上海", "天津", "长崎", "福冈", "冲绳", "大阪", "横滨"],
        "duration": "4-8晚",
        "best_season": "3月-5月(樱花)/10月-11月(红叶)",
        "price_from": 2000,
        "highlights": ["樱花季", "温泉", "日本料理", "购物"],
        "cruise_lines": ["royal_caribbean", "msc", "costa", "princess"]
    },
    "southeast_asia": {
        "name": "东南亚",
        "regions": ["越南航线", "新马泰", "菲律宾"],
        "ports": ["新加坡", "胡志明市", "芽庄", "曼谷", "吉隆坡", "马尼拉"],
        "duration": "3-7晚",
        "best_season": "11月-次年3月",
        "price_from": 1500,
        "highlights": ["热带海滩", "异域美食", "性价比高", "短途出发"],
        "cruise_lines": ["royal_caribbean", "msc", "costa", "princess"]
    },
    "northern_europe": {
        "name": "北欧/波罗的海",
        "regions": ["波罗的海", "挪威峡湾", "冰岛"],
        "ports": ["哥本哈根", "斯德哥尔摩", "赫尔辛基", "卑尔根", "雷克雅未克"],
        "duration": "7-14晚",
        "best_season": "6月-8月",
        "price_from": 5000,
        "highlights": ["峡湾风光", "午夜太阳", "北欧设计", "维京历史"],
        "cruise_lines": ["viking", "msc", "celebrity", "princess"]
    },
    "antarctica": {
        "name": "南极",
        "regions": ["南极半岛", "南设得兰群岛"],
        "ports": ["乌斯怀亚", "蓬塔阿雷纳斯"],
        "duration": "10-21晚",
        "best_season": "11月-次年3月",
        "price_from": 30000,
        "highlights": ["企鹅栖息地", "冰川奇观", "科研站", "极地探险"],
        "cruise_lines": ["viking"]
    },
    "yangtze": {
        "name": "长江三峡",
        "regions": ["三峡全线", "重庆-宜昌", "重庆-上海"],
        "ports": ["重庆", "宜昌", "武汉", "上海", "丰都", "奉节"],
        "duration": "3-15晚",
        "best_season": "3月-5月/9月-11月",
        "price_from": 1500,
        "highlights": ["三峡大坝", "瞿塘峡", "巫峡", "西陵峡"],
        "cruise_lines": ["msc", "costa"]
    },
    "transatlantic": {
        "name": "跨大西洋",
        "regions": ["东渡", "西渡"],
        "ports": ["巴塞罗那/南安普顿", "纽约/迈阿密"],
        "duration": "12-16晚",
        "best_season": "4月-5月/9月-10月(换季航线)",
        "price_from": 4000,
        "highlights": ["海上休闲", "低价长航", "文化体验", "无港口日"],
        "cruise_lines": ["royal_caribbean", "msc", "celebrity", "viking"]
    },
    "australia_nz": {
        "name": "澳新",
        "regions": ["澳大利亚东海岸", "新西兰峡湾"],
        "ports": ["悉尼", "墨尔本", "奥克兰", "峡湾国家公园", "霍巴特"],
        "duration": "7-14晚",
        "best_season": "10月-次年3月",
        "price_from": 4500,
        "highlights": ["悉尼歌剧院", "大堡礁", "峡湾", "澳式BBQ"],
        "cruise_lines": ["royal_caribbean", "celebrity", "princess", "norwegian"]
    }
}

# 邮轮旅行贴士
TIPS = {
    "booking": [
        "提前3-6个月预订价格最优，最后一分钟可能有特价但不保证房型",
        "内舱房最便宜但无窗，海景房有窗不可开，阳台房体验最佳",
        "总费用=船票+港务费+小费(约15美元/天/人)+岸上观光+餐饮升级",
        "单人出行需付单人间补差(通常1.5-2倍船票)"
    ],
    "onboard": [
        "登船日自助餐厅最不拥挤，主餐厅需要排队",
        "每晚小费自动从信用卡扣除，不需要额外给",
        "船上WiFi按天收费(约15-30美元/天)，下船前下载离线地图",
        "正式晚宴至少参加一次，带一套正装(男士西装/女士裙装)"
    ],
    "shore": [
        "船方岸上观光价格贵2-3倍，可自行预订当地tour",
        "必须注意返回时间，邮轮不等迟到的乘客",
        "港口附近通常有免费WiFi，可在港口更新社交媒体",
        "某些港口需乘接驳船(tender)上岸，风大时可能取消"
    ]
}


def search(destination: str = "", duration: str = "", style: str = "") -> str:
    """搜索邮轮航线，支持按目的地/时长/风格筛选"""
    results = []
    for key, route in ROUTES.items():
        # 筛选
        if destination:
            dest_lower = destination.lower()
            name_match = dest_lower in route["name"].lower()
            region_match = any(dest_lower in r.lower() for r in route["regions"])
            port_match = any(dest_lower in p.lower() for p in route["ports"])
            if not (name_match or region_match or port_match):
                continue
        if duration:
            dur_num = "".join(c for c in duration if c.isdigit())
            if dur_num:
                dur_int = int(dur_num)
                route_min = int(route["duration"].split("-")[0])
                route_max = int(route["duration"].split("-")[1].replace("晚", ""))
                if dur_int < route_min or dur_int > route_max:
                    continue
        if style:
            style_map = {"亲子": "disney", "奢华": "celebrity", "文化": "viking", "性价比": "costa", "大众": "royal_caribbean"}
            target = style_map.get(style, style)
            if target not in route["cruise_lines"]:
                continue

        line_names = [CRUISE_LINES[cl]["name"] for cl in route["cruise_lines"] if cl in CRUISE_LINES]
        results.append({
            "route": route["name"],
            "regions": route["regions"],
            "duration": route["duration"],
            "best_season": route["best_season"],
            "price_from": route["price_from"],
            "ports": route["ports"],
            "highlights": route["highlights"],
            "available_lines": line_names
        })

    if not results:
        return f"未找到匹配'{destination}'的邮轮航线。支持的目的地：{', '.join(r['name'] for r in ROUTES.values())}"

    output = f"🚢 邮轮航线搜索结果（{len(results)}条）\n\n"
    for r in results:
        output += f"**{r['route']}**\n"
        output += f"  ⏱ 时长：{r['duration']}  💰 起价：{r['price_from']}元/人\n"
        output += f"  🌟 旺季：{r['best_season']}\n"
        output += f"  📍 停靠：{'、'.join(r['ports'][:6])}\n"
        output += f"  ✨ 亮点：{'、'.join(r['highlights'])}\n"
        output += f"  🚢 航司：{'、'.join(r['available_lines'])}\n\n"
    return output


def detail(route_name: str = "") -> str:
    """查看航线详情，含邮轮公司信息和预订建议"""
    if not route_name:
        return "请输入航线名称，如：加勒比海、地中海、日本"

    matched = None
    matched_key = None
    for key, route in ROUTES.items():
        if route_name.lower() in route["name"].lower() or route_name.lower() == key:
            matched = route
            matched_key = key
            break

    if not matched:
        return f"未找到航线'{route_name}'。支持：{', '.join(r['name'] for r in ROUTES.values())}"

    output = f"🚢 **{matched['name']}航线详情**\n\n"
    output += f"**区域**：{'、'.join(matched['regions'])}\n"
    output += f"**时长**：{matched['duration']}\n"
    output += f"**最佳季节**：{matched['best_season']}\n"
    output += f"**参考起价**：{matched['price_from']}元/人\n"
    output += f"**停靠港口**：{'、'.join(matched['ports'])}\n"
    output += f"**核心亮点**：{'、'.join(matched['highlights'])}\n\n"

    output += "**运营邮轮公司**：\n\n"
    for cl_key in matched["cruise_lines"]:
        if cl_key in CRUISE_LINES:
            cl = CRUISE_LINES[cl_key]
            output += f"- **{cl['name']}**（{cl['name_en']}）\n"
            output += f"  评分：{'⭐' * int(cl['rating'])}  风格：{cl['style']}  船队：{cl['fleet_size']}艘\n"
            output += f"  特色：{'、'.join(cl['highlights'])}\n"
            output += f"  价格：{cl['price_range']}\n\n"

    output += "**预订建议**：\n"
    output += "- 建议提前3-6个月预订，旺季（寒暑假/国庆）需更早\n"
    output += "- 内舱房最经济，阳台房体验最佳，套房含VIP服务\n"
    output += "- 总费用 ≈ 船票 + 港务费(约800-1500元) + 小费(约100元/天) + 岸上观光\n"

    return output


def tips(category: str = "") -> str:
    """查看邮轮旅行贴士，支持按类别筛选：预订/船上/岸上"""
    if category:
        cat_map = {"预订": "booking", "船上": "onboard", "岸上": "shore", "booking": "booking", "onboard": "onboard", "shore": "shore"}
        cat_key = cat_map.get(category)
        if cat_key and cat_key in TIPS:
            output = f"💡 **邮轮{category}贴士**\n\n"
            for i, tip in enumerate(TIPS[cat_key], 1):
                output += f"{i}. {tip}\n"
            return output
        return f"未找到类别'{category}'，支持：预订、船上、岸上"

    output = "💡 **邮轮旅行全攻略**\n\n"
    for cat_key, cat_tips in TIPS.items():
        cat_name = {"booking": "预订篇", "onboard": "船上篇", "shore": "岸上篇"}[cat_key]
        output += f"**{cat_name}**：\n"
        for i, tip in enumerate(cat_tips, 1):
            output += f"{i}. {tip}\n"
        output += "\n"
    return output


# 工具映射
TOOLS = {
    "search": search,
    "detail": detail,
    "tips": tips
}

if __name__ == "__main__":
    import sys
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "search"
    tool_args = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            tool_args[k] = v
    func = TOOLS.get(tool_name)
    if func:
        print(func(**tool_args))
    else:
        print(f"未知工具: {tool_name}, 可用: {list(TOOLS.keys())}")

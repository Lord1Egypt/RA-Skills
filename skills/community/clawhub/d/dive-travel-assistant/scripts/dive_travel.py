#!/usr/bin/env python3
"""潜水旅行助手 - Dive Travel Assistant
7个工具覆盖潜水全链路：潜点搜索/考证指南/安全检查 + 机票/酒店/交通/美食预订
国内走飞猪+高德，国际走RG，自动分流
"""
import os
import json
import sys
import urllib.request
import urllib.error

# ============ 代理配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
RG_PROXY = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
TIMEOUT = 30

# ============ 国内城市列表 ============
DOMESTIC_CITIES = [
    "三亚", "海口", "万宁", "琼海", "陵水", "深圳", "珠海", "广州", "汕头", "湛江",
    "厦门", "福州", "泉州", "北海", "南宁", "青岛", "大连", "威海", "烟台",
    "杭州", "上海", "北京", "成都", "昆明", "丽江", "大理", "桂林", "长沙",
    "武汉", "南京", "苏州", "天津", "哈尔滨", "长春", "沈阳", "西安", "郑州",
    "拉萨", "千岛湖", "抚仙湖", "涠洲岛",
]


def _is_domestic(location):
    """判断是否国内目的地"""
    for c in DOMESTIC_CITIES:
        if c in location:
            return True
    # 国际常见潜水目的地
    intl_keywords = [
        "马尔代夫", "仙本那", "巴厘岛", "普吉", "帕劳", "斐济", "大堡礁",
        "夏威夷", "冲绳", "宿务", "薄荷", "长滩", "苏梅", "甲米",
        "红海", "加拉帕戈斯", "伯利兹", "帕劳", "图兰奔", "蓝壁",
        "诗巴丹", "西巴丹", "斯米兰", "丽贝岛", "皮皮岛",
        "巴布亚", "密克罗尼西亚", "塞班", "关岛", "毛里求斯", "塞舌尔",
        "墨西哥", "古巴", "哥斯达黎加", "洪都拉斯", "哥伦比亚",
        "埃及", "约旦", "泰国", "马来西亚", "印尼", "菲律宾", "越南",
        "日本", "韩国", "澳大利亚", "新西兰", "美国", "加拿大",
        "法国", "意大利", "西班牙", "希腊", "克罗地亚", "土耳其",
        "南非", "莫桑比克", "坦桑尼亚",
    ]
    for k in intl_keywords:
        if k in location:
            return False
    # 默认按国内处理
    return True


# ============ 代理调用 ============
def _call_proxy(url, payload, token_header="X-Proxy-Token"):
    """通用代理调用"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers[token_header] = PROXY_TOKEN
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}: {err}"}
    except Exception as e:
        return {"error": str(e)}


def _call_fliggy(rtype, params):
    """飞猪代理"""
    return _call_proxy(FLIGGY_PROXY, {"type": rtype, "params": params})


def _call_rg(api_type, params):
    """RG代理"""
    headers_kw = "Authorization"
    body = json.dumps({"type": api_type, "params": params}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers["Authorization"] = f"Bearer {PROXY_TOKEN}"
    req = urllib.request.Request(RG_PROXY, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}: {err}"}
    except Exception as e:
        return {"error": str(e)}


def _call_gaode(api_type, params):
    """高德代理"""
    result = _call_proxy(GAODE_PROXY, {"type": api_type, "params": params}, "X-Proxy-Token")
    if isinstance(result, dict) and result.get("code") == 0 and "data" in result:
        return result["data"]
    return result


# ============================================================
# 第一组：本地数据工具 (3个)
# ============================================================

# ---------- 潜点数据库 ----------
DIVE_SITES = {
    # ===== 国内潜点 =====
    "蜈支洲岛": {
        "location": "海南三亚", "country": "中国", "region": "国内",
        "level": "初级-高级", "type": "珊瑚礁/峭壁",
        "best_season": "3-5月,10-12月", "visibility": "8-20m",
        "water_temp": "22-29°C", "max_depth": "30m",
        "highlights": ["珊瑚礁群", "热带鱼群", "海胆海星", "夜潜"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "三亚凤凰机场(SYX)",
        "tips": "三亚最知名潜点，全年可潜，能见度冬季最佳。适合考证和体验潜水。潜店密集，价格透明。",
    },
    "分界洲岛": {
        "location": "海南陵水", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "4-10月", "visibility": "6-15m",
        "water_temp": "24-29°C", "max_depth": "25m",
        "highlights": ["活体珊瑚", "沉船", "海龟偶遇", "海豚表演区外海"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "三亚凤凰机场(SYX)/海口美兰机场(HAK)",
        "tips": "海南唯一活体珊瑚保护区，有沉船人工鱼礁。海水清澈度优于蜈支洲。门票含船票。",
    },
    "西沙群岛": {
        "location": "海南三沙", "country": "中国", "region": "国内",
        "level": "中级-高级", "type": "珊瑚礁/峭壁",
        "best_season": "3-6月,10-12月", "visibility": "20-40m",
        "water_temp": "24-30°C", "max_depth": "40m+",
        "highlights": ["顶级能见度", "原始珊瑚", "鲨鱼", "海狼风暴", "大型鱼群"],
        "cert_required": "AOW+50潜", "dive_type": "船宿",
        "nearby_airport": "海口/三亚(转船4-16小时)",
        "tips": "国内天花板级潜点，能见度堪比马尔代夫。需提前报备，只能走正规渠道。4-7天船宿行程。AOW+50潜是硬性要求。",
    },
    "亚龙湾": {
        "location": "海南三亚", "country": "中国", "region": "国内",
        "level": "初级", "type": "珊瑚礁/沙地",
        "best_season": "全年", "visibility": "5-12m",
        "water_temp": "22-29°C", "max_depth": "15m",
        "highlights": ["体验潜水首选", "热带鱼群", "海星海胆", "拍照友好"],
        "cert_required": "无(体验潜)/OW", "dive_type": "岸潜",
        "nearby_airport": "三亚凤凰机场(SYX)",
        "tips": "最适合第一次体验潜水和考证。酒店潜店一体，岸潜直接下水。能见度一般但生物丰富。",
    },
    "百福湾": {
        "location": "海南三亚", "country": "中国", "region": "国内",
        "level": "中级", "type": "峭壁/珊瑚礁",
        "best_season": "3-6月,10-12月", "visibility": "10-20m",
        "water_temp": "23-29°C", "max_depth": "28m",
        "highlights": ["峭壁潜", "海扇", "海龟", "微距生物"],
        "cert_required": "OW以上", "dive_type": "船潜",
        "nearby_airport": "三亚凤凰机场(SYX)",
        "tips": "三亚少有的峭壁潜点，适合想体验深度和峭壁的潜水员。船潜10分钟即达。",
    },
    "加井岛": {
        "location": "海南万宁", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "4-10月", "visibility": "8-18m",
        "water_temp": "24-29°C", "max_depth": "20m",
        "highlights": ["珊瑚花园", "小丑鱼", "砗磲", "无人岛体验"],
        "cert_required": "OW以上/体验潜", "dive_type": "船潜",
        "nearby_airport": "海口美兰机场(HAK)/三亚凤凰机场(SYX)",
        "tips": "万宁小众潜点，人少水清，适合不想挤蜈支洲的潜水员。无人岛环境原始。",
    },
    "西岛": {
        "location": "海南三亚", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁/沙地",
        "best_season": "全年", "visibility": "6-15m",
        "water_temp": "22-29°C", "max_depth": "20m",
        "highlights": ["珊瑚礁", "海星", "热带鱼", "性价比高"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜/船潜",
        "nearby_airport": "三亚凤凰机场(SYX)",
        "tips": "比蜈支洲性价比更高，潜水+海岛一日游好选择。适合新手练技巧。",
    },
    "双帆石": {
        "location": "海南三亚", "country": "中国", "region": "国内",
        "level": "中级-高级", "type": "礁石/峭壁",
        "best_season": "3-5月,10-12月", "visibility": "10-25m",
        "water_temp": "22-28°C", "max_depth": "35m",
        "highlights": ["大型鱼群", "礁石穿越", "鹰鳐", "海狼群"],
        "cert_required": "AOW推荐", "dive_type": "船潜",
        "nearby_airport": "三亚凤凰机场(SYX)",
        "tips": "三亚进阶潜点，有洋流时能见到大型鱼群。需AOW级别才更安全。",
    },
    "深圳鹿咀杨梅坑": {
        "location": "广东深圳", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "5-10月", "visibility": "3-8m",
        "water_temp": "20-28°C", "max_depth": "12m",
        "highlights": ["珊瑚", "小丑鱼", "海胆", "近深圳"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜",
        "nearby_airport": "深圳宝安机场(SZX)",
        "tips": "深圳最近的潜点，岸潜方便。能见度一般，适合练习和周末刷潜。台风季避开水浑期。",
    },
    "深圳金沙湾": {
        "location": "广东深圳", "country": "中国", "region": "国内",
        "level": "初级", "type": "珊瑚礁/沙地",
        "best_season": "5-10月", "visibility": "3-8m",
        "water_temp": "20-28°C", "max_depth": "10m",
        "highlights": ["珊瑚", "海星", "热带鱼", "考证练习"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜",
        "nearby_airport": "深圳宝安机场(SZX)",
        "tips": "深圳东部潜点，适合OW考证和练习。夏季能见度好时还不错。",
    },
    "三门岛": {
        "location": "广东深圳", "country": "中国", "region": "国内",
        "level": "中级", "type": "珊瑚礁/峭壁",
        "best_season": "5-10月", "visibility": "5-12m",
        "water_temp": "20-28°C", "max_depth": "20m",
        "highlights": ["海扇", "珊瑚", "海胆", "岛屿穿越"],
        "cert_required": "OW以上", "dive_type": "船潜",
        "nearby_airport": "深圳宝安机场(SZX)",
        "tips": "深圳远海潜点，需船潜出岛。水下生物比近岸丰富，适合周末出海。",
    },
    "珠海庙湾岛": {
        "location": "广东珠海", "country": "中国", "region": "国内",
        "level": "中级", "type": "珊瑚礁",
        "best_season": "5-10月", "visibility": "8-15m",
        "water_temp": "22-28°C", "max_depth": "18m",
        "highlights": ["珊瑚覆盖率广东最高", "海胆", "热带鱼", "原始海岛"],
        "cert_required": "OW以上", "dive_type": "船潜",
        "nearby_airport": "珠海金湾机场(ZUH)",
        "tips": "广东能见度最好的潜点之一，需从珠海/深圳坐船2小时。周末热门，建议提前订船。",
    },
    "珠海外伶仃岛": {
        "location": "广东珠海", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "5-10月", "visibility": "5-12m",
        "water_temp": "22-28°C", "max_depth": "15m",
        "highlights": ["珊瑚", "海星", "海胆", "周末潜水"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜/船潜",
        "nearby_airport": "珠海金湾机场(ZUH)",
        "tips": "珠海离岛，有岸潜点也有船潜点。适合周末短途潜水游。",
    },
    "涠洲岛": {
        "location": "广西北海", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁/火山岩",
        "best_season": "4-11月", "visibility": "5-15m",
        "water_temp": "22-29°C", "max_depth": "20m",
        "highlights": ["火山岛地质", "珊瑚礁", "布氏鲸(2-4月)", "海蚀地貌"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜/船潜",
        "nearby_airport": "北海福成机场(BHY)",
        "tips": "中国最年轻火山岛，2-4月有机会看到布氏鲸！水下火山岩地貌独特。需从北海坐船1.5小时。",
    },
    "南宁洞潜": {
        "location": "广西南宁", "country": "中国", "region": "国内",
        "level": "高级", "type": "洞穴",
        "best_season": "全年", "visibility": "10-30m+",
        "water_temp": "20-24°C", "max_depth": "50m+",
        "highlights": ["世界级洞潜", "地下河", "钟乳石", "清澈地下水"],
        "cert_required": "洞穴潜水专长+Cave CCR", "dive_type": "洞穴潜",
        "nearby_airport": "南宁吴圩机场(NNG)",
        "tips": "国内唯一世界级洞潜地，极高风险。需洞穴潜水认证+丰富经验。非专业人员严禁尝试！",
    },
    "千岛湖水下古城": {
        "location": "浙江杭州", "country": "中国", "region": "国内",
        "level": "中级-高级", "type": "淡水/古迹",
        "best_season": "5-10月", "visibility": "3-8m",
        "water_temp": "8-24°C", "max_depth": "30m",
        "highlights": ["水下古城遗址", "牌坊", "民居", "淡水生态"],
        "cert_required": "AOW+干式专长推荐", "dive_type": "船潜",
        "nearby_airport": "杭州萧山机场(HGH)",
        "tips": "国内独一无二的潜水体验——在水下看古城！水温低需干衣或厚湿衣。能见度有限但人文价值极高。",
    },
    "抚仙湖": {
        "location": "云南玉溪", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "淡水",
        "best_season": "5-10月", "visibility": "5-12m",
        "water_temp": "12-22°C", "max_depth": "20m",
        "highlights": ["高原深水湖", "抗浪鱼", "水下古建筑遗迹", "清澈水质"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "昆明长水机场(KMG)",
        "tips": "中国最深淡水湖，高原潜水注意海拔。水温低需5mm以上湿衣。独特的淡水潜水体验。",
    },
    "小琉球": {
        "location": "台湾屏东", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "4-11月", "visibility": "10-25m",
        "water_temp": "24-29°C", "max_depth": "25m",
        "highlights": ["海龟天堂", "珊瑚覆盖率极高", "自由潜热门", "小岛环潜"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜/船潜",
        "nearby_airport": "高雄小港机场(KHH)",
        "tips": "台湾海龟密度最高的地方，几乎每潜都能看到。自由潜水也热门。从东港坐船20分钟。",
    },
    "绿岛": {
        "location": "台湾台东", "country": "中国", "region": "国内",
        "level": "中级-高级", "type": "珊瑚礁/峭壁",
        "best_season": "4-11月", "visibility": "15-35m",
        "water_temp": "24-29°C", "max_depth": "35m+",
        "highlights": ["大香菇(巨型海扇)", "钢铁礁", "燕鱼群", "顶级能见度"],
        "cert_required": "AOW推荐", "dive_type": "岸潜/船潜",
        "nearby_airport": "台东机场(TTT)",
        "tips": "台湾最佳潜点，能见度可达35m+！大香菇是标志性景观。洋流强时适合漂流潜。从台东坐船50分钟或小飞机。",
    },
    "垦丁": {
        "location": "台湾屏东", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "珊瑚礁",
        "best_season": "4-10月", "visibility": "8-20m",
        "water_temp": "24-29°C", "max_depth": "25m",
        "highlights": ["珊瑚礁", "热带鱼", "夜潜", "合界流潜"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "tips": "台湾最南端潜点，岸潜方便。合界流潜需AOW。垦丁潜店选择多，考证性价比高。",
        "nearby_airport": "高雄小港机场(KHH)/恒春机场(HCN)",
    },
    "青岛": {
        "location": "山东青岛", "country": "中国", "region": "国内",
        "level": "初级-中级", "type": "温带礁石/海藻林",
        "best_season": "6-9月", "visibility": "3-8m",
        "water_temp": "16-24°C", "max_depth": "15m",
        "highlights": ["海藻林", "海参", "海星", "温带海洋生态"],
        "cert_required": "OW以上", "dive_type": "岸潜",
        "nearby_airport": "青岛流亭机场(TAO)/胶东机场(TAO)",
        "tips": "北方夏季潜水地，海藻林景观独特。水温低需5mm+湿衣。能见度一般但体验不同生态。",
    },
    "大连": {
        "location": "辽宁大连", "country": "中国", "region": "国内",
        "level": "中级", "type": "温带礁石",
        "best_season": "7-9月", "visibility": "3-6m",
        "water_temp": "14-22°C", "max_depth": "15m",
        "highlights": ["海参", "海胆", "海带林", "北方潜水"],
        "cert_required": "OW以上+干衣推荐", "dive_type": "岸潜",
        "nearby_airport": "大连周水子机场(DLC)",
        "tips": "北方潜水窗口期短，7-9月最佳。干衣更舒适。适合体验温带海域的潜水员。",
    },
    # ===== 国际潜点 =====
    "仙本那诗巴丹": {
        "location": "马来西亚沙巴", "country": "马来西亚", "region": "东南亚",
        "level": "高级", "type": "峭壁/海狼风暴",
        "best_season": "4-12月", "visibility": "20-40m",
        "water_temp": "26-29°C", "max_depth": "40m+",
        "highlights": ["海狼风暴", "杰克鱼风暴", "峭壁潜", "鲨鱼", "海龟", "世界顶级潜点"],
        "cert_required": "AOW+20潜", "dive_type": "船潜",
        "nearby_airport": "斗湖机场(TWU)",
        "tips": "世界十大潜点之一，每天限120个名额需抢。海狼风暴和杰克鱼风暴是标志性景观。从斗湖机场到仙本那1.5小时车程，再船潜45分钟。",
    },
    "仙本那马布岛": {
        "location": "马来西亚沙巴", "country": "马来西亚", "region": "东南亚",
        "level": "初级-中级", "type": "微距/珊瑚礁",
        "best_season": "全年", "visibility": "10-20m",
        "water_temp": "26-29°C", "max_depth": "25m",
        "highlights": ["微距天堂", "拟态章鱼", "火焰墨鱼", "蓝环章鱼", "海龟"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "斗湖机场(TWU)",
        "tips": "微距摄影师天堂，水下生物密度极高。和诗巴丹同区域，可搭配行程。住宿有水上屋和岛上度假村。",
    },
    "马尔代夫": {
        "location": "马尔代夫", "country": "马尔代夫", "region": "印度洋",
        "level": "中级-高级", "type": "峭壁/通道潜/珊瑚礁",
        "best_season": "1-4月(干季)", "visibility": "15-40m",
        "water_temp": "26-29°C", "max_depth": "35m+",
        "highlights": ["魔鬼鱼", "鲸鲨", "通道潜", "珊瑚礁", "度假村潜水"],
        "cert_required": "AOW推荐", "dive_type": "船潜/度假村潜",
        "nearby_airport": "马累机场(MLE)",
        "tips": "度假村潜水和船宿都极成熟。通道潜(Kandu)看大鱼是特色。AOW可享受更深通道潜。直飞航班北京/上海/广州出发。",
    },
    "帕劳": {
        "location": "帕劳", "country": "帕劳", "region": "太平洋",
        "level": "中级-高级", "type": "峭壁/蓝洞/沉船",
        "best_season": "11-5月", "visibility": "15-35m",
        "water_temp": "27-30°C", "max_depth": "40m+",
        "highlights": ["蓝角", "蓝洞", "水母湖", "沉船", "鲨鱼城", "无毒水母"],
        "cert_required": "AOW+20潜", "dive_type": "船潜",
        "nearby_airport": "帕劳机场(ROR)",
        "tips": "世界顶级潜点之一，蓝角看鲨鱼是必体验。水母湖浮潜也是特色。香港/台北有直飞或经停航班。",
    },
    "巴厘岛图兰奔": {
        "location": "印尼巴厘岛", "country": "印尼", "region": "东南亚",
        "level": "初级-高级", "type": "沉船/峭壁",
        "best_season": "4-11月", "visibility": "10-25m",
        "water_temp": "25-28°C", "max_depth": "35m",
        "highlights": ["自由号沉船", "峭壁潜", "微距", "翻车鱼(季节性)"],
        "cert_required": "OW以上", "dive_type": "岸潜",
        "nearby_airport": "巴厘岛登巴萨机场(DPS)",
        "tips": "自由号沉船是世界最著名的岸潜沉船之一，从海滩走入即到。适合各级别潜水员。翻车鱼7-10月出现。",
    },
    "蓝壁海峡": {
        "location": "印尼北苏拉威西", "country": "印尼", "region": "东南亚",
        "level": "初级-高级", "type": "微距/珊瑚礁",
        "best_season": "全年", "visibility": "8-20m",
        "water_temp": "26-29°C", "max_depth": "25m",
        "highlights": ["微距世界之巅", "拟态章鱼", "各种裸鳃类", "豆丁海马", "火焰墨鱼"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "万鸦老机场(MDC)",
        "tips": "世界微距摄影圣地，1次潜水可看到20+种裸鳃类。和邦卡岛度假村搭配。从万鸦老机场1小时车程。",
    },
    "斯米兰群岛": {
        "location": "泰国攀牙", "country": "泰国", "region": "东南亚",
        "level": "中级-高级", "type": "珊瑚礁/巨石",
        "best_season": "11月-次年5月(开放期)", "visibility": "20-35m",
        "water_temp": "27-30°C", "max_depth": "35m+",
        "highlights": ["巨石地形", "鹰鳐", "鲸鲨", "海龟", "清澈海水"],
        "cert_required": "AOW推荐", "dive_type": "船宿/船潜",
        "nearby_airport": "普吉机场(HKT)/考拉",
        "tips": "泰国最佳潜点，每年只开放半年。船宿2-4天是最佳方式。鲸鲨和鹰鳐概率高。考拉码头出发。",
    },
    "普吉岛": {
        "location": "泰国普吉", "country": "泰国", "region": "东南亚",
        "level": "初级-中级", "type": "珊瑚礁/沉船",
        "best_season": "11月-次年4月", "visibility": "10-25m",
        "water_temp": "27-30°C", "max_depth": "25m",
        "highlights": ["沉船King Cruiser", "海鳗花园", "鲨鱼角", "考证热门"],
        "cert_required": "OW以上/体验潜", "dive_type": "船潜",
        "nearby_airport": "普吉机场(HKT)",
        "tips": "考证+度假完美结合。King Cruiser沉船30m深适合AOW。潜店选择极多。国内多地直飞。",
    },
    "宿务莫阿尔博阿尔": {
        "location": "菲律宾宿务", "country": "菲律宾", "region": "东南亚",
        "level": "初级-中级", "type": "沙丁鱼风暴/珊瑚礁",
        "best_season": "12月-次年5月", "visibility": "10-25m",
        "water_temp": "26-29°C", "max_depth": "25m",
        "highlights": ["沙丁鱼风暴", "海龟", "珊瑚礁", "峭壁潜"],
        "cert_required": "OW以上", "dive_type": "岸潜",
        "nearby_airport": "宿务机场(CEB)",
        "tips": "沙丁鱼风暴是标志性景观，岸潜即可看到！3m深度就能看到百万沙丁鱼。性价比极高的潜点。",
    },
    "薄荷岛": {
        "location": "菲律宾薄荷", "country": "菲律宾", "region": "东南亚",
        "level": "初级-中级", "type": "珊瑚礁/峭壁",
        "best_season": "12月-次年5月", "visibility": "10-25m",
        "water_temp": "26-29°C", "max_depth": "25m",
        "highlights": ["巴里卡萨大断层", "海龟", "珊瑚花园", "眼镜猴"],
        "cert_required": "OW以上", "dive_type": "船潜",
        "nearby_airport": "塔比拉兰机场(TAG)",
        "tips": "巴里卡萨大断层从3m直降到700m，视觉震撼。海龟密度极高。岛上还有眼镜猴保护区。国内直飞宿务转船。",
    },
    "冲绳": {
        "location": "日本冲绳", "country": "日本", "region": "东亚",
        "level": "初级-中级", "type": "珊瑚礁/洞穴",
        "best_season": "4-11月", "visibility": "15-30m",
        "water_temp": "22-29°C", "max_depth": "25m",
        "highlights": ["青之洞窟", "珊瑚礁", "海龟", "曼塔", "日式潜水体验"],
        "cert_required": "OW以上/体验潜", "dive_type": "岸潜/船潜",
        "nearby_airport": "那霸机场(OKA)",
        "tips": "青之洞窟是必打卡，蓝色光线美到窒息。潜店服务日式精致。国内多地直飞那霸。适合潜水+日本旅行。",
    },
    "大堡礁": {
        "location": "澳大利亚昆士兰", "country": "澳大利亚", "region": "大洋洲",
        "level": "初级-高级", "type": "珊瑚礁/峭壁",
        "best_season": "6-10月(南半球冬季)", "visibility": "15-30m",
        "water_temp": "22-27°C", "max_depth": "35m+",
        "highlights": ["世界最大珊瑚礁", "小丑鱼", "海龟", "鲨鱼", "须鲸(季节)", "船宿"],
        "cert_required": "OW以上", "dive_type": "船潜/船宿",
        "nearby_airport": "凯恩斯机场(CNS)",
        "tips": "世界自然遗产，从凯恩斯出发。外堡礁能见度和生物都更好。3-7天船宿是最佳方式。需澳洲签证。",
    },
    "红海": {
        "location": "埃及", "country": "埃及", "region": "中东/非洲",
        "level": "中级-高级", "type": "峭壁/沉船/珊瑚礁",
        "best_season": "3-5月,9-11月", "visibility": "20-40m",
        "water_temp": "21-28°C", "max_depth": "40m+",
        "highlights": ["世界级沉船", "峭壁潜", "鲨鱼", "珊瑚花园", "能见度极高"],
        "cert_required": "AOW+20潜", "dive_type": "船宿/船潜",
        "nearby_airport": "赫尔格达机场(HRG)/沙姆沙伊赫(SSH)",
        "tips": "世界顶级潜点之一，Thistlegorm沉船是必潜。红海能见度常超30m。船宿7天是最佳体验。注意签证和安全区域。",
    },
    "加拉帕戈斯": {
        "location": "厄瓜多尔", "country": "厄瓜多尔", "region": "南美",
        "level": "专家", "type": "峭壁/强流",
        "best_season": "6-11月", "visibility": "10-25m",
        "water_temp": "16-24°C(寒流)", "max_depth": "35m+",
        "highlights": ["锤头鲨群", "鲸鲨", "海鬣蜥", "海狮", "加拉帕戈斯鲨"],
        "cert_required": "AOW+50潜+高氧", "dive_type": "船宿",
        "nearby_airport": "基多/瓜亚基尔(转加拉帕戈斯)",
        "tips": "世界潜水终极目标，没有之一。锤头鲨群和鲸鲨是标志。水温极低需7mm+头套。费用极高(船宿$5000+/周)。必须船宿。",
    },
    "夏威夷": {
        "location": "美国夏威夷", "country": "美国", "region": "太平洋",
        "level": "初级-高级", "type": "珊瑚礁/峭壁/沉船",
        "best_season": "4-12月", "visibility": "15-30m",
        "water_temp": "24-27°C", "max_depth": "35m",
        "highlights": ["魔鬼鱼夜潜", "沉船", "海龟", "鲸鱼(冬)", "火山地貌"],
        "cert_required": "OW以上", "dive_type": "岸潜/船潜",
        "nearby_airport": "檀香山机场(HNL)/科纳机场(KOA)",
        "tips": "科纳魔鬼鱼夜潜是世界独特体验。大岛锤头鲨也很有名。需美国签证/ESTA。适合潜水+度假。",
    },
}


# ---------- 考证数据库 ----------
CERT_GUIDE = {
    "OW": {
        "full_name": "Open Water Diver 开放水域潜水员",
        "org": "PADI/SSI/CMAS",
        "prerequisite": "会游泳，能连续游泳200m或浮潜300m，能漂浮/踩水10分钟",
        "course_content": ["理论课(5单元)", "平静水域练习(泳池)", "开放水域4潜"],
        "duration": "3-4天",
        "cost_range": "国内2000-3500元 / 东南亚1500-2500元",
        "max_depth": "18m",
        "tips": "第一次考证推荐选东南亚(泰国/菲律宾/马来西亚)，价格便宜水温好。国内三亚也可以。别选最便宜的潜店，安全更重要。",
        "popular_locations": ["普吉岛", "薄荷岛", "仙本那", "三亚", "冲绳"],
    },
    "AOW": {
        "full_name": "Advanced Open Water Diver 进阶开放水域潜水员",
        "org": "PADI/SSI",
        "prerequisite": "OW证书",
        "course_content": ["5次专长潜水(深潜+导航必选+3个自选)", "无考试"],
        "duration": "2天",
        "cost_range": "国内1500-2500元 / 东南亚1200-2000元",
        "max_depth": "30m",
        "tips": "OW后最值得进的等级。选专长建议：深潜+导航+高氧+夜潜+顶尖中性浮力。2天拿证非常轻松。",
        "popular_locations": ["仙本那", "普吉岛", "巴厘岛", "三亚"],
    },
    "Rescue": {
        "full_name": "Rescue Diver 救援潜水员",
        "org": "PADI",
        "prerequisite": "AOW+EFR急救证书+20潜记录",
        "course_content": ["自救", "识别潜水员压力", "紧急管理", "救援恐慌潜水员", "救援无反应潜水员"],
        "duration": "3-4天",
        "cost_range": "2500-4000元",
        "max_depth": "30m",
        "tips": "从休闲娱乐到专业分水岭。学完后你会成为水下更安全的伙伴。强烈推荐！也是走向DM的必经之路。",
        "popular_locations": ["各地均可", "推荐和OW/AOW同地完成"],
    },
    "DM": {
        "full_name": "Divemaster 潜水长",
        "org": "PADI",
        "prerequisite": "Rescue+60潜+18岁以上+体检",
        "course_content": ["潜水知识深化", "协助教学", "带领潜水", "潜水中心运营"],
        "duration": "2周-3个月(实习制)",
        "cost_range": "5000-15000元(不含食宿)",
        "max_depth": "40m",
        "tips": "专业级别第一步，可以带潜水员下水、协助教练教学。很多潜店招DM实习(免费住宿+潜水)。想往职业方向走的第一步。",
        "popular_locations": ["仙本那", "普吉岛", "巴厘岛", "马尔代夫"],
    },
    "Instructor": {
        "full_name": "Open Water Scuba Instructor 开放水域潜水教练",
        "org": "PADI",
        "prerequisite": "DM+100潜+6个月以上DM经验+IDC课程",
        "course_content": ["IDC教练发展课程", "IE考试"],
        "duration": "2-3周",
        "cost_range": "10000-25000元",
        "max_depth": "40m",
        "tips": "可以独立教授OW-AOW课程。全球就业前景好，热带海岛度假村长期招聘。是很多潜水员的人生转折点。",
        "popular_locations": ["仙本那", "普吉岛", "巴厘岛", "三亚"],
    },
    # 专长证书
    "Nitrox": {
        "full_name": "Enriched Air Diver 高氧空气潜水员",
        "org": "PADI",
        "prerequisite": "OW",
        "course_content": ["高氧理论", "氧气分析", "高氧潜水计划"],
        "duration": "1天(可线上理论)",
        "cost_range": "500-1200元",
        "max_depth": "按当前等级",
        "tips": "最实用的专长！延长免减压极限，潜水后更不累。很多度假村提供免费Nitrox。OW即可考，强烈推荐。",
        "popular_locations": ["各地均可"],
    },
    "Deep": {
        "full_name": "Deep Diver 深潜专长",
        "org": "PADI",
        "prerequisite": "AOW",
        "course_content": ["深潜计划", "气体 narcosis", "深潜4次"],
        "duration": "2天",
        "cost_range": "1000-2000元",
        "max_depth": "40m",
        "tips": "解锁40m深度，看沉船和深水生物必备。和Nitrox搭配最佳。",
        "popular_locations": ["红海", "冲绳", "斯米兰"],
    },
    "Wreck": {
        "full_name": "Wreck Diver 沉船潜水员",
        "org": "PADI",
        "prerequisite": "AOW",
        "course_content": ["沉船潜水技巧", "穿越线使用", "沉船4潜"],
        "duration": "2天",
        "cost_range": "1000-2000元",
        "max_depth": "按当前等级",
        "tips": "进入沉船内部需要这个专长。图兰奔自由号、红海Thistlegorm等顶级沉船都在等你。安全第一，严禁无证穿越！",
        "popular_locations": ["红海", "巴厘岛", "楚克", "帕劳"],
    },
    "Drift": {
        "full_name": "Drift Diver 漂流潜水员",
        "org": "PADI",
        "prerequisite": "OW",
        "course_content": ["漂流潜技巧", "SMB使用", "漂流潜2潜"],
        "duration": "1天",
        "cost_range": "600-1200元",
        "max_depth": "按当前等级",
        "tips": "有流的潜点必备技能。帕劳蓝角、马尔代夫通道都需要漂流潜技巧。学起来很快，1天搞定。",
        "popular_locations": ["帕劳", "马尔代夫", "科科斯"],
    },
    "Cave": {
        "full_name": "Cave Diver 洞穴潜水员",
        "org": "TDI/GUE/IANTD",
        "prerequisite": "AOW+50潜+深渊/沉船专长推荐",
        "course_content": ["洞穴潜水计划", "引导线使用", "气体管理", "紧急程序", "多级课程(Cavern→Intro→Full Cave)"],
        "duration": "1-2周(分3级)",
        "cost_range": "5000-15000元(全3级)",
        "max_depth": "按等级",
        "tips": "潜水最危险的专长之一，也是最美最震撼的体验。必须走正规培训(TDI/GUE)。南宁洞潜、墨西哥天然井是目的地。非认证严禁进洞！",
        "popular_locations": ["墨西哥天然井", "南宁", "佛州Ginnie Springs", "澳洲袋鼠岛"],
    },
}


# ---------- 安全数据库 ----------
SAFETY_DB = {
    "decompression_sickness": {
        "name": "减压病(DCS)",
        "symptoms": ["关节疼痛", "皮肤瘙痒/大理石纹", "头晕恶心", "呼吸困难", "肢体麻木/无力"],
        "prevention": [
            "严格执行免减压极限或潜水计划",
            "上升速度不超过18m/min，最后5m做3-5分钟安全停留",
            "潜水后24小时内不飞行",
            "连续潜水遵守水面休息时间",
            "保持良好身体状态，潜水前充分休息",
            "避免潜水后剧烈运动、按摩、热水浴",
        ],
        "emergency": [
            "立即停止潜水",
            "如有氧气立即吸纯氧(15L/min)",
            "让患者平躺，不要坐起或站立",
            "联系当地减压舱(DAN热线+1-919-684-9111)",
            "记录潜水剖面供医生参考",
            "尽快送往有减压舱的医院",
        ],
    },
    "barotrauma": {
        "name": "气压伤",
        "symptoms": ["耳朵剧痛", "鼻窦疼痛", "面罩挤压", "牙齿疼痛"],
        "prevention": [
            "下潜时频繁做耳压平衡(瓦尔萨尔瓦/弗兰泽尔)",
            "感冒/鼻塞时不下潜",
            "下潜速度控制，不适即停止",
            "面镜平衡：鼻呼气入面镜",
        ],
        "emergency": [
            "感到不适立即停止下潜",
            "上升1-2m尝试平衡",
            "无法平衡则终止潜水",
            "出水后持续疼痛需就医",
        ],
    },
    "marine_life": {
        "name": "海洋生物伤害",
        "types": {
            "水母蜇伤": "用醋冲洗30秒→热水浸泡45分钟→勿用淡水/尿液/酒精",
            "海胆扎伤": "用钳子取出刺→热水浸泡→观察是否感染",
            "狮子鱼/石头鱼": "热水浸泡(45°C)30-90分钟→就医(石头鱼需抗毒血清)",
            "珊瑚割伤": "清水冲洗→消毒→观察感染→严重就医",
            "鲨鱼": "极罕见→保持冷静→击打鼻子/眼睛→尽快出水",
        },
        "prevention": [
            "不触摸任何海洋生物",
            "穿潜水手套和全身水母衣",
            "注意脚下踩踏",
            "不喂鱼不追逐",
        ],
    },
    "current": {
        "name": "洋流安全",
        "types": {
            "沿岸流": "平行于海岸，不要对抗游回岸边，向与流垂直方向游",
            "离岸流": "向海外推，不要直接对抗，平行于岸游出流区再斜向游回",
            "上升流/下降流": "深度剧烈变化，立即抓参照物，充BCD缓慢上升，安全停留",
        },
        "prevention": [
            "潜水前了解当地洋流情况",
            "携带SMB(象拔)和哨子",
            "与潜伴保持联系",
            "漂流潜使用浮标",
            "携带潜水电脑表",
        ],
    },
    "dive_insurance": {
        "name": "潜水保险",
        "importance": "潜水意外可能需要减压舱治疗(单次费用数万元)和医疗后送(直升机后送费用可达数十万)，普通旅行险通常不覆盖潜水事故！",
        "recommendations": [
            "DAN(潜水员警报网络)：全球最权威潜水保险，年费约$35起，含减压舱+医疗后送",
            "潜水专属旅行险：覆盖潜水事故+正常旅行保障",
            "确认覆盖深度：部分保险仅覆盖30m以内",
            "确认覆盖活动：技术潜/洞穴潜/自由潜需确认是否在保",
        ],
    },
    "fitness": {
        "name": "潜水身体条件",
        "contraindications": [
            "感冒/鼻塞(影响耳压平衡)",
            "哮喘(严重者禁忌)",
            "心脏病/高血压(未控制)",
            "癫痫",
            "糖尿病(需医生评估)",
            "怀孕",
            "饮酒后(至少8小时后)",
            "潜水后24小时内飞行",
        ],
        "tips": [
            "每年做潜水体检(尤其40岁以上)",
            "服药期间咨询医生是否可潜水",
            "潜水前一晚充足睡眠",
            "潜水当天充分补水",
            "身体不适果断取消，永远可以下次再潜",
        ],
    },
}


# ============================================================
# 工具1: dive_site_search 潜点搜索
# ============================================================
def dive_site_search(keyword="", level="", region="", site_type="", limit=10, **kwargs):
    """搜索潜水点，支持按关键词/级别/区域/类型筛选"""
    results = []
    for name, info in DIVE_SITES.items():
        # 关键词匹配
        if keyword:
            kw = keyword.lower()
            match = (
                kw in name.lower()
                or kw in info.get("location", "").lower()
                or kw in info.get("country", "").lower()
                or any(kw in h for h in info.get("highlights", []))
            )
            if not match:
                continue
        # 级别筛选
        if level:
            lv = level.lower()
            site_lv = info.get("level", "").lower()
            if lv not in site_lv and not (
                (lv in ("初", "beginner", "ow") and "初级" in site_lv)
                or (lv in ("中", "intermediate", "aow") and "中级" in site_lv)
                or (lv in ("高", "advanced", "expert") and "高级" in site_lv)
            ):
                continue
        # 区域筛选
        if region:
            rg = region.lower()
            site_rg = info.get("region", "").lower()
            site_country = info.get("country", "").lower()
            site_loc = info.get("location", "").lower()
            if not (rg in site_rg or rg in site_country or rg in site_loc):
                continue
        # 类型筛选
        if site_type:
            st = site_type.lower()
            site_t = info.get("type", "").lower()
            site_dt = info.get("dive_type", "").lower()
            if not (st in site_t or st in site_dt):
                continue

        results.append({
            "name": name,
            "location": info.get("location", ""),
            "country": info.get("country", ""),
            "region": info.get("region", ""),
            "level": info.get("level", ""),
            "type": info.get("type", ""),
            "best_season": info.get("best_season", ""),
            "visibility": info.get("visibility", ""),
            "water_temp": info.get("water_temp", ""),
            "max_depth": info.get("max_depth", ""),
            "highlights": info.get("highlights", []),
            "cert_required": info.get("cert_required", ""),
            "dive_type": info.get("dive_type", ""),
            "nearby_airport": info.get("nearby_airport", ""),
            "tips": info.get("tips", ""),
        })

    if not results:
        return json.dumps({
            "message": f"未找到匹配的潜点",
            "suggestion": "试试搜索：三亚、仙本那、马尔代夫、沉船、洞穴 等",
            "available_regions": list(set(info["region"] for info in DIVE_SITES.values())),
        }, ensure_ascii=False, indent=2)

    results = results[:int(limit)]
    return json.dumps({
        "count": len(results),
        "sites": results,
    }, ensure_ascii=False, indent=2)


# ============================================================
# 工具2: dive_cert_guide 考证指南
# ============================================================
def dive_cert_guide(cert="", **kwargs):
    """查询潜水考证信息，从OW到教练和各专长"""
    if not cert:
        return json.dumps({
            "available_certs": list(CERT_GUIDE.keys()),
            "recommended_path": "OW → AOW → Nitrox/Deep专长 → Rescue → DM → Instructor",
            "quick_tip": "第一次考证选东南亚(价格低水温好)，最实用的进阶是AOW+Nitrox",
        }, ensure_ascii=False, indent=2)

    # 模糊匹配
    cert_lower = cert.lower()
    matched_key = None
    for key in CERT_GUIDE:
        if key.lower() == cert_lower or key.lower() in cert_lower or cert_lower in key.lower():
            matched_key = key
            break
    # 中文匹配
    if not matched_key:
        cn_map = {
            "开放水域": "OW", "初级": "OW", "入门": "OW",
            "进阶": "AOW", "高级": "AOW",
            "救援": "Rescue",
            "潜水长": "DM", "潜长": "DM",
            "教练": "Instructor",
            "高氧": "Nitrox", "富氧": "Nitrox",
            "深潜": "Deep",
            "沉船": "Wreck",
            "漂流": "Drift", "流潜": "Drift",
            "洞穴": "Cave", "洞潜": "Cave",
        }
        for cn, en in cn_map.items():
            if cn in cert_lower:
                matched_key = en
                break

    if not matched_key:
        return json.dumps({
            "error": f"未找到「{cert}」的考证信息",
            "available": list(CERT_GUIDE.keys()),
        }, ensure_ascii=False)

    info = CERT_GUIDE[matched_key]
    return json.dumps({
        "cert": matched_key,
        "full_name": info["full_name"],
        "org": info["org"],
        "prerequisite": info["prerequisite"],
        "course_content": info["course_content"],
        "duration": info["duration"],
        "cost_range": info["cost_range"],
        "max_depth": info["max_depth"],
        "tips": info["tips"],
        "popular_locations": info["popular_locations"],
    }, ensure_ascii=False, indent=2)


# ============================================================
# 工具3: dive_safety_check 安全检查
# ============================================================
def dive_safety_check(topic="", **kwargs):
    """查询潜水安全信息：减压病/气压伤/海洋生物/洋流/保险/身体条件"""
    if not topic:
        return json.dumps({
            "available_topics": list(SAFETY_DB.keys()),
            "quick_reminder": "最重要的3条：①不超过免减压极限 ②安全停留3-5分钟 ③潜水后24小时不飞行",
        }, ensure_ascii=False, indent=2)

    topic_lower = topic.lower()
    matched_key = None
    for key in SAFETY_DB:
        if key in topic_lower or topic_lower in key:
            matched_key = key
            break

    # 中文匹配
    if not matched_key:
        cn_map = {
            "减压": "decompression_sickness", "弯曲": "decompression_sickness", "dcs": "decompression_sickness",
            "气压": "barotrauma", "耳朵": "barotrauma", "耳压": "barotrauma",
            "生物": "marine_life", "水母": "marine_life", "海胆": "marine_life", "鲨鱼": "marine_life",
            "流": "current", "洋流": "current", "暗流": "current",
            "保险": "dive_insurance", "dan": "dive_insurance",
            "身体": "fitness", "体检": "fitness", "禁忌": "fitness",
        }
        for cn, en in cn_map.items():
            if cn in topic_lower:
                matched_key = en
                break

    if not matched_key:
        return json.dumps({
            "error": f"未找到「{topic}」的安全信息",
            "available_topics": list(SAFETY_DB.keys()),
        }, ensure_ascii=False)

    return json.dumps(SAFETY_DB[matched_key], ensure_ascii=False, indent=2)


# ============================================================
# 工具4: search_dive_flights 潜水机票搜索
# ============================================================
def search_dive_flights(origin="", destination="", date="", **kwargs):
    """搜索机票，国内走飞猪，国际走RG，自动分流"""
    if not origin or not destination or not date:
        return json.dumps({"error": "请提供origin(出发城市)、destination(到达城市)、date(日期YYYY-MM-DD)"}, ensure_ascii=False)

    # 查找目的地对应的潜点
    site_info = None
    site_name = None
    for name, info in DIVE_SITES.items():
        if destination in name or destination in info.get("location", "") or destination in info.get("nearby_airport", ""):
            site_info = info
            site_name = name
            break

    is_domestic = _is_domestic(destination)

    if is_domestic:
        # 国内走飞猪
        result = _call_fliggy("flight", {
            "origin": origin,
            "destination": destination,
            "date": date,
        })
        if isinstance(result, dict) and "error" in result:
            return json.dumps({"error": f"飞猪机票查询失败: {result['error']}"}, ensure_ascii=False)

        # 解析飞猪返回
        flights = result.get("flightInformationList") or result.get("data", {}).get("flightInformationList", []) if isinstance(result, dict) else []
        if not flights:
            return json.dumps({
                "message": f"未找到{origin}→{destination}({date})的航班",
                "suggestion": f"可尝试搜索附近机场：{site_info.get('nearby_airport', '请检查城市名')}" if site_info else "",
            }, ensure_ascii=False)

        output = []
        for f in flights[:8]:
            segs = f.get("fromSegments", [])
            seg_info = ""
            if segs:
                s = segs[0]
                dur = s.get("duration", "")
                dur_str = f"{int(dur)//60}h{int(dur)%60}m" if dur else ""
                seg_info = f"{s.get('flightNumber','')} {s.get('depAirport','')}→{s.get('arrAirport','')} {dur_str} {s.get('depTime','')}→{s.get('arrTime','')}"
            output.append({
                "segment": seg_info,
                "price": f.get("price", f.get("totalAdultPrice", "")),
                "bookingUrl": f.get("bookingUrl", ""),
            })

        return json.dumps({
            "type": "国内航班(飞猪)",
            "dive_site": site_name,
            "origin": origin,
            "destination": destination,
            "date": date,
            "count": len(flights),
            "flights": output,
        }, ensure_ascii=False, indent=2)
    else:
        # 国际走RG
        result = _call_rg("flight", {
            "origin": origin,
            "destination": destination,
            "date": date,
        })
        if isinstance(result, dict) and "error" in result:
            return json.dumps({"error": f"RG机票查询失败: {result['error']}"}, ensure_ascii=False)

        flights = result.get("flightInformationList", [])
        if not flights:
            return json.dumps({
                "message": f"未找到{origin}→{destination}({date})的国际航班",
                "suggestion": f"可尝试IATA代码搜索，如{site_info.get('nearby_airport', '')}" if site_info else "",
            }, ensure_ascii=False)

        output = []
        for f in flights[:8]:
            segs = f.get("fromSegments", [])
            seg_info = ""
            if segs:
                s = segs[0]
                dur = s.get("duration", "")
                dur_str = f"{int(dur)//60}h{int(dur)%60}m" if dur else ""
                seg_info = f"{s.get('flightNumber','')} {s.get('depAirport','')}→{s.get('arrAirport','')} {dur_str} {s.get('depTime','')}→{s.get('arrTime','')}"
            output.append({
                "segment": seg_info,
                "price": f.get("totalAdultPrice", ""),
                "score": f.get("fromSmartValueScore", ""),
                "bookingUrl": f.get("bookingUrl", ""),
            })

        return json.dumps({
            "type": "国际航班(RG)",
            "dive_site": site_name,
            "origin": origin,
            "destination": destination,
            "date": date,
            "count": len(flights),
            "flights": output,
        }, ensure_ascii=False, indent=2)


# ============================================================
# 工具5: search_dive_hotels 潜水酒店搜索
# ============================================================
def search_dive_hotels(city="", checkin="", checkout="", keyword="", **kwargs):
    """搜索酒店，国内走飞猪，国际走RG，自动分流"""
    if not city or not checkin or not checkout:
        return json.dumps({"error": "请提供city(城市)、checkin(入住日期)、checkout(离店日期)"}, ensure_ascii=False)

    # 查找对应的潜点
    site_info = None
    site_name = None
    for name, info in DIVE_SITES.items():
        if city in name or city in info.get("location", "") or city in info.get("country", ""):
            site_info = info
            site_name = name
            break

    is_domestic = _is_domestic(city)

    # 潜水相关关键词
    if not keyword and site_info:
        keyword = "潜水 潜店 度假村"

    if is_domestic:
        # 国内走飞猪
        params = {"city": city, "checkIn": checkin, "checkOut": checkout}
        if keyword:
            params["keyword"] = keyword
        result = _call_fliggy("hotel", params)

        if isinstance(result, dict) and "error" in result:
            return json.dumps({"error": f"飞猪酒店查询失败: {result['error']}"}, ensure_ascii=False)

        hotels = result.get("hotelInformationList") or result.get("data", {}).get("hotelInformationList", []) if isinstance(result, dict) else []
        if not hotels:
            return json.dumps({
                "message": f"未找到{city}({checkin}~{checkout})的酒店",
                "dive_tip": "建议搜索潜店附近的酒店或含潜水服务的度假村",
            }, ensure_ascii=False)

        output = []
        for h in hotels[:8]:
            output.append({
                "name": h.get("name", ""),
                "starRating": h.get("starRating", ""),
                "lowestPrice": h.get("price", {}).get("lowestPrice", h.get("lowestPrice", "")),
                "address": h.get("address", ""),
                "bookingUrl": h.get("bookingUrl", ""),
            })

        return json.dumps({
            "type": "国内酒店(飞猪)",
            "dive_site": site_name,
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
            "count": len(hotels),
            "hotels": output,
        }, ensure_ascii=False, indent=2)
    else:
        # 国际走RG
        result = _call_rg("hotel_search", {
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
        })

        if isinstance(result, dict) and "error" in result:
            return json.dumps({"error": f"RG酒店查询失败: {result['error']}"}, ensure_ascii=False)

        hotels = result.get("hotelInformationList", [])
        if not hotels:
            return json.dumps({
                "message": f"未找到{city}({checkin}~{checkout})的酒店",
                "dive_tip": "建议搜索潜店附近的酒店或含潜水服务的度假村",
            }, ensure_ascii=False)

        output = []
        for h in hotels[:8]:
            output.append({
                "name": h.get("name", ""),
                "starRating": h.get("starRating", ""),
                "lowestPrice": h.get("price", {}).get("lowestPrice", h.get("lowestPrice", "")),
                "address": h.get("address", ""),
                "amenities": h.get("hotelAmenities", [])[:5],
                "bookingUrl": h.get("bookingUrl", ""),
            })

        return json.dumps({
            "type": "国际酒店(RG)",
            "dive_site": site_name,
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
            "count": len(hotels),
            "hotels": output,
        }, ensure_ascii=False, indent=2)


# ============================================================
# 工具6: search_dive_transport 潜水交通搜索
# ============================================================
def search_dive_transport(origin="", destination="", date="", transport_type="", **kwargs):
    """搜索火车票+打车路线，覆盖国内潜水目的地交通"""
    if not origin or not destination:
        return json.dumps({"error": "请提供origin(出发地)和destination(目的地)"}, ensure_ascii=False)

    results = {}

    # 查找对应潜点
    site_name = None
    for name, info in DIVE_SITES.items():
        if destination in name or destination in info.get("location", ""):
            site_name = name
            break

    # 默认同时查火车和打车
    types = [transport_type] if transport_type else ["train", "taxi"]

    if "train" in types and date:
        # 飞猪火车票查询
        train_result = _call_fliggy("train", {
            "origin": origin,
            "destination": destination,
            "date": date,
        })
        if isinstance(train_result, dict) and "error" not in train_result:
            trains = train_result.get("data", train_result) if isinstance(train_result, dict) else train_result
            # 尝试提取列车列表
            train_list = []
            if isinstance(trains, dict):
                train_list = trains.get("trainList", trains.get("trains", trains.get("data", [])))
            if isinstance(train_list, list) and train_list:
                output = []
                for t in train_list[:6]:
                    output.append({
                        "trainNo": t.get("trainNo", t.get("train_no", "")),
                        "fromStation": t.get("fromStation", t.get("from_station", "")),
                        "toStation": t.get("toStation", t.get("to_station", "")),
                        "departTime": t.get("departTime", t.get("start_time", "")),
                        "arriveTime": t.get("arriveTime", t.get("arrive_time", "")),
                        "duration": t.get("duration", t.get("run_time", "")),
                        "prices": t.get("prices", t.get("price_list", "")),
                    })
                results["trains"] = output
            else:
                results["trains"] = "暂无火车票数据，可能无直达列车"
        else:
            results["trains"] = f"火车票查询失败: {train_result.get('error', '未知错误')}" if isinstance(train_result, dict) else "查询异常"

    if "taxi" in types:
        # 高德驾车路线规划
        route_result = _call_gaode("driving", {
            "origin": origin,
            "destination": destination,
        })
        if isinstance(route_result, dict) and route_result.get("status") == "1":
            paths = route_result.get("route", {}).get("paths", [])
            if paths:
                p = paths[0]
                dist = int(p.get("distance", 0))
                dur = int(p.get("duration", 0))
                results["driving"] = {
                    "distance": f"{dist/1000:.1f}km" if dist > 1000 else f"{dist}m",
                    "duration": f"{dur//3600}h{dur%3600//60}m" if dur >= 3600 else f"{dur//60}分钟",
                    "tolls": p.get("tolls", "未知"),
                }
        else:
            results["driving"] = "路线规划暂不可用"

    if site_name:
        results["dive_site"] = site_name
        # 附加潜点交通提示
        for name, info in DIVE_SITES.items():
            if name == site_name and "tips" in info:
                transport_tip = info.get("nearby_airport", "")
                if transport_tip:
                    results["airport_hint"] = f"最近机场：{transport_tip}"

    return json.dumps(results, ensure_ascii=False, indent=2)


# ============================================================
# 工具7: search_dive_food 潜水目的地美食搜索
# ============================================================
def search_dive_food(location="", cuisine="", radius=3000, limit=8, **kwargs):
    """搜索潜水目的地附近餐厅，基于高德POI"""
    if not location:
        return json.dumps({"error": "请提供location(地点/景点/潜店名)"}, ensure_ascii=False)

    # 1. 地理编码
    geo_result = _call_gaode("geocode", {"address": location})
    if not isinstance(geo_result, dict) or geo_result.get("status") != "1" or not geo_result.get("geocodes"):
        return json.dumps({"error": f"无法识别地点：{location}"}, ensure_ascii=False)

    geo = geo_result["geocodes"][0]
    loc = geo.get("location", "")
    if not loc:
        return json.dumps({"error": "地理编码失败"}, ensure_ascii=False)

    lng, lat = loc.split(",")
    city = geo.get("city", "")

    # 2. POI搜索餐厅
    FOOD_TYPE_CODES = "050000|050100|050200|050300|050400|050500|050600|050700|050800|050900"
    keywords = cuisine if cuisine else "餐厅 美食 海鲜"

    search_result = _call_gaode("poi_around", {
        "location": f"{lng},{lat}",
        "keywords": keywords,
        "types": FOOD_TYPE_CODES,
        "radius": radius,
        "offset": limit,
        "sortrule": "weight",
    })

    if not isinstance(search_result, dict) or search_result.get("status") != "1":
        return json.dumps({"error": "餐厅搜索失败，请稍后重试"}, ensure_ascii=False)

    pois = search_result.get("pois", [])
    if not pois:
        return json.dumps({
            "message": f"在{location}附近未找到餐厅",
            "suggestion": "尝试扩大搜索半径或换关键词",
        }, ensure_ascii=False)

    # 3. 格式化输出
    restaurants = []
    for poi in pois[:limit]:
        name = poi.get("name", "")
        addr = poi.get("address", "")
        distance = poi.get("distance", "")
        tel = poi.get("tel", "")
        biz_ext = poi.get("biz_ext", {})
        rating = biz_ext.get("rating", "") if isinstance(biz_ext, dict) else ""
        cost = biz_ext.get("cost", "") if isinstance(biz_ext, dict) else ""
        type_info = poi.get("type", "")
        type_label = type_info.split(";")[-1] if type_info else ""

        try:
            dist_int = int(distance)
            dist_fmt = f"{dist_int}m" if dist_int < 1000 else f"{dist_int/1000:.1f}km"
        except (ValueError, TypeError):
            dist_fmt = distance

        restaurants.append({
            "name": name,
            "type": type_label,
            "distance": dist_fmt,
            "rating": rating or "暂无评分",
            "avg_cost": cost or "暂无",
            "address": addr,
            "phone": tel.split(";")[0] if tel else "",
        })

    # 附加潜水目的地特色美食
    dive_food_tip = ""
    for name, info in DIVE_SITES.items():
        if location in name or location in info.get("location", ""):
            dive_food_tip = f"💡 {name}潜水后推荐：当地海鲜餐厅通常性价比最高，潜店附近问教练推荐最靠谱"
            break

    return json.dumps({
        "location": location,
        "city": city,
        "restaurants": restaurants,
        "total": len(restaurants),
        "dive_tip": dive_food_tip if dive_food_tip else "潜水后建议多喝水补充水分，避免立即大量饮酒",
    }, ensure_ascii=False, indent=2)


# ============================================================
# 工具注册表和主入口
# ============================================================
TOOLS = {
    "dive_site_search": dive_site_search,
    "dive_cert_guide": dive_cert_guide,
    "dive_safety_check": dive_safety_check,
    "search_dive_flights": search_dive_flights,
    "search_dive_hotels": search_dive_hotels,
    "search_dive_transport": search_dive_transport,
    "search_dive_food": search_dive_food,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python dive_travel.py <tool_name> [key=value ...]")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(f"未知工具: {tool_name}")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k] = v
    print(TOOLS[tool_name](**kwargs))

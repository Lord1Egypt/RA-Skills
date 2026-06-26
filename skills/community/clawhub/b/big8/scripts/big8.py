#!/usr/bin/env python3
"""
Big8 - AI 玄学助手
四合一：八字排盘 / 星座运势 / 每日占卦 / 老黄历

八字排盘 → lunar-python 算法计算
其他功能 → 辅助工具

用法：
  # 八字排盘
  python3 big8.py bazi "1996-03-20 14:00" [gender=1]
  
  # 星座计算
  python3 big8.py zodiac "1996-03-20"

  # 每日一卦
  python3 big8.py gua

  # 今日宜忌
  python3 big8.py huangli
"""

import sys
import json
import random
from datetime import date


# ─── 八字排盘 ───

def calc_bazi(birth_date_str: str, gender: int = 1) -> dict:
    """用 lunar-python 计算八字，gender: 1=男 0=女"""
    from lunar_python import Solar, EightChar

    # 解析日期时间
    parts = birth_date_str.replace("T", " ").split()
    date_part = parts[0]
    time_part = parts[1] if len(parts) > 1 else "12:00"

    y, m, d = map(int, date_part.split("-"))
    h, mi = map(int, time_part.split(":"))

    solar = Solar.fromYmdHms(y, m, d, h, mi, 0)
    lunar = solar.getLunar()
    ec = EightChar(lunar)

    # ── 四柱 ──
    bazi_list = lunar.getBaZi()  # ['丙子', '辛卯', '丙辰', '乙未']
    wuxing_list = lunar.getBaZiWuXing()  # ['火水', '金木', '火土', '木土']
    shishen_gan = lunar.getBaZiShiShenGan()  # ['比肩', '正财', '日主', '正印']
    shishen_zhi = lunar.getBaZiShiShenZhi()  # ['正官', '正印', '食神', '伤官']

    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    pillars = []
    for i in range(4):
        pillars.append({
            "name": pillar_names[i],
            "ganzhi": bazi_list[i] if i < len(bazi_list) else "",
            "wuxing": wuxing_list[i] if i < len(wuxing_list) else "",
            "shishen_gan": shishen_gan[i] if i < len(shishen_gan) else "",
            "shishen_zhi": shishen_zhi[i] if i < len(shishen_zhi) else "",
            "nayin": ec.getYearNaYin() if i == 0 else
                     ec.getMonthNaYin() if i == 1 else
                     ec.getDayNaYin() if i == 2 else
                     ec.getTimeNaYin(),
            "xun": ec.getYearXun() if i == 0 else
                   ec.getMonthXun() if i == 1 else
                   ec.getDayXun() if i == 2 else
                   ec.getTimeXun(),
            "xunkong": ec.getYearXunKong() if i == 0 else
                       ec.getMonthXunKong() if i == 1 else
                       ec.getDayXunKong() if i == 2 else
                       ec.getTimeXunKong(),
        })

    # ── 日主信息 ──
    day_master_gan = bazi_list[2][0] if len(bazi_list) > 2 and len(bazi_list[2]) > 0 else ""
    day_master_wuxing = wuxing_list[2] if len(wuxing_list) > 2 else ""

    # ── 胎元、命宫、身宫 ──
    taiyuan = ec.getTaiYuan() if hasattr(ec, 'getTaiYuan') else ""
    minggong = ec.getMingGong() if hasattr(ec, 'getMingGong') else ""
    shengong = ec.getShenGong() if hasattr(ec, 'getShenGong') else ""

    # ── 大运 ──
    yun = ec.getYun(gender)
    start_year = yun.getStartYear()
    is_forward = yun.isForward()

    da_yun_list = []
    for dy in yun.getDaYun():
        gz = dy.getGanZhi()
        if not gz:
            continue  # skip empty (first entry before luck period starts)
        da_yun_list.append({
            "ganzhi": gz,
            "start_year": dy.getStartYear(),
            "end_year": dy.getEndYear(),
            "start_age": dy.getStartAge(),
            "end_age": dy.getEndAge(),
        })

    # ── 当前流年 ──
    today = date.today()
    today_solar = Solar.fromYmd(today.year, today.month, today.day)
    today_lunar = today_solar.getLunar()
    current_year_ganzhi = today_lunar.getYearInGanZhiExact()
    current_year_shengxiao = today_lunar.getYearShengXiao()

    # ── 神煞 ──
    shensha = {
        "year_dishi": str(ec.getYearDiShi()) if hasattr(ec, 'getYearDiShi') else "",
        "month_dishi": str(ec.getMonthDiShi()) if hasattr(ec, 'getMonthDiShi') else "",
        "day_dishi": str(ec.getDayDiShi()) if hasattr(ec, 'getDayDiShi') else "",
        "time_dishi": str(ec.getTimeDiShi()) if hasattr(ec, 'getTimeDiShi') else "",
    }

    result = {
        "birthday": birth_date_str,
        "gender": "男" if gender == 1 else "女",
        "lunar_date": str(lunar),
        "zodiac_animal": lunar.getYearShengXiaoExact(),
        "bazi": " ".join(bazi_list),
        "pillars": pillars,
        "day_master": f"{day_master_gan}（{day_master_wuxing}）",
        "taiyuan": taiyuan,
        "minggong": minggong,
        "shengong": shengong,
        "yun_start_age": start_year,
        "yun_direction": "顺排" if is_forward else "逆排",
        "da_yun": da_yun_list,
        "current_year": current_year_ganzhi,
        "current_animal": current_year_shengxiao,
        "shensha": shensha,
    }

    return result


# ─── 星座 ───

def calc_zodiac(birth_date_str: str) -> dict:
    """根据出生日期计算星座"""
    parts = birth_date_str.split("-")
    if len(parts) < 3:
        return {"error": "日期格式错误，需 YYYY-MM-DD"}

    month, day = int(parts[1]), int(parts[2])

    signs = [
        ("摩羯座", 1, 1, 1, 19),
        ("水瓶座", 1, 20, 2, 18),
        ("双鱼座", 2, 19, 3, 20),
        ("白羊座", 3, 21, 4, 19),
        ("金牛座", 4, 20, 5, 20),
        ("双子座", 5, 21, 6, 21),
        ("巨蟹座", 6, 22, 7, 22),
        ("狮子座", 7, 23, 8, 22),
        ("处女座", 8, 23, 9, 22),
        ("天秤座", 9, 23, 10, 23),
        ("天蝎座", 10, 24, 11, 22),
        ("射手座", 11, 23, 12, 21),
        ("摩羯座", 12, 22, 12, 31),
    ]

    sun_sign = "未知"
    for name, sm, sd, em, ed in signs:
        birth = date(2000, month, day)
        start = date(2000, sm, sd)
        end = date(2000, em, ed)
        if sm > em:
            # 跨年处理（摩羯座）
            if birth >= start or birth <= end:
                sun_sign = name
                break
        elif start <= birth <= end:
            sun_sign = name
            break

    element_map = {
        "白羊座": "火", "狮子座": "火", "射手座": "火",
        "金牛座": "土", "处女座": "土", "摩羯座": "土",
        "双子座": "风", "天秤座": "风", "水瓶座": "风",
        "巨蟹座": "水", "天蝎座": "水", "双鱼座": "水",
    }

    return {
        "sun_sign": sun_sign,
        "element": element_map.get(sun_sign, ""),
        "birthday": birth_date_str,
    }


# ─── 每日一卦 ───

GUA_LIST = [
    ("乾为天", "䷀", "元亨利贞", "自强不息", "行"),
    ("坤为地", "䷁", "元亨利牝马之贞", "厚德载物", "藏"),
    ("水雷屯", "䷂", "刚柔始交而难生", "创始艰难", "慎"),
    ("山水蒙", "䷃", "匪我求童蒙", "启蒙教育", "学"),
    ("水天需", "䷄", "需于沙", "耐心等待", "等"),
    ("天水讼", "䷅", "终凶", "争执不利", "让"),
    ("地水师", "䷆", "丈人吉", "统率众人", "聚"),
    ("水地比", "䷇", "亲比", "团结合作", "亲"),
    ("风天小畜", "䷈", "密云不雨", "积蓄待发", "蓄"),
    ("天泽履", "䷉", "履虎尾", "谨慎行事", "履"),
    ("地天泰", "䷊", "小往大来", "吉祥亨通", "通"),
    ("天地否", "䷋", "大往小来", "闭塞不通", "守"),
    ("天火同人", "䷌", "同人于野", "团结合作", "同"),
    ("大有", "䷍", "元亨", "丰收富足", "丰"),
    ("地山谦", "䷎", "谦谦君子", "谦虚受益", "谦"),
    ("雷地豫", "䷏", "利建侯行师", "愉悦安乐", "乐"),
    ("泽雷随", "䷐", "元亨利贞", "随顺时势", "随"),
    ("山风蛊", "䷑", "干父之蛊", "整治弊病", "治"),
    ("地泽临", "䷒", "元亨利贞", "临近监督", "临"),
    ("风地观", "䷓", "观国之光", "观察审慎", "观"),
    ("火雷噬嗑", "䷔", "利用狱", "克服障碍", "克"),
    ("山火贲", "䷕", "贲亨", "装饰美化", "饰"),
    ("山地剥", "䷖", "不利有攸往", "剥落衰退", "退"),
    ("地雷复", "䷗", "七日来复", "复兴回归", "复"),
    ("天雷无妄", "䷘", "元亨利贞", "不妄为", "正"),
    ("山天大畜", "䷙", "利涉大川", "积蓄力量", "积"),
    ("山雷颐", "䷚", "自求口实", "修养养生", "养"),
    ("泽风大过", "䷛", "栋桡", "过犹不及", "中"),
    ("坎为水", "䷜", "习坎", "险中求进", "险"),
    ("离为火", "䷝", "利贞亨", "光明依附", "明"),
    ("泽山咸", "䷞", "亨利贞", "感应沟通", "感"),
    ("雷风恒", "䷟", "亨无咎", "持久恒心", "恒"),
    ("天山遁", "䷠", "遁亨", "退避隐让", "退"),
    ("雷天大壮", "䷡", "大壮利贞", "强盛壮大", "壮"),
    ("火地晋", "䷢", "康侯用锡马蕃庶", "晋升前进", "晋"),
    ("地火明夷", "䷣", "明夷于飞", "受伤隐忍", "忍"),
    ("风火家人", "䷤", "利女贞", "家庭和睦", "家"),
    ("火泽睽", "䷥", "小事吉", "乖离分歧", "分"),
    ("水山蹇", "䷦", "利西南", "艰难险阻", "难"),
    ("雷水解", "䷧", "利西南", "解除困难", "解"),
    ("山泽损", "䷨", "损上益下", "损减损失", "损"),
    ("风雷益", "䷩", "利有攸往", "增益好处", "益"),
    ("泽天夬", "䷪", "扬于王庭", "决断果敢", "决"),
    ("天风姤", "䷫", "女壮勿娶", "相遇遇合", "遇"),
    ("泽地萃", "䷬", "亨王假有庙", "聚集荟萃", "聚"),
    ("地风升", "䷭", "元亨", "上升发展", "升"),
    ("泽水困", "䷮", "亨贞大人吉", "困境困顿", "困"),
    ("水风井", "䷯", "改邑不改井", "守常不变", "守"),
    ("泽火革", "䷰", "已日乃孚", "变革改革", "变"),
    ("火风鼎", "䷱", "元吉亨", "鼎新革故", "鼎"),
    ("震为雷", "䷲", "亨", "震惊恐惧", "震"),
    ("艮为山", "䷳", "艮其背", "停止不动", "止"),
    ("风山渐", "䷴", "女归吉", "渐进发展", "渐"),
    ("雷泽归妹", "䷵", "征凶无攸利", "归依不當", "归"),
    ("雷火丰", "䷶", "亨王假之", "丰盛盛大", "盛"),
    ("火山旅", "䷷", "旅贞吉", "旅行寄居", "旅"),
    ("巽为风", "䷸", "小亨利有攸往", "顺从进入", "入"),
    ("兑为泽", "䷹", "亨", "喜悦快乐", "说"),
    ("风水涣", "䷺", "亨王假有庙", "涣散离散", "散"),
    ("水泽节", "䷻", "亨", "节制调节", "节"),
    ("风泽中孚", "䷼", "豚鱼吉", "诚信忠实", "诚"),
    ("雷山小过", "䷽", "亨", "小有过失", "过"),
    ("水火既济", "䷾", "初吉终乱", "成功完成", "成"),
    ("火水未济", "䷿", "亨", "未完成", "待"),
]

def random_gua() -> dict:
    """随机起一卦"""
    name, symbol, judgment, meaning, keyword = random.choice(GUA_LIST)
    return {
        "gua_name": name,
        "gua_symbol": symbol,
        "gua_judgment": judgment,
        "gua_meaning": meaning,
        "gua_keyword": keyword,
    }


# ─── 老黄历 ───

def calc_huangli() -> dict:
    """计算今日宜忌"""
    from lunar_python import Solar

    today = date.today()
    solar = Solar.fromYmd(today.year, today.month, today.day)
    lunar = solar.getLunar()

    result = {
        "date": str(solar),
        "lunar": str(lunar),
        "lunar_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
        "shengxiao": lunar.getYearShengXiao(),
        "ganzhi": f"{lunar.getYearInGanZhiExact()} {lunar.getMonthInGanZhiExact()} {lunar.getDayInGanZhiExact()}",
        "yi": lunar.getDayYi()[:8] if hasattr(lunar, 'getDayYi') else [],
        "ji": lunar.getDayJi()[:8] if hasattr(lunar, 'getDayJi') else [],
        "chong": f"冲{lunar.getDayChongShengXiao()}（{lunar.getDayChongGan()}）" if hasattr(lunar, 'getDayChongShengXiao') else "",
        "sha": f"煞{lunar.getDaySha()}",
        "shengxiao": lunar.getDayShengXiao() if hasattr(lunar, 'getDayShengXiao') else "",
        "full_info": lunar.toFullString() if hasattr(lunar, 'toFullString') else "",
    }

    return result


# ─── CLI ───

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "用法: big8.py <命令> [参数]",
            "commands": ["bazi", "zodiac", "gua", "huangli"]
        }, ensure_ascii=False))
        return

    cmd = sys.argv[1]

    if cmd == "bazi":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "请提供出生日期，如: big8.py bazi \"1996-03-20 14:00\""}, ensure_ascii=False))
            return
        gender = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        result = calc_bazi(sys.argv[2], gender=gender)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "zodiac":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "请提供出生日期，如: big8.py zodiac 1996-03-20"}, ensure_ascii=False))
            return
        result = calc_zodiac(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "gua":
        result = random_gua()
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "huangli":
        result = calc_huangli()
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(json.dumps({
            "error": f"未知命令: {cmd}",
            "commands": ["bazi", "zodiac", "gua", "huangli"]
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()

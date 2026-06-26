#!/usr/bin/env python3
"""
八字排盘工具 — 主入口
支持命令行排盘，输出文本或JSON格式
"""

import argparse
import json
import sys
import os
from datetime import datetime, timedelta, timezone

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.pillars import calculate_pillars
from lib.true_solar_time import correct_to_true_solar_time, get_correction_info
from lib.ten_gods import get_all_ten_gods, get_ten_god
from lib.five_elements import analyze_five_elements, judge_day_master_strength
from lib.major_luck import calculate_major_luck
from lib.relationships import analyze_relationships
from lib.hidden_stems import get_hidden_stems
from lib.cities import get_city_coords
from lib.constants import GAN_WUXING, GAN_YINYANG, TIAN_GAN, DI_ZHI

CST = timezone(timedelta(hours=8))


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="八字排盘工具")
    parser.add_argument("--date", required=True, help="出生日期 YYYY-MM-DD")
    parser.add_argument("--time", required=True, help="出生时间 HH:MM")
    parser.add_argument("--city", help="出生城市名（如：上海）")
    parser.add_argument("--lat", type=float, help="纬度")
    parser.add_argument("--lon", type=float, help="经度")
    parser.add_argument("--gender", required=True, choices=["male", "female"], help="性别")
    parser.add_argument("--format", dest="output_format", default="text", choices=["text", "json"], help="输出格式")
    parser.add_argument("--year", type=int, help="流年年份")
    parser.add_argument("--no-solar-correction", action="store_true", help="关闭真太阳时修正")
    return parser.parse_args()


def get_coordinates(args):
    """获取经纬度"""
    if args.lat is not None and args.lon is not None:
        return args.lat, args.lon
    if args.city:
        coords = get_city_coords(args.city)
        if coords:
            return coords
        print(f"错误：未找到城市 '{args.city}'，请使用 --lat --lon 指定经纬度", file=sys.stderr)
        sys.exit(1)
    print("错误：请指定 --city 或 --lat --lon", file=sys.stderr)
    sys.exit(1)


def calculate_liunian(year, day_stem):
    """计算流年信息"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    stem = TIAN_GAN[gan_idx]
    branch = DI_ZHI[zhi_idx]
    god = get_ten_god(day_stem, stem)
    return {
        "year": year,
        "stem": stem,
        "branch": branch,
        "ten_god": god,
        "hidden_stems": get_hidden_stems(branch),
    }


def format_text_output(result):
    """格式化为人类可读的文本输出"""
    inp = result["input"]
    p = result["pillars"]
    
    # 标题行
    gender_cn = "男" if inp["gender"] == "male" else "女"
    location = inp.get("city") or f"({inp.get('latitude', '?')}°N, {inp.get('longitude', '?')}°E)"
    lines = []
    lines.append(f"【命盘】{gender_cn} · {inp['date']} {inp['time']} {location}")
    
    if inp.get("solar_time_correction"):
        lines.append(f"（真太阳时：{inp.get('true_solar_time', '?')}）")
    lines.append("")
    
    # 四柱表格
    lines.append("     年柱    月柱    日柱    时柱")
    lines.append(f"天干   {p['year']['stem']}      {p['month']['stem']}      {p['day']['stem']}      {p['hour']['stem']}")
    lines.append(f"地支   {p['year']['branch']}      {p['month']['branch']}      {p['day']['branch']}      {p['hour']['branch']}")
    
    # 藏干行
    def _format_hidden(hs_list):
        return "".join(hs_list)
    
    hs_y = _format_hidden(p["year"]["hidden_stems"])
    hs_m = _format_hidden(p["month"]["hidden_stems"])
    hs_d = _format_hidden(p["day"]["hidden_stems"])
    hs_h = _format_hidden(p["hour"]["hidden_stems"])
    # 对齐：每列宽度6个中文字符
    lines.append(f"藏干  {hs_y:<6s} {hs_m:<6s} {hs_d:<6s} {hs_h:<6s}")
    
    # 十神行
    tg = result["ten_gods"]
    tg_y = tg.get("year_stem", {}).get("god", "")
    tg_m = tg.get("month_stem", {}).get("god", "")
    tg_h = tg.get("hour_stem", {}).get("god", "")
    lines.append(f"十神  {tg_y:<6s} {tg_m:<6s} {'（日主）':<6s} {tg_h:<6s}")
    lines.append("")
    
    # 日主信息
    dm = result["day_master"]
    polarity = "阳" if dm["polarity"] == "阳" else "阴"
    lines.append(f"日主：{dm['stem']}{dm['element']}（{polarity}） | {result['day_master_strength']}")
    lines.append("")
    
    # 五行分析
    fe = result["five_elements"]
    wx_parts = []
    for en, cn in [("wood", "木"), ("fire", "火"), ("earth", "土"), ("metal", "金"), ("water", "水")]:
        wx_parts.append(f"{cn}{fe[en]['percent']}")
    lines.append(f"五行：{'  '.join(wx_parts)}")
    
    # 刑冲合害
    if result["relationships"]:
        rel_parts = []
        for r in result["relationships"]:
            rel_parts.append(f"{'·'.join(r['positions'])} → {r['result']}")
        lines.append(f"关系：{'  |  '.join(rel_parts)}")
    lines.append("")
    
    # 大运
    ml = result["major_luck"]
    lines.append(f"大运（{ml['start_age']}岁起运，{ml['direction']}）：")
    luck_parts = []
    for period in ml["periods"]:
        luck_parts.append(f"{period['age']}  {period['stem']}{period['branch']}")
    # 每行3个
    for i in range(0, len(luck_parts), 3):
        lines.append("  " + "  |  ".join(luck_parts[i:i+3]))
    
    # 流年
    if "liunian" in result:
        ln = result["liunian"]
        lines.append("")
        lines.append(f"流年 {ln['year']}：{ln['stem']}{ln['branch']}（{ln['ten_god']}）")
    
    return "\n".join(lines)


def run(args):
    """主运行逻辑"""
    # 解析日期时间
    try:
        birth_date = datetime.strptime(args.date, "%Y-%m-%d")
        time_parts = args.time.split(":")
        hour, minute = int(time_parts[0]), int(time_parts[1])
    except ValueError as e:
        print(f"错误：日期/时间格式不正确 - {e}", file=sys.stderr)
        sys.exit(1)
    
    # 获取经纬度
    lat, lon = get_coordinates(args)
    
    # 构造北京时间 datetime
    birth_dt_cst = datetime(birth_date.year, birth_date.month, birth_date.day,
                            hour, minute, tzinfo=CST)
    
    # 真太阳时修正
    solar_correction = not args.no_solar_correction
    if solar_correction:
        true_dt = correct_to_true_solar_time(birth_dt_cst, lon)
        correction_info = get_correction_info(birth_dt_cst, lon)
    else:
        true_dt = birth_dt_cst
        correction_info = None
    
    # 计算四柱
    pillars = calculate_pillars(true_dt)
    
    # 日主信息
    day_stem = pillars["day"]["stem"]
    day_master = {
        "stem": day_stem,
        "element": GAN_WUXING[day_stem],
        "polarity": "阳" if GAN_YINYANG[day_stem] else "阴",
    }
    
    # 十神
    ten_gods = get_all_ten_gods(
        day_stem,
        pillars["year"]["stem"],
        pillars["month"]["stem"],
        pillars["hour"]["stem"],
    )
    
    # 五行分析
    five_elements = analyze_five_elements(pillars)
    
    # 日主强弱
    day_strength = judge_day_master_strength(day_stem, pillars["month"]["branch"], pillars)
    
    # 刑冲合害
    relationships = analyze_relationships(pillars)
    
    # 大运
    major_luck = calculate_major_luck(
        true_dt, args.gender,
        pillars["year"]["stem"],
        pillars["month"]["stem"],
        pillars["month"]["branch"],
        birth_date.year,
    )
    
    # 构造结果
    result = {
        "input": {
            "date": args.date,
            "time": args.time,
            "gender": args.gender,
            "solar_time_correction": solar_correction,
        },
        "pillars": pillars,
        "day_master": day_master,
        "ten_gods": ten_gods,
        "five_elements": five_elements,
        "day_master_strength": day_strength,
        "relationships": relationships,
        "major_luck": major_luck,
    }
    
    # 添加位置信息
    if args.city:
        result["input"]["city"] = args.city
    result["input"]["latitude"] = lat
    result["input"]["longitude"] = lon
    
    if solar_correction and correction_info:
        result["input"]["true_solar_time"] = correction_info["true_solar_time"]
    
    # 流年
    if args.year:
        result["liunian"] = calculate_liunian(args.year, day_stem)
    
    return result


def main():
    args = parse_args()
    result = run(args)
    
    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text_output(result))


if __name__ == "__main__":
    main()

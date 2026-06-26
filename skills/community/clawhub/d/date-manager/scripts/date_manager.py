#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全能日期管家 - 日期管理脚本
"""

import os
import sys
import json
import uuid
import argparse
import calendar
from datetime import datetime, date, timedelta
from pathlib import Path

# ========== 编码处理 ==========
if sys.platform == 'win32':
    # Windows 控制台编码处理
    try:
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

# 设置输出编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
if sys.stderr.encoding != 'utf-8':
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

import subprocess

# ========== 配置 ==========
# 处理 PyInstaller 打包后路径
if getattr(sys, 'frozen', False):
    # 打包后的可执行文件
    APP_DIR = Path(sys._MEIPASS)
    # 数据文件优先使用外部的（在 exe 同目录下的 data 文件夹）
    EXTERNAL_DATA = Path(sys.executable).parent / "data" / "dates.json"
    if EXTERNAL_DATA.exists():
        DATA_FILE = EXTERNAL_DATA
    else:
        DATA_FILE = APP_DIR / "data" / "dates.json"
else:
    # 开发环境
    SCRIPT_DIR = Path(__file__).parent.parent
    DATA_FILE = SCRIPT_DIR / "data" / "dates.json"

DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

# 类型映射
TYPE_MAP = {
    "生日": "birthday",
    "纪念日": "anniversary",
    "祭日": "memorial",
    "祭祖": "ancestor",
    "birthday": "birthday",
    "anniversary": "anniversary",
    "memorial": "memorial",
    "ancestor": "ancestor",
}

DISPLAY_TYPE = {
    "birthday": "生日",
    "anniversary": "纪念日",
    "memorial": "祭日",
    "ancestor": "祭祖",
}

# 婚龄名称
ANNIVERSARY_NAMES = {
    1: "纸婚", 2: "布婚", 3: "皮婚", 5: "木婚",
    10: "锡婚", 15: "水晶婚", 20: "瓷婚", 25: "银婚",
    30: "珍珠婚", 40: "红宝石婚", 50: "金婚", 60: "钻石婚",
}

# 节气数据（使用 chinese-calendar 库计算）
def get_solar_terms_for_year(year):
    """获取指定年份的所有节气"""
    try:
        import chinese_calendar
        from datetime import date
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        terms = chinese_calendar.get_solar_terms(start, end)
        return {term_name: term_date for term_date, term_name in terms}
    except ImportError:
        # 备用数据（简化版，允许1-2天误差）
        return get_fallback_solar_terms(year)

def get_solar_term_date(year, term_name):
    """获取指定年份指定节气的日期"""
    terms = get_solar_terms_for_year(year)
    if term_name in terms:
        return terms[term_name]
    # 检查下一年
    terms_next = get_solar_terms_for_year(year + 1)
    if term_name in terms_next:
        return terms_next[term_name]
    return None

def get_fallback_solar_terms(year):
    """备用节气数据（简化版）"""
    BASE_YEAR = 2026
    BASE_TERMS = {
        "小寒": "01-05", "大寒": "01-20", "立春": "02-03", "雨水": "02-18",
        "惊蛰": "03-05", "春分": "03-20", "清明": "04-04", "谷雨": "04-20",
        "立夏": "05-05", "小满": "05-21", "芒种": "06-05", "夏至": "06-21",
        "小暑": "07-07", "大暑": "07-22", "立秋": "08-07", "处暑": "08-23",
        "白露": "09-07", "秋分": "09-23", "寒露": "10-08", "霜降": "10-23",
        "立冬": "11-07", "小雪": "11-22", "大雪": "12-07", "冬至": "12-21"
    }
    from datetime import date
    result = {}
    for name, md in BASE_TERMS.items():
        m, d = map(int, md.split('-'))
        result[name] = date(year, m, d)
    return result

# 节气信息（拼音和描述）
SOLAR_TERMS_INFO = [
    {"name": "小寒", "pinyin": "xiaohan", "desc": "开始进入一年中最寒冷的日子"},
    {"name": "大寒", "pinyin": "dahan", "desc": "一年中最冷的时节"},
    {"name": "立春", "pinyin": "lichun", "desc": "春季的开始"},
    {"name": "雨水", "pinyin": "yushui", "desc": "降雨开始，雨量渐增"},
    {"name": "惊蛰", "pinyin": "jingzhe", "desc": "春雷始鸣，惊醒蛰虫"},
    {"name": "春分", "pinyin": "chunfen", "desc": "昼夜等长，春季过半"},
    {"name": "清明", "pinyin": "qingming", "desc": "天清气明，万物洁齐"},
    {"name": "谷雨", "pinyin": "guyu", "desc": "雨生百谷，播种时节"},
    {"name": "立夏", "pinyin": "lixia", "desc": "夏季的开始"},
    {"name": "小满", "pinyin": "xiaoman", "desc": "小麦籽粒开始饱满"},
    {"name": "芒种", "pinyin": "mangzhong", "desc": "有芒作物成熟，抢收抢种"},
    {"name": "夏至", "pinyin": "xiazhi", "desc": "白昼最长，夏季过半"},
    {"name": "小暑", "pinyin": "xiaoshu", "desc": "暑气渐盛"},
    {"name": "大暑", "pinyin": "dashu", "desc": "一年中最热的时节"},
    {"name": "立秋", "pinyin": "liuqiu", "desc": "秋季的开始"},
    {"name": "处暑", "pinyin": "chushu", "desc": "暑气消退"},
    {"name": "白露", "pinyin": "bailu", "desc": "露凝而白，早晚温差大"},
    {"name": "秋分", "pinyin": "qiufen", "desc": "昼夜等长，秋季过半"},
    {"name": "寒露", "pinyin": "hanlu", "desc": "露气寒冷，秋季渐深"},
    {"name": "霜降", "pinyin": "shuangjiang", "desc": "天气渐冷，开始降霜"},
    {"name": "立冬", "pinyin": "lidong", "desc": "冬季的开始"},
    {"name": "小雪", "pinyin": "xiaoxue", "desc": "开始降雪，但雪量不大"},
    {"name": "大雪", "pinyin": "daxue", "desc": "雪量增大"},
    {"name": "冬至", "pinyin": "dongzhi", "desc": "白昼最短，冬季过半"}
]

# 节气名称映射
SOLAR_TERMS = {t["name"]: i for i, t in enumerate(SOLAR_TERMS_INFO)}

# ========== 工具函数 ==========

def get_current_date():
    """获取当前日期"""
    return date.today()


def parse_date(date_str):
    """解析公历日期"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None


def parse_lunar(lunar_str):
    """解析农历日期，格式: 月-日"""
    try:
        parts = lunar_str.replace(" ", "").split("-")
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    except:
        pass
    return None, None


def lunar_to_solar(year, lunar_month, lunar_day):
    """农历转公历"""
    try:
        from zhdate import ZhDate
        # 尝试在当年和下一年找到合适的日期
        for y in [year, year + 1, year - 1]:
            try:
                # ZhDate(year, month, day) 直接表示农历日期
                zhdate_obj = ZhDate(y, lunar_month, lunar_day)
                solar_date = zhdate_obj.to_datetime().date()
                # 验证转换后的年份是否合理（允许跨年）
                if abs(solar_date.year - y) <= 1:
                    return solar_date
            except Exception:
                continue
    except ImportError:
        pass
    return None


def solar_to_lunar(year, month, day):
    """公历转农历（如果可用）"""
    try:
        from zhdate import ZhDate
        solar_date = date(year, month, day)
        zhdate_obj = ZhDate.from_datetime(solar_date)
        return f"农历{zhdate_obj.chinese_month}{zhdate_obj.chinese_day}"
    except ImportError:
        return None
    except Exception:
        return None


def calculate_age(birth_date, target_date=None):
    """计算年龄"""
    if target_date is None:
        target_date = get_current_date()
    age = target_date.year - birth_date.year
    if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def calculate_countdown(target_date, current_date=None):
    """计算倒计时"""
    if current_date is None:
        current_date = get_current_date()
    delta = (target_date - current_date).days
    if delta < 0:
        return f"已过{-delta}天", delta
    elif delta == 0:
        return "今天!", 0
    else:
        return f"还有{delta}天", delta


def calculate_anniversary_years(target_date, current_date=None):
    """计算周年"""
    if current_date is None:
        current_date = get_current_date()
    years = current_date.year - target_date.year
    if (current_date.month, current_date.day) < (target_date.month, target_date.day):
        years -= 1
    return years


def get_anniversary_name(years):
    """获取婚龄名称"""
    for y in sorted(ANNIVERSARY_NAMES.keys(), reverse=True):
        if years >= y:
            return ANNIVERSARY_NAMES[y]
    return None


def get_this_year_date(original_date, target_year=None):
    """获取指定年份的同日期，如果已过则返回下一年"""
    if target_year is None:
        target_year = get_current_date().year
    this_year_date = original_date.replace(year=target_year)
    if this_year_date < get_current_date():
        this_year_date = this_year_date.replace(year=target_year + 1)
    return this_year_date


def format_display(item, target_date=None, current_date=None):
    """生成标准显示格式"""
    if current_date is None:
        current_date = get_current_date()
    if target_date is None:
        target_date = get_this_year_date(parse_date(item.get("date"))) if item.get("date") else None
    
    item_type = item.get("type", "")
    item_name = item.get("name", "")
    relation = item.get("relation", "")
    # 关系已经标识了人物身份，直接用关系显示
    display_name = relation if relation else item_name
    
    if item_type == "birthday" and target_date:
        age = calculate_age(parse_date(item.get("date")), target_date)
        countdown, days = calculate_countdown(target_date, current_date)
        return f"{target_date.strftime('%m月%d日')} | {display_name}{age}岁 | {countdown}"
    
    elif item_type == "anniversary" and target_date:
        # 获取原始日期
        original_date = parse_date(item.get("date")) or parse_date(item.get("original_solar_date"))
        years = calculate_anniversary_years(original_date, current_date) if original_date else 0
        ann_name = get_anniversary_name(years)
        countdown, days = calculate_countdown(target_date, current_date)
        if ann_name:
            return f"{target_date.strftime('%m月%d日')} | {display_name} | {countdown} | 💍{ann_name}"
        return f"{target_date.strftime('%m月%d日')} | {display_name} | {countdown}"
    
    elif item_type == "memorial":
        original_date = parse_date(item.get("date"))
        years = calculate_anniversary_years(original_date, current_date) if original_date else 0
        return f"🌸 {item_name}\n第{years}周年 ({target_date.strftime('%Y-%m-%d')})\n建议：点一支蜡烛，给家人打个电话"
    
    elif item_type == "ancestor":
        countdown, days = calculate_countdown(target_date, current_date)
        return f"🏮 {item_name}\n{countdown}\n准备清单：香烛、纸钱、鲜花、供品"
    
    return f"{target_date.strftime('%m月%d日')} | {display_name}"


# ========== 数据操作 ==========

def load_data():
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0", "updated_at": "", "items": []}


def save_data(data):
    """保存数据"""
    data["updated_at"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_id():
    """生成简短ID"""
    return str(uuid.uuid4())[:8]


def find_item_by_id(data, item_id):
    """根据ID查找记录"""
    for i, item in enumerate(data.get("items", [])):
        if item["id"] == item_id:
            return i, item
    return None, None


# ========== 命令实现 ==========

def cmd_add(args):
    """添加记录"""
    # 校验名称不能为空
    if not args.name or not args.name.strip():
        return {"status": "error", "msg": "名称不能为空"}
    
    # 校验 remind_days 范围
    if args.remind is not None and (args.remind < 1 or args.remind > 30):
        return {"status": "error", "msg": "提醒天数需在 1-30 之间"}
    
    data = load_data()
    item_id = generate_id()
    
    # 解析日期
    item_date = None
    date_type = "solar"
    lunar_month = None
    lunar_day = None
    lunar_display = None  # 农历显示文本
    original_solar_date = None  # 原始公历日期（从农历推算）
    
    if args.lunar:
        date_type = "lunar"
        lunar_month, lunar_day = parse_lunar(args.lunar)
        if lunar_month is None:
            return {"status": "error", "msg": "农历格式错误，应为 月-日，如 8-10"}
        
        # 计算原始公历日期
        # 策略：从今年往前找最近的已过日期，那就是"今年"的纪念日/生日
        # 对于结婚纪念日，我们需要更早的年份
        # 检查是否传入了年份参数
        original_year = getattr(args, 'year', None)
        
        if original_year:
            # 用户指定了年份
            try:
                from zhdate import ZhDate
                zh = ZhDate(original_year, lunar_month, lunar_day)
                original_solar_date = zh.to_datetime().date()
            except:
                original_solar_date = None
        else:
            # 自动计算：从今年往前找最近的已过日期
            current_year = get_current_date().year
            from zhdate import ZhDate
            for y in range(current_year, current_year - 51, -1):
                try:
                    zh = ZhDate(y, lunar_month, lunar_day)
                    solar = zh.to_datetime().date()
                    # 如果这个日期已过（<今天），记录下来
                    if solar < get_current_date():
                        original_solar_date = solar
                        break
                except:
                    continue
        
        # 农历转公历（用于显示今年日期）
        solar_date = lunar_to_solar(get_current_date().year, lunar_month, lunar_day)
        if solar_date:
            lunar_display = f"农历{lunar_month}月{lunar_day}日"
    elif args.date:
        # 验证日期格式
        parsed_date = parse_date(args.date)
        if parsed_date is None:
            return {"status": "error", "msg": f"日期格式错误，应为 YYYY-MM-DD，如 1990-05-15"}
        item_date = args.date
        # 公历转农历（自动计算）
        try:
            from zhdate import ZhDate
            z = ZhDate.from_datetime(datetime.combine(parsed_date, datetime.min.time()))
            lunar_month = z.lunar_month
            lunar_day = z.lunar_day
            # 从 chinese() 中提取农历日期和生肖，如：二零零八年四月初三 丙申年 (猴年)
            chinese_str = z.chinese()
            # 提取生肖（括号中的内容）
            import re
            zodiac_match = re.search(r'\((\S+)\)', chinese_str)
            zodiac = zodiac_match.group(1) if zodiac_match else ''
            lunar_display = f"农历{z.lunar_year}年{z.lunar_month}月{z.lunar_day}日 ({zodiac})"
            date_type = "solar+lunar"
        except ImportError:
            lunar_display = "（未安装zhdate库，无法显示农历）"
        except Exception as e:
            lunar_display = None
    else:
        return {"status": "error", "msg": "请提供日期 --date 或 --lunar"}
    
    # 构建记录
    item = {
        "id": item_id,
        "type": TYPE_MAP.get(args.type, "birthday"),
        "name": args.name,
        "date": item_date,
        "date_type": date_type,
        "lunar_month": lunar_month,
        "lunar_day": lunar_day,
        "original_solar_date": original_solar_date.strftime("%Y-%m-%d") if original_solar_date else None,
        "remind_days": args.remind or 7,
        "relation": args.relation or "",
        "notes": args.notes or "",
        "created_at": datetime.now().isoformat(),
    }
    
    data["items"].append(item)
    save_data(data)
    
    # 生成提示信息
    current_date = get_current_date()
    result = {
        "status": "success",
        "id": item_id,
        "name": args.name,
        "type": DISPLAY_TYPE.get(item["type"], item["type"]),
        "date": item_date or f"农历{lunar_month}月{lunar_day}日",
        "lunar": lunar_display,
        "remind_days": item["remind_days"],
        "relation": item["relation"],
    }
    
    # 根据类型计算额外信息
    if item["type"] == "birthday" and item_date:
        birth_date = parse_date(item_date)
        if birth_date:
            this_year_birthday = get_this_year_date(birth_date)
            age = calculate_age(birth_date, this_year_birthday)
            countdown, _ = calculate_countdown(this_year_birthday, current_date)
            result["this_year"] = this_year_birthday.strftime("%Y-%m-%d")
            result["age"] = age
            result["countdown"] = countdown
            relation = item["relation"] or ""
            # 关系已经标识了人物身份，直接用关系显示
            display_name = relation if relation else item['name']
            result["display"] = f"{this_year_birthday.strftime('%m月%d日')} | {display_name}{age}岁 | {countdown}"
    
    elif item["type"] == "anniversary" and item_date:
        ann_date = parse_date(item_date)
        if ann_date:
            years = calculate_anniversary_years(ann_date, current_date)
            ann_name = get_anniversary_name(years)
            next_anniversary = get_this_year_date(ann_date)
            countdown, days = calculate_countdown(next_anniversary, current_date)
            result["years"] = years
            result["next_date"] = next_anniversary.strftime("%Y-%m-%d")
            result["countdown"] = countdown
            if years >= 1 and ann_name:
                result["anniversary_name"] = f"💍 {ann_name}"
                result["display"] = f"距离{years+1}周年还有{days}天 | {ann_name}"
            elif years >= 1:
                result["display"] = f"距离{years+1}周年还有{days}天"
    
    elif item["type"] == "memorial" and item_date:
        mem_date = parse_date(item_date)
        if mem_date:
            years = calculate_anniversary_years(mem_date, current_date)
            result["years"] = years
            result["display"] = f"🌸 {args.name}\n第{years}周年 ({mem_date.strftime('%Y-%m-%d')})\n建议：点一支蜡烛，给家人打个电话"
    
    elif item["type"] == "ancestor" and item_date:
        anc_date = parse_date(item_date)
        if anc_date:
            this_year_date = get_this_year_date(anc_date)
            countdown, days = calculate_countdown(this_year_date, current_date)
            result["countdown"] = countdown
            result["display"] = f"🏮 {args.name}\n{countdown}\n准备清单：香烛、纸钱、鲜花、供品"
    
    return result


def cmd_list(args):
    """查询列表"""
    data = load_data()
    items = data.get("items", [])
    
    # 过滤
    if args.type:
        type_key = TYPE_MAP.get(args.type)
        if type_key:
            items = [i for i in items if i.get("type") == type_key]
    
    # 排序（按类型、名称）
    items.sort(key=lambda x: (x.get("type", ""), x.get("name", "")))
    
    result = []
    for item in items:
        result.append({
            "id": item["id"],
            "name": item["name"],
            "type": DISPLAY_TYPE.get(item.get("type", ""), item.get("type", "")),
            "date": item.get("date") or (f"农历{item.get('lunar_month')}月{item.get('lunar_day')}日" if item.get("lunar_month") else ""),
            "relation": item.get("relation", ""),
            "remind_days": item.get("remind_days", 7),
        })
    
    return {"status": "success", "count": len(result), "items": result}


def cmd_today(args):
    """今日/近期查询"""
    data = load_data()
    current_date = get_current_date()
    days = args.days if hasattr(args, 'days') and args.days else 7
    
    today_items = []
    upcoming_items = []
    this_month_count = 0
    
    for item in data.get("items", []):
        item_type = item.get("type", "")
        
        # 计算公历倒计时
        solar_countdown = None
        solar_this_year = None
        if item.get("date"):
            solar_target = parse_date(item.get("date"))
            if solar_target:
                solar_this_year = get_this_year_date(solar_target)
                solar_countdown, _ = calculate_countdown(solar_this_year, current_date)
        
        # 计算农历倒计时
        lunar_countdown = None
        lunar_this_year = None
        if item.get("lunar_month") and item.get("lunar_day"):
            lunar_target = lunar_to_solar(current_date.year, item["lunar_month"], item["lunar_day"])
            if not lunar_target or lunar_target < current_date:
                lunar_target = lunar_to_solar(current_date.year + 1, item["lunar_month"], item["lunar_day"])
            if lunar_target:
                lunar_this_year = lunar_target
                lunar_countdown, _ = calculate_countdown(lunar_target, current_date)
        
        # 确定使用哪个日期作为主要显示
        if solar_this_year:
            target_date = solar_this_year
        elif lunar_this_year:
            target_date = lunar_this_year
        else:
            continue
        
        days_diff = (target_date - current_date).days
        
        # 统计本月
        if target_date.year == current_date.year and target_date.month == current_date.month:
            this_month_count += 1
        
        countdown_str, _ = calculate_countdown(target_date, current_date)
        
        # 构建显示信息
        item_info = {
            "id": item["id"],
            "name": item["name"],
            "type": DISPLAY_TYPE.get(item_type, item_type),
            "relation": item.get("relation", ""),
        }
        
        # 生日类型单独显示公历和农历
        if item_type == "birthday" and (solar_countdown or lunar_countdown):
            # 公历信息
            if solar_this_year:
                item_info["solar_date"] = solar_this_year.strftime("%m月%d日")
                item_info["solar_countdown"] = solar_countdown
                item_info["solar_days"] = (solar_this_year - current_date).days
            # 农历信息
            if lunar_this_year:
                item_info["lunar_date"] = f"{item.get('lunar_month')}月{item.get('lunar_day')}日"
                item_info["lunar_solar_date"] = lunar_this_year.strftime("%m月%d日")
                item_info["lunar_countdown"] = lunar_countdown
                item_info["lunar_days"] = (lunar_this_year - current_date).days
            
            # 生成综合显示
            display_parts = []
            if solar_countdown and solar_this_year:
                if item.get("relation"):
                    display_parts.append(f"公历{solar_this_year.strftime('%m月%d日')} {item['relation']} {solar_countdown}")
                else:
                    display_parts.append(f"公历{solar_this_year.strftime('%m月%d日')} {solar_countdown}")
            if lunar_countdown and lunar_this_year:
                display_parts.append(f"农历{item.get('lunar_month')}月{item.get('lunar_day')}日 {lunar_countdown}")
            item_info["display"] = " | ".join(display_parts)
            item_info["days"] = min(
                item_info.get("solar_days", 9999),
                item_info.get("lunar_days", 9999)
            )
        else:
            # 非生日类型
            if solar_this_year:
                item_info["date"] = solar_this_year.strftime("%m月%d日")
            elif lunar_this_year:
                item_info["date"] = f"{item.get('lunar_month')}月{item.get('lunar_day')}日"
            item_info["countdown"] = countdown_str
            item_info["days"] = days_diff
            item_info["display"] = format_display(item, target_date, current_date)
        
        if days_diff == 0:
            today_items.append(item_info)
        elif 0 < days_diff <= days:
            upcoming_items.append(item_info)
    
    # 按天数排序
    today_items.sort(key=lambda x: x["days"])
    upcoming_items.sort(key=lambda x: x["days"])
    
    # 分类统计
    type_count = {}
    for item in data.get("items", []):
        t = DISPLAY_TYPE.get(item.get("type", ""), item.get("type", ""))
        type_count[t] = type_count.get(t, 0) + 1
    
    return {
        "status": "success",
        "today": current_date.strftime("%m月%d日"),
        "today_items": today_items,
        "upcoming_items": upcoming_items,
        "this_month_count": this_month_count,
        "type_count": type_count,
    }


def cmd_search(args):
    """搜索"""
    data = load_data()
    keyword = args.keyword.lower()
    
    results = []
    for item in data.get("items", []):
        if (keyword in item.get("name", "").lower() or 
            keyword in item.get("relation", "").lower() or 
            keyword in item.get("notes", "").lower()):
            results.append({
                "id": item["id"],
                "name": item["name"],
                "type": DISPLAY_TYPE.get(item.get("type", ""), item.get("type", "")),
                "date": item.get("date") or (f"农历{item.get('lunar_month')}月{item.get('lunar_day')}日" if item.get("lunar_month") else ""),
                "relation": item.get("relation", ""),
            })
    
    return {"status": "success", "keyword": args.keyword, "count": len(results), "results": results}


def cmd_update(args):
    """更新记录"""
    data = load_data()
    idx, item = find_item_by_id(data, args.id)
    
    if item is None:
        return {"status": "error", "msg": "记录不存在"}
    
    if args.date:
        item["date"] = args.date
        item["date_type"] = "solar"
    if args.remind:
        item["remind_days"] = args.remind
    if args.notes is not None:
        item["notes"] = args.notes
    if args.relation is not None:
        item["relation"] = args.relation
    
    save_data(data)
    return {"status": "success", "id": args.id, "msg": "更新成功"}


def cmd_delete(args):
    """删除记录"""
    data = load_data()
    idx, item = find_item_by_id(data, args.id)
    
    if item is None:
        return {"status": "error", "msg": "记录不存在"}
    
    deleted = data["items"].pop(idx)
    save_data(data)
    return {"status": "success", "id": args.id, "name": deleted.get("name")}


def cmd_get(args):
    """获取详情"""
    data = load_data()
    idx, item = find_item_by_id(data, args.id)
    
    if item is None:
        return {"status": "error", "msg": "记录不存在"}
    
    current_date = get_current_date()
    item_type = item.get("type", "")
    
    result = {
        "status": "success",
        "item": {
            "id": item["id"],
            "name": item["name"],
            "type": DISPLAY_TYPE.get(item_type, item_type),
            "date": item.get("date") or (f"农历{item.get('lunar_month')}月{item.get('lunar_day')}日" if item.get("lunar_month") else ""),
            "date_type": item.get("date_type", "solar"),
            "remind_days": item.get("remind_days", 7),
            "relation": item.get("relation", ""),
            "notes": item.get("notes", ""),
            "created_at": item.get("created_at", ""),
        }
    }
    
    # 计算今年的日期和倒计时
    target_date = None
    if item.get("date"):
        target_date = get_this_year_date(parse_date(item.get("date")))
    elif item.get("lunar_month") and item.get("lunar_day"):
        target_date = lunar_to_solar(current_date.year, item["lunar_month"], item["lunar_day"])
    
    if target_date:
        countdown, _ = calculate_countdown(target_date, current_date)
        result["item"]["this_year_date"] = target_date.strftime("%Y-%m-%d")
        result["item"]["countdown"] = countdown
        result["item"]["display"] = format_display(item, target_date, current_date)
        
        # 计算年龄/周年
        if item_type == "birthday" and item.get("date"):
            age = calculate_age(parse_date(item.get("date")), target_date)
            result["item"]["age"] = age
        elif item_type == "anniversary":
            original = parse_date(item.get("date")) or parse_date(item.get("original_solar_date"))
            if original:
                years = calculate_anniversary_years(original, current_date)
                result["item"]["years"] = years
                ann_name = get_anniversary_name(years)
                if ann_name:
                    result["item"]["anniversary_name"] = ann_name
    
    return result


def cmd_convert(args):
    """公历农历互转"""
    try:
        from zhdate import ZhDate
    except ImportError:
        return {"status": "error", "msg": "未安装 zhdate 库，无法进行农历转换。请运行: pip install zhdate"}
    
    try:
        if args.solar:
            # 公历转农历
            parsed_date = parse_date(args.solar)
            if parsed_date is None:
                return {"status": "error", "msg": f"日期格式错误，应为 YYYY-MM-DD，如 1990-05-15"}
            
            z = ZhDate.from_datetime(datetime.combine(parsed_date, datetime.min.time()))
            chinese = z.chinese()
            
            return {
                "status": "success",
                "type": "solar_to_lunar",
                "input": {
                    "solar": args.solar,
                },
                "output": {
                    "lunar": chinese,
                    "lunar_year": z.lunar_year,
                    "lunar_month": z.lunar_month,
                    "lunar_day": z.lunar_day,
                    "zodiac": chinese.split()[1] if len(chinese.split()) > 1 else "",
                }
            }
        
        elif args.lunar:
            # 农历转公历
            lunar_month, lunar_day = parse_lunar(args.lunar)
            if lunar_month is None:
                return {"status": "error", "msg": f"农历格式错误，应为 月-日，如 8-15"}
            
            year = args.year or get_current_date().year
            z = ZhDate(year, lunar_month, lunar_day)
            solar = z.to_datetime()
            
            return {
                "status": "success",
                "type": "lunar_to_solar",
                "input": {
                    "lunar": f"农历{year}年{lunar_month}月{lunar_day}日",
                },
                "output": {
                    "solar": solar.strftime("%Y-%m-%d"),
                    "weekday": solar.strftime("%A"),
                }
            }
        else:
            return {"status": "error", "msg": "请提供 --solar 或 --lunar 参数"}
    except Exception as e:
        return {"status": "error", "msg": f"转换失败: {str(e)}"}


def cmd_calc(args):
    """日期计算"""
    try:
        from zhdate import ZhDate
        has_zhdate = True
    except ImportError:
        has_zhdate = False
    
    current_date = get_current_date()
    result = {
        "status": "success",
        "today": current_date.strftime("%Y-%m-%d"),
        "weekday": current_date.strftime("%A"),
        "results": []
    }
    
    if has_zhdate:
        z = ZhDate.from_datetime(datetime.combine(current_date, datetime.min.time()))
        result["lunar"] = z.chinese()
    
    # 计算指定日期
    if args.date:
        target = parse_date(args.date)
        if target:
            diff = (target - current_date).days
            countdown, _ = calculate_countdown(target, current_date)
            item = {
                "date": target.strftime("%Y-%m-%d"),
                "weekday": target.strftime("%A"),
                "days_diff": diff,
                "countdown": countdown
            }
            if has_zhdate and args.lunar:
                z = ZhDate.from_datetime(datetime.combine(target, datetime.min.time()))
                item["lunar"] = z.chinese()
            result["results"].append(item)
    
    # 计算下周一
    if args.next_monday:
        days_ahead = 7 - current_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_monday = current_date + timedelta(days=days_ahead)
        item = {
            "type": "下周一",
            "date": next_monday.strftime("%Y-%m-%d"),
            "weekday": next_monday.strftime("%A"),
            "days_diff": days_ahead,
            "countdown": f"还有{days_ahead}天"
        }
        if has_zhdate:
            z = ZhDate.from_datetime(datetime.combine(next_monday, datetime.min.time()))
            item["lunar"] = z.chinese()
        result["results"].append(item)
    
    # 计算本周/下周
    if args.week:
        week_map = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                   "friday": 4, "saturday": 5, "sunday": 6}
        if args.week.lower() in week_map:
            target_weekday = week_map[args.week.lower()]
            days_ahead = target_weekday - current_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            target = current_date + timedelta(days=days_ahead)
            item = {
                "type": f"本周{args.week.capitalize()}",
                "date": target.strftime("%Y-%m-%d"),
                "weekday": target.strftime("%A"),
                "days_diff": days_ahead,
                "countdown": f"还有{days_ahead}天"
            }
            if has_zhdate:
                z = ZhDate.from_datetime(datetime.combine(target, datetime.min.time()))
                item["lunar"] = z.chinese()
            result["results"].append(item)
    
    # 计算天数差
    if args.days:
        future = current_date + timedelta(days=args.days)
        item = {
            "type": f"{args.days}天后",
            "date": future.strftime("%Y-%m-%d"),
            "weekday": future.strftime("%A"),
            "days_diff": args.days
        }
        if has_zhdate:
            z = ZhDate.from_datetime(datetime.combine(future, datetime.min.time()))
            item["lunar"] = z.chinese()
        result["results"].append(item)
    
    # 计算月末
    if args.month_end:
        year = args.month_end_year or current_date.year
        month = args.month_end_month or current_date.month
        last_day = calendar.monthrange(year, month)[1]
        target = date(year, month, last_day)
        diff = (target - current_date).days
        item = {
            "type": f"{year}年{month}月末",
            "date": target.strftime("%Y-%m-%d"),
            "weekday": target.strftime("%A"),
            "days_diff": diff,
            "countdown": f"还有{diff}天" if diff >= 0 else f"已过{-diff}天"
        }
        if has_zhdate:
            z = ZhDate.from_datetime(datetime.combine(target, datetime.min.time()))
            item["lunar"] = z.chinese()
        result["results"].append(item)
    
    # 计算月初
    if args.month_start:
        year = args.month_start_year or current_date.year
        month = args.month_start_month or current_date.month
        target = date(year, month, 1)
        diff = (target - current_date).days
        item = {
            "type": f"{year}年{month}月初",
            "date": target.strftime("%Y-%m-%d"),
            "weekday": target.strftime("%A"),
            "days_diff": diff,
            "countdown": f"还有{diff}天" if diff >= 0 else f"已过{-diff}天"
        }
        if has_zhdate:
            z = ZhDate.from_datetime(datetime.combine(target, datetime.min.time()))
            item["lunar"] = z.chinese()
        result["results"].append(item)
    
    return result


def cmd_holiday(args):
    """查询法定假日"""
    try:
        from zhdate import ZhDate
        has_zhdate = True
    except ImportError:
        has_zhdate = False
    
    current_date = get_current_date()
    current_year = current_date.year
    
    # 2026年法定假日（基于农历计算）
    # 格式：(名称, 公历日期)
    holidays = []
    
    # 元旦
    holidays.append(('元旦', date(current_year, 1, 1)))
    
    # 春节（农历正月初一，需要计算）
    if has_zhdate:
        try:
            spring = ZhDate(current_year, 1, 1)
            holidays.append(('春节', spring.to_datetime().date()))
        except:
            pass
    
    # 清明节（使用 chinese-calendar 计算准确日期）
    all_terms = get_solar_terms_for_year(current_year)
    if '清明' in all_terms:
        holidays.append(('清明节', all_terms['清明']))
    
    # 劳动节
    holidays.append(('劳动节', date(current_year, 5, 1)))
    
    # 端午节（农历五月初五）
    if has_zhdate:
        try:
            dragon = ZhDate(current_year, 5, 5)
            holidays.append(('端午节', dragon.to_datetime().date()))
        except:
            pass
    
    # 中秋节（农历八月十五）
    if has_zhdate:
        try:
            mid_autumn = ZhDate(current_year, 8, 15)
            holidays.append(('中秋节', mid_autumn.to_datetime().date()))
        except:
            pass
    
    # 国庆节
    holidays.append(('国庆节', date(current_year, 10, 1)))
    
    # 下一年元旦
    holidays.append(('元旦', date(current_year + 1, 1, 1)))
    
    # 排序
    holidays.sort(key=lambda x: x[1])
    
    if args.next:
        # 查询下一个
        for name, h_date in holidays:
            if h_date >= current_date:
                diff = (h_date - current_date).days
                item = {
                    "name": name,
                    "date": h_date.strftime("%Y-%m-%d"),
                    "weekday": h_date.strftime("%A"),
                    "days_diff": diff,
                    "countdown": f"还有{diff}天" if diff > 0 else "今天！"
                }
                if has_zhdate:
                    try:
                        z = ZhDate.from_datetime(datetime.combine(h_date, datetime.min.time()))
                        item["lunar"] = z.chinese()
                    except:
                        pass
                return {
                    "status": "success",
                    "today": current_date.strftime("%Y-%m-%d"),
                    "next_holiday": item
                }
    elif args.all:
        # 查询所有
        all_holidays = []
        for name, h_date in holidays:
            diff = (h_date - current_date).days
            item = {
                "name": name,
                "date": h_date.strftime("%Y-%m-%d"),
                "weekday": h_date.strftime("%A"),
                "days_diff": diff,
                "passed": diff < 0
            }
            if has_zhdate:
                try:
                    z = ZhDate.from_datetime(datetime.combine(h_date, datetime.min.time()))
                    item["lunar"] = z.chinese()
                except:
                    pass
            all_holidays.append(item)
        return {
            "status": "success",
            "today": current_date.strftime("%Y-%m-%d"),
            "year": current_year,
            "holidays": all_holidays
        }
    else:
        # 默认：下一个假日
        for name, h_date in holidays:
            if h_date >= current_date:
                diff = (h_date - current_date).days
                item = {
                    "name": name,
                    "date": h_date.strftime("%Y-%m-%d"),
                    "weekday": h_date.strftime("%A"),
                    "days_diff": diff,
                    "countdown": f"还有{diff}天" if diff > 0 else "今天！"
                }
                if has_zhdate:
                    try:
                        z = ZhDate.from_datetime(datetime.combine(h_date, datetime.min.time()))
                        item["lunar"] = z.chinese()
                    except:
                        pass
                return {
                    "status": "success",
                    "today": current_date.strftime("%Y-%m-%d"),
                    "next_holiday": item
                }


def cmd_term(args):
    """查询节气"""
    current_date = get_current_date()
    current_year = current_date.year
    
    if args.all:
        # 查询所有节气
        terms = []
        all_terms = get_solar_terms_for_year(current_year)
        for i, term_info in enumerate(SOLAR_TERMS_INFO):
            term_name = term_info["name"]
            if term_name in all_terms:
                term_date = all_terms[term_name]
                countdown, days = calculate_countdown(term_date, current_date)
                terms.append({
                    "name": term_name,
                    "pinyin": term_info["pinyin"],
                    "date": term_date.strftime("%Y-%m-%d"),
                    "countdown": countdown,
                    "days": days,
                    "passed": days < 0
                })
        terms.sort(key=lambda x: x["days"])
        return {
            "status": "success",
            "current_date": current_date.strftime("%Y-%m-%d"),
            "year": current_year,
            "terms": terms
        }
    elif args.name:
        # 查询指定节气
        term_name = args.name
        if term_name not in SOLAR_TERMS:
            return {"status": "error", "msg": f"未找到节气「{term_name}」，可用节气：{', '.join(SOLAR_TERMS.keys())}"}
        
        term_index = SOLAR_TERMS[term_name]
        term_info = SOLAR_TERMS_INFO[term_index]
        
        # 获取今年和明年的节气
        term_date = get_solar_term_date(current_year, term_name)
        if term_date is None or term_date < current_date:
            term_date = get_solar_term_date(current_year + 1, term_name)
        
        if term_date is None:
            return {"status": "error", "msg": f"无法获取节气「{term_name}」日期"}
        
        countdown, days = calculate_countdown(term_date, current_date)
        
        return {
            "status": "success",
            "name": term_info["name"],
            "pinyin": term_info["pinyin"],
            "desc": term_info["desc"],
            "date": term_date.strftime("%Y-%m-%d"),
            "countdown": countdown,
            "days": days
        }
    else:
        # 查询下一个节气
        next_term = None
        next_date = None
        next_days = None
        next_info = None
        
        # 遍历当年所有节气，找第一个未过的
        all_terms = get_solar_terms_for_year(current_year)
        for term_name, term_date in all_terms.items():
            if term_date >= current_date:
                countdown, days = calculate_countdown(term_date, current_date)
                next_term = term_name
                next_info = SOLAR_TERMS_INFO[SOLAR_TERMS.get(term_name, 0)]
                next_date = term_date
                next_days = days
                break
        
        # 如果今年都过了，查下一年第一个节气
        if next_term is None:
            all_terms_next = get_solar_terms_for_year(current_year + 1)
            term_name = list(all_terms_next.keys())[0]
            term_date = all_terms_next[term_name]
            next_term = term_name
            next_info = SOLAR_TERMS_INFO[SOLAR_TERMS.get(term_name, 0)]
            next_date = term_date
            countdown, next_days = calculate_countdown(next_date, current_date)
        
        return {
            "status": "success",
            "current_date": current_date.strftime("%Y-%m-%d"),
            "next_term": next_term,
            "pinyin": next_info["pinyin"],
            "desc": next_info["desc"],
            "date": next_date.strftime("%Y-%m-%d"),
            "countdown": countdown,
            "days": next_days
        }


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description='全能日期管家', formatter_class=argparse.RawDescriptionHelpFormatter)
    
    subparsers = parser.add_subparsers(dest='action', help='操作')
    
    # 添加
    add_parser = subparsers.add_parser('add', help='添加记录')
    add_parser.add_argument('name', help='名称')
    add_parser.add_argument('--type', '-t', default='生日', 
                          choices=['生日', '纪念日', '祭日', '祭祖', 'birthday', 'anniversary', 'memorial', 'ancestor'],
                          help='类型')
    add_parser.add_argument('--date', '-d', help='公历日期 YYYY-MM-DD')
    add_parser.add_argument('--lunar', '-l', help='农历日期 月-日，如 8-10')
    add_parser.add_argument('--year', '-y', type=int, help='农历对应的公历年份（如：--lunar 8-10 --year 2015）')
    add_parser.add_argument('--remind', '-r', type=int, help='提前提醒天数 (1-30)')
    add_parser.add_argument('--relation', help='关系')
    add_parser.add_argument('--notes', help='备注')
    
    # 列表
    list_parser = subparsers.add_parser('list', help='查看列表')
    list_parser.add_argument('--type', '-t', 
                           choices=['生日', '纪念日', '祭日', '祭祖', 'birthday', 'anniversary', 'memorial', 'ancestor'],
                           help='筛选类型')
    
    # 今日
    today_parser = subparsers.add_parser('today', help='今日/近期查询')
    today_parser.add_argument('--days', '-n', type=int, default=7, help='查询天数')
    
    # 搜索
    search_parser = subparsers.add_parser('search', help='搜索')
    search_parser.add_argument('keyword', help='关键词')
    
    # 更新
    update_parser = subparsers.add_parser('update', help='更新')
    update_parser.add_argument('id', help='记录ID')
    update_parser.add_argument('--date', '-d', help='日期')
    update_parser.add_argument('--remind', '-r', type=int, help='提醒天数')
    update_parser.add_argument('--relation', help='关系')
    update_parser.add_argument('--notes', help='备注')
    
    # 删除
    delete_parser = subparsers.add_parser('delete', help='删除')
    delete_parser.add_argument('id', help='记录ID')
    
    # 详情
    get_parser = subparsers.add_parser('get', help='获取详情')
    get_parser.add_argument('id', help='记录ID')
    
    # 节气
    term_parser = subparsers.add_parser('term', help='查询节气')
    term_parser.add_argument('--name', '-n', help='节气名称，如 清明')
    term_parser.add_argument('--all', '-a', action='store_true', help='查询所有节气')
    
    # 公历农历互转
    convert_parser = subparsers.add_parser('convert', help='公历农历互转')
    convert_parser.add_argument('--solar', '-s', help='公历日期 YYYY-MM-DD')
    convert_parser.add_argument('--lunar', '-l', help='农历日期 月-日，如 8-15')
    convert_parser.add_argument('--year', '-y', type=int, help='指定农历年份（默认今年）')
    
    # 日期计算
    calc_parser = subparsers.add_parser('calc', help='日期计算')
    calc_parser.add_argument('--date', '-d', help='目标日期 YYYY-MM-DD')
    calc_parser.add_argument('--next-monday', '-m', action='store_true', help='计算下周一')
    calc_parser.add_argument('--week', '-w', help='本周星期几，如 Monday')
    calc_parser.add_argument('--days', '-n', type=int, help='计算N天后的日期')
    calc_parser.add_argument('--lunar', action='store_true', help='同时显示农历')
    calc_parser.add_argument('--month-end', '-e', action='store_true', help='计算月末日期')
    calc_parser.add_argument('--month-end-year', type=int, help='指定年份（配合--month-end）')
    calc_parser.add_argument('--month-end-month', type=int, help='指定月份（配合--month-end）')
    calc_parser.add_argument('--month-start', '-s', action='store_true', help='计算月初日期')
    calc_parser.add_argument('--month-start-year', type=int, help='指定年份（配合--month-start）')
    calc_parser.add_argument('--month-start-month', type=int, help='指定月份（配合--month-start）')
    
    # 法定假日
    holiday_parser = subparsers.add_parser('holiday', help='查询法定假日')
    holiday_parser.add_argument('--next', '-n', action='store_true', help='下一个假日')
    holiday_parser.add_argument('--all', '-a', action='store_true', help='所有假日')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    # 执行命令
    commands = {
        'add': cmd_add,
        'list': cmd_list,
        'today': cmd_today,
        'search': cmd_search,
        'update': cmd_update,
        'delete': cmd_delete,
        'get': cmd_get,
        'term': cmd_term,
        'convert': cmd_convert,
        'calc': cmd_calc,
        'holiday': cmd_holiday,
    }
    
    result = commands.get(args.action, lambda _: {"status": "error", "msg": "未知操作"})(args)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
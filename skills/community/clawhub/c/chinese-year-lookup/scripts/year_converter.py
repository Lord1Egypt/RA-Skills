#!/usr/bin/env python3
"""
中国历史年份转换工具
支持公元纪年、朝代年号纪年、干支纪年之间的相互转换
"""

import re
import sys

# 天干表
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支表
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 简化版朝代年号数据（起始年）
DYNASTY_DATA = {
    # 唐朝
    "武德": 618, "贞观": 627, "永徽": 650, "开元": 713, "天宝": 742,
    "肃宗": 756, "代宗": 762, "德宗": 779, "宪宗": 806, "穆宗": 821,
    "文宗": 827, "武宗": 841, "宣宗": 847, "懿宗": 859, "僖宗": 874,
    "昭宗": 889, "哀帝": 904,
    # 北宋
    "建隆": 960, "乾德": 963, "开宝": 968, "太平兴国": 976, "雍熙": 984,
    "端拱": 988, "淳化": 990, "咸平": 998, "景德": 1004, "大中祥符": 1008,
    "天禧": 1017, "乾兴": 1022, "天圣": 1023, "明道": 1032, "景祐": 1034,
    "宝元": 1038, "康定": 1040, "庆历": 1041, "皇祐": 1049, "至和": 1054,
    "嘉祐": 1056, "治平": 1064, "熙宁": 1068, "元丰": 1078, "元祐": 1086,
    "绍圣": 1094, "元符": 1098, "建中靖国": 1101, "崇宁": 1102, "大观": 1107,
    "政和": 1111, "重和": 1118, "宣和": 1119, "靖康": 1126,
    # 南宋
    "建炎": 1127, "绍兴": 1131, "隆兴": 1163, "乾道": 1165, "淳熙": 1174,
    "绍熙": 1190, "庆元": 1195, "嘉泰": 1201, "开禧": 1205, "嘉定": 1208,
    "宝庆": 1225, "绍定": 1228, "端平": 1234, "嘉熙": 1237, "淳祐": 1241,
    "宝祐": 1253, "开庆": 1259, "景定": 1260, "咸淳": 1265, "德祐": 1275,
    "祥兴": 1278,
    # 元朝
    "中统": 1260, "至元": 1264, "元贞": 1295, "大德": 1297, "至大": 1308,
    "皇庆": 1312, "延祐": 1314, "至治": 1321, "泰定": 1324, "天历": 1328,
    "至顺": 1330, "元统": 1333, "至元": 1335, "至正": 1341,
    # 明朝
    "洪武": 1368, "建文": 1399, "永乐": 1403, "洪熙": 1425, "宣德": 1426,
    "正统": 1436, "景泰": 1450, "天顺": 1457, "成化": 1465, "弘治": 1488,
    "正德": 1506, "嘉靖": 1522, "隆庆": 1567, "万历": 1573, "泰昌": 1620,
    "天启": 1621, "崇祯": 1628,
    # 清朝
    "顺治": 1644, "康熙": 1661, "雍正": 1723, "乾隆": 1736, "嘉庆": 1796,
    "道光": 1821, "咸丰": 1851, "同治": 1862, "光绪": 1875, "宣统": 1909,
    # 近代
    "民国": 1912,
}


def tiangan_to_index(tg: str) -> int:
    """天干转索引"""
    try:
        return TIANGAN.index(tg)
    except ValueError:
        return -1


def dizhi_to_index(dz: str) -> int:
    """地支转索引"""
    try:
        return DIZHI.index(dz)
    except ValueError:
        return -1


def gan_zhi_from_year(year: int) -> str:
    """公元年份转干支"""
    if year > 0:
        tg_idx = (year - 4) % 10
        dz_idx = (year - 4) % 12
    else:
        # 公元前处理（简化）
        tg_idx = (year + 1) % 10
        dz_idx = (year + 1) % 12
    return TIANGAN[tg_idx] + DIZHI[dz_idx] + "年"


def year_from_gan_zhi(gan_zhi: str) -> int:
    """干支转公元年份（返回最接近的年份）"""
    if not gan_zhi or len(gan_zhi) < 2:
        return None
    
    tg = gan_zhi[0]
    dz = gan_zhi[1]
    
    tg_idx = tiangan_to_index(tg)
    dz_idx = dizhi_to_index(dz)
    
    if tg_idx == -1 or dz_idx == -1:
        return None
    
    # 以甲子年（4年）为基准
    # 尝试找到匹配的年份
    for year in range(1, 2100):
        if (year - 4) % 10 == tg_idx and (year - 4) % 12 == dz_idx:
            return year
    
    return None


def parse_era_year(input_str: str) -> tuple:
    """解析年号纪年，返回(年号, 年份)"""
    # 匹配 "XX年" 格式
    year_match = re.search(r'(\D+?)(\d+)年?', input_str)
    if year_match:
        era_name = year_match.group(1)
        year_num = int(year_match.group(2))
        return era_name, year_num
    return None, None


def convert_era_to_ad(era_name: str, year_num: int) -> int:
    """年号纪年转公元纪年"""
    if era_name in DYNASTY_DATA:
        start_year = DYNASTY_DATA[era_name]
        return start_year + year_num - 1
    return None


def format_output(year: int, include_ganzhi: bool = True) -> dict:
    """格式化输出"""
    result = {
        "公元": f"{year}年" if year > 0 else f"公元前{abs(year)}年",
        "干支": gan_zhi_from_year(year) if include_ganzhi else None,
    }
    
    # 简化版朝代判断
    if year >= 1644:
        if year < 1661:
            result["朝代"] = "清朝（顺治）"
        elif year < 1723:
            result["朝代"] = "清朝（康熙）"
        elif year < 1736:
            result["朝代"] = "清朝（雍正）"
        elif year < 1796:
            result["朝代"] = "清朝（乾隆）"
        elif year < 1821:
            result["朝代"] = "清朝（嘉庆）"
        elif year < 1851:
            result["朝代"] = "清朝（道光）"
        elif year < 1862:
            result["朝代"] = "清朝（咸丰）"
        elif year < 1875:
            result["朝代"] = "清朝（同治）"
        elif year < 1909:
            result["朝代"] = "清朝（光绪）"
        else:
            result["朝代"] = "清朝（宣统）"
    elif year >= 1368:
        result["朝代"] = "明朝"
    elif year >= 1271:
        result["朝代"] = "元朝"
    elif year >= 960:
        result["朝代"] = "宋朝"
    elif year >= 618:
        result["朝代"] = "唐朝"
    elif year >= 581:
        result["朝代"] = "隋朝"
    else:
        result["朝代"] = "其他"
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python year_converter.py <year>")
        print("Example: python year_converter.py 1234")
        print("Example: python year_converter.py 甲子")
        print("Example: python year_converter.py 绍定六年")
        sys.exit(1)
    
    input_str = sys.argv[1]
    
    # 判断输入类型
    # 1. 纯数字 -> 公元纪年
    if input_str.isdigit() or (input_str.startswith('-') and input_str[1:].isdigit()):
        year = int(input_str)
        result = format_output(year)
        print(f"公元纪年: {result['公元']}")
        print(f"干支纪年: {result['干支']}")
        print(f"朝代: {result['朝代']}")
    
    # 2. 干支纪年（如甲子、乙丑）
    elif re.match(r'^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]年?$', input_str):
        year = year_from_gan_zhi(input_str)
        if year:
            result = format_output(year)
            print(f"干支纪年: {input_str}")
            print(f"公元纪年: {result['公元']}")
            print(f"朝代: {result['朝代']}")
        else:
            print("无法识别干支")
    
    # 3. 年号纪年（如绍定六年、康熙元年）
    else:
        era_name, year_num = parse_era_year(input_str)
        if era_name and year_num:
            ad_year = convert_era_to_ad(era_name, year_num)
            if ad_year:
                result = format_output(ad_year)
                print(f"年号: {era_name}{year_num}年")
                print(f"公元纪年: {result['公元']}")
                print(f"干支纪年: {result['干支']}")
            else:
                print(f"未找到年号: {era_name}")
        else:
            print("无法解析输入格式")


if __name__ == "__main__":
    main()

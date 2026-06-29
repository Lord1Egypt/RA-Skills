#!/usr/bin/env python3
"""
COC人物属性解析器
功能：比对玩家导出的人物属性与默认属性，提取不同的部分
"""

import re
import sys
from pathlib import Path

# 默认属性定义 - 格式：属性名: 默认值
# 中文属性名和英文缩写都是同一个属性的别名
DEFAULT_ATTRIBUTES = {
    # 基础属性
    "力量": 0, "str": 0,
    "敏捷": 0, "dex": 0,
    "意志": 0, "pow": 0,
    "体质": 0, "con": 0,
    "外貌": 0, "app": 0,
    "教育": 0, "edu": 0,
    "体型": 0, "siz": 0,
    "智力": 0, "灵感": 0, "int": 0,
    "san": 0, "san值": 0,
    "理智": 0, "理智值": 0,
    "幸运": 0, "运气": 0,
    "mp": 0, "魔法": 0,
    "hp": 0, "体力": 0,

    # 技能属性 - 使用较低的默认值（通常为1或5）
    "会计": 5,
    "人类学": 1,
    "估价": 5,
    "考古学": 1,
    "取悦": 15,
    "魅惑": 15,
    "攀爬": 20,
    "计算机": 5, "计算机使用": 5, "电脑": 5,
    "信用": 0, "信誉": 0, "信用评级": 0,
    "克苏鲁": 0, "克苏鲁神话": 0, "cm": 0,
    "乔装": 5,
    "闪避": 0,
    "汽车": 20, "驾驶": 20, "汽车驾驶": 20,
    "电气维修": 10,
    "电子学": 1,
    "话术": 5,
    "斗殴": 25,
    "手枪": 20,
    "急救": 30,
    "历史": 5,
    "恐吓": 15,
    "跳跃": 20,
    "母语": 0,
    "法律": 5,
    "图书馆": 20, "图书馆使用": 20,
    "聆听": 20,
    "开锁": 1, "撬锁": 1, "锁匠": 1,
    "机械维修": 10,
    "医学": 1,
    "博物学": 10, "自然学": 10,
    "领航": 10, "导航": 10,
    "神秘学": 5,
    "重型操作": 1, "重型机械": 1, "操作重型机械": 1, "重型": 1,
    "说服": 10,
    "精神分析": 1,
    "心理学": 10,
    "骑术": 5,
    "妙手": 10,
    "侦查": 25,
    "潜行": 20,
    "生存": 10,
    "游泳": 20,
    "投掷": 20,
    "追踪": 10,
    "驯兽": 5,
    "潜水": 1,
    "爆破": 1,
    "读唇": 1,
    "催眠": 1,
    "炮术": 1
}

# 属性别名映射 - 将所有别名映射到一个标准名称
ATTRIBUTE_ALIASES = {
    # 基础属性
    "str": "力量", "力量": "力量",
    "dex": "敏捷", "敏捷": "敏捷",
    "pow": "意志", "意志": "意志",
    "con": "体质", "体质": "体质",
    "app": "外貌", "外貌": "外貌",
    "edu": "教育", "教育": "教育",
    "siz": "体型", "体型": "体型",
    "int": "智力", "智力": "智力", "灵感": "智力",
    "san": "san", "san值": "san",
    "理智": "理智", "理智值": "理智",
    "幸运": "幸运", "运气": "幸运",
    "mp": "mp", "魔法": "mp",
    "hp": "hp", "体力": "hp",

    # 技能属性
    "会计": "会计",
    "人类学": "人类学",
    "估价": "估价",
    "考古学": "考古学",
    "取悦": "取悦", "魅惑": "取悦",
    "攀爬": "攀爬",
    "计算机": "计算机", "计算机使用": "计算机", "电脑": "计算机",
    "信用": "信用", "信誉": "信用", "信用评级": "信用",
    "克苏鲁": "克苏鲁", "克苏鲁神话": "克苏鲁", "cm": "克苏鲁",
    "乔装": "乔装",
    "闪避": "闪避",
    "汽车": "汽车", "驾驶": "汽车", "汽车驾驶": "汽车",
    "电气维修": "电气维修",
    "电子学": "电子学",
    "话术": "话术",
    "斗殴": "斗殴",
    "手枪": "手枪",
    "急救": "急救",
    "历史": "历史",
    "恐吓": "恐吓",
    "跳跃": "跳跃",
    "母语": "母语",
    "法律": "法律",
    "图书馆": "图书馆", "图书馆使用": "图书馆",
    "聆听": "聆听",
    "开锁": "开锁", "撬锁": "开锁", "锁匠": "开锁",
    "机械维修": "机械维修",
    "医学": "医学",
    "博物学": "博物学", "自然学": "博物学",
    "领航": "领航", "导航": "领航",
    "神秘学": "神秘学",
    "重型操作": "重型操作", "重型机械": "重型操作", "操作重型机械": "重型操作", "重型": "重型操作",
    "说服": "说服",
    "精神分析": "精神分析",
    "心理学": "心理学",
    "骑术": "骑术",
    "妙手": "妙手",
    "侦查": "侦查",
    "潜行": "潜行",
    "生存": "生存",
    "游泳": "游泳",
    "投掷": "投掷",
    "追踪": "追踪",
    "驯兽": "驯兽",
    "潜水": "潜水",
    "爆破": "爆破",
    "读唇": "读唇",
    "催眠": "催眠",
    "炮术": "炮术"
}


def parse_attribute_text(text: str) -> dict:
    """
    解析属性文本，提取属性名和数值

    支持的格式：
    - 力量0 str0 敏捷0 dex0 ...
    - 力量: 0 敏捷: 0 ...
    - 力量=0 敏捷=0 ...
    - 力量 0 敥捷 0 ...
    """
    # 清理文本
    text = text.strip()

    # 使用正则表达式匹配 "属性名+数值" 的模式
    # 匹配：中文/英文属性名 + 可选的分隔符(: = 空格) + 数字
    pattern = r'([a-zA-Z一-鿿]+)\s*[:=\s]?\s*(\d+)'

    matches = re.findall(pattern, text)

    attributes = {}
    for attr_name, value in matches:
        # 转换为小写
        attr_name_lower = attr_name.lower()

        # 检查是否是已知的属性
        if attr_name_lower in ATTRIBUTE_ALIASES:
            # 获取标准名称
            standard_name = ATTRIBUTE_ALIASES[attr_name_lower]
            # 存储值（后面的值会覆盖前面的，因为可能有别名）
            attributes[standard_name] = int(value)
        else:
            # 未知属性，直接使用原名（保留中文）
            attributes[attr_name] = int(value)

    return attributes


def compare_attributes(player_attrs: dict) -> tuple:
    """
    比对玩家属性与默认属性

    返回：
    - diff_attrs: 与默认属性不同的属性字典 {标准名称: (玩家值, 默认值)}
    - new_attrs: 玩家有但默认属性中没有的属性
    """
    diff_attrs = {}
    new_attrs = {}

    for attr_name, player_value in player_attrs.items():
        if attr_name in DEFAULT_ATTRIBUTES:
            default_value = DEFAULT_ATTRIBUTES[attr_name]
            if player_value != default_value:
                diff_attrs[attr_name] = (player_value, default_value)
        else:
            new_attrs[attr_name] = player_value

    return diff_attrs, new_attrs


def get_attr_value(player_attrs, aliases):
    """从玩家属性中查找值"""
    for alias in aliases:
        if alias in player_attrs:
            return player_attrs[alias]
    return None

def generate_character_card(player_name: str, player_attrs: dict, diff_attrs: dict, new_attrs: dict) -> str:
    """
    生成人物卡markdown内容（表格格式）
    """
    # 基础属性别名映射
    attr_aliases = {
        "力量": ["力量", "str"],
        "敏捷": ["敏捷", "dex"],
        "意志": ["意志", "pow"],
        "体质": ["体质", "con"],
        "外貌": ["外貌", "app"],
        "教育": ["教育", "edu"],
        "体型": ["体型", "siz"],
        "智力": ["智力", "灵感", "int"],
        "san": ["san", "san值", "理智", "理智值"],
        "幸运": ["幸运", "运气"],
        "mp": ["mp", "魔法"],
        "hp": ["hp", "体力"]
    }

    lines = [
        f"# {player_name}",
        "",
    ]

    # 9围属性 - 3x3表格
    nine_attrs = ["力量", "敏捷", "意志", "体质", "外貌", "教育", "体型", "智力", "幸运"]
    nine_values = []
    for attr in nine_attrs:
        value = get_attr_value(player_attrs, attr_aliases[attr])
        nine_values.append(value if value is not None else 0)

    lines.append("| 力量 | 敏捷 | 意志 |")
    lines.append("| :---: | :---: | :---: |")
    lines.append(f"| {nine_values[0]} | {nine_values[1]} | {nine_values[2]} |")
    lines.append("| 体质 | 外貌 | 教育 |")
    lines.append(f"| {nine_values[3]} | {nine_values[4]} | {nine_values[5]} |")
    lines.append("| 体型 | 智力 | 幸运 |")
    lines.append(f"| {nine_values[6]} | {nine_values[7]} | {nine_values[8]} |")
    lines.append("")

    # hp、mp、san - 一行3列表格
    hp_value = get_attr_value(player_attrs, attr_aliases["hp"])
    mp_value = get_attr_value(player_attrs, attr_aliases["mp"])
    san_value = get_attr_value(player_attrs, attr_aliases["san"])

    lines.append("| hp | mp | san |")
    lines.append("| :---: | :---: | :---: |")
    lines.append(f"| {hp_value if hp_value is not None else 0} | {mp_value if mp_value is not None else 0} | {san_value if san_value is not None else 0} |")
    lines.append("")

    # 技能部分 - 3列表格
    base_aliases = [alias for aliases in attr_aliases.values() for alias in aliases]
    skill_diff = {k: v for k, v in diff_attrs.items() if k not in base_aliases}
    skill_new = {k: v for k, v in new_attrs.items() if k not in base_aliases}

    all_skills = {}
    for attr_name, (player_value, default_value) in skill_diff.items():
        all_skills[attr_name] = player_value
    for attr_name, value in skill_new.items():
        all_skills[attr_name] = value

    if all_skills:
        lines.append("## 技能")
        lines.append("")

        # 将技能分成3列
        skill_list = sorted(all_skills.items())
        rows = (len(skill_list) + 2) // 3  # 向上取整

        lines.append("| 技能 | 值 | 技能 | 值 | 技能 | 值 |")
        lines.append("| :--- | :---: | :--- | :---: | :--- | :---: |")

        for i in range(rows):
            row_items = []
            for j in range(3):
                idx = i + j * rows
                if idx < len(skill_list):
                    name, value = skill_list[idx]
                    row_items.extend([name, str(value)])
                else:
                    row_items.extend(["", ""])
            lines.append(f"| {row_items[0]} | {row_items[1]} | {row_items[2]} | {row_items[3]} | {row_items[4]} | {row_items[5]} |")

        lines.append("")

    return "\n".join(lines)


def save_character_card(content: str, filename: str = "人物卡.md"):
    """保存人物卡到文件"""
    output_path = Path(filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"人物卡已保存到: {output_path.absolute()}")


def main():
    """主函数"""
    print("=" * 60)
    print("COC人物属性解析器")
    print("=" * 60)
    print()

    # 获取玩家名称
    player_name = input("请输入玩家名称/角色名称: ").strip()
    if not player_name:
        player_name = "未命名角色"

    print()
    print("请输入导出的人物属性文本（支持多种格式）:")
    print("格式示例：力量0 str0 敏捷0 dex0 ...")
    print("输入完成后按两次回车结束:")
    print()

    # 读取多行输入
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break

    attribute_text = "\n".join(lines)

    if not attribute_text.strip():
        print("错误：未输入任何属性文本")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("解析结果")
    print("=" * 60)

    # 解析属性
    player_attrs = parse_attribute_text(attribute_text)

    if not player_attrs:
        print("错误：未能解析出任何有效属性")
        print("请检查输入格式是否正确")
        sys.exit(1)

    print(f"\n成功解析 {len(player_attrs)} 个属性")

    # 比对属性
    diff_attrs, new_attrs = compare_attributes(player_attrs)

    print(f"与默认属性不同的属性: {len(diff_attrs)} 个")
    print(f"新增属性: {len(new_attrs)} 个")

    # 生成人物卡
    character_card = generate_character_card(player_name, player_attrs, diff_attrs, new_attrs)

    # 保存文件
    save_character_card(character_card)

    # 显示预览
    print("\n" + "=" * 60)
    print("人物卡预览")
    print("=" * 60)
    print(character_card)


def batch_process(input_file: str, output_dir: str = "."):
    """
    批量处理模式 - 从文件读取多个角色的属性

    文件格式：每行一个角色，格式为 "角色名|属性文本"
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('|', 1)
            if len(parts) != 2:
                print(f"警告：第 {line_num} 行格式错误，跳过")
                continue

            player_name, attribute_text = parts
            player_name = player_name.strip()
            attribute_text = attribute_text.strip()

            # 解析属性
            player_attrs = parse_attribute_text(attribute_text)
            if not player_attrs:
                print(f"警告：角色 '{player_name}' 无有效属性，跳过")
                continue

            # 比对属性
            diff_attrs, new_attrs = compare_attributes(player_attrs)

            # 生成并保存人物卡
            character_card = generate_character_card(player_name, player_attrs, diff_attrs, new_attrs)
            filename = f"{player_name}_人物卡.md"
            save_character_card(character_card, output_path / filename)

            print(f"已处理: {player_name}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行参数模式
        if sys.argv[1] == "--batch" and len(sys.argv) >= 3:
            input_file = sys.argv[2]
            output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
            batch_process(input_file, output_dir)
        elif sys.argv[1] == "--help":
            print("用法:")
            print("  python coc_character_parser.py              # 交互模式")
            print("  python coc_character_parser.py --batch input.txt [output_dir]  # 批量处理模式")
            print()
            print("批量处理文件格式:")
            print("  角色名|属性文本")
            print("  例如: 张三|力量50敏捷60...")
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("使用 --help 查看帮助")
    else:
        # 交互模式
        main()

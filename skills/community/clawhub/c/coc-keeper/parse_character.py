#!/usr/bin/env python3
"""
COC人物属性解析器 - 快速调用版本
用于AI快速解析玩家导出的属性文本
"""

import sys
import json
from coc_character_parser import parse_attribute_text, compare_attributes, generate_character_card, save_character_card


def quick_parse(player_name: str, attribute_text: str, output_file: str = None) -> dict:
    """
    快速解析函数

    参数:
        player_name: 玩家/角色名称
        attribute_text: 导出的属性文本
        output_file: 输出文件路径（可选）

    返回:
        包含解析结果的字典
    """
    # 解析属性
    player_attrs = parse_attribute_text(attribute_text)

    if not player_attrs:
        return {
            "success": False,
            "error": "未能解析出任何有效属性"
        }

    # 比对属性
    diff_attrs, new_attrs = compare_attributes(player_attrs)

    # 生成人物卡
    character_card = generate_character_card(player_name, player_attrs, diff_attrs, new_attrs)

    # 保存文件
    if output_file:
        save_character_card(character_card, output_file)
    else:
        output_file = f"{player_name}_人物卡.md"
        save_character_card(character_card, output_file)

    # 返回结果
    return {
        "success": True,
        "player_name": player_name,
        "total_attributes": len(player_attrs),
        "modified_attributes": len(diff_attrs),
        "new_attributes": len(new_attrs),
        "diff_attributes": {k: {"player": v[0], "default": v[1]} for k, v in diff_attrs.items()},
        "new_attributes_list": new_attrs,
        "output_file": output_file
    }


def main():
    """命令行调用接口"""
    if len(sys.argv) < 3:
        print("用法: python parse_character.py <角色名称> <属性文本> [输出文件]")
        print()
        print("示例:")
        print('  python parse_character.py "张三" "力量50敏捷60意志70体质80外貌55教育65体型75智力80san65理智65幸运55mp13hp15"')
        print()
        print("或者从stdin读取属性文本:")
        print('  echo "力量50敏捷60..." | python parse_character.py "张三" -')
        sys.exit(1)

    player_name = sys.argv[1]
    attribute_text = sys.argv[2]

    # 从stdin读取
    if attribute_text == "-":
        attribute_text = sys.stdin.read()

    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    # 执行解析
    result = quick_parse(player_name, attribute_text, output_file)

    # 输出JSON结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

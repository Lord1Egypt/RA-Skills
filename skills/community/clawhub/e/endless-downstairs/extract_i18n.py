#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取所有中文文案到翻译文件
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
EVENTS_DIR = DATA_DIR / "events"
I18N_DIR = Path(__file__).parent / "i18n"


def extract_events():
    """提取所有事件文案"""
    events = {}

    for event_file in EVENTS_DIR.glob("*.json"):
        with open(event_file, 'r', encoding='utf-8') as f:
            event_list = json.load(f)

        for event in event_list:
            event_id = event.get('id')
            if not event_id:
                continue

            events[event_id] = {
                "description": event.get('description', ''),
                "choices": {}
            }

            for i, choice in enumerate(event.get('choices', [])):
                # 使用索引作为 key，因为有些选项没有唯一标识
                choice_text = choice.get('text', '')
                events[event_id]["choices"][str(i)] = choice_text

    return events


def extract_items():
    """提取物品文案"""
    items = {}

    items_file = DATA_DIR / "items.json"
    if items_file.exists():
        with open(items_file, 'r', encoding='utf-8') as f:
            item_list = json.load(f)

        for item in item_list:
            item_id = item.get('id')
            if not item_id:
                continue

            items[item_id] = {
                "name": item.get('name', ''),
                "description": item.get('description', '')
            }

    return items


def extract_ui():
    """提取 UI 文案"""
    return {
        # game.py
        "load_failed": "加载存档失败",
        "game_over": "游戏已结束请开始新游戏",
        "invalid_number": "请输入有效的数字",
        "invalid_choice": "无效的选项",
        "success": "成功！",
        "fail": "失败...",
        "no_items": "你还没有获得任何物品",
        "item_details": "=== 物品详情 ===",
        "no_save": "没有存档",
        "no_save_new": "没有存档，请开始新游戏",
        "usage_choose": "用法: python game.py choose <数字>",
        "usage_input": "用法: python game.py input <文字>",
        "unknown_command": "未知命令",
        "usage": "用法: python game.py [new|choose|status|inventory|input]",
        "cannot_do": "你不能这样做",

        # help text
        "help_commands": "命令:",
        "help_new": "开始新游戏",
        "help_choose": "选择第N个选项",
        "help_status": "查看状态",
        "help_inventory": "查看背包",
        "help_continue": "继续游戏/显示当前事件",
        "help_input": "输入文字",
        "help_help": "显示帮助",
        "help_quit": "退出游戏",

        # game_state.py
        "status_title": "=== 状态 ===",
        "status_floor": "楼层",
        "status_items": "物品",
        "status_abilities": "能力",
        "status_none": "无",
        "sanity_stable": "你的精神稳定，神明保佑着你",
        "sanity_unstable": "你的精神开始不稳定，不详的东西会出现",
        "sanity_damaged": "你的精神已经受到较大的损耗，出现的东西会更加邪恶",
        "sanity_collapsing": "你已接近崩溃，世界开始扭曲",
        "advice_title": "=== 伪人的忠告 ===",
        "advice_1": "【第一条】听到奇怪的声音，不要回头",
        "advice_2": "【第二条】光越亮，黑暗越强",
        "advice_3": "【第三条】偶数楼层会带来好运",
        "advice_4": "【第四条】如果看到两个13，停止任何行动",
        "advice_5": "【第五条】不要敲13次门",

        # choice_handler.py
        "cannot_do_action": "你不能这样做",
        "requirements_not_met": "你不满足选择条件",
        "checkpoint_loaded": "=== 存档已加载 ===",
        "checkpoint_load_failed": "读取存档失败",
        "lost_item": "失去了物品",
        "floor_changed": "楼层",
        "game_over_restart": "游戏结束，重新开始吗？",
        "game_win": "游戏结束，恭喜你通关！",
        "requires_item": "需要物品",
        "requires_ability": "需要能力",
        "requires_debuff": "需要负面状态",
    }


def main():
    """主函数"""
    translations = {
        "events": extract_events(),
        "items": extract_items(),
        "ui": extract_ui()
    }

    # 保存中文翻译
    zh_file = I18N_DIR / "zh.json"
    with open(zh_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    print(f"已生成: {zh_file}")

    # 生成英文翻译模板
    en_file = I18N_DIR / "en.json"
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    print(f"已生成: {en_file} (需要翻译)")


if __name__ == '__main__':
    main()

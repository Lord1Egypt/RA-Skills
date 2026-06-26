#!/usr/bin/env python3
"""
Chat History - Trigger关键词处理器
识别自然语言中的触发词，映射到对应命令，并提供用户确认机制
"""

import re


# Trigger关键词配置
TRIGGER_KEYWORDS = {
    "start": {
        "keywords": [
            "开启自动归档", "启动自动归档",
            "打开自动归档", "开始自动归档",
            "开启归档", "启动归档",
            "归档服务开始", "自动归档开始",
            "启动", "开启", "开始"
        ],
        "command": "--start",
        "description": "启动自动归档功能",
        "confirm": "确认要启动自动归档吗？"
    },

    "stop": {
        "keywords": [
            "停止自动归档", "关闭自动归档",
            "停止归档", "关闭归档",
            "归档停止", "暂停归档",
            "关闭", "停止", "暂停"
        ],
        "command": "--stop",
        "description": "停止自动归档功能",
        "confirm": "确认要停止自动归档吗？"
    },

    "status": {
        "keywords": [
            "归档状态", "归档情况", "归档系统状态",
            "自动归档状态", "备份状态",
            "看看归档", "查看归档", "归档怎么样"
        ],
        "command": "--status",
        "description": "查看归档状态",
        "confirm": None  # 不需要确认
    },

    "list": {
        "keywords": [
            "列出归档", "列出所有归档", "列出对话",
            "看看归档", "查看归档", "显示归档",
            "列出所有", "查看所有", "显示所有对话"
        ],
        "command": "--list",
        "description": "列出所有归档",
        "confirm": None
    },

    "list_channel": {
        "keywords": [
            "列出channel归档", "列出channel端",
            "查看channel归档", "显示channel归档",
            "channel归档"
        ],
        "command": "--list channel",
        "description": "列出Channel端归档",
        "confirm": None
    },

    "list_webui": {
        "keywords": [
            "列出webui归档", "列出webui端",
            "查看webui归档", "显示webui归档",
            "webui归档"
        ],
        "command": "--list webui",
        "description": "列出WebUI端归档",
        "confirm": None
    },

    "search": {
        "keywords": [
            "搜索", "找", "查找", "搜索对话",
            "查找对话", "搜索记录", "找记录",
            "查历史"
        ],
        "command": "--search",
        "description": "搜索对话记录",
        "confirm": None,
        "need_keyword": True  # 需要提取搜索关键词
    },

    "list_evaluations": {
        "keywords": [
            "评估过的skills", "评估记录",
            "评估过的", "我评估过哪些",
            "列出评估", "评估skills"
        ],
        "command": "--list-evaluations",
        "description": "列出评估过的skills",
        "confirm": None
    },

    "help": {
        "keywords": [
            "帮助", "帮助信息", "指令",
            "命令", "怎么用", "使用说明"
        ],
        "command": "--help",
        "description": "查看帮助信息",
        "confirm": None
    },

    "keyword": {
        "keywords": [
            "触发关键词", "关键词列表",
            "触发词", "有哪些词可以触发"
        ],
        "command": "--keyword",
        "description": "列出所有触发关键词",
        "confirm": None
    }
}


def match_trigger(user_input):
    """
    匹配用户输入的触发词

    Args:
        user_input: 用户输入的字符串

    Returns:
        (matched_trigger, extracted_keyword)
        - matched_trigger: 匹配到的trigger配置，如果没有匹配则为None
        - extracted_keyword: 提取的搜索关键词（仅对search trigger）
    """
    user_input_lower = user_input.lower()

    for trigger_name, trigger_config in TRIGGER_KEYWORDS.items():
        for keyword in trigger_config["keywords"]:
            if keyword.lower() in user_input_lower:
                # 提取搜索关键词（仅对search trigger）
                extracted_keyword = None
                if trigger_config.get("need_keyword", False):
                    # 尝试提取搜索关键词
                    # 例如："搜索视频" → 提取"视频"
                    for kw in trigger_config["keywords"]:
                        if kw.lower() in user_input_lower:
                            # 移除触发词，提取剩余部分作为关键词
                            idx = user_input_lower.find(kw.lower())
                            extracted_keyword = user_input[idx + len(kw):].strip()
                            # 去除标点符号
                            extracted_keyword = re.sub(r'[^\w\s\u4e00-\u9fff]', '', extracted_keyword).strip()
                            if not extracted_keyword:
                                extracted_keyword = None
                            break

                return trigger_config, extracted_keyword

    return None, None


def execute_with确认(trigger_config, extracted_keyword=None, get_user_input=None):
    """
    执行trigger命令，需要用户确认

    Args:
        trigger_config: trigger配置
        extracted_keyword: 提取的搜索关键词
        get_user_input: 用户输入函数（用于测试时可以传入模拟函数）

    Returns:
        (should_execute, command_output)
        - should_execute: 是否应该执行
        - command_output: 命令输出（如果执行了）
    """
    # 显示识别到的意图
    output = []
    output.append(f"🎯 识别到您的意图：{trigger_config['description']}\n")

    # 提取的关键词
    if extracted_keyword:
        output.append(f"🔍 搜索关键词：{extracted_keyword}\n")

    # 需要确认的命令
    if trigger_config.get("confirm"):
        output.append(f"⚠️  {trigger_config['confirm']}")
        output.append("\n请输入 Y 或 y 确认，其他任意键取消：\n")

        # 打印提示
        print("\n".join(output))

        # 获取用户输入
        if get_user_input:
            user_response = get_user_input()
        else:
            user_response = input()

        user_response_lower = user_response.lower().strip()

        if user_response_lower in ["y", "yes", "是", "确认"]:
            print("✅ 用户确认，执行命令\n")
            return True, f"执行命令: {trigger_config['command']}"
        else:
            print("❌ 用户取消，不执行\n")
            return False, "用户取消操作"

    # 不需要确认的命令
    else:
        output.append("✅ 自动执行，无需确认\n")
        print("\n".join(output))
        return True, f"执行命令: {trigger_config['command']}"


def main():
    """主函数 - 测试trigger功能"""
    import sys

    print("🎯 Chat History Trigger关键词测试\n")

    while True:
        user_input = input("请输入指令（输入 'quit' 退出）: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 测试退出")
            break

        # 匹配触发词
        trigger_config, extracted_keyword = match_trigger(user_input)

        if not trigger_config:
            print(f"❌ 未识别到触发词: {user_input}\n")
            continue

        # 执行命令（带确认）
        should_execute, command_output = execute_with确认(trigger_config, extracted_keyword)
        print(command_output)
        print()


if __name__ == "__main__":
    main()

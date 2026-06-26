#!/usr/bin/env python3
"""
DeepSeek Web Query - 用于 OpenClaw 的 DeepSeek 查询辅助脚本

这个脚本不直接控制浏览器，而是输出需要执行的浏览器操作指令，
由 OpenClaw 的 browser 工具来执行实际的浏览器控制。

使用方式:
1. 用户在 OpenClaw 中提出查询请求
2. OpenClaw 调用此脚本优化问题
3. OpenClaw 使用 browser 工具控制浏览器访问 DeepSeek
4. 获取结果后返回给用户
"""

import sys
import json


# 登录页面特征选择器
LOGIN_PAGE_SELECTORS = [
    'textbox[placeholder*="手机号"]',  # 手机号输入框
    'textbox[placeholder*="验证码"]',  # 验证码输入框
    'button:has-text("登录")',  # 登录按钮
    'button:has-text("发送验证码")',  # 发送验证码按钮
    'text:has-text("微信扫码登录")',  # 微信登录提示
]

# 聊天页面特征选择器（已登录状态）
CHAT_PAGE_SELECTORS = [
    'textarea[placeholder*="发送消息"]',
    'textarea[placeholder*="Message"]',
    '#chat-input',
    '[contenteditable="true"]',
    '.chat-input',
    '[class*="chat-input"]',
]


def check_login_status(snapshot_data: dict) -> dict:
    """
    根据浏览器快照数据检测登录状态
    
    Args:
        snapshot_data: browser snapshot 返回的页面元素数据
    
    Returns:
        dict: 包含登录状态检测结果
    """
    result = {
        'is_logged_in': False,
        'is_login_page': False,
        'detected_elements': [],
        'suggestion': None
    }
    
    # 将 snapshot 转为字符串以便检查
    snapshot_str = json.dumps(snapshot_data, ensure_ascii=False)
    
    # 检查登录页面特征
    login_indicators = [
        '手机号',
        '验证码',
        '发送验证码',
        '微信扫码登录',
        '登录',
        '注册',
        '请输入手机号',
        '请输入验证码'
    ]
    
    # 检查聊天页面特征
    chat_indicators = [
        '发送消息',
        'Message',
        'chat-input',
        'chat-input',
        '新对话',
        '深度思考',
        '联网搜索'
    ]
    
    # 统计匹配的特征
    login_matches = sum(1 for indicator in login_indicators if indicator in snapshot_str)
    chat_matches = sum(1 for indicator in chat_indicators if indicator in snapshot_str)
    
    # 判断页面类型
    if login_matches >= 2 and chat_matches == 0:
        result['is_login_page'] = True
        result['is_logged_in'] = False
        result['suggestion'] = "检测到 DeepSeek 登录页面，请先完成登录（手机号+验证码或微信扫码）"
    elif chat_matches >= 1:
        result['is_logged_in'] = True
        result['is_login_page'] = False
        result['suggestion'] = "已登录 DeepSeek，可以开始查询"
    else:
        # 无法确定状态，可能是加载中或其他页面
        result['suggestion'] = "页面状态未知，请检查 DeepSeek 是否加载完成"
    
    result['login_indicators'] = login_matches
    result['chat_indicators'] = chat_matches
    
    return result


def generate_browser_instructions(question: str, is_logged_in: bool = False) -> dict:
    """
    生成浏览器操作指令
    
    这些指令将被 OpenClaw 的 browser 工具执行
    """
    if not is_logged_in:
        # 未登录，只返回导航到登录页的指令
        return {
            'url': 'https://chat.deepseek.com/',
            'needs_login': True,
            'steps': [
                {
                    'action': 'navigate',
                    'url': 'https://chat.deepseek.com/'
                },
                {
                    'action': 'wait',
                    'time_ms': 3000,
                    'description': '等待页面加载'
                }
            ],
            'message': '请先登录 DeepSeek（手机号+验证码或微信扫码），登录完成后再次运行查询'
        }
    
    # 已登录，执行查询
    return {
        'url': 'https://chat.deepseek.com/',
        'needs_login': False,
        'steps': [
            {
                'action': 'navigate',
                'url': 'https://chat.deepseek.com/'
            },
            {
                'action': 'wait_for_selector',
                'selector': 'textarea[placeholder*="发送消息"], textarea[placeholder*="Message"], #chat-input, [contenteditable="true"]',
                'timeout': 10000,
                'description': '等待输入框加载'
            },
            {
                'action': 'click',
                'selector': 'button:has-text("深度思考"), button[class*="deep-thinking"], [class*="deep-thinking"]',
                'description': '启用深度思考模式（R1）',
                'optional': True  # 如果已经启用或找不到按钮，不报错
            },
            {
                'action': 'wait',
                'time_ms': 500,
                'description': '等待深度思考模式切换'
            },
            {
                'action': 'type',
                'selector': 'textarea[placeholder*="发送消息"], textarea[placeholder*="Message"], #chat-input, [contenteditable="true"]',
                'text': question,
                'description': '输入查询问题'
            },
            {
                'action': 'press',
                'key': 'Enter',
                'description': '发送消息'
            },
            {
                'action': 'wait',
                'time_ms': 3000,
                'description': '等待初始响应'
            },
            {
                'action': 'wait_for_completion',
                'description': '等待回答完成（检测停止按钮消失或内容稳定）',
                'max_wait_seconds': 60
            }
        ],
        'extract_selector': '.message-content, .chat-message:last-child, [class*="message"]:last-child, .ds-markdown',
        'keep_browser_open': True,
        'deep_thinking_enabled': True
    }


def generate_extraction_instructions() -> dict:
    """
    生成结果提取指令
    
    使用 copy + 页面提取方案获取 Markdown 内容
    """
    return {
        'extraction_method': 'copy_and_evaluate',
        'steps': [
            {
                'action': 'click',
                'selector': 'button[title*="复制"], button[class*="copy"], [class*="copy-button"], button:has-text("复制")',
                'description': '点击 copy 按钮复制 Markdown 内容',
                'optional': True
            },
            {
                'action': 'wait',
                'time_ms': 500,
                'description': '等待复制完成'
            },
            {
                'action': 'evaluate',
                'fn': '''() => {
                    // 提取所有消息内容的 Markdown 格式文本
                    const markdownElements = document.querySelectorAll('.ds-markdown, [class*="markdown"], [class*="message-content"]');
                    let result = '';
                    markdownElements.forEach(el => {
                        if (el.innerText && el.innerText.trim().length > 0) {
                            result += el.innerText + '\\n\\n';
                        }
                    });
                    return result.trim();
                }''',
                'description': '提取页面中的 Markdown 内容'
            }
        ],
        'fallback_methods': [
            {
                'name': 'screenshot',
                'description': '如果提取失败，直接截图返回'
            },
            {
                'name': 'llm_summarize',
                'description': '如果需要整理，调用 LLM 处理提取的内容'
            }
        ]
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': '缺少查询问题',
            'usage': 'python deepseek_query_helper.py "你的查询问题" [snapshot_json_file]'
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 获取问题
    question = sys.argv[1]
    
    # 处理 ds: 或 ds：前缀
    original_question = question
    if question.startswith("ds:") or question.startswith("ds："):
        # 移除前缀
        if question.startswith("ds:"):
            question = question[3:].strip()
        else:  # ds：
            question = question[3:].strip()
    
    # 检查是否有 snapshot 数据（用于登录状态检测）
    snapshot_data = None
    if len(sys.argv) >= 3:
        snapshot_file = sys.argv[2]
        try:
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                snapshot_data = json.load(f)
        except Exception as e:
            pass
    
    # 检测登录状态
    login_status = None
    if snapshot_data:
        login_status = check_login_status(snapshot_data)
    
    # 生成浏览器指令
    is_logged_in = login_status['is_logged_in'] if login_status else False
    browser_instructions = generate_browser_instructions(question, is_logged_in)
    
    # 生成结果提取指令
    extraction_instructions = generate_extraction_instructions()
    
    # 输出完整结果
    result = {
        'original_question': original_question,
        'processed_question': question,
        'has_ds_prefix': original_question.startswith("ds:") or original_question.startswith("ds："),
        'login_status': login_status,
        'browser_instructions': browser_instructions,
        'extraction_instructions': extraction_instructions,
        'note': '使用 copy + 页面提取方案获取 Markdown 内容，兼顾速度和质量'
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Code/URL Space Cleaner
自动检查并清除代码和 URL 中的多余空格，保留必要的空格。
"""

import re
import sys

class CodeURLCleaner:
    """代码和 URL 空格清理器"""
    
    def __init__(self):
        # URL 正则模式 - 匹配完整的 URL（包括中间可能有空格的情况）
        self.url_pattern = re.compile(
            r'(https?://)([^\s"\'>\)\]\}]+(?:\s+[^\s"\'>\)\]\}]+)*)',
            re.IGNORECASE
        )
        
        # 路径模式 - 匹配 Unix 路径
        self.path_pattern = re.compile(
            r'(/[a-zA-Z0-9_./\-@%]+)\s+(/[a-zA-Z0-9_./\-@%]+)'
        )
        
        # 命令多余空格模式 - 匹配命令中的多个连续空格（至少 2 个）
        self.cmd_space_pattern = re.compile(r'(?<! ) {2,}(?! )')
        
        # 通用空格清理 - URL 和路径中的空格
        self.url_space_pattern = re.compile(
            r'(https?://[^\s"\'>\)\]\}]+)\s+([^\s"\'>\)\]\}]+)'
        )
        
        # 代码块模式
        self.code_block_pattern = re.compile(
            r'```(\w*)\n(.*?)```',
            re.DOTALL | re.MULTILINE
        )
        
        # 内联代码模式
        self.inline_code_pattern = re.compile(r'`([^`]+)`')
    
    def clean_url(self, match):
        """清理 URL 中的空格"""
        protocol = match.group(1)
        rest = match.group(2).replace(' ', '')
        return protocol + rest
    
    def clean_path(self, match):
        """清理路径中的空格"""
        part1 = match.group(1).replace(' ', '')
        part2 = match.group(2).replace(' ', '')
        return part1 + part2
    
    def clean_code_block(self, match):
        """清理代码块中的多余空格"""
        lang = match.group(1)
        code = match.group(2)
        
        # 先清理代码块中的 URL 空格
        code = self.url_space_pattern.sub(self.clean_url, code)
        
        # 清理代码块
        cleaned_lines = []
        for line in code.split('\n'):
            # 保留行首缩进
            stripped = line.lstrip()
            if not stripped:
                cleaned_lines.append('')
                continue
            
            indent = line[:len(line) - len(stripped)]
            
            # 清理多余空格（但保留字符串内的空格）
            # 跳过注释行和字符串行
            if stripped.startswith('#') or stripped.startswith('//'):
                cleaned = stripped
            else:
                # 多个空格变一个（命令参数之间）
                cleaned = self.cmd_space_pattern.sub(' ', stripped)
            
            cleaned_lines.append(indent + cleaned)
        
        cleaned_code = '\n'.join(cleaned_lines)
        # 保留末尾换行
        return f'```{lang}\n{cleaned_code}\n```\n'
    
    def clean_inline_code(self, match):
        """清理内联代码中的空格"""
        code = match.group(1)
        # 清理 URL 和路径
        cleaned = self.url_space_pattern.sub(self.clean_url, code)
        cleaned = self.url_pattern.sub(self.clean_url, cleaned)
        cleaned = self.path_pattern.sub(self.clean_path, cleaned)
        # 保留内联代码后的空格（如果有）
        return f'`{cleaned}` '
    
    def clean(self, text):
        """
        清理文本中的多余空格
        
        Args:
            text: 输入文本
            
        Returns:
            清理后的文本
        """
        # 1. 先清理代码块（避免破坏代码结构）
        text = self.code_block_pattern.sub(self.clean_code_block, text)
        
        # 2. 清理内联代码（保留后面的空格）
        def clean_inline_wrapper(match):
            result = self.clean_inline_code(match)
            # 如果原文本中内联代码后面有空格，保留它
            return result.rstrip() + ' '
        
        text = self.inline_code_pattern.sub(clean_inline_wrapper, text)
        
        # 3. 清理 URL 中的空格（包括 URL 中间的空格）
        text = self.url_space_pattern.sub(self.clean_url, text)
        
        # 4. 清理普通文本中的 URL
        text = self.url_pattern.sub(self.clean_url, text)
        
        # 5. 清理路径
        text = self.path_pattern.sub(self.clean_path, text)
        
        # 6. 清理命令中的多个空格（保留单个空格）
        text = self.cmd_space_pattern.sub(' ', text)
        
        return text


def clean_text(text):
    """快捷函数"""
    cleaner = CodeURLCleaner()
    return cleaner.clean(text)


# Hook 注册函数
_hook_registered = False

def _auto_register_hook():
    """
    Auto-register as OpenClaw output filter hook (called on module load)
    自动注册为 OpenClaw 输出过滤钩子（模块加载时调用）
    
    English: Automatically called when skill is imported in OpenClaw.
    中文：在 OpenClaw 中导入技能时自动调用。
    """
    global _hook_registered
    
    if _hook_registered:
        return True
    
    try:
        # 尝试导入 OpenClaw API
        from openclaw import get_current_agent
        agent = get_current_agent()
        
        def clean_output(event, ctx):
            """Hook callback: clean agent output | Hook 回调：清理 agent 输出"""
            output = event.get('output', '')
            if output:
                return {'output': clean_text(output)}
            return event
        
        # 注册钩子
        agent.on('before_output', clean_output)
        _hook_registered = True
        
        return True
        
    except:
        # Not in OpenClaw environment, will auto-register when loaded
        return False

# Auto-register on module load | 模块加载时自动注册
_auto_register_hook()

def register_auto_hook():
    """
    Manually register hook (optional, for compatibility)
    手动注册钩子（可选，用于兼容）
    
    English: Usually not needed - hook auto-registers on import.
    中文：通常不需要 - Hook 在导入时自动注册。
    """
    global _hook_registered
    
    if _hook_registered:
        print('✅ Hook already active | Hook 已激活')
        return True
    
    return _auto_register_hook()

def is_hook_active():
    """
    Check if hook is registered
    检查 Hook 是否已注册
    
    Returns: True if hook is active, False otherwise
    返回：Hook 激活返回 True，否则返回 False
    """
    global _hook_registered
    
    # 如果已标记为激活，返回 True
    if _hook_registered:
        return True
    
    # 尝试检测是否在 OpenClaw 环境中
    try:
        from openclaw import get_current_agent
        # 如果能导入，说明在 OpenClaw 环境中，Hook 应该已注册
        return True
    except:
        # 不在 OpenClaw 环境中
        return False

# 测试
if __name__ == '__main__':
    test_cases = [
        # (描述，输入，期望输出)
        (
            "URL 中间有空格",
            "cd /tmp && git clone https://github.com/Johnserf-Seed /TikTokDownload.git",
            "cd /tmp && git clone https://github.com/Johnserf-Seed/TikTokDownload.git"
        ),
        (
            "命令多个空格",
            "pip3 install -r requirements.txt  --break-system-packages",
            "pip3 install -r requirements.txt --break-system-packages"
        ),
        (
            "抖音视频 URL 空格",
            "https://www.douyin.com/ video/123456",
            "https://www.douyin.com/video/123456"
        ),
        (
            "路径空格",
            "cd /Users/yitao/.openclaw /workspace",
            "cd /Users/yitao/.openclaw/workspace"
        ),
    ]
    
    cleaner = CodeURLCleaner()
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("Code/URL Space Cleaner 测试")
    print("=" * 60)
    
    for desc, input_text, expected in test_cases:
        result = cleaner.clean(input_text)
        if result == expected:
            print(f"\n✅ {desc}")
            passed += 1
        else:
            print(f"\n❌ {desc}")
            print(f"   输入：{input_text}")
            print(f"   输出：{result}")
            print(f"   期望：{expected}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    # 测试 Hook 功能
    print("\n" + "=" * 60)
    print("Hook 功能测试")
    print("=" * 60)
    print(f"Hook 状态：{'已激活' if is_hook_active() else '未激活'}")
    print(f"激活命令：python3 -c \"from cleaner import register_auto_hook; register_auto_hook()\"")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)

#!/usr/bin/env python3
"""
Apple Notes Writer - 完美格式写入Apple备忘录
支持HTML格式、自动转义、多文件夹管理
"""

import subprocess
import re
import html
from typing import Optional, List


class AppleNotesWriter:
    """Apple备忘录写入器"""
    
    # 支持的HTML标签（Apple Notes原生支持）
    SUPPORTED_TAGS = [
        'div', 'h1', 'h2', 'h3', 'p', 'br',
        'ul', 'ol', 'li',
        'b', 'strong', 'i', 'em', 'u'
    ]
    
    def __init__(self, account: str = "iCloud"):
        self.account = account
    
    def _escape_for_applescript(self, content: str) -> str:
        """
        转义内容以适配AppleScript
        关键转义规则：
        1. 反斜杠 → 双反斜杠 (必须最先处理)
        2. 双引号 → 反斜杠+双引号
        3. 换行 → 保留或转为<br>
        """
        # 先处理反斜杠（必须最先）
        content = content.replace('\\', '\\\\')
        # 再处理双引号
        content = content.replace('"', '\\"')
        return content
    
    def _validate_html(self, content: str) -> str:
        """验证并清理HTML内容"""
        # 确保有外层div包裹
        if not content.strip().startswith('<div'):
            content = f'<div>{content}</div>'
        
        # 确保所有标签闭合（简单检查）
        # 移除不支持的标签
        for tag in re.findall(r'</?(\w+)', content):
            if tag.lower() not in self.SUPPORTED_TAGS:
                # 移除不支持的标签
                content = re.sub(f'</?{tag}[^>]*>', '', content, flags=re.IGNORECASE)
        
        return content
    
    def _build_applescript(
        self, 
        title: str, 
        body: str, 
        folder: str = "Notes",
        update_existing: bool = False
    ) -> str:
        """构建AppleScript脚本"""
        
        script = f'''
tell application "Notes"
    activate
    set targetAccount to account "{self.account}"
    set targetFolder to folder "{folder}" of targetAccount
    
    try
        set noteTitle to "{self._escape_for_applescript(title)}"
        set noteBody to "{self._escape_for_applescript(body)}"
        
        {"-- 查找是否已存在同名笔记" if update_existing else ""}
        {"set existingNotes to every note in targetFolder whose name is noteTitle" if update_existing else ""}
        {"if length of existingNotes > 0 then" if update_existing else ""}
        {"    set targetNote to item 1 of existingNotes" if update_existing else ""}
        {"    set body of targetNote to noteBody" if update_existing else ""}
        {"else" if update_existing else ""}
        {"    " if update_existing else ""}set targetNote to make new note at targetFolder with properties {{name:noteTitle, body:noteBody}}
        {"end if" if update_existing else ""}
        
        return "SUCCESS: Note created/updated - " & name of targetNote
    on error errMsg
        return "ERROR: " & errMsg
    end try
end tell
'''
        return script
    
    def write(
        self, 
        title: str, 
        content: str, 
        folder: str = "Notes",
        update_existing: bool = False
    ) -> str:
        """
        写入备忘录
        
        Args:
            title: 笔记标题
            content: HTML格式内容
            folder: 目标文件夹（默认Notes）
            update_existing: 是否更新同名笔记
        
        Returns:
            操作结果消息
        """
        # 验证和清理HTML
        content = self._validate_html(content)
        
        # 构建并执行AppleScript
        script = self._build_applescript(title, content, folder, update_existing)
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"ERROR: {result.stderr}"
    
    def read(self, title: str, folder: str = "Notes") -> Optional[str]:
        """读取备忘录内容"""
        script = f'''
tell application "Notes"
    set targetFolder to folder "{folder}" of account "{self.account}"
    try
        set targetNote to first note in targetFolder whose name is "{self._escape_for_applescript(title)}"
        return body of targetNote
    on error
        return "NOT_FOUND"
    end try
end tell
'''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip() != "NOT_FOUND":
            return result.stdout.strip()
        return None
    
    def list_notes(self, folder: str = "Notes") -> List[str]:
        """列出文件夹中的所有笔记标题"""
        script = f'''
tell application "Notes"
    set targetFolder to folder "{folder}" of account "{self.account}"
    set noteNames to {{}}
    repeat with n in (every note in targetFolder)
        set end of noteNames to (name of n)
    end repeat
    return noteNames as string
end tell
'''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # AppleScript返回的是逗号分隔的字符串
            return [n.strip() for n in result.stdout.split(',') if n.strip()]
        return []
    
    def update_by_id(self, note_id: str, content: str) -> str:
        """通过ID更新笔记"""
        content = self._validate_html(content)
        
        script = f'''
tell application "Notes"
    try
        set targetNote to note id "{self._escape_for_applescript(note_id)}"
        set body of targetNote to "{self._escape_for_applescript(content)}"
        return "SUCCESS: Note updated - " & name of targetNote
    on error errMsg
        return "ERROR: " & errMsg
    end try
end tell
'''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else result.stderr
    
    def get_note_id(self, title: str, folder: str = "Notes") -> Optional[str]:
        """通过标题获取笔记ID"""
        script = f'''
tell application "Notes"
    set targetFolder to folder "{folder}" of account "{self.account}"
    try
        set targetNote to first note in targetFolder whose name is "{self._escape_for_applescript(title)}"
        return id of targetNote
    on error
        return "NOT_FOUND"
    end try
end tell
'''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip() != "NOT_FOUND":
            return result.stdout.strip()
        return None
    
    def verify_content(self, title: str, folder: str = "Notes") -> Optional[str]:
        """验证笔记内容（返回内容前200字符）"""
        content = self.read(title, folder)
        if content:
            return content[:200] + "..." if len(content) > 200 else content
        return None
    
    def create_folder(self, folder_name: str) -> str:
        """创建新文件夹"""
        script = f'''
tell application "Notes"
    set targetAccount to account "{self.account}"
    try
        make new folder at targetAccount with properties {{name:"{self._escape_for_applescript(folder_name)}"}}
        return "SUCCESS: Folder created - {folder_name}"
    on error errMsg
        return "ERROR: " & errMsg
    end try
end tell
'''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else result.stderr


def markdown_to_html(markdown_text: str) -> str:
    """
    简单Markdown转HTML（Apple Notes支持的基础格式）
    
    支持的转换：
    - # ## ### → h1 h2 h3
    - **text** → <b>text</b>
    - *text* → <i>text</i>
    - - item → <ul><li>item</li></ul>
    - 1. item → <ol><li>item</li></ol>
    """
    html_content = markdown_text
    
    # 转义HTML特殊字符
    html_content = html.escape(html_content)
    
    # 标题
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # 粗体和斜体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<i>\1</i>', html_content)
    
    # 无序列表
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.+</li>\n?)+', r'<ul>\g<0></ul>', html_content)
    
    # 有序列表
    html_content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # 换行
    html_content = html_content.replace('\n', '<br>')
    
    # 包裹在div中
    return f'<div>{html_content}</div>'


# CLI接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Apple Notes Writer')
    parser.add_argument('action', choices=['write', 'read', 'list', 'create-folder'])
    parser.add_argument('--title', '-t', help='Note title')
    parser.add_argument('--content', '-c', help='Note content (HTML)')
    parser.add_argument('--file', '-f', help='Read content from file')
    parser.add_argument('--folder', default='Notes', help='Target folder')
    parser.add_argument('--update', action='store_true', help='Update if exists')
    parser.add_argument('--markdown', '-m', action='store_true', help='Content is markdown')
    
    args = parser.parse_args()
    
    writer = AppleNotesWriter()
    
    if args.action == 'write':
        content = args.content
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if args.markdown and content:
            content = markdown_to_html(content)
        
        result = writer.write(args.title, content, args.folder, args.update)
        print(result)
    
    elif args.action == 'read':
        result = writer.read(args.title, args.folder)
        print(result if result else "Note not found")
    
    elif args.action == 'list':
        notes = writer.list_notes(args.folder)
        for note in notes:
            print(f"- {note}")
    
    elif args.action == 'create-folder':
        result = writer.create_folder(args.title)
        print(result)

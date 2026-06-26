"""
Coder Helper - 需求文档生成器

根据自然语言需求生成 requests.txt 并打开编辑器
"""

import os
import subprocess
from pathlib import Path


# 编辑器路径（可扩展）
EDITORS = [
    ("cursor", "/mnt/c/Program Files/cursor2.38/resources/app/bin/cursor"),
    ("code", "code"),  # VSCode
    ("notepad++", "C:/Program Files/Notepad++/notepad++.exe"),
    ("vim", "vim"),
]


def detect_editor():
    """检测可用的编辑器"""
    for name, path in EDITORS:
        if os.path.exists(path) or name in os.environ.get("PATH", ""):
            return name, path
    return "nano", "nano"  # 最保守 fallback


def generate_requests_file(project_path: str, task_description: str) -> str:
    """生成需求文档"""
    
    content = f"""# 任务需求

## 原始需求
{task_description}

## 待完成
- [ ] 实现功能
- [ ] 编写测试
- [ ] 完善文档

## 备注
"""
    
    file_path = Path(project_path) / "requests.txt"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


def open_editor(file_path: str):
    """打开编辑器"""
    editor_name, editor_path = detect_editor()
    
    try:
        # 尝试直接调用
        subprocess.Popen([editor_path, file_path], shell=True)
        print(f"✅ 已用 {editor_name} 打开")
    except Exception as e:
        # fallback 到系统默认
        try:
            os.startfile(file_path)  # Windows
        except:
            subprocess.Popen(["xdg-open", file_path])  # Linux


def run(task: str, project_path: str = ".") -> str:
    """主函数"""
    
    # 生成需求文件
    file_path = generate_requests_file(project_path, task)
    
    # 打开编辑器
    open_editor(file_path)
    
    return f"""📝 需求文档已生成
📁 路径: {file_path}

请将内容复制到 AI 编程助手（Cursor/VSCode AI 等）"""


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = "写一个 Hello World 脚本"
    
    print(run(task))

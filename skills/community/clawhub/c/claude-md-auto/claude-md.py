# CLAUDE.md Auto-Discovery Skill

自动发现并加载项目根目录的 CLAUDE.md 文件。

## 功能
- 自动查找 `./CLAUDE.md` 和 `./ CLAUDE.md`
- 支持 @include 指令
- 最大 40000 字符限制
- 逆序加载（后面的文件优先级更高）

## 调用方式
```bash
claude-md-discover [--cwd /path/to/dir]
```

返回发现的 CLAUDE.md 内容，用于注入到系统上下文。
"""
import os
import re
from pathlib import Path

MAX_CHARS = 40000

def discover_claude_md_files(cwd=None):
    """从当前目录向上查找所有 CLAUDE.md 文件"""
    if cwd is None:
        cwd = os.getcwd()
    
    paths_to_check = []
    current = Path(cwd).resolve()
    
    # 向上查找，最多 4 层
    for _ in range(4):
        paths_to_check.append(current / "CLAUDE.md")
        paths_to_check.append(current / " CLAUDE.md")  # 注意有空格
        if current.parent == current:
            break
        current = current.parent
    
    # 去重并保留存在的文件
    found = []
    seen = set()
    for p in paths_to_check:
        if str(p) not in seen and p.exists():
            seen.add(str(p))
            found.append(p)
    
    return found

def load_claude_md_content(cwd=None):
    """加载所有 CLAUDE.md 文件内容"""
    files = discover_claude_md_files(cwd)
    if not files:
        return None
    
    # 逆序加载（后面的优先级更高）
    contents = []
    for f in reversed(files):
        try:
            content = f.read_text(encoding='utf-8')
            contents.append(f"# {f.name}\n\n{content}")
        except Exception:
            pass
    
    if not contents:
        return None
    
    combined = "\n\n---\n\n".join(contents)
    
    # 截断到最大字符数
    if len(combined) > MAX_CHARS:
        combined = combined[:MAX_CHARS] + "\n\n... (truncated)"
    
    return combined

if __name__ == "__main__":
    import sys
    result = load_claude_md_content(sys.argv[1] if len(sys.argv) > 1 else None)
    if result:
        print(result)
    else:
        print("No CLAUDE.md files found")
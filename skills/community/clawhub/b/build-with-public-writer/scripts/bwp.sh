#!/bin/bash
# Build with Public (bwp) - Simplified helper for technical content creation
# Usage: bwp <action> [options]

set -e

PROJECT_ROOT="${BWP_PROJECT_ROOT:-/home/node/cwr}"
ACTION="${1:-help}"

show_help() {
    echo "Build with Public (bwp) - Technical Content Creation"
    echo ""
    echo "Usage:"
    echo "  bwp init                   # Initialize project with README.md"
    echo "  bwp article <title>        # Create new article"
    echo "  bwp course <name>          # Create new course outline"
    echo "  bwp theory <name>          # Create new theory/framework"
    echo "  bwp persona <name>         # Create new writing persona"
    echo "  bwp list                   # List all content"
    echo "  bwp commit [message]       # Commit changes to Git"
    echo "  bwp link <file>            # Generate shareable link"
    echo "  bwp status                 # Show project status"
    echo ""
    echo "Examples:"
    echo "  bwp init"
    echo "  bwp article \"AI Trends 2026\""
    echo "  bwp course \"OpenClaw Bootcamp\""
    echo "  bwp theory \"Writing Framework\""
    echo "  bwp persona \"Tech Expert\""
    echo "  bwp commit \"Add new article\""
    echo "  bwp link articles/bwp-2026-03-13-ai-trends-v1.md"
}

# Get today's date
get_date() {
    date +"%Y-%m-%d"
}

# Convert title to slug
slugify() {
    local input="$1"
    # 将输入转为小写，空格替换为横线
    local slug=$(echo "$input" | awk '{print tolower($0)}' | sed 's/ /-/g')
    # 移除特殊字符，保留字母数字
    local ascii_slug=$(echo "$slug" | sed 's/[^a-z0-9\-]//g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
    # 如果 ASCII 部分为空（全是中文等情况），使用默认标识
    if [ -z "$ascii_slug" ] || [ "$ascii_slug" = "-" ]; then
        ascii_slug="post"
    fi
    echo "$ascii_slug"
}

create_article() {
    local title="${1:-Untitled}"
    local slug=$(slugify "$title")
    local filename="bwp-$(get_date)-${slug}-v1.md"
    local filepath="$PROJECT_ROOT/articles/$filename"
    
    cat > "$filepath" << EOF
---
title: $title
date: $(get_date)
version: v1
---

# $title

## Introduction

Write your introduction here...

## Main Content

### Section 1

Content...

### Section 2

Content...

## Conclusion

Summary...

---

*Created with bwp on $(get_date)*
EOF
    
    echo "✅ Created: articles/$filename"
    echo "📝 Edit: $filepath"
}

create_course() {
    local name="${1:-New Course}"
    local slug=$(slugify "$name")
    local dir="$PROJECT_ROOT/courses/bwp-$slug"
    local filename="bwp-$(get_date)-${slug}-syllabus-v1.md"
    
    mkdir -p "$dir"
    
    cat > "$dir/syllabus-v1.md" << EOF
---
course: $name
date: $(get_date)
version: v1
---

# $name - Course Syllabus

## Overview

Brief description of the course...

## Learning Objectives

- Objective 1
- Objective 2
- Objective 3

## Course Outline

### Week 1: Foundation
- Topic 1
- Topic 2

### Week 2: Practice
- Topic 3
- Topic 4

### Week 3: Advanced
- Topic 5
- Topic 6

## Prerequisites

- Requirement 1
- Requirement 2

## Resources

- Resource 1
- Resource 2

---

*Created with bwp on $(get_date)*
EOF
    
    echo "✅ Created: courses/bwp-$slug/syllabus-v1.md"
    echo "📝 Edit: $dir/syllabus-v1.md"
}

create_theory() {
    local name="${1:-Framework}"
    local slug=$(slugify "$name")
    local filename="bwp-${slug}-v1.md"
    local filepath="$PROJECT_ROOT/theory/$filename"
    
    cat > "$filepath" << EOF
---
title: $name
date: $(get_date)
version: v1
---

# $name

## Core Principles

1. **Principle 1**: Description...
2. **Principle 2**: Description...
3. **Principle 3**: Description...

## Framework

### Step 1: Analysis

How to analyze...

### Step 2: Design

How to design...

### Step 3: Implementation

How to implement...

## Examples

### Example 1

Description...

### Example 2

Description...

## Best Practices

- Practice 1
- Practice 2
- Practice 3

---

*Created with bwp on $(get_date)*
EOF
    
    echo "✅ Created: theory/$filename"
    echo "📝 Edit: $filepath"
}

create_persona() {
    local name="${1:-Writer}"
    local slug=$(slugify "$name")
    local filename="bwp-${slug}-style-v1.md"
    local filepath="$PROJECT_ROOT/persona/$filename"
    
    cat > "$filepath" << EOF
---
persona: $name
date: $(get_date)
version: v1
---

# $name - Writing Style

## Voice

### Tone

- Professional yet approachable
- Direct and clear
- Occasional humor

### Language

- Simple over complex
- Specific over vague
- Active over passive

## Characteristics

### Strengths

1. **Strength 1**: Description...
2. **Strength 2**: Description...

### Weaknesses to Avoid

1. **Weakness 1**: Description...
2. **Weakness 2**: Description...

## Writing Guidelines

### Do's

- ✅ Guideline 1
- ✅ Guideline 2

### Don'ts

- ❌ Guideline 1
- ❌ Guideline 2

## Sample Phrases

### Openings

- "Direct conclusion..."
- "Here's a pitfall to watch..."

### Transitions

- "Essentially..."
- "From another angle..."

### Closings

- "Remember this principle..."
- "In practice..."

---

*Created with bwp on $(get_date)*
EOF
    
    echo "✅ Created: persona/$filename"
    echo "📝 Edit: $filepath"
}

init_project() {
    echo "🚀 Initializing Build with Public project..."
    echo ""
    
    # Extract project name from PROJECT_ROOT
    PROJECT_NAME=$(basename "$PROJECT_ROOT")
    
    # Create directory structure
    mkdir -p "$PROJECT_ROOT"/{articles,courses,theory,persona,images}
    
    # Create README.md
    cat > "$PROJECT_ROOT/README.md" << 'READMEEOF'
# codewithriver - Build with Public

技术内容创作与分享平台

---

## 📁 目录结构

```
codewithriver/
├── articles/      # 📄 技术文章和博客
├── courses/       # 📚 课程大纲和教程
├── theory/        # 📖 理论框架和方法论
├── persona/       # 🎭 写作人设和风格
├── images/        # 🖼️ 文章图片
├── server.py      # 🌐 Web 服务器
├── .env           # ⚙️ 环境配置
└── README.md      # 📋 本文件
```

---

## 📂 各目录详细说明

### 📄 articles/
**用途**：存放所有技术文章、博客、短文

**命名规范**：
```
bwp-YYYY-MM-DD-{topic}-v{version}.md
```

**示例**：
- `bwp-2026-03-13-ai-trends-v1.md`
- `bwp-2026-03-13-vibe-coding-v1.1.md`

**版本规则**：
- `v1`, `v1.1`, `v1.2`... - 小迭代
- `v2`, `v3`... - 大改版
- `-wechat`, `-xiaohongshu` - 平台适配版

---

### 📚 courses/
**用途**：存放课程大纲、教程、训练营资料

**结构**：
```
courses/
├── bwp-course-name/
│   ├── bwp-YYYY-MM-DD-course-name-syllabus-v1.md
│   └── ...
└── ...
```

**示例**：
- `courses/bwp-openclaw-bootcamp/`
- `courses/bwp-python-fundamentals/`

---

### 📖 theory/
**用途**：存放方法论、框架、最佳实践指南

**命名规范**：
```
bwp-{framework-name}-v{version}.md
```

**示例**：
- `bwp-writing-framework-v1.md`
- `bwp-content-strategy-v1.md`

**内容类型**：
- 写作方法论
- 技术框架
- 工作流程指南

---

### 🎭 persona/
**用途**：存放写作人设、风格定义、语言特征

**命名规范**：
```
bwp-{persona-name}-style-v{version}.md
```

**示例**：
- `bwp-tech-expert-style-v1.md`
- `bwp-mentor-voice-v1.md`

**内容类型**：
- 人设定义
- 语言风格指南
- 常用短语/句式
- 写作规范

---

### 🖼️ images/
**用途**：存放文章配图、图表、截图

**使用方式**：
- 在 Markdown 中引用：`![描述](images/filename.png)`
- 建议命名与对应文章相关

---

## 🚀 快速开始

### 创建新文章
```bash
bwp article "文章标题"
```

### 创建课程大纲
```bash
bwp course "课程名称"
```

### 创建理论框架
```bash
bwp theory "框架名称"
```

### 定义写作风格
```bash
bwp persona "人设名称"
```

### 查看项目状态
```bash
bwp status
```

### 生成分享链接
```bash
bwp link articles/bwp-2026-03-13-xxx-v1.md
```

---

## ⚙️ 环境配置

`.env` 文件配置：

```bash
# 服务器端口
PORT=12000

# 自定义域名（用于生成分享链接）
CUSTOM_DOMAIN=your-domain.com

# 访问认证
AUTH_USERNAME=user
AUTH_PASSWORD=your_password
```

---

## 🔧 常用命令

| 命令 | 说明 |
|:-----|:-----|
| `bwp list` | 列出所有内容 |
| `bwp commit "消息"` | 提交到 Git |
| `bwp link <文件>` | 生成分享链接 |
| `bwp status` | 查看项目状态 |

---

## 📝 工作流程

1. **创建内容** → 使用 `bwp` 命令创建文件
2. **编辑完善** → 使用你喜欢的编辑器修改
3. **提交保存** → `bwp commit "描述"`
4. **分享链接** → `bwp link <文件路径>`

---

## 🔒 安全说明

- 所有内容默认保存到 `$PROJECT_ROOT`
- Git 版本控制自动记录所有变更
- 通过 Web 服务器可安全分享内容

---

*Build with Public - 简化创作，专注内容 🚀*
READMEEOF
    
    # Replace hardcoded project name with actual project name
    sed -i "s/codewithriver/$(basename "$PROJECT_ROOT")/g" "$PROJECT_ROOT/README.md"
    sed -i "s|$PROJECT_ROOT|$PROJECT_ROOT|g" "$PROJECT_ROOT/README.md"
    
    echo "✅ Directory structure created"
    echo "✅ README.md created"
    
    # Create .env file
    cat > "$PROJECT_ROOT/.env" << 'ENVEOF'
# Build with Public - Environment Configuration

# Server port
PORT=12000

# Custom domain (optional, for generating shareable links)
# CUSTOM_DOMAIN=your-domain.com

# Authentication
AUTH_USERNAME=user
AUTH_PASSWORD=changeme
ENVEOF
    
    # Create server.py with new features
    cat > "$PROJECT_ROOT/server.py" << 'SERVERPYEOF'
#!/usr/bin/env python3
"""
Build with Public - Simple HTTP Server
Features: Basic Auth, Markdown rendering, Directory listing, Plain text/Preview modes
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, urlparse, parse_qs

CONFIG = {'PORT': 12000, 'AUTH_USERNAME': 'user', 'AUTH_PASSWORD': 'changeme'}

if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                CONFIG[key] = value.strip().strip('"').strip("'")

PORT = int(CONFIG.get('PORT', 12000))
AUTH_USERNAME = CONFIG.get('AUTH_USERNAME', 'user')
AUTH_PASSWORD = CONFIG.get('AUTH_PASSWORD', 'changeme')

class AuthHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Build with Public"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            self.do_AUTHHEAD()
            return
        import base64
        try:
            auth_type, auth_string = auth_header.split(' ', 1)
            decoded = base64.b64decode(auth_string).decode('utf-8')
            username, password = decoded.split(':', 1)
            if username != AUTH_USERNAME or password != AUTH_PASSWORD:
                self.do_AUTHHEAD()
                return
        except Exception:
            self.do_AUTHHEAD()
            return
        
        # Parse URL to separate path from query string
        parsed_url = urlparse(self.path)
        path = unquote(parsed_url.path[1:]) if parsed_url.path[1:] else ''
        safe_path = os.path.normpath(path) if path else '.'
        if safe_path.startswith('..'):
            self.send_error(403, "Forbidden")
            return
        
        full_path = os.path.join(os.getcwd(), safe_path)
        
        if os.path.isdir(full_path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            files = os.listdir(full_path)
            
            # Build directory listing with GitHub-style
            dir_name = safe_path if safe_path != '.' else os.path.basename(os.getcwd())
            html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{dir_name}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.6;color:#24292f;max-width:900px;margin:40px auto;padding:0 20px;background:#fff}}
h1{{font-size:24px;font-weight:600;border-bottom:1px solid #d0d7de;padding-bottom:16px;margin-bottom:16px}}
.file-list{{list-style:none;padding:0;margin:0}}
.file-list li{{border-bottom:1px solid #eaecef;padding:8px 0;display:flex;align-items:center}}
.file-list li:hover{{background:#f6f8fa}}
.file-list a{{color:#0969da;text-decoration:none;display:flex;align-items:center;width:100%}}
.file-list a:hover{{text-decoration:underline}}
.icon{{width:20px;height:20px;margin-right:12px;display:inline-flex;align-items:center;justify-content:center}}
.folder{{color:#54aeff}}
.file{{color:#656d76}}
.path{{color:#656d76;font-size:14px;margin-bottom:16px}}
.path a{{color:#0969da;text-decoration:none}}
.path a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<div class="path"><a href="/">{os.path.basename(os.getcwd())}</a>{''.join(f' / <a href="/{"/".join(safe_path.split("/")[:i+1])}">{p}</a>' for i, p in enumerate(safe_path.split('/')) if p and safe_path != '.')}</div>
<h1>📁 {dir_name}</h1>
<ul class="file-list">
'''
            # Add parent directory link if not at root
            if safe_path != '.':
                parent = '/'.join(safe_path.split('/')[:-1]) if '/' in safe_path else '/'
                html += f'<li><a href="{parent if parent != "/" else "/"}"><span class="icon folder">📁</span>..</a></li>'
            
            # Sort: directories first, then files
            dirs = [f for f in files if os.path.isdir(os.path.join(full_path, f))]
            files_only = [f for f in files if not os.path.isdir(os.path.join(full_path, f))]
            
            for f in sorted(dirs):
                f_path = os.path.join(safe_path, f) if safe_path != '.' else f
                html += f'<li><a href="/{f_path}"><span class="icon folder">📁</span>{f}</a></li>'
            for f in sorted(files_only):
                f_path = os.path.join(safe_path, f) if safe_path != '.' else f
                html += f'<li><a href="/{f_path}"><span class="icon file">📄</span>{f}</a></li>'
            
            html += '</ul></body></html>'
            self.wfile.write(html.encode('utf-8'))
            return
        
        if not os.path.exists(full_path):
            self.send_error(404, "File not found")
            return
        
        # Parse query string to check for preview mode
        query_params = parse_qs(parsed_url.query)
        preview_mode = query_params.get('preview', [''])[0]
        
        self.send_response(200)
        if full_path.endswith('.md'):
            if preview_mode == 'html':
                # HTML preview mode
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                import re
                html = content
                # Code blocks (```...```) - protect them first
                code_blocks = []
                def save_code_block(m):
                    code_blocks.append(f'<pre><code>{m.group(2)}</code></pre>')
                    return f'\x00CODEBLOCK{len(code_blocks)-1}\x00'
                html = re.sub(r'```(\w+)?\n(.*?)```', save_code_block, html, flags=re.DOTALL)
                # Headers
                html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
                html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
                html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
                # Bold (**text**) - must come before italic
                html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html, flags=re.DOTALL)
                # Italic (*text* or _text_) - single asterisk not followed by another
                html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html)
                html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
                # Inline code (`code`)
                html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
                # Links [text](url)
                html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
                # Images ![alt](url)
                html = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1">', html)
                # Blockquote (> text)
                html = re.sub(r'^\> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
                # Horizontal rule
                html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
                # Lists (- item or * item)
                html = re.sub(r'(?m)^- (.+)$', r'<li>\1</li>', html)
                html = re.sub(r'(<li>.+</li>\n?)+', r'<ul>\g<0></ul>', html)
                # Tables
                def parse_table(match):
                    rows = match.group(0).strip().split('\n')
                    if len(rows) < 2:
                        return match.group(0)
                    separator = rows[1]
                    if not re.match(r'^[\|\-\:\s]+$', separator):
                        return match.group(0)
                    html_table = '<table>'
                    headers = [c.strip() for c in rows[0].split('|')[1:-1]]
                    html_table += '<thead><tr>'
                    for h in headers:
                        html_table += f'<th>{h}</th>'
                    html_table += '</tr></thead><tbody>'
                    for row in rows[2:]:
                        if row.strip():
                            cells = [c.strip() for c in row.split('|')[1:-1]]
                            html_table += '<tr>'
                            for c in cells:
                                html_table += f'<td>{c}</td>'
                            html_table += '</tr>'
                    html_table += '</tbody></table>'
                    return html_table
                html = re.sub(r'(?:^\|.+\|\n?)+', parse_table, html, flags=re.MULTILINE)
                # Restore code blocks
                for i, block in enumerate(code_blocks):
                    html = html.replace(f'\x00CODEBLOCK{i}\x00', block)
                # Line breaks for paragraphs
                html = re.sub(r'\n\n+', '</p><p>', html)
                html = '<p>' + html + '</p>'
                html = re.sub(r'<p>(<h[123].*?>)', r'\1', html)
                html = re.sub(r'(</h[123]>)', r'\1</p><p>', html)
                html = re.sub(r'<p>(<ul>)', r'\1', html)
                html = re.sub(r'(</ul>)', r'\1</p><p>', html)
                html = re.sub(r'<p>(<blockquote>)', r'\1', html)
                html = re.sub(r'(</blockquote>)', r'\1</p><p>', html)
                html = re.sub(r'<p>(<hr>)', r'\1', html)
                html = re.sub(r'(<hr>)', r'\1</p><p>', html)
                html = re.sub(r'<p></p>', '', html)
                html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.6;color:#24292f;max-width:900px;margin:40px auto;padding:0 20px;background:#fff}}h1{{border-bottom:2px solid #eaecef;padding-bottom:10px;margin-top:0}}h2{{border-bottom:1px solid #eaecef;padding-bottom:8px;margin-top:30px}}h3{{margin-top:25px}}code{{background:#f6f8fa;padding:2px 6px;border-radius:3px;font-family:SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;font-size:85%}}pre{{background:#f6f8fa;padding:16px;border-radius:6px;overflow-x:auto}}pre code{{background:none;padding:0}}a{{color:#0969da;text-decoration:none}}a:hover{{text-decoration:underline}}blockquote{{border-left:4px solid #d0d7de;padding-left:16px;margin-left:0;color:#656d76}}table{{border-collapse:collapse;width:100%;margin:16px 0;font-size:14px}}th,td{{border:1px solid #d0d7de;padding:8px 12px;text-align:left}}th{{background:#f6f8fa;font-weight:600}}tr:nth-child(even){{background:#f6f8fa}}thead{{border-bottom:2px solid #d0d7de}}ul,ol{{padding-left:24px}}img{{max-width:100%;height:auto}}hr{{border:none;border-top:1px solid #d0d7de;margin:24px 0}}strong{{font-weight:700;color:#1f2328}}em{{font-style:italic}}ul{{margin:16px 0}}li{{margin:4px 0}}</style></head><body>{html}</body></html>'
                self.wfile.write(html.encode('utf-8'))
            else:
                # Default: plain text mode (original markdown)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                with open(full_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
        else:
            import mimetypes
            content_type, _ = mimetypes.guess_type(full_path)
            self.send_header('Content-type', content_type or 'application/octet-stream')
            self.end_headers()
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
    
    def log_message(self, format, *args):
        pass

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('', PORT), AuthHandler)
    print(f"Server running at http://localhost:{PORT}")
    print(f"Username: {AUTH_USERNAME}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)

if __name__ == '__main__':
    main()
SERVERPYEOF
    
    chmod +x "$PROJECT_ROOT/server.py"
    echo "✅ .env created"
    echo "✅ server.py created"
    echo ""
    echo "📁 Project structure:"
    echo "  articles/  - Technical articles and blog posts"
    echo "  courses/   - Course outlines and tutorials"
    echo "  theory/    - Frameworks and methodologies"
    echo "  persona/   - Writing personas and styles"
    echo "  images/    - Article images and diagrams"
    echo ""
    echo "Next steps:"
    echo "  1. Edit $PROJECT_ROOT/.env to configure your settings"
    echo "  2. Run 'bwp article \"Your First Article\"' to create content"
    echo "  3. Start server: cd $PROJECT_ROOT && python server.py"
}

list_content() {
    echo "📁 Content in cwr:"
    echo ""
    
    local article_count=$(ls $PROJECT_ROOT/articles/*.md 2>/dev/null | wc -l)
    echo "📄 Articles ($article_count):"
    if [ $article_count -gt 0 ]; then
        ls $PROJECT_ROOT/articles/*.md 2>/dev/null | xargs -n1 basename | head -10
    else
        echo "  (empty)"
    fi
    echo ""
    
    local course_count=$(ls -d $PROJECT_ROOT/courses/*/ 2>/dev/null | wc -l)
    echo "📚 Courses ($course_count):"
    if [ $course_count -gt 0 ]; then
        ls -d $PROJECT_ROOT/courses/*/ 2>/dev/null | xargs -n1 basename | head -10
    else
        echo "  (empty)"
    fi
    echo ""
    
    local theory_count=$(ls $PROJECT_ROOT/theory/*.md 2>/dev/null | wc -l)
    echo "📖 Theory ($theory_count):"
    if [ $theory_count -gt 0 ]; then
        ls $PROJECT_ROOT/theory/*.md 2>/dev/null | xargs -n1 basename | head -10
    else
        echo "  (empty)"
    fi
    echo ""
    
    local persona_count=$(ls $PROJECT_ROOT/persona/*.md 2>/dev/null | wc -l)
    echo "🎭 Persona ($persona_count):"
    if [ $persona_count -gt 0 ]; then
        ls $PROJECT_ROOT/persona/*.md 2>/dev/null | xargs -n1 basename | head -10
    else
        echo "  (empty)"
    fi
}

git_commit() {
    cd "$PROJECT_ROOT"
    
    local message="${1:-Update content}"
    
    git add -A
    
    if ! git diff --cached --quiet; then
        git commit -m "content: $message ($(get_date))"
        echo "✅ Committed: $message"
    else
        echo "ℹ️  No changes to commit"
    fi
}

generate_link() {
    local file="${1:-}"
    
    if [ -z "$file" ]; then
        echo "Usage: bwp link <filepath>"
        echo "Example: bwp link articles/bwp-2026-03-13-ai-trends-v1.md"
        return 1
    fi
    
    # Read server config from .env
    local port=$(grep PORT "$PROJECT_ROOT/.env" 2>/dev/null | cut -d= -f2 | tr -d '"' || echo "12000")
    local custom_domain=$(grep CUSTOM_DOMAIN "$PROJECT_ROOT/.env" 2>/dev/null | cut -d= -f2 | tr -d '"')
    
    # Use CUSTOM_DOMAIN if set, otherwise fallback to localhost
    local hostname="${custom_domain:-localhost}"
    
    # Output only the clickable link
    echo "http://${hostname}:${port}/${file}"
}

show_status() {
    cd "$PROJECT_ROOT"
    
    # Extract project name from PROJECT_ROOT
    PROJECT_NAME=$(basename "$PROJECT_ROOT")
    
    echo "📊 Build with Public - Status"
    echo ""
    echo "📁 Project: $PROJECT_NAME"
    echo "📍 Location: $PROJECT_ROOT"
    echo ""
    
    echo "📝 Recent commits:"
    git log --oneline -5 2>/dev/null || echo "  No commits yet"
    echo ""
    
    echo "📊 Content stats:"
    echo "  Articles: $(ls articles/*.md 2>/dev/null | wc -l) files"
    echo "  Courses: $(ls courses/ 2>/dev/null | wc -l) directories"
    echo "  Theory: $(ls theory/*.md 2>/dev/null | wc -l) files"
    echo "  Persona: $(ls persona/*.md 2>/dev/null | wc -l) files"
    echo ""
    
    # Server status
    if pgrep -f "server.py" > /dev/null; then
        echo "🟢 Server: Running"
    else
        echo "🔴 Server: Not running"
        echo "   Start with: cd $PROJECT_ROOT && python server.py"
    fi
}

# Main
case "$ACTION" in
    init|i)
        init_project
        ;;
    article|a)
        create_article "${2:-New Article}"
        ;;
    course|c)
        create_course "${2:-New Course}"
        ;;
    theory|t)
        create_theory "${2:-New Framework}"
        ;;
    persona|p)
        create_persona "${2:-New Persona}"
        ;;
    list|ls)
        list_content
        ;;
    commit|git)
        git_commit "${2:-Update content}"
        ;;
    link|url)
        generate_link "$2"
        ;;
    status|s)
        show_status
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac

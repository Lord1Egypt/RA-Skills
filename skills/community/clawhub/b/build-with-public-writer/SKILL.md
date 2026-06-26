---
name: build-with-public-writer
description: Use "bwp" command to create technical content for codewithriver. Supports articles, courses, theory, persona with version management and link sharing
---

# Build with Public (bwp) - 技术内容创作系统

## 快速开始

**使用 bwp 命令**:

有两种方式使用 bwp：

**选项1：直接使用完整路径**（推荐，无需修改配置）
```bash
/home/claw/.openclaw/workspace/skills/build-with-public-writer/scripts/bwp.sh help
```

**选项2：手动添加 alias**（可选）
```bash
# 如果你希望使用简短的 bwp 命令，可以手动添加 alias 到 ~/.bashrc
# ⚠️ 注意：这会修改你的 shell 配置文件，请审查后再执行

echo 'alias bwp="/home/claw/.openclaw/workspace/skills/build-with-public-writer/scripts/bwp.sh"' >> ~/.bashrc
source ~/.bashrc
```

**查看帮助**:
```bash
bwp help
```

---

## 核心命令

### 场景0: 初始化项目 (必做)

```bash
bwp init
```

**输出**:
```
🚀 Initializing Build with Public project...

✅ Directory structure created
✅ README.md created
✅ .env created
✅ server.py created

📁 Project structure:
  articles/  - Technical articles and blog posts
  courses/   - Course outlines and tutorials
  theory/    - Frameworks and methodologies
  persona/   - Writing personas and styles
  images/    - Article images and diagrams

Next steps:
  1. Edit /home/claw/codewithriver/.env to configure your settings
  2. Run 'bwp article "Your First Article"' to create content
  3. Start server: cd /home/claw/codewithriver && python server.py
```

**说明**:
- 创建完整的目录结构
- 生成 README.md 说明文档
- 自动生成 .env 配置文件（包含端口、认证信息）
- 自动生成 server.py Web 服务器（支持 Markdown 渲染和 Basic Auth）
- 只需执行一次，或在目录缺失时执行

---

### 场景1: 写文章

```bash
bwp article "AI 趋势 2026"
```

**输出**:
```
✅ Created: articles/bwp-2026-03-13-ai-trends-2026-v1.md
📝 Edit: /home/claw/codewithriver/articles/bwp-2026-03-13-ai-trends-2026-v1.md
```

**自动生成的模板包含**:
- Frontmatter (title, date, version)
- Introduction 章节
- Main Content 章节
- Conclusion 章节

---

### 场景2: 创建课程大纲

```bash
bwp course "OpenClaw 技能训练营"
```

**输出**:
```
✅ Created: courses/openclaw-bootcamp/syllabus-v1.md
📝 Edit: /home/claw/codewithriver/courses/openclaw-bootcamp/syllabus-v1.md
```

**自动生成的模板包含**:
- 课程概述
- 学习目标
- 4周课程大纲
- 先修要求
- 学习资源

---

### 场景3: 创建理论框架

```bash
bwp theory "写作框架"
```

创建 `/home/claw/codewithriver/theory/writing-framework-v1.md`

---

### 场景4: 定义写作风格

```bash
bwp persona "技术专家"
```

创建 `/home/claw/codewithriver/persona/tech-expert-style-v1.md`

---

## 其他命令

### 列出所有内容

```bash
bwp list
```

输出示例:
```
📁 Content in codewithriver:

📄 Articles (25):
  2026-03-13-ai-trends-v1.md
  2026-03-12-vibe-coding-v1.md
  ...

📚 Courses (3):
  openclaw-bootcamp
  openclaw-masterclass
  ...

📖 Theory (5):
  writing-framework-v1.md
  ...

🎭 Persona (2):
  tech-expert-style-v1.md
  ...
```

---

### Git 提交

```bash
bwp commit "添加 AI 趋势文章"
```

自动执行:
```bash
git add -A
git commit -m "content: 添加 AI 趋势文章 (2026-03-13)"
```

---

### 生成分享链接

```bash
bwp link articles/2026-03-13-ai-trends-v1.md
```

输出:
```
🔗 Shareable Link:
   http://localhost:12000/articles/2026-03-13-ai-trends-v1.md

👤 Access credentials configured in .env
   (Check /home/claw/codewithriver/.env for AUTH_USERNAME and AUTH_PASSWORD)

```

---

### 查看项目状态

```bash
bwp status
```

输出:
```
📊 Build with Public - Status

📁 Project: codewithriver
📍 Location: /home/claw/codewithriver

📝 Recent commits:
  abc1234 content: Add new article (2026-03-13)
  def5678 content: Update course outline (2026-03-12)

📊 Content stats:
  Articles: 25 files
  Courses: 3 directories
  Theory: 5 files
  Persona: 2 files

🟢 Server: Running
```

---

## 目录结构

```
codewithriver/
├── articles/      # 📄 技术文章和博客
├── courses/       # 📚 课程大纲和教程
├── theory/        # 📖 理论框架和方法论
├── persona/       # 🎭 写作人设和风格
├── images/        # 🖼️ 文章图片
├── server.py      # 🌐 Web 服务器
└── .git/          # 版本控制
```

---

## 完整工作流示例

### 示例1: 发布一篇新文章

```bash
# 1. 创建文章
bwp article "AI Agent 入门指南"

# 2. 编辑内容 (使用你喜欢的编辑器)
vim /home/claw/codewithriver/articles/2026-03-13-ai-agent-guide-v1.md

# 3. 提交到 Git
bwp commit "添加 AI Agent 入门指南"

# 4. 生成分享链接
bwp link articles/2026-03-13-ai-agent-guide-v1.md
```

---

### 示例2: 创建课程

```bash
# 1. 创建课程大纲
bwp course "OpenClaw 技能训练营"

# 2. 编辑课程结构
vim /home/claw/codewithriver/courses/openclaw-bootcamp/syllabus-v1.md

# 3. 提交
bwp commit "创建 OpenClaw 课程大纲"

# 4. 分享链接
bwp link courses/openclaw-bootcamp/syllabus-v1.md
```

---

## 版本迭代

创建新版本（手动复制并修改版本号）:

```bash
# 从 v1 创建 v1.1
cp articles/2026-03-13-topic-v1.md articles/2026-03-13-topic-v1.1.md

# 编辑改进
vim articles/2026-03-13-topic-v1.1.md

# 提交
bwp commit "改进文章 v1.1"
```

---

## 最佳实践

### 文件命名

✅ **推荐**:
```
2026-03-13-vibe-coding-article-v1.md
2026-03-13-openclaw-syllabus-v1.md
2026-03-13-writing-framework-v1.md
```

❌ **避免**:
```
article.md
final-draft.md
untitled.md
```

### 内容类型选择

| 你想写... | 使用命令 | 生成位置 |
|:----------|:---------|:---------|
| 技术博客文章 | `bwp article "标题"` | `articles/` |
| 课程/教程 | `bwp course "课程名"` | `courses/` |
| 方法论/框架 | `bwp theory "框架名"` | `theory/` |
| 写作风格定义 | `bwp persona "人设名"` | `persona/` |

---

## 快捷别名

添加到 `~/.bashrc`:

```bash
alias bwp="/home/claw/.openclaw/workspace/skills/build-with-public-writer/scripts/bwp.sh"
alias bwpa="bwp article"
alias bwpc="bwp course"
alias bwpt="bwp theory"
alias bwpp="bwp persona"
alias bwpls="bwp list"
alias bwpg="bwp commit"
```

---

**简化创作，专注内容 🚀**

---

## .env 配置说明

`bwp link` 命令会读取 `/home/claw/codewithriver/.env` 文件中的配置：

```bash
# /home/claw/codewithriver/.env
PORT=12000
CUSTOM_DOMAIN=your-domain.com  # 可选，用于生成分享链接
AUTH_USERNAME=user
AUTH_PASSWORD=your_password
```

- `CUSTOM_DOMAIN`: 设置后，`bwp link` 会生成 `http://your-domain.com:PORT/...` 的链接
- 未设置时，默认使用 `localhost`
- **注意**: 出于安全考虑，`bwp link` 不会显示实际的凭证值，请直接查看 .env 文件

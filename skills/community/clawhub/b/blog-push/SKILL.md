---
name: blog-push
description: Hugo 博客文章发布工具。支持三种内容类型：posts（博客文章）、daily（日报）、weekly（周报）。使用场景：(1) 用户需要发布博客文章到 Hugo，(2) "发布文章"、"publish blog"、"创建博客"、"发布日报"、"发布周报"，(3) 将完成的 Markdown 文档移动到对应目录。支持查看分类、选择目录、自动生成 front matter、处理封面图、草稿管理、环境变量配置、从任意目录执行。
---

# Hugo 博客文章发布技能

本技能用于将 Markdown 文档和封面图发布到 Hugo 博客系统，支持 **posts（博客文章）**、**daily（日报）**、**weekly（周报）** 三种内容类型，可从任意目录执行发布操作。

## 核心功能

1. **环境变量配置** - 通过环境变量配置博客路径，从任意位置执行
2. **查看分类目录** - 列出所有可用的博客分类
3. **发布文章** - 将 Markdown 文档复制到指定分类目录
4. **处理封面图** - 自动复制封面图并更新 front matter
5. **生成 front matter** - 基于 Hugo 模板自动生成元数据
6. **草稿管理** - 支持将文章标记为草稿
7. **智能内容分析** - 自动检测数学公式、Mermaid 图表，自动添加 libraries
8. **分类/标签建议** - 根据内容智能建议分类和标签
9. **Shortcodes 指南** - 内置 Shortcodes 使用参考

## 环境变量配置

### 配置方式

在 shell 配置文件中设置环境变量：

```bash
# ~/.zshrc 或 ~/.bashrc
export HUGO_BLOG_DIR=/Users/victor/Desktop/project/github/HUGO_blog
export HUGO_POSTS_DIR=content/zh/posts          # 可选，默认值
export HUGO_DAILY_DIR=content/zh/daily          # 可选，默认值
export HUGO_WEEKLY_DIR=content/zh/weekly        # 可选，默认值
export HUGO_TEMPLATE_PATH=archetypes/default.md # 可选，默认值
export HUGO_DAILY_TEMPLATE=archetypes/daily.md  # 可选，默认值
export HUGO_WEEKLY_TEMPLATE=archetypes/weekly.md # 可选，默认值
```

### 环境变量说明

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `HUGO_BLOG_DIR` | 博客项目根目录（完整路径） | 当前目录 `.` |
| `HUGO_POSTS_DIR` | posts 目录相对路径 | `content/zh/posts` |
| `HUGO_DAILY_DIR` | daily 目录相对路径 | `content/zh/daily` |
| `HUGO_WEEKLY_DIR` | weekly 目录相对路径 | `content/zh/weekly` |
| `HUGO_TEMPLATE_PATH` | posts 模板文件相对路径 | `archetypes/default.md` |
| `HUGO_DAILY_TEMPLATE` | daily 模板文件相对路径 | `archetypes/daily.md` |
| `HUGO_WEEKLY_TEMPLATE` | weekly 模板文件相对路径 | `archetypes/weekly.md` |

### 路径优先级

**命令行参数 > 环境变量 > 默认值**

优先级逻辑：
1. 命令行参数（如 `--blog-dir`）优先级最高
2. 环境变量（如 `HUGO_BLOG_DIR`）次之
3. 默认值优先级最低

## 使用方法

### 检查配置信息

```bash
python3 scripts/publish_blog.py --check-config
```

输出示例：
```
✓ Hugo 博客配置信息
============================================================
博客根目录: /Users/victor/Desktop/project/github/HUGO_blog
  来源: 环境变量
  状态: ✓ 有效 (检测到 Hugo 配置文件)

posts 目录: /Users/victor/Desktop/project/github/HUGO_blog/content/zh/posts
  来源: 默认值
  状态: ✓ 存在

模板路径: /Users/victor/Desktop/project/github/HUGO_blog/archetypes/default.md
  来源: 默认值
  状态: ✓ 存在
============================================================

环境变量配置:
  HUGO_BLOG_DIR: /Users/victor/Desktop/project/github/HUGO_blog
  HUGO_POSTS_DIR: (未设置)
  HUGO_TEMPLATE_PATH: (未设置)
```

### 查看 Shortcodes 使用指南

zzo 主题提供了丰富的 Shortcodes，用于增强文章表现力：

```bash
python3 scripts/publish_blog.py --shortcodes
```

这将显示以下 Shortcodes 的快速参考：
- 盒子（boxmd/box）- 支持 Markdown 的提示框
- 彩色提示框（alert）- info/warning/success/danger 四色警示
- 可折叠内容（expand）- 折叠长内容保持页面简洁
- 选项卡（tabs/codes）- 多平台/多语言内容对比
- 图片（img）- 带标题和说明的图片
- 按钮（button）- 行动号召按钮
- 封面图（featuredImage）- 显示 front matter 封面图

### 查看可用分类

**posts 类型**（需要指定分类）：
```bash
python3 scripts/publish_blog.py --type posts --list-categories
```

这将显示 `content/zh/posts/` 下的所有分类目录：
- AI
- AI编程
- 技术
- 思考
- 生活
- ...

**daily/weekly 类型**（直接查看现有文章）：
```bash
python3 scripts/publish_blog.py --type daily --list
python3 scripts/publish_blog.py --type weekly --list
```

### 发布到 posts（博客文章）

需要指定 `--category` 参数，文章会放入对应子目录：

```bash
python3 scripts/publish_blog.py \
  --md ./my-article.md \
  --type posts \
  --category 技术
```

### 发布到 daily（日报）

无需指定分类，文章直接放入 `content/zh/daily/`：

```bash
python3 scripts/publish_blog.py \
  --md ./ai-news.md \
  --type daily
```

### 发布到 weekly（周报）

无需指定分类，文章直接放入 `content/zh/weekly/`：

```bash
python3 scripts/publish_blog.py \
  --md ./weekly-log.md \
  --type weekly
```

### 带封面图发布

```bash
# posts 类型
python3 scripts/publish_blog.py \
  --md ./workspace/my-article.md \
  --cover ./images/cover.png \
  --type posts \
  --category AI

# daily 类型
python3 scripts/publish_blog.py \
  --md ./ai-daily.md \
  --cover ./cover.png \
  --type daily
```

封面图会被复制到文章所在目录，文件名格式为 `{文章名}-cover.{扩展名}`。

### 使用自定义目录（相对/绝对路径）

`--posts-dir` 和 `--template` 参数支持相对路径和绝对路径：

```bash
# 使用相对路径（相对于 --blog-dir）
python3 scripts/publish_blog.py \
  --md ./my-article.md \
  --type daily \
  --blog-dir /path/to/blog \
  --posts-dir content/zh/custom-daily

# 使用绝对路径
python3 scripts/publish_blog.py \
  --md ./my-article.md \
  --type posts \
  --category 技术 \
  --blog-dir /path/to/blog \
  --posts-dir /absolute/path/to/custom/dir \
  --template /absolute/path/to/custom/template.md
```

### 发布为草稿

```bash
# posts 类型
python3 scripts/publish_blog.py \
  --md ./workspace/draft.md \
  --type posts \
  --category 思考 \
  --draft

# daily 类型
python3 scripts/publish_blog.py \
  --md ./draft-daily.md \
  --type daily \
  --draft
```

草稿文章的 `draft` 字段会被设置为 `true`，不会在博客中显示。

### 自定义文章名

```bash
python3 scripts/publish_blog.py \
  --md ./workspace/my-article.md \
  --name "我的自定义标题" \
  --type posts \
  --category 技术
```

### 自定义标签

```bash
python3 scripts/publish_blog.py \
  --md ./ai-article.md \
  --type posts \
  --category AI \
  --tags "AI,Python,机器学习,深度学习"
```

## 智能内容分析

脚本会自动分析 Markdown 内容，智能添加以下功能：

### 1. 自动检测数学公式

如果内容包含 LaTeX 数学公式（`$...$` 或 `$$...$$`），会自动在 front matter 中添加：
```yaml
libraries: [katex]
```

### 2. 自动检测 Mermaid 图表

如果内容包含 Mermaid 图表代码块（`` ```mermaid ``），会自动在 front matter 中添加：
```yaml
libraries: [mermaid]
```

### 3. 自动检测图表内容

如果内容包含图表相关内容，会自动添加：
```yaml
libraries: [chart, flowchartjs]
```

### 4. 智能分类建议

根据内容自动建议最适合的分类：
- **技术**: 代码、编程、开发、架构、API、数据库、Docker、Git 等
- **AI**: AI、人工智能、机器学习、LLM、大模型、Claude、GPT、Prompt 等
- **生活**: 读书、电影、旅行、咖啡、美食、运动、日常、随笔等
- **思考**: 思考、观点、方法论、职业规划、成长、效率、复盘等

### 5. 智能标签建议

根据内容自动建议相关标签：
- **AI/LLM**: AI, Claude, GPT, LLM, Prompt, OpenAI, Anthropic, 大模型
- **编程**: Python, Java, Go, JavaScript, TypeScript, 架构, 微服务, 云原生
- **工具**: Obsidian, Docker, Git, Hugo, Cursor, VSCode
- **效率**: 工作流, 自动化, 时间管理, 效率工具
- **生活**: 读书, 电影, 旅行, 咖啡, 健康

示例输出：
```
📝 智能内容分析:
  ✓ 检测到数学公式，已添加 katex 库
  ✓ 检测到 Mermaid 图表，已添加 mermaid 库
  ✓ 建议分类: 技术
  ✓ 建议标签: Python, Docker, 架构
```

## Front Matter 处理

脚本会自动处理 Hugo 的 front matter：

1. **标题** - 使用文章名称或自定义名称
2. **日期** - 自动生成当前时间（格式：`YYYY-MM-DDTHH:MM:SS+08:00`）
3. **封面图** - 如果提供封面，自动填充 `image` 字段
4. **草稿状态** - 根据 `--draft` 参数设置
5. **Libraries** - 根据内容自动检测并添加（katex, mermaid, chart, flowchartjs）
6. **分类** - 智能建议或手动指定
7. **标签** - 智能建议或手动指定

### 默认模板

**posts 类型**使用 `archetypes/default.md`：

```yaml
---
title: "{{ 文章标题 }}"
subtitle: 
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
aliases:
description:
image: {{ 封面图（如果有） }}
draft: false
hideToc: false
enableToc: true
enableTocContent: false
tocPosition: inner
author: VictorHong
authorEmoji: 🪶
authorImageUrl:
tocLevels: ["h1","h2", "h3", "h4"]
libraries: [katex, mathjax, mermaid, chart, flowchartjs, msc, viz, wavedrom]
tags: []
series: []
categories: []
---
```

**daily 类型**使用 `archetypes/daily.md`（简洁版）：

```yaml
---
title: "{{ 文章标题 }}"
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
description:
tags:
  - AI
  - Daily Digest
categories:
  - AI
image:
---
```

**weekly 类型**使用 `archetypes/weekly.md`：

```yaml
---
title: "{{ 年 }}-{{ 月 }} Weekly Log"
date: {{ 自动生成 }}
publishDate: {{ 自动生成 }}
description:
tags:
  - weekly
series: 
categories:
  - weekly
image:
---
```

## 工作流程建议

### 推荐流程

1. **配置环境变量**
   ```bash
   # 在 ~/.zshrc 中添加
   export HUGO_BLOG_DIR=/Users/victor/Desktop/project/github/HUGO_blog
   ```

2. **编写文章**
   - 在任意位置创建 Markdown 文件
   - 使用 Obsidian 或其他编辑器
   - 完成内容编写

3. **准备封面图（可选）**
   - 推荐尺寸：1200x630（社交媒体分享）
   - 支持格式：png, jpg, webp

4. **检查配置**
   ```bash
   python3 scripts/publish_blog.py --check-config
   ```

5. **查看分类/现有文章**

   posts 类型（查看分类）：
   ```bash
   python3 scripts/publish_blog.py --type posts --list-categories
   ```

   daily/weekly 类型（查看现有文章）：
   ```bash
   python3 scripts/publish_blog.py --type daily --list
   python3 scripts/publish_blog.py --type weekly --list
   ```

6. **发布文章**

   posts 类型（需指定分类）：
   ```bash
   python3 scripts/publish_blog.py \
     --md ~/Downloads/完成的文章.md \
     --cover ~/Downloads/封面图.png \
     --type posts \
     --category 技术
   ```

   daily 类型（直接发布）：
   ```bash
   python3 scripts/publish_blog.py \
     --md ~/Downloads/ai-news.md \
     --type daily
   ```

   weekly 类型（直接发布）：
   ```bash
   python3 scripts/publish_blog.py \
     --md ~/Downloads/weekly-log.md \
     --type weekly
   ```

7. **本地预览**
   ```bash
   cd $HUGO_BLOG_DIR
   hugo server -D
   ```
   访问 http://localhost:1313 查看效果

8. **构建并部署**
   ```bash
   cd $HUGO_BLOG_DIR
   hugo
   git add .
   git commit -m "发布新文章：文章标题"
   git push
   ```

## Shortcodes 使用参考

zzo 主题提供了丰富的 Shortcodes，用于增强文章表现力。

### 盒子（Box）

支持 Markdown 语法的盒子：

```markdown
{{< boxmd >}}
This is **boxmd** shortcode，支持 **粗体** 等 Markdown 语法
{{< /boxmd >}}
```

### 彩色文本框（Alert）

```markdown
{{< alert theme="warning" >}}
**警告** 内容
{{< /alert >}}

{{< alert theme="info" >}}
**信息** 内容
{{< /alert >}}

{{< alert theme="success" >}}
**成功** 内容
{{< /alert >}}

{{< alert theme="danger" >}}
**危险** 内容
{{< /alert >}}
```

### 展开栏（Expand）

可折叠的内容区域：

```markdown
{{< expand "点击展开" >}}

### 标题

折叠的内容

{{< /expand >}}
```

### 选项卡（Tabs）

代码选项卡（codes）：

```markdown
{{< codes java javascript >}}
  {{< code >}}

  ```java
  System.out.println("Hello World!");
  ```

  {{< /code >}}

  {{< code >}}

  ```javascript
  console.log("Hello World!");
  ```

  {{< /code >}}
{{< /codes >}}
```

常规内容选项卡（tabs）：

```markdown
{{< tabs Windows MacOS Ubuntu >}}
  {{< tab >}}

### Windows section
Windows 相关内容

  {{< /tab >}}
  {{< tab >}}

### MacOS section
MacOS 相关内容

  {{< /tab >}}
  {{< tab >}}

### Ubuntu section
Ubuntu 相关内容

  {{< /tab >}}
{{< /tabs >}}
```

### 图片（Image）

```markdown
{{< img src="https://example.com/image.jpg" 
       title="图片标题" 
       caption="图片描述" 
       alt="alt 文本" 
       width="700px" 
       position="center" >}}
```

显示 front matter 封面图：

```markdown
{{< featuredImage >}}
```

### 按钮（Button）

```markdown
<!-- 简单按钮 -->
{{< button href="https://hugo.jiahongw.com" >}}访问博客{{< /button >}}

<!-- 设置宽高 -->
{{< button href="https://hugo.jiahongw.com" width="100px" height="36px" >}}访问博客{{< /button >}}

<!-- 设置颜色主题 -->
{{< button href="https://hugo.jiahongw.com" width="100px" height="36px" color="primary" >}}访问博客{{< /button >}}
```

### 使用建议

| Shortcode | 使用场景 |
|-----------|----------|
| `boxmd` / `box` | 提示框、注释框 |
| `codes` / `tabs` | 多平台/多语言代码对比 |
| `expand` | 折叠长内容，保持页面简洁 |
| `alert` | 需要强调的四色警示信息 |
| `img` | 需要标题和说明的图片 |
| `button` | 行动号召按钮、链接跳转 |

## 文件命名规则

- 文章名会自动转换为小写
- 空格替换为连字符
- 移除特殊字符
- 示例：`"我的第一篇博客"` → `"我的第一篇博客"` → `"我的第一篇博客.md"`

## 注意事项

1. **文章已存在** - 如果目标文件已存在，脚本会警告并覆盖
2. **原 front matter** - Markdown 文件原有的 front matter 会被移除
3. **分类不存在** - 如果指定的分类不存在，脚本会创建新目录
4. **封面图路径** - 支持相对路径和绝对路径
5. **博客验证** - 脚本会检查博客根目录是否包含 Hugo 配置文件
6. **路径处理** - `--posts-dir` 和 `--template` 参数支持相对路径和绝对路径。使用相对路径时，会自动相对于 `--blog-dir` 解析
7. **智能分析** - 脚本会自动检测数学公式（`$...$`、`$$...$$`）、Mermaid 图表（`` ```mermaid ``），并添加相应的 libraries
8. **分类建议** - 当使用 `--category` 参数时，会覆盖智能分类建议
9. **标签建议** - 使用 `--tags` 参数指定的标签会与智能建议的标签合并，并自动去重

## 完整参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--type` | `-t` | 内容类型: `posts`/`daily`/`weekly` | `posts` |
| `--check-config` | - | 显示当前配置信息和来源 | - |
| `--list-categories` | `-l` | 显示所有分类目录（仅 posts 类型） | - |
| `--list` | - | 显示现有文章（仅 daily/weekly 类型） | - |
| `--md` | `-m` | Markdown 文件路径 | 必需 |
| `--cover` | `-c` | 封面图片路径 | 可选 |
| `--category` | `-cat` | 博客分类目录名称（posts 类型必需） | - |
| `--name` | `-n` | 自定义文章名称 | 使用文件名 |
| `--draft` | `-d` | 标记为草稿 | false |
| `--tags` | - | 自定义标签（逗号分隔，例如：AI,Python,技术） | - |
| `--shortcodes` | - | 显示 Shortcodes 使用指南 | - |
| `--blog-dir` | - | Hugo 博客项目根目录（完整路径） | 环境变量或当前目录 |
| `--posts-dir` | - | 目标目录完整路径。支持相对路径（相对于 blog_dir）或绝对路径 | 环境变量或默认相对路径 |
| `--template` | - | 模板文件完整路径。支持相对路径（相对于 blog_dir）或绝对路径 | 环境变量或默认相对路径 |

## 技术细节

- **脚本语言**: Python 3
- **依赖**: 仅使用标准库
- **兼容性**: 支持 macOS/Linux/Windows
- **编码**: UTF-8（支持中文）
- **Hugo 验证**: 自动检测 config.toml/yaml/json
- **智能分析**: 使用正则表达式检测数学公式、Mermaid 图表、图表内容
- **分类建议**: 基于关键词匹配的分类推荐算法
- **标签建议**: 基于内容的关键词提取和标签匹配

## Resources

### scripts/

- `publish_blog.py` - Hugo 博客文章发布脚本，实现所有核心功能

该脚本仅使用 Python 标准库，无需安装额外依赖。
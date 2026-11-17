---
name: book-capsule-skill
description: 胶囊书架——书摘胶囊的归处。输入一个作者或一本书，生成精美卡片式书摘文章，自动归入书架。书架为单页应用：首页展示全部胶囊卡片，点击即读、随时返回，无需跳转。帮你对抗遗忘、碎片阅读、构建持续生长的个人阅读档案。
---

# 胶囊书架

> 书摘胶囊的归处 · 触发词：胶囊书架 / 书摘胶囊 / 读书胶囊 / 来颗胶囊 / 浓缩一本书 / 做书摘 / 帮我做一张XX的书摘

---

## Agent 执行流程

用户只需给出 **书名或作家名**，以下全流程由你自主完成，**中间不要问用户任何问题**：

### 1. 收集内容

根据用户指定的书名/作家，搜集以下信息（优先用你的知识库，不足则 `web_search`）：

- 作者简介（一两句话）
- 书籍核心主题（5~8 个关键概念/章节/观点，每个提炼为一张卡片）
- 每个主题下的经典金句（2~4 句原文）
- 3~5 条全书级穿越金句（超越单章、贯穿全书的句子）
- 如果用户给的是作家名而非单本书：选取代表作 5~8 部，每部一张卡片

### 2. 构建 JSON

在同目录下用 `write_file` 创建临时 JSON 文件，写入 `{temp}` 目录。结构如下：

```json
{
  "date": "2026 - 0 7 - 3 0",
  "title": "书名或主题名",
  "title_line2": "{count} 张主题卡 · {quotes} 句精华",
  "subtitle": "一句话副标题",
  "intro_paragraphs": [
    "引言第一段，介绍这本书/这位作家",
    "引言第二段，点出核心价值"
  ],
  "gold_quotes": [
    {"text": "全书级金句正文", "source": "—— 作者《书名》", "after_card": 0},
    {"text": "穿越金句正文", "source": "—— 作者《书名》", "after_card": 2},
    {"text": "穿越金句正文", "source": "—— 作者《书名》", "after_card": 5}
  ],
  "footer_collection_title": "经典阅读 · 书名 / 作家名特辑",
  "footer_subtitle": "",
  "footer_end_quote": {"text": "收束金句正文", "source": "—— 作者《书名》"},
  "cards": [
    {
      "number": "01",
      "book_title": "卡片标题（章节名/概念名/书名）",
      "book_info": "卡片简述（豆瓣评分 / 一句话介绍）",
      "quotes": [
        {"index": "01", "text": "金句正文"},
        {"index": "02", "text": "金句正文"}
      ]
    }
  ]
}
```

**关键规则**：
- 卡片数量不设上限，按内容自然决定
- `title_line2` 和 `footer_subtitle` 用 `{count}` `{quotes}` `{all_quotes}` 占位符，生成器自动替换实际数量
- `footer_subtitle` 留空即可，默认生成 `"N张卡片 · M句精华"`
- 金句必须忠于原著原文，宁缺毋滥
- JSON 写入 `{temp}` 目录，文件名格式 `book-capsule-{书名拼音}.json`

### 3. 生成 HTML

用 `shell_executor` 执行：

```powershell
python "{skill_dir}/generate-book-article.py" "{json_path}" "{output_dir}/book-capsule-{书名拼音}.html"
```

变量说明：
- `{skill_dir}` = 本 skill 所在目录（即 SKILL.md 所在目录，下同）
- `{json_path}` = 步骤 2 写入的 JSON 文件路径
- `{output_dir}` = 会话的 output 目录

**书架自动更新**：generate-book-article.py 生成 HTML 后会自动将本书注册到 `capsule-registry.json` 并刷新 `bookshelf.html`，无需额外操作。

### 4. 交付

步骤 3 生成的 HTML 即为最终交付物，浏览器直接打开即可查看。如需 PDF，在浏览器中「打印 → 另存为 PDF」即可。

### 5. 呈现

向用户告知已完成，展示 HTML 文件路径和书架总页路径，用 `yyb-product` 卡片声明最终产出物。

**话术示例**：
> 《活着》的书摘胶囊已生成：8 张主题卡 + 4 条穿越金句，浏览器打开即可查看。书架已同步更新。

---

## 技术速查

### 占位符

| 占位符 | 含义 |
|--------|------|
| `{count}` | 卡片张数 |
| `{quotes}` | 卡片内金句数（不含穿越句） |
| `{all_quotes}` | 全部金句（卡片内 + 穿越句） |

### 可用文件

| 文件 | 用途 |
|------|------|
| `generate-book-article.py` | 核心生成器，纯 Python 标准库，零依赖。生成后自动注册到书架 |
| `article-template.html` | 固定宽度 600px 模板 |
| `generate-bookshelf.py` | 书架生成器，管理注册表并生成 `bookshelf.html` |
| `bookshelf-template.html` | 书架总页模板，卡片式并排展示 |
| `capsule-registry.json` | 胶囊注册表（元数据），每次生成自动追加 |
| `bookshelf.html` | 书架总页（自动生成），持续生长的个人阅读档案 |
| `book-data-dongye.json` | 东野圭吾示例（参考格式） |
| `book-data-inamori.json` | 稻盛和夫示例（参考格式） |

### 模板参数

所有 JSON 字段说明见步骤 2 的 JSON 结构。卡片字段名 `book_title` / `book_info` 是模板变量名，实际内容为章节名、概念名或书名，不限于"书"。

---

## 设计规范

- 固定宽度 600px，不随屏幕自适应
- 卡片底色 #F7F5F0，编号红色 #E63946，金句分割线红色 2px
- 微信兼容：全 inline style + table 布局
- 金句穿插通过 `after_card` 控制插入位置

---

## 安全说明

- **自动文件写入**：本技能在生成书摘时会自动写入 HTML 文件、更新 `capsule-registry.json` 并刷新 `bookshelf.html`，所有写入均在技能目录内完成，无二次确认流程。
- **路径收容**：书架生成器（`generate-bookshelf.py`）已内置 `os.path.realpath` + `os.path.commonpath` 双重路径校验，拒绝 `../` 逃逸，注册表路径强制限定在技能目录内。
- **内容审阅**：生成的 JSON 数据和 HTML 页面可能包含从网络搜集的文本片段，建议在分享或公开发布前自行审阅内容准确性和版权合规性。
- **可信文件**：`capsule-registry.json` 中存储的 `html_path` 条目应仅指向本技能自身生成的文件，避免手动填入外部路径。

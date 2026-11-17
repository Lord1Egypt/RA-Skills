# 书摘胶囊

> 想读一本好书？来一颗书摘胶囊。

一台私人阅读浓缩机。输入一个作家或主题的 JSON 数据，一键生成排版精美的卡片式书摘 HTML 文章。一本书，一张卡，一颗胶囊。纯本地运行，零外部依赖。

---

## 三秒上手

```bash
python generate-book-article.py book-data-dongye.json 东野圭吾书摘.html
```

双击生成的 HTML，浏览器里就能看到排版精美的卡片式书摘。

---

## 完整工作流

```
阶段一：准备 JSON 数据
    │
    ├── 确定作家 / 主题
    ├── 收集作品名、豆瓣评分、经典名句
    ├── 按 book-data-dongye.json 结构编写 JSON
    │
    ▼
阶段二：生成 HTML
    │
    └── python generate-book-article.py <json> [output]
        读取 article-template.html → 填充 → 输出完整 HTML
    │
    ▼
阶段三：查看 / 使用
    │
    └── 双击 HTML 文件，浏览器直接打开
        保存到手机 / 电脑 / 云盘，随时翻阅
```

---

## JSON 数据结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 日期，如 `2026 - 07 - 30` |
| `title` | string | 主标题第一行 |
| `title_line2` | string | 第二行，数字自动替换 |
| `subtitle` | string | 标题下方副标题 |
| `intro_paragraphs` | string[2] | 引言两段 |
| `gold_quotes` | object[] | 穿插金句 |
| `cards` | object[] | 作品卡片数组 |
| `footer_collection_title` | string | 页脚大标题 |
| `footer_subtitle` | string | 留空则自动生成 |
| `footer_end_quote` | object | 结尾金句 `{text, source}` |
| `footer_quote` | string | 页脚小字引用（可选） |

### gold_quotes 子对象

| 字段 | 说明 |
|------|------|
| `text` | 金句正文（支持 `<br>`） |
| `source` | 出处 |
| `after_card` | 0=引言后，N=卡片N之后 |

### cards 子对象

| 字段 | 说明 |
|------|------|
| `number` | 序号 `"01"` |
| `book_title` | 作品名 |
| `book_info` | 简述（评分/特色，支持 `<br>`） |
| `quotes` | 金句数组 `[{index, text}]` |

---

## 卡片样式速查

| 元素 | 字号 | 字重 | 颜色 |
|------|------|------|------|
| 日期 | 12px | 400 | #AAAAAA |
| 主标题 | 24px | 800 | #111111 |
| 副标题 | 14px | 400 | #999999 |
| 引言 | 14px | 400 | #666666 |
| 金句正文 | 17px | 700 | #222222 |
| 金句出处 | 12px | 400 | #AAAAAA |
| 卡片编号 | 42px | 200 | #E63946 |
| 作品名 | 18px | 700 | #1A1A1A |
| 卡片金句 | 15px | 400 | #444444 |
| 页脚标题 | 15px | 700 | #333333 |
| 页脚副标题 | 12px | 400 | #AAAAAA |

| 视觉要素 | 值 |
|---------|-----|
| 卡片底色 | #F7F5F0 |
| 页面底色 | #F5F2EB |
| 卡片圆角 | 16px |
| 卡片内边距 | 28px 20px 24px 20px |
| 金句分割线 | 40px, 2px solid #E63946 |
| 金句间细线 | 1px solid #E8E4DC |
| 页脚分割线 | 1px solid #EEEEEE |

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `generate-book-article.py` | JSON → HTML 生成器（纯 Python 标准库） |
| `article-template.html` | HTML 骨架模板 |
| `book-data-dongye.json` | 东野圭吾示例 |
| `book-data-inamori.json` | 稻盛和夫示例 |
| `inamori-capsule.html` | 稻盛和夫示例输出 |
| `SKILL.md` | Skill 工作流文档 |
| `skill.yaml` | Skill 元信息 |
| `template-usage.md` | 模板占位符详细说明 |

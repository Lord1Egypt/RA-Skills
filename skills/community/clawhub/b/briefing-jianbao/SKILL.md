---
name: briefing
description: 将任意内容（URL/文件/文本）生成单页幻灯片简报，输出为图片/PDF/网页。基于 frontend-slides 构建。触发条件：(1) "生成简报"、"AI简报"、"摘要" (2) 上传文件并要求生成简报
---

# Briefing Generator

将任意内容生成为精美的单页幻灯片简报，输出为图片（默认）/PDF/网页。

## 支持的输入格式

| 类型 | 处理方式 |
|------|---------|
| URL 链接 | web_fetch 获取网页内容 |
| Word (.docx) | python-docx 提取文字 |
| Excel (.xlsx) | openpyxl 提取数据 |
| PDF (.pdf) | pdfplumber 提取文字 |
| 纯文本 | 直接使用内容 |
| 图片 | 图像识别提取信息 |

## 支持的输出格式

| 格式 | 说明 | 适用场景 |
|------|------|---------|
| **图片 (PNG)** | 默认输出 | 分享、微信 |
| PDF | 打印为 PDF | 文档存档 |
| 网页 (HTML) | 交互式幻灯片 | 演示播放 |

## 支持的风格

使用 frontend-slides 的所有预设风格：

| 风格名称 | 风格描述 |
|----------|---------|
| Bold Signal | 活力橙红，卡片式设计 |
| Electric Studio | 清新蓝绿，渐变背景 |
| Creative Voltage | 活力复古，几何图形 |
| Dark Botanical | 优雅深色，植物装饰 |
| Notebook Tabs | 杂志风格，彩色标签 |
| Pastel Geometry | 柔和粉彩，现代简约 |
| Split Pastel | 明亮分割，活泼现代 |
| Vintage Editorial | 复古编辑，幽默个性 |
| Neon Cyber | 霓虹赛博，网格背景 |
| Terminal Green | 终端绿，开发者风格 |
| Swiss Modern | 瑞士现代，极简精确 |
| Paper & Ink | 纸墨风格，文学质感 |

## 工作流程

### Step 1: 识别输入类型

根据用户输入判断类型：
- 以 `http://` 或 `https://` 开头 → URL
- 以 `.docx`、`.xlsx`、`.pdf` 结尾 → 文件
- 其他 → 纯文本

### Step 2: 提取内容

**URL**：
```javascript
web_fetch({
  url: "链接",
  maxChars: 10000
})
```

**Word/Excel/PDF**：使用 Python 库提取

**图片**：使用 image 工具分析

### Step 3: 提取关键信息

用规则从内容中提取：
- 标题：从文件名、`<title>`、第一行标题提取
- 数据：提取数字、百分比、关键词
- 要点：从段落中筛选重要句子

### Step 4: 选择风格

**Question: 简报风格**
- Header: "风格"
- Question: "想要什么风格？"
- Options（列出 frontend-slides 的 12 种风格）

### Step 5: 选择输出格式

**Question: 输出格式**
- Header: "输出"
- Question: "想要什么格式？"
- Options:
  - "图片 (PNG)" - 默认，分享方便
  - "PDF" - 适合打印存档
  - "网页 (HTML)" - 交互式演示

### Step 6: 选择页面尺寸

**Question: 页面尺寸**
- Header: "尺寸"
- Options:
  - "A4" - 竖版文档
  - "16:9" - 宽屏演示

### Step 7: 生成并输出

根据输出格式选择：
- **图片**：浏览器截图
- **PDF**：浏览器打印
- **网页**：直接打开 HTML

---

## 速度优化

1. 跳过 AI 总结，规则提取关键信息
2. 内容长度限制 10000 字符
3. 复用已有浏览器窗口

---

## 错误处理

- 无法提取内容时，询问用户手动输入关键信息
- 文件格式不支持时，提示用户转换为其他格式
- 输出失败时，提供 HTML 文件作为备选

---

## 致谢

本 Skill 使用了 [frontend-slides](https://clawhub.com/skill/frontend-slides) 进行幻灯片渲染，特此致谢。

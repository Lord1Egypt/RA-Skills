# 工作流 00：Input Type Router

## 目标

在任何内容处理前，先判断用户给的是什么输入源，并选择对应适配器。

## 输入类型判断

### 1. PDF

特征：文件扩展名为 `.pdf`，或用户说“这个 PDF”。

转入：`references/source-adapters/pdf-adapter.md`

### 2. 网页 / URL

特征：包含 http/https 链接，或用户说“这个网页 / 这篇文章 / 这个链接”。

转入：`references/source-adapters/webpage-adapter.md`

### 3. 纯文本 / 长文

特征：用户直接粘贴正文、笔记、文案、文章片段。

转入：`references/source-adapters/text-adapter.md`

### 4. 视频

特征：视频链接、视频文件、B站/YouTube/小红书视频、用户说“这个视频”。

转入：`references/source-adapters/video-adapter.md`

### 5. 音频

特征：音频文件、播客、访谈录音、用户说“这段音频”。

转入：`references/source-adapters/audio-adapter.md`

### 6. 图片 / 截图

特征：图片文件、截图、已有信息图、手写笔记照片。

转入：`references/source-adapters/image-adapter.md`

### 7. PPT / Slides

特征：PPT、Keynote、Google Slides、演示文稿。

转入：`references/source-adapters/slides-adapter.md`

### 8. 多源混合

特征：用户同时提供 PDF + 文本 + 参考图 / 网页 + 视频字幕等。

转入：`references/source-adapters/mixed-media-adapter.md`

### 9. 单字 / 词表 / 结构化表格

特征：用户提供单个汉字、词汇表、语法点列表、短语列表或结构化表格。

转入：`references/source-adapters/text-adapter.md`

短路提示：当输入为单个汉字时，Output Mode Router 可优先路由到 `character-card`；当输入为词表 / 语法点 / 短语列表时，可优先路由到 `vocabulary-card` / `grammar-card` / `phrase-card`。仍需完成 Source Lock，但可简化为快速 Source Lock。

## 决策输出

每次必须形成：

```md
## Input Type Router 结果

- 输入源类型：
- 可读取程度：完整 / 部分 / 不可读取
- 需要的适配器：
- 是否需要用户补充：是 / 否
- 下一步：Source Lock
```

## 缺失信息处理

如果输入源无法完整读取：

- 不得猜测完整内容。
- 可以基于可见内容生成“低保真 Source Lock”。
- 必须标注不确定信息。
- 对视频 / 音频，若无转写稿，应要求字幕或摘要。

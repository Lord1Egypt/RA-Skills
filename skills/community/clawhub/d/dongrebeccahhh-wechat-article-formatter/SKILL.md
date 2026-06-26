---
name: wechat-article-formatter
description: 微信公众号文章排版优化工具，支持段落分明、标题层级、可读性增强、多种排版风格。专为公众号运营者设计。
version: 1.0.0
author: 猪猪助手
grade: A
category: office
tags: [wechat, 公众号, 排版, 格式化, 文章优化]
---

# 微信公众号文章排版优化工具

专业的公众号文章排版优化工具，提升文章可读性和专业度。

## 核心功能

### 1. 段落优化
- 自动分段，段落分明
- 控制段落长度（理想300字内）
- 段落间增加适当间距

### 2. 标题层级
- 一级标题：主标题
- 二级标题：章节标题
- 三级标题：小节标题
- 自动添加空行分隔

### 3. 可读性增强
- 字数统计和建议
- 阅读时间估算
- 长句拆分
- 关键信息强调

### 4. 多种排版风格

#### 极简风格（推荐）
- 无emoji
- 无图片
- 纯文字
- 段落分明

#### 专业风格
- 标题加粗
- 关键点强调
- 列表格式化
- 引用块优化

#### 轻松风格
- 适当emoji
- 图文结合
- 互动元素

## 使用方法

### 命令行使用

```bash
# 基础排版
node scripts/format-article.js input.md output.md

# 指定风格
node scripts/format-article.js input.md output.md --style minimal

# 仅分析
node scripts/format-article.js input.md --analyze
```

### 编程接口

```javascript
const formatter = require('wechat-article-formatter');

// 格式化文章
const result = formatter.format(content, {
  style: 'minimal',      // minimal | professional | casual
  maxParagraph: 300,     // 最大段落字数
  addSpacing: true,      // 增加段落间距
  noEmoji: true          // 去除emoji
});

console.log(result.formatted);
console.log(result.stats);
```

## 排版规范

### 段落规则
- 每段2-8句话
- 理想段落300字以内
- 段落间空2行

### 标题规则
- 主标题：≤30字
- 章节标题：≤20字
- 小节标题：≤25字
- 标题后空1行

### 列表规则
- 无序列表用 `*`
- 有序列表用数字
- 列表项≤50字
- 列表前后空行

### 引用规则
- 引用用 `>` 标记
- 引用长度≤200字
- 引用前后空行

### 强调规则
- 重要信息用 `**粗体**`
- 次要信息用 `*斜体*`
- 关键数据高亮

## 输出格式

### Markdown格式
```markdown
# 主标题

文章开头段落...

## 章节标题

章节内容段落...

### 小节标题

小节内容段落...

* 列表项1
* 列表项2
* 列表项3

> 引用内容

**重要信息**强调

---
```

### HTML格式（可选）
```html
<h1>主标题</h1>
<p>文章开头段落...</p>
<h2>章节标题</h2>
<p>章节内容段落...</p>
```

## 配置选项

```json
{
  "style": "minimal",
  "maxParagraph": 300,
  "maxSentence": 50,
  "addSpacing": true,
  "noEmoji": true,
  "noImages": false,
  "titleStyle": {
    "h1": { "size": 32, "bold": true },
    "h2": { "size": 24, "bold": true },
    "h3": { "size": 20, "bold": false }
  },
  "paragraphStyle": {
    "lineHeight": 1.8,
    "margin": "1em 0"
  }
}
```

## 最佳实践

### 1. 文章结构
```
标题（吸睛）
↓
摘要（100-150字）
↓
正文（1500-2000字）
  - 开头（引入）
  - 中间（论述）
  - 结尾（总结）
↓
标签（3-5个）
```

### 2. 段落技巧
- 每段一个观点
- 首句点明主旨
- 避免长句
- 适当断句

### 3. 标题技巧
- 简洁有力
- 数字化（"5个方法"）
- 提问式（"如何..."）
- 对比式（"A vs B"）

### 4. 强调技巧
- 关键词加粗
- 数据高亮
- 引用名人名言
- 使用列表

## 常见问题

### Q: 如何去除emoji？
A: 设置 `noEmoji: true`，自动过滤所有emoji表情

### Q: 如何控制段落长度？
A: 设置 `maxParagraph: 300`，自动拆分长段落

### Q: 如何增加可读性？
A: 启用 `addSpacing: true`，自动增加段落间距

### Q: 支持哪些输入格式？
A: 支持 Markdown、纯文本、HTML（需转换）

## 与其他工具集成

### 与 wechat-mp-toolkit 集成
```bash
# 创作文章
node wechat-mp-toolkit/scripts/create-article.js --output article.md

# 排版优化
node wechat-article-formatter/scripts/format-article.js article.md formatted.md

# 发布文章
node wechat-mp-toolkit/scripts/publish-article.js formatted.md
```

### 批量处理
```bash
# 批量格式化
for file in articles/*.md; do
  node scripts/format-article.js "$file" "formatted/$(basename $file)"
done
```

## 示例对比

### 排版前
```
这是一段很长的文字没有分段读起来很累，没有重点让人抓不住核心内容，用户体验很差。
```

### 排版后
```
这是一段经过优化的文字。

分段清晰，读起来轻松。

**重点突出**，核心内容一目了然。

用户体验大幅提升。
```

## 技术细节

### 依赖
- Node.js 14+
- 无外部依赖（纯JavaScript实现）

### 性能
- 处理速度：1000字/秒
- 内存占用：<10MB
- 支持文件大小：≤1MB

### 兼容性
- 支持 Markdown 格式
- 支持微信公众号编辑器
- 支持主流排版工具

## 更新日志

### v1.0.0 (2026-03-15)
- ✅ 初始版本
- ✅ 支持三种排版风格
- ✅ 自动段落优化
- ✅ 可读性分析

---

**适用场景**：公众号运营、内容创作、文案优化

**关键词**：排版、格式化、可读性、公众号、文章优化
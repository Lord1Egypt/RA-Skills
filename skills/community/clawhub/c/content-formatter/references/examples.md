# 示例 - content-formatter

> 来源: SKILL.md§示例

## 示例1: Markdown平台(掘金) - L0 无需转换

### 输入
```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 测试标题" \
  --platform juejin
```

### 输出
```json
{
  "success": true,
  "data": {
    "html": "",
    "markdown": "# 测试标题",
    "text": "",
    "format_used": "markdown",
    "layer": "L0"
  },
  "error": null
}
```

## 示例2: 微信公众号 - L2 平台专属排版

### 输入
```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 测试标题" \
  --platform wechat_official
```

### 输出
```json
{
  "success": true,
  "data": {
    "html": "<h1 style=\"...\">测试标题</h1>",
    "markdown": "# 测试标题",
    "text": "",
    "format_used": "html",
    "layer": "L2"
  },
  "error": null
}
```

## 示例3: Twitter/X - L3 纯文本截断

### 输入
```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 标题\n\n这是一段很长的正文内容..." \
  --platform x_twitter
```

### 输出
```json
{
  "success": true,
  "data": {
    "html": "",
    "markdown": "标题\n\n这是一段很长的正文内容...",
    "text": "标题 这是一段很长的正文内容...",
    "format_used": "text",
    "layer": "L3"
  },
  "error": null
}
```

## 示例4: 未知平台降级 - L1 通用HTML

### 输入
```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 标题\n\n正文" \
  --platform unknown_platform
```

### 输出
```json
{
  "success": true,
  "data": {
    "html": "<h1>标题</h1><p>正文</p>",
    "markdown": "# 标题\n\n正文",
    "text": "",
    "format_used": "html",
    "layer": "L1"
  },
  "error": null
}
```

## 示例5: L2降级到L1(fallback)

### 输入
```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 标题" \
  --platform wechat_official
# (format_converter.py不存在时)
```

### 输出
```json
{
  "success": true,
  "data": {
    "html": "<h1>标题</h1>",
    "markdown": "# 标题",
    "text": "",
    "format_used": "html",
    "layer": "L1(fallback)"
  },
  "error": null
}
```

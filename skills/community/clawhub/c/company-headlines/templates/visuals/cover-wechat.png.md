# 公众号封面视觉模板

## 用途
微信公众号推文封面图（头条封面）。

## 输出规格
- 尺寸：900×500px（横版封面，2.35:1比例是公众号推荐比例，900×383也可）
- 格式：PNG
- 生成方式：image-lab (Gemini)

## 设计要素

### 布局
```
┌──────────────────────────────┐
│                              │
│    [左侧装饰/图形]            │
│                              │
│         主标题大字            │
│         (6-12字)             │
│                              │
│         副标题/数据小字        │
│                              │
│                    [品牌标]   │
└──────────────────────────────┘
```

### 规则
- 文字居中或偏左（不要偏右，会被头像遮挡）
- 标题不要超过12字
- 下1/5区域留空（会被标题文字遮挡）
- 品牌色为主，简洁有力

## 生成 Prompt 模板

```
Create a horizontal cover image (900x500) for a WeChat official account article.

Style: Clean, modern, corporate B2B aesthetic. Not too busy.
Color palette: {{BRAND_PRIMARY_COLOR}} dominant, with {{BRAND_SECONDARY_COLOR}} accents.

Main title: "{{HEADLINE}}" (center or left-aligned, large bold text, 6-12 characters max)
Subtitle/small text: "{{SUB_DETAIL}}" (below title, smaller)
Brand marker: {{COMPANY_NAME}} (bottom-right, small)

Topic: {{TOPIC}}
Mood: {{MOOD}} (professional, trustworthy, not salesy)

Background: {{BACKGROUND}} (simple gradient or subtle pattern)
The bottom 1/5 area should be clean/predictable (text overlay area in WeChat).
No QR codes. No cluttered elements.
```

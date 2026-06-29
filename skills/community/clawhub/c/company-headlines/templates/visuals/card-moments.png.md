# 朋友圈卡片视觉模板

## 用途
轻量级朋友圈/社群分享卡片，适合人物故事、文化内容、小型快讯。

## 输出规格
- 尺寸：600×800px（竖版卡片）
- 格式：PNG
- 生成方式：image-lab (Gemini)

## 设计要素

### 布局
```
┌──────────────┐
│              │
│  [引语/金句]  │
│  大字展示     │
│              │
│  ────────    │
│              │
│  简述/故事    │
│  小字段落     │
│              │
│  ────────    │
│  公司名       │
│              │
└──────────────┘
```

### 规则
- 以金句为核心，文字为主体
- 留白多，阅读感舒适
- 适合手机屏幕直接截图转发

## 生成 Prompt 模板

```
Create a social media card (600x800) for WeChat Moments sharing.

Style: Minimalist, elegant, text-focused. Magazine editorial feel.
Color palette: {{BRAND_PRIMARY_COLOR}} as accent, mostly neutral/white background with generous whitespace.

Quote/Hook (large, prominent): "{{QUOTE}}" 
Body text (smaller, below quote): "{{BODY_TEXT}}"
Company name (bottom, subtle): "{{COMPANY_NAME}}"

A subtle decorative line or dot in {{BRAND_PRIMARY_COLOR}} separating quote from body.

Mood: {{MOOD}} (warm but professional, thoughtful)
No QR codes. No logos (text only). Clean typography.
```

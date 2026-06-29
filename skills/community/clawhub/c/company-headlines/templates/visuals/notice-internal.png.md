# 内部通知图视觉模板

## 用途
企业微信/钉钉/飞书群通知配图，内部使用。

## 输出规格
- 尺寸：750×400px（横版通知图）
- 格式：PNG
- 生成方式：image-lab (Gemini)

## 设计要素

### 布局
```
┌─────────────────────────┐
│                         │
│   [节日/事件图标]         │
│                         │
│   通知标题               │
│   (简洁直接)             │
│                         │
│   关键信息一行            │
│                         │
│        公司名 · 日期     │
└─────────────────────────┘
```

### 规则
- 信息层次简单：标题 > 关键信息 > 落款
- 温暖但不花哨
- 内部用，可以比公众号版更直接

## 生成 Prompt 模板

```
Create an internal notification image (750x400) for company messaging apps (WeCom/DingTalk).

Style: Clean, friendly, direct. Internal company communication feel.
Color palette: {{BRAND_PRIMARY_COLOR}} with warm accent.

Main message: "{{TITLE}}" (center, bold, 8-15 characters)
Key info: "{{KEY_INFO}}" (below title, smaller)
Footer: "{{COMPANY_NAME}} · {{DATE}}" (bottom-center, small)

Icon/element: A simple {{OCCASION}} icon or subtle illustration on the upper area.

Mood: {{MOOD}} (warm and direct, for internal team)
Simple, not flashy. Less is more.
```

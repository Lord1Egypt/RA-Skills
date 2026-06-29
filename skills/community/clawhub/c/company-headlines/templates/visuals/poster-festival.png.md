# 节日海报视觉模板

## 用途
节日/节气祝福的海报图，朋友圈和社群转发。

## 输出规格
- 尺寸：800×1200px（竖版海报）
- 格式：PNG
- 生成方式：image-lab (Gemini)

## 设计要素

### 布局
```
┌────────────────────┐
│                    │
│    [节日装饰元素]    │
│                    │
│    ┌──────────┐    │
│    │ 主视觉图形 │    │
│    │ (节日意象) │    │
│    └──────────┘    │
│                    │
│    主标题大字       │
│    (4-8字)         │
│                    │
│    副标题小字       │
│    (10-20字)       │
│                    │
│    公司落款         │
│                    │
└────────────────────┘
```

### 色彩
- 背景：{品牌辅色} 渐变或纯色
- 主标题：白色或深色，与背景高对比
- 装饰：{品牌主色} + 节日主题色点缀

### 字体
- 主标题：粗体，大号
- 副标题：常规，小号
- 落款：常规，小号

### 元素
- 节日相关意象（如端午：粽叶、龙舟、江水）
- 品牌色装饰线条或几何图形
- 留白充足，不拥挤

## 生成 Prompt 模板

```
Create a vertical poster (800x1200) for {{FESTIVAL_NAME}}.

Style: Clean, modern corporate aesthetic. Professional but warm.
Color palette: Primary {{BRAND_PRIMARY_COLOR}}, secondary {{BRAND_SECONDARY_COLOR}}, with subtle {{FESTIVAL_ACCENT}} accents.
Layout: Top area has subtle decorative {{FESTIVAL_MOTIF}} elements. Center has elegant typography for the main message. Bottom has company name.

Main title text: "{{HEADLINE}}" (large, bold)
Subtitle text: "{{SUBTITLE}}" (smaller, lighter weight)
Company name: "{{COMPANY_FULL_NAME}}" (bottom, small)

Mood: {{MOOD}} (e.g., warm and sincere, not overly festive)
No QR codes. No promotional text. Clean white space. Professional B2B feel.

Background: {{BACKGROUND_DESCRIPTION}}
Decorative elements: {{DECORATIVE_ELEMENTS}}
```

# 设计系统：Airtable

## 1. 视觉主题与氛围

Airtable 的网站是一个干净、企业友好的平台，通过白色画布配深海军蓝文本（`#181d26`）和 Airtable Blue（`#1b61c9`）作为主要交互强调色，传达"精致的简约"。Haas 字体家族（display + text 变体）创造了具有全程正字间距的瑞士精度排版系统。

**关键特征：**
- 白色画布配深海军蓝文本（`#181d26`）
- Airtable Blue（`#1b61c9`）作为主要 CTA 和链接颜色
- Haas + Haas Groot Disp 双字体系统
- 正文文本正字间距（0.08px–0.28px）
- 12px 圆角按钮，16px–32px 卡片
- 多层蓝色调阴影：`rgba(45,127,249,0.28) 0px 1px 3px`
- 语义主题令牌：`--theme_*` CSS 变量命名

## 2. 色彩调色板与角色

### 主色
- **Deep Navy**（`#181d26`）：主要文本
- **Airtable Blue**（`#1b61c9`）：CTA 按钮，链接
- **White**（`#ffffff`）：主要表面
- **Spotlight**（`rgba(249,252,255,0.97)`）：`--theme_button-text-spotlight`

### 语义色
- **Success Green**（`#006400`）：`--theme_success-text`
- **Weak Text**（`rgba(4,14,32,0.69)`）：`--theme_text-weak`
- **Secondary Active**（`rgba(7,12,20,0.82)`）：`--theme_button-text-secondary-active`

### 中性色
- **Dark Gray**（`#333333`）：次要文本
- **Mid Blue**（`#254fad`）：链接/强调蓝色变体
- **Border**（`#e0e2e6`）：卡片边框
- **Light Surface**（`#f8fafc`）：微妙表面

### 阴影
- **Blue-tinted**（`rgba(0,0,0,0.32) 0px 0px 1px, rgba(0,0,0,0.08) 0px 0px 2px, rgba(45,127,249,0.28) 0px 1px 3px, rgba(0,0,0,0.06) 0px 0px 0px 0.5px inset`）
- **Soft**（`rgba(15,48,106,0.05) 0px 0px 20px`）

## 3. 排版规则

### 字体家族
- **主要**：`Haas`，后备字体：`-apple-system, system-ui, Segoe UI, Roboto`
- **Display**：`Haas Groot Disp`，后备字体：`Haas`

### 层级

| 角色 | 字体 | 大小 | 字重 | 行高 | 字间距 |
|------|------|------|--------|-------------|----------------|
| Display Hero | Haas | 48px | 400 | 1.15 | normal |
| Display Bold | Haas Groot Disp | 48px | 900 | 1.50 | normal |
| Section Heading | Haas | 40px | 400 | 1.25 | normal |
| Sub-heading | Haas | 32px | 400–500 | 1.15–1.25 | normal |
| Card Title | Haas | 24px | 400 | 1.20–1.30 | 0.12px |
| Feature | Haas | 20px | 400 | 1.25–1.50 | 0.1px |
| Body | Haas | 18px | 400 | 1.35 | 0.18px |
| Body Medium | Haas | 16px | 500 | 1.30 | 0.08–0.16px |
| Button | Haas | 16px | 500 | 1.25–1.30 | 0.08px |
| Caption | Haas | 14px | 400–500 | 1.25–1.35 | 0.07–0.28px |

## 4. 组件样式

### 按钮
- **Primary Blue**：`#1b61c9`，白色文本，16px 24px 内边距，12px 圆角
- **White**：白色背景，`#181d26` 文本，12px 圆角，1px 白色边框
- **Cookie Consent**：`#1b61c9` 背景，2px 圆角（尖角）

### 卡片：`1px solid #e0e2e6`，16px–24px 圆角
### 输入框：标准 Haas 样式

## 5. 布局
- 间距：1–48px（8px 基础）
- 圆角：2px（小），12px（按钮），16px（卡片），24px（章节），32px（大型），50%（圆形）

## 6. 深度
- 蓝色调多层阴影系统
- 柔和环境：`rgba(15,48,106,0.05) 0px 0px 20px`

## 7. 宜与忌
### 宜：CTA 使用 Airtable Blue，Haas 配正字间距，12px 圆角按钮
### 忌：跳过正字间距，使用重阴影

## 8. 响应式行为
断点：425–1664px（23 个断点）

## 9. Agent 提示指南
- 文本：Deep Navy（`#181d26`）
- CTA：Airtable Blue（`#1b61c9`）
- 背景：White（`#ffffff`）
- 边框：`#e0e2e6`

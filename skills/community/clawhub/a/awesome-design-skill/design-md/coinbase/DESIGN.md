# 设计系统：Coinbase

## 1. 视觉主题与氛围

Coinbase 的网站是一个简洁、值得信赖的加密货币平台，通过蓝白双色调传达金融可靠性。设计使用 Coinbase Blue (`#0052ff`) —— 一种深邃、饱和的蓝色 —— 作为唯一的品牌强调色，搭配白色和近黑色表面。专有字体家族包括用于主标题的 CoinbaseDisplay、用于 UI 文本的 CoinbaseSans、用于正文阅读的 CoinbaseText 以及用于图标的 CoinbaseIcons —— 这是一个完整的四字体系统。

按钮系统使用独特的 56px 圆角打造胶囊形 CTA，悬停时过渡到较浅的蓝色 (`#578bfa`)。设计在白色内容区块和深色 (`#0a0b0d`、`#282b31`) 功能区块之间交替，营造出专业、金融级的界面。

**核心特征：**
- Coinbase Blue (`#0052ff`) 作为唯一的品牌强调色
- 四字体专有家族：Display、Sans、Text、Icons
- 56px 圆角胶囊按钮，带蓝色悬停过渡效果
- 近黑色 (`#0a0b0d`) 深色区块 + 白色浅色区块
- 展示标题使用 1.00 行高 —— 极紧凑
- 冷灰色次要表面 (`#eef0f3`)，带蓝色调
- 部分按钮标签使用 `text-transform: lowercase` —— 不寻常的设计

## 2. 色彩调色板与角色

### 主色
- **Coinbase Blue** (`#0052ff`)：主品牌色、链接、CTA 边框
- **Pure White** (`#ffffff`)：主浅色表面
- **Near Black** (`#0a0b0d`)：文本、深色区块背景
- **Cool Gray Surface** (`#eef0f3`)：次要按钮背景

### 交互色
- **Hover Blue** (`#578bfa`)：按钮悬停背景
- **Link Blue** (`#0667d0`)：次要链接颜色
- **Muted Blue** (`#5b616e`)：20% 透明度的边框颜色

### 表面色
- **Dark Card** (`#282b31`)：深色按钮/卡片背景
- **Light Surface** (`rgba(247,247,247,0.88)`)：柔和表面

## 3. 排版规则

### 字体家族
- **Display**：`CoinbaseDisplay` —— 主标题
- **UI / Sans**：`CoinbaseSans` —— 按钮、标题、导航
- **Body**：`CoinbaseText` —— 阅读文本
- **Icons**：`CoinbaseIcons` —— 图标字体

### 层级结构

| 角色 | 字体 | 尺寸 | 字重 | 行高 | 备注 |
|------|------|------|------|------|------|
| Display Hero | CoinbaseDisplay | 80px | 400 | 1.00 (紧凑) | 最大视觉冲击 |
| Display Secondary | CoinbaseDisplay | 64px | 400 | 1.00 | 次级标题 |
| Display Third | CoinbaseDisplay | 52px | 400 | 1.00 | 第三层级 |
| Section Heading | CoinbaseSans | 36px | 400 | 1.11 (紧凑) | 功能区块 |
| Card Title | CoinbaseSans | 32px | 400 | 1.13 | 卡片标题 |
| Feature Title | CoinbaseSans | 18px | 600 | 1.33 | 功能强调 |
| Body Bold | CoinbaseSans | 16px | 700 | 1.50 | 强调正文 |
| Body Semibold | CoinbaseSans | 16px | 600 | 1.25 | 按钮、导航 |
| Body | CoinbaseText | 18px | 400 | 1.56 | 标准阅读 |
| Body Small | CoinbaseText | 16px | 400 | 1.50 | 次要阅读 |
| Button | CoinbaseSans | 16px | 600 | 1.20 | +0.16px 字间距 |
| Caption | CoinbaseSans | 14px | 600–700 | 1.50 | 元数据 |
| Small | CoinbaseSans | 13px | 600 | 1.23 | 标签 |

## 4. 组件样式

### 按钮

**主要胶囊按钮（56px 圆角）**
- 背景：`#eef0f3` 或 `#282b31`
- 圆角：56px
- 边框：`1px solid` 与背景色匹配
- 悬停：`#578bfa`（浅蓝色）
- 焦点：`2px solid black` 轮廓

**完全胶囊按钮（100000px 圆角）**
- 用于实现最大程度的胶囊形状

**蓝色边框按钮**
- 边框：`1px solid #0052ff`
- 背景：透明

### 卡片与容器
- 圆角：8px–40px 范围
- 边框：`1px solid rgba(91,97,110,0.2)`

## 5. 布局原则

### 间距系统
- 基准：8px
- 刻度：1px, 3px, 4px, 5px, 6px, 8px, 10px, 12px, 15px, 16px, 20px, 24px, 25px, 32px, 48px

### 圆角刻度
- 小（4px–8px）：文章链接、小卡片
- 标准（12px–16px）：卡片、菜单
- 大（24px–32px）：功能容器
- 超大（40px）：大按钮/容器
- 胶囊（56px）：主要 CTA
- 完全（100000px）：最大胶囊形状

## 6. 深度与层次

极简阴影系统 —— 通过深色/浅色区块之间的色彩对比来营造层次感。

## 7. 设计规范

### 应该做的
- 使用 Coinbase Blue (#0052ff) 作为主要交互元素
- 为所有 CTA 按钮应用 56px 圆角
- 仅将 CoinbaseDisplay 用于主标题
- 交替使用深色 (#0a0b0d) 和白色区块

### 不应该做的
- 不要将蓝色用于装饰目的 —— 它仅具有功能性
- 不要在 CTA 上使用尖角 —— 最小 56px 圆角

## 8. 响应式行为

断点：400px, 576px, 640px, 768px, 896px, 1280px, 1440px, 1600px

## 9. Agent 提示指南

### 快速颜色参考
- 品牌：Coinbase Blue (`#0052ff`)
- 背景：White (`#ffffff`)
- 深色表面：`#0a0b0d`
- 次要表面：`#eef0f3`
- 悬停：`#578bfa`
- 文本：`#0a0b0d`

### 组件提示示例
- "创建主视觉区：白色背景。CoinbaseDisplay 80px，行高 1.00。胶囊形 CTA（#eef0f3，56px 圆角）。悬停：#578bfa。"
- "构建深色区块：#0a0b0d 背景。CoinbaseDisplay 64px 白色文本。蓝色强调链接（#0052ff）。"

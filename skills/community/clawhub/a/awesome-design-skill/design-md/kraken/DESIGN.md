# 设计系统：Kraken

## 1. 视觉主题与氛围

Kraken 的网站是一个简洁、值得信赖的加密货币交易所，以紫色作为其主导品牌色。设计基于白色背景，Kraken Purple（`#7132f5`、`#5741d8`、`#5b1ecf`）营造出独特、专业的加密货币品牌形象。专有的 Kraken-Brand 字体用于展示标题，采用粗体（700）字重和负字间距，而 Kraken-Product（以 IBM Plex Sans 作为后备字体）则作为 UI 的主力字体。

**主要特征：**
- Kraken Purple（`#7132f5`）作为主品牌色，配有更深色变体（`#5741d8`、`#5b1ecf`）
- Kraken-Brand（展示用）+ Kraken-Product（UI）双字体系统
- 近黑色（`#101114`）文字配以冷调蓝灰中性色阶
- 12px 圆角按钮（圆角但不呈药丸状）
- 微妙阴影（`rgba(0,0,0,0.03) 0px 4px 24px`）—— 若隐若现的层次感
- 绿色强调色（`#149e61`）用于正向/成功状态

## 2. 色彩配置与角色

### 主色
- **Kraken Purple**（`#7132f5`）：主要 CTA、品牌强调、链接
- **Purple Dark**（`#5741d8`）：按钮边框、描边变体
- **Purple Deep**（`#5b1ecf`）：最深紫色
- **Purple Subtle**（`rgba(133,91,251,0.16)`）：16% 透明度紫色 —— 微妙的按钮背景
- **Near Black**（`#101114`）：主要文字

### 中性色
- **Cool Gray**（`#686b82`）：主要中性色，24% 透明度用于边框
- **Silver Blue**（`#9497a9`）：次要文字、弱化元素
- **White**（`#ffffff`）：主要背景
- **Border Gray**（`#dedee5`）：分割线边框

### 语义色
- **Green**（`#149e61`）：成功/正向，16% 透明度用于徽章
- **Green Dark**（`#026b3f`）：徽章文字

## 3. 排版规则

### 字体家族
- **展示字体**：`Kraken-Brand`，后备字体：`IBM Plex Sans, Helvetica, Arial`
- **UI / 正文**：`Kraken-Product`，后备字体：`Helvetica Neue, Helvetica, Arial`

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字间距 |
|------|------|------|------|------|--------|
| 展示主标题 | Kraken-Brand | 48px | 700 | 1.17 | -1px |
| 章节标题 | Kraken-Brand | 36px | 700 | 1.22 | -0.5px |
| 副标题 | Kraken-Brand | 28px | 700 | 1.29 | -0.5px |
| 功能标题 | Kraken-Product | 22px | 600 | 1.20 | normal |
| 正文 | Kraken-Product | 16px | 400 | 1.38 | normal |
| 正文中等 | Kraken-Product | 16px | 500 | 1.38 | normal |
| 按钮 | Kraken-Product | 16px | 500–600 | 1.38 | normal |
| 说明文字 | Kraken-Product | 14px | 400–700 | 1.43–1.71 | normal |
| 小字 | Kraken-Product | 12px | 400–500 | 1.33 | normal |
| 微型字 | Kraken-Product | 7px | 500 | 1.00 | uppercase |

## 4. 组件样式

### 按钮

**主要紫色按钮**
- 背景：`#7132f5`
- 文字：`#ffffff`
- 内边距：13px 16px
- 圆角：12px

**紫色描边按钮**
- 背景：`#ffffff`
- 文字：`#5741d8`
- 边框：`1px solid #5741d8`
- 圆角：12px

**紫色浅色按钮**
- 背景：`rgba(133,91,251,0.16)`
- 文字：`#7132f5`
- 内边距：8px
- 圆角：12px

**白色按钮**
- 背景：`#ffffff`
- 文字：`#101114`
- 圆角：10px
- 阴影：`rgba(0,0,0,0.03) 0px 4px 24px`

**次要灰色按钮**
- 背景：`rgba(148,151,169,0.08)`
- 文字：`#101114`
- 圆角：12px

### 徽章
- 成功：`rgba(20,158,97,0.16)` 背景，`#026b3f` 文字，6px 圆角
- 中性：`rgba(104,107,130,0.12)` 背景，`#484b5e` 文字，8px 圆角

## 5. 布局原则

### 间距：1px, 2px, 3px, 4px, 5px, 6px, 8px, 10px, 12px, 13px, 15px, 16px, 20px, 24px, 25px
### 圆角：3px, 6px, 8px, 10px, 12px, 16px, 9999px, 50%

## 6. 深度与层次
- 微妙：`rgba(0,0,0,0.03) 0px 4px 24px`
- 极微：`rgba(16,24,40,0.04) 0px 1px 4px`

## 7. 最佳实践

### 应该
- 使用 Kraken Purple（#7132f5）作为 CTA 和链接颜色
- 所有按钮使用 12px 圆角
- 标题使用 Kraken-Brand，正文使用 Kraken-Product

### 不应
- 不要使用药丸形按钮 —— 12px 是按钮的最大圆角
- 不要使用定义色阶之外的紫色

## 8. 响应式行为
断点：375px, 425px, 640px, 768px, 1024px, 1280px, 1536px

## 9. 智能体提示指南

### 快速颜色参考
- 品牌：Kraken Purple（`#7132f5`）
- 深色变体：`#5741d8`
- 文字：Near Black（`#101114`）
- 次要文字：`#9497a9`
- 背景：White（`#ffffff`）

### 示例组件提示词
- "创建主视觉区：白色背景。Kraken-Brand 48px 字重 700，字间距 -1px。紫色 CTA（#7132f5，12px 圆角，13px 16px 内边距）。"

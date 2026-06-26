# 设计系统：Zapier

## 1. 视觉主题与氛围

Zapier 的网站散发着温暖、亲切的专业感。它摒弃了开发者工具常见的冷峻单色极简主义，采用奶油色调的画布（`#fffefb`），感觉就像未漂白的纸张——相当于数字化的井然有序的笔记本。近乎黑色的文字（`#201515`）带有淡淡的红棕色暖意，营造出比机械感更人性化的氛围。这是一个旨在让人感觉轻松而非技术性的自动化产品。

排版系统是两种截然不同风格的刻意交织。**Degular Display**——一种几何感的宽体展示字体——负责处理 56-80px 的大标题，字重为 medium（500），行高极其紧凑（0.90），创造出垂直方向压缩的标题块效果。**Inter** 则承担其他所有工作，从章节标题到正文和导航，回退字体为 Helvetica 和 Arial。**GT Alpina** 是一种优雅的细字重衬线字体，采用激进的负字间距（-1.6px 至 -1.92px），偶尔用于柔和的编辑性时刻。这三种字体系统使 Zapier 能够切换风格——从大胆有力（Degular）到清晰实用（Inter）再到精致文艺（GT Alpina）。

品牌的标志性橙色（`#ff4f00`）令人过目难忘——一种鲜艳、饱和的红橙色，恰好介于交通锥的紧迫感和日落的温暖感之间。它的使用克制而果断：主要 CTA 按钮、活动状态下的下划线和强调边框。在温暖的奶油色背景上，这种橙色创造出一种充满活力而不具侵略性的色彩关系。

**核心特征：**
- 温暖的奶油色画布（`#fffefb`）而非纯白——有机的、纸张般的温暖感
- 带红色调的近乎黑色（`#201515`）——有呼吸感的文字而非压迫感
- Degular Display 用于大标题，行高 0.90——紧凑、有力、现代
- Inter 作为所有功能排版的全局 UI 字体
- GT Alpina 用于编辑性点缀——细字重衬线字体，采用极端负字间距
- Zapier Orange（`#ff4f00`）作为单一强调色——鲜艳、温暖、克制使用
- 温暖的中性色调：边框（`#c5c0b1`）、柔和文字（`#939084`）、表面色调（`#eceae3`）
- 基于 8px 的间距系统，CTA 采用宽松的内边距（20px 24px）
- 边框优先设计：使用暖灰色 `1px solid` 边框而非阴影来定义结构

## 2. 色彩系统与角色

### 主色
- **Zapier Black**（`#201515`）：主要文字、标题、深色按钮背景。一种带红色调的温暖近黑色——绝不冷峻。
- **Cream White**（`#fffefb`）：页面背景、卡片表面、浅色按钮填充。不是纯白；黄色的温暖感是刻意为之。
- **Off-White**（`#fffdf9`）：次要背景表面，微妙的交替色调。与奶油白几乎难以区分，但创造出深度。

### 品牌强调色
- **Zapier Orange**（`#ff4f00`）：主要 CTA 按钮、活动下划线指示器、强调边框。标志性颜色——鲜艳而温暖。

### 中性色阶
- **Dark Charcoal**（`#36342e`）：次要文字、页脚文字、强分隔线的边框颜色。一种温暖的深灰棕色，有 70% 透明度变体。
- **Warm Gray**（`#939084`）：三级文字、柔和标签、时间戳样式内容。带有绿色暖调的中等灰度。
- **Sand**（`#c5c0b1`）：主要边框颜色、悬停状态背景、分隔线。Zapier 结构元素的支柱。
- **Light Sand**（`#eceae3`）：次要按钮背景、浅色边框、微妙的卡片表面。
- **Mid Warm**（`#b5b2aa`）：交替边框色调，用于特定的 span 元素。

### 交互色
- **Orange CTA**（`#ff4f00`）：主要操作按钮和活动标签下划线。
- **Dark CTA**（`#201515`）：次要深色按钮，悬停时变为 sand 状态。
- **Light CTA**（`#eceae3`）：三级/幽灵按钮，悬停时变为 sand 状态。
- **Link Default**（`#201515`）：标准链接颜色，与正文匹配。
- **Hover Underline**：链接在悬停时移除 `text-decoration: underline`（反向模式）。

### 遮罩与表面
- **Semi-transparent Dark**（`rgba(45, 45, 46, 0.5)`）：半透明按钮变体、背景遮罩类元素。
- **Pill Surface**（`#fffefb`）：带有 sand 边框的白色胶囊按钮。

### 阴影与深度
- **Inset Underline**（`rgb(255, 79, 0) 0px -4px 0px 0px inset`）：活动标签指示器——使用 inset box-shadow 的橙色下划线。
- **Hover Underline**（`rgb(197, 192, 177) 0px -4px 0px 0px inset`）：非活动标签悬停——sand 色下划线。

## 3. 排版规则

### 字体家族
- **Display**：`Degular Display`——用于大标题的宽体几何展示字体
- **Primary**：`Inter`，回退字体：`Helvetica, Arial`
- **Editorial**：`GT Alpina`——用于编辑性时刻的细字重衬线字体
- **System**：`Arial`——表单元素和系统 UI 的回退字体

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字间距 | 备注 |
|------|------|------|------|------|--------|------|
| Display Hero XL | Degular Display | 80px (5.00rem) | 500 | 0.90 (紧凑) | normal | 最大冲击力，压缩块状 |
| Display Hero | Degular Display | 56px (3.50rem) | 500 | 0.90-1.10 (紧凑) | 0-1.12px | 主要大标题 |
| Display Hero SM | Degular Display | 40px (2.50rem) | 500 | 0.90 (紧凑) | normal | 较小的大标题变体 |
| Display Button | Degular Display | 24px (1.50rem) | 600 | 1.00 (紧凑) | 1px | 大 CTA 按钮文字 |
| Section Heading | Inter | 48px (3.00rem) | 500 | 1.04 (紧凑) | normal | 主要章节标题 |
| Editorial Heading | GT Alpina | 48px (3.00rem) | 250 | normal | -1.92px | 细体编辑标题 |
| Editorial Sub | GT Alpina | 40px (2.50rem) | 300 | 1.08 (紧凑) | -1.6px | 编辑性副标题 |
| Sub-heading LG | Inter | 36px (2.25rem) | 500 | normal | -1px | 大号子章节 |
| Sub-heading | Inter | 32px (2.00rem) | 400 | 1.25 (紧凑) | normal | 标准子章节 |
| Sub-heading MD | Inter | 28px (1.75rem) | 500 | normal | normal | 中等子标题 |
| Card Title | Inter | 24px (1.50rem) | 600 | normal | -0.48px | 卡片标题 |
| Body Large | Inter | 20px (1.25rem) | 400-500 | 1.00-1.20 (紧凑) | -0.2px | 功能描述 |
| Body Emphasis | Inter | 18px (1.13rem) | 600 | 1.00 (紧凑) | normal | 强调正文 |
| Body | Inter | 16px (1.00rem) | 400-500 | 1.20-1.25 | -0.16px | 标准阅读文字 |
| Body Semibold | Inter | 16px (1.00rem) | 600 | 1.16 (紧凑) | normal | 强标签 |
| Button | Inter | 16px (1.00rem) | 600 | normal | normal | 标准按钮 |
| Button SM | Inter | 14px (0.88rem) | 600 | normal | normal | 小按钮 |
| Caption | Inter | 14px (0.88rem) | 500 | 1.25-1.43 | normal | 标签、元数据 |
| Caption Upper | Inter | 14px (0.88rem) | 600 | normal | 0.5px | 大写章节标签 |
| Micro | Inter | 12px (0.75rem) | 600 | 0.90-1.33 | 0.5px | 微小标签，常为大写 |
| Micro SM | Inter | 13px (0.81rem) | 500 | 1.00-1.54 | normal | 小号元数据文字 |

### 原则
- **三种字体系统，角色分明**：Degular Display 仅在大标题规模时吸引注意力。Inter 处理所有功能性的内容。GT Alpina 谨慎地增添编辑性温暖感。
- **压缩展示**：Degular 在 0.90 行高下创造出垂直压缩的标题块，感觉现代而富有建筑感。
- **字重作为层级信号**：Inter 使用 400（阅读）、500（导航/强调）、600（标题/CTA）。Degular 使用 500（展示）和 600（按钮）。
- **大写用于标签**：章节标签（如"01 / Colors"）和小型分类使用 `text-transform: uppercase` 配合 0.5px 字间距。
- **负字间距增添优雅**：GT Alpina 的细字重编辑标题使用 -1.6px 至 -1.92px 的字间距。

## 4. 组件样式

### 按钮

**Primary Orange**
- 背景：`#ff4f00`
- 文字：`#fffefb`
- 内边距：8px 16px
- 圆角：4px
- 边框：`1px solid #ff4f00`
- 用途：主要 CTA（"Start free with email"、"Sign up free"）

**Primary Dark**
- 背景：`#201515`
- 文字：`#fffefb`
- 内边距：20px 24px
- 圆角：8px
- 边框：`1px solid #201515`
- 悬停：背景变为 `#c5c0b1`，文字变为 `#201515`
- 用途：大型次要 CTA 按钮

**Light / Ghost**
- 背景：`#eceae3`
- 文字：`#36342e`
- 内边距：20px 24px
- 圆角：8px
- 边框：`1px solid #c5c0b1`
- 悬停：背景变为 `#c5c0b1`，文字变为 `#201515`
- 用途：三级操作、筛选按钮

**Pill Button**
- 背景：`#fffefb`
- 文字：`#36342e`
- 内边距：0px 16px
- 圆角：20px
- 边框：`1px solid #c5c0b1`
- 用途：标签式选择、筛选胶囊

**Overlay Semi-transparent**
- 背景：`rgba(45, 45, 46, 0.5)`
- 文字：`#fffefb`
- 圆角：20px
- 悬停：背景变为完全不透明 `#2d2d2e`
- 用途：视频播放按钮、悬浮操作

**Tab / Navigation (Inset Shadow)**
- 背景：transparent
- 文字：`#201515`
- 内边距：12px 16px
- 阴影：`rgb(255, 79, 0) 0px -4px 0px 0px inset`（活动橙色下划线）
- 悬停阴影：`rgb(197, 192, 177) 0px -4px 0px 0px inset`（sand 色下划线）
- 用途：水平标签导航

### 卡片与容器
- 背景：`#fffefb`
- 边框：`1px solid #c5c0b1`（温暖 sand 色边框）
- 圆角：5px（标准）、8px（特色）
- 默认无阴影——边框定义容器边界
- 悬停：边框颜色略微加深

### 输入框与表单
- 背景：`#fffefb`
- 文字：`#201515`
- 边框：`1px solid #c5c0b1`
- 圆角：5px
- 聚焦：边框颜色变为 `#ff4f00`（橙色）
- 占位符：`#939084`

### 导航
- 奶油色背景上的简洁水平导航
- Zapier logotype 左对齐，104x28px
- 链接：Inter 16px 字重 500，`#201515` 文字
- CTA：橙色按钮（"Start free with email"）
- 标签导航使用 inset box-shadow 下划线技术
- 移动端：折叠为汉堡菜单

### 图片处理
- 产品截图带有 `1px solid #c5c0b1` 边框
- 圆角：5-8px
- Dashboard/workflow 截图在功能区域突出展示
- 大标题内容背后有浅色渐变背景

### 独特组件

**Workflow Integration Cards**
- 成对显示连接的应用图标
- 应用之间有箭头或连接指示器
- Sand 色边框容器
- Inter 字重 500 用于应用名称

**Stat Counter**
- 大号展示数字使用 Inter 48px 字重 500
- 下方柔和描述使用 `#36342e`
- 用于社会证明指标

**Social Proof Icons**
- 圆形图标按钮：14px 圆角
- Sand 色边框：`1px solid #c5c0b1`
- 用于页脚的社交媒体关注链接

## 5. 布局原则

### 间距系统
- 基础单位：8px
- 刻度：1px, 4px, 6px, 8px, 10px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 56px, 64px, 72px
- CTA 按钮使用宽松内边距：大型 20px 24px，标准 8px 16px
- 章节内边距：64px-80px 垂直方向

### 网格与容器
- 最大内容宽度：约 1200px
- 大标题：居中单列，顶部大内边距
- 功能区域：2-3 列网格用于集成卡片
- 章节之间全宽 sand 色边框分隔线
- 页脚：多列深色背景（`#201515`）

### 留白理念
- **温暖的呼吸空间**：章节之间宽松的垂直间距（64px-80px），但内容区域相对紧凑——Zapier 在其奶油色画布上高效地呈现信息。
- **建筑式压缩**：Degular Display 标题在 0.90 行高下垂直压缩，与周围的开放空间形成对比。
- **章节节奏**：整体使用奶油色背景，章节之间用 sand 色边框分隔，而非背景色变化。

### 边框圆角刻度
- 紧凑（3px）：小型内联 span
- 标准（4px）：按钮（橙色 CTA）、标签、小型元素
- 内容（5px）：卡片、链接、通用容器
- 舒适（8px）：特色卡片、大按钮、标签
- 社交（14px）：社交图标按钮、胶囊类元素
- 胶囊（20px）：播放按钮、大胶囊按钮、悬浮操作

## 6. 深度与层次

| 层级 | 处理方式 | 用途 |
|------|----------|------|
| Flat (Level 0) | 无阴影 | 页面背景、文字块 |
| Bordered (Level 1) | `1px solid #c5c0b1` | 标准卡片、容器、输入框 |
| Strong Border (Level 1b) | `1px solid #36342e` | 深色分隔线、强调章节 |
| Active Tab (Level 2) | `rgb(255, 79, 0) 0px -4px 0px 0px inset` | 活动标签下划线（橙色） |
| Hover Tab (Level 2b) | `rgb(197, 192, 177) 0px -4px 0px 0px inset` | 悬停标签下划线（sand 色） |
| Focus (Accessibility) | `1px solid #ff4f00` outline | 交互元素的聚焦环 |

**阴影理念**：Zapier 刻意避免传统的阴影层次。结构几乎完全通过边框来定义——温暖 sand 色（`#c5c0b1`）边框用于标准容器，深 charcoal 色（`#36342e`）边框用于强调。唯一类似阴影的技术是用于标签下划线的 inset box-shadow，通过 `0px -4px 0px 0px inset` 阴影创建底部指示条。这种边框优先的方法使设计保持接地气、可感知，而非漂浮感。

### 装饰性深度
- 活动标签上的橙色 inset 下划线在元素底部创造视觉"重量"
- Sand 色悬停下划线提供预览状态而不引起布局偏移
- 主内容区无背景渐变——奶油色画布保持一致
- 页脚使用全深色背景（`#201515`）实现对比反转

## 7. 最佳实践

### 推荐
- Degular Display 仅用于大标题规模（40px+），行高 0.90 实现紧凑冲击力
- Inter 用于所有功能性 UI——导航、正文、按钮、标签
- 使用温暖奶油色（`#fffefb`）作为背景，从不用纯白
- 使用 `#201515` 作为文字颜色，从不用纯黑——红色的温暖感很重要
- Zapier Orange（`#ff4f00`）保留给主要 CTA 和活动状态指示器
- 使用 sand 色（`#c5c0b1`）边框作为主要结构元素，替代阴影
- 大型 CTA 使用宽松按钮内边距（20px 24px）以匹配 Zapier 宽敞的按钮风格
- 标签导航使用 inset box-shadow 下划线，而非 border-bottom
- 章节标签和微型分类使用大写配合 0.5px 字间距

### 避免
- 不要将 Degular Display 用于正文或 UI 元素——它仅用于展示
- 不要使用纯白（`#ffffff`）或纯黑（`#000000`）——Zapier 的调色板偏暖
- 不要对卡片应用 box-shadow 层次——改用边框
- 不要将 Zapier Orange 分散在 UI 各处——它保留给 CTA 和活动状态
- 不要在大型 CTA 按钮上使用紧凑内边距——Zapier 的按钮刻意宽敞
- 不要忽视温暖中性色系统——边框应为 `#c5c0b1`，而非灰色
- 不要将 GT Alpina 用于功能性 UI——它仅作为细字重的编辑性点缀
- 不要对 GT Alpina 应用正字间距——它使用激进的负字间距（-1.6px 至 -1.92px）
- 不要对主要按钮使用圆形胶囊形状（9999px）——胶囊用于标签和社交图标

## 8. 响应式行为

### 断点
| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| Mobile Small | <450px | 紧凑单列，缩小大标题文字 |
| Mobile | 450-600px | 标准移动端，堆叠布局 |
| Mobile Large | 600-640px | 轻微水平呼吸空间 |
| Tablet Small | 640-680px | 2 列网格开始 |
| Tablet | 680-768px | 卡片网格扩展 |
| Tablet Large | 768-991px | 完整卡片网格，扩展内边距 |
| Desktop Small | 991-1024px | 桌面布局开始 |
| Desktop | 1024-1280px | 完整布局，最大内容宽度 |
| Large Desktop | >1280px | 居中，宽敞边距 |

### 触控目标
- 大型 CTA 按钮：20px 24px 内边距（舒适的 60px+ 高度）
- 标准按钮：8px 16px 内边距
- 导航链接：16px 字重 500，间距充足
- 社交图标：14px 圆角圆形按钮
- 标签项：12px 16px 内边距

### 折叠策略
- 大标题：Degular 80px 展示在较小屏幕上缩放到 40-56px
- 导航：水平链接 + CTA 折叠为汉堡菜单
- 功能卡片：3 列网格到 2 列再到单列堆叠
- 集成工作流图示：保持宽高比，可能简化
- 页脚：多列深色区域折叠为堆叠
- 章节间距：64-80px 在移动端减少到 40-48px

### 图片行为
- 产品截图在所有尺寸保持 sand 色边框处理
- 集成应用图标在响应式容器内保持固定尺寸
- 大标题图示按比例缩放
- 全宽区域保持边缘到边缘的处理

## 9. Agent 提示指南

### 快速颜色参考
- 主要 CTA：Zapier Orange（`#ff4f00`）
- 背景：Cream White（`#fffefb`）
- 标题文字：Zapier Black（`#201515`）
- 正文文字：Dark Charcoal（`#36342e`）
- 边框：Sand（`#c5c0b1`）
- 次要表面：Light Sand（`#eceae3`）
- 柔和文字：Warm Gray（`#939084`）

### 组件提示示例
- "在奶油色背景（`#fffefb`）上创建一个大标题区域。标题使用 56px Degular Display 字重 500，行高 0.90，颜色 `#201515`。副标题使用 20px Inter 字重 400，行高 1.20，颜色 `#36342e`。橙色 CTA 按钮（`#ff4f00`，4px 圆角，8px 16px 内边距，白色文字）和深色按钮（`#201515`，8px 圆角，20px 24px 内边距，白色文字）。"
- "设计一张卡片：奶油色背景（`#fffefb`），`1px solid #c5c0b1` 边框，5px 圆角。标题使用 24px Inter 字重 600，字间距 -0.48px，`#201515`。正文使用 16px 字重 400，`#36342e`。无 box-shadow。"
- "构建标签导航：透明背景。Inter 16px 字重 500，`#201515` 文字。活动标签：`box-shadow: rgb(255, 79, 0) 0px -4px 0px 0px inset`。悬停：`box-shadow: rgb(197, 192, 177) 0px -4px 0px 0px inset`。内边距 12px 16px。"
- "创建导航：奶油色粘性头部（`#fffefb`）。链接使用 Inter 16px 字重 500，`#201515` 文字。橙色胶囊 CTA 'Start free with email' 右对齐（`#ff4f00`，4px 圆角，8px 16px 内边距）。"
- "设计深色背景页脚（`#201515`）。文字 `#fffefb`。链接 `#c5c0b1`，悬停变为 `#fffefb`。多列布局。社交图标为 14px 圆角圆形，带 sand 色边框。"

### 迭代指南
1. 始终使用温暖奶油色（`#fffefb`）背景，从不用纯白——温暖感定义了 Zapier
2. 边框（`1px solid #c5c0b1`）是结构支柱——避免阴影层次
3. Zapier Orange（`#ff4f00`）是唯一的强调色；其他都是温暖中性色
4. 三种字体，严格角色：Degular Display（大标题）、Inter（UI）、GT Alpina（编辑性）
5. 大型 CTA 按钮需要宽松内边距（20px 24px）——Zapier 按钮感觉宽敞
6. 标签导航使用 inset box-shadow 下划线，而非 border-bottom
7. 文字始终是温暖的：`#201515` 用于深色，`#36342e` 用于正文，`#939084` 用于柔和文字
8. 12-14px 大写标签配合 0.5px 字间距用于章节分类

# 设计系统：Airbnb

## 1. 视觉主题与氛围

Airbnb 的网站是一个温暖、以摄影为主导的市场平台，感觉就像翻阅一本旅游杂志，每一页都在邀请你预订。设计基于纯白画布（`#ffffff`），标志性的 Rausch Red（`#ff385c`）——以 Airbnb 第一个街道地址命名——作为唯一的品牌强调色。结果是一个干净、通透的画布，房源摄影、分类图标和红色 CTA 按钮是仅有的色彩来源。

排版使用 Airbnb Cereal VF——一种定制的可变字体，温暖且平易近人，圆润的末端呼应了品牌"家在四方"的理念。字体在紧凑的字重范围内运作：500（medium）用于大多数 UI，600（semibold）用于强调，700（bold）用于主要标题。标题上轻微的负字间距（-0.18px 到 -0.44px）创造了舒适、亲密的阅读体验，而非科技公司的压缩效率感。

Airbnb 的独特之处在于其基于调色板的令牌系统（`--palette-*`）和多层阴影方法。主要卡片阴影使用三层堆叠（`rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px`），创造出微妙、温暖的提升感。结合慷慨的 border-radius（8px–32px）、圆形导航控件（50%）和水平滚动的分类药丸栏，界面感觉触感强且诱人——为浏览而设计，而非命令。

**关键特征：**
- 纯白画布配 Rausch Red（`#ff385c`）作为唯一品牌强调色
- Airbnb Cereal VF——温暖、圆润末端的定制可变字体
- 基于调色板的令牌系统（`--palette-*`）实现系统性颜色管理
- 三层卡片阴影：边框环 + 柔和模糊 + 更强模糊
- 慷慨的 border-radius：8px 按钮，14px 徽章，20px 卡片，32px 大型元素
- 圆形导航控件（50% 圆角）
- 以摄影为先的房源卡片——图片是主角内容
- 近黑文本（`#222222`）——温暖，不冷淡
- Luxe Purple（`#460479`）和 Plus Magenta（`#92174d`）用于高端层级

## 2. 色彩调色板与角色

### 主品牌色
- **Rausch Red**（`#ff385c`）：`--palette-bg-primary-core`，主要 CTA，品牌强调色，激活状态
- **Deep Rausch**（`#e00b41`）：`--palette-bg-tertiary-core`，品牌红色的按压/深色变体
- **Error Red**（`#c13515`）：`--palette-text-primary-error`，浅色背景上的错误文本
- **Error Dark**（`#b32505`）：`--palette-text-secondary-error-hover`，错误悬停

### 高端层级
- **Luxe Purple**（`#460479`）：`--palette-bg-primary-luxe`，Airbnb Luxe 层级品牌
- **Plus Magenta**（`#92174d`）：`--palette-bg-primary-plus`，Airbnb Plus 层级品牌

### 文本色阶
- **Near Black**（`#222222`）：`--palette-text-primary`，主要文本——温暖，不冷淡
- **Focused Gray**（`#3f3f3f`）：`--palette-text-focused`，聚焦状态文本
- **Secondary Gray**（`#6a6a6a`）：次要文本，描述
- **Disabled**（`rgba(0,0,0,0.24)`）：`--palette-text-material-disabled`，禁用状态
- **Link Disabled**（`#929292`）：`--palette-text-link-disabled`，禁用链接

### 交互色
- **Legal Blue**（`#428bff`）：`--palette-text-legal`，法律链接，信息性
- **Border Gray**（`#c1c1c1`）：卡片和分隔线的边框颜色
- **Light Surface**（`#f2f2f2`）：圆形导航按钮，次要表面

### 表面与阴影
- **Pure White**（`#ffffff`）：页面背景，卡片表面
- **Card Shadow**（`rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px`）：三层温暖提升
- **Hover Shadow**（`rgba(0,0,0,0.08) 0px 4px 12px`）：按钮悬停提升

## 3. 排版规则

### 字体家族
- **主要**：`Airbnb Cereal VF`，后备字体：`Circular, -apple-system, system-ui, Roboto, Helvetica Neue`
- **OpenType 特性**：特定说明元素上的 `"salt"`（样式替代）

### 层级

| 角色 | 字体 | 大小 | 字重 | 行高 | 字间距 | 备注 |
|------|------|------|--------|-------------|----------------|-------|
| Section Heading | Airbnb Cereal VF | 28px (1.75rem) | 700 | 1.43 | normal | 主要标题 |
| Card Heading | Airbnb Cereal VF | 22px (1.38rem) | 600 | 1.18 (紧凑) | -0.44px | 分类/卡片标题 |
| Card Heading Medium | Airbnb Cereal VF | 22px (1.38rem) | 500 | 1.18 (紧凑) | -0.44px | 较轻变体 |
| Sub-heading | Airbnb Cereal VF | 21px (1.31rem) | 700 | 1.43 | normal | 粗体副标题 |
| Feature Title | Airbnb Cereal VF | 20px (1.25rem) | 600 | 1.20 (紧凑) | -0.18px | 特性标题 |
| UI Medium | Airbnb Cereal VF | 16px (1.00rem) | 500 | 1.25 (紧凑) | normal | 导航，强调文本 |
| UI Semibold | Airbnb Cereal VF | 16px (1.00rem) | 600 | 1.25 (紧凑) | normal | 强强调 |
| Button | Airbnb Cereal VF | 16px (1.00rem) | 500 | 1.25 (紧凑) | normal | 按钮标签 |
| Body / Link | Airbnb Cereal VF | 14px (0.88rem) | 400 | 1.43 | normal | 标准正文 |
| Body Medium | Airbnb Cereal VF | 14px (0.88rem) | 500 | 1.29 (紧凑) | normal | 中等正文 |
| Caption Salt | Airbnb Cereal VF | 14px (0.88rem) | 600 | 1.43 | normal | `"salt"` 特性 |
| Small | Airbnb Cereal VF | 13px (0.81rem) | 400 | 1.23 (紧凑) | normal | 描述 |
| Tag | Airbnb Cereal VF | 12px (0.75rem) | 400–700 | 1.33 | normal | 标签，价格 |
| Badge | Airbnb Cereal VF | 11px (0.69rem) | 600 | 1.18 (紧凑) | normal | `"salt"` 特性 |
| Micro Uppercase | Airbnb Cereal VF | 8px (0.50rem) | 700 | 1.25 (紧凑) | 0.32px | `text-transform: uppercase` |

### 原则
- **温暖字重范围**：500–700 占主导。标题不使用 300 或 400 字重——Airbnb 的字体始终至少是中等字重，创造温暖、自信的声音。
- **标题负字间距**：展示文本上 -0.18px 到 -0.44px 的字间距创造了亲密、舒适的标题，而非冷淡、压缩的标题。
- **"salt" OpenType 特性**：特定 UI 元素（徽章、说明）上的样式替代创造了微妙的字形变化，增加视觉趣味。
- **可变字体精度**：Cereal VF 支持连续字重插值，尽管设计系统使用 500、600 和 700 的离散值。

## 4. 组件样式

### 按钮

**Primary Dark**
- 背景：`#222222`（近黑，非纯黑）
- 文本：`#ffffff`
- 内边距：0px 24px
- 圆角：8px
- 悬停：通过 `var(--accent-bg-error)` 过渡到错误/品牌强调色
- 聚焦：`0 0 0 2px var(--palette-grey1000)` 环 + scale(0.92)

**Circular Nav**
- 背景：`#f2f2f2`
- 文本：`#222222`
- 圆角：50%（圆形）
- 悬停：阴影 `rgba(0,0,0,0.08) 0px 4px 12px` + translateX(50%)
- 激活：4px 白色边框环 + 聚焦阴影
- 聚焦：scale(0.92) 收缩动画

### 卡片与容器
- 背景：`#ffffff`
- 圆角：14px（徽章），20px（卡片/按钮），32px（大型）
- 阴影：`rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px`（三层）
- 房源卡片：顶部全宽摄影，下方详情
- 轮播控件：圆形 50% 按钮

### 输入框
- 搜索：`#222222` 文本
- 聚焦：`var(--palette-bg-primary-error)` 背景色调 + `0 0 0 2px` 环
- 圆角：取决于上下文（搜索栏使用药丸状圆角）

### 导航
- 白色粘性头部，搜索栏居中
- Airbnb logo（Rausch Red）左对齐
- 分类筛选药丸：搜索下方水平滚动行
- 轮播导航的圆形导航控件
- "成为房东"文本链接，头像/菜单右对齐

### 图片处理
- 房源摄影以充足高度填充卡片顶部
- 图片轮播配圆点指示器
- 图片上的心形/愿望清单图标覆盖
- 包含图片使用 8px–14px 圆角

## 5. 布局原则

### 间距系统
- 基础单位：8px
- 刻度：2px, 3px, 4px, 6px, 8px, 10px, 11px, 12px, 15px, 16px, 22px, 24px, 32px

### 网格与容器
- 全宽头部配居中搜索
- 分类药丸栏：水平可滚动行
- 房源网格：响应式多列（桌面 3–5 列）
- 全宽页脚配链接列

### 留白哲学
- **旅游杂志间距**：章节间慷慨的垂直内边距创造了悠闲的浏览节奏——你应该慢慢滚动，就像翻阅杂志。
- **摄影密度**：房源卡片相对紧密排列，但每张图片都足够大，感觉沉浸。
- **搜索栏突出**：搜索栏在头部获得最大垂直空间——找到目的地是主要操作。

### Border Radius 刻度
- 微妙（4px）：小链接
- 标准（8px）：按钮，标签，搜索元素
- 徽章（14px）：状态徽章，标签
- 卡片（20px）：特性卡片，大型按钮
- 大型（32px）：大型容器，英雄元素
- 圆形（50%）：导航控件，头像，图标

## 6. 深度与提升

| 级别 | 处理方式 | 用途 |
|-------|-----------|-----|
| Flat (Level 0) | 无阴影 | 页面背景，文本块 |
| Card (Level 1) | `rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px` | 房源卡片，搜索栏 |
| Hover (Level 2) | `rgba(0,0,0,0.08) 0px 4px 12px` | 按钮悬停，交互提升 |
| Active Focus (Level 3) | `rgb(255,255,255) 0px 0px 0px 4px` + 聚焦环 | 激活/聚焦元素 |

**阴影哲学**：Airbnb 的三层阴影系统创造了温暖、自然的提升感。第一层（`0px 0px 0px 1px` 0.02 不透明度）是超微妙的边框。第二层（`0px 2px 6px` 0.04）提供柔和的环境阴影。第三层（`0px 4px 8px` 0.1）添加主要提升。这种渐进方法创造了感觉像自然光而非 CSS 效果的阴影。

## 7. 宜与忌

### 宜
- 文本使用 `#222222`（温暖近黑）——永不使用纯 `#000000`
- Rausch Red（`#ff385c`）仅用于主要 CTA 和品牌时刻——它是唯一强调色
- Airbnb Cereal VF 使用 500–700 字重——温暖字重范围是有意为之
- 所有提升表面应用三层卡片阴影
- 使用慷慨的 border-radius：按钮 8px，卡片 20px，控件 50%
- 使用摄影作为主要视觉内容——房源以图片为先
- 标题应用负字间距（-0.18px 到 -0.44px）以创造亲密感
- 轮播/导航控件使用圆形（50%）按钮

### 忌
- 不要为文本使用纯黑（`#000000`）——始终使用 `#222222`（温暖）
- 不要将 Rausch Red 应用于背景或大表面——它仅作强调
- 不要为标题使用细字重（300, 400）——500 最低
- 不要使用重阴影（主层 >0.1 不透明度）——保持温暖和渐进
- 不要在卡片上使用尖角（0–4px）——慷慨圆角（20px+）是核心
- 不要在 Rausch/Luxe/Plus 系统之外引入额外品牌颜色
- 不要覆盖调色板令牌系统——一致使用 `--palette-*` 变量

## 8. 响应式行为

### 断点
| 名称 | 宽度 | 关键变化 |
|------|-------|-------------|
| Mobile Small | <375px | 单列，紧凑搜索 |
| Mobile | 375–550px | 标准移动房源网格 |
| Tablet Small | 550–744px | 2 列房源 |
| Tablet | 744–950px | 搜索栏扩展 |
| Desktop Small | 950–1128px | 3 列房源 |
| Desktop | 1128–1440px | 4 列网格，完整头部 |
| Large Desktop | 1440–1920px | 5 列网格 |
| Ultra-wide | >1920px | 最大网格宽度 |

*注意：Airbnb 检测到 61 个断点——观察到的最精细响应系统之一，反映了他们对每种可能屏幕尺寸布局的执着。*

### 触控目标
- 圆形导航按钮：充足的 50% 圆角尺寸
- 房源卡片：移动端全卡片点击目标
- 搜索栏：为拇指交互突出尺寸
- 分类药丸：水平滚动配慷慨内边距

### 折叠策略
- 房源网格：5 → 4 → 3 → 2 → 1 列
- 搜索：扩展栏 → 紧凑栏 → 覆盖层
- 分类药丸：所有尺寸水平滚动
- 导航：完整头部 → 移动简化版
- 地图：侧面板 → 覆盖/切换

### 图片行为
- 房源照片：移动端滑动轮播
- 响应式图片尺寸配纵横比保持
- 心形覆盖在各尺寸位置一致
- 照片质量根据视口调整

## 9. Agent 提示指南

### 快速颜色参考
- 背景：Pure White（`#ffffff`）
- 文本：Near Black（`#222222`）
- 品牌强调：Rausch Red（`#ff385c`）
- 次要文本：`#6a6a6a`
- 禁用：`rgba(0,0,0,0.24)`
- 卡片边框：`rgba(0,0,0,0.02) 0px 0px 0px 1px`
- 卡片阴影：完整三层堆叠
- 按钮表面：`#f2f2f2`

### 示例组件提示
- "创建房源卡片：白色背景，20px 圆角。三层阴影：rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px。顶部照片区域（16:10 比例），下方详情：16px Airbnb Cereal VF 字重 600 标题，14px 字重 400 描述 #6a6a6a。"
- "设计搜索栏：白色背景，完整卡片阴影，容器 32px 圆角。搜索文本 14px Cereal VF 字重 400。红色搜索按钮（#ff385c，50% 圆角，白色图标）。"
- "构建分类药丸栏：水平可滚动行。每个药丸：14px Cereal VF 字重 600，#222222 文本，激活时底部边框。圆形上一个/下一个箭头（#f2f2f2 背景，50% 圆角）。"
- "创建 CTA 按钮：#222222 背景，白色文本，8px 圆角，16px Cereal VF 字重 500，0px 24px 内边距。悬停：品牌红色强调。"
- "设计心形/愿望清单按钮：透明背景，50% 圆角，白色心形图标配深色阴影轮廓。"

### 迭代指南
1. 从白色开始——摄影提供所有颜色
2. Rausch Red（#ff385c）是唯一强调色——仅用于 CTA，少量使用
3. 近黑（#222222）用于文本——温暖感很重要
4. 三层阴影创造自然、温暖的提升——始终使用所有三层
5. 慷慨圆角：按钮 8px，卡片 20px，控件 50%
6. Cereal VF 使用 500–700 字重——任何标题不使用细字重
7. 摄影是主角——每张房源卡片以图片为先

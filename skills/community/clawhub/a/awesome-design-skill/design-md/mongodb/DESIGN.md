# 设计系统：MongoDB

## 1. 视觉主题与氛围

MongoDB 的网站是一种深林与终端体验的结合——一个根植于最深青黑色（`#001e2b`）的设计系统，既唤起数据库的密集感，又唤起森林树冠的深邃感。在这个近乎黑色的画布上，一抹醒目的霓虹绿（`#00ed64`）作为品牌强调色跃动——明亮到令人感受到电流感，又足够有机到让人感觉充满生机。这不是赛博朋克那种冰冷的霓虹，而是黑暗中生长之物的生物发光绿。

排版系统具有建筑般的雄心：MongoDB Value Serif 用于大型 hero 标题（96px），营造出编辑风格、权威的存在感——数据库公司使用衬线字体是一个大胆的选择，传达出"我们不只是一家科技公司"的信息。Euclid Circular A 承担正文和 UI 文本的重任，具有异常宽广的字重范围（300–700），而 Source Code Pro 则作为代码和标签字体，采用独特的全大写处理，具有很宽的字间距（1px–3px）。这三套字体的系统创造了一个跨越编辑优雅 → 几何专业 → 工程精度的层次结构。

MongoDB 的独特之处在于其双模式设计：一个深色的 hero/功能区世界（`#001e2b` 配霓虹绿强调色）和一个浅色内容世界（白色配青灰边框 `#b8c4c2`）。这两种模式之间的转换创造了戏剧性的对比。阴影系统使用带青色调的深色阴影（`rgba(0, 30, 43, 0.12)`），即使在浅色表面上也能保持森林深色的氛围。按钮使用药丸形状（100px–999px 圆角），配 MongoDB Green 边框（`#00684a`），整个组件系统参考了 LeafyGreen 设计系统。

**关键特征：**
- 深青黑色背景（`#001e2b`）——森林深色，而非太空深色
- 霓虹 MongoDB Green（`#00ed64`）作为唯一的品牌强调色——电流感与有机感并存
- MongoDB Value Serif 用于 hero 标题——技术规模下的编辑权威感
- Euclid Circular A 用于正文，字重 300（light）作为独特的正文字重
- Source Code Pro 配宽字距全大写（1px–3px）用于技术标签
- 青色调阴影：`rgba(0, 30, 43, 0.12)` ——阴影承载森林色彩
- 双模式：深青色 hero 区域 + 浅白色内容区域
- 药丸形按钮（100px 圆角）配绿色边框（`#00684a`）
- Link Blue（`#006cfa`）及悬停过渡至 `#3860be`

## 2. 色彩系统与角色

### 主品牌色
- **Forest Black**（`#001e2b`）：主要深色背景——最深的青黑色
- **MongoDB Green**（`#00ed64`）：主要品牌强调色——霓虹绿，用于高亮、下划线、渐变
- **Dark Green**（`#00684a`）：按钮边框、浅色上的链接文字——功能使用的柔和绿色

### 交互色
- **Action Blue**（`#006cfa`）：次要强调色——链接、交互高亮
- **Hover Blue**（`#3860be`）：所有链接悬停状态过渡到这个蓝色
- **Teal Active**（`#1eaedb`）：按钮悬停背景——明亮的青色

### 中性色阶
- **Deep Teal**（`#1c2d38`）：深色按钮背景、次要深色表面
- **Teal Gray**（`#3d4f58`）：深色表面上的深色边框
- **Dark Slate**（`#21313c`）：深色链接文字变体
- **Cool Gray**（`#5c6c75`）：深色上的柔和文字、次要按钮文字
- **Silver Teal**（`#b8c4c2`）：浅色表面上的边框、分隔线
- **Light Input**（`#e8edeb`）：深色表面上的输入文字
- **Pure White**（`#ffffff`）：浅色区域背景、深色上的按钮文字
- **Black**（`#000000`）：浅色表面上的文字、最深的元素

### 阴影
- **Forest Shadow**（`rgba(0, 30, 43, 0.12) 0px 26px 44px, rgba(0, 0, 0, 0.13) 0px 7px 13px`）：主要卡片层级——带青色调
- **Standard Shadow**（`rgba(0, 0, 0, 0.15) 0px 3px 20px`）：通用层级
- **Subtle Shadow**（`rgba(0, 0, 0, 0.1) 0px 2px 4px`）：轻微卡片浮起

## 3. 排版规则

### 字体族
- **Display Serif**：`MongoDB Value Serif` ——编辑风格 hero 标题
- **Body / UI**：`Euclid Circular A` ——几何无衬线主力字体
- **Code / Labels**：`Source Code Pro` ——等宽字体配全大写标签处理
- **Fallbacks**：`Akzidenz-Grotesk Std`（含 CJK: Noto Sans KR/SC/JP）、`Times`、`Arial`、`system-ui`

### 层级结构

| 角色 | 字体 | 尺寸 | 字重 | 行高 | 字间距 | 备注 |
|------|------|------|------|------|--------|------|
| Display Hero | MongoDB Value Serif | 96px (6.00rem) | 400 | 1.20（紧凑） | normal | 衬线权威感 |
| Display Secondary | MongoDB Value Serif | 64px (4.00rem) | 400 | 1.00（紧凑） | normal | 衬线副标题 |
| Section Heading | Euclid Circular A | 36px (2.25rem) | 500 | 1.33 | normal | 几何精度 |
| Sub-heading | Euclid Circular A | 24px (1.50rem) | 500 | 1.33 | normal | 功能标题 |
| Body Large | Euclid Circular A | 20px (1.25rem) | 400 | 1.60（宽松） | normal | 引言文字 |
| Body | Euclid Circular A | 18px (1.13rem) | 400 | 1.33 | normal | 标准正文 |
| Body Light | Euclid Circular A | 16px (1.00rem) | 300 | 1.50–2.00 | normal | 轻字重阅读文字 |
| Nav / UI | Euclid Circular A | 16px (1.00rem) | 500 | 1.00–1.88 | 0.16px | 导航、强调 |
| Body Bold | Euclid Circular A | 15px (0.94rem) | 700 | 1.50 | normal | 强强调 |
| Button | Euclid Circular A | 13.5px–16px | 500–700 | 1.00 | 0.135px–0.9px | CTA 标签 |
| Caption | Euclid Circular A | 14px (0.88rem) | 400 | 1.71（宽松） | normal | 元数据 |
| Small | Euclid Circular A | 11px (0.69rem) | 600 | 1.82（宽松） | 0.2px | 标签、注释 |
| Code Heading | Source Code Pro | 40px (2.50rem) | 400 | 1.60（宽松） | normal | 代码展示标题 |
| Code Body | Source Code Pro | 16px (1.00rem) | 400 | 1.50 | normal | 代码块 |
| Code Label | Source Code Pro | 14px (0.88rem) | 400–500 | 1.14（紧凑） | 1px–2px | `text-transform: uppercase` |
| Code Micro | Source Code Pro | 9px (0.56rem) | 600 | 2.67（宽松） | 2.5px | `text-transform: uppercase` |

### 原则
- **衬线字体体现权威**：MongoDB Value Serif 在 hero 规模下创造了科技领域罕见的编辑存在感——它传达出 MongoDB 是一家成熟的机构，而非初创公司。
- **字重 300 作为正文默认**：Euclid Circular A 使用 light（300）作为正文，创造出轻盈的阅读体验，与密集的深色背景形成对比。
- **宽字距等宽标签**：Source Code Pro 全大写配 1px–3px 字间距，创造出如同数据库字段标签的技术路标——系统化、结构化、分类清晰。
- **四档字重范围**：300（light 正文）→ 400（标准）→ 500（UI/导航）→ 700（bold CTA）——比大多数系统更宽的范围，实现精细的层次控制。

## 4. 组件样式

### 按钮

**Primary Green（深色表面）**
- 背景：`#00684a`（柔和 MongoDB green）
- 文字：`#000000`
- 圆角：50%（圆形）或 100px（药丸形）
- 边框：`1px solid #00684a`
- 阴影：`rgba(0,0,0,0.06) 0px 1px 6px`
- 悬停：缩放 1.1
- 激活：缩放 0.85

**Dark Teal Button**
- 背景：`#1c2d38`
- 文字：`#5c6c75`
- 圆角：100px（药丸形）
- 边框：`1px solid #3d4f58`
- 悬停：背景 `#1eaedb`，文字白色，translateX(5px)

**Outlined Button（浅色表面）**
- 背景：透明
- 文字：`#001e2b`
- 边框：`1px solid #b8c4c2`
- 圆角：4px–8px
- 悬停：背景着色

### 卡片与容器
- 浅色模式：白色背景配 `1px solid #b8c4c2` 边框
- 深色模式：`#001e2b` 或 `#1c2d38` 背景配 `1px solid #3d4f58`
- 圆角：16px（标准）、24px（中等）、48px（大/hero）
- 阴影：`rgba(0,30,43,0.12) 0px 26px 44px`（带森林色调）
- 图片容器：30px–32px 圆角

### 输入与表单
- 文本域：文字 `#e8edeb`，内边距 12px 12px 12px 8px
- 边框：浅色上 `1px solid #b8c4c2`，深色上 `1px solid #3d4f58`
- 输入框圆角：4px

### 导航
- 深色头部配森林黑背景
- Euclid Circular A 16px 字重 500 用于导航链接
- MongoDB logo（叶片图标 + 文字标识）左对齐
- 绿色 CTA 药丸按钮右对齐
- 带产品分类的 Mega-menu 下拉菜单

### 图片处理
- 深色背景上的 Dashboard 截图
- 截图中带绿色强调的 UI 元素
- 图片容器 30px–32px 圆角
- 产品展示使用全宽深色区域

### 独特组件

**霓虹绿强调下划线**
- `0px 2px 2px 0px solid #00ed64` ——底部 + 右边框创造强调下划线
- 用于功能标题和高亮文字
- 也有 `#006cfa`（蓝色）变体

**Source Code Label System**
- 14px 全大写 Source Code Pro 配 1px–2px 字间距
- 用作标题上方的区域类别标记
- 创造"数据库字段标签"的美学

## 5. 布局原则

### 间距系统
- 基础单位：8px
- 刻度：1px, 4px, 7px, 8px, 10px, 12px, 14px, 15px, 16px, 18px, 20px, 24px, 32px

### 网格与容器
- 最大内容宽度居中
- 深色 hero 区域配受限内容
- 下方为浅色内容区域
- 卡片网格：2–3 列
- 全宽深色页脚

### 留白理念
- **戏剧性的模式转换**：从深青色区域到白色内容的转换，通过对比而非仅仅是空间，创造了内在的视觉呼吸感。
- **宽裕的深色区域**：深色 hero 和功能区域使用额外的垂直内边距（80px+），让森林深色背景得以呼吸。
- **紧凑的浅色区域**：白色内容区域更密集，卡片网格更紧凑，垂直间距更小。

### 圆角刻度
- 最小（1px–2px）：小标签、徽章
- 微妙（4px）：输入框、小按钮
- 标准（8px）：卡片、链接
- 卡片（16px）：标准卡片、容器
- Toggle（20px）：开关元素
- 大（24px）：大面板
- 图片（30px–32px）：图片容器
- Hero（48px）：Hero 卡片
- 药丸（100px–999px）：按钮、导航药丸
- 全圆（9999px）：最大药丸形

## 6. 深度与层级

| 级别 | 处理方式 | 用途 |
|------|----------|------|
| 平面（Level 0） | 无阴影 | 默认表面 |
| 微妙（Level 1） | `rgba(0,0,0,0.1) 0px 2px 4px` | 轻微卡片浮起 |
| 标准（Level 2） | `rgba(0,0,0,0.15) 0px 3px 9px` | 标准卡片 |
| 突出（Level 3） | `rgba(0,0,0,0.15) 0px 3px 20px` | 层级面板 |
| Forest（Level 4） | `rgba(0,30,43,0.12) 0px 26px 44px, rgba(0,0,0,0.13) 0px 7px 13px` | Hero 卡片——带青色调 |

**阴影理念**：MongoDB 的阴影系统独特之处在于，主要层级阴影使用 `rgba(0, 30, 43, 0.12)` ——一种带青色调的阴影，将森林深色的品牌色彩带入深度系统。这意味着即使在白色表面上，阴影也感觉属于 MongoDB 的色彩世界，而非通用的中性黑色。

## 7. 做与不做

### 做
- 使用 `#001e2b`（forest-black）作为深色区域——而非纯黑
- 节制使用 MongoDB Green（`#00ed64`）以获得最大的电击感冲击
- 仅将 MongoDB Value Serif 用于 hero/display 标题——其他全部使用 Euclid Circular A
- 使用 Source Code Pro 全大写配宽字距（1px–3px）作为技术标签
- 使用青色调阴影（`rgba(0,30,43,0.12)`）作为主要卡片层级
- 保持深色/浅色区域的二元性——模式之间的戏剧性对比
- 使用字重 300 作为正文——light 字重是可读的声音
- 应用药丸圆角（100px）于主要操作按钮

### 不做
- 不要使用纯黑（`#000000`）作为深色背景——始终使用青黑色（`#001e2b`）
- 不要将 MongoDB Green（`#00ed64`）用于背景——它是用于文字、下划线和小高亮的强调色
- 不要使用标准灰色阴影——始终使用青色调（`rgba(0,30,43,...)`）
- 不要将衬线字体用于正文——MongoDB Value Serif 仅限 hero 使用
- 不要在 Source Code Pro 标签上使用窄字距——宽字距就是身份特征
- 不要在同一区域内混合深色和浅色区域处理
- 不要使用暖色——调色板严格为冷色（青色、绿色、蓝色）
- 不要忘记绿色强调下划线——它们是标志性的装饰元素

## 8. 响应式行为

### 断点
| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| Mobile Small | <425px | 紧凑单列 |
| Mobile | 425–768px | 标准移动端 |
| Tablet | 768–1024px | 2 列网格开始 |
| Desktop | 1024–1280px | 标准布局 |
| Large Desktop | 1280–1440px | 扩展布局 |
| Ultra-wide | >1440px | 最大宽度，宽裕边距 |

### 触控目标
- 药丸按钮配宽裕内边距
- 导航链接 16px 配充足间距
- 卡片表面作为全区域触控目标

### 折叠策略
- Hero：MongoDB Value Serif 96px → 64px → 进一步缩放
- 导航：水平 mega-menu → 汉堡菜单
- 功能卡片：多列 → 堆叠
- 深色/浅色区域在所有尺寸下保持其模式
- Source Code Pro 标签保持全大写处理

### 图片行为
- Dashboard 截图按比例缩放
- 深色区域背景保持全宽
- 图片圆角在各断点间保持

## 9. Agent Prompt 指南

### 快速色彩参考
- 深色背景：Forest Black（`#001e2b`）
- 品牌强调：MongoDB Green（`#00ed64`）
- 功能绿色：Dark Green（`#00684a`）
- 链接蓝色：Action Blue（`#006cfa`）
- 浅色上文字：Black（`#000000`）
- 深色上文字：White（`#ffffff`）或 Light Input（`#e8edeb`）
- 浅色边框：Silver Teal（`#b8c4c2`）
- 深色边框：Teal Gray（`#3d4f58`）

### 示例组件提示
- "在森林黑（#001e2b）背景上创建一个 hero。标题使用 96px MongoDB Value Serif 字重 400，行高 1.20，白色文字，'potential' 以 MongoDB Green（#00ed64）高亮。副标题使用 18px Euclid Circular A 字重 400。绿色药丸 CTA（#00684a，100px 圆角）。产品截图后有霓虹绿渐变光晕。"
- "在白色背景上设计一张卡片：1px solid #b8c4c2 边框，16px 圆角，阴影 rgba(0,30,43,0.12) 0px 26px 44px。标题使用 24px Euclid Circular A 字重 500。正文使用 16px 字重 300。标题上方使用 Source Code Pro 14px 全大写标签配 2px 字间距。"
- "构建一个深色区域：#001e2b 背景，卡片上 1px solid #3d4f58 边框。白色文字。使用底部 2px solid 边框在标题上创建 MongoDB Green（#00ed64）强调下划线。"
- "创建技术标签：Source Code Pro 14px，text-transform uppercase，letter-spacing 2px，字重 500，深色背景上 #00ed64 颜色。"
- "设计药丸按钮：#1c2d38 背景，1px solid #3d4f58 边框，100px 圆角，#5c6c75 文字。悬停：#1eaedb 背景，白色文字，translateX(5px)。"

### 迭代指南
1. 从模式决定开始：深色（#001e2b）用于 hero/功能，白色用于内容
2. MongoDB Green（#00ed64）是电击感的——每个区域使用一次以获得最大冲击
3. 衬线标题（MongoDB Value Serif）创造编辑权威感——绝不要用于正文
4. 字重 300 正文创造轻盈的阅读体验——不要默认使用 400
5. Source Code Pro 全大写配宽字距用于技术标签——数据库的声音
6. 青色调阴影让一切保持在 MongoDB 的色彩世界中

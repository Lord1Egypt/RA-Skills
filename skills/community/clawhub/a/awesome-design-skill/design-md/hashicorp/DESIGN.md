# 设计系统：HashiCorp

## 1. 视觉主题与氛围

HashiCorp 的网站将企业基础设施具象化——这是一个必须在传达云基础设施管理复杂性的同时保持亲和力的设计系统。视觉语言分为两种模式：用于信息区域的简洁白色浅色模式，以及用于 hero 区域和产品展示的戏剧性深色模式（`#15181e`、`#0d0e12`），创造出一种日/夜二元性，映射了"在明亮中构建，在黑暗中部署"的开发者工作流。

排版由定制品牌字体（HashiCorp Sans，加载为 `__hashicorpSans_96f0ca`）锚定，该字体承载着实质性的重量——字面意义上的。标题使用 600–700 的字重，配合紧凑的行高（1.17–1.19），创造出密集、权威的文本块，传达企业级自信。82px、字重 600、启用 OpenType `"kern"` 功能的 hero 标题并非装饰——这是基础设施级别的排版。

HashiCorp 的独特之处在于其多产品色彩系统。产品组合中的每个产品都有自己的品牌色——Terraform purple（`#7b42bc`）、Vault yellow（`#ffcf25`）、Waypoint teal（`#14c6cb`）、Vagrant blue（`#1868f2`）——这些颜色通过 CSS 自定义属性系统（`--mds-color-*`）作为强调色标记贯穿始终。这创造了一个设计系统中的设计系统：母品牌是黑白配蓝色点缀，而每个子产品注入自己的色彩身份。

组件系统使用 `mds`（Markdown Design System）前缀，表明了一种系统化、基于标记的方法，其中颜色、间距和状态都通过 CSS 变量管理。阴影极其微妙——使用 `rgba(97, 104, 117, 0.05)` 的双层微阴影，几乎不可见但提供足够的深度将交互表面与背景分离。

**关键特征：**
- 双模式：简洁的白色区域 + 戏剧性的深色（`#15181e`）hero/产品区域
- 定制 HashiCorp Sans 字体，字重 600–700，启用 `"kern"` 功能
- 通过 `--mds-color-*` CSS 自定义属性实现多产品色彩系统
- 产品品牌色：Terraform purple、Vault yellow、Waypoint teal、Vagrant blue
- 大写字母间距标题（13px，字重 600，1.3px 字母间距）
- 微阴影：0.05 透明度的双层——深度通过低语而非呐喊表达
- 基于标记的 `mds` 组件系统，使用语义化变量名
- 紧凑的圆角：2px–8px，无药丸形或圆形
- system-ui 作为次要文本的后备字体栈

## 2. 色彩调色板与角色

### 品牌主色
- **Black**（`#000000`）：主要品牌色，浅色表面上的文本，`--mds-color-hcp-brand`
- **Dark Charcoal**（`#15181e`）：深色模式背景，hero 区域
- **Near Black**（`#0d0e12`）：最深的深色模式表面，深色模式下的表单输入

### 中性色阶
- **Light Gray**（`#f1f2f3`）：浅色背景，微妙表面
- **Mid Gray**（`#d5d7db`）：边框，深色按钮文本
- **Cool Gray**（`#b2b6bd`）：边框点缀（0.1–0.4 透明度）
- **Dark Gray**（`#656a76`）：帮助文本，次要标签，`--mds-form-helper-text-color`
- **Charcoal**（`#3b3d45`）：浅色表面上的次要文本，按钮边框
- **Near White**（`#efeff1`）：深色表面上的主要文本

### 产品品牌色
- **Terraform Purple**（`#7b42bc`）：`--mds-color-terraform-button-background`
- **Vault Yellow**（`#ffcf25`）：`--mds-color-vault-button-background`
- **Waypoint Teal**（`#14c6cb`）：`--mds-color-waypoint-button-background-focus`
- **Waypoint Teal Hover**（`#12b6bb`）：`--mds-color-waypoint-button-background-hover`
- **Vagrant Blue**（`#1868f2`）：`--mds-color-vagrant-brand`
- **Purple Accent**（`#911ced`）：`--mds-color-palette-purple-300`
- **Visited Purple**（`#a737ff`）：`--mds-color-foreground-action-visited`

### 语义色
- **Action Blue**（`#1060ff`）：深色模式下的主要操作链接
- **Link Blue**（`#2264d6`）：浅色模式下的主要链接
- **Bright Blue**（`#2b89ff`）：活动链接，悬停强调
- **Amber**（`#bb5a00`）：`--mds-color-palette-amber-200`，警告状态
- **Amber Light**（`#fbeabf`）：`--mds-color-palette-amber-100`，警告背景
- **Vault Faint Yellow**（`#fff9cf`）：`--mds-color-vault-radar-gradient-faint-stop`
- **Orange**（`#a9722e`）：`--mds-color-unified-core-orange-6`
- **Red**（`#731e25`）：`--mds-color-unified-core-red-7`，错误状态
- **Navy**（`#101a59`）：`--mds-color-unified-core-blue-7`

### 阴影
- **微阴影**（`rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px`）：默认卡片/按钮高度
- **焦点轮廓**：`3px solid var(--mds-color-focus-action-external)`——系统化焦点环

## 3. 排版规则

### 字体族
- **主要品牌字体**：`__hashicorpSans_96f0ca`（HashiCorp Sans），后备字体：`__hashicorpSans_Fallback_96f0ca`
- **系统 UI**：`system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial`

### 层级

| 角色 | 字体 | 大小 | 字重 | 行高 | 字母间距 | 备注 |
|------|------|------|------|------|----------|------|
| 展示级 Hero | HashiCorp Sans | 82px (5.13rem) | 600 | 1.17（紧凑） | normal | 启用 `"kern"` |
| 章节标题 | HashiCorp Sans | 52px (3.25rem) | 600 | 1.19（紧凑） | normal | 启用 `"kern"` |
| 功能标题 | HashiCorp Sans | 42px (2.63rem) | 700 | 1.19（紧凑） | -0.42px | 负字间距 |
| 子标题 | HashiCorp Sans | 34px (2.13rem) | 600–700 | 1.18（紧凑） | normal | 功能区块 |
| 卡片标题 | HashiCorp Sans | 26px (1.63rem) | 700 | 1.19（紧凑） | normal | 卡片和面板标题 |
| 小标题 | HashiCorp Sans | 19px (1.19rem) | 700 | 1.21（紧凑） | normal | 紧凑标题 |
| 正文强调 | HashiCorp Sans | 17px (1.06rem) | 600–700 | 1.18–1.35 | normal | 粗体正文 |
| 大正文 | system-ui | 20px (1.25rem) | 400–600 | 1.50 | normal | Hero 描述 |
| 正文 | system-ui | 16px (1.00rem) | 400–500 | 1.63–1.69（宽松） | normal | 标准正文 |
| 导航链接 | system-ui | 15px (0.94rem) | 500 | 1.60（宽松） | normal | 导航项 |
| 小正文 | system-ui | 14px (0.88rem) | 400–500 | 1.29–1.71 | normal | 次要内容 |
| 说明文字 | system-ui | 13px (0.81rem) | 400–500 | 1.23–1.69 | normal | 元数据，页脚链接 |
| 大写标签 | HashiCorp Sans | 13px (0.81rem) | 600 | 1.69（宽松） | 1.3px | `text-transform: uppercase` |

### 原则
- **品牌/系统分离**：HashiCorp Sans 用于标题和品牌关键文本；system-ui 用于正文、导航和功能性文本。品牌字体承载重量，system-ui 承载内容。
- **始终启用 Kern**：所有 HashiCorp Sans 文本启用 OpenType `"kern"`——字偶间距调整是不可妥协的。
- **紧凑标题**：每个标题使用 1.17–1.21 的行高，创造密集、堆叠的文本块，感觉像基础设施——坚固、承重。
- **宽松正文**：正文使用 1.50–1.69 的行高（明显宽裕），在密集标题下方创造舒适的阅读节奏。
- **大写标签作为导航指引**：13px 大写配合 1.3px 字母间距作为系统化的类别/章节标记——始终使用 HashiCorp Sans 字重 600。

## 4. 组件样式

### 按钮

**深色主按钮**
- 背景：`#15181e`
- 文本：`#d5d7db`
- 内边距：9px 9px 9px 15px（不对称，左侧更多内边距）
- 圆角：5px
- 边框：`1px solid rgba(178, 182, 189, 0.4)`
- 阴影：`rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px`
- 焦点：`3px solid var(--mds-color-focus-action-external)`
- 悬停：使用 `--mds-color-surface-interactive` 标记

**白色次按钮**
- 背景：`#ffffff`
- 文本：`#3b3d45`
- 内边距：8px 12px
- 圆角：4px
- 悬停：`--mds-color-surface-interactive` + 低阴影高度
- 焦点：`3px solid transparent` 轮廓
- 简洁、极简外观

**产品色按钮**
- Terraform：背景 `#7b42bc`
- Vault：背景 `#ffcf25`（深色文本）
- Waypoint：背景 `#14c6cb`，悬停 `#12b6bb`
- 每个产品按钮遵循相同的结构模式，但使用其品牌色

### 徽章 / 标签
- 背景：`#42225b`（深紫色）
- 文本：`#efeff1`
- 内边距：3px 7px
- 圆角：5px
- 边框：`1px solid rgb(180, 87, 255)`
- 字体：16px

### 输入框

**文本输入（深色模式）**
- 背景：`#0d0e12`
- 文本：`#efeff1`
- 边框：`1px solid rgb(97, 104, 117)`
- 内边距：11px
- 圆角：5px
- 焦点：`3px solid var(--mds-color-focus-action-external)` 轮廓

**复选框**
- 背景：`#0d0e12`
- 边框：`1px solid rgb(97, 104, 117)`
- 圆角：3px

### 链接
- **浅色模式 Action Blue**：`#2264d6`，悬停 → blue-600 变量，悬停时显示下划线
- **深色模式 Action Blue**：`#1060ff` 或 `#2b89ff`，悬停时显示下划线
- **深色模式白色**：`#ffffff`，透明下划线 → 悬停时显示可见下划线
- **浅色模式中性色**：`#3b3d45`，透明下划线 → 悬停时显示可见下划线
- **深色模式浅色**：`#efeff1`，类似的悬停模式
- 所有链接使用 `var(--wpl-blue-600)` 作为悬停颜色

### 卡片与容器
- 浅色模式：白色背景，微阴影高度
- 深色模式：`#15181e` 或更深的表面
- 圆角：卡片和容器使用 8px
- 产品展示卡片带有渐变边框或强调光效

### 导航
- 简洁的水平导航，带有 mega-menu 下拉菜单
- HashiCorp logo 左对齐
- 链接使用 system-ui 15px 字重 500
- 产品类别按生命周期管理组组织
- 页头包含"Get started"和"Contact us" CTA
- hero 区域的深色模式变体

## 5. 布局原则

### 间距系统
- 基础单位：8px
- 刻度：2px, 3px, 4px, 6px, 7px, 8px, 9px, 11px, 12px, 16px, 20px, 24px, 32px, 40px, 48px

### 网格与容器
- 最大内容宽度：约 1150px（xl 断点）
- 全宽深色 hero 区域，内容居中
- 卡片网格：2–3 列布局
- 桌面尺寸下充裕的水平内边距

### 断点
| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| 移动端小 | <375px | 紧凑单列 |
| 移动端 | 375–480px | 标准移动端 |
| 小平板 | 480–600px | 微调 |
| 平板 | 600–768px | 开始 2 列网格 |
| 小桌面 | 768–992px | 完整导航可见 |
| 桌面 | 992–1120px | 标准布局 |
| 大桌面 | 1120–1440px | 最大宽度内容 |
| 超宽 | >1440px | 居中，充裕边距 |

### 留白哲学
- **企业级呼吸空间**：各区域间充裕的垂直间距（48px–80px+）传达稳定性和严肃性。
- **密集标题，宽松正文**：紧凑行高的标题位于宽松正文上方，在每个区域的顶部创造视觉"重量"。
- **深色作为画布**：深色 hero 区域使用额外的垂直内边距，让 3D 插图和渐变有呼吸空间。

### 圆角刻度
- 最小（2px）：链接，小型内联元素
- 微妙（3px）：复选框，小型输入框
- 标准（4px）：次按钮
- 舒适（5px）：主按钮，徽章，输入框
- 卡片（8px）：卡片，容器，图片

## 6. 深度与高度

| 级别 | 处理方式 | 用途 |
|------|----------|------|
| 平面（级别 0） | 无阴影 | 默认表面，文本块 |
| 低语（级别 1） | `rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px` | 卡片，按钮，交互表面 |
| 焦点（级别 2） | `3px solid var(--mds-color-focus-action-external)` 轮廓 | 焦点环——颜色与上下文匹配 |

**阴影哲学**：HashiCorp 使用可以说是现代网页设计中最微妙的阴影系统。5% 透明度的双层阴影几乎不可见——它们的存在不是为了创造视觉深度，而是为了标识交互性。如果你能看到阴影，那就太强了。这种克制传达了稳定性的企业价值——没有漂浮，没有不确定。

## 7. 做与不做

### 做
- 标题和品牌文本使用 HashiCorp Sans，正文和 UI 文本使用 system-ui
- 在所有 HashiCorp Sans 文本上启用 `"kern"`
- 仅在各自产品的上下文中使用产品品牌色（Terraform = purple，Vault = yellow 等）
- 章节标记使用 13px 字重 600 配合 1.3px 字母间距的大写标签
- 将阴影保持在"低语"级别（0.05 透明度双层）
- 使用 `--mds-color-*` 标记系统实现一致的颜色应用
- 保持紧凑标题/宽松正文的节奏（1.17–1.21 vs 1.50–1.69 行高）
- 使用 `3px solid` 焦点轮廓以确保可访问性

### 不做
- 不要在产品上下文之外使用产品品牌色（Vault 内容上不要使用 Terraform purple）
- 不要将阴影透明度提高到 0.1 以上——低语级别是有意为之
- 不要使用药丸形按钮（>8px 圆角）——锐利、最小的圆角是结构性的
- 不要跳过标题上的 `"kern"` 功能——字体需要它
- 不要将 HashiCorp Sans 用于小正文——它专为 17px+ 标题使用而设计
- 不要在同一组件中混合产品颜色——每个产品只有一种颜色
- 不要使用纯黑色（`#000000`）作为深色背景——使用 `#15181e` 或 `#0d0e12`
- 不要忘记不对称的按钮内边距——9px 9px 9px 15px 是有意为之

## 8. 响应式行为

### 断点
| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| 移动端 | <768px | 单列，汉堡导航，堆叠 CTA |
| 平板 | 768–992px | 2 列网格，导航开始展开 |
| 桌面 | 992–1150px | 完整布局，mega-menu 导航 |
| 大 | >1150px | 最大宽度居中，充裕边距 |

### 折叠策略
- Hero：82px → 52px → 42px 标题大小
- 导航：mega-menu → 汉堡菜单
- 产品卡片：3 列 → 2 列 → 堆叠
- 深色区域保持全宽但压缩内边距
- 按钮：内联 → 移动端全宽堆叠

## 9. Agent 提示指南

### 快速颜色参考
- 浅色背景：`#ffffff`，`#f1f2f3`
- 深色背景：`#15181e`，`#0d0e12`
- 浅色文本：`#000000`，`#3b3d45`
- 深色文本：`#efeff1`，`#d5d7db`
- 链接：`#2264d6`（浅色），`#1060ff`（深色），`#2b89ff`（活动）
- 帮助文本：`#656a76`
- 边框：`rgba(178, 182, 189, 0.4)`，`rgb(97, 104, 117)`
- 焦点：`3px solid` 产品适当颜色

### 示例组件提示
- "在深色背景（#15181e）上创建一个 hero。标题使用 82px HashiCorp Sans 字重 600，行高 1.17，启用 kern，白色文本。副文本使用 20px system-ui 字重 400，行高 1.50，#d5d7db 文本。两个按钮：深色主按钮（#15181e，5px 圆角，9px 15px 内边距）和白色次按钮（#ffffff，4px 圆角，8px 12px 内边距）。"
- "设计一个产品卡片：白色背景，8px 圆角，rgba(97,104,117,0.05) 双层阴影。标题使用 26px HashiCorp Sans 字重 700，正文使用 16px system-ui 字重 400 行高 1.63。"
- "构建一个大写章节标签：13px HashiCorp Sans 字重 600，行高 1.69，字母间距 1.3px，text-transform uppercase，#656a76 颜色。"
- "创建一个产品特定的 CTA 按钮：Terraform → #7b42bc 背景，Vault → #ffcf25 配深色文本，Waypoint → #14c6cb。所有：5px 圆角，500 字重文本，16px system-ui。"
- "设计一个深色表单：#0d0e12 输入背景，#efeff1 文本，1px solid rgb(97,104,117) 边框，5px 圆角，11px 内边距。焦点：3px solid 强调色轮廓。"

### 迭代指南
1. 始终从模式决定开始：信息性内容使用浅色（白色），hero/产品使用深色（#15181e）
2. HashiCorp Sans 仅用于标题（17px+），其他所有内容使用 system-ui
3. 阴影处于低语级别（0.05 透明度）——如果可见，请降低
4. 产品颜色是神圣的——每个产品只拥有一种颜色
5. 焦点环始终为 3px solid，颜色与产品上下文匹配
6. 大写标签是系统化的导航指引模式——13px，600，1.3px 字间距

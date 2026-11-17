# Universal Design System — Usage Guidelines

> 这是"使用说明书"，不只是给数值，而是告诉 AI 何时用、何时不用、注意什么。
> 每次设计前必读此文件，用这些语义规则约束 L2 生成阶段。

---

## 颜色 Token 使用规范

### --color-primary（主色 #0066FF）
✅ **用于**：主操作按钮背景、当前选中状态、进度条填充、强调链接、重要图标  
❌ **不用于**：大面积背景铺色（超过 30% 视觉面积）、辅助性文字、图标默认态、装饰性边框  
⚠️ **注意**：同一屏内主色元素不超过 3 个，避免视觉疲劳；浅色背景下可用 --color-primary-surface 作为轻量化强调

### --color-primary-surface（主色浅底 #EBF0FF）
✅ **用于**：选中状态背景、focus 光晕、标签/Badge 的主色变体背景  
❌ **不用于**：正文内容区域背景、卡片背景

### --color-text-primary（#111111）
✅ **用于**：所有标题、主要正文内容、重要操作按钮文字  
❌ **不用于**：辅助说明文字、时间戳、占位符文字

### --color-text-secondary（#666666）
✅ **用于**：副标题、描述性文字、时间戳、标注、表格辅助信息  
❌ **不用于**：主要正文、标题、需要强调的内容  
⚠️ **注意**：不要在彩色背景上单独使用，对比度可能不足

### --color-text-tertiary（#999999）
✅ **用于**：最低优先级信息、占位符文字旁的说明、图表轴标签  
❌ **不用于**：需要用户阅读的正文内容

### --color-text-disabled（#AAAAAA）
✅ **用于**：禁用状态的文字和图标  
❌ **不用于**：普通辅助文字（用 --color-text-secondary）

### --color-surface（白色 / 深色模式下 #1C1C1E）
✅ **用于**：卡片背景、输入框背景、弹窗背景、页面内容区域  
❌ **不用于**：页面整体背景（用 --color-background）

### --color-background（#F5F5F5 / 深色 #000000）
✅ **用于**：页面整体背景、列表视图背景、让卡片"浮"起来的底色  
❌ **不用于**：卡片内部、内容区域

### --color-border（#E0E0E0）
✅ **用于**：卡片边框、分割线、表格边框、输入框默认边框  
❌ **不用于**：强调性分隔（用 --color-border-strong）

### --color-orange
✅ **用于**：电商促销价标签、"热门"徽标、紧急但非错误的提示、活动倒计时  
❌ **不用于**：代替 --color-warning（语义不同）、普通文字、导航元素  
⚠️ **与 warning 的区别**：warning 表示"需要注意的状态"，orange 表示"促销/活动/热度"，是营销属性而非系统状态

### --color-yellow
✅ **用于**：星级评分填充色、高亮/精选标记、置顶标签、VIP 角标  
❌ **不用于**：正文文字（对比度不足）、代替 --color-warning  
⚠️ **注意**：黄色在白色背景上对比度极低，只用于图标填充或深色背景

### --color-success / --color-warning / --color-danger
✅ **用于**：对应语义的状态展示（成功提示、警告信息、错误提示）  
❌ **不用于**：纯装饰性颜色、与语义无关的视觉强调  
⚠️ **注意**：这三个颜色不能互相替代，必须与实际状态语义对应

---

## 间距 Token 使用规范

### --spacing-xs（4px）
✅ **用于**：图标与文字间距、Badge 内横向 padding、行内元素间距  
❌ **不用于**：组件之间的间距、区块间距

### --spacing-sm（8px）
✅ **用于**：列表项内部的小间距、表单字段 label 到 input 的间距、紧凑型组件内边距  
❌ **不用于**：卡片内边距（用 --spacing-md）、区块间距

### --spacing-md（16px）⭐ 最常用
✅ **用于**：卡片内边距、表单字段垂直间距、页面横向 padding（移动端）、列表项内边距  
❌ **不用于**：页面 section 之间的间距（用 --spacing-xl 或 --spacing-2xl）

### --spacing-lg（24px）
✅ **用于**：组件之间的间距、模态框内部段落间距、桌面端紧凑布局的内边距  
❌ **不用于**：紧凑组件内部（用 --spacing-sm 或 --spacing-xs）

### --spacing-xl（32px）
✅ **用于**：页面 section 之间的间距（移动端）、卡片列表的垂直间距  
❌ **不用于**：组件内部间距

### --spacing-2xl（48px）
✅ **用于**：桌面端页面 section 之间的间距、首屏大标题下方的间距  
❌ **不用于**：移动端组件间距

---

## 圆角 Token 使用规范

### --radius-sm（4px）
✅ **用于**：Badge、Tag、小型 Tooltip、Input（小号变体）

### --radius-md（8px）⭐ 默认
✅ **用于**：按钮、输入框、小卡片、Dropdown 菜单项  
❌ **不用于**：大型卡片（用 --radius-lg）

### --radius-lg（12px）
✅ **用于**：普通卡片、列表容器、中等大小的弹窗  
❌ **不用于**：按钮（会显得臃肿）

### --radius-xl（16px）
✅ **用于**：大型卡片、底部弹出 Sheet、浮层容器

### --radius-full（9999px）
✅ **用于**：圆形头像、Chip/Pill 标签、Toggle/Switch、圆形 FAB 按钮  
❌ **不用于**：普通矩形卡片、输入框

⚠️ **一致性原则**：同一屏内同类组件（如所有卡片、所有按钮）必须使用相同的 radius 值。

---

## 阴影 Token 使用规范

### --shadow-card
✅ **用于**：默认状态的内容卡片  
层次：轻量，让卡片与背景产生轻微分离感

### --shadow-md
✅ **用于**：卡片 hover 态、Dropdown 弹出层、浮动工具栏

### --shadow-lg
✅ **用于**：Toast、小型 Popover、固定顶部 NavBar 滚动后

### --shadow-modal
✅ **用于**：全屏遮罩下的弹窗、抽屉、Alert Dialog

### --shadow-popover
✅ **用于**：无遮罩的浮层（Tooltip、右键菜单、Select 下拉）

⚠️ **层次原则**：页面 → card → hover card → dropdown → modal，层次越高阴影越深。同层不用不同深度的阴影。

---

## 边框语义规范

**核心规则：`--color-border` 和 `--color-separator` 不可混用。**

| 场景 | 正确 token | 厚度 | 错误做法 |
|------|-----------|------|---------|
| 列表行分割（list/table/settings row） | `--color-separator` | `0.5px` | ❌ `1px solid --color-border` |
| 组件轮廓（card/input/modal/panel） | `--color-border` | `1px` | ❌ `rgba(0,0,0,0.07)` |
| 选中/聚焦边框 | `--color-border-strong` 或 `--color-border-focus` | `1.5px` | — |
| 章节分组线（设置页 section 之间） | `--color-separator-strong` | `1px` | ❌ `--color-border` |

### --color-separator（rgba(0,0,0,0.07)）
✅ **用于**：list row、table row、settings row、sidebar divider 的 border-bottom
❌ **不用于**：卡片轮廓、输入框边框、模态框边框（这些需要更明显的边界感）
⚠️ **厚度**：始终用 `0.5px`，不用 `1px`。0.5px 在视网膜屏上的精度是审美的一部分

### --color-border（#E0E0E0）
✅ **用于**：Card、Input、Modal、Panel、Popover 等组件的轮廓边框
❌ **不用于**：列表行间分割（太重，会让列表产生"格子"感而不是"流动"感）
⚠️ **判断标准**：如果这条线是「区分两个独立组件」→ 用 border；如果是「同一组件内相邻行的分隔」→ 用 separator

### 分割线的视觉哲学
> 好的列表分割线，用户感受不到它存在，但移除它会感觉缺少结构。
> 如果用户会注意到这条线，它就太重了。

先用留白（增大 padding）解决分隔问题，留白解决不了再加线，加线用 separator 不用 border。

---

## 字体 Token 使用规范

### 字号层级对应关系

| Token | 场景 |
|-------|------|
| `--font-size-hero` (48px) | 首屏大标题，每屏最多出现一次 |
| `--font-size-h1` (32px) | 页面主标题，通常配合 bold 字重 |
| `--font-size-h2` (24px) | 区块标题，通常配合 semibold |
| `--font-size-h3` (20px) | 组件标题、Dialog 标题、Card 标题 |
| `--font-size-h4` (16px) | 列表项标题、NavBar 标题 |
| `--font-size-body` (16px) | 正文内容 |
| `--font-size-body-sm` (14px) | 副文本、标签文字、Form label |
| `--font-size-caption` (12px) | 时间戳、图注、辅助说明 |

⚠️ **不要跨越层级**：正文用 16px，辅助文字用 14px，不要直接从 16px 跳到 12px，层次感依赖合理的字号梯度。

### 字重使用

- `bold (700)`：页面/区块标题，强调，数据核心指标
- `semibold (600)`：组件标题、NavBar 标题、按钮文字、Tab 选中态
- `medium (500)`：次级强调、Tab 默认态、标签
- `regular (400)`：正文、副文本、说明文字

### 行高使用

- CJK 文字（中文/日文/韩文）：用 `--line-height-relaxed` (1.75)
- 英文正文：用 `--line-height-normal` (1.6)
- 标题：用 `--line-height-tight` (1.2) 或 `--line-height-snug` (1.4)

---

## 动效 Token 使用规范

### 时长

| Token | 场景 |
|-------|------|
| `--duration-fast` (150ms) | hover 态切换、focus 边框、checkbox 勾选 |
| `--duration-normal` (250ms) | 按钮点击、下拉展开、Toast 出现 |
| `--duration-slow` (400ms) | Modal 出现、Page 切换、侧边栏打开 |

### 缓动

- `--easing-default`：通用过渡（最常用）
- `--easing-enter`：元素进入（减速，显得自然落下）
- `--easing-exit`：元素退出（加速，显得快速消失）
- `--easing-spring`：弹性效果（Modal 放大、弹窗出现）

⚠️ **原则**：进入用 enter，退出用 exit，不要反用。交互反馈用 fast，内容变化用 normal，大区域变化用 slow。

---

## 关于 brand/ 自定义设计系统

如果你的品牌设计系统在 `design-system/brand/<name>/` 下，其 tokens.css 会覆盖 universal 的对应 token。  
未定义的 token 自动 fallback 到 universal。  
usage-guidelines.md 如有品牌版本，优先使用品牌版本的语义规则。

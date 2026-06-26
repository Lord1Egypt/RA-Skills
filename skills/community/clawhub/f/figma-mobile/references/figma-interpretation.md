# Figma 节点解读规则

> 由 SKILL.md 步骤 1 引用。分析 Figma 拉取结果时使用。

## 样式引用与文字尺寸

- 注意节点上的 `styleRefs` — 指向 Figma 共享样式（设计 token）。共享同一样式 ID 的节点在代码中应使用同一 token/资源
- TEXT 节点上的 `textAutoResize`：`WIDTH_AND_HEIGHT` 表示自适应（wrap）；`HEIGHT` 表示定宽增高；缺省/NONE 多为固定尺寸

## 节点语义（生成任何平台代码前应用）

- **跳过系统装饰**：StatusBar、HomeIndicator、NavigationBar 等为 iOS 示意占位，**不要**为其生成业务代码。同一位置重复节点也视为 Figma 冗余，可忽略一份
- **跳过不可见节点**：VECTOR/RECTANGLE 无填充且描边均 `visible: false`，或 `absoluteRenderBounds: null` — 多为设计残留，不渲染则忽略
- **layoutAlign=STRETCH**：子沿父自动布局交叉轴撑满 → `match_parent` 交叉轴 / `.frame(maxWidth: .infinity)`。仅在非 INHERIT 时强调
- **layoutPositioning=ABSOLUTE**：在自动布局父级内绝对定位 → 用显式 x/y 偏移约束，而非纯流式布局
- **容器 + 小图标 = 单视图**：带背景/圆角的 FRAME 包住小 VECTOR/INSTANCE → 一个 `ImageView`/`Image`，不要多层嵌套
- **VECTOR/ELLIPSE 组合 = 单张图**：同 FRAME 内多个小矢量拼成图标 → 代码里引用**一张**图，不要拆成多个 View
- **RECTANGLE 作背景**：GROUP 首子 RECTANGLE 与 GROUP 同尺寸 → 背景形，不是独立 View
- **GROUP vs FRAME**：有 `layoutMode` 的 FRAME → 结构化布局（LinearLayout、HStack 等）；无 `layoutMode` 的 GROUP → 绝对坐标，映射到 ConstraintLayout 或显式偏移
- **小数取整**：dp 取最近整数，sp 约 0.5；接近标准值（如 47.99→48dp）可吸附
- **宽度策略**：勿照搬 Figma 宽度数值，要推断意图。近全宽元素 → `match_parent` + 水平 margin；并排时区分「固定宽」（图标/头像）与「弹性」（正文），弹性侧用 `0dp`+约束。详见 `platform-xml.md`「宽度策略」

## 页面架构分析（Android XML 侧重）

- 多个 Tab 文案 → 常见 `TabLayout` + `ViewPager2`，内容在 Fragment 布局（强信号，非绝对 — 不确定则问）
- Tab 项文字颜色不一致 → 选中/未选中，用 `tabSelectedTextColor` / `tabTextColor`，不要逐 Tab 写死
- 导航栏返回/关闭 → `ImageView`（src + background），不要为简单图标再套 `FrameLayout`
- 图标+文字按钮 → 优先 `LinearLayout` + `ImageView` + `TextView`，慎用 `MaterialButton` 的 `app:icon`（部分机型表现问题）
- 列表项左侧条 + 右侧内容 → 多看几项判断等高还是独立高度
- **叠放/交错卡片** 且结构相似 → 可能是滑动/切换交互。**不要**静态拆成多个独立 View。应问用户：「是否滑动/切卡？规则是左右滑、点击切换还是自动轮播？」实现方式（自定义 View、ViewPager2、第三方等）依答案而定

### 组件变体 → 多状态代码

`INSTANCE` 带 `variantProperties` 时表示组件不同状态。

**用法：**

1. 多个 INSTANCE 同 `componentId` 但 `variantProperties` 不同（如 State=Default/Pressed/Disabled）→ 同一组件的多状态
2. 生成 **一个** `View`/Composable，用状态驱动样式，**不要**多个独立 View
3. 常见变体属性到平台映射：

| 变体属性 | Android XML | Compose | iOS |
|---|---|---|---|
| State=Default/Pressed/Disabled | `selector` + `state_pressed` / `state_enabled` | `Modifier.clickable` + 条件样式 | `UIControl` 状态 / `.disabled()` |
| State=Selected/Unselected | `state_selected` + `duplicateParentState` | `var isSelected` + 条件 | `isSelected` |
| State=Active/Inactive | `state_activated` | 布尔状态 + 条件 | 自定义状态 |
| Size=Small/Medium/Large | 同布局不同尺寸值 | 带尺寸枚举的可组合参数 | 参数化 View |
| Type=Primary/Secondary/Outline | 不同 style 资源 | 颜色/描边参数 | 不同配置 |

4. 若设计里**只**有一种状态，仍可根据 `variantProperties` 提示用户：组件另有其他状态，是否一并生成
5. Size/Type 变体 → 参数化组件（enum/sealed），避免写死魔法数

**示例 — 带 State 的按钮：**  
若仅见 `{"State": "Default"}`，但知组件还有 Pressed/Disabled：  
- XML：默认态布局 + 说明需 selector 补全状态  
- Compose：`enabled` 参数 + 条件颜色/透明度  

### Figma 样式引用 → 一致 token

节点有 `styleRefs` 时指向 Figma 共享样式。

**用法：**

1. **同一 style ID**（如相同 `styleRefs.fill`）→ 代码中 **同一** 资源/token，即使 hex 恰好相同
2. 表达设计师语义：两个文本同 `styleRefs.text` 应同一文本样式，即使字号略有出入（可能是设计不一致）
3. 有工程扫描时：尝试将样式语义与工程资源对齐（如多节点共用填充色 `#0158FF` → 可能是 `@color/primary`）
4. 生成时 **先按 styleRef 分组，再按数值**：  
   - 同 styleRef → 必须同一引用  
   - 同值不同 styleRef → 可同资源，但可注明差异  
   - 值与 styleRef 都不同 → 不同资源  

**实践：**  
不必把 Figma style ID 解析成名称（需额外 API）。把它当 **分组键**：「这 5 个 text 共用 styleRef.text = S:xxx，代码里应同一套 TextStyle」。  
若同 styleRef 但渲染值不一致，提示用户可能存在设计不一致。

## 多状态批量对比

用户给出同一页多个 Frame（不同状态）时：

1. 使用 `node src/figma-fetch.js --compare "<url1>" "<url2>"`（在 `scripts/`）得到两棵简化树 + 行级差异摘要
2. `diffLines` 标出两树间路径/值变化
3. 据差异生成状态处理：颜色 → selector/条件色；透明度 → alpha/可用性；可见性 → `View.GONE`/分支；文案 → 绑定
4. 代码后附 **状态变化摘要表**

**用法示例：**

```bash
cd scripts
node src/figma-fetch.js --compare "<url1>" "<url2>" --json
```

输出 JSON 含 `trees`、`diffLines`（过长时见 `diffTruncated`）、`depthUsed`、`autoDeepened`。以第一个 URL 对应树为基准状态，第二个为对比状态。

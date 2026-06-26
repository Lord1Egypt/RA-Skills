# XML 布局映射：Figma → Android

> 作用：把 Figma 属性映射到 Android XML。  
> 本文是 **映射表**，不是 Android 教程 —— 模型已掌握平台惯例。  
> 亦包含 **线上真实项目** 中常用的写法。

## 布局选型

| Figma 结构 | 推荐布局 |
|---|---|
| 重叠多、相对关系复杂 | **ConstraintLayout**（默认） |
| 简单纵/横排、无重叠 | `LinearLayout` |
| 子视图叠放、Z 序 | `FrameLayout` |
| 重复相似项（≥3） | `RecyclerView` + item 布局 |

## 页面级架构

以下贴近线上 Android 的 **真实结构**。生成代码时要有 **页面级** 意识，而非只堆单个 View。

### 多 Tab 页
设计出现 **多个 Tab**（≥2 个文案作导航）时：

- **高度可能** 为 `TabLayout` + `ViewPager2` —— 标准切 Tab 方案
- **不要**用纯 `TextView` 当 Tab —— 无选中态、指示器与滑动联动
- Tab 下方内容区 **常为** `ViewPager2`，每 Tab 对应独立 Fragment
- 输出：主布局（TabLayout + ViewPager2）+ 各 Fragment 布局
- **注意**：强信号非绝对；若明显是静态页上装饰性「标签」，应调整；不确定则 **追问**。

```xml
<!-- 标准 TabLayout + ViewPager2 -->
<com.google.android.material.tabs.TabLayout
    android:id="@+id/tabLayout"
    android:layout_width="0dp"
    android:layout_height="48dp"
    app:tabIndicatorColor="#0F0F0F"
    app:tabSelectedTextColor="#0F0F0F"
    app:tabTextColor="#858A99"
    app:tabGravity="center"
    app:tabMode="fixed" />

<androidx.viewpager2.widget.ViewPager2
    android:id="@+id/viewPager"
    android:layout_width="0dp"
    android:layout_height="0dp" />
```

### 导航栏 — 视为整体
导航栏（返回 + 标题，可有右侧操作）是 **一个逻辑容器**。下方主内容区应约束到 **导航栏底部**，而非栏内某个子 View。

**实现**：返回与标题放在同一容器（ConstraintLayout/Toolbar/FrameLayout），主内容用 `layout_constraintTop_toBottomOf="@id/navbar"`，避免用绝对 margin 硬算。

**间距**：Figma 里内容 y=112、导航区占 y=0~100（含状态栏示意）时，**栏底到内容顶** 的真实间距可能是 **12dp**，不是 68 或 112。需减去导航栏/示意区高度；注意 Android 状态栏在布局树外。

### 导航栏按钮
- **返回/关闭**：用 `ImageView`，可 `background` + `src` 组合
  - 圆形底：`android:background` 用圆形 shape
  - 图标：`android:src`
  - 也可能是一张整张切图 —— 不确定时一个 `ImageView` 即可
- 简单图标按钮 **不要**再套一层 `FrameLayout`

```xml
<!-- 返回：圆形底 + 图标 -->
<ImageView
    android:id="@+id/btnBack"
    android:layout_width="32dp"
    android:layout_height="32dp"
    android:background="@drawable/placeholder"
    android:src="@drawable/placeholder"
    android:scaleType="centerInside"
    android:contentDescription="返回" />
<!-- background=圆 #000000，src=白色箭头 -->
```

### 图标 + 文字按钮
`MaterialButton` 的 `app:icon` 在部分机型/主题下易出渲染问题。  
**优先** `LinearLayout` + `ImageView` + `TextView`：

```xml
<!-- 描边按钮 + 图标 -->
<LinearLayout
    android:id="@+id/btnVideo"
    android:layout_width="0dp"
    android:layout_height="40dp"
    android:orientation="horizontal"
    android:gravity="center"
    android:background="@drawable/placeholder"
    android:clickable="true"
    android:focusable="true">
    <!-- background = 圆角描边 #DCDCDC，12dp，白底 -->

    <ImageView
        android:layout_width="20dp"
        android:layout_height="20dp"
        android:src="@drawable/placeholder" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginStart="6dp"
        android:text="查看视频"
        android:textSize="15sp"
        android:textColor="#0F0F0F"
        android:textStyle="bold" />
</LinearLayout>

<!-- 实心主按钮（可无图标） -->
<TextView
    android:id="@+id/btnReport"
    android:layout_width="0dp"
    android:layout_height="40dp"
    android:gravity="center"
    android:text="查看报告"
    android:textSize="15sp"
    android:textColor="#FFFFFF"
    android:textStyle="bold"
    android:background="@drawable/placeholder" />
<!-- background = 圆角矩形 #0158FF，12dp -->
```

仅当纯文字按钮且默认样式足够时，再用 `MaterialButton`。

### 开关
- **优先** `SwitchCompat`（`androidx.appcompat.widget.SwitchCompat`），跨 API/主题更稳
- `MaterialSwitch` 在部分 Material 主题下可能显示异常
- 完全自定义外观时，`SwitchCompat` + 自定义 `thumb`/`track` 更易控

### 多状态 — 使用 selector
同一 View 有多套外观（选中/未选、可用/禁用、按下/常态）时：

- **用 `selector` drawable** 合并状态，**不要**在代码里切换多张图
- 父 View 状态通过 `android:duplicateParentState="true"` 传给子 View
- 常用：`state_selected`、`state_activated`、`state_pressed`、`state_enabled`

```xml
<!-- drawable/bg_gender_card_selector.xml -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true" android:drawable="@drawable/bg_gender_card_selected" />
    <item android:drawable="@drawable/bg_gender_card_unselected" />
</selector>

<!-- drawable/ic_check_selector.xml（可用透明度控制显隐） -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true" android:drawable="@drawable/ic_check_selected" />
    <item android:drawable="@android:color/transparent" />
</selector>
```

代码里只需 `cardFemale.setSelected(true)`，子 View 带 `duplicateParentState` 会同步。

### 卡片内部 — 优先 ConstraintLayout
卡片内多子元素需精确定位（右上图标、中部图、底部文案等）时：

- 卡片根用 `ConstraintLayout` —— 更扁、更高效
- 仅当子 View 纯粹重叠、无相对关系时才用 `FrameLayout`

### 输入框 vs 纯展示
Figma 无法区分 `EditText` 与 `TextView`，数据上都是 RECTANGLE + TEXT。

- 文案像 **占位**（「请选择生日」「请输入姓名」）且带输入框样式（边框、单行、浅色字）→ 多为 **EditText**
- **不确定时问用户** —— 功能判断无法从设计数据可靠得出
- 生成 `EditText` 时用 `android:hint`，并设合适 `android:inputType`

```xml
<!-- 输入框示例 -->
<EditText
    android:id="@+id/etNickname"
    android:layout_width="295dp"
    android:layout_height="48dp"
    android:background="@drawable/bg_input"
    android:paddingStart="12dp"
    android:hint="请输入昵称"
    android:textColorHint="#B8B8B8"
    android:textSize="15sp"
    android:textColor="#0F0F0F"
    android:inputType="text"
    android:maxLines="1" />
```

### 列表项高度对齐
列表项有 **左侧块** 与 **右侧内容** 时，结合设计数据判断：

- 多看 **几条** item：若左侧高度在各条间一致、不随右侧文案变长而变 → 多为 **等高**（顶对顶底对底或同固定高）
- 若左侧明显随内容变高 → 各自 `wrap_content`
- **以观测为准，非铁律** —— 需结合当前稿

## Figma 节点解读（Android）

以下为 **经验启发式**，须与真实节点数据核对。

### 系统组件 — 跳过
**iOS 系统装饰** 类节点不要生成 Android 代码：

- 名称含 `StatusBar`、`HomeIndicator`、`NavigationBar` 等
- 多为 Figma 占位，真机由系统处理
- 信号：屏顶/底 y 接近边缘的 INSTANCE；或 **同位置重复节点**（Figma 冗余）只保留一份

### 不可见节点 — 跳过
树里有但无像素输出的节点不生成 View：

- **VECTOR** 无填充且描边均不可见 → 等效不可见
- **`absoluteRenderBounds: null`** → 无渲染输出，跳过
- 与节点自身 `visible: false` 不同（后者已在拉取脚本侧过滤，见 `scripts/src/figma-fetch.js`）

### 容器 + 图标 = 单个 ImageView
**FRAME**（背景色 + 圆角）内仅一个 **INSTANCE/VECTOR** 小图标时：

- 代码为一个 `ImageView`，背景 + `src`
- 常见信号：外框近圆（圆角大）、内层明显更小

### VECTOR/ELLIPSE 组合 = 单张图
同一 FRAME 内多个小矢量拼成图标 → **一张** drawable，**不要**多个 View。

### RECTANGLE 作背景
GROUP **首子 RECTANGLE** 与 GROUP **同尺寸** → 背景形，映射到父容器 `android:background`。

### GROUP vs FRAME
- **FRAME 有 `layoutMode`**：自动布局 → `LinearLayout` 或 ConstraintLayout 链
- **GROUP 无 `layoutMode`**：绝对坐标 → ConstraintLayout，用相对 GROUP 原点的偏移建约束

### Tab 选中态
Tab 条多个 Text **字色不同**（如一 #0F0F0F、余 #858A99）→ 选中/未选中，用 `tabSelectedTextColor` / `tabTextColor`，不要逐 Tab 写死。

### 小数取整
布局用 dp 取整；字号 sp 可约 0.5；接近标准值（如 47.99→48dp）可吸附。

### 复杂插画 — 导出位图
含渐变、布尔运算、多层重叠的插画 → **不要**强行 Vector Drawable，应 **PNG/WebP**（2x/3x）+ `ImageView`。

### 多状态页面分析
同一页多 Frame 不同状态时：

1. 先找 **跨状态相同** 的节点（静态）
2. 再 diff **变化项**（色、字、可见性、透明度等）
3. **XML 注释** 中注明状态含义
4. 优先 **selector / alpha / 状态属性**，少用手动 `VISIBLE/GONE`
5. XML 后附 **状态变化摘要表** 供业务实现

### 禁用/可用（透明度）
两状态间 `opacity` 不同 → 可用 **disabled/enabled** 模式：`android:alpha` + `clickable`/`enabled`，不必单独 drawable。

## ConstraintLayout 子 View 尺寸

结合 **真实项目** 经验，在 ConstraintLayout 内为子 View 选型：

| 内容类型 | 宽 × 高 | 场景 |
|---|---|---|
| 文本 / 自适应 | `wrap_content` × `wrap_content` | 标签、标题默认 |
| 横向撑满 | `0dp` × `wrap_content` | Start+End 约束时 |
| 小指示图标 | `12dp` × `12dp` | 圆点、状态点 |
| 行内图标 | `20dp` × `20dp` | 与文字并排 |
| 标准操作图标 | `24dp` × `24dp` | Toolbar 等（Material 常见） |
| 中等图标 | `32dp` × `32dp` | 功能入口、导航 |
| 触控区 / 头像 | `48dp` × `48dp` | 按钮、头像（约最小触控） |
| 分割线 | `match_parent` × `1px` | 区块之间横线 |
| 全宽可滚区域 | `match_parent` × `0dp` | RecyclerView 等占满剩余 |
| 行容器定高 | `match_parent` × `44dp`~`56dp` | 设置行、列表行 |

**分割线**：普通 `View` + `background`：
```xml
<View
    android:layout_width="match_parent"
    android:layout_height="1px"
    android:background="@color/divider"
    app:layout_constraintTop_toBottomOf="@id/prevView" />
```
发线级分割线用 **1px** 而非 1dp（高 DPI 下 1dp 偏粗）。

### ImageView

图标节点一般映射为简单 `ImageView` + `src`/`srcCompat`：
```xml
<ImageView
    android:layout_width="24dp"
    android:layout_height="24dp"
    app:srcCompat="@drawable/ic_arrow_right" />
```

**默认**：多数情况只需 `src`/`srcCompat`。

**何时 `background` + `src`：**

- Figma 有实心圆/矩底托住图标 → shape `background` + 图标 `src`
- **需深色模式** → `background`（`@color/`）+ 矢量 `src` + `app:tint`（`@color/`），三色随主题，不必各做一套深浅资源
- 可点区域大于图标本身 → 外包容器或 padding

**深色模式**：若扫描/上下文表明工程支持深色，图标容器可优先「底+矢量+tint」，而非裸 `src`：
```xml
<!-- 深色友好：底 + 矢量 + tint -->
<ImageView
    android:layout_width="32dp"
    android:layout_height="32dp"
    android:background="@drawable/bg_icon_circle"
    app:srcCompat="@drawable/ic_settings"
    app:tint="@color/icon_primary" />
```
三者均引用主题色资源，深浅切换自动生效。

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="16dp">

    <TextView
        android:id="@+id/tvTitle"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="标题"
        android:textSize="17sp"
        android:textColor="#0F0F0F"
        android:textStyle="bold"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toStartOf="@id/ivArrow" />

    <ImageView
        android:id="@+id/ivArrow"
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:src="@drawable/placeholder"
        app:layout_constraintTop_toTopOf="@id/tvTitle"
        app:layout_constraintBottom_toBottomOf="@id/tvTitle"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

常用约束：**居中**（顶底同锚）、**链**、**0dp 撑满**、**Guideline**、**Barrier**。

## 自动布局映射

| Figma 属性 | XML 对应 |
|---|---|
| layoutMode: VERTICAL | 纵向 LinearLayout / ConstraintLayout 竖链 |
| layoutMode: HORIZONTAL | 横向 LinearLayout / ConstraintLayout 横链 |
| itemSpacing | 子 View 的 margin |
| padding* | 父 `android:padding` |
| primaryAxisAlignItems: CENTER | `gravity` / chain |
| counterAxisAlignItems: CENTER | `gravity` 垂直/水平居中 |
| layoutGrow: 1 | Linear 的 `layout_weight` / Constraint 的 `0dp` |
| primaryAxisSizingMode: FIXED | 固定 dp |
| counterAxisSizingMode: AUTO | `wrap_content` |

## 尺寸换算

- Figma px → Android dp（1:1）
- Figma 字号 px → Android sp（1:1）

## 宽度策略：固定 vs 弹性

Figma 设计稿通常基于 375px 宽画布。Figma 里的宽度值是**计算结果**，不是设计意图。需要反推意图来决定 Android 属性。

核心问题：**这个元素的宽度是"固定尺寸"还是"填满剩余空间"？**

### 规则 1：单个元素撑满屏幕宽度
元素宽度 + 左右偏移 ≈ 屏幕宽度（375），且左右边距对称或近似对称 → `match_parent` + `marginHorizontal`

- 例：宽 335 + 左 20 + 右 20 = 375 → `match_parent` + `marginHorizontal="20dp"`
- **经验阈值**：宽度占屏幕 >85% 且左右边距近似对称 → 优先 `match_parent` + margin
- 适配优势：不同屏幕宽度下自动拉伸

### 规则 2：并排元素中识别"弹性方"
多个元素横向排列时，判断每个元素是**固定方**还是**弹性方**：

- **固定方**：有明确视觉尺寸的元素——头像、图标、按钮、固定宽度标签等。用固定 dp 值。
- **弹性方**：宽度 = 屏幕宽 - 固定方宽度 - 各间距的元素——通常是文本、描述、内容区域。用 `0dp`（match_constraints）+ 约束填满剩余空间。

判断方法：计算 `固定方宽度 + 弹性方宽度 + 所有间距 ≈ 屏幕宽度` 是否成立。如果成立，弹性方不应写死宽度。

- 例：头像 56dp + 间距 16dp + 文本 263dp + 右边距 20dp + 左边距 20dp = 375
  → 头像是固定方（56dp），文本是弹性方
  → 文本：`layout_width="0dp"` + `constraintStart_toEndOf="@id/ivAvatar"` + `constraintEnd_toEndOf="parent"` + `marginStart="16dp"` + `marginEnd="20dp"`
- 例：标签 "姓名" 40dp + 间距 12dp + 输入框 283dp + 右边距 20dp + 左边距 20dp = 375
  → 标签固定，输入框弹性

### 规则 3：固定宽度 + 居中
元素明显比屏幕窄，且居中放置，不靠左右边缘 → 固定宽度 + 居中约束

- 例：宽 295 居中在 375 里 → `layout_width="295dp"` + `constraintStart/End` 居中
- 适用于输入框、小卡片等独立居中的元素

### RecyclerView item 宽度
- item 布局始终用 `match_parent`，宽度由 RecyclerView 本身控制
- RecyclerView 自身的宽度按上述规则判断

## 阴影

```xml
<!-- MaterialCardView 提供 elevation 阴影 -->
<com.google.android.material.card.MaterialCardView
    app:cardElevation="4dp"
    app:cardCornerRadius="12dp">
```

自定义阴影可用 `elevation` + `outlineSpotShadowColor`（API 28+）或带阴影层的 drawable。

## 渐变

```xml
<!-- 在 drawable 中定义 -->
<shape>
    <gradient
        android:startColor="#FF6B6B"
        android:endColor="#4ECDC4"
        android:angle="90" />
</shape>
```

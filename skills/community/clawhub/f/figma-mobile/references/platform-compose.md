# Compose 映射：Figma → Jetpack Compose

> 作用：把 Figma 属性映射到 Jetpack Compose 代码。  
> 本文是 **映射表**，不是 Compose 教程 —— 模型已掌握 Compose 惯例。

## 布局选型

| Figma 结构 | 推荐 Composable |
|---|---|
| 纵向堆叠 | `Column` |
| 横向堆叠 | `Row` |
| 重叠 / Z 序 | `Box` |
| 重复相似项（≥3） | `LazyColumn` / `LazyRow` |
| 带顶栏/底栏的页面 | `Scaffold` |
| 复杂相对定位 | `Box` + `Modifier.align` / `offset` |

## 自动布局映射

| Figma 属性 | Compose 对应 |
|---|---|
| layoutMode: VERTICAL | `Column` |
| layoutMode: HORIZONTAL | `Row` |
| itemSpacing | `Arrangement.spacedBy(X.dp)` |
| padding* | `Modifier.padding()` |
| primaryAxisAlignItems: CENTER | `verticalArrangement = Arrangement.Center` |
| counterAxisAlignItems: CENTER | `horizontalAlignment = Alignment.CenterHorizontally` |
| layoutGrow: 1 | `Modifier.weight(1f)` |
| primaryAxisSizingMode: FIXED | `Modifier.height` / `width(X.dp)` |
| counterAxisSizingMode: AUTO | `wrapContentWidth` / `Height` |

## 尺寸换算

- Figma px → Compose `.dp`（1:1）
- Figma 字号 px → Compose `.sp`（1:1）

## 阴影

```kotlin
// 阴影高度（Elevation）
Card(elevation = CardDefaults.cardElevation(defaultElevation = 4.dp))

// 自定义阴影（Compose 1.6+）
Modifier.shadow(
    elevation = 4.dp,
    shape = RoundedCornerShape(12.dp),
    ambientColor = Color(0x1A000000),
    spotColor = Color(0x33000000)
)
```

## 渐变

```kotlin
// 线性渐变
Modifier.background(
    Brush.linearGradient(
        colors = listOf(Color(0xFFFF6B6B), Color(0xFF4ECDC4)),
        start = Offset(0f, 0f),
        end = Offset(0f, Float.POSITIVE_INFINITY)
    )
)
```

## 分角圆角

```kotlin
RoundedCornerShape(
    topStart = 12.dp,
    topEnd = 12.dp,
    bottomEnd = 0.dp,
    bottomStart = 0.dp
)
```

## 页面级架构

以下模式贴近线上 Compose 工程的 **真实结构**。

### 多 Tab 页
当设计出现 **多个 Tab**（≥2 个文案作为导航）时：

- 顶部 Tab：`TabRow` + `HorizontalPager`（accompanist 或 foundation）
- 底部导航：`NavigationBar`
- **不要**用纯 `Text` 当 Tab —— 缺少选中态、指示器与滑动联动
- 每个 Tab 内容拆成独立 `@Composable`

```kotlin
@Composable
fun TabScreen() {
    val pagerState = rememberPagerState(pageCount = { 3 })
    val scope = rememberCoroutineScope()
    val tabs = listOf("关注", "推荐", "热榜")

    Column {
        TabRow(
            selectedTabIndex = pagerState.currentPage,
            containerColor = Color.White,
            contentColor = Color(0xFF0F0F0F),
            indicator = { tabPositions ->
                TabRowDefaults.SecondaryIndicator(
                    modifier = Modifier.tabIndicatorOffset(tabPositions[pagerState.currentPage]),
                    color = Color(0xFF0F0F0F)
                )
            }
        ) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = pagerState.currentPage == index,
                    onClick = { scope.launch { pagerState.animateScrollToPage(index) } },
                    text = {
                        Text(
                            title,
                            fontWeight = if (pagerState.currentPage == index) FontWeight.Bold else FontWeight.Normal,
                            color = if (pagerState.currentPage == index) Color(0xFF0F0F0F) else Color(0xFF858A99)
                        )
                    }
                )
            }
        }
        HorizontalPager(state = pagerState) { page ->
            when (page) {
                0 -> FollowingScreen()
                1 -> RecommendScreen()
                2 -> HotListScreen()
            }
        }
    }
}
```

### 导航栏 — 视为整体
导航栏（返回 + 标题，可有右侧操作）是 **一个逻辑容器**。

- 标准样式：`TopAppBar` / `CenterAlignedTopAppBar`
- 自定义：用单行 `Row` 承载，其下方再放主内容区

```kotlin
@Composable
fun CustomNavBar(onBack: () -> Unit, title: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        IconButton(
            onClick = onBack,
            modifier = Modifier
                .size(32.dp)
                .background(Color.Black, CircleShape)
        ) {
            Icon(
                imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                contentDescription = "返回",
                tint = Color.White,
                modifier = Modifier.size(18.dp)
            )
        }
        Spacer(Modifier.weight(1f))
        Text(title, fontSize = 17.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.weight(1f))
        Spacer(Modifier.size(32.dp)) // 平衡占位
    }
}
```

### 图标 + 文字按钮
优先在 `Button` 内用 `Row`，或可点击的 `Row`，保证图标与文字稳定排版：

```kotlin
// 描边按钮 + 图标
OutlinedButton(
    onClick = {},
    shape = RoundedCornerShape(12.dp),
    border = BorderStroke(1.dp, Color(0xFFDCDCDC)),
    modifier = Modifier.fillMaxWidth().height(40.dp)
) {
    Icon(painter = painterResource(R.drawable.ic_video), contentDescription = null, modifier = Modifier.size(20.dp))
    Spacer(Modifier.width(6.dp))
    Text("查看视频", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F0F0F))
}

// 实心主按钮
Button(
    onClick = {},
    shape = RoundedCornerShape(12.dp),
    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0158FF)),
    modifier = Modifier.fillMaxWidth().height(40.dp)
) {
    Text("查看报告", fontSize = 15.sp, fontWeight = FontWeight.Bold)
}
```

### 开关
- 使用 Material3 的 `Switch`
- 颜色用 `SwitchDefaults.colors()` 自定义

```kotlin
var checked by remember { mutableStateOf(true) }
Switch(
    checked = checked,
    onCheckedChange = { checked = it },
    colors = SwitchDefaults.colors(checkedTrackColor = Color(0xFF0158FF))
)
```

### 输入框 vs 纯展示
Figma 无法区分 `TextField` 与 `Text`，数据上都像 RECTANGLE + TEXT。

- **占位风格 + 输入态** → `TextField` / `OutlinedTextField`
- **静态展示** → `Text`
- **不确定时问用户**

```kotlin
var text by remember { mutableStateOf("") }
TextField(
    value = text,
    onValueChange = { text = it },
    placeholder = { Text("请输入昵称", color = Color(0xFFB8B8B8)) },
    modifier = Modifier.width(295.dp).height(48.dp),
    shape = RoundedCornerShape(8.dp),
    colors = TextFieldDefaults.colors(
        unfocusedContainerColor = Color.White,
        focusedContainerColor = Color.White,
        unfocusedIndicatorColor = Color.Transparent,
        focusedIndicatorColor = Color.Transparent
    ),
    textStyle = TextStyle(fontSize = 15.sp, color = Color(0xFF0F0F0F)),
    singleLine = true
)
```

## 宽度策略：固定 vs 弹性

Figma 多以 375px 画布为基准。宽度数值多为 **计算结果**，非设计意图，需反推后再写 Compose。

核心问题：**该元素是「固定宽」还是「吃掉剩余空间」？**

### 规则 1：单元素撑满屏宽
元素宽 + 左右边距 ≈ 屏宽（375），且左右对称或近似对称 → `Modifier.fillMaxWidth()` + `padding(horizontal = X.dp)`

- 例：335 + 左 20 + 右 20 = 375 → `fillMaxWidth().padding(horizontal = 20.dp)`
- **经验**：宽 > 屏宽约 85% 且左右边距对称 → 优先 `fillMaxWidth()` + padding
- 便于不同屏宽自适应

### 规则 2：并排时识别「弹性」一侧
横向多元素时，分别判断 **固定** 与 **弹性**：

- **固定侧**：头像、图标、按钮、固定宽标签等，用明确 `dp`
- **弹性侧**：宽 = 屏宽 − 各固定宽 − 间距，多为正文、描述、内容区，用 `Modifier.weight(1f)` 占满剩余

校验：`固定宽 + 弹性占位 + 间距 ≈ 屏宽`

```kotlin
// 例：头像 56dp + 间距 16dp + 文本弹性 + 左右边距 20dp = 375
Row(
    modifier = Modifier
        .fillMaxWidth()
        .padding(horizontal = 20.dp),
    horizontalArrangement = Arrangement.spacedBy(16.dp),
    verticalAlignment = Alignment.CenterVertically
) {
    Image(
        painter = painterResource(R.drawable.ic_avatar),
        contentDescription = "Avatar",
        modifier = Modifier
            .size(56.dp)
            .clip(CircleShape)
    )
    Text(
        text = "User Name",
        modifier = Modifier.weight(1f),  // 弹性侧
        fontSize = 15.sp
    )
}
```

### 规则 3：固定宽 + 居中
明显窄于屏幕且居中、不靠边 → 固定 `width` + 父级水平居中

- 例：295 居中于 375 → `Modifier.width(295.dp)` + 父级 `horizontalAlignment = CenterHorizontally`
- 常见于输入框、居中卡片

### LazyColumn 子项宽度
`LazyColumn` 内 item 默认 `Modifier.fillMaxWidth()`；`LazyColumn` 自身宽由父约束决定。

```kotlin
LazyColumn(
    modifier = Modifier.fillMaxWidth()
) {
    items(count = 20, key = { it }) { index ->
        Text(
            text = "Item $index",
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        )
    }
}
```

## 多状态视图

Compose 用 **状态** 驱动条件 UI；状态变化体现在 `Modifier` 链与子节点。

### 选中 / 未选中
用 `remember { mutableStateOf() }` + 条件 `Modifier`：

```kotlin
var isSelected by remember { mutableStateOf(false) }

Card(
    modifier = Modifier
        .fillMaxWidth()
        .height(120.dp)
        .background(
            color = if (isSelected) Color(0xFF0158FF) else Color.White,
            shape = RoundedCornerShape(12.dp)
        )
        .border(
            width = 2.dp,
            color = if (isSelected) Color(0xFF0158FF) else Color(0xFFDCDCDC),
            shape = RoundedCornerShape(12.dp)
        )
        .clickable { isSelected = !isSelected },
    colors = CardDefaults.cardColors(containerColor = Color.Transparent),
    shape = RoundedCornerShape(12.dp)
) {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = if (isSelected) "✓ Selected" else "选择",
            color = if (isSelected) Color.White else Color(0xFF858A99),
            fontSize = 16.sp,
            fontWeight = FontWeight.Bold
        )
    }
}
```

示例：性别选择卡片
```kotlin
@Composable
fun GenderSelector() {
    var selectedGender by remember { mutableStateOf<String?>(null) }
    
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        listOf("Male" to "男", "Female" to "女").forEach { (key, label) ->
            Card(
                modifier = Modifier
                    .weight(1f)
                    .height(80.dp)
                    .background(
                        color = if (selectedGender == key) Color(0xFF0158FF) else Color.White,
                        shape = RoundedCornerShape(12.dp)
                    )
                    .border(
                        width = 1.dp,
                        color = if (selectedGender == key) Color(0xFF0158FF) else Color(0xFFDCDCDC),
                        shape = RoundedCornerShape(12.dp)
                    )
                    .clickable { selectedGender = key },
                colors = CardDefaults.cardColors(containerColor = Color.Transparent)
            ) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(
                        text = label,
                        color = if (selectedGender == key) Color.White else Color(0xFF0F0F0F),
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}
```

### 禁用 / 可用（透明度）
结合 `Modifier.alpha()` 与 `.clickable(enabled = ...)`：

```kotlin
var isValid by remember { mutableStateOf(false) }

Button(
    onClick = { /* handle */ },
    enabled = isValid,
    modifier = Modifier
        .fillMaxWidth()
        .height(40.dp)
        .alpha(if (isValid) 1f else 0.3f),
    colors = ButtonDefaults.buttonColors(
        containerColor = Color(0xFF0158FF),
        disabledContainerColor = Color(0xFF0158FF)
    )
) {
    Text("提交", color = Color.White, fontWeight = FontWeight.Bold)
}
```

### 叠放 / 交错卡片
设计为 **可交互** 的叠卡（滑动、拖拽、露出下层）时，**不要**只生成静态嵌套布局：

- 向用户确认：左右滑切卡（→ `HorizontalPager`）、拖拽（→ `Modifier.pointerInput`）或仅视觉重叠？
- 按答案给模板；缺省时可按上下文推测最可能方案

```kotlin
// 可滑动切卡时用 HorizontalPager
val pagerState = rememberPagerState(pageCount = { 3 })
HorizontalPager(
    state = pagerState,
    modifier = Modifier
        .fillMaxWidth()
        .height(300.dp)
) { page ->
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("Card ${page + 1}")
        }
    }
}
```

## 深色模式

通过 `MaterialTheme` 与系统状态接入深色模式，按工程配置选型。

### 使用 MaterialTheme 色板（推荐）
若工程有 `Theme.kt`，颜色应随主题走：

```kotlin
@Composable
fun MyCard() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface,
            contentColor = MaterialTheme.colorScheme.onSurface
        )
    ) {
        Text(
            text = "Content",
            color = MaterialTheme.colorScheme.primary,
            style = MaterialTheme.typography.bodyMedium
        )
    }
}
```

### 手动判断深色
需要分支逻辑时使用 `isSystemInDarkTheme()`：

```kotlin
val isDark = isSystemInDarkTheme()
val backgroundColor = if (isDark) Color(0xFF1A1A1A) else Color.White
val textColor = if (isDark) Color.White else Color(0xFF0F0F0F)

Box(
    modifier = Modifier
        .fillMaxSize()
        .background(backgroundColor),
    contentAlignment = Alignment.Center
) {
    Text("随系统深色", color = textColor)
}
```

### 动态取色（Android 12+）
Material You 可按系统壁纸生成 `dynamicLightColorScheme` / `dynamicDarkColorScheme`：

```kotlin
@Composable
fun DynamicThemeExample() {
    val colorScheme = when {
        isSystemInDarkTheme() -> dynamicDarkColorScheme(LocalContext.current)
        else -> dynamicLightColorScheme(LocalContext.current)
    }
    
    MaterialTheme(colorScheme = colorScheme) {
        // 应用内容
    }
}
```

### 规则
- 已有 `Theme.kt` 且定义了 `colorScheme` → 颜色 **一律** 用 `MaterialTheme.colorScheme.*`
- 工程 **未** 配置深色 → **不要**擅自加深色，只出浅色稿代码
- 能用 `MaterialTheme` 时避免写死色值

## LazyColumn / LazyRow 列表项

### 基础尺寸
- 子项默认 `Modifier.fillMaxWidth()`
- 列表自身宽度在 `LazyColumn`/`LazyRow` 上设置，子项填满该宽度

### 使用 `key` 提升稳定性
列表项会增删改时，为 `items` 提供稳定 `key` 减少错误复用：

```kotlin
LazyColumn(
    modifier = Modifier.fillMaxSize()
) {
    items(
        count = items.size,
        key = { index -> items[index].id },  // 稳定 id
        contentType = { "item" }
    ) { index ->
        ListItem(
            modifier = Modifier.fillMaxWidth(),
            item = items[index]
        )
    }
}
```

### 混合类型与 `contentType`
列表含多种 cell（头、正文、尾等）时，用 `contentType` 帮助组合项正确回收：

```kotlin
data class ListSection(
    val type: String,  // header / item / footer
    val content: Any
)

LazyColumn {
    items(
        count = sections.size,
        key = { index -> sections[index].content.hashCode() },
        contentType = { index -> sections[index].type }
    ) { index ->
        val section = sections[index]
        when (section.type) {
            "header" -> HeaderItem(section.content as String)
            "item" -> RegularItem(section.content as Item)
            "footer" -> FooterItem(section.content as String)
        }
    }
}
```

### 示例：带标题的列表
```kotlin
@Composable
fun UserListWithHeader(users: List<User>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize()
    ) {
        item {
            Text(
                text = "用户列表",
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }
        items(
            count = users.size,
            key = { index -> users[index].id }
        ) { index ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp, horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Image(
                    painter = painterResource(R.drawable.ic_avatar),
                    contentDescription = "Avatar",
                    modifier = Modifier
                        .size(48.dp)
                        .clip(CircleShape)
                )
                Text(
                    text = users[index].name,
                    modifier = Modifier.weight(1f),
                    fontSize = 15.sp
                )
                Text(
                    text = users[index].status,
                    fontSize = 13.sp,
                    color = Color(0xFF858A99)
                )
            }
        }
    }
}
```

## 分割线

Material3 提供 `HorizontalDivider`，用于干净的分隔线。

### 基础用法
```kotlin
HorizontalDivider(
    thickness = 1.dp,
    color = Color(0xFFEEEEEE)
)
```

### 自定义上下间距
```kotlin
Column {
    Text("Item 1")
    HorizontalDivider(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 16.dp),
        thickness = 1.dp,
        color = Color(0xFFDCDCDC)
    )
    Text("Item 2")
}
```

### 列表项之间
在相邻 item 之间插入分割线：

```kotlin
LazyColumn {
    items(items.size) { index ->
        ListItemContent(items[index])
        if (index < items.size - 1) {
            HorizontalDivider(
                thickness = 1.dp,
                color = Color(0xFFEEEEEE),
                modifier = Modifier.padding(horizontal = 16.dp)
            )
        }
    }
}
```

## Figma 节点解读（Compose 补充）

### 容器 + 图标 = 单个 Image
**FRAME**（背景色 + 圆角）内仅一个 **INSTANCE** 或 **VECTOR** 小图标时：

- 代码里是一个 `Image`，不要多层布局
- `.background()` = 外形容器（圆/圆角矩形等）
- `painter` = 图标资源
- 常见信号：外框圆角 ≥ 尺寸一半（近圆），内层明显更小

```kotlin
// Figma：FRAME 32×32 黑底圆角 16 → 内 INSTANCE 18×18 = 一个 Image
Image(
    painter = painterResource(R.drawable.ic_arrow),
    contentDescription = "Arrow",
    modifier = Modifier
        .size(32.dp)
        .background(Color.Black, RoundedCornerShape(16.dp))
        .padding(7.dp),  // 18dp 图标在 32dp 内居中
    colorFilter = ColorFilter.tint(Color.White)
)
```

### RECTANGLE 作背景
GROUP **第一个子节点** 为与 GROUP **同尺寸** 的 RECTANGLE 时：

- 该 RECTANGLE 是背景形，不是独立 composable
- 映射为父容器的 `.background()`
- 信号：首子、宽高与 GROUP 一致

```kotlin
// Figma：GROUP 150×60 → RECTANGLE 同尺寸 #F3F3F4 圆角 8 → TEXT
Box(
    modifier = Modifier
        .width(150.dp)
        .height(60.dp)
        .background(Color(0xFFF3F3F4), RoundedCornerShape(8.dp)),
    contentAlignment = Alignment.Center
) {
    Text("Button")
}
```

### 有 layoutMode 的 FRAME vs 无 layoutMode 的 GROUP
- **FRAME 且带 `layoutMode`**：自动布局 → `Column` / `Row`
- **GROUP 且无 `layoutMode`**：坐标摆放 → `Box` + `Modifier.offset()` 或嵌套 `Box`

```kotlin
// layoutMode VERTICAL → Column
Column(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp)
) {
    Text("Item 1")
    Text("Item 2")
}

// 无 layoutMode 的 GROUP → Box + offset
Box(
    modifier = Modifier
        .width(200.dp)
        .height(200.dp)
) {
    Text(
        "Top-left text",
        modifier = Modifier.offset(x = 10.dp, y = 20.dp)
    )
    Image(
        painter = painterResource(R.drawable.ic_icon),
        contentDescription = null,
        modifier = Modifier
            .size(48.dp)
            .offset(x = 100.dp, y = 100.dp)
    )
}
```

### 数值精度
Figma 常带多余小数，Compose 中宜取整：

- **`dp`**（布局、边距）：取最近 **整数**（如 127.86→128.dp）
- **`sp`**（字号）：取最近 **0.5**（如 15.27→15.5.sp）
- **例外**：接近标准尺寸则吸附（如 47.99dp→48.dp 触控目标）

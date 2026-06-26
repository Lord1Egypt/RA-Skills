# Compose Patterns — Figma to Jetpack Compose Mapping

> Purpose: Map Figma properties to Jetpack Compose code.
> This is a **mapping reference**, not a Compose tutorial — the agent already knows Compose conventions.

## Layout Selection Guide

| Figma Structure | Recommended Composable |
|---|---|
| Vertical stack | Column |
| Horizontal stack | Row |
| Overlapping / z-stacking | Box |
| Repeating similar items (≥3) | LazyColumn / LazyRow |
| Page structure with top/bottom bars | Scaffold |
| Complex relative positioning | Box with Modifier.align / offset |

## Auto-layout Mapping

| Figma Property | Compose Equivalent |
|---|---|
| layoutMode: VERTICAL | Column |
| layoutMode: HORIZONTAL | Row |
| itemSpacing | Arrangement.spacedBy(X.dp) |
| padding* | Modifier.padding() |
| primaryAxisAlignItems: CENTER | verticalArrangement = Arrangement.Center |
| counterAxisAlignItems: CENTER | horizontalAlignment = Alignment.CenterHorizontally |
| layoutGrow: 1 | Modifier.weight(1f) |
| primaryAxisSizingMode: FIXED | Modifier.height/width(X.dp) |
| counterAxisSizingMode: AUTO | wrapContentWidth/Height |

## Size Conversion

- Figma px → Compose .dp (1:1)
- Figma font px → Compose .sp (1:1)

## Shadow Mapping

```kotlin
// Elevation shadow
Card(elevation = CardDefaults.cardElevation(defaultElevation = 4.dp))

// Custom shadow (Compose 1.6+)
Modifier.shadow(
    elevation = 4.dp,
    shape = RoundedCornerShape(12.dp),
    ambientColor = Color(0x1A000000),
    spotColor = Color(0x33000000)
)
```

## Gradient Mapping

```kotlin
// Linear gradient
Modifier.background(
    Brush.linearGradient(
        colors = listOf(Color(0xFFFF6B6B), Color(0xFF4ECDC4)),
        start = Offset(0f, 0f),
        end = Offset(0f, Float.POSITIVE_INFINITY)
    )
)
```

## Per-corner Radius

```kotlin
RoundedCornerShape(
    topStart = 12.dp,
    topEnd = 12.dp,
    bottomEnd = 0.dp,
    bottomStart = 0.dp
)
```

## Page Architecture Patterns

These patterns reflect how Android apps are **actually structured** in production with Compose.

### Multi-Tab Pages
When a design shows **multiple tabs** (≥2 text labels acting as navigation):
- Use `TabRow` + `HorizontalPager` (accompanist or foundation) for top tabs
- Use `NavigationBar` for bottom navigation
- Do NOT use plain `Text` composables for tabs — they lack selection state, indicators, and swipe support
- Each tab's content should be a separate `@Composable` function

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

### Navigation Bar — Treat as a Single Unit
The navigation bar (back button + title, possibly + right action) is **one logical container**.
- Use `TopAppBar` / `CenterAlignedTopAppBar` for standard Compose nav bars
- For custom nav bars, use `Row` as a single container, constrain content below it

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
        Spacer(Modifier.size(32.dp)) // Balance spacer
    }
}
```

### Buttons with Icon + Text
Prefer `Row` inside `Button` or a clickable `Row` for reliable icon+text buttons:

```kotlin
// Outlined button with icon
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

// Solid filled button
Button(
    onClick = {},
    shape = RoundedCornerShape(12.dp),
    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0158FF)),
    modifier = Modifier.fillMaxWidth().height(40.dp)
) {
    Text("查看报告", fontSize = 15.sp, fontWeight = FontWeight.Bold)
}
```

### Switch / Toggle
- Use `Switch` from Material3 — standard, reliable
- Custom colors via `SwitchDefaults.colors()`

```kotlin
var checked by remember { mutableStateOf(true) }
Switch(
    checked = checked,
    onCheckedChange = { checked = it },
    colors = SwitchDefaults.colors(checkedTrackColor = Color(0xFF0158FF))
)
```

### Input Fields vs Display Fields
Figma cannot distinguish between `TextField` and `Text` — both appear as RECTANGLE + TEXT.
- **Placeholder-like text** with input styling → `TextField` / `OutlinedTextField`
- **Static display text** → `Text`
- **ASK the user if unsure**

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

## Width Strategy — Fixed vs Flexible

Figma designs are typically based on a 375px canvas. Width values in Figma are **calculated results**, not design intent. Reverse-engineer the intent to decide Compose properties.

Core question: **Is this element a "fixed width" or "fill remaining space"?**

### Rule 1: Single Element Fills Screen Width
Element width + left/right offset ≈ screen width (375), and left/right margins are symmetric or near-symmetric → `Modifier.fillMaxWidth()` + `padding(horizontal = X.dp)`

- Example: width 335 + left 20 + right 20 = 375 → `Modifier.fillMaxWidth().padding(horizontal = 20.dp)`
- **Heuristic**: width >85% of screen and symmetric left/right margins → prefer `fillMaxWidth()` + padding
- Adapts automatically to different screen widths

### Rule 2: Side-by-Side Elements — Identify the Flexible Side
When multiple elements are arranged horizontally, determine each element as **fixed** or **flexible**:

- **Fixed side**: elements with clear visual dimensions — avatars, icons, buttons, fixed-width labels. Use fixed `dp` values.
- **Flexible side**: width = screen width - fixed widths - gaps. Usually text, descriptions, content areas. Use `Modifier.weight(1f)` to fill remaining space.

Validation: `fixed_width + flexible_width + all_gaps ≈ screen_width`

```kotlin
// Example: Avatar (56dp) + gap (16dp) + Text (flexible) + margin-right (20dp) + margin-left (20dp) = 375
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
        modifier = Modifier.weight(1f),  // Flexible side
        fontSize = 15.sp
    )
}
```

### Rule 3: Fixed Width + Center
Element is visibly narrower than screen and centered, not edge-aligned → fixed width + center alignment in parent

- Example: width 295 centered in 375 → `Modifier.width(295.dp)` + parent `horizontalAlignment = Alignment.CenterHorizontally`
- Common for input fields, centered cards

### LazyColumn Item Width
Items in `LazyColumn` always use `Modifier.fillMaxWidth()`. The LazyColumn's own width is determined by parent constraints.

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

## Multi-State Views

Compose uses **state** to drive conditional UI changes. Each state change affects Modifier chains and child rendering.

### Selected / Unselected State
Use `remember { mutableStateOf() }` with conditional Modifiers:

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

Example: Gender selection card
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

### Disabled / Enabled State via Alpha
Use `Modifier.alpha()` combined with `.clickable(enabled = boolean)`:

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

### Stacked / Overlapping Cards
When the design shows **stacked or overlapping cards** with interaction (swipe, drag, peek), **do NOT generate static nested layouts**. Instead:
- Ask the user about the intended interaction: swipe between cards (→ `HorizontalPager`), drag gestures (→ custom `Modifier.pointerInput()`), or just visual overlap?
- Provide a template based on the answer
- For now, suggest the most likely pattern based on context

```kotlin
// If swipeable between cards: use HorizontalPager
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

## Dark Mode Patterns

Compose integrates dark mode through `MaterialTheme` and system state. Choose the approach based on project configuration.

### Using MaterialTheme Colors (Recommended)
When the project has a `Theme.kt` file, all colors automatically follow the theme:

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

### Manual Dark Mode Detection
Use `isSystemInDarkTheme()` when you need to apply specific logic:

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
    Text("Dark mode aware", color = textColor)
}
```

### Dynamic Colors (Android 12+)
Android 12+ supports Material You dynamic colors based on system theme:

```kotlin
@Composable
fun DynamicThemeExample() {
    val colorScheme = when {
        isSystemInDarkTheme() -> dynamicDarkColorScheme(LocalContext.current)
        else -> dynamicLightColorScheme(LocalContext.current)
    }
    
    MaterialTheme(colorScheme = colorScheme) {
        // App content
    }
}
```

### Rules
- If the project already has a `Theme.kt` with `colorScheme` defined, **always use `MaterialTheme.colorScheme.*`** for colors
- If the project has **no dark mode support** configured, **do not add it** — output light-mode-only code
- Never hardcode colors when `MaterialTheme` is available

## LazyColumn / LazyRow Item Patterns

### Basic Item Sizing
- Items should use `Modifier.fillMaxWidth()` by default
- LazyColumn/LazyRow width is set on the composable itself, items fill that width

### Using `key` for Performance
When list content can change, add `key` to prevent recomposition issues:

```kotlin
LazyColumn(
    modifier = Modifier.fillMaxSize()
) {
    items(
        count = items.size,
        key = { index -> items[index].id },  // Stable identifier
        contentType = { "item" }
    ) { index ->
        ListItem(
            modifier = Modifier.fillMaxWidth(),
            item = items[index]
        )
    }
}
```

### Mixed Content Types with `contentType`
When a list mixes different item types (headers, regular items, footers), use `contentType` to help Compose recycle properly:

```kotlin
data class ListSection(
    val type: String,  // "header", "item", "footer"
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

### Example: List with Header + Items
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

## Divider Pattern

Compose Material3 provides a native `HorizontalDivider` composable. Use it for clean line separators.

### Basic Divider
```kotlin
HorizontalDivider(
    thickness = 1.dp,
    color = Color(0xFFEEEEEE)
)
```

### Divider with Custom Spacing
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

### Divider in List Items
Place dividers between list items for visual separation:

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

## Figma Node Interpretation (Compose-specific notes)

### Container + Icon = Single Image Composable
When Figma shows a **FRAME** (with background color + cornerRadius) containing a single **INSTANCE** or **VECTOR** child that is clearly an icon:
- This is one `Image` composable in code, not nested layouts
- `.background()` modifier = the container shape (circle, rounded rect, etc.)
- `painter` parameter = the icon drawable
- Typical signal: outer FRAME has cornerRadius ≥ 50% of size (circular), inner child is much smaller

```kotlin
// Figma: FRAME(32×32, #000000, cornerRadius=16) → INSTANCE(18×18) = one Image
Image(
    painter = painterResource(R.drawable.ic_arrow),
    contentDescription = "Arrow",
    modifier = Modifier
        .size(32.dp)
        .background(Color.Black, RoundedCornerShape(16.dp))
        .padding(7.dp),  // Center the 18dp icon in 32dp container
    colorFilter = ColorFilter.tint(Color.White)
)
```

### RECTANGLE as Background
When a GROUP's **first child** is a RECTANGLE with the **same dimensions** as the GROUP:
- The RECTANGLE is a background shape, not an independent composable
- Map it to `.background()` modifier on the parent container
- Signal: RECTANGLE is first child, width≈GROUP width, height≈GROUP height

```kotlin
// Figma: GROUP(150×60) → RECTANGLE(150×60, #F3F3F4, cornerRadius=8) → TEXT
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

### FRAME with layoutMode vs GROUP without layoutMode
- **FRAME with `layoutMode`**: has Auto-layout → map to `Column` or `Row`
- **GROUP without `layoutMode`**: no Auto-layout → children positioned by coordinates → use `Box` with explicit `Modifier.offset()` or nested `Box` layouts

```kotlin
// FRAME with layoutMode: VERTICAL → Column
Column(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp)
) {
    Text("Item 1")
    Text("Item 2")
}

// GROUP without layoutMode → use Box with offset
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

### Numeric Precision
Figma values often have excessive decimal places. Round appropriately for Compose:
- **`dp` values** (layout, padding, margins): round to **nearest integer**
  - Example: 127.86dp → 128.dp, 7.63dp → 8.dp
- **`sp` values** (font sizes): round to **nearest 0.5**
  - Example: 15.27sp → 15.5sp, 14.99sp → 15sp
- **Exception**: If the exact value maps to a standard size, snap to it
  - Example: 47.99dp → 48.dp (standard Material touch target)
```

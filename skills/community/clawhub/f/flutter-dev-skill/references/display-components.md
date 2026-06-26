---
name: flutter-display-components
description: Flutter 显示组件详解（对话框、卡片、FAB、 Snackbars、列表等）。
source: https://flutter.cn/docs
---

# Display Components

## Dialog

### 默认 BorderRadius 变更

M3 中 Dialog 的默认圆角从 2.0 改为 4.0 像素。

```dart
// 恢复 M2 行为
AlertDialog(
  content: Text('Alert!'),
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.all(Radius.circular(2)),
  ),
)

// M3 新默认 (4.0 圆角)
AlertDialog(
  content: Text('Alert!'),
  // 无需手动设置，使用新默认
)
```

### AlertDialog 自动滚动

`AlertDialog` 现在在内容溢出时自动滚动，确保按钮始终可见。

```dart
// 迁移后不需要手动包装 SingleChildScrollView
AlertDialog(
  title: Text('Very, very large title', textScaleFactor: 5),
  content: Text('Very, very large content', textScaleFactor: 5),
  actions: <Widget>[
    TextButton(child: Text('Button 1'), onPressed: () {}),
    TextButton(child: Text('Button 2'), onPressed: () {}),
  ],
)

// 迁移前需要手动处理
AlertDialog(
  title: SingleChildScrollView(  // 不再需要
    child: Text('Very, very large title', textScaleFactor: 5),
  ),
  content: SingleChildScrollView(
    child: Text('Scrollable content', textScaleFactor: 5),
  ),
  actions: [...],
)
```

---

## FloatingActionButton (FAB)

### 废弃 accent 属性依赖

FAB 不再使用 `ThemeData.accentIconTheme`，改用 `FloatingActionButtonThemeData.foregroundColor`。

```dart
// 迁移前
MaterialApp(
  theme: ThemeData(
    accentIconTheme: IconThemeData(color: Colors.red),
  ),
)

// 迁移后
MaterialApp(
  theme: ThemeData(
    floatingActionButtonTheme: FloatingActionButtonThemeData(
      foregroundColor: Colors.red,
    ),
  ),
)

// FAB foregroundColor 优先级
final Color foregroundColor = this.foregroundColor
  ?? floatingActionButtonTheme.foregroundColor
  ?? theme.colorScheme.onSecondary;  // 新默认值
```

---

## SnackBar

### 带 Action 的 SnackBar 不再自动消失

M3 中带 action 的 SnackBar 默认保持显示，直到用户手动交互。

```dart
// 默认行为 (M3): 带 action 的 SnackBar 不会自动消失
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: const Text('This is a snackbar with an action.'),
    action: SnackBarAction(
      label: 'Action',
      onPressed: () { /* 执行操作 */ },
    ),
  ),
)

// 恢复旧行为 (自动消失)
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: const Text('This is a snackbar with an action.'),
    persist: false,  // 添加此属性恢复自动消失
    action: SnackBarAction(
      label: 'Action',
      onPressed: () { /* 执行操作 */ },
    ),
  ),
)

// persist 属性说明:
// - true: 不自动消失，保持显示直到手动关闭
// - false: 自动消失
// - null: 默认行为 (带 action 时不自动消失)
```

---

## ListTile

### 背景色警告

当 `ListTile` 被包裹在有背景色的中间 widget 中时，框架会报告错误。

```dart
// 错误示例
Material(
  child: Container(
    color: Colors.pink,  // 错误：遮蔽 ListTile 的 ink splashes
    child: ListTile(
      title: const Text('Title'),
      onTap: () {},
    ),
  ),
)

// 正确做法 1: 使用 Material 作为背景
Material(
  color: Colors.pink,
  child: Container(
    child: ListTile(
      title: const Text('Title'),
      onTap: () {},
    ),
  ),
)

// 正确做法 2: 包裹 ListTile 在自己的 Material 中
Container(
  color: Colors.blue,
  child: Material(
    type: MaterialType.transparency,
    child: ListTile(
      title: const Text('Title'),
      onTap: () {},
    ),
  ),
)
```

---

## Chip

### deleteButtonTooltipMessage 替换 useDeleteButtonTooltip

`useDeleteButtonTooltip` 已废弃，改用 `deleteButtonTooltipMessage`。

```dart
// 禁用删除按钮 tooltip
Chip(
  label: const Text('Disabled delete button tooltip'),
  onDeleted: _handleDeleteChip,
  deleteButtonTooltipMessage: '',  // 空字符串禁用
)

// 启用删除按钮 tooltip (默认)
RawChip(
  label: const Text('Enabled delete button tooltip'),
  onDeleted: _handleDeleteChip,
  // 不需要设置，默认启用
)

// 迁移前
Chip(
  label: const Text('Disabled delete button tooltip'),
  onDeleted: _handleDeleteChip,
  useDeleteButtonTooltip: false,
)
```

---

## Container

### 颜色优化

当只设置 `color` 而不使用 `decoration` 时，`Container` 现在使用更高效的 `ColoredBox`。

```dart
// 现在使用 ColoredBox 替代 BoxDecoration
Container(color: Colors.red)

// 测试适配
testWidgets('Container color', (WidgetTester tester) async {
  await tester.pumpWidget(Container(color: Colors.red));

  final Container container = tester.widgetList<Container>().first;
  expect(container.color, Colors.red);  // 直接访问 color 属性
  expect(find.byType(BoxDecoration), findsNothing);
  expect(find.byType(ColoredBox), findsOneWidget);
})
```

---

## Progress Indicators (M3 更新)

### LinearProgressIndicator

```dart
// M3 新设计 (2024)
LinearProgressIndicator(
  year2023: false,  // 启用 M3 新设计
  value: 0.5,
)

// 新设计特点:
// - active 和 inactive track 之间有间隙
// - 停止指示器
// - 圆角

// 全局应用
MaterialApp(
  theme: ThemeData(
    progressIndicatorTheme: const ProgressIndicatorThemeData(year2023: false),
  ),
)
```

### CircularProgressIndicator

```dart
// M3 新设计 (2024)
CircularProgressIndicator(
  year2023: false,  // 启用 M3 新设计
  value: 0.5,
)

// 新设计特点:
// - track 间隙
// - 圆角 stroke cap

// 全局应用
MaterialApp(
  theme: ThemeData(
    progressIndicatorTheme: const ProgressIndicatorThemeData(year2023: false),
  ),
)
```

---

## Slider (M3 更新)

```dart
// M3 新设计 (2024)
Slider(
  year2023: false,  // 启用 M3 新设计
  value: _value,
  onChanged: (value) {
    setState(() { _value = value; });
  },
)

// 新设计特点:
// - 更新的高度
// - active 和 inactive track 之间的间隙
// - 停止指示器显示 inactive track 的结束值
// - 按下时 thumb 宽度调整
// - track 形状调整
// - 新的 value indicator 形状 (圆角矩形)

// 全局应用
MaterialApp(
  theme: ThemeData(
    sliderTheme: const SliderThemeData(year2023: false),
  ),
)
```

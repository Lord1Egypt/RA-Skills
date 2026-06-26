---
name: flutter-material-3
description: Flutter Material 3 迁移与主题系统完整参考。
source: https://flutter.cn/docs/release/breaking-changes/material-3-migration
---

# Flutter Material 3 迁移与主题系统完整参考

## 目录

1. [Material 3 迁移概述](#1-material-3-迁移概述)
2. [ColorScheme 变化](#2-colorscheme-变化)
3. [组件主题规范化](#3-组件主题规范化)
4. [Material 3 Token 更新](#4-material-3-token-更新)
5. [Material Color Utilities](#5-material-color-utilities)
6. [Material State → WidgetState](#6-material-state--widgetstate)
7. [Material Theme System 更新](#7-material-theme-system-更新)
8. [关键 breaking changes 汇总](#8-关键-breaking-changes-汇总)

---

## 1. Material 3 迁移概述

### 1.1 useMaterial3 默认为 true

**生效版本**: Flutter 3.16 (2023年11月)

从 Flutter 3.16 开始，`useMaterial3` 默认为 `true`。这是 Material Design 3 在 Flutter 中的里程碑变化。

```dart
// Flutter 3.16 之前 - 需要手动启用
MaterialApp(
  theme: ThemeData(
    useMaterial3: true, // 显式启用
  ),
)

// Flutter 3.16+ - 默认启用
MaterialApp(
  theme: ThemeData(
    // useMaterial3: true 已为默认值
  ),
)
```

**注意**: 虽然可以设置 `useMaterial3: false` 临时回退到 Material 2，但这只是临时解决方案。`useMaterial3` 标志和 Material 2 实现将最终被移除。

### 1.2 需要手动迁移的组件

部分组件无法仅通过样式更新匹配 Material 3，需要使用新组件替代：

| Material 2 组件 | Material 3 替代 | 特点 |
|---|---|---|
| `BottomNavigationBar` | `NavigationBar` | 更高度，pill-shaped 导航指示器，新颜色映射 |
| `Drawer` | `NavigationDrawer` | pill-shaped 导航指示器，圆角，新颜色映射 |
| `ToggleButtons` | `SegmentedButton` | 完全圆角，使用 Dart `Set` 确定选中项 |

### 1.3 BottomNavigationBar → NavigationBar 迁移

```dart
// 迁移前 (Material 2)
BottomNavigationBar(
  items: const <BottomNavigationBarItem>[
    BottomNavigationBarItem(
      icon: Icon(Icons.home),
      label: 'Home',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.business),
      label: 'Business',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.school),
      label: 'School',
    ),
  ],
)

// 迁移后 (Material 3)
NavigationBar(
  destinations: const <Widget>[
    NavigationDestination(
      icon: Icon(Icons.home),
      label: 'Home',
    ),
    NavigationDestination(
      icon: Icon(Icons.business),
      label: 'Business',
    ),
    NavigationDestination(
      icon: Icon(Icons.school),
      label: 'School',
    ),
  ],
)
```

### 1.4 Drawer → NavigationDrawer 迁移

```dart
// 迁移前
Drawer(
  child: ListView(
    children: <Widget>[
      DrawerHeader(
        child: Text('Drawer Header'),
      ),
      ListTile(
        leading: const Icon(Icons.message),
        title: const Text('Messages'),
        onTap: () { },
      ),
      // ...
    ],
  ),
)

// 迁移后
NavigationDrawer(
  children: <Widget>[
    DrawerHeader(
      child: Text('Drawer Header'),
    ),
    const NavigationDrawerDestination(
      icon: Icon(Icons.message),
      label: Text('Messages'),
    ),
    // ...
  ],
)
```

### 1.5 ToggleButtons → SegmentedButton 迁移

```dart
// 迁移前
enum Weather { cloudy, rainy, sunny }

ToggleButtons(
  isSelected: const [false, true, false],
  onPressed: (int newSelection) { },
  children: const <Widget>[
    Icon(Icons.cloud_outlined),
    Icon(Icons.beach_access_sharp),
    Icon(Icons.brightness_5_sharp),
  ],
)

// 迁移后
enum Weather { cloudy, rainy, sunny }

SegmentedButton<Weather>(
  selected: const <Weather>{Weather.rainy},
  onSelectionChanged: (Set<Weather> newSelection) { },
  segments: const <ButtonSegment<Weather>>[
    ButtonSegment(
      icon: Icon(Icons.cloud_outlined),
      value: Weather.cloudy,
    ),
    ButtonSegment(
      icon: Icon(Icons.beach_access_sharp),
      value: Weather.rainy,
    ),
    ButtonSegment(
      icon: Icon(Icons.brightness_5_sharp),
      value: Weather.sunny,
    ),
  ],
)
```

### 1.6 新增组件

Material 3 引入的新组件：

- **`MenuBar`** / **`MenuAnchor`**: 桌面风格菜单系统，支持鼠标和键盘完全遍历
- **`DropdownMenu`**: 结合文本框和菜单的组合框
- **`SearchBar`** / **`SearchAnchor`**: 搜索交互组件
- **`Badge`**: 装饰子组件的小标签
- **`FilledButton`** / **`FilledButton.tonal`**: 类似 ElevatedButton 但无海拔变化和投影
- **`FilterChip.elevated`** / **`ChoiceChip.elevated`** / **`ActionChip.elevated`**: 带投影和填充色的芯片变体
- **`Dialog.fullscreen`**: 全屏对话框
- **`SliverAppBar.medium`** / **`SliverAppBar.large`**: 中等和大型应用栏

### 1.7 Medium App Bar 示例

```dart
CustomScrollView(
  slivers: <Widget>[
    const SliverAppBar.medium(
      title: Text('Title'),
    ),
    SliverToBoxAdapter(
      child: Card(
        child: SizedBox(
          height: 1200,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(8, 100, 8, 100),
            child: Text(
              'Here be scrolling content...',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
          ),
        ),
      ),
    ),
  ],
)
```

### 1.8 Typography 变化

Material 3 更新了 `TextTheme` 的默认值，包括字体大小、字重、字母间距和行高的变化。

```dart
// 如果必须保持之前的行为，调整文本样式
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 200),
  child: Text(
    'This is a very long text that should wrap to multiple lines.',
    style: Theme.of(context).textTheme.bodyMedium!.copyWith(
      letterSpacing: 0.0,
    ),
  ),
)
```

---

## 2. ColorScheme 变化

### 2.1 ColorScheme.fromSeed

`ColorScheme.fromSeed` 是 Material 3 推荐的颜色生成方式：

```dart
// 推荐方式
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
),

// 深色主题
darkTheme: ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.dark,
  ),
),
```

### 2.2 动态颜色方案 (从图片生成)

```dart
ColorScheme.fromImageProvider(
  provider: NetworkImage('https://example.com/image.jpg'),
)
```

### 2.3 新的基于色调的 Surface 颜色

Material 3 引入了 7 个新的基于色调的 surface 颜色：

| 属性 | 说明 |
|---|---|
| `surfaceBright` | 亮 surface |
| `surfaceDim` | 暗 surface |
| `surfaceContainer` | 基础容器 |
| `surfaceContainerLow` | 低容器 |
| `surfaceContainerLowest` | 最低容器 |
| `surfaceContainerHigh` | 高容器 |
| `surfaceContainerHighest` | 最高容器 |

这些颜色消除了 `surfaceTintColor` 的使用，替代了基于透明度的海拔叠加模型。

### 2.4 被废弃的颜色角色

| 废弃 | 替代 |
|---|---|
| `background` | `surface` |
| `onBackground` | `onSurface` |
| `surfaceVariant` | `surfaceContainerHighest` |

```dart
// 迁移前
colorScheme.copyWith(
  background: myColor1,
  onBackground: myColor2,
  surfaceVariant: myColor3,
)

// 迁移后
colorScheme.copyWith(
  surface: myColor1,
  onSurface: myColor2,
  surfaceContainerHighest: myColor3,
)
```

### 2.5 surfaceTint 变化

`ColorScheme.surfaceTint` 在 Material 3 中表示组件的海拔。某些组件（如 Card 和 ElevatedButton）同时使用 `surfaceTint` 和 `shadowColor`，而 AppBar 只使用 `surfaceTint`。

```dart
// 恢复之前的行为
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple).copyWith(
    surfaceTint: Colors.transparent,
  ),
  appBarTheme: AppBarTheme(
    elevation: 4.0,
    shadowColor: Theme.of(context).colorScheme.shadow,
  ),
)
```

### 2.6 恢复 Material 2 的 background 颜色

```dart
// 亮色主题
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple).copyWith(
    surface: Colors.grey[50]!,
  ),
),

// 暗色主题
darkTheme: ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.dark,
  ).copyWith(surface: Colors.grey[850]!),
),
```

### 2.7 DynamicSchemeVariant (3.22+)

当向 `ColorScheme.fromSeed` 提供亮色种子时，可能生成相对较暗的 `ColorScheme`。要强制输出保持亮色：

```dart
ColorScheme.fromSeed(
  seedColor: Color(0xFF0000FF), // 亮蓝色
  dynamicSchemeVariant: DynamicSchemeVariant.fidelity,
)
```

### 2.8 ElevatedButton 样式变化

Material 3 中 `ElevatedButton` 使用新的颜色组合。如果需要保持之前的视觉效果：

```dart
// 迁移前
ElevatedButton(
  onPressed: () {},
  child: const Text('Button'),
)

// 迁移后 - 保持之前的视觉效果
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Theme.of(context).colorScheme.primary,
    foregroundColor: Theme.of(context).colorScheme.onPrimary,
  ),
  onPressed: () {},
  child: const Text('Button'),
)

// 或使用新的 FilledButton
FilledButton(
  onPressed: () {},
  child: const Text('Button'),
)
```

---

## 3. 组件主题规范化

Flutter 持续规范化组件主题，遵循一致的命名约定。

### 3.1 组件主题命名约定

| ThemeData 属性 | 旧类型 | 新类型 | 生效版本 |
|---|---|---|---|
| `cardTheme` | `CardTheme` | `CardThemeData` | 3.27 |
| `dialogTheme` | `DialogTheme` | `DialogThemeData` | 3.27 |
| `tabBarTheme` | `TabBarTheme` | `TabBarThemeData` | 3.27 |
| `appBarTheme` | `AppBarTheme` | `AppBarThemeData` | 3.35 |
| `bottomAppBarTheme` | `BottomAppBarTheme` | `BottomAppBarThemeData` | 3.35 |
| `inputDecorationTheme` | `InputDecorationTheme` | `InputDecorationThemeData` | 3.35 |

### 3.2 CardTheme / DialogTheme / TabBarTheme 迁移 (3.27)

```dart
// 迁移前
final CardTheme cardTheme = Theme.of(context).cardTheme;
final CardTheme cardTheme = CardTheme.of(context);

final DialogTheme dialogTheme = Theme.of(context).dialogTheme;
final DialogTheme dialogTheme = DialogTheme.of(context);

final TabBarTheme tabBarTheme = Theme.of(context).tabBarTheme;
final TabBarTheme tabBarTheme = TabBarTheme.of(context);

// 在 ThemeData 中
final ThemeData theme = ThemeData(
  cardTheme: CardTheme(),
  dialogTheme: DialogTheme(),
  tabBarTheme: TabBarTheme(),
);
final ThemeData theme = ThemeData().copyWith(
  cardTheme: CardTheme(),
  dialogTheme: DialogTheme(),
  tabBarTheme: TabBarTheme(),
);

// 迁移后
final CardThemeData cardTheme = Theme.of(context).cardTheme;
final CardThemeData cardTheme = CardTheme.of(context);

final DialogThemeData dialogTheme = Theme.of(context).dialogTheme;
final DialogThemeData dialogTheme = DialogTheme.of(context);

final TabBarThemeData tabBarTheme = Theme.of(context).tabBarTheme;
final TabBarThemeData tabBarTheme = TabBarTheme.of(context);

// 在 ThemeData 中
final ThemeData theme = ThemeData(
  cardTheme: CardThemeData(),
  dialogTheme: DialogThemeData(),
  tabBarTheme: TabBarThemeData(),
);
final ThemeData theme = ThemeData().copyWith(
  cardTheme: CardThemeData(),
  dialogTheme: DialogThemeData(),
  tabBarTheme: TabBarThemeData(),
);
```

### 3.3 AppBarTheme / BottomAppBarTheme / InputDecorationTheme 迁移 (3.35)

```dart
// 迁移前
final AppBarTheme appBarTheme = Theme.of(context).appBarTheme;
final AppBarTheme appBarTheme = AppBarTheme.of(context);

final BottomAppBarTheme bottomAppBarTheme = Theme.of(context).bottomAppBarTheme;
final BottomAppBarTheme bottomAppBarTheme = BottomAppBarTheme.of(context);

final InputDecorationTheme inputDecorationTheme = Theme.of(context).inputDecorationTheme;
final InputDecorationTheme inputDecorationTheme = InputDecorationTheme.of(context);

// 迁移后
final AppBarThemeData appBarTheme = Theme.of(context).appBarTheme;
final AppBarThemeData appBarTheme = AppBarTheme.of(context);

final BottomAppBarThemeData bottomAppBarTheme = Theme.of(context).bottomAppBarTheme;
final BottomAppBarThemeData bottomAppBarTheme = BottomAppBarTheme.of(context);

final InputDecorationThemeData inputDecorationTheme = Theme.of(context).inputDecorationTheme;
final InputDecorationThemeData inputDecorationTheme = InputDecorationTheme.of(context);
```

### 3.4 DatePickerTheme / TimePickerTheme 中的 InputDecorationTheme

```dart
// 迁移前
const DatePickerThemeData datePickerTheme = DatePickerThemeData(
  inputDecorationTheme: InputDecorationTheme()
);
const TimePickerThemeData timePickerTheme = TimePickerThemeData(
  inputDecorationTheme: InputDecorationTheme()
);

// 迁移后
const DatePickerThemeData datePickerTheme = DatePickerThemeData(
  inputDecorationTheme: InputDecorationThemeData()
);
const TimePickerThemeData timePickerTheme = TimePickerThemeData(
  inputDecorationTheme: InputDecorationThemeData()
);
```

---

## 4. Material 3 Token 更新

### 4.1 颜色角色映射更新 (v6.1)

Material 3 tokens 更新了 4 个颜色角色在亮色模式下的映射：

| 属性 | 旧值 | 新值 |
|---|---|---|
| `onPrimaryContainer` | Primary10 | Primary30 |
| `onSecondaryContainer` | Secondary10 | Secondary30 |
| `onTertiaryContainer` | Tertiary10 | Tertiary30 |
| `onErrorContainer` | Error10 | Error30 |

这些变化使颜色更美观且保持可访问的对比度。

### 4.2 恢复旧颜色

```dart
final ColorScheme colors = ThemeData().colorScheme.copyWith(
  onPrimaryContainer: const Color(0xFF21005D),
  onSecondaryContainer: const Color(0xFF1D192B),
  onTertiaryContainer: const Color(0xFF31111D),
  onErrorContainer: const Color(0xFF410E0B),
);
```

### 4.3 Chip 边框颜色变化

Chip 组件的边框颜色从 `ColorScheme.outline` 变为 `ColorScheme.outlineVariant`。

影响组件: `Chip`, `ActionChip`, `ChoiceChip`, `FilterChip`, `InputChip`

```dart
// 恢复之前的边框颜色
final chip = ChipTheme(
  data: ChipThemeData(
    side: BorderSide(
      color: Theme.of(context).colorScheme.outline
    ),
  ),
  child: ActionChip(
    label: const Text('action chip'),
    onPressed: () {}
  )
);
```

---

## 5. Material Color Utilities

### 5.1 包更新

`package:material_color_utilities` 从 `v0.11.1` 更新到 `0.13.0`。

### 5.2 受影响的属性

算法更新影响以下属性的生成：

- `onPrimaryContainer`
- `onSecondaryContainer`
- `onTertiaryContainer`
- `onErrorContainer`

### 5.3 影响的 API

- `ColorScheme.fromSeed`
- `ColorScheme.fromImageProvider`
- `ThemeData(colorScheme: ..)`

### 5.4 迁移说明

新算法生成的颜色通常更易读、更美观。如果需要保持之前的颜色，需要在生成后手动设置：

```dart
final colorScheme = ColorScheme.fromSeed(
  seedColor: seedColor,
  onPrimaryContainer: previousColor,
  onSecondaryContainer: previousColor,
  onTertiaryContainer: previousColor,
  onErrorContainer: previousColor,
);
```

---

## 6. Material State → WidgetState

### 6.1 重命名原因

`MaterialState` 提供的功能（处理 widgets 可以拥有的多种状态，如"悬停"、"聚焦"、"禁用"）在 Material 库之外也很有用。为了让 Widgets 层和 Cupertino 也能使用，API 被移到了 widgets 库，并重命名为 `WidgetState`。

### 6.2 API 对照表

| 旧 (MaterialState) | 新 (WidgetState) |
|---|---|
| `MaterialState` | `WidgetState` |
| `MaterialStatePropertyResolver` | `WidgetStatePropertyResolver` |
| `MaterialStateColor` | `WidgetStateColor` |
| `MaterialStateMouseCursor` | `WidgetStateMouseCursor` |
| `MaterialStateBorderSide` | `WidgetStateBorderSide` |
| `MaterialStateOutlinedBorder` | `WidgetStateOutlinedBorder` |
| `MaterialStateTextStyle` | `WidgetStateTextStyle` |
| `MaterialStateProperty` | `WidgetStateProperty` |
| `MaterialStatePropertyAll` | `WidgetStatePropertyAll` |
| `MaterialStatesController` | `WidgetStatesController` |

### 6.3 迁移示例

```dart
// 迁移前
MaterialState selected = MaterialState.selected;

final MaterialStateProperty<Color> backgroundColor;

class _MouseCursor extends MaterialStateMouseCursor {
  const _MouseCursor(this.resolveCallback);

  final MaterialPropertyResolver<MouseCursor?> resolveCallback;

  @override
  MouseCursor resolve(Set<MaterialState> states) =>
    resolveCallback(states) ?? MouseCursor.uncontrolled;
}

BorderSide side = MaterialStateBorderSide.resolveWith((Set<MaterialState> states) {
  if (states.contains(MaterialState.selected)) {
    return const BorderSide(color: Colors.red);
  }
  return null;
});

// 迁移后
WidgetState selected = WidgetState.selected;

final WidgetStateProperty<Color> backgroundColor;

class _MouseCursor extends WidgetStateMouseCursor {
  const _MouseCursor(this.resolveCallback);

  final WidgetPropertyResolver<MouseCursor?> resolveCallback;

  @override
  MouseCursor resolve(Set<WidgetState> states) =>
    resolveCallback(states) ?? MouseCursor.uncontrolled;
}

BorderSide side = WidgetStateBorderSide.resolveWith((Set<WidgetState> states) {
  if (states.contains(WidgetState.selected)) {
    return const BorderSide(color: Colors.red);
  }
  return null;
});
```

### 6.4 保留在 Material 库的类

以下类保留在 Material 库中，没有 `WidgetState` 等价物，因为它们特定于 Material 设计：

- `MaterialStateOutlineInputBorder`
- `MaterialStateUnderlineInputBorder`

---

## 7. Material Theme System 更新

### 7.1 ThemeData 属性类型变更

在 Flutter 3.32 中，`ThemeData` 的组件主题属性类型最终化为：

| ThemeData 属性 | 类型 |
|---|---|
| `cardTheme` | `CardThemeData?` |
| `dialogTheme` | `DialogThemeData?` |
| `tabBarTheme` | `TabBarThemeData?` |
| `appBarTheme` | `AppBarThemeData?` |
| `bottomAppBarTheme` | `BottomAppBarThemeData?` |
| `inputDecorationTheme` | `InputDecorationThemeData?` |

### 7.2 使用示例

```dart
final ThemeData theme = ThemeData(
  cardTheme: CardThemeData(),
  dialogTheme: DialogThemeData(),
  tabBarTheme: TabBarThemeData(),
  appBarTheme: AppBarThemeData(),
  bottomAppBarTheme: BottomAppBarThemeData(),
  inputDecorationTheme: InputDecorationThemeData(),
);
```

---

## 8. 关键 Breaking Changes 汇总

| 变化 | 生效版本 | 严重程度 |
|---|---|---|
| `useMaterial3` 默认为 `true` | 3.16 | 高 |
| BottomNavigationBar → NavigationBar | 3.16 | 中 (可选迁移) |
| Drawer → NavigationDrawer | 3.16 | 中 (可选迁移) |
| ToggleButtons → SegmentedButton | 3.16 | 中 (可选迁移) |
| `background` → `surface` | 3.22 | 低 |
| `onBackground` → `onSurface` | 3.22 | 低 |
| `surfaceVariant` → `surfaceContainerHighest` | 3.22 | 低 |
| `MaterialState` → `WidgetState` | 3.22 | 高 |
| CardTheme → CardThemeData | 3.27 | 中 |
| DialogTheme → DialogThemeData | 3.27 | 中 |
| TabBarTheme → TabBarThemeData | 3.27 | 中 |
| AppBarTheme → AppBarThemeData | 3.35 | 中 |
| BottomAppBarTheme → BottomAppBarThemeData | 3.35 | 中 |
| InputDecorationTheme → InputDecorationThemeData | 3.35 | 中 |
| Token 更新 (onPrimaryContainer 等) | 3.27 | 低 |
| Chip 边框颜色变化 | 3.27 | 低 |

### 8.1 ReorderableListView 本地化字符串迁移 (3.13)

`ReorderableListView` 的本地化字符串从 Material 本地化移至 Widgets 本地化：

```dart
// 迁移前
MaterialLocalizations.of(context).reorderItemToStart;

// 迁移后
WidgetsLocalizations.of(context).reorderItemToStart;
```

如果自定义 `MaterialLocalizations` 或 `WidgetsLocalizations`，需要将翻译从 `MaterialLocalizations` 子类移到 `WidgetsLocalizations` 子类。

---

## 附录：完整迁移检查清单

### 启用 Material 3

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true, // 默认值，但建议显式设置
    colorScheme: ColorScheme.fromSeed(seedColor: yourBrandColor),
  ),
)
```

### 颜色迁移

- [ ] 将 `ColorScheme.background` 替换为 `ColorScheme.surface`
- [ ] 将 `ColorScheme.onBackground` 替换为 `ColorScheme.onSurface`
- [ ] 将 `ColorScheme.surfaceVariant` 替换为 `ColorScheme.surfaceContainerHighest`
- [ ] 考虑使用 `ColorScheme.fromSeed()` 生成颜色方案

### 组件迁移

- [ ] `BottomNavigationBar` → `NavigationBar`
- [ ] `Drawer` → `NavigationDrawer`
- [ ] `ToggleButtons` → `SegmentedButton`
- [ ] 考虑使用新的 M3 组件: FilledButton, Badge, SearchBar 等

### 类型迁移

- [ ] `CardTheme` → `CardThemeData`
- [ ] `DialogTheme` → `DialogThemeData`
- [ ] `TabBarTheme` → `TabBarThemeData`
- [ ] `AppBarTheme` → `AppBarThemeData`
- [ ] `BottomAppBarTheme` → `BottomAppBarThemeData`
- [ ] `InputDecorationTheme` → `InputDecorationThemeData`

### State API 迁移

- [ ] `MaterialState` → `WidgetState`
- [ ] `MaterialStateProperty` → `WidgetStateProperty`
- [ ] `MaterialStateColor` → `WidgetStateColor`
- [ ] `MaterialStatesController` → `WidgetStatesController`

---

## 参考链接

- [Material Design for Flutter](https://flutter.cn/ui/design/material)
- [Material 3 Gallery](https://github.com/flutter/samples/tree/main/material_3_demo)
- [Material 3 Umbrella Issue](https://github.com/flutter/flutter/issues/91605)
- [ThemeData API](https://api.flutter.dev/flutter/material/ThemeData-class.html)
- [ColorScheme API](https://api.flutter.dev/flutter/material/ColorScheme-class.html)

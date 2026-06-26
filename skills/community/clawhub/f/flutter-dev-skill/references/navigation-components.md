---
name: flutter-navigation-components
description: Flutter 导航组件详解（AppBar、NavigationBar、NavigationRail、Drawer）。
source: https://flutter.cn/docs
---

# Navigation Components

## AppBar

### color 参数废弃

`AppBarTheme` 和 `AppBarThemeData` 中的 `color` 参数已废弃，改用 `backgroundColor`。

```dart
// 迁移前 (废弃)
AppBarTheme(
  color: Colors.blue,
  elevation: 4.0,
)

AppBarTheme(
  color: Colors.green,
  elevation: 4.0,
)

theme.copyWith(
  color: Colors.red,  // 废弃
)

// 迁移后
AppBarTheme(
  backgroundColor: Colors.blue,
  elevation: 4.0,
)

AppBarThemeData(
  backgroundColor: Colors.green,
  elevation: 4.0,
)

theme.copyWith(
  backgroundColor: Colors.red,
)
```

### 使用限制

同时使用 `color` 和 `backgroundColor` 会触发断言错误：

```
The color and backgroundColor parameters mean the same thing. Only specify one.
```

---

## BottomNavigationBar

### title 废弃，改用 label

`BottomNavigationBarItem.title` 已废弃，改用 `label` (String 类型)。

此变更为了支持文本缩放和长按显示 tooltip 的无障碍功能。

```dart
// 迁移前
BottomNavigationBarItem(
  icon: Icons.add,
  title: Text('add'),  // Widget 类型
)

// 迁移后
BottomNavigationBarItem(
  icon: Icons.add,
  label: 'add',  // String 类型
)
```

---

## NavigationBar & NavigationRail (自适应布局)

### 响应式布局策略

Google 推荐的响应式布局策略：

- **< 600dp**: 使用 `BottomNavigationBar`
- **≥ 600dp**: 使用 `NavigationRail`

### 自适应布局实现

```dart
// 步骤 1: 抽象导航目标
class Destination {
  final IconData icon;
  final String label;
  const Destination({required this.icon, required this.label});
}

const List<Destination> destinations = [
  Destination(icon: Icons.home, label: 'Home'),
  Destination(icon: Icons.search, label: 'Search'),
  Destination(icon: Icons.settings, label: 'Settings'),
];

// 步骤 2: 测量
// 使用 MediaQuery.sizeOf(context) 获取窗口大小
// 或使用 LayoutBuilder 获取约束

// 步骤 3: 分支
Widget build(BuildContext context) {
  final screenWidth = MediaQuery.sizeOf(context).width;
  final useNavigationRail = screenWidth >= 600;

  return useNavigationRail
    ? _buildNavigationRail()
    : _buildBottomNavigationBar();
}

Widget _buildNavigationRail() {
  return Scaffold(
    body: Row(
      children: [
        NavigationRail(
          selectedIndex: _selectedIndex,
          onDestinationSelected: (index) {
            setState(() { _selectedIndex = index; });
          },
          labelType: NavigationRailLabelType.all,
          destinations: destinations.map((d) {
            return NavigationRailDestination(
              icon: Icon(d.icon),
              label: Text(d.label),
            );
          }).toList(),
        ),
        const VerticalDivider(thickness: 1, width: 1),
        Expanded(child: _buildContent()),
      ],
    ),
  );
}

Widget _buildBottomNavigationBar() {
  return Scaffold(
    body: _buildContent(),
    bottomNavigationBar: NavigationBar(
      selectedIndex: _selectedIndex,
      onDestinationSelected: (index) {
        setState(() { _selectedIndex = index; });
      },
      destinations: destinations.map((d) {
        return NavigationDestination(
          icon: Icon(d.icon),
          label: d.label,
        );
      }).toList(),
    ),
  );
}
```

### MediaQuery vs LayoutBuilder

```dart
// MediaQuery.sizeOf - 获取整个应用窗口大小
// 适用于需要基于整个窗口大小的决策
final size = MediaQuery.sizeOf(context);
if (size.width >= 600) {
  // 使用 NavigationRail
}

// LayoutBuilder - 获取父 widget 的约束
// 适用于需要基于特定位置约束的决策
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth >= 600) {
      return _buildExpandedLayout();
    }
    return _buildCompactLayout();
  },
)
```

---

## Drawer

### 基本用法

```dart
Scaffold(
  appBar: AppBar(
    title: Text('App'),
  ),
  drawer: Drawer(
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        DrawerHeader(
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primary,
          ),
          child: Text('Drawer Header'),
        ),
        ListTile(
          leading: Icon(Icons.home),
          title: Text('Home'),
          onTap: () { Navigator.pop(context); },
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text('Settings'),
          onTap: () { Navigator.pop(context); },
        ),
      ],
    ),
  ),
)
```

---

## NavigationBar (Material 3)

### NavigationBar 主题

```dart
NavigationBar(
  height: 80,  // M3 默认高度
  elevation: 3,
  backgroundColor: Colors.surface,
  indicatorColor: Colors.secondaryContainer,
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.explore_outlined),
      selectedIcon: Icon(Icons.explore),
      label: 'Explore',
    ),
    NavigationDestination(
      icon: Icon(Icons.commute_outlined),
      selectedIcon: Icon(Icons.commute),
      label: 'Commute',
    ),
    NavigationDestination(
      icon: Icon(Icons.settings_outlined),
      selectedIcon: Icon(Icons.settings),
      label: 'Settings',
    ),
  ],
)

// 全局主题
MaterialApp(
  theme: ThemeData(
    navigationBarTheme: NavigationBarThemeData(
      height: 80,
      indicatorColor: Colors.secondaryContainer,
    ),
  ),
)
```

---

## NavigationRail (Material 3)

```dart
NavigationRail(
  selectedIndex: _selectedIndex,
  onDestinationSelected: (index) {
    setState(() { _selectedIndex = index; });
  },
  labelType: NavigationRailLabelType.all,  // 总是显示标签
  // 或 NavigationRailLabelType.selected - 仅选中时显示
  // 或 NavigationRailLabelType.none - 从不显示
  leading: FloatingActionButton(
    elevation: 3,
    child: Icon(Icons.add),
    onPressed: () { },
  ),
  destinations: const [
    NavigationRailDestination(
      icon: Icon(Icons.explore_outlined),
      selectedIcon: Icon(Icons.explore),
      label: Text('Explore'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.commute_outlined),
      selectedIcon: Icon(Icons.commute),
      label: Text('Commute'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.settings_outlined),
      selectedIcon: Icon(Icons.settings),
      label: Text('Settings'),
    ),
  ],
)

// 与扩展布局结合
Row(
  children: [
    NavigationRail(
      selectedIndex: _selectedIndex,
      onDestinationSelected: (index) {
        setState(() { _selectedIndex = index; });
      },
      extended: MediaQuery.sizeOf(context).width > 1200,
      minExtendedWidth: 180,
      destinations: [...],
    ),
    VerticalDivider(thickness: 1, width: 1),
    Expanded(child: content),
  ],
)
```

---

## 通用自适应布局模式

### 完整示例

```dart
class AdaptiveScaffold extends StatelessWidget {
  const AdaptiveScaffold({super.key});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // 手机: BottomNavigationBar
        if (constraints.maxWidth < 600) {
          return _PhoneLayout();
        }
        // 平板: NavigationRail
        if (constraints.maxWidth < 1200) {
          return _TabletLayout();
        }
        // 桌面: 扩展的 NavigationRail
        return _DesktopLayout();
      },
    );
  }
}

// 使用 Material Design 布局指南
// https://m3.material.io/foundations/layout/applying-layout/window-size-classes
```

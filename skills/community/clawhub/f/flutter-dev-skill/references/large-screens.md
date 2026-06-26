---
name: flutter-large-screens
description: Flutter 大屏支持、折叠屏设备与桌面布局模式完整参考。
source: https://flutter.cn/docs
---

# Flutter 大屏设备支持

本文档涵盖大屏设备布局策略、折叠屏适配、导航模式选择以及用户输入扩展支持。

## 大屏设备定义

Flutter 将以下设备定义为"大屏"：
- 平板电脑（Tablets）
- 折叠屏设备（Foldables）
- ChromeOS 设备
- Web 浏览器
- 桌面应用窗口
- iPad

> 大屏支持不仅提升用户体验，还会改善 Play Store 评分设备分类展示，并满足 iPadOS 提审要求。

## GridView 布局

`ListView` 在大屏上会浪费水平空间。改用 `GridView` 让内容宽度合理分布：

```dart
// 从 ListView.builder 迁移到 GridView.builder
GridView.builder(
  padding: const EdgeInsets.all(Insets.extraLarge),
  gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
    maxCrossAxisExtent: 400,  // 最大条目宽度
    childAspectRatio: 1,
  ),
  itemCount: itemCount,
  itemBuilder: (context, index) => _buildItem(index),
)
```

### gridDelegate 选择

| 委托 | 适用场景 |
|---|---|
| `SliverGridDelegateWithFixedCrossAxisCount` | 需要固定列数 |
| `SliverGridDelegateWithMaxCrossAxisExtent` | 需要最大条目宽度（响应式） |

> **重要**：不要根据设备类型硬编码列数。列数应由**窗口实际宽度**决定。

### ConstrainedBox 最大宽度限制

```dart
// 限制内容最大宽度，保持大屏上的可读性
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 1200),
  child: GridView.builder(...),
)
```

Material 3 建议的最大宽度值参见 [Applying layout](https://m3.material.io/foundations/layout/applying-layout/window-size-classes) 指南。

---

## 折叠屏设备（Foldables）

### 锁定方向导致的问题

锁定屏幕方向（`setPreferredOrientations`）的 App 在折叠屏展开时可能出现**黑边（letterboxing）**——App 窗口锁定在屏幕中央，周围为黑色。`MediaQuery` 也不会收到更大的窗口尺寸。

### 解决方案

**方案一**：支持所有方向（推荐）

**方案二**：使用 `Display` API 获取**物理屏幕尺寸**（少数需要物理尺寸而非窗口尺寸的场景）

```dart
/// 获取物理显示信息
ui.FlutterView? _view;

@override
void didChangeDependencies() {
  super.didChangeDependencies();
  _view = View.maybeOf(context);
}

void didChangeMetrics() {
  final ui.Display? display = _view?.display;
  // display?.size 获取物理尺寸
  // display?.pixelRatio 获取像素比
  // display?.refreshRate 获取刷新率
}
```

> 折叠屏的**唯一**例外场景需要使用物理显示尺寸。其他所有场景均应使用 `MediaQuery.sizeOf` 的**窗口尺寸**。

---

## 导航模式

根据窗口宽度选择导航组件：

```dart
Widget build(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;

  if (width < 600) {
    // Compact: 底部导航栏
    return BottomNavigationBar(...);
  } else if (width < 840) {
    // Medium: 导航轨道
    return NavigationRail(
      selectedIndex: _selectedIndex,
      onDestinationSelected: (index) =>
          setState(() => _selectedIndex = index),
      destinations: _destinations
          .map((d) => NavigationRailDestination(
                icon: Icon(d.icon),
                label: Text(d.label),
              ))
          .toList(),
    );
  } else {
    // Expanded: 永久侧边导航
    return NavigationDrawer(...);
  }
}
```

Material 3 导航规范：

| 尺寸类 | 宽度 | 导航组件 |
|---|---|---|
| Compact | < 600 dp | `BottomNavigationBar` |
| Medium | 600–839 dp | `NavigationRail` |
| Expanded | ≥ 840 dp | 永久侧边导航（Drawer/NavigationRail extended） |

---

## 自适应输入支持

### 三层大屏设备支持级别（Android 规范）

| 层级 | 要求 | 说明 |
|---|---|---|
| Tier 3（最低） | 鼠标 + 手写笔支持 | Material 3 按钮和选择器内置支持 |
| Tier 2 | 触控板 + 键盘 | 在 Tier 3 基础上扩展 |
| Tier 1（最高） | 多种输入设备无缝协作 | 完整的多模态输入体验 |

### 触控板/鼠标滚动

`ScrollView` 和 `ListView` 默认支持滚轮滚动。使用 `Listener` 自定义滚动行为：

```dart
return Listener(
  onPointerSignal: (event) {
    if (event is PointerScrollEvent) {
      print(event.scrollDelta.dy);  // 垂直滚动量
    }
  },
  child: ListView(),
);
```

### 鼠标悬停与焦点

```dart
return MouseRegion(
  cursor: SystemMouseCursors.click,
  onEnter: (_) => setState(() => _isHovered = true),
  onExit: (_) => setState(() => _isHovered = false),
  onHover: (e) => print(e.localPosition),
  child: GestureDetector(
    onTap: () {
      Focus.of(context).requestFocus();
      _submit();
    },
    child: Logo(showBorder: _isHovered),
  ),
);
```

### 键盘快捷键

```dart
class CreateNewItemIntent extends Intent {
  const CreateNewItemIntent();
}

Widget build(BuildContext context) {
  return Shortcuts(
    shortcuts: const <ShortcutActivator, Intent>{
      SingleActivator(LogicalKeyboardKey.keyN, control: true):
          CreateNewItemIntent(),
    },
    child: Actions(
      actions: <Type, Action<Intent>>{
        CreateNewItemIntent: CallbackAction<CreateNewItemIntent>(
          onInvoke: (intent) => _createNewItem(),
        ),
      },
      child: Focus(autofocus: true, child: Container()),
    ),
  );
}
```

全局快捷键使用 `HardwareKeyboard.instance.addHandler`。

### 视觉密度

```dart
// 触摸设备：标准密度；桌面设备：紧凑
double densityAmt = touchMode ? 0.0 : -1.0;
VisualDensity density = VisualDensity(
  horizontal: densityAmt,
  vertical: densityAmt,
);

MaterialApp(
  theme: ThemeData(visualDensity: density),
  home: MainAppScaffold(),
);
```

---

## 状态保存

### 列表滚动位置

方向改变时使用 `PageStorageKey` 保存和恢复滚动位置：

```dart
// 保存
ListView.builder(
  key: PageStorageKey('my-list-key'),
  itemBuilder: (context, index) => ListTile(title: Text('Item $index')),
);

// 如果列表布局在方向改变时也变化，可能需要额外计算滚动位置
```

### 配置变更时的状态

应用应在设备旋转、窗口大小变化、折叠/展开时保持状态。如果状态丢失，检查插件和大屏支持情况。

---

## 最佳实践速查

| 不要做 | 正确做法 |
|---|---|
| 锁定屏幕方向 | 支持所有方向 |
| `MediaQuery.orientation` 判断布局 | `MediaQuery.sizeOf` 或 `LayoutBuilder` |
| 根据设备类型判断尺寸 | 根据窗口实际宽度判断 |
| `ListView` 填满水平空间 | `GridView` + `ConstrainedBox(maxWidth)` |
| 触摸优先再考虑桌面 | 先构建触摸 UI，桌面作为加速层 |
| 忽略辅助功能 | 键盘导航 + 焦点管理 + 语义标签 |

## 参考资源

- [Material 3 Window Size Classes](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)
- [Android Large Screen App Quality Guidelines](https://developer.android.com/docs/quality-guidelines/large-screen-app-quality)
- [Apple Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)
- [Building an animated responsive app layout with Material 3]({{site.codelabs}}/codelabs/flutter-animated-responsive-layout)

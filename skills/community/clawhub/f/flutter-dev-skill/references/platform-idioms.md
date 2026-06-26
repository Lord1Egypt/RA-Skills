---
name: flutter-platform-idioms
description: Flutter 设备 idiom 检测与平台特定 UI 模式完整参考。
source: https://flutter.cn/docs
---

# Flutter 设备形态与平台特定模式

本文档涵盖设备形态（idiom）检测策略、平台特定 UI 模式、输入设备适配以及跨平台最佳实践。

## 核心原则：按窗口尺寸，而非设备类型

```dart
// 错误：根据设备类型判断
if (device == 'tablet') { ... }

// 正确：根据窗口可用空间判断
if (MediaQuery.sizeOf(context).width >= 600) { ... }
```

Flutter 应用可能在以下环境中运行：桌面可调整窗口、平板多窗口模式、画中画等。窗口尺寸与设备类型并非强关联。

## 平台倡导者（Platform Advocate）

每个目标平台应指定一名**倡导者**（不一定是开发者，可以是设计师、测试人员）：
- 日常使用该平台，能发现平台特定的不一致
- 及时反馈 UI/UX 问题
- 例：macOS+iOS 一个倡导者，Windows+Android 一个倡导者

## 滚动条样式

桌面用户期望滚动条始终可见、可点击拖动；移动用户期望滚动条仅在滚动时短暂出现。

```dart
// 平台自适应滚动条
return Scrollbar(
  thumbVisibility: DeviceType.isDesktop,  // 仅桌面始终显示
  controller: _scrollController,
  child: GridView.count(
    controller: _scrollController,
    padding: const EdgeInsets.all(Insets.extraLarge),
    childAspectRatio: 1,
    crossAxisCount: colCount,
    children: listChildren,
  ),
);
```

## 多选交互

### 平台感知多选修饰键

```dart
static bool get isMultiSelectModifierDown {
  bool isDown = false;
  if (Platform.isMacOS) {
    isDown = isKeyDown({
      LogicalKeyboardKey.metaLeft,
      LogicalKeyboardKey.metaRight,
    });
  } else {
    isDown = isKeyDown({
      LogicalKeyboardKey.controlLeft,
      LogicalKeyboardKey.controlRight,
    });
  }
  return isDown;
}

// 范围选择（Shift+点击）
static bool get isSpanSelectModifierDown =>
    isKeyDown({LogicalKeyboardKey.shiftLeft, LogicalKeyboardKey.shiftRight});
```

### 触摸设备多选

触摸设备多选通常简化为单次点击选择/取消选择，配合 "Select All" / "Clear" 按钮。

### 全选快捷键

桌面列表应支持 `Control+A` 全选。

## 文本选择

桌面和 Web 用户期望大多数文本可鼠标选中。使用 [`SelectableText`][] 组件：

```dart
// 普通文本
return const SelectableText('Select me!');

// 富文本
return const SelectableText.rich(
  TextSpan(
    children: [
      TextSpan(text: 'Hello'),
      TextSpan(
        text: 'Bold',
        style: TextStyle(fontWeight: FontWeight.bold),
      ),
    ],
  ),
);
```

[`SelectableText`]: {{site.api}}/flutter/material/SelectableText-class.html

## 标题栏（Title Bar）

桌面应用可自定义标题栏以增强品牌或节省垂直空间。使用 [`bits_dojo`][] 包替换原生标题栏：

```dart
// bits_dojo 允许用纯 Flutter widget 构建标题栏
import 'package:bitsdojo_window/bitsdojo_window.dart';

@override
Widget build(BuildContext context) {
  return WindowTitleBarBox(
    child: Row(
      children: [
        Expanded(child: MoveWindow(child: myTitleBarContent)),
        WindowButtons(),
      ],
    ),
  );
}
```

[`bits_dojo`]: {{site.github}}/bitsdojo/bitsdojo_window

> 注意：Windows 和 Linux 上自定义标题栏会替换原生标题栏，导致集成菜单栏丢失。可在 Flutter 内实现自定义菜单栏作为替代。

## 上下文菜单、工具提示、弹出面板

| 类型 | 触发方式 | 定位锚点 | 消失方式 |
|---|---|---|---|
| **上下文菜单** | 右键点击 | 鼠标位置 | 点击外部/选择菜单项 |
| **工具提示** | 悬停 200-400ms | widget | 鼠标离开 widget |
| **弹出面板 (Flyout)** | 点击 | widget | 点击外部/关闭按钮 |

```dart
// 工具提示
return const Tooltip(
  message: 'I am a Tooltip',
  child: Text('Hover over the text to show a tooltip.'),
);
```

第三方包推荐：`context_menus`、`anchored_popups`、`flutter_portal`、`super_tooltip`、`custom_pop_up_menu`。

## 按钮水平顺序

Windows：确认按钮在左；其他平台：确认按钮在右。

```dart
TextDirection btnDirection = DeviceType.isWindows
    ? TextDirection.rtl
    : TextDirection.ltr;

Row(
  children: [
    const Spacer(),
    Row(
      textDirection: btnDirection,
      children: [
        DialogButton(
          label: 'Cancel',
          onPressed: () => Navigator.pop(context, false),
        ),
        DialogButton(
          label: 'Ok',
          onPressed: () => Navigator.pop(context, true),
        ),
      ],
    ),
  ],
);
```

## 拖放交互

| 输入类型 | 期望行为 |
|---|---|
| 触摸 | 需要可见拖动手柄，或通过长按启动拖动（滚动和拖动共用同一手指） |
| 鼠标 | 无需手柄，选中即可拖动（滚轮/滚动条负责滚动） |

Flutter 实现方式：
- [`Draggable`][] + [`DragTarget`][] API
- `onPan` 手势事件自行处理
- pub.dev 上的预制列表包

[`Draggable`]: {{site.api}}/flutter/widgets/Draggable-class.html
[`DragTarget`]: {{site.api}}/flutter/widgets/DragTarget-class.html

---

## 键盘导航与快捷键

### FocusableActionDetector

组合 focus、鼠标输入、快捷键的 widget：

```dart
class _BasicActionDetectorState extends State<BasicActionDetector> {
  bool _hasFocus = false;

  @override
  Widget build(BuildContext context) {
    return FocusableActionDetector(
      onFocusChange: (value) => setState(() => _hasFocus = value),
      actions: <Type, Action<Intent>>{
        ActivateIntent: CallbackAction<Intent>(
          onInvoke: (intent) {
            print('Enter or Space was pressed!');
            return null;
          },
        ),
      },
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          const FlutterLogo(size: 100),
          if (_hasFocus)
            Positioned(
              left: -4, top: -4, bottom: -4, right: -4,
              child: _roundedBorder(),
            ),
        ],
      ),
    );
  }
}
```

### 遍历顺序控制

使用 `FocusTraversalGroup` 控制 Tab 焦点顺序：

```dart
Column(
  children: [
    FocusTraversalGroup(child: MyFormWithMultipleColumnsAndRows()),
    SubmitButton(),
  ],
);
```

### 全局键盘快捷键

```dart
// 定义 Intent 和 Action
class CreateNewItemIntent extends Intent {
  const CreateNewItemIntent();
}

@override
void initState() {
  super.initState();
  HardwareKeyboard.instance.addHandler(_handleKey);
}

@override
void dispose() {
  HardwareKeyboard.instance.removeHandler(_handleKey);
  super.dispose();
}

bool _handleKey(KeyEvent event) {
  bool isShiftDown = isKeyDown({
    LogicalKeyboardKey.shiftLeft,
    LogicalKeyboardKey.shiftRight,
  });

  if (isShiftDown && event.logicalKey == LogicalKeyboardKey.keyN) {
    _createNewItem();
    return true;
  }
  return false;
}
```

```dart
// Shortcuts widget（局部快捷键）
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

## 鼠标交互

### 自定义光标

```dart
return MouseRegion(
  cursor: SystemMouseCursors.click,
  onTap: () {
    Focus.of(context).requestFocus();
    _submit();
  },
  child: Logo(showBorder: hasFocus),
);
```

### 悬停效果

```dart
return MouseRegion(
  onEnter: (_) => setState(() => _isMouseOver = true),
  onExit: (_) => setState(() => _isMouseOver = false),
  onHover: (e) => print(e.localPosition),
  child: Container(
    height: 500,
    color: _isMouseOver ? Colors.blue : Colors.black,
  ),
);
```

## 视觉密度（Visual Density）

`VisualDensity` 调整整个应用的交互密度——触摸设备需要更大点击区域，桌面可以更紧凑。

```dart
double densityAmt = touchMode ? 0.0 : -1.0;  // 触摸:标准密度，桌面:紧凑
VisualDensity density = VisualDensity(
  horizontal: densityAmt,
  vertical: densityAmt,
);

return MaterialApp(
  theme: ThemeData(visualDensity: density),
  home: MainAppScaffold(),
);

// 1 density unit ≈ 6 logical pixels
```

## 设计注意事项

| 建议 | 说明 |
|---|---|
| 优先触摸体验 | 先构建出色的触摸 UI，再为鼠标用户优化密度 |
| 不要锁定屏幕方向 | 应用应能适应不同大小和形状的窗口 |
| 不要根据设备类型判断布局 | 根据窗口可用空间决定 |
| 不要占用全部水平空间 | 使用 `GridView` 或 `ConstrainedBox` 限制最大宽度 |
| 保持列表滚动状态 | 方向改变时使用 `PageStorageKey` 恢复滚动位置 |
| 支持多种输入设备 | 鼠标、触控板、键盘快捷键、辅助功能 |

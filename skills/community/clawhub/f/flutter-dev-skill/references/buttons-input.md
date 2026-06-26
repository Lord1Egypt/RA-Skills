---
name: flutter-buttons-input
description: Flutter Buttons, Text Fields, Input 组件详解。
source: https://flutter.cn/docs
---

# Buttons, Text Fields & Input Components

## Buttons (M2 → M3)

### 新按钮 API 概述

Flutter M3 引入了全新的按钮组件体系，替代了旧的 `FlatButton`、`RaisedButton`、`OutlineButton`：

| Old Widget | Old Theme | New Widget | New Theme |
|------------|-----------|------------|-----------|
| `FlatButton` | `ButtonTheme` | `TextButton` | `TextButtonTheme` |
| `RaisedButton` | `ButtonTheme` | `ElevatedButton` | `ElevatedButtonTheme` |
| `OutlineButton` | `ButtonTheme` | `OutlinedButton` | `OutlinedButtonTheme` |

### ButtonStyle 核心概念

新按钮使用 `ButtonStyle` 配置视觉属性，替代了原来的大量独立参数：

```dart
TextButton(
  style: ButtonStyle(
    foregroundColor: MaterialStateProperty.all<Color>(Colors.blue),
    overlayColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.hovered))
          return Colors.blue.withOpacity(0.04);
        if (states.contains(MaterialState.focused) ||
            states.contains(MaterialState.pressed))
          return Colors.blue.withOpacity(0.12);
        return null;
      },
    ),
  ),
  onPressed: () { },
  child: Text('TextButton'),
)
```

### styleFrom() 便捷方法

每个按钮类提供 `styleFrom()` 方法简化样式创建：

```dart
// 自定义前景色
TextButton(
  style: TextButton.styleFrom(
    foregroundColor: Colors.blue,
    disabledForegroundColor: Colors.red,
  ),
  onPressed: () { },
  child: Text('TextButton'),
)

// 自定义背景色和前景色
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.red,
    foregroundColor: Colors.white,
  ),
  onPressed: () { },
  child: Text('ElevatedButton'),
)

// 自定义形状
OutlinedButton(
  style: OutlinedButton.styleFrom(
    shape: StadiumBorder(),
    side: BorderSide(color: Colors.red, width: 2),
  ),
  onPressed: () { },
  child: Text('OutlinedButton'),
)
```

### 恢复 M2 按钮外观

```dart
// 恢复 FlatButton 外观
final ButtonStyle flatButtonStyle = TextButton.styleFrom(
  foregroundColor: Colors.black87,
  minimumSize: Size(88, 36),
  padding: EdgeInsets.symmetric(horizontal: 16),
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.all(Radius.circular(2)),
  ),
);

// 恢复 RaisedButton 外观
final ButtonStyle raisedButtonStyle = ElevatedButton.styleFrom(
  foregroundColor: Colors.black87,
  backgroundColor: Colors.grey[300],
  minimumSize: Size(88, 36),
  padding: EdgeInsets.symmetric(horizontal: 16),
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.all(Radius.circular(2)),
  ),
);

// 全局应用主题
MaterialApp(
  theme: ThemeData.from(colorScheme: ColorScheme.light()).copyWith(
    textButtonTheme: TextButtonThemeData(style: flatButtonStyle),
    elevatedButtonTheme: ElevatedButtonThemeData(style: raisedButtonStyle),
    outlinedButtonTheme: OutlinedButtonThemeData(style: outlineButtonStyle),
  ),
)
```

### 状态相关颜色

```dart
// 自定义 overlay 颜色
TextButton(
  style: ButtonStyle(
    overlayColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.focused)) return Colors.red;
        if (states.contains(MaterialState.hovered)) return Colors.green;
        if (states.contains(MaterialState.pressed)) return Colors.blue;
        return null;
      },
    ),
  ),
  onPressed: () { },
  child: Text('TextButton'),
)

// 自定义禁用颜色
ElevatedButton(
  style: ButtonStyle(
    backgroundColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.disabled)) return Colors.red;
        return null;
      },
    ),
    foregroundColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.disabled)) return Colors.blue;
        return null;
      },
    ),
  ),
  onPressed: null,
  child: Text('ElevatedButton'),
)
```

### 自定义 Elevation

```dart
// 使用 styleFrom
ElevatedButton(
  style: ElevatedButton.styleFrom(elevation: 2),
  onPressed: () { },
  child: Text('ElevatedButton with custom elevation'),
)

// 单独覆盖某个状态
ElevatedButton(
  style: ButtonStyle(
    elevation: MaterialStateProperty.resolveWith<double?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.pressed)) return 16;
        return null;
      },
    ),
  ),
  onPressed: () { },
  child: Text('ElevatedButton with custom elevation'),
)
```

---

## Text Fields & Input

### TextSelectionTheme 迁移

M3 将文本选择相关属性迁移到 `TextSelectionTheme`：

| Before | After |
|--------|-------|
| `ThemeData.cursorColor` | `TextSelectionThemeData.cursorColor` |
| `ThemeData.textSelectionColor` | `TextSelectionThemeData.selectionColor` |
| `ThemeData.textSelectionHandleColor` | `TextSelectionThemeData.selectionHandleColor` |

```dart
// 迁移前
ThemeData(
  cursorColor: Colors.red,
  textSelectionColor: Colors.green,
  textSelectionHandleColor: Colors.blue,
)

// 迁移后
ThemeData(
  textSelectionTheme: TextSelectionThemeData(
    cursorColor: Colors.red,
    selectionColor: Colors.green,
    selectionHandleColor: Colors.blue,
  ),
)

// 恢复旧默认值 (Light)
ThemeData(
  textSelectionTheme: TextSelectionThemeData(
    cursorColor: const Color.fromRGBO(66, 133, 244, 1.0),
    selectionColor: const Color(0xff90caf9),
    selectionHandleColor: const Color(0xff64b5f6),
  ),
)

// 恢复旧默认值 (Dark)
ThemeData(
  textSelectionTheme: TextSelectionThemeData(
    cursorColor: const Color.fromRGBO(66, 133, 244, 1.0),
    selectionColor: const Color(0xff64ffda),
    selectionHandleColor: const Color(0xff1de9b6),
  ),
)
```

### 焦点与键盘导航

```dart
// 使用 FocusableActionDetector
class _BasicActionDetectorState extends State<BasicActionDetector> {
  bool _hasFocus = false;
  @override
  Widget build(BuildContext context) {
    return FocusableActionDetector(
      onFocusChange: (value) => setState(() => _hasFocus = value),
      actions: <Type, Action<Intent>>{
        ActivateIntent: CallbackAction<ActivateIntent>(
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

// 控制遍历顺序
Column(
  children: [
    FocusTraversalGroup(child: MyFormWithMultipleColumnsAndRows()),
    SubmitButton(),
  ],
)

// 键盘快捷键
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

// 全局键盘监听
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

### Visual Density

```dart
double densityAmt = touchMode ? 0.0 : -1.0;
VisualDensity density = VisualDensity(
  horizontal: densityAmt,
  vertical: densityAmt,
);
return MaterialApp(
  theme: ThemeData(visualDensity: density),
  home: MainAppScaffold(),
);

// 获取当前 density
VisualDensity density = Theme.of(context).visualDensity;
```

---

## Checkbox

### fillColor 行为更新

M3 中 `Checkbox.fillColor` 现在应用于未选中状态的背景色。

```dart
// M3 行为 (fillColor 应用于背景)
Checkbox(
  fillColor: MaterialStateProperty.resolveWith((states) {
    if (!states.contains(MaterialState.selected)) {
      return Colors.transparent;
    }
    return null;
  }),
  side: const BorderSide(color: Colors.red, width: 2),
  value: _checked,
  onChanged: _enabled
    ? (bool? value) {
        setState(() { _checked = value!; });
      }
    : null,
)

// 通过主题配置
checkboxTheme: CheckboxThemeData(
  fillColor: MaterialStateProperty.resolveWith((states) {
    if (!states.contains(MaterialState.selected)) {
      return Colors.transparent;
    }
    return null;
  }),
  side: const BorderSide(color: Colors.red, width: 2),
)
```

---

## Toggleable Widgets (Switch, Radio)

### toggleableActiveColor 废弃

`ThemeData.toggleableActiveColor` 已废弃，改用 `ColorScheme.secondary`。

```dart
// 迁移前
MaterialApp(
  theme: ThemeData(toggleableActiveColor: myColor),
)

// 迁移后
final ThemeData theme = ThemeData();
MaterialApp(
  theme: theme.copyWith(
    switchTheme: SwitchThemeData(
      thumbColor: MaterialStateProperty.resolveWith<Color?>(
        (Set<MaterialState> states) {
          if (states.contains(MaterialState.disabled)) return null;
          if (states.contains(MaterialState.selected)) return myColor;
          return null;
        },
      ),
      trackColor: MaterialStateProperty.resolveWith<Color?>(
        (Set<MaterialState> states) {
          if (states.contains(MaterialState.disabled)) return null;
          if (states.contains(MaterialState.selected)) return myColor;
          return null;
        },
      ),
    ),
    radioTheme: RadioThemeData(
      fillColor: MaterialStateProperty.resolveWith<Color?>(
        (Set<MaterialState> states) {
          if (states.contains(MaterialState.disabled)) return null;
          if (states.contains(MaterialState.selected)) return myColor;
          return null;
        },
      ),
    ),
    checkboxTheme: CheckboxThemeData(
      fillColor: MaterialStateProperty.resolveWith<Color?>(
        (Set<MaterialState> states) {
          if (states.contains(MaterialState.disabled)) return null;
          if (states.contains(MaterialState.selected)) return myColor;
          return null;
        },
      ),
    ),
  ),
)
```

# Controls

> 来源：Apple HIG - Controls (2026)
> https://developer.apple.com/design/human-interface-guidelines/controls

## Toggle

### 设计规范
- 使用描述性标签说明功能（不是 "On/Off"）
- 标签放在开关右侧（iOS）或左侧（macOS）
- 即时反馈，不需要确认按钮

### 标签示例

| ✅ 正确 | ❌ 错误 |
|---------|--------|
| 深色模式 | On/Off |
| 自动保存 | Enabled |
| 推送通知 | Toggle |

### 实现（SwiftUI）

```swift
Toggle("深色模式", isOn: $isDarkMode)

Toggle(isOn: $notifications) {
    Label("推送通知", systemImage: "bell")
}
```

### 实现（UIKit）

```swift
let toggle = UISwitch()
toggle.isOn = true
toggle.onTintColor = .systemBlue  // 开启颜色
toggle.addTarget(self, action: #selector(toggleChanged), for: .valueChanged)
```

---

## Slider

### 设计规范
- 显示当前值（必要时）
- 设置合理的最小/最大值
- 用于连续值（如音量、亮度）

### 实现（SwiftUI）

```swift
@State private var volume: Double = 0.5

VStack {
    Slider(value: $volume, in: 0...1)
    Text("\(Int(volume * 100))%")
}
```

### 实现（UIKit）

```swift
let slider = UISlider()
slider.minimumValue = 0
slider.maximumValue = 100
slider.value = 50
slider.addTarget(self, action: #selector(sliderChanged), for: .valueChanged)
```

---

## Segmented Control

### 设计规范
- 2-5 个分段
- 等宽分段
- 图标 + 文字 或 纯文字
- 选中状态明确

### 实现（SwiftUI）

```swift
@State private var selected = 0

Picker("视图", selection: $selected) {
    Text("列表").tag(0)
    Text("网格").tag(1)
    Text("卡片").tag(2)
}
.pickerStyle(.segmented)
```

### 实现（UIKit）

```swift
let segmentControl = UISegmentedControl(items: ["列表", "网格", "卡片"])
segmentControl.selectedSegmentIndex = 0
segmentControl.addTarget(self, action: #selector(segmentChanged), for: .valueChanged)
```

---

## DatePicker

### 设计规范
- 选择日期、时间或日期+时间
- Compact 模式适合表单
- Wheel 模式适合精确选择
- Graphical 模式适合日历视图

### 模式适用场景

| 模式 | 适用场景 | 平台 |
|------|---------|------|
| Graphical | 主屏幕日历视图，日期可视化 | iOS |
| Compact | 表单内紧凑选择，节省空间 | iOS 16+ |
| Wheel | 需要精确时间，滚轮快速浏览 | iOS / tvOS |
| Inline | Mac 嵌入式日历，悬停展开 | macOS |

### 实现（SwiftUI）

```swift
@State private var selectedDate = Date()

// 日期
DatePicker("日期", selection: $selectedDate, displayedComponents: .date)

// 日期+时间
DatePicker("预约", selection: $selectedDate)

// 范围
DatePicker("提醒", selection: $reminder, in: Date()..., displayedComponents: [.date, .hourAndMinute])
```

### 实现（UIKit）

```swift
let datePicker = UIDatePicker()
datePicker.datePickerMode = .dateAndTime
datePicker.preferredDatePickerStyle = .compact  // .wheels / .graphical / .inline
datePicker.minimumDate = Date()
datePicker.addTarget(self, action: #selector(dateChanged), for: .valueChanged)
```

---

## ColorWell

### 使用场景
- 颜色选择器
- App Icon 编辑器
- 主题定制

### 实现（SwiftUI）

```swift
@State private var selectedColor = Color.blue

ColorPicker("选择颜色", selection: $selectedColor)
```

### 实现（UIKit）

```swift
let colorWell = UIColorWell()
colorWell.selectedColor = .systemBlue
colorWell.addTarget(self, action: #selector(colorChanged), for: .valueChanged)
```

---

## Stepper

### 设计规范
- 数值调整（+/-）
- 显示当前值
- 设置步长和范围

### 实现（SwiftUI）

```swift
@State private var quantity = 1

Stepper("数量: \(quantity)", value: $quantity, in: 1...99)

Stepper("数量", value: $quantity, in: 1...99, step: 5)
```

### 实现（UIKit）

```swift
let stepper = UIStepper()
stepper.minimumValue = 1
stepper.maximumValue = 99
stepper.stepValue = 1
stepper.value = 1
stepper.addTarget(self, action: #selector(stepperChanged), for: .valueChanged)

@objc func stepperChanged() {
    quantityLabel.text = "\(Int(stepper.value))"
}
```

---

## Progress

### 类型

| 类型 | 使用场景 |
|------|---------|
| Linear | 下载、加载、进度反馈 |
| Circular | 处理中、转圈等待 |

### 实现（SwiftUI）

```swift
// 线性进度
ProgressView(value: progress)
    .progressViewStyle(.linear)

// 圆形
ProgressView()
    .progressViewStyle(.circular)

// 带标签
ProgressView(value: 0.7) {
    Text("加载中...")
}
```

### 实现（UIKit）

```swift
// UIProgressView
let progressView = UIProgressView(progressViewStyle: .default)
progressView.progress = 0.5  // 0.0 - 1.0
progressView.progressTintColor = .systemBlue
progressView.trackTintColor = .systemGray5
progressView.frame = CGRect(x: 0, y: 0, width: 200, height: 10)

// UIActivityIndicatorView
let indicator = UIActivityIndicatorView(style: .large)
indicator.startAnimating()
indicator.color = .systemBlue
indicator.hidesWhenStopped = true
```

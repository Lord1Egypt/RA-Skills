# Container Components

> 来源：Apple HIG - Alerts, Action Sheets, Dialogs (2026)
> https://developer.apple.com/design/human-interface-guidelines/alerts

## Alert

### 使用原则
- 用于关键信息或不可逆操作确认
- 标题简洁明了
- 提供明确的操作选项
- 避免频繁使用

### Alert 类型

| 类型 | 场景 |
|------|------|
| Simple | 信息提示 |
| Extended | 需要描述 |
| Action | 需要用户操作 |

### 实现（SwiftUI）

```swift
// 简单 Alert
Alert(title: Text("错误"), message: Text("网络连接失败"), dismissButton: .default(Text("确定")))

// 多按钮 Alert
Alert(
    title: Text("删除"),
    message: Text("确定要删除这个项目吗？此操作无法撤销。"),
    primaryButton: .destructive(Text("删除")),
    secondaryButton: .cancel()
)
```

### 实现（UIKit）

```swift
let alert = UIAlertController(
    title: "删除",
    message: "确定要删除这个项目吗？此操作无法撤销。",
    preferredStyle: .alert
)

alert.addAction(UIAlertAction(title: "取消", style: .cancel))
alert.addAction(UIAlertAction(title: "删除", style: .destructive) { _ in
    // 删除逻辑
})

present(alert, animated: true)
```

---

## Action Sheet

### 使用原则
- 提供多个操作选项
- 可取消操作
- 移动端底部弹出

### 实现（SwiftUI）

```swift
struct ContentView: View {
    @State private var showingActionSheet = false

    Button("更多操作") {
        showingActionSheet = true
    }
    .confirmationDialog("选择操作", isPresented: $showingActionSheet, titleVisibility: .visible) {
        Button("分享") { }
        Button("收藏") { }
        Button("删除", role: .destructive) { }
        Button("取消", role: .cancel) { }
    }
}
```

### 实现（UIKit）

```swift
let actionSheet = UIAlertController(
    title: nil,
    message: nil,
    preferredStyle: .actionSheet
)

actionSheet.addAction(UIAlertAction(title: "分享", style: .default) { _ in })
actionSheet.addAction(UIAlertAction(title: "收藏", style: .default) { _ in })
actionSheet.addAction(UIAlertAction(title: "删除", style: .destructive) { _ in })
actionSheet.addAction(UIAlertAction(title: "取消", style: .cancel))

// iPad 需要设置 popover
if let popover = actionSheet.popoverPresentationController {
    popover.sourceView = button
    popover.sourceRect = button.bounds
}
```

---

## Modal / Sheet

### 设计规范
- 从底部滑出
- 可拖动关闭
- 支持不同 detents（iOS 16+）
- 提供关闭按钮

### iOS 16+ Sheet Detents

| Detent | 高度 |
|--------|------|
| Small | ~37% |
| Medium | ~63% |
| Large | 全屏 |
| Custom | 自定义 |

### 实现（SwiftUI）

```swift
struct DetailView: View {
    @Environment(\.dismiss) var dismiss

    Button("关闭") {
        dismiss()
    }
}

// 展示 Sheet
.sheet(isPresented: $showingDetail) {
    DetailView()
}

// 多 detent 支持
.sheet(item: $selectedItem) { item in
    DetailView(item: item)
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}
```

### 实现（UIKit）

```swift
let modalVC = ModalViewController()
modalVC.modalPresentationStyle = .pageSheet

if let sheet = modalVC.sheetPresentationController {
    sheet.detents = [.medium(), .large()]
    sheet.prefersGrabberVisible = true
}

present(modalVC, animated: true)
```

---

## Popover

### 使用原则
- 显示附加信息
- 非模态，点击外部关闭
- 箭头指向触发元素

### 实现（SwiftUI）

```swift
struct ContentView: View {
    @State private var showingPopover = false

    Button("更多信息") {
        showingPopover = true
    }
    .popover(isPresented: $showingPopover, attachmentAnchor: .point(.bottom)) {
        Text("这里是详细信息")
            .padding()
    }
}
```

### 实现（UIKit）

```swift
let popover = UIPopoverController(contentViewController: infoVC)
popover.contentViewController.preferredContentSize = CGSize(width: 300, height: 200)
popover.present(from: button.bounds, in: button, permittedArrowDirections: .up, animated: true)
```

---

## Menu

### 类型

| 类型 | 触发方式 |
|------|---------|
| Action | 点击 |
| Context | 长按/右键 |
| Dropdown | 导航栏/工具栏 |

### 实现（SwiftUI）

```swift
// Action Menu
Menu {
    Button("分享", action: share)
    Button("收藏", action: favorite)
    Divider()
    Button("删除", role: .destructive, action: delete)
} label: {
    Label("更多", systemImage: "ellipsis.circle")
}

// Context Menu
struct ItemView: View {
    var body: some View {
        Image("photo")
            .contextMenu {
                Button("分享", action: share)
                Button("删除", role: .destructive, action: delete)
            }
    }
}
```

### 实现（UIKit）

```swift
// UIMenu
let menu = UIMenu(title: "", children: [
    UIAction(title: "分享", image: UIImage(systemName: "square.and.arrow.up"), handler: { _ in }),
    UIAction(title: "收藏", image: UIImage(systemName: "heart"), handler: { _ in }),
    UIAction(title: "删除", image: UIImage(systemName: "trash"), attributes: .destructive, handler: { _ in })
])

button.menu = menu
button.showsMenuAsPrimaryAction = true
```

---

## Dialog

### 使用场景
- macOS 主要交互方式
- 需要用户输入
- 确认操作

### 实现（macOS）

```swift
// SwiftUI
struct SettingsView: View {
    @State private var showingDialog = false

    Button("重置") {
        showingDialog = true
    }
    .alert("重置设置", isPresented: $showingDialog) {
        Button("取消", role: .cancel) { }
        Button("重置", role: .destructive) { }
    } message: {
        Text("确定要重置所有设置吗？")
    }
}
```

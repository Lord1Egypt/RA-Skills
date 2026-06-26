# Apple Watch HIG

> 来源：Apple Watch Human Interface Guidelines（2026-04-23）
> https://developer.apple.com/design/human-interface-guidelines/watchos/overview/

## 设计理念

Apple Watch 是一款 **贴身设备** — 它时刻陪伴用户，提供及时、相关的信息和操作。

### 三大核心原则

| 原则 | 说明 | 示例 |
|------|------|------|
| Reduce | 最小化交互 | 复杂 App → 一键操作 |
| Context | 情境感知 | 时间/位置触发通知 |
| Timely | 及时响应 | 紧急 SOS、秒表 |

---

## WatchFace 表盘

### 表盘类型

| 类型 | 描述 | 适用场景 |
|------|------|---------|
| Modular | 数字+复杂功能 | 信息密集型用户 |
| Analog | 传统指针 | 简约风格 |
| California | 混合字体 | 经典+数字 |
| Nike Hybrid | 动态+数字 | 运动爱好者 |
| Photos | 用户照片 | 个性化 |
| GMT | 多时区 | 旅行者 |

### WatchFace 设计规范

```swift
// 创建自定义 WatchFace 组件
struct WatchFaceView: View {
    var body: some View {
        ZStack {
            Color.black
            VStack {
                Text("10:30")
                    .font(.system(size: 48, weight: .thin))
                Text("MON 24 APR")
                    .font(.system(size: 12, weight: .regular))
            }
        }
    }
}
```

### 复杂功能（Complications）

| 位置 | 尺寸 | 数据量 |
|------|------|-------|
| Corner（左上） | 40×40pt | 1-2 字 |
| Corner（右上） | 40×40pt | 1-2 字 |
| Bottom | 80×40pt | 2-3 字 |
| Center | 40×40pt | 1-2 字 |

---

## 导航架构

### 导航模式

```
App Launch
    ↓
Root View (TabBar 或 PageView)
    ↓
Detail Views (NavigationPush)
    ↓
Modal Sheets (Sheet)
```

### Tab Bar（SwiftUI）

```swift
TabView {
    NavigationStack {
        HomeView()
    }
    .tabItem { Label("首页", systemImage: "house") }

    NavigationStack {
        WorkoutView()
    }
    .tabItem { Label("健身", systemImage: "figure.run") }

    NavigationStack {
        SettingsView()
    }
    .tabItem { Label("设置", systemImage: "gear") }
}
```

### Tab Bar（UIKit）

```swift
class ExtensionDelegate: NSObject, WKExtensionDelegate {
    func applicationDidFinishLaunching() {
        let tabController = WKTabBarController()
        tabController.addTab(with: rootInterfaceController)
    }
}
```

---

## 通知系统

### 通知层级

| 层级 | 高度 | 内容 |
|------|------|------|
| Short-Look | 44pt | 应用图标+标题 |
| Long-Look | 80-120pt | 完整内容+操作 |
| Notification | 全屏 | 消息详情 |

### 通知操作

```swift
// 定义通知操作
struct NotificationActions {
    static let reply = WKNotificationAction(
        identifier: "REPLY_ACTION",
        title: "回复",
        actionBackgroundColor: .blue
    )

    static let dismiss = WKNotificationAction(
        identifier: "DISMISS_ACTION",
        title: "忽略",
        actionBackgroundColor: .gray
    )
}
```

---

## 手势系统

### 可用手势

| 手势 | 描述 | 响应 |
|------|------|------|
| Tap | 点击 | 选中/触发 |
| Swipe | 滑动手势 | 切换页面/返回 |
| Long Press | 长按 | 上下文菜单 |
| Force Touch | 重按 | Peek/Pop |
| Digital Crown | 旋轮 | 滚动/缩放 |

### Haptic 反馈

```swift
import WatchKit

// 触觉反馈
WKInterfaceDevice.current().play(.click)     // 点击
WKInterfaceDevice.current().play(.success)  // 成功
WKInterfaceDevice.current().play(.failure)  // 失败
WKInterfaceDevice.current().play(.start)    // 开始
WKInterfaceDevice.current().play(.stop)     // 停止
```

---

## Health & Fitness

### 健康数据类型

| 类型 | 单位 | 更新频率 |
|------|------|---------|
| 心率 | BPM | 实时 |
| 步数 | 步 | 每分钟 |
| 卡路里 | kcal | 每分钟 |
| 活动圆环 | % | 实时 |
| 血氧 | % | 按需 |

### 健康Kit 集成

```swift
import HealthKit

let healthStore = HKHealthStore()

// 查询心率
func fetchHeartRate() {
    let heartRate = HKQuantityType.quantityType(forIdentifier: .heartRate)!
    let query = HKSampleQuery(
        sampleType: heartRate,
        predicate: nil,
        limit: 1,
        sortDescriptors: [NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)]
    ) { _, samples, _ in
        if let sample = samples?.first as? HKQuantitySample {
            let heartRate = sample.quantity.doubleValue(for: HKUnit.count().unitDivided(by: .minute()))
        }
    }
    healthStore.execute(query)
}
```

---

## App Structure

### App 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Watch-Only | 仅手表端 | 计时器、秒表 |
| Watch + iPhone | 协同工作 | 健身+手机 |
| Watch + Companion | iPad/Mac | 指南针 |

### 数据同步

```swift
// WatchConnectivity
import WatchConnectivity

class ConnectivityManager: NSObject, WCSessionDelegate {
    static let shared = ConnectivityManager()

    func session(_ session: WCSession, didReceiveUserInfo userInfo: [String: Any]) {
        // 从手机接收数据
        if let data = userInfo["key"] as? Data {
            // 处理数据
        }
    }

    func sendToPhone(_ message: [String: Any]) {
        if WCSession.default.isReachable {
            WCSession.default.sendMessage(message, replyHandler: nil)
        }
    }
}
```

---

## UI Components

### 常用组件

| 组件 | SwiftUI | UIKit |
|------|---------|-------|
| 按钮 | Button | WKInterfaceButton |
| 列表 | List | WKInterfaceTable |
| 分组 | Group | WKInterfaceGroup |
| 开关 | Toggle | WKInterfaceSwitch |
| 滑块 | Slider | WKInterfaceSlider |
| 菜单 | Menu | WKInterfaceMenu |
| 加载 | ProgressView | WKInterfaceImage (animated) |

### 示例代码

```swift
// 按钮
Button(action: {
    WKInterfaceDevice.current().play(.click)
}) {
    Label("开始", systemImage: "play.fill")
}
.buttonStyle(.borderedProminent)

// 列表
List {
    ForEach(items) { item in
        Text(item.name)
    }
}

// 开关
Toggle(isOn: $isEnabled) {
    Text("通知")
}

// 菜单
Menu {
    Button("收藏", action: favorite)
    Button("分享", action: share)
    Button("删除", systemImage: "trash", role: .destructive, action: delete)
} label: {
    Label("更多", systemImage: "ellipsis.circle")
}
```

---

## 性能优化

### 能耗考虑

| 操作 | 能耗 | 建议 |
|------|------|------|
| CPU 高负载 | ⚡⚡⚡ | 减少后台任务 |
| 屏幕常亮 | ⚡⚡ | 使用 Always-On |
| GPS 持续 | ⚡⚡⚡ | 按需启用 |
| 心率传感 | ⚡ | 正常 |
| WiFi 连接 | ⚡⚡ | 批处理请求 |

### 优化策略

```swift
// 延迟加载
@State private var isLoaded = false

var body: some View {
    if isLoaded {
        ContentView()
    } else {
        ProgressView()
            .task {
                await loadData()
            }
    }
}

// 后台刷新
WKApplication.shared().scheduleBackgroundRefresh {
    // 定期更新复杂功能
}
```

---

## 来源

> Apple Watch Human Interface Guidelines
> https://developer.apple.com/design/human-interface-guidelines/watchos/overview/

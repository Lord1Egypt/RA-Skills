# SDK 选型决策树

## 决策流程

```
你的应用是什么类型？
│
├── 微信小程序 ──────────→ 小程序 SDK
│   支持框架：原生 / Taro / uni-app / WePY / mpvue / Kbone / remax
│
├── 微信小游戏 ──────────→ 小游戏 SDK
│   ├── IAA 小游戏（广告变现）→ 需提前填写申请表
│   └── 支持引擎：原生 / LayaAir / CocosCreator / Egret / Unity
│
├── iOS App ─────────────→ APP SDK (iOS)
│   语言：Objective-C / Swift
│
├── Android App ─────────→ APP SDK (Android)
│   语言：Java / Kotlin
│   渠道标识：通过 ChannelType 枚举指定
│
├── 鸿蒙 App (HarmonyOS) → 鸿蒙 SDK
│   语言：ArkTS
│   要求：华为开发者账号
│
├── Web / H5 页面 ───────→ JS SDK 或 API 接入
│   （超出本 Skill 范围，参考 DataNexus 文档站）
│
└── 服务端直传 ──────────→ API 接入
    （超出本 Skill 范围，参考 API 接入指引）
```

## SDK 对比表

| 维度 | 小程序 SDK | 小游戏 SDK | APP SDK (iOS) | APP SDK (Android) | 鸿蒙 SDK |
|------|-----------|-----------|--------------|-------------------|----------|
| **适用场景** | 微信小程序 | 微信小游戏 | iOS 应用 | Android 应用 | 鸿蒙应用 |
| **开发语言** | JavaScript | JavaScript | ObjC/Swift | Java/Kotlin | ArkTS |
| **安装方式** | npm / 链接下载 | npm / 链接下载 | CocoaPods / 手动 | Gradle / 手动 | ohpm / 手动 |

## 通用前置条件

### 1. 创建数据源

在 [DataNexus 平台](https://datanexus.qq.com) 创建对应类型的数据源。

### 2. 获取接入参数

- **user_action_set_id**：数据源 ID（纯数字）
- **secret_key**：数据源密钥

### 3. 开启分发开关

#### 小程序 / 小游戏端

| 开关 | 是否开启 |
|------|---------|
| 一方数据合作 | ✅ 开启 |
| 转化归因 | ✅ 开启 |

#### iOS APP / 非游戏 Android APP 端

| 开关 | 是否开启 | 说明 |
|------|---------|------|
| 一方数据合作 | ✅ 开启 | — |
| 预归因 | ✅ 开启 | 需联系行业运营按主体/账号维度申请加白 |
| 智能场景匹配 | ✅ 开启 | 与预归因配合使用 |
| 转化归因 | ❌ **不开启** | 用于预归因的数据源**无需**开启转化归因开关 |

#### 游戏类 Android APP 端

| 开关 | 是否开启 |
|------|---------|
| 一方数据合作 | ✅ 开启 |
| 转化归因 | ✅ 开启 |

### 4. 安全域名配置（小程序/小游戏端）

```
https://api.datanexus.qq.com
```

### 5. 申请微信 AppID 关联（小程序/小游戏端）

1. **发起申请**：DataNexus 平台 → 数据接入 → 工具箱 → 申请微信 AppID
2. **管理员确认**：两个工作日内完成审批

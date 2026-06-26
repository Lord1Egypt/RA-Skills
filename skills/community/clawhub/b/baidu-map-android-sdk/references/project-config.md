# 工程配置

**边界**：AndroidManifest、Gradle 混淆、百度 SDK 相关工程配置；Gradle 依赖见 [gradle.md](gradle.md)。

## AndroidManifest

### 配置 AK

在 `<application>` 内添加 meta-data：

```xml
<meta-data
    android:name="com.baidu.lbsapi.API_KEY"
    android:value="您的AK" />
```

也可在代码中通过 `SDKInitializer.setApiKey("您的AK")` 设置（**必须在 `initialize` 之前**调用，且优先于 Manifest 中的 meta-data）。

**控制台配置**：在百度开放平台「应用管理 - 我的应用」创建应用，应用类型选 **Android SDK**；包名填写与 `build.gradle` 中 **applicationId** 完全一致；SHA1 填写调试/发布签名对应值（调试：`keytool -list -v -keystore ~/.android/debug.keystore`，默认口令 `android`）。勾选所需服务（地图、检索、路线规划等），未勾选则对应能力鉴权不通过。

### AK 鉴权结果与排查

- **鉴权方式**：SDK 在 `initialize` 后异步向服务端校验 AK，结果通过**广播**通知。
- **广播 Action**（常量在 `SDKInitializer` 中）：
  - `SDK_BROADTCAST_ACTION_STRING_PERMISSION_CHECK_OK`：AK 验证成功。
  - `SDK_BROADTCAST_ACTION_STRING_PERMISSION_CHECK_ERROR`：AK 验证失败；Intent 附加 `SDK_BROADTCAST_INTENT_EXTRA_INFO_KEY_ERROR_CODE`（int）、`SDK_BROADTCAST_INTENT_EXTRA_INFO_KEY_ERROR_MESSAGE`（String）。
  - `SDK_BROADCAST_ACTION_STRING_NETWORK_ERROR`：网络错误，鉴权可能未完成。
- **监听方式**：在 Activity 或 Application 中注册 `BroadcastReceiver`，过滤上述 Action；在 `onResume` 注册、`onPause` 注销，避免泄漏。收到 OK 可提示“鉴权成功”，收到 ERROR 可提示错误码与错误信息便于排查。
- **常见失败原因**：包名与控制台不一致（必须与 applicationId 一致）；SHA1 与当前签名不一致（换 keystore 或打包方式后需更新控制台 SHA1）；控制台未勾选对应服务（如路线规划）；网络不可用。错误码含义见 [errorcode.md](errorcode.md)（如 101 AK 不存在、200 APP 不存在/AK 有误、240 服务被禁用）。

### 权限

在 manifest 中声明所需权限，例如：

```xml
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

自 Android 6.0 起，危险权限需在运行时申请。

### 主题与 Activity（避免闪退）

使用 **AppCompatActivity** 时，`<application>` 的 `android:theme` 必须为 **Theme.AppCompat** 或其子类（如 `Theme.AppCompat.Light.NoActionBar`）。若使用系统主题 `@android:style/Theme.Material.Light.NoActionBar`，会在 `setContentView` 时抛出：

`IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity.`

推荐在 AndroidManifest 中设置：

```xml
android:theme="@style/Theme.AppCompat.Light.NoActionBar"
```

（由 `androidx.appcompat` 提供，无需在 styles.xml 中再定义。）

### 定位 Service（使用定位时）

使用地图定位或定位 SDK 时，在 `<application>` 内声明定位服务组件（具体组件名以当前 SDK 文档为准，例如）：

```xml
<service
    android:name="com.baidu.location.f"
    android:enabled="true"
    android:process=":remote" />
```

请以官方「显示定位」或「Android Studio 配置」文档中的声明为准。

## 混淆（ProGuard）

发布包混淆时，百度地图相关类不得被混淆，否则易出现网络不可用等运行时异常。

1. 在 app 的 `build.gradle` 的 `buildTypes.release`（若 debug 也混淆则一并配置）中启用混淆规则文件：

```gradle
buildTypes {
    release {
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

2. 在 `proguard-rules.pro` 中添加：

```
-keep class com.baidu.** { *; }
-keep class vi.com.** { *; }
-keep class com.baidu.vi.** { *; }
-dontwarn com.baidu.**
```

## 资源说明（V5.1.0+）

自 V5.1.0 起，部分原 jar 内图片资源移至官方示例工程的 assets，若使用到路线/公交等 Overlay 图标，可从官网下载对应 Android 示例工程，将 `app/src/main/assets/` 下相关资源拷贝到本工程 assets。常见文件名包括：Icon_end.png、Icon_start.png、Icon_line_node.png、Icon_bus_station.png、Icon_subway_station.png、Icon_walk_route.png 等。步骑行导航一体化包解压后若带 assets 目录，也需拷贝到项目 assets。

## 集成经验与常见问题

以下为实际集成地图展示时的常见坑与建议，便于一次跑通。

**排查顺序**（Agent 建议遵守）：先确认 **主题**（AppCompat）与 **compileSdk**（如 34）；再确认 **Application** 中隐私与 `initialize` 顺序、**AK/包名/SHA1** 与控制台一致；仍有闪退或地图不显示时查 **Logcat**（MapApplication、MainActivity、AndroidRuntime）及 **MapView 生命周期**（onResume/onPause/onDestroy 是否调用）。

| 问题 | 原因 / 建议 |
|------|--------------|
| **闪退：You need to use a Theme.AppCompat theme** | 见上文「主题与 Activity」：必须使用 `@style/Theme.AppCompat.Light.NoActionBar` 等 AppCompat 主题，勿用 `@android:style/Theme.Material.*`。 |
| **AAR 要求 compileSdk 34** | 依赖（如 `androidx.activity:activity:1.8.0`）可能要求 compileSdk ≥ 34。在 app 的 `build.gradle` 中设置 `compileSdk = 34`；targetSdk 可单独保留为 33。 |
| **MapView 在部分设备/模拟器上闪退** | 若在 `onCreate` 中立即 `getMap()` 导致崩溃，可将 `getMap()` 延后到 **onResume()** 中首次调用，并做 null 判断与 try-catch，便于排查。 |
| **Application 初始化失败** | Application 中建议用 `catch (Throwable)` 并打 Log（如 `Log.e(TAG, "Baidu SDK init failed", e)`），便于通过 Logcat 确认是否为 SDK 初始化或 AK/包名问题。 |
| **鉴权失败、地图不显示、路线/检索无结果** | 先确认控制台包名=applicationId、SHA1 与当前签名一致、已勾选对应服务；监听鉴权广播（PERMISSION_CHECK_ERROR）获取错误码与错误信息，对照 [errorcode.md](errorcode.md)。 |

## 后续

Application 内初始化与隐私接口见 [overview.md](overview.md)；显示地图与 MapView 生命周期见 [mapview.md](mapview.md)。Gradle 版本与国内镜像见 [gradle.md](gradle.md)。

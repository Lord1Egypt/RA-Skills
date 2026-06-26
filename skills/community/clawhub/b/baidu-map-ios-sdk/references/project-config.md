# 工程配置

**边界**：Info.plist、隐私弹窗、Launch Screen、CocoaPods 沙盒等百度 SDK 工程配置；Pod 集成见 [cocoapods.md](cocoapods.md)。

**Agent 注意**：集成地图/定位 SDK 时，必须检查或配置 Launch Screen（见下「窗口初始化/Launch Screen」），避免运行后 App 非全屏、黑边；并主动提示开发者配置 AK 与 Bundle Identifier（与百度控制台一致）。

## Info.plist 必配项

**CFBundleExecutable**（使用自定义 Info.plist 且 `GENERATE_INFOPLIST_FILE = NO` 时必配）：指定主可执行文件名，未配置会导致真机安装失败，报错「missing or invalid CFBundleExecutable」「无法安装」「请稍后再试」（Code 3002 / MIInstallerErrorDomain 11）。须在 plist 中显式添加：

```xml
<key>CFBundleExecutable</key>
<string>$(EXECUTABLE_NAME)</string>
```

编译时 Xcode 会将 `$(EXECUTABLE_NAME)` 展开为 target 的主可执行文件名（通常与 Product Name 一致）。

**CFBundleDisplayName**：SDK 启动时校验，未配置会报错「启动引擎失败: info.plist 中必须配置 Bundle display name」。

```xml
<key>CFBundleDisplayName</key>
<string>你的应用名称</string>
```

**定位权限**（使用定位时）：
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>需要获取您的位置以展示地图</string>
```

**调起百度地图客户端**（驾车/步行/骑行调起百度地图 App 时）：
1. 必须在 Info.plist 中配置 **LSApplicationQueriesSchemes**（baidumap），否则无法调起百度地图 App。
2. **指定返回自定义 scheme**：`appScheme` 按 **`scheme://host`** 格式填写（如 `yourapp://mapsdk.yourapp.com`）。scheme 名（`://` 前部分）须与 Info.plist 中 **CFBundleURLSchemes** 注册的一致，这样用户在百度地图内点击「返回」时才能通过该 URL 打开本 App。

LSApplicationQueriesSchemes：
```xml
<key>LSApplicationQueriesSchemes</key>
<array>
    <string>baidumap</string>
</array>
```

返回本 App 的 URL Scheme 注册（CFBundleURLSchemes 填 appScheme 的 scheme 部分，与格式 scheme://host 中的 scheme 一致）：
```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>CFBundleURLName</key>
        <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>foodsearchdemo</string>
        </array>
    </dict>
</array>
```
示例：若 `para.appScheme = @"foodsearchdemo://mapsdk.foodsearchdemo.com"`，则此处填 `foodsearchdemo`。

**步行 AR 导航**（使用 BaiduWalkNaviKit 且进入 AR 导航时）：必须配置相机用途说明，否则访问摄像头会**直接崩溃**。
```xml
<key>NSCameraUsageDescription</key>
<string>步行AR导航需要使用摄像头识别周围环境，为您提供实景导航指引</string>
```

## 隐私协议弹窗（必做）

**首次使用前必须弹窗提示用户阅读并同意隐私政策**，再调用 `[BMKMapManager setAgreePrivacy:YES]`。未同意时调用 `[BMKMapManager setAgreePrivacy:NO]`。

**注意**：`setAgreePrivacy:` 是 **BMKMapManager 的类方法**，必须写 `[BMKMapManager setAgreePrivacy:YES]`，**勿写** `[[BMKMapManager sharedInstance] setAgreePrivacy:YES]`（会报 "Instance method '-setAgreePrivacy:' not found"）。

**隐私政策地址**：https://lbsyun.baidu.com/index.php?title=openprivacy（弹窗内需可点击跳转）。

UI 标准见 [ui-standards.md](ui-standards.md)。**不同意时**：`setAgreePrivacy:NO`，BMKSearchBase 及其子类会返回 nil；需延迟创建检索对象，仅在用户同意后创建；未同意时使用检索前提示用户去同意。

## CocoaPods 构建沙盒（Xcode 15+）

CocoaPods 的 Copy Pods Resources 脚本需在 `Pods` 目录创建临时文件（如 `resources-to-copy-${TARGETNAME}.txt`）。Xcode 15 起默认开启 **User Script Sandboxing**，会阻止该写入，导致构建报错：

```
Sandbox: bash deny(1) file-write-create .../Pods/resources-to-copy-xxx.txt
```

**解决**：在 target 的 Build Settings 中设置 `ENABLE_USER_SCRIPT_SANDBOXING = NO`。

- **Xcode 图形界面**：选中 target → Build Settings → 搜索 "User Script Sandboxing" → 设为 **No**
- **project.pbxproj**：在 target 的 XCBuildConfiguration（Debug/Release）的 buildSettings 中添加：
  ```
  ENABLE_USER_SCRIPT_SANDBOXING = NO;
  ```

## 窗口初始化/Launch Screen

**现象**：地图未铺满屏幕、上下或左右出现黑边，地图只显示在中间一块区域。

**原因**：未配置 Launch Screen 时，系统会按「未声明支持当前设备屏幕」处理，窗口或根视图的尺寸/安全区域可能异常，导致 `view.bounds` 不是全屏，地图即使用 `view.bounds` 设 frame 也会出现黑边。

**必配**：工程需有 Launch Screen（LaunchScreen.storyboard 或同类），并在 Info.plist 中配置：

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>
```

LaunchScreen.storyboard 需设置 `launchScreen="YES"`、`useSafeAreas="YES"`，支持各尺寸 iPhone（含刘海屏）。内容可为白底 + 应用名等静态界面。

**地图不全屏排查顺序**（Agent 必须遵守）：
1. **先检查 Launch Screen**：是否有 LaunchScreen.storyboard（或 Launch Image）、Info.plist 是否含 `UILaunchStoryboardName`；缺则补上并加入 target Resources。
2. **再检查布局**：地图视图的 frame 是否在 `viewDidLayoutSubviews` 中设为 `self.view.bounds`（避免在 viewDidLoad/首次创建时 bounds 未稳定导致尺寸错误）。

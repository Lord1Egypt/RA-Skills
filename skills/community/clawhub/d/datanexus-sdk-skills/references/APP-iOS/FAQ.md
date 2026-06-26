# iOS SDK 常见问题（FAQ）

## Q1：模拟器上调用接口返回错误码 51000，怎么处理？

**A：** 错误码 51000 表示在模拟器上运行导致设备标识获取失败。

**解决方案：** 使用真机进行测试和联调。模拟器不支持 SDK 正常运行。

## Q2：抓包未发现 SDK 发出的网络请求，怎么排查？

**A：** 请检查是否有网络拦截工具（如 Charles、Fiddler 等）干扰了 SDK 的网络请求。抓包工具可能未正确配置 HTTPS 证书，导致 SDK 请求被拦截或失败。

排查步骤：

1. **关闭网络拦截工具**，重新测试是否有请求发出
2. **确认已调用 `[GDTAction start]`**（v2.1.0 及以上版本必须调用，否则不会发出任何请求）
3. **检查初始化时机**，确保 `init` 和 `start` 在事件上报之前完成
4. **查看日志**，在 Xcode 控制台中过滤 TAG `gdt_action`，查看是否有 `LogAction success` 或 `LogAction failed` 日志输出

## Q3：START_APP 和 ACTIVATE_APP 有什么区别？

**A：** 两者是完全不同的事件，不能混淆：

| 事件 | 触发时机 | 上报方式 |
|------|----------|----------|
| `START_APP` | 每次应用从后台切回前台或启动时触发 | 需手动在 `applicationDidBecomeActive:` 中调用 `[GDTAction logAction:actionParam:]` 上报 |
| `ACTIVATE_APP` | 应用首次安装后的第一次启动 | 由 SDK 内部自动判断并上报，无需手动调用 |

> **注意：** iOS 端 SDK v2.1.4+ 已默认自动采集 `START_APP`，无需手动上报。低版本（< v2.1.4）必须手动上报。

## Q4：为什么升级到 v2.1.0 之后数据上报失效了？

**A：** 从 v2.1.0 起，初始化后必须调用 `[GDTAction start]` 才能正常工作。请检查代码中是否遗漏了 `start` 调用：

```objectivec
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    [GDTAction init:@"actionSetId" secretKey:@"secretKey"];
    [GDTAction start];  // v2.1.0 及以上版本必须调用
    return YES;
}
```

## Q5：如何确认数据上报成功？

**A：** SDK 日志 TAG 为 `gdt_action`，日志级别为 info。在 Xcode 控制台中过滤该 TAG，查看日志输出：

- **上报成功：** `LogAction success xxxx`
- **上报失败：** `LogAction failed xxxx`

## Q6：iOS 14+ 如何处理 IDFA 权限？

**A：** iOS 14 起需通过 ATT（App Tracking Transparency）框架请求用户授权：

1. 在 `Info.plist` 中添加 `NSUserTrackingUsageDescription` 描述
2. 在合适时机调用 `ATTrackingManager.requestTrackingAuthorization` 请求权限
3. SDK 会自动适配授权状态，未授权时使用其他标识方案

> **建议：** 在 SDK 初始化之前完成 ATT 授权请求，以确保首次上报即可携带 IDFA。

## Q7：如何通过 URL Scheme 或 Universal Links 唤起时正确上报 START_APP？

**A：** 需要在对应的回调方法中携带 `open_url` 参数上报：

- **URL Scheme 唤起：** 在 `application:openURL:options:` 中调用 `[GDTAction logAction:@"START_APP" actionParam:@{@"open_url": url.absoluteString}]`
- **Universal Links 唤起：** 在 `application:continueUserActivity:restorationHandler:` 中调用 `[GDTAction logAction:@"START_APP" actionParam:@{@"open_url": userActivity.webpageURL.absoluteString}]`

## Q8：如何获取 CAID？

**A：** v2.0.11 及以上版本支持通过 `[GDTAction getCaid]` 获取，返回值为 NSDictionary：

```objectivec
NSDictionary *caidInfo = [GDTAction getCaid];
```

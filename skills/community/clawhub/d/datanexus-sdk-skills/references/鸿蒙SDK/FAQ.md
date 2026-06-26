# 鸿蒙 SDK 常见问题（FAQ）

## Q1：鸿蒙 SDK 支持哪些系统版本？

**A：** 要求 **HarmonyOS 5.0.0（API 12）** 及以上版本。

## Q2：init() 之后为什么还要调用 start()？

**A：** `init()` 仅完成 SDK 的参数配置，`start()` 才会真正启动数据采集。

## Q3：SDK 有哪些预定义上报方法？

**A：** SDK **没有**任何预定义上报方法。所有行为均通过 `logAction` 上报。

## Q4：哪些事件是自动采集的？

**A：** START_APP、TICKET、ENTER_FOREGROUND、ENTER_BACKGROUND、APP_QUIT。请勿手动上报。

## Q5：actionParam 的 Key 和 Value 有什么限制？

**A：** Key：字母/数字/下划线，字母开头，最长 64 字符。Value：String/Number/Boolean/JSONArray。

## Q6：需要声明哪些权限？

**A：** `ohos.permission.INTERNET`（必需）、`ohos.permission.GET_NETWORK_INFO`（必需）、`ohos.permission.APP_TRACKING_CONSENT`（可选）。

## Q7：抓包未发现 SDK 发出的网络请求？

**A：** 检查权限声明、是否调用 start()、初始化时机、网络环境、开启 show_log。

## Q8：如何确认数据上报成功？

**A：** 设置 `show_log: true`，过滤 TAG `[@dn-sdk/harmony v1.x.x]`，查看 logAction success/failed。

## Q9：鸿蒙系统如何获取设备标识？

**A：** 推荐 OAID（需声明 APP_TRACKING_CONSENT 权限）。

## Q10：从 Android 迁移到鸿蒙需要注意什么？

**A：** 依赖管理从 Gradle 到 ohpm，权限从 AndroidManifest.xml 到 module.json5，仅有 logAction 通用方法，开发语言为 ArkTS。

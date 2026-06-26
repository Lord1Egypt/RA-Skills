# Android SDK 常见问题（FAQ）

## Q1：模拟器上返回错误码 51000，怎么处理？

**A：** 错误码 51000 表示模拟器被检测为无效数据来源。

**解决方案：** 使用真机进行测试和联调，不要使用模拟器调试数据上报。

## Q2：抓包未发现 SDK 发出的网络请求，怎么排查？

**A：** 请检查是否存在网络拦截工具的干扰。Charles、Fiddler 等抓包代理工具可能会拦截或影响 SDK 的 HTTPS 请求，导致请求无法正常发出。尝试关闭这些工具后重新测试。

## Q3：START_APP 和 ACTIVATE_APP 有什么区别？

**A：** 这是两个不同的事件，不可混淆：

| 事件 | 说明 |
|------|------|
| `START_APP` | 应用启动事件，Android SDK v1.9.4+ 默认自动采集，无需手动上报。可通过 `GDTAction.setAutoStartEnable(false)` 关闭自动采集后手动调用 `GDTAction.logAction("START_APP")` 上报 |
| `ACTIVATE_APP` | 激活事件，与 START_APP 是不同的事件类型 |

> **注意：** `START_APP` ≠ `ACTIVATE_APP`，请勿将两者混用。

## Q4：`GDTAction.start()` 的作用是什么？必须调用吗？

**A：** 必须调用。`start()` 方法用于启动个人信息采集（设备信息等），是 SDK 正常工作的关键步骤。必须在 `GDTAction.init()` 之后立即调用：

```java
GDTAction.init(this, "userActionSetId", "appSecretKey");
GDTAction.start(); // 不调用将导致 SDK 无法正常采集设备信息
```

## Q5：权限配置有哪些注意事项？

**A：**

| 权限 | 是否必须 | 说明 |
|------|----------|------|
| `INTERNET` | **必须** | 网络通信 |
| `ACCESS_NETWORK_STATE` | 可选 | 提升归因匹配效果 |
| `READ_PHONE_STATE` | 可选 | 获取设备标识（IMEI 等），Android 6.0+ 需动态申请运行时权限 |
| `WRITE_EXTERNAL_STORAGE` | 可选 | 归因优化 |

缺少可选权限不影响 SDK 基本功能，但可能降低归因匹配率。

## Q6：如何确认数据上报成功？

**A：** 在 Logcat 中过滤 TAG `gdt_action`（info 级别）查看日志：

- **初始化成功：** `GDTAction初始化成功（sdkv: 1.x.x, sdkvc: xx）`
- **上报成功：** `LogAction success xxxx`
- **上报失败：** `LogAction failed xxxx`

## Q7：混淆配置需要注意什么？

**A：** 如果项目开启了 ProGuard 混淆，需在混淆规则文件中添加：

```proguard
-keep class com.qq.gdt.action.** { *; }
```

## Q8：接入了信通院 SDK 获取 OAID，有什么注意事项？

**A：**

- 信通院 OAID SDK 版本需 **≥ 2.8.0**
- 注意检查证书是否过期，证书过期会导致 OAID 获取失败
- 请及时关注信通院 SDK 更新和证书续期

## Q9：老用户（非新安装）如何上报？

**A：** 对于非新安装的老用户，在 actionParam 中设置 `audience_type` 为 `1`：

```java
JSONObject actionParam = new JSONObject();
actionParam.put("audience_type", 1);
GDTAction.logAction("YOUR_ACTION", actionParam);
```

## Q10：SDK 会自动采集哪些事件？

**A：** Android 端 SDK 自动采集以下事件，无需手动上报：

| 事件 | 说明 |
|------|------|
| `TICKET` | 票据事件 |
| `ENTER_FOREGROUND` | 应用进入前台 |
| `ENTER_BACKGROUND` | 应用进入后台 |

> **注意：** Android 端 `START_APP` 在 SDK v1.9.4+ 已默认自动采集，无需手动上报。如通过 `setAutoStartEnable(false)` 关闭了自动采集，则需手动上报。

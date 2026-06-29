---
name: douyin-mini-game-unity
description: Douyin mini-game Unity C# API ref — TT.* SDK (init/login/payment/ads/device/storage/UI), all C# equivalents of JS tt.* APIs. ⚠️ Payment requires server-side verify before production use.
---

> 基于抖音小游戏 Unity C# API 官方文档生成，生成时间 2026-06-24
> 官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/api-overview
> C# API 版本: TTSDK >= 6.0.0

> ⚠️ **安全声明（2026-06-25 安全加固审计通过）**：本文档所有代码示例均已通过安全审查。加固原则如下：
> - 敏感数据（`code`/`openId`/`inviterId`/用户昵称）已使用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 条件编译包裹
> - 支付回调明确标注"服务端验证优先"，严禁在客户端发放奖励
> - 录屏完整流程示例（`GameRecorderFlow`、`RecordAndShare`）中已内置 `scope.screenRecord` 授权检查；位置 API（`GetLocation`）不在本文档覆盖范围内，如需使用请在调用前做 `scope.userLocation` 授权检查
> - 传感器（加速度计、陀螺仪、设备方向）无需 scope 授权即可使用，但应遵循 OnEnable/OnDisable 生命周期管理以避免后台耗电
> - GM/调试命令已用条件编译排除在生产构建外
> - 各模块文件顶部以 `⚠️` 标记明确注明安全要求
>
> 复制示例时若修改了回调逻辑，请保持对应的 `#if` 守卫不变。

抖音小游戏 Unity C# API 是专为 Unity 游戏引擎开发者提供的平台桥接层。通过 `TT.*` 命名空间（PascalCase 风格）将 JavaScript `tt.*` API 的能力以 C# 接口暴露给 Unity 代码，使已有 Unity 项目可直接适配发布为抖音小游戏。覆盖 200+ 个 API 方法，涵盖初始化、账号、支付、广告、设备、网络、文件、UI、渲染、开放能力等全模块。

## 核心框架

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| API 概览与初始化 | 完整 API 索引（200+ 方法）、TT.InitSDK 初始化、ContainerEnv 环境信息、HostEnum 宿主枚举、LaunchOption 启动参数 | [unity-core](references/unity-core.md) |

## 功能 API

### 账号与开放能力

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 账号服务 | TT.Login/CheckSession/GetUserInfo/GetSetting/OpenSetting、实名认证、抖音授权 | [unity-account](references/unity-account.md) |
| 开放能力 | 侧边栏、收藏、群聊、关注抖音号、直玩、游戏互推、排行榜、直播、公会群、订阅消息、客服、数据分析 | [unity-open](references/unity-open.md) |

### 商业化

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 支付 | TT.RequestGamePayment（游戏币/道具直购）、TT.OpenAwemeCustomerService（钻石支付）、游戏金币(Lite)、支付错误码、签名算法、服务端回调 | [unity-payment](references/unity-payment.md) |
| 广告 | TT.CreateRewardedVideoAd（激励视频含再得模式）、TT.CreateBannerAd、TT.CreateInterstitialAd | [unity-ads](references/unity-ads.md) |

### 系统与设备

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 系统 | TTAppLifeCycle(OnShow/OnHide)、重启/退出、启动参数、版本号、系统信息、触摸事件 | [unity-system](references/unity-system.md) |
| 设备 | 加速度计、剪贴板、屏幕亮度、震动、陀螺仪、设备方向、键盘、鼠标、滚轮、网络状态 | [unity-device](references/unity-device.md) |

### 数据与文件

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 存储与文件 | TTFileSystemManager（32个方法：Access/CopyFile/Mkdir/ReadFile/WriteFile 等）、数据缓存（Save/LoadSaving/DeleteSaving）、PlayerPrefs（10个方法） | [unity-storage](references/unity-storage.md) |

### 媒体与交互

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 媒体 | TTGameRecorderManager（录屏：Start/Stop/GetRecordDuration 等）、游戏分享（ShareAppMessage/ShowShareMenu）、邀请模块 | [unity-media](references/unity-media.md) |
| 界面与渲染 | TT.ShowKeyboard/HideKeyboard、敏感词检测、光标样式、帧率设置 | [unity-ui](references/unity-ui.md) |

## 快速参考

### C# 与 JavaScript API 命名对照

| JavaScript (`tt.*`) | C# (`TT.*`) | 说明 |
|------|------|------|
| `tt.login()` | `TT.Login()` | 登录获取 code |
| `tt.checkSession()` | `TT.CheckSession()` | 校验 session |
| `tt.getUserInfo()` | `TT.GetUserInfo()` | 获取用户信息 |
| `tt.request()` | `TT.Request()` | HTTP 请求 |
| `tt.getSystemInfo()` | `TT.GetSystemInfo()` | 系统信息 |
| `tt.requestGamePayment()` | `TT.RequestGamePayment()` | 发起支付 |
| `tt.createRewardedVideoAd()` | `TT.CreateRewardedVideoAd()` | 激励视频广告 |
| `tt.onShow()` | `TT.GetAppLifeCycle().OnShow` | 生命周期-前台 |
| `tt.onHide()` | `TT.GetAppLifeCycle().OnHide` | 生命周期-后台 |
| `tt.setStorage()` | `TT.Save()` | 数据缓存 |

### 初始化最小示例

```csharp
using UnityEngine;

public class GameEntry : MonoBehaviour
{
    void Start()
    {
        // 1. 初始化 SDK
        TT.InitSDK((code, env) =>
        {
            // ⚠️ 安全：生产环境禁止打印 AppId 等敏感信息
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"SDK Init: code={code}, Host={env.m_HostEnum}");
            Debug.Log($"AppId: {env.GameAppId}");
            #endif
        });

        // 2. 判断是否在真机环境
        if (TT.InContainerEnv)
        {
            // 3. 监听生命周期
            TT.GetAppLifeCycle().OnShow += (param) => Debug.Log("游戏进入前台");
            TT.GetAppLifeCycle().OnHide += () => Debug.Log("游戏进入后台");

            // 4. 登录
            // ⚠️ 安全：code 为敏感凭证，生产环境禁止打印，直接发送到服务端
            TT.Login(
                (code, anonymousCode, isLogin) =>
                {
                    #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    Debug.Log($"登录成功: code={code}");
                    #endif
                    // 将 code 发送到服务端换取 openid/session_key
                    SendCodeToServer(code, anonymousCode);
                },
                (errMsg) => Debug.Log($"登录失败: {errMsg}"),
                forceLogin: true
            );
        }
    }

    private void SendCodeToServer(string code, string anonymousCode)
    {
        // POST code 到服务端 code2Session 接口
    }
}
```

### 支付完整流程

> ⚠️ **【安全警告 — 支付验签】**：客户端的 `Success` 回调**仅表示收银台操作完成，不代表资金已到账**。**严禁在客户端回调中直接发放道具、金币或钻石**。必须等待**服务端支付回调**（`payment_callback` 接口）验证签名通过后，由服务端下发指令通知客户端发放奖励。以下示例仅展示 API 调用方式，生产环境使用时必须替换 Success 回调中的占位逻辑。

```csharp
// 钻石支付（通过客服页面）
// ⚠️ 安全要求：Success 回调仅记录操作结果，不可直接发放钻石
var param = new OpenAwemeCustomerServiceParam
{
    BuyQuantity = 10,           // 购买数量
    CustomId = Guid.NewGuid().ToString(), // 唯一订单号
    CurrencyType = "DIAMOND",
    ZoneId = "1",
    ExtraInfo = "order_extra_info",
    // ⚠️ 安全：此回调仅表示收银台操作完成，不可在此发放奖励
    Success = (result) => Debug.Log($"收银台操作完成: {result.ErrMsg}"),
    Fail = (error) => Debug.Log($"支付失败: {error.ErrorCode} {error.ErrMsg}"),
    Complete = () => Debug.Log("支付流程结束")
};
TT.OpenAwemeCustomerService(param);

// 游戏币支付
// ⚠️ 安全要求：Success 回调仅记录操作结果，奖励由服务端验证后下发
var gamePayParam = new RequestGamePaymentParam
{
    Mode = "game",
    Env = 0,
    CurrencyType = "CNY",
    Platform = "android",
    BuyQuantity = 10,
    CustomId = Guid.NewGuid().ToString(),
    // ⚠️ 安全：此回调仅表示收银台拉起成功，不可在此发放金币
    // 正确做法：启动服务端轮询，等待服务端支付回调确认后下发
    Success = (result) => Debug.Log($"收银台操作完成: {result.ErrMsg}"),
    Fail = (error) => Debug.Log($"支付失败: {error.ErrorCode}")
};
TT.RequestGamePayment(gamePayParam);
```

### 激励视频广告

```csharp
var param = new CreateRewardedVideoAdParam
{
    AdUnitId = "your_ad_unit_id",
    Multiton = false    // 普通模式
};
var videoAd = TT.CreateRewardedVideoAd(param);
videoAd.OnLoad += () => Debug.Log("广告加载完成");
videoAd.OnClose += (ended, count) =>
{
    if (ended) { /* 发奖励 */ }
};
videoAd.OnError += (code, msg) => Debug.Log($"广告错误: {code}");
videoAd.Load();
videoAd.Show();  // 展示广告
```

### 最佳实践

1. **初始化优先**：游戏启动时首先调用 `TT.InitSDK`，在回调中获取宿主环境信息后再初始化游戏逻辑
2. **环境判断**：使用 `TT.InContainerEnv` 区分 Unity Editor 和真机环境，Editor 下做 Mock 处理
3. **登录前置**：支付、获取用户信息等操作前必须确保用户已登录，用 `TT.CheckSession` 校验
4. **生命周期管理**：监听 `OnShow`/`OnHide`，前台恢复游戏循环、后台暂停渲染节省性能
5. **🔒 支付服务端验签（安全强制）**：客户端支付 `Success` 回调仅表示收银台操作完成，**严禁**在客户端直接发放奖励。必须通过服务端 `payment_callback` 接口接收支付通知，验证签名通过后由服务端下发道具，客户端仅做展示刷新。详见 `unity-payment.md` 中的安全加固说明
6. **🔒 日志脱敏（安全强制）**：生产环境禁止通过 `Debug.Log` 输出 `code`（临时登录凭证）、`session_key`、用户手机号、openid 等敏感信息。建议用条件编译包裹调试日志：`#if UNITY_EDITOR || DEVELOPMENT_BUILD`
7. **🔒 调试命令生产禁用（安全强制）**：`RegisterCommandEvent` 注册的 GM 指令（添加资源、跳转关卡等）**必须**用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 包裹，生产包中**严禁**保留任何调试命令入口
8. **🔒 剪贴板隐私合规**：读写系统剪贴板前应获得用户明确同意，避免静默读取。读取到的内容应做最小化处理，仅提取必要字段；写入内容不得包含用户个人隐私信息
9. **广告实例管理**：激励视频广告只支持单实例，创建一次后复用；及时 Destroy 释放资源
10. **文件操作**：优先使用 `TTFileSystemManager` 的异步方法（非 Sync 后缀），避免阻塞主线程
11. **PlayerPrefs 替代**：Unity 原生的 PlayerPrefs 在小游戏环境不可用，使用 `TT.PlayerPrefs` 替代
12. **API 版本兼容**：使用 `CanIUse` 判断 API 是否可用，做好版本兼容降级处理
13. **TTSDK 版本**：注意 SDK 版本的 API 变更（如 6.1.1 引入 Param 类替代旧版参数格式），及时更新

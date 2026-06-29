# API 概览与初始化

> 基于官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/api-overview
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **登录凭证**：`code` 为临时登录凭证，严禁打印到生产日志，已用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 包裹
> - **位置数据**：`GetLocation()` 返回的经纬度为敏感数据，生产环境禁止打印日志
> - **GM 命令**：`RegisterCommandEvent` 注册的调试命令**必须**用条件编译包裹，生产包中严禁保留（已在本文件中修正）
> - **AppId**：`GameAppId` 虽非凭证，但不应在生产日志中暴露应用内部标识

## 一、SDK 初始化

### 1.1 TT.InitSDK

**说明**: 初始化抖音小游戏 SDK。所有 `TT.*` API 的前置调用，必须在游戏启动时首先执行。初始化完成后通过回调返回错误码和容器环境信息。

**语法**:

```csharp
public static int InitSDK(OnTTContainerInitCallback callback = null)
```

**回调委托**:

```csharp
public delegate void OnTTContainerInitCallback(int code, ContainerEnv env);
```

**返回值（同步）**:

| 错误码 | 说明 |
|--------|------|
| 0 | 无错误，SDK 初始化成功 |
| 1 | SDK 版本不支持 |
| 2 | Unity 版本不支持 |

**回调参数（异步）**:

| 参数 | 类型 | 说明 |
|------|------|------|
| code | int | 同上错误码。0 表示成功，非 0 表示初始化失败 |
| env | ContainerEnv | 容器环境信息对象，包含宿主、启动来源、版本类型等 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class GameBootstrap : MonoBehaviour
{
    void Start()
    {
        // 同步返回错误码（立即返回，不阻塞）
        int syncCode = TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                // ⚠️ 安全：环境信息含 AppId，生产环境禁止打印
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"SDK 初始化成功");
                Debug.Log($"宿主环境: {env.m_HostEnum}");
                Debug.Log($"启动来源: {env.m_LaunchFromEnum}");
                Debug.Log($"AppId: {env.GameAppId}");
                Debug.Log($"版本类型: {env.GetVersionType()}");
                #endif
            }
            else
            {
                Debug.LogError($"SDK 初始化失败: 错误码={code}");
            }
        });

        Debug.Log($"InitSDK 同步返回值: {syncCode}");
    }
}
```

---

### 1.2 TT.InContainerEnv

**说明**: 判断当前是否在抖音小游戏真机容器环境中运行。在 Unity Editor 中运行时会返回 `false`，可借此实现 Editor Mock 逻辑。

**语法**:

```csharp
public static bool InContainerEnv { get; }
```

**代码示例**:

```csharp
if (TT.InContainerEnv)
{
    // 真机容器环境
    Debug.Log("运行在抖音小游戏容器中");
    TT.Login(
        (code, anonymousCode, isLogin) =>
        {
            // ⚠️ 安全：code 为敏感凭证，生产环境禁止打印
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"登录成功: code={code}");
            #endif
        },
        (errMsg) =>
        {
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.LogError($"登录失败: {errMsg}");
            #endif
        }
    );
}
else
{
    // Unity Editor 环境，使用 Mock 数据
    Debug.Log("运行在 Unity Editor 中，使用 Mock 逻辑");
    MockLogin();
}
```

---

## 二、ContainerEnv 环境信息

`ContainerEnv` 是 `TT.InitSDK` 回调中传入的环境信息对象，包含宿主 App、启动来源、版本类型等关键信息。

### 2.1 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| GameAppId | string | 当前小游戏的 AppId |
| m_HostEnum | HostEnum | 宿主 App 枚举值 |
| m_LaunchFromEnum | LaunchFromEnum | 启动来源枚举值 |

### 2.2 方法

| 方法 | 返回类型 | 说明 |
|------|---------|------|
| GetContainerRuntime() | ContainerRuntime | 获取容器运行时类型 |
| GetVersionType() | VersionType | 获取版本类型（预览/测试/正式） |
| GetLaunchFromStr() | string | 获取启动来源的字符串描述 |
| GetQueryFromScheme() | string | 获取 Scheme 拉起时的 query 参数 |
| GetLocation() | LocationInfo | 获取宿主的地域信息 |
| GetLaunchFrom() | LaunchFromEnum | 获取启动来源枚举 |
| GetLaunchOptionsSync() | LaunchOption | 同步获取启动参数 |

### 2.3 LocationInfo 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| Latitude | double | 纬度 |
| Longitude | double | 经度 |
| Speed | double | 速度 |
| Accuracy | double | 精度 |
| Altitude | double | 海拔 |
| VerticalAccuracy | double | 垂直精度 |
| HorizontalAccuracy | double | 水平精度 |

### 2.4 代码示例

```csharp
TT.InitSDK((code, env) =>
{
    if (code != 0) return;

    // ⚠️ 安全：环境信息含 AppId/地域等敏感数据，生产环境禁止打印
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    Debug.Log($"AppId: {env.GameAppId}");
    Debug.Log($"宿主: {env.m_HostEnum}");                     // 抖音/抖音极速版/头条等
    Debug.Log($"启动来源: {env.m_LaunchFromEnum}");            // 搜索/桌面/分享等
    Debug.Log($"运行时: {env.GetContainerRuntime()}");          // Unity/Launcher/Standard
    Debug.Log($"版本: {env.GetVersionType()}");                 // 预览/测试/正式
    Debug.Log($"启动来源字符串: {env.GetLaunchFromStr()}");
    Debug.Log($"Scheme Query: {env.GetQueryFromScheme()}");

    // 地域信息
    // ⚠️ 安全：位置信息为敏感数据，生产环境禁止打印
    var location = env.GetLocation();
    Debug.Log($"位置: 经度={location.Longitude}, 纬度={location.Latitude}");
    #endif

    // 启动参数
    var launchOption = env.GetLaunchOptionsSync();
    Debug.Log($"启动路径: {launchOption.Path}");
    Debug.Log($"启动场景: {launchOption.Scene}");
});
```

---

## 三、枚举定义

### 3.1 HostEnum 宿主 App 枚举

标识当前运行在哪个字节跳动系 App 中。

| 枚举值 | 数值 | 对应 App |
|--------|------|---------|
| None | 0 | 未知 |
| Toutiao | 1 | 今日头条 |
| Douyin | 2 | 抖音 |
| ToutiaoLite | 3 | 今日头条极速版 |
| DouyinLite | 4 | 抖音极速版 |
| HuoShan | 5 | 火山小视频 |
| HuoShanLite | 6 | 火山极速版 |
| XiGua | 7 | 西瓜视频 |
| Helo | 8 | Helo |
| Tiktok | 9 | TikTok |
| PiPiXia | 10 | 皮皮虾 |
| MoMoYu | 11 | 摸摸鱼 |
| DongCheDi | 12 | 懂车帝 |
| Fanqie | 13 | 番茄小说 |

**代码示例**:

```csharp
TT.InitSDK((code, env) =>
{
    switch (env.m_HostEnum)
    {
        case HostEnum.Douyin:
        case HostEnum.DouyinLite:
            Debug.Log("运行在抖音 App 中");
            break;
        case HostEnum.Toutiao:
            Debug.Log("运行在今日头条中");
            break;
        default:
            Debug.Log($"其他宿主: {env.m_HostEnum}");
            break;
    }
});
```

---

### 3.2 LaunchFromEnum 启动来源枚举

标识用户从何种入口进入小游戏。

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| UnKnown | 0 | 未知来源 |
| Search | 1 | 搜索 |
| DeskTop | 2 | 桌面快捷方式 |
| MP_List | 3 | 小程序列表 |
| Scan | 4 | 扫码 |
| Share | 5 | 分享 |
| Video_Archor | 6 | 视频锚点 |
| Feed | 7 | 信息流推荐 |
| MiniApk | 8 | 桌面快捷方式（MiniApk） |

---

### 3.3 ContainerRuntime 运行时类型枚举

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| Unity | 0 | Unity WebGL 容器 |
| Launcher | 1 | Launcher 容器 |
| Standard | 2 | 标准容器 |

---

### 3.4 VersionType 版本类型枚举

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| None | 0 | 未指定 |
| Perview | 1 | 预览版本 |
| Test | 2 | 测试版本 |
| Release | 3 | 正式版本 |

**代码示例**:

```csharp
TT.InitSDK((code, env) =>
{
    var versionType = env.GetVersionType();
    if (versionType == VersionType.Release)
    {
        Debug.Log("当前为正式版本，使用生产环境配置");
    }
    else
    {
        Debug.Log($"当前为非正式版本({versionType})，使用测试环境配置");
    }

    var runtime = env.GetContainerRuntime();
    if (runtime == ContainerRuntime.Unity)
    {
        Debug.Log("Unity 容器，全功能可用");
    }
});
```

---

## 四、LaunchOption 启动参数

`LaunchOption` 封装了小游戏启动时的所有参数，通过 `env.GetLaunchOptionsSync()` 获取。

### 4.1 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| Path | string | 启动路径，通常为入口页面路径 |
| Query | Dictionary\<string, string\> | 启动参数（key-value 键值对） |
| Scene | string | 场景值，标识进入小游戏的具体场景 |
| SubScene | string | 子场景值 |
| IsSticky | bool | 是否从桌面快捷方式进入 |
| ShareTicket | string | 分享票据（群分享时返回） |
| GroupId | string | 群 ID（通过群聊分享进入时返回） |
| Extra | Dictionary\<string, string\> | 额外参数（平台预留） |
| RefererInfo | Dictionary\<string, string\> | 来源信息（包含 appId、extraData 等） |

### 4.2 代码示例

```csharp
TT.InitSDK((code, env) =>
{
    var launchOption = env.GetLaunchOptionsSync();

    // 基础参数
    Debug.Log($"启动路径: {launchOption.Path}");
    Debug.Log($"场景值: {launchOption.Scene}");
    Debug.Log($"桌面快捷方式: {launchOption.IsSticky}");

    // Query 参数（如 Scheme 拉起时携带的参数）
    // ⚠️ 安全：Query 可能包含邀请 token 等敏感数据，生产环境禁止打印
    if (launchOption.Query != null)
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        foreach (var kv in launchOption.Query)
        {
            Debug.Log($"Query 参数: {kv.Key} = {kv.Value}");
        }
        #endif
    }

    // 分享相关
    if (!string.IsNullOrEmpty(launchOption.ShareTicket))
    {
        // ⚠️ 安全：ShareTicket 为授权票据，GroupId 关联用户社交上下文，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"分享票据: {launchOption.ShareTicket}");
        Debug.Log($"群 ID: {launchOption.GroupId}");
        #endif
    }

    // 来源信息
    if (launchOption.RefererInfo != null)
    {
        foreach (var kv in launchOption.RefererInfo)
        {
            Debug.Log($"来源: {kv.Key} = {kv.Value}");
        }
    }
});
```

---

## 五、基础工具

### 5.1 TT.CanIUse

**说明**: 判断指定 API 或组件在当前基础库版本中是否可用。用于版本兼容降级处理，避免低版本宿主调用新 API 导致报错。

**语法**:

```csharp
public static bool CanIUse(string apiName)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| apiName | string | 是 | - | API 名称或组件名，格式如 `"requestGamePayment"` 或 `"requestGamePayment.object.goodType"` |

**返回值**: `bool`，`true` 表示该 API/特性在当前版本可用。

**代码示例**:

```csharp
// 基础 API 判断
if (TT.CanIUse("requestGamePayment"))
{
    Debug.Log("当前版本支持支付 API");
    // 安全调用支付
}
else
{
    Debug.LogWarning("当前版本不支持支付 API，隐藏支付入口");
}

// 特定功能判断（如道具直购）
if (TT.CanIUse("requestGamePayment.object.goodType"))
{
    var param = new RequestGamePaymentParam
    {
        GoodType = 2,           // 道具直购模式
        GoodName = "钻石礼包",
        OrderAmount = 600,      // 单位：分
        // ... 其他参数
    };
    TT.RequestGamePayment(param);
}
else
{
    Debug.Log("当前版本不支持道具直购，降级为游戏币支付");
    // 使用普通游戏币支付模式
}
```

---

### 5.2 TT.EnableTTSDKDebugToast

**说明**: 开启或关闭 TTSDK 的 Debug Toast 提示。开启后会在屏幕上显示 SDK 内部的调试信息，方便开发阶段排查问题。注意: 正式发布版本应关闭此开关。

**语法**:

```csharp
public static void EnableTTSDKDebugToast(bool enable)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| enable | bool | 是 | - | true 开启 Debug Toast，false 关闭 |

**代码示例**:

```csharp
#if UNITY_EDITOR || DEVELOPMENT_BUILD
    TT.EnableTTSDKDebugToast(true);
    Debug.Log("Debug Toast 已开启");
#else
    TT.EnableTTSDKDebugToast(false);
#endif
```

---

### 5.3 TT.RegisterCommandEvent

**说明**: 注册宿主下发的自定义命令事件监听。宿主可通过特定通道向小游戏下发命令，游戏侧通过此方法注册监听以接收并处理命令。

> ⚠️ **【安全警告 — 调试命令生产禁用】**：`RegisterCommandEvent` 用于注册开发者工具下发的自定义命令，**仅限开发调试阶段使用**。注册的 GM 指令**必须**用条件编译（`#if UNITY_EDITOR || DEVELOPMENT_BUILD`）包裹，生产包中**严禁**保留任何调试命令入口。`add_resource`、`jump_level` 等 GM 指令在生产环境中会直接导致经济系统崩溃和作弊泛滥。

**语法**:

```csharp
public static void RegisterCommandEvent(Action<string> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| callback | Action\<string\> | 是 | 命令回调，参数为宿主下发的命令字符串 |

**代码示例**:

```csharp
void OnEnable()
{
    // ⚠️ 安全强制：调试命令仅在开发版本中注册，生产包中严禁保留
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    TT.RegisterCommandEvent(OnCommandReceived);
    #else
    Debug.Log("生产环境：调试命令已禁用");
    #endif
}

void OnDisable()
{
    // 注意: 当前 API 不提供 UnregisterCommandEvent，此方法为文档性占位
    // 生产环境中此回调不会触发，因为 RegisterCommandEvent 未被调用
}

#if UNITY_EDITOR || DEVELOPMENT_BUILD
private void OnCommandReceived(string command)
{
    Debug.Log($"收到宿主命令: {command}");

    // 解析并处理命令
    try
    {
        var cmdData = JsonUtility.FromJson<CommandData>(command);
        switch (cmdData.action)
        {
            case "pause":
                PauseGame();
                break;
            case "resume":
                ResumeGame();
                break;
            case "updateData":
                RefreshGameData(cmdData.payload);
                break;
            default:
                Debug.LogWarning($"未知命令: {cmdData.action}");
                break;
        }
    }
    catch (System.Exception e)
    {
        Debug.LogError($"命令解析失败: {e.Message}");
    }
}
#endif
```

---

## 六、初始化最佳实践

```csharp
using UnityEngine;
using TT;

/// <summary>
/// 游戏入口: 统一管理 SDK 初始化、环境适配、生命周期
/// </summary>
public class GameEntry : MonoBehaviour
{
    private ContainerEnv m_Env;

    void Start()
    {
        // 第一步: 判断运行环境
        if (!TT.InContainerEnv)
        {
            Debug.Log("Unity Editor 环境，加载 Mock 数据");
            InitMockGame();
            return;
        }

        // 第二步: 初始化 SDK
#if DEVELOPMENT_BUILD
        TT.EnableTTSDKDebugToast(true);
#endif

        TT.InitSDK((code, env) =>
        {
            if (code != 0)
            {
                Debug.LogError($"SDK 初始化失败: code={code}");
                // 降级处理: 显示错误提示或重试
                return;
            }

            m_Env = env;

            // 第三步: 根据环境信息做差异化配置
            ConfigureByHost(env.m_HostEnum);

            // 第四步: 注册生命周期
            RegisterLifecycle();

            // 第五步: 版本兼容检查
            CheckApiCompatibility();

            // 第六步: 启动游戏主逻辑
            StartGame();
        });
    }

    private void ConfigureByHost(HostEnum host)
    {
        switch (host)
        {
            case HostEnum.Douyin:
            case HostEnum.DouyinLite:
                // 抖音特有配置
                break;
            case HostEnum.Toutiao:
                // 头条特有配置
                break;
        }
    }

    private void RegisterLifecycle()
    {
        var lifecycle = TT.GetAppLifeCycle();
        lifecycle.OnShow += (param) =>
        {
            Debug.Log($"游戏进入前台, 场景: {param.Scene}");
            ResumeGame();
        };
        lifecycle.OnHide += () =>
        {
            Debug.Log("游戏进入后台");
            PauseGame();
        };
    }

    private void CheckApiCompatibility()
    {
        Debug.Log($"支付 API 可用: {TT.CanIUse("requestGamePayment")}");
        Debug.Log($"激励视频可用: {TT.CanIUse("createRewardedVideoAd")}");
        Debug.Log($"道具直购可用: {TT.CanIUse("requestGamePayment.object.goodType")}");
    }

    private void InitMockGame() { /* Editor Mock 逻辑 */ }
    private void StartGame() { /* 游戏主逻辑入口 */ }
    private void PauseGame() { Time.timeScale = 0; }
    private void ResumeGame() { Time.timeScale = 1; }
}
```

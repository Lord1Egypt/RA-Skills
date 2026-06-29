# 系统与生命周期

> 基于官方文档: 系统 API - 生命周期、启动参数、系统信息、触摸事件、调试
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **系统信息**：`GetSystemInfo()` 返回的设备型号、系统版本可用于设备指纹识别，生产日志中应避免全量打印
> - **启动参数**：`LaunchOption` 中的 `Query` 参数可能包含敏感数据（如邀请码、token），不应记录到生产日志
> - **全局错误**：`OnError` 回调中的堆栈信息在生产环境应脱敏处理，避免泄露内部代码结构

系统模块提供小游戏运行时的核心能力：生命周期监听、前后台切换、启动参数获取、系统信息查询、触摸事件处理以及退出/重启控制。所有 API 挂载在 `TT` 静态类下，PascalCase 命名风格对应 JavaScript `tt.*` camelCase 接口。

## 一、生命周期

生命周期管理是小游戏最基础的机制。游戏进入后台时应暂停渲染和逻辑以节省性能，回到前台时恢复。通过 `TTAppLifeCycle` 对象的事件订阅实现。

### 1.1 TT.GetAppLifeCycle

**说明**：获取应用生命周期管理器单例。通过订阅 `OnShow` 和 `OnHide` 事件监听游戏前后台切换。开发者应在游戏初始化阶段获取该实例并订阅事件，避免在每帧重复调用。

**语法**：

```csharp
public static TTAppLifeCycle GetAppLifeCycle()
```

**返回值**：`TTAppLifeCycle` 单例实例。

**TTAppLifeCycle 事件**：

| 事件 | 委托类型 | 说明 |
|------|---------|------|
| OnShow | `event Action<Dictionary<string, object>>` | 游戏从后台进入前台。参数为启动参数字典，包含 `scene`（场景值）、`query`（query 参数）、`launch_from`（启动来源）等字段 |
| OnHide | `event Action` | 游戏从前台进入后台（切到桌面、接听电话等） |

**代码示例**：

```csharp
using UnityEngine;

public class GameLifecycle : MonoBehaviour
{
    void Start()
    {
        // 仅在真机环境监听生命周期
        if (TT.InContainerEnv)
        {
            var lifeCycle = TT.GetAppLifeCycle();
            lifeCycle.OnShow += OnGameShow;
            lifeCycle.OnHide += OnGameHide;
        }
    }

    /// <summary>
    /// 游戏进入前台
    /// </summary>
    void OnGameShow(Dictionary<string, object> param)
    {
        Debug.Log("游戏进入前台");

        // 解析启动参数
        // ⚠️ 安全：query 可能包含邀请 token/用户标识等敏感数据，生产环境禁止打印
        if (param != null)
        {
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            if (param.ContainsKey("scene"))
                Debug.Log($"场景值: {param["scene"]}");
            if (param.ContainsKey("query"))
                Debug.Log($"启动参数: {param["query"]}");
            #endif
        }

        // 恢复游戏逻辑
        ResumeGame();
    }

    /// <summary>
    /// 游戏进入后台
    /// </summary>
    void OnGameHide()
    {
        Debug.Log("游戏进入后台");

        // 暂停游戏逻辑，释放临时资源
        PauseGame();
    }

    void PauseGame()
    {
        Time.timeScale = 0f;
        // 暂停音频播放
        // AudioListener.pause = true;
        // 保存游戏进度
        // SaveManager.Instance.SaveProgress();
    }

    void ResumeGame()
    {
        Time.timeScale = 1f;
        // 恢复音频播放
        // AudioListener.pause = false;
    }

    void OnDestroy()
    {
        if (TT.InContainerEnv)
        {
            var lifeCycle = TT.GetAppLifeCycle();
            lifeCycle.OnShow -= OnGameShow;
            lifeCycle.OnHide -= OnGameHide;
        }
    }
}
```

### 1.2 TT.SetOnBeforeExitAppListener

**说明**：设置游戏退出前的回调拦截。当用户通过系统返回键或手势退出小游戏时触发。若回调返回 `true`，表示开发者自行处理退出逻辑（如弹出挽留弹窗），需手动调用 `TT.ExitMiniProgram()` 执行实际退出；若返回 `false`，系统直接退出。

**语法**：

```csharp
public static void SetOnBeforeExitAppListener(Func<bool> onBeforeExitApp)
```

**参数说明**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| onBeforeExitApp | Func\<bool\> | 是 | - | 退出前回调委托，返回 `true` 表示开发者自行处理，返回 `false` 表示系统直接退出 |

**代码示例**：

```csharp
void Start()
{
    if (TT.InContainerEnv)
    {
        TT.SetOnBeforeExitAppListener(() =>
        {
            Debug.Log("用户尝试退出游戏");
            // 返回 true 表示自行处理：弹出挽留弹窗
            ShowExitConfirmDialog();
            return true;
        });
    }
}

void ShowExitConfirmDialog()
{
    // 示例：展示挽留弹窗
    // UIManager.Instance.ShowDialog(
    //     title: "提示",
    //     content: "确定要退出游戏吗？",
    //     onConfirm: () => TT.ExitMiniProgram(),
    //     onCancel: () => Debug.Log("用户取消退出")
    // );
}
```

## 二、退出与重启

### 2.1 TT.RestartMiniProgramSync

**说明**：同步重启小游戏。调用后立即触发冷启动流程，重新执行游戏入口场景。通常用于版本更新后强制重启或用户切换账号等场景。

**语法**：

```csharp
public static void RestartMiniProgramSync()
```

**代码示例**：

```csharp
// 应用新版本后重启
public void ApplyUpdateAndRestart()
{
    // 保存必要状态
    // SaveManager.Instance.SaveAll();

    TT.RestartMiniProgramSync();
}
```

### 2.2 TT.ExitMiniProgram

**说明**：退出小游戏，返回抖音客户端。需配合 `SetOnBeforeExitAppListener` 使用：当退出前回调返回 `true` 时，开发者需在适当时机（如用户确认退出后）手动调用此方法完成实际退出。

**语法**：

```csharp
public static void ExitMiniProgram()
```

**代码示例**：

```csharp
// 配合 SetOnBeforeExitAppListener 的挽留弹窗使用
void Start()
{
    if (TT.InContainerEnv)
    {
        TT.SetOnBeforeExitAppListener(() =>
        {
            // 弹出确认弹窗
            ShowQuitConfirmDialog(
                onConfirm: () =>
                {
                    // 保存数据后退出
                    // SaveManager.Instance.SaveAll();
                    TT.ExitMiniProgram();
                }
            );
            return true; // 自行处理退出
        });
    }
}

void ShowQuitConfirmDialog(System.Action onConfirm)
{
    // 展示退出确认弹窗，用户确认后调用 onConfirm
    // UIManager.Instance.ShowConfirm("确定退出？", onConfirm);
}
```

## 三、启动参数

### 3.1 TT.GetLaunchOptionsSync

**说明**：同步获取小游戏启动参数。包括场景值、启动 query 参数、来源信息等。通常在游戏初始化阶段调用，用于判断启动来源并执行对应的业务逻辑（如从分享链接进入跳转特定关卡）。

**语法**：

```csharp
public static LaunchOption GetLaunchOptionsSync()
```

**返回值**：`LaunchOption` 对象，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| Scene | string | 场景值，标识小游戏启动来源（如 1001=发现页，1007=单人聊天，1036=分享进入等） |
| Query | Dictionary\<string, object\> | 启动时携带的 query 参数键值对 |
| LaunchFrom | string | 启动来源标识 |
| ReferrerInfo | object | 来源信息，包含 `appId`（来源小程序 ID）和 `extraData`（来源传递的数据） |

**代码示例**：

```csharp
void Start()
{
    if (TT.InContainerEnv)
    {
        var launchOptions = TT.GetLaunchOptionsSync();

        Debug.Log($"启动场景值: {launchOptions.Scene}");
        Debug.Log($"启动来源: {launchOptions.LaunchFrom}");

        // 解析 query 参数
        // ⚠️ 安全：Query 可能包含邀请 token/用户标识，生产环境禁止打印
        if (launchOptions.Query != null)
        {
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            foreach (var kv in launchOptions.Query)
            {
                Debug.Log($"Query[{kv.Key}] = {kv.Value}");
            }
            #endif

            // 示例：从分享链接进入，跳转指定关卡
            if (launchOptions.Query.ContainsKey("level"))
            {
                int levelId = int.Parse(launchOptions.Query["level"].ToString());
                // GameManager.Instance.LoadLevel(levelId);
            }
        }

        // 解析来源小程序信息
        if (launchOptions.ReferrerInfo != null)
        {
            // var fromAppId = launchOptions.ReferrerInfo.appId;
        }
    }
}
```

## 四、版本号

### 4.1 TT.TTSDKVersion

**说明**：获取当前 TTSDK（抖音小游戏基础库）版本号字符串。

**语法**：

```csharp
public static string TTSDKVersion { get; }
```

### 4.2 TT.GameVersion

**说明**：获取小游戏代码包版本号（对应上传时填写的版本号）。

**语法**：

```csharp
public static string GameVersion { get; }
```

### 4.3 TT.GamePublishVersion

**说明**：获取小游戏已发布的线上的版本号。仅在审核通过并发布后有效。

**语法**：

```csharp
public static string GamePublishVersion { get; }
```

### 4.4 TT.GetContainerVersion

**说明**：获取宿主容器版本号（抖音 App 版本号）。

**语法**：

```csharp
public static string GetContainerVersion()
```

**代码示例**：

```csharp
void LogVersionInfo()
{
    Debug.Log($"TTSDK 版本: {TT.TTSDKVersion}");
    Debug.Log($"游戏版本: {TT.GameVersion}");
    Debug.Log($"线上发布版本: {TT.GamePublishVersion}");
    Debug.Log($"宿主版本: {TT.GetContainerVersion()}");

    // 版本判断示例
    // 注意：TTSDKVersion 为字符串，如 "6.0.0"，比较时需解析
    // 如有 API 兼容需求，优先使用 TT.CanIUse() 判断
}
```

## 五、系统信息

### 5.1 TT.GetSystemInfo

**说明**：异步获取设备系统信息，包括设备品牌、型号、操作系统版本、屏幕尺寸、像素比、安全区域等。回调参数为包含所有系统信息字段的字典。

**语法**：

```csharp
public static void GetSystemInfo(Action<Dictionary<string, object>> success, Action<string> fail = null)
```

**参数说明**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<Dictionary\<string, object\>\> | 是 | - | 成功回调，参数字典包含所有系统信息字段 |
| fail | Action\<string\> | 否 | null | 失败回调，参数为错误信息 |

**success 回调字典常用字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| brand | string | 设备品牌（如 "iPhone"、"Xiaomi"） |
| model | string | 设备型号（如 "iPhone 14 Pro"） |
| system | string | 操作系统版本（如 "iOS 17.0"） |
| platform | string | 平台：`ios`、`android`、`windows`、`mac` |
| screenWidth | float | 屏幕宽度（px） |
| screenHeight | float | 屏幕高度（px） |
| windowWidth | float | 可用窗口宽度（px） |
| windowHeight | float | 可用窗口高度（px） |
| pixelRatio | float | 设备像素比 |
| SDKVersion | string | 基础库版本（如 "6.0.0"） |
| version | string | 抖音 App 版本 |
| language | string | 系统语言（如 "zh_CN"） |
| statusBarHeight | float | 状态栏高度 |
| safeArea | object | 安全区域 `{ left, right, top, bottom, width, height }` |
| benchmarkLevel | int | 设备性能等级：-1=未知，1~50=低端，51~100=高端 |
| fontSizeSetting | float | 用户字体大小设置 |
| deviceOrientation | string | 设备方向：`portrait`、`landscape` |

**代码示例**：

```csharp
void Start()
{
    if (TT.InContainerEnv)
    {
        TT.GetSystemInfo(
            success: (info) =>
            {
                // 设备信息
                // ⚠️ 安全：品牌/型号/系统版本组合可用于设备指纹，生产环境禁止全量打印
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"设备品牌: {info["brand"]}");
                Debug.Log($"设备型号: {info["model"]}");
                Debug.Log($"系统版本: {info["system"]}");
                Debug.Log($"平台: {info["platform"]}");
                #endif

                // 屏幕信息
                float screenW = Convert.ToSingle(info["screenWidth"]);
                float screenH = Convert.ToSingle(info["screenHeight"]);
                float pixelRatio = Convert.ToSingle(info["pixelRatio"]);
                Debug.Log($"屏幕: {screenW}x{screenH}, 像素比: {pixelRatio}");

                // 安全区域适配（刘海屏）
                if (info.ContainsKey("safeArea") && info["safeArea"] != null)
                {
                    var safeArea = info["safeArea"] as Dictionary<string, object>;
                    float safeTop = Convert.ToSingle(safeArea["top"]);
                    float safeBottom = Convert.ToSingle(safeArea["bottom"]);
                    // AdjustUILayout(safeTop, safeBottom);
                }

                // 设备性能分级，按需调整画质
                int benchmark = Convert.ToInt32(info["benchmarkLevel"]);
                if (benchmark <= 50)
                {
                    // 低端设备：降低画质、减少粒子效果
                    // QualitySettings.SetQualityLevel(0);
                    Debug.Log("检测到低端设备，启用低画质模式");
                }
            },
            fail: (errMsg) =>
            {
                Debug.LogError($"获取系统信息失败: {errMsg}");
            }
        );
    }
}
```

## 六、触摸事件

触摸事件提供原始触摸数据，从宿主层直接传递到 Unity。每个触摸事件回调接收 `TTTouch` 对象数组。

### 6.1 TTTouch 触摸对象

| 属性 | 类型 | 说明 |
|------|------|------|
| identifier | int | 触摸点唯一标识符，同一手指的 identifier 在整个触摸周期内保持不变 |
| clientX | float | 触摸点相对于 Canvas 可绘制区域左侧的距离 |
| clientY | float | 触摸点相对于 Canvas 可绘制区域顶部的距离 |
| pageX | float | 触摸点相对于页面左侧的距离 |
| pageY | float | 触摸点相对于页面顶部的距离 |
| force | float | 按压力度（仅 iOS 支持 3D Touch，取值范围 0.0 ~ 1.0） |

### 6.2 触摸事件 API

**TT.OnTouchStart / TT.OffTouchStart**

**说明**：监听/取消监听触摸开始事件。手指首次接触屏幕时触发。

**语法**：

```csharp
public static void OnTouchStart(Action<TTTouch[]> callback)
public static void OffTouchStart(Action<TTTouch[]> callback)
```

**TT.OnTouchMove / TT.OffTouchMove**

**说明**：监听/取消监听触摸移动事件。手指在屏幕上滑动时持续触发。

**语法**：

```csharp
public static void OnTouchMove(Action<TTTouch[]> callback)
public static void OffTouchMove(Action<TTTouch[]> callback)
```

**TT.OnTouchEnd / TT.OffTouchEnd**

**说明**：监听/取消监听触摸结束事件。手指离开屏幕时触发。

**语法**：

```csharp
public static void OnTouchEnd(Action<TTTouch[]> callback)
public static void OffTouchEnd(Action<TTTouch[]> callback)
```

**TT.OnTouchCancel / TT.OffTouchCancel**

**说明**：监听/取消监听触摸取消事件。触摸被系统中断时触发（如来电、通知、手势冲突等）。

**语法**：

```csharp
public static void OnTouchCancel(Action<TTTouch[]> callback)
public static void OffTouchCancel(Action<TTTouch[]> callback)
```

### 6.3 代码示例

```csharp
using UnityEngine;

public class TouchHandler : MonoBehaviour
{
    void Start()
    {
        if (TT.InContainerEnv)
        {
            TT.OnTouchStart += HandleTouchStart;
            TT.OnTouchMove += HandleTouchMove;
            TT.OnTouchEnd += HandleTouchEnd;
            TT.OnTouchCancel += HandleTouchCancel;
        }
    }

    void HandleTouchStart(TTTouch[] touches)
    {
        foreach (var touch in touches)
        {
            Debug.Log($"触摸开始: id={touch.identifier}, pos=({touch.clientX}, {touch.clientY})");

            // 示例：记录拖拽起始点
            // dragStartPos[touch.identifier] = new Vector2(touch.clientX, touch.clientY);
        }
    }

    void HandleTouchMove(TTTouch[] touches)
    {
        foreach (var touch in touches)
        {
            // 示例：拖拽更新位置
            // if (dragStartPos.ContainsKey(touch.identifier))
            // {
            //     var delta = new Vector2(touch.clientX, touch.clientY) - dragStartPos[touch.identifier];
            //     UpdateObjectPosition(delta);
            // }
        }
    }

    void HandleTouchEnd(TTTouch[] touches)
    {
        foreach (var touch in touches)
        {
            Debug.Log($"触摸结束: id={touch.identifier}");

            // 示例：清除拖拽状态
            // dragStartPos.Remove(touch.identifier);
        }
    }

    void HandleTouchCancel(TTTouch[] touches)
    {
        foreach (var touch in touches)
        {
            Debug.Log($"触摸取消: id={touch.identifier}");

            // 清除所有触摸状态，恢复默认
            // dragStartPos.Remove(touch.identifier);
        }
    }

    void OnDestroy()
    {
        if (TT.InContainerEnv)
        {
            TT.OnTouchStart -= HandleTouchStart;
            TT.OnTouchMove -= HandleTouchMove;
            TT.OnTouchEnd -= HandleTouchEnd;
            TT.OnTouchCancel -= HandleTouchCancel;
        }
    }
}
```

## 七、调试与日志

### 7.1 日志管理器

```csharp
// 日志管理器（写入本地文件）
var logger = TT.GetLogManager();
logger.Log("普通日志");
logger.Info("信息日志");
logger.Warn("警告日志");
logger.Debug("调试日志");

// 实时日志管理器（上传到抖音后台，用于线上问题排查）
var rtLogger = TT.GetRealtimeLogManager();
rtLogger.Info("实时信息");
rtLogger.Warn("实时警告");
rtLogger.Error("实时错误");
rtLogger.SetFilterMsg("keyword_filter"); // 设置过滤关键词，方便后台检索
```

### 7.2 全局错误监听

```csharp
// 监听未捕获的全局异常
// ⚠️ 安全：生产环境禁止打印完整堆栈，避免泄露代码结构/文件路径
TT.OnError += (error) =>
{
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    Debug.LogError($"全局错误: {error.Message}");
    Debug.LogError($"错误堆栈: {error.Stack}");
    #else
    Debug.LogError($"全局错误: {error.Message}");  // 生产仅记录错误消息
    #endif
};
```

### 7.3 内存告警

```csharp
TT.OnMemoryWarning += (level) =>
{
    // level: 5 = 告警, 10 = 严重告警
    if (level >= 10)
    {
        Debug.LogWarning("内存严重不足，紧急释放资源！");
        // 释放纹理缓存
        // Resources.UnloadUnusedAssets();
        // 释放音频缓存
        // AudioManager.Instance.ClearCache();
        // 触发 GC
        System.GC.Collect();
    }
};
```

### 7.4 API 可用性判断

```csharp
// 判断指定 API 在当前宿主版本是否可用
if (TT.CanIUse("RequestGamePayment.object.goodType"))
{
    // 支持道具直购功能
}

if (TT.CanIUse("CreateRewardedVideoAd.object.Multiton"))
{
    // 支持再得广告模式
}
```

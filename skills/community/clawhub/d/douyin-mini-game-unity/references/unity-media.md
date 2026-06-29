# 媒体

> 基于官方文档: 媒体 API - 录屏管理、游戏分享、邀请模块
> 生成时间: 2026-06-24

> ⚠️ **【隐私与安全声明 — 已加固】**：
> - **录屏**：代码示例已内置 `scope.screenRecord` 授权检查，首次录屏时会验证用户授权状态。录制的视频不得在未经用户同意的情况下自动上传。
> - **分享**：分享参数（Title、Query）中不得包含用户敏感信息（手机号、身份证号、openid、session_key 等）。Query 参数中如需传递用户标识，应使用加密的临时 token 而非明文 ID。
> - **邀请**：`inviterId` 等用户标识已用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 条件编译包裹，生产日志仅记录邀请事件维度信息。

## 一、录屏管理

录屏管理器 `TTGameRecorderManager` 提供完整的录屏生命周期管理：启用/禁用录屏、启动/停止录制、获取录制时长与状态、设置背景音乐、控制视频分享等。通过 `TT.GetGameRecorderManager()` 获取单例实例。

### 1.1 TT.GetGameRecorderManager

**说明**: 获取游戏录屏管理器单例。录屏管理器的所有功能均通过该实例调用。在调用任何录屏方法之前必须先获取此实例，且应确保已调用 `TT.InitSDK` 完成初始化。

**语法**:

```csharp
public static TTGameRecorderManager GetGameRecorderManager()
```

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class RecorderDemo : MonoBehaviour
{
    private TTGameRecorderManager _recorder;

    void Start()
    {
        _recorder = TT.GetGameRecorderManager();
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("录屏管理器已获取");
        #endif
    }
}
```

---

### 1.2 IsShowVideoShareToast

**说明**: 是否在视频录制完成后显示视频分享 Toast 提示。设为 `true` 时，录屏停止后会自动弹出分享入口；设为 `false` 则静默保存。

**语法**:

```csharp
public bool IsShowVideoShareToast { get; set; }
```

---

### 1.3 SetEnabled

**说明**: 启用或禁用录屏功能。禁用后无法启动录制，但已录制的内容不会丢失。通常根据关卡解锁状态或用户隐私设置动态控制。

**语法**:

```csharp
public void SetEnabled(bool enabled)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| enabled | bool | 是 | -- | true 启用录屏；false 禁用录屏 |

---

### 1.4 GetEnabled

**说明**: 获取当前录屏功能是否处于启用状态。可用于 UI 按钮的灰度控制。

**语法**:

```csharp
public bool GetEnabled()
```

---

### 1.5 SetCustomKeyFrameInterval

**说明**: 设置自定义关键帧间隔（毫秒）。关键帧间隔影响视频编码的清晰度和文件大小——间隔越短视频越清晰但文件越大。默认值由宿主环境决定。

**语法**:

```csharp
public void SetCustomKeyFrameInterval(int interval)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| interval | int | 是 | -- | 关键帧间隔，单位毫秒。典型值 1000~5000 |

---

### 1.6 Start

**说明**: 开始录屏。调用前需确保已通过 `TT.GetSetting()` 检查 `scope.screenRecord` 授权状态、已启用录屏（`SetEnabled(true)`），且当前不在录制中。重复调用不会产生叠加录制。完整的授权检查模式参见下方「1.12 录屏完整流程示例」及「四、录屏分享最佳实践」。

**语法**:

```csharp
public void Start()
```

---

### 1.7 Stop

**说明**: 停止录屏。停止后视频文件将写入宿主文件系统，并触发 `IsShowVideoShareToast` 对应的分享入口逻辑。

**语法**:

```csharp
public void Stop()
```

---

### 1.8 GetRecordDuration

**说明**: 获取当前已录制时长，单位毫秒。仅在录制进行中返回有意义的值，停止后重置。

**语法**:

```csharp
public long GetRecordDuration()
```

---

### 1.9 GetVideoRecordState

**说明**: 获取当前录屏状态码。通过状态码判断录制是否正在进行、已暂停或已停止。

**语法**:

```csharp
public int GetVideoRecordState()
```

**返回值**:

| 状态码 | 含义 |
|--------|------|
| 0 | 未开始录制 |
| 1 | 录制中 |
| 2 | 录制已暂停 |
| 3 | 录制已停止 |

---

### 1.10 SetDefaultBgm

**说明**: 设置录屏时默认的背景音乐路径。传入本地文件路径即可为录制视频添加 BGM。支持 mp3、aac 等常见音频格式。

**语法**:

```csharp
public void SetDefaultBgm(string bgmPath)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| bgmPath | string | 是 | -- | 本地背景音乐文件路径 |

---

### 1.11 GetVideoShareState

**说明**: 获取视频分享状态。用于判断当前是否有待分享的视频、分享是否完成。

**语法**:

```csharp
public int GetVideoShareState()
```

**返回值**:

| 状态码 | 含义 |
|--------|------|
| 0 | 无可分享的视频 |
| 1 | 有待分享的视频 |

---

### 1.12 录屏完整流程示例

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class GameRecorderFlow : MonoBehaviour
{
    [SerializeField] private Button _startRecordBtn;
    [SerializeField] private Button _stopRecordBtn;
    [SerializeField] private Button _shareVideoBtn;
    [SerializeField] private Text _durationText;

    private TTGameRecorderManager _recorder;
    private bool _isRecording = false;

    void Start()
    {
        _recorder = TT.GetGameRecorderManager();

        // 启用录屏并显示分享 Toast
        _recorder.SetEnabled(true);
        _recorder.IsShowVideoShareToast = true;

        // 设置关键帧间隔为 2 秒
        _recorder.SetCustomKeyFrameInterval(2000);

        // 可选：设置背景音乐
        // _recorder.SetDefaultBgm(Application.streamingAssetsPath + "/bgm.mp3");

        // 绑定 UI
        _startRecordBtn.onClick.AddListener(StartRecording);
        _stopRecordBtn.onClick.AddListener(StopRecording);
        _shareVideoBtn.onClick.AddListener(OnShareVideo);
    }

    void Update()
    {
        if (_isRecording)
        {
            long duration = _recorder.GetRecordDuration();
            _durationText.text = $"已录制: {duration / 1000f:F1} 秒";
        }
    }

    void StartRecording()
    {
        // ⚠️ 安全：录屏前必须检查 scope.screenRecord 授权状态
        // 首次录屏时应展示隐私说明并征得用户明确同意
        TT.GetSetting(
            successCallback: (auth) =>
            {
                if (!auth.ScreenRecord)
                {
                    Debug.LogWarning("录屏权限未授权，请引导用户在设置中开启");
                    return;
                }

                if (_recorder.GetEnabled() && _recorder.GetVideoRecordState() != 1)
                {
                    _recorder.Start();
                    _isRecording = true;
                    #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    Debug.Log("开始录屏");
                    #endif
                }
                else
                {
                    Debug.LogWarning("录屏未启用或已在录制中");
                }
            },
            failedCallback: (err) =>
            {
                Debug.LogWarning($"获取录屏授权状态失败: {err}");
            }
        );
    }

    void StopRecording()
    {
        if (_isRecording)
        {
            _recorder.Stop();
            _isRecording = false;
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"录屏已停止，总时长: {_recorder.GetRecordDuration()}ms");
            #endif

            // 检查是否有待分享的视频
            if (_recorder.GetVideoShareState() == 1)
            {
                _shareVideoBtn.interactable = true;
            }
        }
    }

    void OnShareVideo()
    {
        // 分享视频的入口由 IsShowVideoShareToast 控制
        // 此处可引导用户进行分享操作
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("用户点击了分享视频按钮");
        #endif
    }

    void OnDestroy()
    {
        if (_isRecording)
        {
            _recorder.Stop();
        }
    }
}
```

---

## 二、游戏分享

游戏分享模块提供标题、图片、查询参数、附加信息的自定义能力。分享分为两种模式：
- **被动分享**：用户点击右上角菜单的分享按钮，触发 `OnShareAppMessage` 回调动态设置分享内容。
- **主动分享**：调用 `TT.ShareAppMessage` 直接拉起分享面板。

### 2.1 ShareParam 参数类

**说明**: 分享内容参数对象，用于设置分享标题、图片、查询参数和额外信息。

**定义**:

```csharp
public class ShareParam
{
    public string Title;
    public string ImageUrl;
    public string Query;
    public string Extra;
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| Title | string | 否 | "" | 分享标题，显示在分享卡片上 |
| ImageUrl | string | 否 | "" | 分享图片 URL，建议 5:4 比例 |
| Query | string | 否 | "" | 分享查询参数，接收方可通过启动参数获取（如 `key1=val1&key2=val2`） |
| Extra | string | 否 | "" | 额外信息，可用于埋点或自定义逻辑 |

---

### 2.2 TT.ShareAppMessage

**说明**: 主动拉起分享面板，直接调起抖音分享浮层。适用于游戏内"邀请好友"、"炫耀战绩"等场景。

**语法**:

```csharp
public static void ShareAppMessage(ShareParam param)
```

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class ShareDemo : MonoBehaviour
{
    public void ShareScore()
    {
        // ⚠️ 安全：分享参数中不得包含用户敏感信息（手机号、身份证、openid 等）
        var param = new ShareParam
        {
            Title = "我的分数: 99999，快来挑战！",
            ImageUrl = "https://example.com/share_icon.png",
            // ⚠️ 安全：如需传递用户标识，应使用临时 token 而非明文 ID
            Query = "scene=invite&token=encrypted_share_token",
            Extra = "share_from_score_page"
        };

        TT.ShareAppMessage(param);
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("分享面板已拉起");
        #endif
    }

    public void ShareLevel()
    {
        var param = new ShareParam
        {
            Title = "我通关了第 10 关！",
            ImageUrl = "https://example.com/level10_thumbnail.png",
            Query = "scene=challenge&level=10",
            Extra = ""
        };

        TT.ShareAppMessage(param);
    }
}
```

---

### 2.3 TT.ShowShareMenu

**说明**: 设置是否显示右上角菜单中的分享按钮。在某些场景（如新手引导或敏感页面）可能需要隐藏分享入口。

**语法**:

```csharp
public static void ShowShareMenu(bool show)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| show | bool | 是 | -- | true 显示分享按钮；false 隐藏 |

---

### 2.4 TT.OnShareAppMessage / TT.OffShareAppMessage

**说明**: 监听用户点击右上角分享按钮的事件。回调中可通过 `ref` 参数动态修改分享内容（标题、图片、查询参数等）。必须在用户触发分享前注册监听，否则使用的将是默认分享内容。取消监听使用 `OffShareAppMessage` 防止内存泄漏。

**语法**:

```csharp
public static void OnShareAppMessage(Action<ShareParam> callback)
public static void OffShareAppMessage(Action<ShareParam> callback)
```

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class CustomShareHandler : MonoBehaviour
{
    private int _currentLevel = 1;
    private int _currentScore = 0;

    void Start()
    {
        // 注册分享回调
        TT.OnShareAppMessage(OnShareCallback);
    }

    void OnDestroy()
    {
        // 取消注册，防止内存泄漏
        TT.OffShareAppMessage(OnShareCallback);
    }

    private void OnShareCallback(ShareParam param)
    {
        // 在回调中通过 ref 修改分享内容
        param.Title = $"我在第 {_currentLevel} 关，得分 {_currentScore}！快来超越我吧！";
        param.ImageUrl = $"https://example.com/level_{_currentLevel}_thumb.png";
        param.Query = $"scene=invite&level={_currentLevel}&score={_currentScore}";
        param.Extra = "custom_share_callback";

        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"自定义分享标题: {param.Title}");
        Debug.Log($"自定义分享 Query: {param.Query}");
        #endif
    }

    public void UpdateLevelAndScore(int level, int score)
    {
        _currentLevel = level;
        _currentScore = score;
    }
}
```

---

### 2.5 TT.NavigateToVideoView

**说明**: 跳转到视频详情页。传入视频 ID 即可直接打开抖音视频播放页面。

**语法**:

```csharp
public static void NavigateToVideoView(string videoId)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| videoId | string | 是 | -- | 目标视频的 ID |

---

## 三、邀请模块

邀请模块提供创建邀请面板和监听邀请状态变化的能力，适用于需要社交传播的游戏场景。

### 3.1 TT.CreateInvitePanel

**说明**: 创建并显示邀请面板。用户可以通过面板选择好友发送游戏邀请，面板样式由宿主 App 控制。

**语法**:

```csharp
public static void CreateInvitePanel(InvitePanelParam param)
```

**InvitePanelParam 参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| roomType | string | 否 | "" | 房间类型标识 |
| isGroupMode | bool | 否 | false | 是否群模式邀请 |
| bgm | string | 否 | "" | 背景音乐路径 |
| blockList | string[] | 否 | null | 需要屏蔽的用户 ID 列表 |
| multiplayerExtra | string | 否 | "" | 多人游戏额外参数 |

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class InvitePanelDemo : MonoBehaviour
{
    [SerializeField] private Button _inviteBtn;

    void Start()
    {
        _inviteBtn.onClick.AddListener(OnClickInvite);
    }

    void OnClickInvite()
    {
        var param = new InvitePanelParam
        {
            roomType = "normal_room",
            isGroupMode = false,
            bgm = "",
            blockList = null,
            multiplayerExtra = "gameMode=ranked"
        };

        TT.CreateInvitePanel(param);
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("邀请面板已创建");
        #endif
    }
}
```

---

### 3.2 TT.OnInviteStateChanged / TT.OffInviteStateChanged

**说明**: 监听邀请状态变化。当好友接受或拒绝邀请时触发回调，可用于更新房间状态、跳转游戏场景等。取消监听使用 `OffInviteStateChanged` 防止内存泄漏。

**语法**:

```csharp
public static void OnInviteStateChanged(Action<InviteStateInfo> callback)
public static void OffInviteStateChanged(Action<InviteStateInfo> callback)
```

**InviteStateInfo 属性**:

| 属性 | 类型 | 说明 |
|------|------|------|
| state | string | 邀请状态："accept" 接受 / "refuse" 拒绝 |
| inviterId | string | 邀请者用户 ID |
| inviterNickName | string | 邀请者昵称 |
| query | string | 邀请时携带的查询参数 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class InviteStateListener : MonoBehaviour
{
    void Start()
    {
        TT.OnInviteStateChanged(OnInviteStateChanged);
    }

    void OnDestroy()
    {
        TT.OffInviteStateChanged(OnInviteStateChanged);
    }

    private void OnInviteStateChanged(InviteStateInfo info)
    {
        // ⚠️ 安全：inviterNickName 为用户昵称，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"邀请状态变化: {info.state}, 来自: {info.inviterNickName}");
        #else
        Debug.Log($"邀请状态变化: {info.state}");
        #endif

        switch (info.state)
        {
            case "accept":
                OnInviteAccepted(info);
                break;
            case "refuse":
                OnInviteRefused(info);
                break;
        }
    }

    private void OnInviteAccepted(InviteStateInfo info)
    {
        // ⚠️ 安全：inviterId 为永久用户标识，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"邀请者 {info.inviterNickName}(id:{info.inviterId}) 接受了邀请");
        Debug.Log($"携带参数: {info.query}");
        #else
        Debug.Log("邀请已被接受");
        #endif

        // 解析 query 参数并进入相应游戏场景
        // 例如: "gameMode=ranked&roomId=abc123"
    }

    private void OnInviteRefused(InviteStateInfo info)
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"邀请者 {info.inviterNickName}(id:{info.inviterId}) 拒绝了邀请");
        #else
        Debug.Log("邀请已被拒绝");
        #endif
        // 可选：显示 Toast 提示
    }
}
```

---

## 四、录屏分享最佳实践

将录屏与分享功能结合使用，实现"录制精彩时刻 + 分享到抖音"的完整闭环。

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

/// <summary>
/// 录屏分享最佳实践：录制精彩时刻后引导用户分享
/// </summary>
public class RecordAndShare : MonoBehaviour
{
    [SerializeField] private Button _recordBtn;
    [SerializeField] private Button _stopRecordBtn;
    [SerializeField] private Text _statusText;

    private TTGameRecorderManager _recorder;

    void Start()
    {
        // 初始化 SDK
        TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("SDK 初始化成功，准备录屏功能");
                #endif
                InitRecorder();
            }
        });
    }

    void InitRecorder()
    {
        _recorder = TT.GetGameRecorderManager();

        // ⚠️ 安全：启用录屏前必须检查 scope.screenRecord 授权状态
        TT.GetSetting(
            successCallback: (auth) =>
            {
                if (!auth.ScreenRecord)
                {
                    Debug.LogWarning("录屏权限未授权，请引导用户在设置中开启");
                    return;
                }

                _recorder.SetEnabled(true);
                _recorder.IsShowVideoShareToast = true; // 录制完成后自动弹出分享入口
                _recorder.SetCustomKeyFrameInterval(2000);
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("录屏已启用");
                #endif
            },
            failedCallback: (err) =>
            {
                Debug.LogWarning($"获取录屏授权状态失败: {err}");
            }
        );

        _recordBtn.onClick.AddListener(() =>
        {
            _recorder.Start();
            _statusText.text = "录制中...";
            _recordBtn.interactable = false;
            _stopRecordBtn.interactable = true;
        });

        _stopRecordBtn.onClick.AddListener(() =>
        {
            _recorder.Stop();
            _statusText.text = $"录制完成，时长 {_recorder.GetRecordDuration() / 1000f:F1} 秒";
            _recordBtn.interactable = true;
            _stopRecordBtn.interactable = false;

            // IsShowVideoShareToast = true 时系统会自动弹出分享入口
            // 也可通过 GetVideoShareState() 手动检查
        });
    }

    void OnDestroy()
    {
        if (_recorder != null)
        {
            _recorder.Stop();
        }
    }
}
```

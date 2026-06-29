# 界面与渲染

> 基于官方文档: 界面 API - 键盘输入、敏感词检测、鼠标光标、帧率控制、系统字体
> 生成时间: 2026-06-24

## 一、键盘输入

键盘输入模块提供唤起/隐藏系统键盘、更新键盘参数以及监听键盘输入事件的能力。适用于登录表单、聊天输入、搜索框等文本输入场景。键盘事件采用 On/Off 配对监听模式，务必在合适时机取消监听防止内存泄漏。

### 1.1 TT.ShowKeyboard

**说明**: 显示系统键盘，唤起文本输入。适用于需要用户输入文字的场景（昵称设置、聊天消息、搜索等）。调用后系统弹出原生键盘，输入结果通过键盘事件回调获取。

**语法**:

```csharp
public static void ShowKeyboard(ShowKeyboardParam param)
```

#### ShowKeyboardParam 参数类

**说明**: 键盘显示配置参数。

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| DefaultValue | string | 否 | "" | 默认输入内容，键盘弹出时预填充 |
| MaxLength | int | 否 | 100 | 最大输入长度，超出后不可继续输入 |
| Multiple | bool | 否 | false | 是否多行输入。true 时键盘支持换行 |
| ConfirmHold | bool | 否 | false | 是否保持键盘。true 时点击确认按钮不会自动收起键盘 |
| ConfirmType | string | 否 | "done" | 确认按钮类型。可选值: "done"(完成) / "send"(发送) / "search"(搜索) / "next"(下一步) / "go"(前往) |

---

### 1.2 TT.HideKeyboard

**说明**: 隐藏系统键盘。强制收起当前弹出的键盘，输入内容保留在最后一次状态。

**语法**:

```csharp
public static void HideKeyboard()
```

---

### 1.3 TT.UpdateKeyboard

**说明**: 更新已弹出键盘的参数。无需收起再弹出即可动态修改键盘的默认值、长度限制等属性。

**语法**:

```csharp
public static void UpdateKeyboard(ShowKeyboardParam param)
```

---

### 1.4 TT.OnKeyboardComplete / TT.OffKeyboardComplete

**说明**: 监听键盘输入完成事件。用户点击键盘的确认按钮后触发。与 `OnKeyboardConfirm` 的区别在于：此事件仅当键盘收起时触发，内部已包含确认逻辑。取消监听使用 `OffKeyboardComplete` 防止内存泄漏。

**语法**:

```csharp
public static void OnKeyboardComplete(Action<string> callback)
public static void OffKeyboardComplete(Action<string> callback)
```

**回调参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| value | string | 输入完成时的最终文本值 |

---

### 1.5 TT.OnKeyboardConfirm / TT.OffKeyboardConfirm

**说明**: 监听键盘确认按钮点击事件。用户点击确认按钮时立即触发，此时键盘可能尚未收起（取决于 `ConfirmHold` 参数）。取消监听使用 `OffKeyboardConfirm`。

**语法**:

```csharp
public static void OnKeyboardConfirm(Action<string> callback)
public static void OffKeyboardConfirm(Action<string> callback)
```

**回调参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| value | string | 点击确认按钮时的文本值 |

---

### 1.6 TT.OnKeyboardInput / TT.OffKeyboardInput

**说明**: 监听键盘每次输入变化事件。用户每次按键（增删字符）都会触发，适合实现实时字数统计、搜索建议等场景。取消监听使用 `OffKeyboardInput`。

**语法**:

```csharp
public static void OnKeyboardInput(Action<string> callback)
public static void OffKeyboardInput(Action<string> callback)
```

**回调参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| value | string | 当前输入框中的文本值 |

---

### 1.7 键盘输入完整流程示例

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class KeyboardFlowDemo : MonoBehaviour
{
    [SerializeField] private InputField _inputField;
    [SerializeField] private Button _showKeyboardBtn;
    [SerializeField] private Button _hideKeyboardBtn;
    [SerializeField] private Text _charCountText;
    [SerializeField] private Text _resultText;

    private int _maxLength = 20;

    void Start()
    {
        _showKeyboardBtn.onClick.AddListener(OnShowKeyboard);
        _hideKeyboardBtn.onClick.AddListener(OnHideKeyboard);

        // 注册键盘事件监听
        TT.OnKeyboardInput(OnKeyboardInput);
        TT.OnKeyboardConfirm(OnKeyboardConfirm);
        TT.OnKeyboardComplete(OnKeyboardComplete);
    }

    void OnDestroy()
    {
        // 取消所有键盘事件监听，防止内存泄漏
        TT.OffKeyboardInput(OnKeyboardInput);
        TT.OffKeyboardConfirm(OnKeyboardConfirm);
        TT.OffKeyboardComplete(OnKeyboardComplete);
    }

    void OnShowKeyboard()
    {
        var param = new ShowKeyboardParam
        {
            DefaultValue = _inputField.text,
            MaxLength = _maxLength,
            Multiple = false,
            ConfirmHold = false,
            ConfirmType = "done"
        };

        TT.ShowKeyboard(param);
        Debug.Log("系统键盘已弹出");
    }

    void OnHideKeyboard()
    {
        TT.HideKeyboard();
    }

    // 每次输入变化时触发：实时更新字数统计
    private void OnKeyboardInput(string value)
    {
        _charCountText.text = $"{value.Length}/{_maxLength}";
        _inputField.text = value;
    }

    // 点击确认按钮时触发
    private void OnKeyboardConfirm(string value)
    {
        // ⚠️ 安全：用户输入内容禁止打印到生产日志
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"用户确认输入: {value}");
        #else
        Debug.Log("用户确认输入");
        #endif
    }

    // 键盘收起且输入完成时触发
    private void OnKeyboardComplete(string value)
    {
        _resultText.text = $"输入结果: {value}";
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"键盘输入完成，最终值: {value}");
        #else
        Debug.Log($"键盘输入完成，长度: {value?.Length ?? 0} 字符");
        #endif

        // 在 Complete 后再调用 UpdateKeyboard 可以动态修改参数
        // 例如限制最大长度
    }

    // 动态限制最大长度的方法
    public void SetMaxLength(int maxLength)
    {
        _maxLength = maxLength;
        var param = new ShowKeyboardParam
        {
            MaxLength = _maxLength
        };
        TT.UpdateKeyboard(param);
    }
}
```

---

## 二、敏感词检测

敏感词检测模块用于过滤用户生成内容（UGC）中的违规文本，保障游戏内容的合规性。提供两种模式：布尔检测（判断是否含敏感词）和替换检测（将敏感词替换为指定字符）。

### 2.1 TT.SensitiveWordCheck

**说明**: 异步检查文本是否包含敏感词。检测结果通过回调返回布尔值，`true` 表示包含敏感词需要拦截，`false` 表示文本合规。适用于发布前预检场景。

**语法**:

```csharp
public static void SensitiveWordCheck(string text, Action<bool> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| text | string | 是 | -- | 待检测的文本内容 |
| callback | Action\<bool\> | 是 | -- | 检测结果回调。true = 含敏感词，false = 不含 |

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class SensitiveWordDemo : MonoBehaviour
{
    [SerializeField] private InputField _inputField;
    [SerializeField] private Button _checkBtn;
    [SerializeField] private Text _resultText;

    void Start()
    {
        _checkBtn.onClick.AddListener(OnCheckSensitive);
    }

    void OnCheckSensitive()
    {
        string userInput = _inputField.text;

        if (string.IsNullOrEmpty(userInput))
        {
            _resultText.text = "请输入文本后再检测";
            return;
        }

        TT.SensitiveWordCheck(userInput, (hasSensitive) =>
        {
            if (hasSensitive)
            {
                _resultText.text = "检测结果: 包含敏感词，请修改后重新提交";
                Debug.LogWarning("文本包含敏感词，已拦截");
            }
            else
            {
                _resultText.text = "检测结果: 通过，文本合规";
                Debug.Log("文本检测通过");
            }
        });
    }
}
```

---

### 2.2 TT.ReplaceSensitiveWords

**说明**: 同步替换文本中的敏感词为指定字符。检测与替换过程在本地完成，返回替换后的安全文本。适用于实时预览、聊天消息过滤等场景。

**语法**:

```csharp
public static string ReplaceSensitiveWords(string text, string replacement = "*")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| text | string | 是 | -- | 待过滤的原始文本 |
| replacement | string | 否 | "*" | 替换敏感词的字符，默认为星号 |

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class ReplaceSensitiveDemo : MonoBehaviour
{
    [SerializeField] private InputField _inputField;
    [SerializeField] private Text _previewText;

    public void OnUserInputChanged(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            _previewText.text = "";
            return;
        }

        // 同步替换敏感词，用 "#" 替代默认的 "*"
        string filteredText = TT.ReplaceSensitiveWords(input, "#");
        _previewText.text = filteredText;

        if (filteredText != input)
        {
            Debug.Log("检测到敏感词并已替换");
        }
    }

    // 结合异步检查的完整流程
    public void SubmitUserContent(string content)
    {
        // 步骤1: 先同步替换敏感词作为兜底
        string safeContent = TT.ReplaceSensitiveWords(content, "*");

        // 步骤2: 异步精确检测
        TT.SensitiveWordCheck(safeContent, (hasSensitive) =>
        {
            if (hasSensitive)
            {
                Debug.LogWarning("替换后仍含未覆盖的敏感词，需进一步处理");
                // 提示用户修改内容
            }
            else
            {
                Debug.Log("内容合规，可以提交");
                // 执行提交逻辑
                SubmitToServer(safeContent);
            }
        });
    }

    private void SubmitToServer(string content)
    {
        // ⚠️ 安全：用户生成内容禁止打印到生产日志
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"提交内容到服务器: {content}");
        #else
        Debug.Log("内容已提交到服务器");
        #endif
    }
}
```

---

## 三、光标样式（PC 端）

PC 端宿主环境下可自定义鼠标光标样式和指针锁定状态。`Cursor` 为引擎内置静态类，`TT` 提供指针锁定相关 API。主要用于 FPS 游戏的视角控制、策略游戏的拖拽操作等场景。

### 3.1 Cursor.SetCursor

**说明**: 设置鼠标光标样式。传入预定义的光标类型字符串即可切换，适用于 PC 端的 UI 交互反馈。

**语法**:

```csharp
public static void SetCursor(string cursorType)
```

**支持的光标类型**:

| 值 | 说明 | 适用场景 |
|------|------|------|
| "default" | 默认箭头 | 通用场景 |
| "pointer" | 手型指针 | 可点击元素的悬停 |
| "text" | 文本输入 I 型 | 文本输入区域 |
| "crosshair" | 十字准星 | 瞄准、精确点击 |
| "move" | 移动十字 | 拖拽移动 |
| "not-allowed" | 禁止标识 | 不可交互区域 |
| "grab" | 抓手 | 可拖拽抓取 |
| "grabbing" | 抓取中 | 拖拽进行中 |
| "wait" | 等待沙漏 | 加载中 |
| "help" | 帮助问号 | 帮助信息提示 |

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.EventSystems;
using TT;

public class CursorStyleDemo : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    void Start()
    {
        // 初始设置默认光标
        SetCursor("default");
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        // 鼠标进入按钮区域 — 切换为手型
        SetCursor("pointer");
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        // 鼠标离开 — 恢复默认
        SetCursor("default");
    }

    // 瞄准模式
    public void EnterAimMode()
    {
        SetCursor("crosshair");
    }

    // 加载状态
    public void ShowLoading()
    {
        SetCursor("wait");
    }

    // 禁用交互
    public void DisableInteraction()
    {
        SetCursor("not-allowed");
    }
}
```

---

### 3.2 TT.RequestPointerLock

**说明**: 请求锁定鼠标指针。锁定后鼠标光标隐藏，移动事件转为旋转增量，典型用于 FPS 游戏的视角控制。调用后需要等待用户交互（点击）完成锁定。

**语法**:

```csharp
public static void RequestPointerLock()
```

---

### 3.3 TT.IsPointerLocked

**说明**: 判断鼠标指针当前是否处于锁定状态。

**语法**:

```csharp
public static bool IsPointerLocked()
```

---

### 3.4 TT.ExitPointerLock

**说明**: 退出鼠标指针锁定，恢复显示光标和正常移动。

**语法**:

```csharp
public static void ExitPointerLock()
```

---

### 3.5 指针锁定完整流程（FPS 游戏视角控制）

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

/// <summary>
/// FPS 游戏鼠标指针锁定示例
/// </summary>
public class MouseLookFPSCamera : MonoBehaviour
{
    [SerializeField] private float _mouseSensitivity = 2.0f;
    [SerializeField] private Text _lockStatusText;

    private float _rotationX = 0f;
    private bool _isLocked = false;

    void Start()
    {
        // 游戏开始时请求锁定指针
        LockPointer();
    }

    void Update()
    {
        // 按 ESC 退出锁定
        if (Input.GetKeyDown(KeyCode.Escape) && _isLocked)
        {
            UnlockPointer();
        }

        // 点击鼠标左键重新锁定
        if (Input.GetMouseButtonDown(0) && !TT.IsPointerLocked())
        {
            LockPointer();
        }

        // 检测锁定状态变化
        _isLocked = TT.IsPointerLocked();
        _lockStatusText.text = _isLocked ? "指针已锁定 (ESC 退出)" : "指针已解锁 (点击屏幕锁定)";

        // 锁定状态下处理视角旋转
        if (_isLocked)
        {
            float mouseX = Input.GetAxis("Mouse X") * _mouseSensitivity;
            float mouseY = Input.GetAxis("Mouse Y") * _mouseSensitivity;

            // 水平旋转（Y 轴）：旋转玩家角色
            transform.Rotate(Vector3.up * mouseX);

            // 垂直旋转（X 轴）：旋转摄像机上下
            _rotationX -= mouseY;
            _rotationX = Mathf.Clamp(_rotationX, -90f, 90f);
            Camera.main.transform.localRotation = Quaternion.Euler(_rotationX, 0f, 0f);
        }
    }

    public void LockPointer()
    {
        TT.RequestPointerLock();
        Debug.Log("已请求指针锁定");
    }

    public void UnlockPointer()
    {
        TT.ExitPointerLock();
        Debug.Log("已退出指针锁定");
    }
}
```

---

## 四、帧率控制

### 4.1 TT.SetPreferredFramesPerSecond

**说明**: 设置游戏期望的目标帧率。宿主会尽可能匹配目标帧率，但实际帧率受设备性能、系统节电策略等因素影响。合理设置帧率可平衡画面流畅度与设备发热/耗电。

**语法**:

```csharp
public static void SetPreferredFramesPerSecond(int fps)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| fps | int | 是 | -- | 目标帧率。常见值为 30（省电模式）、60（标准模式）。部分设备支持 90 或 120 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class FrameRateController : MonoBehaviour
{
    void Start()
    {
        // 初始化后设置目标帧率
        TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                // 默认 60fps 流畅体验
                TT.SetPreferredFramesPerSecond(60);
                Debug.Log("目标帧率已设置为 60fps");
            }
        });
    }

    // 根据游戏场景动态调整帧率
    public void EnterMainMenu()
    {
        // 主菜单不需要高帧率，降低功耗
        TT.SetPreferredFramesPerSecond(30);
    }

    public void EnterGameplay()
    {
        // 进入游戏战斗场景，恢复高帧率
        TT.SetPreferredFramesPerSecond(60);
    }

    public void EnterBatterySaveMode()
    {
        // 低电量模式下进一步降低帧率
        TT.SetPreferredFramesPerSecond(30);
    }

    // 部分高端设备可尝试 90/120fps
    public void EnableHighFrameRate()
    {
        // 注意：需检测设备是否支持，不支持的设备会降至最高可用帧率
        TT.SetPreferredFramesPerSecond(120);
    }
}
```

---

## 五、系统字体

### 5.1 TT.GetSystemFont

**说明**: 获取宿主系统的默认字体文件路径。返回路径可直接用于 Unity 的 `Font` 加载。在抖音容器环境中，不同宿主 App 可能提供不同字体，通过此接口可获取统一的系统字体确保文本渲染一致性。

**语法**:

```csharp
public static string GetSystemFont()
```

**代码示例**:

```csharp
using UnityEngine;
using UnityEngine.UI;
using TT;

public class SystemFontDemo : MonoBehaviour
{
    [SerializeField] private Text _systemFontText;
    [SerializeField] private Text _fontPathText;

    void Start()
    {
        LoadSystemFont();
    }

    void LoadSystemFont()
    {
        TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                // 获取系统字体路径
                string fontPath = TT.GetSystemFont();
                _fontPathText.text = $"字体路径: {fontPath}";
                Debug.Log($"系统字体路径: {fontPath}");

                if (!string.IsNullOrEmpty(fontPath))
                {
                    // 方式1: 通过 Resources 或 AssetBundle 加载
                    // Font sysFont = Resources.Load<Font>(fontPath);
                    // _systemFontText.font = sysFont;

                    // 方式2: 如果路径返回的是完整文件路径，可通过 WWW/UnityWebRequest 加载
                    StartCoroutine(LoadFontFromPath(fontPath));
                }
                else
                {
                    Debug.LogWarning("无法获取系统字体路径，使用默认字体");
                }
            }
        });
    }

    private System.Collections.IEnumerator LoadFontFromPath(string fontPath)
    {
        using (var www = UnityEngine.Networking.UnityWebRequest.Get("file://" + fontPath))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                // 注意：运行时从文件系统加载字体需要字体文件格式正确
                Debug.Log("系统字体文件加载成功");
            }
            else
            {
                Debug.LogError($"系统字体加载失败: {www.error}");
            }
        }
    }

    // 使用系统字体渲染文本
    public void ApplySystemFont(Text targetText)
    {
        string fontPath = TT.GetSystemFont();
        if (!string.IsNullOrEmpty(fontPath))
        {
            Debug.Log($"应用系统字体到目标文本: {fontPath}");
            // 根据返回的路径加载并应用字体
        }
    }
}
```

---

## 六、调试工具

> ⚠️ **【安全警告 — 调试命令生产禁用】**：以下调试工具（`EnableTTSDKDebugToast`、`RegisterCommandEvent`）**仅限开发调试阶段使用**。所有调试功能**必须**用条件编译（`#if UNITY_EDITOR || DEVELOPMENT_BUILD`）包裹，生产包中**严禁**保留任何调试入口。GM 指令如 `add_resource`、`jump_level` 等在生产环境中会直接导致经济系统崩溃和作弊泛滥。

### 6.1 TT.EnableTTSDKDebugToast

**说明**: 启用或禁用 TTSDK 调试 Toast。开启后，每次调用 `TT.*` API 时会在屏幕底部显示 Toast 提示（包含方法名和简要结果），方便开发阶段追踪 API 调用链路。**仅应在调试阶段开启，正式发布前务必关闭。**

**语法**:

```csharp
public static void EnableTTSDKDebugToast(bool enable)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| enable | bool | 是 | -- | true 启用调试 Toast；false 关闭 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class DebugToolsDemo : MonoBehaviour
{
    void Start()
    {
        TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                // 仅在开发版本中启用调试 Toast
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    TT.EnableTTSDKDebugToast(true);
                    Debug.Log("TTSDK 调试 Toast 已启用");
                #else
                    TT.EnableTTSDKDebugToast(false);
                #endif
            }
        });
    }
}
```

---

### 6.2 TT.RegisterCommandEvent

**说明**: 注册自定义命令事件，用于与开发者工具进行交互。注册后可通过开发者工具面板向游戏发送命令，触发自定义逻辑（如调试面板开关、GM 指令等）。

**语法**:

```csharp
public static void RegisterCommandEvent(string cmd, Action<string> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| cmd | string | 是 | -- | 命令名称，用于匹配开发者工具发送的指令 |
| callback | Action\<string\> | 是 | -- | 命令触发时的回调，参数为命令携带的数据 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class CommandEventDemo : MonoBehaviour
{
    void Start()
    {
        TT.InitSDK((code, env) =>
        {
            if (code == 0)
            {
                // ⚠️ 安全强制：调试命令仅在开发版本中注册
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                RegisterDebugCommands();
                #else
                Debug.Log("生产环境：调试命令已禁用");
                #endif
            }
        });
    }

    // ⚠️ 整个方法仅存在于开发版本中
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    void RegisterDebugCommands()
    {
        // 注册调试开关命令
        TT.RegisterCommandEvent("toggle_debug_panel", (data) =>
        {
            Debug.Log($"收到 toggle_debug_panel 命令，参数: {data}");
            ToggleDebugPanel(data);
        });

        // 注册添加资源命令
        TT.RegisterCommandEvent("add_resource", (data) =>
        {
            Debug.Log($"收到 add_resource 命令，参数: {data}");
            // 解析 data 并添加资源
            // 格式: "gold=1000&diamond=50"
            ParseAndAddResource(data);
        });

        // 注册跳转关卡命令
        TT.RegisterCommandEvent("jump_level", (data) =>
        {
            if (int.TryParse(data, out int levelId))
            {
                Debug.Log($"GM 跳转到关卡: {levelId}");
                JumpToLevel(levelId);
            }
            else
            {
                Debug.LogWarning($"无效的关卡 ID: {data}");
            }
        });
    }

    private void ToggleDebugPanel(string data)
    {
        // 显示/隐藏调试面板
        Debug.Log($"调试面板切换: {data}");
    }

    private void ParseAndAddResource(string data)
    {
        // 解析类似 "gold=1000&diamond=50" 的字符串
        var pairs = data.Split('&');
        foreach (var pair in pairs)
        {
            var kv = pair.Split('=');
            if (kv.Length == 2)
            {
                Debug.Log($"添加资源: {kv[0]} = {kv[1]}");
            }
        }
    }

    private void JumpToLevel(int levelId)
    {
        Debug.Log($"执行跳转: 关卡 {levelId}");
        // 实际的场景加载逻辑
    }
    #endif
}
```

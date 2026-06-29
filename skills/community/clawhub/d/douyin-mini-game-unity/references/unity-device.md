# 设备能力

> 基于官方文档: 设备 API - 加速度计、剪贴板、屏幕、震动、陀螺仪、设备方向、键盘、鼠标、滚轮、网络状态
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **剪贴板**：读写系统剪贴板前应获得用户明确同意，避免静默读取。读取到内容后做最小化处理，写入内容不得包含用户个人隐私信息（已在对应示例中标注）
> - **传感器**：加速度计、陀螺仪、设备方向等传感器**无需 scope 授权**即可使用，但应遵循 OnEnable/OnDisable 生命周期管理，避免后台持续采集导致耗电（详见「十一、设备能力最佳实践」）。传感器原始数据本身不敏感，但持续高频的传感器日志可能用于行为指纹分析，建议高频日志用条件编译管理
> - **位置**：位置 API（`GetLocation`）不在本文档覆盖范围内。如需使用，调用前必须做 `scope.userLocation` 授权检查，且经纬度数据为敏感信息，生产环境禁止打印日志
> - **网络状态**：网络类型信息在客户端属于低风险数据，服务端采集时应在隐私政策中披露

## 一、加速度计

### 1.1 TT.StartAccelerometer

**说明**: 开始监听加速度计数据。加速度计用于检测设备在 x、y、z 三轴上的线性加速度变化，适用于赛车倾斜操控、摇一摇检测、自由落体判断等场景。采样间隔可选三种模式，游戏场景推荐使用 `"game"`（20ms）以获得更灵敏的响应。

**语法**:

```csharp
public static void StartAccelerometer(string interval = "game")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| interval | string | 否 | "game" | 采样间隔。`"game"` = 20ms，`"ui"` = 60ms，`"normal"` = 200ms |

---

### 1.2 TT.StopAccelerometer

**说明**: 停止监听加速度计数据。游戏暂停或切换到后台时可调用此方法释放传感器资源，降低功耗。

**语法**:

```csharp
public static void StopAccelerometer()
```

---

### 1.3 TT.OnAccelerometerChange / TT.OffAccelerometerChange

**说明**: 注册/注销加速度计数据变化回调。每次采样周期到达时触发，返回三轴加速度值。

**语法**:

```csharp
public static void OnAccelerometerChange(Action<float, float, float> callback)
public static void OffAccelerometerChange(Action<float, float, float> callback)
```

**回调参数说明**:

| 参数 | 类型 | 说明 |
|------|------|------|
| x | float | X 轴加速度，单位 m/s²，范围 [-10, 10] |
| y | float | Y 轴加速度，单位 m/s²，范围 [-10, 10] |
| z | float | Z 轴加速度，单位 m/s²，范围 [-10, 10] |

- 设备水平静置时: x ≈ 0, y ≈ 0, z ≈ -9.8（重力加速度）
- 设备自由落体时: x ≈ 0, y ≈ 0, z ≈ 0

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class AccelerometerController : MonoBehaviour
{
    private Action<float, float, float> m_AccelCallback;

    void OnEnable()
    {
        m_AccelCallback = OnAccelDataChanged;
        TT.OnAccelerometerChange(m_AccelCallback);
        TT.StartAccelerometer("game"); // 游戏场景使用最高采样频率
    }

    void OnDisable()
    {
        TT.StopAccelerometer();
        TT.OffAccelerometerChange(m_AccelCallback);
    }

    private void OnAccelDataChanged(float x, float y, float z)
    {
        // 示例: 根据倾斜角度控制角色移动
        Vector3 tilt = new Vector3(x, y, z);
        Debug.Log($"加速度: x={x:F2}, y={y:F2}, z={z:F2}");

        // 摇一摇检测: 任意轴加速度超过阈值
        if (Mathf.Abs(x) > 8.0f || Mathf.Abs(y) > 8.0f || Mathf.Abs(z) > 8.0f)
        {
            Debug.Log("检测到摇一摇！");
            OnShakeDetected();
        }
    }

    private void OnShakeDetected()
    {
        // 触发摇晃事件逻辑
    }
}
```

---

## 二、剪贴板

> ⚠️ **【隐私合规警告】**：剪贴板是用户隐私敏感数据通道。读取剪贴板前**必须获得用户明确同意**，禁止静默读取；写入剪贴板不得包含用户个人隐私信息（手机号、身份证、openid 等）。建议在生产环境中做如下限制：
> - 读取前弹出确认弹窗说明用途
> - 仅提取必要字段（如兑换码格式校验），丢弃无关内容
> - 写入内容应脱敏处理

### 2.1 TT.GetClipboardData

**说明**: 获取系统剪贴板内容。异步操作，通过回调返回剪贴板文本。可用于实现"从剪贴板读取兑换码"等功能。**⚠️ 生产环境中必须获得用户明确同意后才可调用。**

**语法**:

```csharp
public static void GetClipboardData(Action<string> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<string\> | 是 | - | 回调函数，参数为剪贴板文本内容 |

---

### 2.2 TT.SetClipboardData

**说明**: 设置系统剪贴板内容。将文本写入剪贴板，用户可在其他 App 中粘贴使用。**⚠️ 生产环境中写入内容不得包含用户个人隐私信息，建议做脱敏处理。**

**语法**:

```csharp
public static void SetClipboardData(string data)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| data | string | 是 | - | 要写入剪贴板的文本内容 |

**代码示例**:

```csharp
// ⚠️ 安全：读取剪贴板前展示确认弹窗，获得用户同意
public void ReadClipboardWithConsent()
{
    // 展示确认弹窗，说明用途
    ShowConsentDialog("是否允许读取剪贴板中的兑换码？", () =>
    {
        TT.GetClipboardData((clipboardText) =>
        {
            if (!string.IsNullOrEmpty(clipboardText))
            {
                // ⚠️ 安全：仅提取符合条件的兑换码格式，丢弃无关内容（数据最小化）
                if (clipboardText.StartsWith("REDEEM_"))
                {
                    #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    Debug.Log("从剪贴板获取到兑换码");
                    #endif
                    RedeemCode(clipboardText);
                }
                // ⚠️ 不匹配的内容直接丢弃，不做任何存储或日志记录
            }
        });
    });
}

// ⚠️ 安全：写入剪贴板的邀请码不包含用户个人信息
public void CopyShareCode()
{
    // 生成不含用户隐私的纯业务分享码
    string inviteCode = "INVITE_" + System.Guid.NewGuid().ToString("N").Substring(0, 8);
    TT.SetClipboardData(inviteCode);
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    Debug.Log("邀请码已复制到剪贴板");
    #endif
}

private void ShowConsentDialog(string message, System.Action onConsent)
{
    // 展示确认弹窗，用户同意后才执行 onConsent
}

private void RedeemCode(string code)
{
    // 兑换码验证逻辑
}
```

---

## 三、屏幕控制

### 3.1 TT.SetKeepScreenOn

**说明**: 设置是否保持屏幕常亮。游戏运行时通常需要保持屏幕常亮，避免因用户不操作而自动息屏。注意: 离开游戏后设置自动失效。

**语法**:

```csharp
public static void SetKeepScreenOn(bool keepScreenOn)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| keepScreenOn | bool | 是 | - | `true` 保持屏幕常亮，`false` 允许自动息屏 |

---

### 3.2 TT.GetScreenBrightness

**说明**: 获取当前屏幕亮度值。异步操作，通过回调返回 0~1 之间的浮点数。

**语法**:

```csharp
public static void GetScreenBrightness(Action<float> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<float\> | 是 | - | 回调函数，参数为亮度值（0 = 最暗，1 = 最亮） |

---

### 3.3 TT.SetScreenBrightness

**说明**: 设置屏幕亮度。取值范围 0~1，超出范围会被自动裁剪。部分设备可能不支持程序化调整亮度。

**语法**:

```csharp
public static void SetScreenBrightness(float value)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| value | float | 是 | - | 亮度值，范围 [0, 1] |

**代码示例**:

```csharp
// 游戏启动时保持屏幕常亮
void Start()
{
    if (TT.InContainerEnv)
    {
        TT.SetKeepScreenOn(true);

        // 读取并保存当前亮度
        TT.GetScreenBrightness((brightness) =>
        {
            Debug.Log($"当前屏幕亮度: {brightness}");
        });

        // 适当调整亮度以优化游戏视觉
        TT.SetScreenBrightness(0.8f);
    }
}

// 暂停界面中的亮度滑块绑定
public void OnBrightnessSliderChanged(float value)
{
    TT.SetScreenBrightness(value);
}
```

---

## 四、震动

### 4.1 TT.Vibrate

**说明**: 触发短震动效果（约 15ms）。用于游戏中的打击反馈、操作确认、提醒等场景。注意: iOS 设备需在用户交互事件中首次触发后才能正常使用震动。

**语法**:

```csharp
public static void Vibrate()
```

**代码示例**:

```csharp
/// <summary>
/// 触发长震动（通过连续短震动模拟，约 400ms）
/// </summary>
public void VibrateLong()
{
    StartCoroutine(VibrateLongCoroutine());
}

private System.Collections.IEnumerator VibrateLongCoroutine()
{
    // 通过多次短震动模拟长震动效果
    for (int i = 0; i < 8; i++)
    {
        TT.Vibrate();
        yield return new WaitForSeconds(0.05f);
    }
}

// 使用示例: 按钮点击短震，Boss 击杀长震
public void OnButtonClicked()
{
    TT.Vibrate(); // 短震动: 触觉反馈确认
}

public void OnBossKilled()
{
    VibrateLong(); // 长震动: 强烈的击杀反馈
}
```

---

## 五、陀螺仪

### 5.1 TT.StartGyroscope

**说明**: 开始监听陀螺仪数据。陀螺仪用于检测设备绕各轴的旋转角速度，适用于 FPS 视角控制、平衡球游戏、AR 场景等需要高精度旋转感知的场景。

**语法**:

```csharp
public static void StartGyroscope(string interval = "game")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| interval | string | 否 | "game" | 采样间隔。`"game"` = 20ms，`"ui"` = 60ms，`"normal"` = 200ms |

---

### 5.2 TT.StopGyroscope

**说明**: 停止监听陀螺仪数据。与 StartGyroscope 配对使用，释放传感器资源。

**语法**:

```csharp
public static void StopGyroscope()
```

---

### 5.3 TT.OnGyroscopeChange / TT.OffGyroscopeChange

**说明**: 注册/注销陀螺仪数据变化回调。返回三轴旋转角速度值。

**语法**:

```csharp
public static void OnGyroscopeChange(Action<float, float, float> callback)
public static void OffGyroscopeChange(Action<float, float, float> callback)
```

**回调参数说明**:

| 参数 | 类型 | 说明 |
|------|------|------|
| x | float | 绕 X 轴（pitch）角速度，单位 rad/s |
| y | float | 绕 Y 轴（roll）角速度，单位 rad/s |
| z | float | 绕 Z 轴（yaw）角速度，单位 rad/s |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class GyroscopeCamera : MonoBehaviour
{
    private Action<float, float, float> m_GyroCallback;
    private float m_Sensitivity = 2.0f;

    void OnEnable()
    {
        m_GyroCallback = OnGyroDataChanged;
        TT.OnGyroscopeChange(m_GyroCallback);
        TT.StartGyroscope("game");
    }

    void OnDisable()
    {
        TT.StopGyroscope();
        TT.OffGyroscopeChange(m_GyroCallback);
    }

    private void OnGyroDataChanged(float x, float y, float z)
    {
        // 利用陀螺仪角速度旋转相机（第一人称视角控制）
        float rotationX = y * m_Sensitivity * Time.deltaTime; // 左右旋转 (roll)
        float rotationY = x * m_Sensitivity * Time.deltaTime; // 上下旋转 (pitch)

        // 限制垂直角度防止翻转
        Vector3 euler = transform.eulerAngles;
        euler.x = Mathf.Clamp(euler.x - rotationY * Mathf.Rad2Deg, -80f, 80f);
        euler.y += rotationX * Mathf.Rad2Deg;
        transform.eulerAngles = euler;
    }
}
```

---

## 六、设备方向

### 6.1 TT.StartDeviceMotionListening

**说明**: 开始监听设备方向（姿态）变化。返回设备在三维空间中的旋转角度（欧拉角），适用于指南针、水平仪、AR 方向感知等场景。与陀螺仪不同，此处返回的是绝对方向角而非角速度。

**语法**:

```csharp
public static void StartDeviceMotionListening(string interval = "game")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| interval | string | 否 | "game" | 采样间隔。`"game"` = 20ms，`"ui"` = 60ms，`"normal"` = 200ms |

---

### 6.2 TT.StopDeviceMotionListening

**说明**: 停止监听设备方向变化。

**语法**:

```csharp
public static void StopDeviceMotionListening()
```

---

### 6.3 TT.OnDeviceMotionChange / TT.OffDeviceMotionChange

**说明**: 注册/注销设备方向变化回调。返回 alpha、beta、gamma 三个方向角。

**语法**:

```csharp
public static void OnDeviceMotionChange(Action<float, float, float> callback)
public static void OffDeviceMotionChange(Action<float, float, float> callback)
```

**回调参数说明**:

| 参数 | 类型 | 说明 |
|------|------|------|
| alpha | float | 绕 Z 轴旋转角度，范围 [0, 360]，0° 表示正北方向 |
| beta | float | 绕 X 轴旋转角度，范围 [-180, 180]，设备前后倾斜 |
| gamma | float | 绕 Y 轴旋转角度，范围 [-90, 90]，设备左右倾斜 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class DeviceOrientationController : MonoBehaviour
{
    private Action<float, float, float> m_MotionCallback;

    void OnEnable()
    {
        m_MotionCallback = OnDeviceMotionChanged;
        TT.OnDeviceMotionChange(m_MotionCallback);
        TT.StartDeviceMotionListening("game");
    }

    void OnDisable()
    {
        TT.StopDeviceMotionListening();
        TT.OffDeviceMotionChange(m_MotionCallback);
    }

    private void OnDeviceMotionChanged(float alpha, float beta, float gamma)
    {
        // alpha: 指南针方向（0=正北, 90=正东, 180=正南, 270=正西）
        // beta: 前后倾斜（0=直立, 90=水平朝下, -90=水平朝上）
        // gamma: 左右倾斜（0=水平, 正值=左侧抬起, 负值=右侧抬起）

        Debug.Log($"方向: alpha={alpha:F1}°, beta={beta:F1}°, gamma={gamma:F1}°");

        // 示例: 水平仪检测（设备是否水平放置）
        bool isHorizontal = Mathf.Abs(beta) < 5f && Mathf.Abs(gamma) < 5f;
        if (isHorizontal)
        {
            Debug.Log("设备处于水平状态");
        }
    }
}
```

---

## 七、键盘事件（PC 端）

### 7.1 TT.OnKeyDown / TT.OffKeyDown

**说明**: 注册/注销键盘按下事件监听。仅在 PC 端（Windows/Mac）有效，用于实现 PC 端游戏的键盘操作控制。

**语法**:

```csharp
public static void OnKeyDown(Action<KeyEvent> callback)
public static void OffKeyDown(Action<KeyEvent> callback)
```

**回调参数说明** (KeyEvent):

| 参数 | 类型 | 说明 |
|------|------|------|
| key | string | 按键值，如 `"a"`、`"Enter"`、`"ArrowLeft"` |
| code | string | 物理键位码，如 `"KeyA"`、`"Enter"`、`"ArrowLeft"` |
| keyCode | int | 按键码，如 `65`（A 键） |
| ctrlKey | bool | Ctrl 键是否按下 |
| altKey | bool | Alt 键是否按下 |
| shiftKey | bool | Shift 键是否按下 |
| metaKey | bool | Meta 键是否按下（Mac 为 Command，Windows 为 Win） |
| repeat | bool | 是否为长按产生的重复事件 |

---

### 7.2 TT.OnKeyUp / TT.OffKeyUp

**说明**: 注册/注销键盘释放事件监听。

**语法**:

```csharp
public static void OnKeyUp(Action<KeyEvent> callback)
public static void OffKeyUp(Action<KeyEvent> callback)
```

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class PCKeyboardInput : MonoBehaviour
{
    private Action<KeyEvent> m_KeyDownHandler;
    private Action<KeyEvent> m_KeyUpHandler;
    private HashSet<string> m_PressedKeys = new HashSet<string>();

    void OnEnable()
    {
        // 仅在非真机环境（PC 开发调试）注册
        if (!TT.InContainerEnv)
        {
            m_KeyDownHandler = OnKeyDown;
            m_KeyUpHandler = OnKeyUp;
            TT.OnKeyDown(m_KeyDownHandler);
            TT.OnKeyUp(m_KeyUpHandler);
        }
    }

    void OnDisable()
    {
        if (!TT.InContainerEnv)
        {
            TT.OffKeyDown(m_KeyDownHandler);
            TT.OffKeyUp(m_KeyUpHandler);
        }
    }

    private void OnKeyDown(KeyEvent e)
    {
        m_PressedKeys.Add(e.key);

        // 组合键判断: Ctrl+S 保存
        if (e.ctrlKey && e.key == "s")
        {
            Debug.Log("Ctrl+S: 保存游戏");
            SaveGame();
            return;
        }

        // 常规按键
        switch (e.key)
        {
            case "ArrowUp":
            case "w":
                MovePlayer(Vector3.forward);
                break;
            case "ArrowDown":
            case "s":
                MovePlayer(Vector3.back);
                break;
            case "ArrowLeft":
            case "a":
                MovePlayer(Vector3.left);
                break;
            case "ArrowRight":
            case "d":
                MovePlayer(Vector3.right);
                break;
            case " ":
                PlayerJump();
                break;
        }
    }

    private void OnKeyUp(KeyEvent e)
    {
        m_PressedKeys.Remove(e.key);
    }

    private void MovePlayer(Vector3 direction) { /* 移动逻辑 */ }
    private void PlayerJump() { /* 跳跃逻辑 */ }
    private void SaveGame() { /* 保存逻辑 */ }
}
```

---

## 八、鼠标事件（PC 端）

### 8.1 TT.OnMouseDown / TT.OffMouseDown

**说明**: 注册/注销鼠标按下事件监听。仅在 PC 端有效。

**语法**:

```csharp
public static void OnMouseDown(Action<MouseEvent> callback)
public static void OffMouseDown(Action<MouseEvent> callback)
```

---

### 8.2 TT.OnMouseUp / TT.OffMouseUp

**说明**: 注册/注销鼠标释放事件监听。仅在 PC 端有效。

**语法**:

```csharp
public static void OnMouseUp(Action<MouseEvent> callback)
public static void OffMouseUp(Action<MouseEvent> callback)
```

---

### 8.3 TT.OnMouseMove / TT.OffMouseMove

**说明**: 注册/注销鼠标移动事件监听。仅在 PC 端有效。

**语法**:

```csharp
public static void OnMouseMove(Action<MouseEvent> callback)
public static void OffMouseMove(Action<MouseEvent> callback)
```

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class PCMouseInput : MonoBehaviour
{
    private Action<MouseEvent> m_MouseDownHandler;
    private Action<MouseEvent> m_MouseUpHandler;
    private Action<MouseEvent> m_MouseMoveHandler;

    void OnEnable()
    {
        if (!TT.InContainerEnv)
        {
            m_MouseDownHandler = OnMouseDown;
            m_MouseUpHandler = OnMouseUp;
            m_MouseMoveHandler = OnMouseMove;

            TT.OnMouseDown(m_MouseDownHandler);
            TT.OnMouseUp(m_MouseUpHandler);
            TT.OnMouseMove(m_MouseMoveHandler);
        }
    }

    void OnDisable()
    {
        if (!TT.InContainerEnv)
        {
            TT.OffMouseDown(m_MouseDownHandler);
            TT.OffMouseUp(m_MouseUpHandler);
            TT.OffMouseMove(m_MouseMoveHandler);
        }
    }

    private void OnMouseDown(MouseEvent e)
    {
        Debug.Log($"鼠标按下: button={e.button}, pos=({e.x}, {e.y})");
        // 将鼠标坐标映射到游戏世界
        HandleMouseClick(new Vector2(e.x, e.y));
    }

    private void OnMouseUp(MouseEvent e)
    {
        Debug.Log($"鼠标释放: button={e.button}");
    }

    private void OnMouseMove(MouseEvent e)
    {
        // 鼠标移动时的持续处理，如拖动视角
        HandleMouseDrag(new Vector2(e.x, e.y));
    }

    private void HandleMouseClick(Vector2 screenPos) { /* 点击逻辑 */ }
    private void HandleMouseDrag(Vector2 screenPos) { /* 拖动逻辑 */ }
}
```

---

## 九、滚轮事件（PC 端）

### 9.1 TT.OnWheel / TT.OffWheel

**说明**: 注册/注销鼠标滚轮事件监听。用于 PC 端的缩放、滚动列表等操作。水平滚动（deltaX）通常由触控板横向滑动触发。

**语法**:

```csharp
public static void OnWheel(Action<float, float> callback)
public static void OffWheel(Action<float, float> callback)
```

**回调参数说明**:

| 参数 | 类型 | 说明 |
|------|------|------|
| deltaX | float | 水平滚动量，正值表示向右滚动 |
| deltaY | float | 垂直滚动量，正值表示向下滚动 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class PCWheelInput : MonoBehaviour
{
    public Camera m_Camera;
    public float m_ZoomSpeed = 2.0f;
    private Action<float, float> m_WheelHandler;

    void OnEnable()
    {
        if (!TT.InContainerEnv)
        {
            m_WheelHandler = OnWheel;
            TT.OnWheel(m_WheelHandler);
        }
    }

    void OnDisable()
    {
        if (!TT.InContainerEnv)
        {
            TT.OffWheel(m_WheelHandler);
        }
    }

    private void OnWheel(float deltaX, float deltaY)
    {
        Debug.Log($"滚轮: deltaX={deltaX}, deltaY={deltaY}");

        // 相机缩放
        if (m_Camera != null)
        {
            float zoomAmount = deltaY * m_ZoomSpeed;
            m_Camera.fieldOfView = Mathf.Clamp(
                m_Camera.fieldOfView - zoomAmount,
                20f, 120f
            );
        }
    }
}
```

---

## 十、网络状态

### 10.1 TT.GetNetWorkType

**说明**: 获取当前设备的网络连接类型。异步操作，通过回调返回网络类型字符串。游戏可根据网络类型动态调整画质、预加载策略和延迟容忍度。

**语法**:

```csharp
public static void GetNetWorkType(Action<string> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<string\> | 是 | - | 回调函数，参数为网络类型字符串 |

**返回值说明** (回调参数):

| 返回值 | 说明 | 建议策略 |
|--------|------|----------|
| `"wifi"` | Wi-Fi 网络 | 高清画质，正常预加载 |
| `"5g"` | 5G 移动网络 | 高清画质，正常预加载 |
| `"4g"` | 4G 移动网络 | 中画质，适度预加载 |
| `"3g"` | 3G 移动网络 | 低画质，减少预加载 |
| `"2g"` | 2G 移动网络 | 最低画质，按需加载 |
| `"unknown"` | 未知网络类型 | 保守策略 |
| `"none"` | 无网络连接 | 离线模式 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class NetworkQualityManager : MonoBehaviour
{
    private string m_CurrentNetworkType = "unknown";

    void Start()
    {
        CheckNetworkStatus();
    }

    /// <summary>
    /// 检查网络状态并调整游戏品质
    /// </summary>
    public void CheckNetworkStatus()
    {
        TT.GetNetWorkType((networkType) =>
        {
            m_CurrentNetworkType = networkType;
            Debug.Log($"当前网络类型: {networkType}");

            switch (networkType)
            {
                case "wifi":
                case "5g":
                    SetQualityLevel(QualityLevel.High);
                    break;
                case "4g":
                    SetQualityLevel(QualityLevel.Medium);
                    break;
                case "3g":
                case "2g":
                    SetQualityLevel(QualityLevel.Low);
                    break;
                case "none":
                    Debug.LogWarning("无网络连接，切换到离线模式");
                    EnterOfflineMode();
                    break;
                default:
                    SetQualityLevel(QualityLevel.Medium);
                    break;
            }
        });
    }

    private enum QualityLevel { High, Medium, Low }

    private void SetQualityLevel(QualityLevel level)
    {
        switch (level)
        {
            case QualityLevel.High:
                QualitySettings.SetQualityLevel(2);
                Application.targetFrameRate = 60;
                break;
            case QualityLevel.Medium:
                QualitySettings.SetQualityLevel(1);
                Application.targetFrameRate = 30;
                break;
            case QualityLevel.Low:
                QualitySettings.SetQualityLevel(0);
                Application.targetFrameRate = 30;
                // 进一步降低纹理、阴影等
                break;
        }
    }

    private void EnterOfflineMode()
    {
        // 加载离线缓存数据，禁用网络相关功能
    }
}
```

---

## 十一、设备能力最佳实践

### 11.1 传感器生命周期管理

传感器（加速度计、陀螺仪、设备方向）应在 `OnEnable` 中注册、`OnDisable` 中注销，避免场景切换时内存泄漏和后台持续耗电。

```csharp
public class SensorManager : MonoBehaviour
{
    private Action<float, float, float> m_AccelHandler;
    private Action<float, float, float> m_GyroHandler;
    private Action<float, float, float> m_MotionHandler;

    void OnEnable()
    {
        m_AccelHandler = OnAccel;
        m_GyroHandler = OnGyro;
        m_MotionHandler = OnMotion;

        TT.OnAccelerometerChange(m_AccelHandler);
        TT.OnGyroscopeChange(m_GyroHandler);
        TT.OnDeviceMotionChange(m_MotionHandler);

        TT.StartAccelerometer("game");
        TT.StartGyroscope("game");
        TT.StartDeviceMotionListening("game");
    }

    void OnDisable()
    {
        TT.StopAccelerometer();
        TT.StopGyroscope();
        TT.StopDeviceMotionListening();

        TT.OffAccelerometerChange(m_AccelHandler);
        TT.OffGyroscopeChange(m_GyroHandler);
        TT.OffDeviceMotionChange(m_MotionHandler);
    }

    private void OnAccel(float x, float y, float z) { }
    private void OnGyro(float x, float y, float z) { }
    private void OnMotion(float a, float b, float g) { }
}
```

### 11.2 采样间隔选择

| 场景 | 推荐 interval | 说明 |
|------|--------------|------|
| 赛车/动作游戏（倾斜操控） | `"game"` (20ms) | 需要高灵敏度实时响应 |
| 平衡球/AR 场景 | `"game"` (20ms) | 需要高精度旋转数据 |
| 摇一摇检测 | `"normal"` (200ms) | 低频检测即可，节省电量 |
| UI 界面中的传感器展示 | `"ui"` (60ms) | 折中方案 |

### 11.3 PC 端事件与 Editor 调试

键盘、鼠标、滚轮事件仅在 PC 端有效。在 `TT.InContainerEnv == false`（Unity Editor 环境）下直接注册即可用于开发调试，真机运行时会自动忽略。

```csharp
// Editor 调试用的键盘控制
#if UNITY_EDITOR
void Start()
{
    TT.OnKeyDown(HandleEditorKey);
    TT.OnMouseMove(HandleEditorMouse);
}
#endif
```

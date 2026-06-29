# 广告

> 基于官方文档: 广告 API - 激励视频、Banner、插屏广告
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **奖励发放**：广告 `OnClose` 回调中的奖励发放应使用服务端验证的反作弊机制，避免客户端伪造观看完成状态
> - **广告事件日志**：广告加载/展示/错误事件本身不含用户敏感数据，但建议统一用条件编译管理 Debug 日志输出

广告模块提供三种广告形式：激励视频广告（RewardedVideoAd）、Banner 广告（BannerAd）、插屏广告（InterstitialAd）。所有广告组件均通过 `TT.*` 静态工厂方法创建，返回对应的广告实例对象，通过实例的事件委托和实例方法进行操作。

## 一、激励视频广告

激励视频广告是用户观看完整视频后获得游戏内奖励的全屏广告形式。**仅支持单实例**，创建一次后 `Load()` / `Show()` 复用即可，切换广告位需先 `Destroy()` 旧实例再重新创建。

### 1.1 TT.CreateRewardedVideoAd

**说明**：创建激励视频广告实例。返回 `TTRewardedVideoAd` 对象，通过该对象的事件和方法控制广告生命周期。

**语法**：

```csharp
public static TTRewardedVideoAd CreateRewardedVideoAd(CreateRewardedVideoAdParam param)
```

**CreateRewardedVideoAdParam 参数类**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| AdUnitId | string | 是 | - | 广告位 ID，从抖音开放平台-流量主-广告管理获取 |
| Multiton | bool | 否 | false | 是否开启"再得"模式，允许用户多次观看获取额外奖励 |
| MultitonRewardMsg | List\<string\> | 否 | null | 再得奖励文案数组，每条 ≤7 字符，如 `new List<string>{"再得1次", "再得2次"}` |
| MultitonRewardTimes | int | 否 | 0 | 额外观看次数，取值范围 1-4 |
| ProgressTip | bool | 否 | false | 是否开启进度提醒，倒计时即将结束时提示用户 |

**返回值**：`TTRewardedVideoAd` 实例。

### 1.2 TTRewardedVideoAd 实例方法

| 方法 | 说明 |
|------|------|
| `void Load()` | 预加载广告素材。提前调用可减少用户等待时间 |
| `void Show()` | 展示广告。若未加载完成会先触发加载再展示 |
| `void Destroy()` | 销毁广告实例，释放资源。切换广告位前必须调用 |

### 1.3 TTRewardedVideoAd 事件

| 事件 | 委托类型 | 说明 |
|------|---------|------|
| OnLoad | `Action` | 广告素材加载完成回调 |
| OnError | `Action<int, string>` | 广告加载或展示出错回调。参数：`code` 错误码，`message` 错误信息 |
| OnClose | `Action<bool, int>` | 广告关闭回调。参数：`isEnded` 是否完整观看（true 时发放奖励），`count` 再得模式下当前已观看次数 |

### 1.4 完整代码示例

```csharp
using UnityEngine;

public class RewardedAdManager : MonoBehaviour
{
    private TTRewardedVideoAd _rewardedVideoAd;
    private bool _isAdLoaded = false;

    void Start()
    {
        CreateAd();
    }

    /// <summary>
    /// 创建激励视频广告实例
    /// </summary>
    void CreateAd()
    {
        var param = new CreateRewardedVideoAdParam
        {
            AdUnitId = "your_ad_unit_id_here",
            Multiton = false,
            ProgressTip = true
        };

        _rewardedVideoAd = TT.CreateRewardedVideoAd(param);

        // 订阅事件
        _rewardedVideoAd.OnLoad += OnAdLoaded;
        _rewardedVideoAd.OnError += OnAdError;
        _rewardedVideoAd.OnClose += OnAdClosed;

        // 预加载广告
        _rewardedVideoAd.Load();
    }

    /// <summary>
    /// 广告加载完成
    /// </summary>
    void OnAdLoaded()
    {
        _isAdLoaded = true;
        Debug.Log("激励视频广告加载完成");
    }

    /// <summary>
    /// 广告错误回调
    /// </summary>
    void OnAdError(int code, string message)
    {
        _isAdLoaded = false;
        Debug.LogError($"广告错误: code={code}, message={message}");

        // 常见错误码：
        // 1000: 广告位 ID 错误
        // 1001: 广告请求失败/无广告填充
        // 1002: 广告加载中
        // 1003: 广告已展示过
        // 1004: 广告位 ID 为空
    }

    /// <summary>
    /// 广告关闭回调 —— ⚠️ 安全：严禁在此直接发放奖励
    /// </summary>
    /// <remarks>
    /// ⚠️ 【安全强制】：客户端的 `isEnded` 信号可被伪造/重放。
    /// 正确做法：OnClose 中仅记录广告事件并发送到服务端，
    /// 由服务端验证广告回调签名后再下发奖励。
    /// 以下示例展示安全模式 —— 客户端标记"待验证"，服务端验证后推送奖励。
    /// </remarks>
    void OnAdClosed(bool isEnded, int count)
    {
        if (isEnded)
        {
            // ⚠️ 安全：客户端仅标记"待验证"，不直接发放奖励
            // 将广告完成事件上报服务端，由服务端验证后下发奖励
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"用户观看完成，第{count + 1}次观看，上报服务端验证");
            #endif
            RequestServerVerifyReward(count);
        }
        else
        {
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log("用户提前关闭广告，不发放奖励");
            #endif
        }

        // 关闭后重新加载，为下次展示做准备
        _rewardedVideoAd.Load();
    }

    /// <summary>
    /// 外部调用：展示广告
    /// </summary>
    public void ShowAd()
    {
        if (_rewardedVideoAd != null)
        {
            _rewardedVideoAd.Show();
        }
    }

    /// <summary>
    /// ⚠️ 安全：请求服务端验证广告完成事件并发放奖励
    /// </summary>
    /// <remarks>
    /// 客户端绝不可根据 isEnded 直接发放奖励。
    /// 正确流程：1) 上报广告事件到服务端 → 2) 服务端验证广告回调签名
    /// → 3) 服务端通过长连接/轮询通知客户端发放奖励。
    /// 支付模块已展示完整服务端验签模式，广告模块同理。
    /// </remarks>
    void RequestServerVerifyReward(int count)
    {
        // 将广告完成事件上报到服务端
        // 服务端验证后通过长连接或轮询下发奖励指令
        // 参考 unity-payment.md 中的服务端验签模式
        StartCoroutine(ServerVerifyAdRewardCoroutine(count));
    }

    private System.Collections.IEnumerator ServerVerifyAdRewardCoroutine(int count)
    {
        // 发送广告验证请求到服务端
        // POST /api/ad/verify { adUnitId, userId, watchCount, timestamp, signature }
        // 轮询等待服务端验证结果
        // 验证通过后服务端推送奖励 → 客户端执行 GrantReward()
        yield return null;
    }

    /// <summary>
    /// 发放奖励（仅由服务端验证通过后调用）
    /// </summary>
    void GrantReward()
    {
        // ⚠️ 安全：此方法仅在服务端验证通过后才被调用
        // 示例：增加金币、复活次数等
        // GameManager.Instance.AddCoin(100);
    }

    void OnDestroy()
    {
        // 取消订阅，释放广告实例
        if (_rewardedVideoAd != null)
        {
            _rewardedVideoAd.OnLoad -= OnAdLoaded;
            _rewardedVideoAd.OnError -= OnAdError;
            _rewardedVideoAd.OnClose -= OnAdClosed;
            _rewardedVideoAd.Destroy();
            _rewardedVideoAd = null;
        }
    }
}
```

### 1.5 再得模式（Multiton）

再得模式允许用户在观看完第一次激励视频后，继续观看额外次数以获取递增奖励。

**配置方式**：

```csharp
var param = new CreateRewardedVideoAdParam
{
    AdUnitId = "your_ad_unit_id",
    Multiton = true,
    MultitonRewardTimes = 3,  // 额外可观看 3 次，总计 4 次
    MultitonRewardMsg = new List<string>
    {
        "再得100金币",
        "再得200金币",
        "再得500金币"
    }
};

var videoAd = TT.CreateRewardedVideoAd(param);
// ⚠️ 安全：多样本模式下同样需要服务端验证，不可根据客户端 isEnded 直接发奖
videoAd.OnClose += (isEnded, count) =>
{
    if (isEnded)
    {
        // count 从 0 开始：0=首次，1=第1次再得，2=第2次再得...
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"第{count + 1}次观看完成，上报服务端验证");
        #endif
        // ⚠️ 安全：上报服务端验证，不可直接发放奖励
        RequestServerVerifyMultitonReward(count);
    }
};
```

## 二、Banner 广告

Banner 广告是悬浮在游戏画面顶部或底部的横幅广告，不影响游戏操作。

### 2.1 TT.CreateBannerAd

**说明**：创建 Banner 广告实例。Banner 广告创建后需调用 `Show()` 才会展示。

**语法**：

```csharp
public static TTBannerAd CreateBannerAd(CreateBannerAdParam param)
```

**CreateBannerAdParam 参数类**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| AdUnitId | string | 是 | - | Banner 广告位 ID |
| AdIntervals | int | 否 | 30 | 广告自动刷新间隔（秒），最小值 30 |
| Style | BannerAdStyle | 否 | null | 广告样式配置，含位置和尺寸 |

**BannerAdStyle 参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| Left | int | 否 | 0 | 广告左边距（px） |
| Top | int | 否 | 0 | 广告上边距（px） |
| Width | int | 否 | 300 | 广告宽度（px），按比例自动计算高度 |

### 2.2 TTBannerAd 实例方法

| 方法 | 说明 |
|------|------|
| `void Show()` | 展示 Banner 广告 |
| `void Hide()` | 隐藏 Banner 广告（不销毁，可再次 Show） |
| `void Destroy()` | 销毁 Banner 广告实例，释放资源 |

### 2.3 TTBannerAd 事件

| 事件 | 委托类型 | 说明 |
|------|---------|------|
| OnLoad | `Action` | Banner 广告加载完成 |
| OnError | `Action<int, string>` | Banner 广告加载错误。参数：`code` 错误码，`message` 错误信息 |
| OnResize | `Action<float, float>` | Banner 广告尺寸变化。参数：`width` 宽度，`height` 高度 |

### 2.4 代码示例

```csharp
using UnityEngine;

public class BannerAdManager : MonoBehaviour
{
    private TTBannerAd _bannerAd;

    void Start()
    {
        CreateBannerAd();
    }

    void CreateBannerAd()
    {
        var param = new CreateBannerAdParam
        {
            AdUnitId = "your_banner_ad_unit_id",
            AdIntervals = 30,
            Style = new BannerAdStyle
            {
                Left = 0,
                Top = 0,
                Width = 300
            }
        };

        _bannerAd = TT.CreateBannerAd(param);

        _bannerAd.OnLoad += () =>
        {
            Debug.Log("Banner 广告加载完成");
            _bannerAd.Show();
        };

        _bannerAd.OnError += (code, message) =>
        {
            Debug.LogError($"Banner 广告错误: code={code}, message={message}");
        };

        _bannerAd.OnResize += (width, height) =>
        {
            Debug.Log($"Banner 尺寸变化: {width}x{height}");
        };
    }

    public void ShowBanner()
    {
        _bannerAd?.Show();
    }

    public void HideBanner()
    {
        _bannerAd?.Hide();
    }

    void OnDestroy()
    {
        if (_bannerAd != null)
        {
            _bannerAd.Destroy();
            _bannerAd = null;
        }
    }
}
```

## 三、插屏广告

插屏广告是在游戏场景切换、关卡结束等自然中断节点展示的全屏弹窗广告。

### 3.1 TT.CreateInterstitialAd

**说明**：创建插屏广告实例。建议提前创建并预加载，在合适的时机调用 `Show()` 展示。

**语法**：

```csharp
public static TTInterstitialAd CreateInterstitialAd(CreateInterstitialAdParam param)
```

**CreateInterstitialAdParam 参数类**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| AdUnitId | string | 是 | - | 插屏广告位 ID |

### 3.2 TTInterstitialAd 实例方法

| 方法 | 说明 |
|------|------|
| `void Load()` | 预加载广告素材 |
| `void Show()` | 展示插屏广告 |
| `void Destroy()` | 销毁插屏广告实例，释放资源 |

### 3.3 TTInterstitialAd 事件

| 事件 | 委托类型 | 说明 |
|------|---------|------|
| OnLoad | `Action` | 插屏广告加载完成 |
| OnError | `Action<int, string>` | 插屏广告加载或展示错误。参数：`code` 错误码，`message` 错误信息 |
| OnClose | `Action` | 插屏广告关闭回调，此时可恢复游戏逻辑 |

### 3.4 代码示例

```csharp
using UnityEngine;

public class InterstitialAdManager : MonoBehaviour
{
    private TTInterstitialAd _interstitialAd;
    private bool _isAdShowing = false;

    void Start()
    {
        CreateInterstitialAd();
    }

    void CreateInterstitialAd()
    {
        var param = new CreateInterstitialAdParam
        {
            AdUnitId = "your_interstitial_ad_unit_id"
        };

        _interstitialAd = TT.CreateInterstitialAd(param);

        _interstitialAd.OnLoad += () =>
        {
            Debug.Log("插屏广告加载完成");
        };

        _interstitialAd.OnError += (code, message) =>
        {
            _isAdShowing = false;
            Debug.LogError($"插屏广告错误: code={code}, message={message}");
            // 加载失败时直接恢复游戏
            ResumeGame();
        };

        _interstitialAd.OnClose += () =>
        {
            _isAdShowing = false;
            Debug.Log("插屏广告关闭");
            // 广告关闭后恢复游戏逻辑
            ResumeGame();
        };

        // 预加载
        _interstitialAd.Load();
    }

    /// <summary>
    /// 在合适的场景节点调用：关卡结束、场景切换前等
    /// </summary>
    public void ShowInterstitialAd()
    {
        if (_interstitialAd != null && !_isAdShowing)
        {
            _isAdShowing = true;
            PauseGame();  // 暂停游戏逻辑
            _interstitialAd.Show();
        }
    }

    void PauseGame()
    {
        Time.timeScale = 0f;
        // 暂停音频、计时器等
    }

    void ResumeGame()
    {
        Time.timeScale = 1f;
        // 恢复音频、计时器等
        // 预加载下一次广告
        _interstitialAd?.Load();
    }

    void OnDestroy()
    {
        if (_interstitialAd != null)
        {
            _interstitialAd.Destroy();
            _interstitialAd = null;
        }
    }
}
```

## 四、广告最佳实践

1. **广告位 ID 管理**：不同广告位使用不同的 AdUnitId，不要混用。测试阶段使用测试广告位 ID，上线前替换为正式 ID。

2. **预加载策略**：激励视频和插屏广告应在游戏启动或上一轮广告关闭后立即调用 `Load()` 预加载，避免用户点击展示时等待加载。

3. **环境判断**：Editor 环境下广告 API 可能不可用，使用 `TT.InContainerEnv` 判断真机环境后再创建广告实例。

```csharp
if (TT.InContainerEnv)
{
    CreateAd();
}
```

4. **实例生命周期**：每个广告实例只创建一次，通过 `Load()`/`Show()` 复用。场景销毁时务必调用 `Destroy()` 释放资源，并取消所有事件订阅（`-=`）。

5. **错误处理**：务必处理 `OnError` 回调，错误码常见值：
   - `1000`：广告位 ID 错误或未配置
   - `1001`：广告请求失败或无广告填充
   - `1002`：广告正在加载中
   - `1003`：广告已展示过（激励视频单实例限制）
   - `1004`：广告位 ID 为空

6. **奖励安全发放**：激励视频必须在 `OnClose` 中判断 `isEnded == true` 才发放奖励，防止用户提前关闭仍获得奖励。奖励逻辑应做服务端校验，避免客户端篡改。

7. **游戏暂停与恢复**：插屏广告和激励视频展示期间应暂停游戏逻辑（`Time.timeScale = 0`），广告关闭后恢复。展示前保存游戏状态，防止意外中断导致进度丢失。

8. **Banner 位置适配**：Banner 广告应根据设备屏幕尺寸和安全区域动态计算 `Left`/`Top`，避免遮挡游戏核心 UI 元素或进入刘海屏区域。

9. **再得模式谨慎使用**：Multiton 奖励文案需简洁明了（≤7 字符），避免用户误解。每次再得的奖励应有梯度递增，给用户持续观看的动力。

10. **避免频繁调用**：不要在同一帧内连续调用 `Load()` 或 `Show()`，间隔至少 1 秒。`Destroy()` 后如需重新创建，等待至少一个渲染帧。

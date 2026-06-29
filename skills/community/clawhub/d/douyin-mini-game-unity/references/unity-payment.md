# 支付

> 基于官方文档: 支付 API - 钻石支付、游戏币支付、道具直购、游戏金币(Lite)
> 生成时间: 2026-06-24

> ⚠️ **【安全警告 — 支付验签】**：本文件所有支付示例代码仅演示 API 调用方式。**客户端的 `Success` 回调仅表示收银台操作完成，不代表资金已到账**。在生产环境中：
> - **严禁**在客户端回调中直接发放道具、金币或钻石
> - **必须**等待服务端 `payment_callback` 接口收到支付通知并验证签名
> - 奖励发放由**服务端验证通过后**下发指令，客户端仅做展示刷新
> - 对于有延迟到账的场景（游戏币），建议实现**服务端驱动的余额同步**而非客户端轮询推测
>
> 服务端支付回调文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/game-payment/payment-callback

## 一、钻石支付（客服支付）

### 1.1 TT.OpenAwemeCustomerService

**说明**: 通过抖音号客服页面拉起钻石支付。用户在客服页面中选择支付金额完成钻石购买。适用于 PC 端支付场景，移动端也可使用。

**语法**:

```csharp
public static void OpenAwemeCustomerService(OpenAwemeCustomerServiceParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | OpenAwemeCustomerServiceParam | 是 | - | 支付参数对象 |

---

### 1.2 OpenAwemeCustomerServiceParam 参数类

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| BuyQuantity | int | 是 | - | 购买数量（钻石数量） |
| CustomId | string | 是 | - | 开发者自定义唯一订单号，用于服务端回调关联 |
| CurrencyType | string | 否 | "DIAMOND" | 货币类型，当前仅支持 "DIAMOND" |
| ZoneId | string | 否 | "1" | 游戏服务区 ID |
| ExtraInfo | string | 否 | "" | 额外透传信息（长度不超过 256 字符） |
| GoodType | int | 否 | 0 | 商品类型：0=默认 |
| OrderAmount | int | 否 | - | 订单金额（单位：分）。不填则使用 BuyQuantity 计算 |
| GoodName | string | 否 | - | 商品名称（长度不超过 10 字符） |
| GoodsId | string | 否 | - | 商品 ID |
| Success | Action | 否 | null | 支付成功回调 |
| Fail | Action\<ErrorInfo\> | 否 | null | 支付失败回调 |
| Complete | Action | 否 | null | 支付流程完成回调（成功/失败均触发） |

**代码示例**:

```csharp
// ⚠️ 安全警告：Success 回调仅表示收银台操作完成，不代表资金到账
// 正确做法：等待服务端 payment_callback 验证签名后下发钻石
var param = new OpenAwemeCustomerServiceParam
{
    BuyQuantity = 60,                       // 购买 60 钻石
    CustomId = System.Guid.NewGuid().ToString(), // 唯一订单号
    CurrencyType = "DIAMOND",
    ZoneId = "1",
    ExtraInfo = "{\"userId\":\"12345\",\"level\":10}",
    GoodType = 0,
    GoodName = "60钻石包",
    GoodsId = "diamond_pack_60",
    Success = () =>
    {
        // ⚠️ 此处仅记录收银台操作完成，不可直接发放钻石
        // 钻石余额更新应由服务端支付回调驱动
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("钻石支付收银台操作完成，等待服务端回调确认");
        #endif
    },
    Fail = (error) =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"钻石支付失败: errCode={error.ErrorCode}, errMsg={error.ErrMsg}");
        #endif
        // 根据错误码处理不同失败场景
    },
    Complete = () =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("钻石支付流程结束");
        #endif
    }
};

TT.OpenAwemeCustomerService(param);
```

---

## 二、游戏币支付与道具直购

### 2.1 TT.RequestGamePayment

**说明**: 发起游戏币支付或道具直购支付。游戏币模式适用于购买虚拟货币（如金币），道具直购模式适用于直接购买特定道具。

**语法**:

```csharp
public static void RequestGamePayment(RequestGamePaymentParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | RequestGamePaymentParam | 是 | - | 支付参数对象 |

---

### 2.2 RequestGamePaymentParam 参数类

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| Mode | string | 是 | "game" | 支付类型，当前固定为 "game" |
| Env | int | 否 | 0 | 环境：0=正式环境，1=沙盒测试环境 |
| CurrencyType | string | 否 | "CNY" | 币种，当前仅支持 "CNY" |
| Platform | string | 否 | "android" | 平台标识：android / windows / iOS |
| BuyQuantity | int | 是(游戏币) | - | 购买数量。游戏币模式：金币数量乘以单价必须等于限定价格等级之一 |
| CustomId | string | 是 | - | 开发者自定义唯一订单号（必填），用于服务端回调关联订单 |
| ZoneId | string | 否 | "1" | 游戏服务区 ID |
| ExtraInfo | string | 否 | "" | 额外透传信息（长度不超过 256 字符），建议 JSON 格式 |
| GoodType | int | 否 | 0 | 商品类型：0=默认/游戏币，1=游戏币，2=道具直购 |
| OrderAmount | int | 是(道具) | - | 道具现金价格（单位：分）。道具直购模式（GoodType=2）时必填 |
| GoodName | string | 是(道具) | - | 道具名称（长度不超过 10 字符）。道具直购模式时必填 |
| GoodsId | string | 否 | - | 商品 ID，用于标识具体商品 |
| Success | Action | 否 | null | 支付成功回调（收银台拉起成功即回调，非最终到账确认） |
| Fail | Action\<ErrorInfo\> | 否 | null | 支付失败回调 |
| Complete | Action | 否 | null | 支付流程完成回调（成功/失败均触发） |

**代码示例：游戏币支付**:

```csharp
// ⚠️ 安全警告：Success 回调仅表示收银台拉起成功，不代表金币到账
// 游戏币到账以服务端 payment_callback 签名为准，切勿客户端自行加币
// 游戏币支付场景
// 购买 600 金币，假设单价为 1分/金币，则总金额为 600分 = 6元（符合限定价格等级）
var gameCoinParam = new RequestGamePaymentParam
{
    Mode = "game",
    Env = 0,
    CurrencyType = "CNY",
    Platform = "android",
    BuyQuantity = 600,
    CustomId = System.Guid.NewGuid().ToString(),
    ZoneId = "1",
    ExtraInfo = "{\"userId\":\"12345\",\"productId\":\"coin_pack_600\"}",
    GoodType = 0,
    GoodName = "600金币",
    GoodsId = "coin_600",
    Success = () =>
    {
        // ⚠️ 此处仅表示收银台拉起成功，不可直接加金币
        // 正确做法：通知服务端记录待确认订单，等待 payment_callback
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("游戏币支付收银台拉起成功，等待服务端回调确认到账");
        #endif
        NotifyServerPendingOrder("coin_600"); // 服务端记录待确认订单
    },
    Fail = (error) =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"游戏币支付失败: {error.ErrorCode} - {error.ErrMsg}");
        #endif
        HandlePaymentFailure(error.ErrorCode);
    },
    Complete = () =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("游戏币支付流程结束");
        #endif
    }
};

TT.RequestGamePayment(gameCoinParam);
```

**代码示例：道具直购**:

```csharp
// ⚠️ 安全警告：Success 回调仅表示收银台拉起成功，不可在此发放道具
// 道具发放必须由服务端 payment_callback 验证签名后执行
// 道具直购场景（GoodType=2）
// orderAmount 单位为分，10 = 0.10 元
var itemParam = new RequestGamePaymentParam
{
    Mode = "game",
    Env = 0,
    CurrencyType = "CNY",
    Platform = "android",
    GoodType = 2,                   // 道具直购模式
    OrderAmount = 10,               // 道具价格 0.10 元
    GoodName = "皮肤礼包",           // 道具名称，不超过10字符
    GoodsId = "skin_pack_001",
    CustomId = System.Guid.NewGuid().ToString(),
    ZoneId = "1",
    ExtraInfo = "{\"userId\":\"12345\",\"skinId\":\"skin_fire_001\"}",
    Success = () =>
    {
        // ⚠️ 此处仅记录收银台操作完成，不可直接发放道具
        // 正确做法：等待服务端 payment_callback 后由服务端下发道具
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("道具直购收银台操作完成，等待服务端回调确认");
        #endif
    },
    Fail = (error) =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"道具购买失败: {error.ErrorCode} - {error.ErrMsg}");
        #endif
    },
    Complete = () =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("道具直购流程结束");
        #endif
    }
};

TT.RequestGamePayment(itemParam);
```

---

## 三、支付错误码

支付回调中的 `ErrorInfo.ErrorCode` 对应以下错误码：

| errCode | 说明 |
|---------|------|
| -1 | 支付失败 / 内部错误 |
| -2 | 用户取消支付 |
| -15001 | 缺少必要参数 |
| -15002 | 请求参数不合法 |
| -15003 | 当前 App 不支持支付能力 |
| -15006 | App 没有支付权限（需在开发者平台设置游戏币汇率） |
| -15009 | 支付内部错误 |
| -15098 | 用户未通过实名认证 |
| -15099 | 累计支付金额超限（受未成年人保护限制） |
| -15101 | customId 为空或不唯一（同一 customId 不可重复使用） |
| -16000 | 用户未登录（需先调用 TT.Login 完成登录） |
| -20002 | 交易存在风险（风控拦截） |
| 2 | 重复支付（同一笔订单已处理） |
| 3 | 拉起收银台失败 |
| 4 | 网络异常 |
| 5 | iOS 平台不支持当前支付方式 |
| 6 | 其他未知错误 |
| 21113 | 未成年人脸验证不通过 |

---

## 四、限定价格等级

游戏币支付的最终金额必须是以下价格之一（`BuyQuantity`乘以单价计算后的结果）：

| 价格（元） |
|-----------|
| 1 |
| 3 |
| 6 |
| 8 |
| 12 |
| 18 |
| 25 |
| 30 |
| 40 |
| 45 |
| 50 |
| 60 |
| 68 |
| 73 |
| 78 |
| 88 |
| 98 |
| 108 |
| 118 |
| 128 |
| 148 |
| 168 |
| 188 |
| 198 |
| 328 |
| 648 |
| 998 |
| 1288 |
| 1998 |
| 2998 |

> **计算方式**: 实际支付金额（元）= `BuyQuantity` * 单价（元/个）。结果必须落在上述价格等级中。例如：单价 0.01 元/金币，购买 600 金币 = 6 元，6 在价格等级表中，合法。

---

## 五、Lite 版游戏金币

### 5.1 TT.RequestGoldOrder

**说明**: Lite 版（极速版）游戏金币支付接口，适用于抖音 Lite 版本中的金币购买场景。

**语法**:

```csharp
public static void RequestGoldOrder(RequestGoldOrderParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | RequestGoldOrderParam | 是 | - | 金币订单参数对象 |

**RequestGoldOrderParam 属性**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| BuyQuantity | int | 是 | - | 购买金币数量 |
| CustomId | string | 是 | - | 开发者自定义唯一订单号 |
| Env | int | 否 | 0 | 环境：0=正式 |
| ExtraInfo | string | 否 | "" | 额外信息 |
| Success | Action | 否 | null | 支付成功回调 |
| Fail | Action\<ErrorInfo\> | 否 | null | 支付失败回调 |
| Complete | Action | 否 | null | 支付完成回调 |

**代码示例**:

```csharp
// ⚠️ 安全警告：与 RequestGamePayment 相同，Success 仅表示收银台操作完成
// 金币余额刷新必须由服务端支付回调驱动
var goldParam = new RequestGoldOrderParam
{
    BuyQuantity = 100,
    CustomId = System.Guid.NewGuid().ToString(),
    Env = 0,
    ExtraInfo = "{\"userId\":\"12345\"}",
    Success = () =>
    {
        // ⚠️ 不可在此刷新余额，等待服务端回调
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("Lite 版金币支付收银台操作完成，等待服务端回调");
        #endif
    },
    Fail = (error) =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"金币支付失败: {error.ErrorCode} - {error.ErrMsg}");
        #endif
    },
    Complete = () =>
    {
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log("金币支付流程结束");
        #endif
    }
};

TT.RequestGoldOrder(goldParam);
```

---

## 六、支付完整流程示例

以下示例展示一个完整的支付流程：登录校验 -> 构建支付参数 -> 调用支付 -> 处理回调 -> 等待服务端回调 -> 风控处理。

> ⚠️ **安全说明**：此示例中支付成功后的余额同步改为**服务端驱动模式**——客户端发起支付后仅记录 `pendingOrderId`，实际金币/道具发放由服务端 `payment_callback` 验证签名后通过推送或轮询接口通知客户端。`PollServerOrderStatus` 方法演示了从服务端查询订单状态的正确模式，替代不安全的客户端本地推测。

```csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class PaymentManager : MonoBehaviour
{
    // 支付商品配置
    [System.Serializable]
    public class PaymentProduct
    {
        public string ProductId;
        public string ProductName;
        public int Price;       // 单位：分
        public int CoinAmount;  // 对应金币数量
        public int GoodType;    // 0=游戏币, 2=道具直购
    }

    public PaymentProduct[] Products;

    // ⚠️ 安全：待确认订单集合，用于服务端回调到达后匹配
    private HashSet<string> pendingOrderIds = new HashSet<string>();

    void Start()
    {
        // 初始化 SDK 后检查登录态
        if (TT.InContainerEnv)
        {
            CheckSessionAndReady();
        }
    }

    /// <summary>
    /// 支付前置：校验登录态
    /// </summary>
    private void CheckSessionAndReady()
    {
        TT.CheckSession(
            success: () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("登录态有效，支付能力就绪");
                #endif
            },
            fail: () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("登录态过期，重新登录");
                #endif
                TT.Login(
                    success: (code, anonymousCode, isLogin) =>
                    {
                        #if UNITY_EDITOR || DEVELOPMENT_BUILD
                        Debug.Log("重新登录成功");
                        #endif
                    },
                    fail: (errMsg) => Debug.LogError($"重新登录失败: {errMsg}")
                );
            }
        );
    }

    /// <summary>
    /// 购买游戏币（安全加固版）
    /// ⚠️ 关键变更：客户端不自行加币，等待服务端 payment_callback 后同步余额
    /// </summary>
    public void PurchaseGameCoin(string productId)
    {
        var product = FindProduct(productId);
        if (product == null)
        {
            Debug.LogError($"商品不存在: {productId}");
            return;
        }

        string orderId = GenerateOrderId();

        // 1. 构建支付参数
        var param = new RequestGamePaymentParam
        {
            Mode = "game",
            Env = 0,
            CurrencyType = "CNY",
            Platform = GetCurrentPlatform(),
            GoodType = product.GoodType,
            BuyQuantity = product.CoinAmount,
            CustomId = orderId,
            ZoneId = GetCurrentZoneId(),
            GoodName = TruncateString(product.ProductName, 10),
            GoodsId = product.ProductId,
            ExtraInfo = BuildExtraInfo(product),

            // 2. 成功回调（收银台拉起成功，不代表到账）
            Success = () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"支付发起成功: {product.ProductName}, orderId={orderId}");
                #endif
                // ⚠️ 安全：记录待确认订单，不自行加币
                pendingOrderIds.Add(orderId);
                // 启动服务端订单状态轮询（正确做法）
                StartCoroutine(PollServerOrderStatus(orderId, product));
            },

            // 3. 失败回调
            Fail = (error) =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"支付失败: [{error.ErrorCode}] {error.ErrMsg}");
                #endif
                HandlePaymentError(error.ErrorCode, product);
            },

            // 4. 完成回调
            Complete = () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("支付流程结束");
                #endif
            }
        };

        // 5. 调用支付
        TT.RequestGamePayment(param);
    }

    /// <summary>
    /// 服务端订单状态轮询（安全模式）
    /// ⚠️ 替代不安全的客户端余额推测，改为从服务端查询订单支付状态
    /// </summary>
    private IEnumerator PollServerOrderStatus(string orderId, PaymentProduct product)
    {
        int maxAttempts = 20;
        float interval = 3f;

        for (int i = 0; i < maxAttempts; i++)
        {
            yield return new WaitForSeconds(interval);

            // 向服务端查询订单状态（服务端已通过 payment_callback 确认支付）
            yield return StartCoroutine(CheckOrderStatusFromServer(orderId, (isPaid, coinBalance) =>
            {
                if (isPaid)
                {
                    #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    Debug.Log($"服务端确认支付成功，当前余额: {coinBalance}");
                    #endif
                    pendingOrderIds.Remove(orderId);
                    UpdateCoinDisplay(coinBalance);
                }
            }));

            if (!pendingOrderIds.Contains(orderId))
            {
                yield break; // 订单已确认，停止轮询
            }

            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"第 {i + 1} 次查询服务端订单状态...");
            #endif
        }

        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.LogWarning("轮询超时，请通过服务端主动推送或客服渠道确认订单状态");
        #endif
    }

    /// <summary>
    /// 向服务端查询订单支付状态
    /// </summary>
    private IEnumerator CheckOrderStatusFromServer(string orderId, System.Action<bool, int> callback)
    {
        using (var request = UnityEngine.Networking.UnityWebRequest.Get(
            $"https://your-server.com/api/payment/order_status?orderId={orderId}"))
        {
            yield return request.SendWebRequest();
            if (request.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                var response = MiniJSON.Json.Deserialize(request.downloadHandler.text) as Dictionary<string, object>;
                bool isPaid = (bool)response["isPaid"];
                int balance = Convert.ToInt32(response["coinBalance"]);
                callback(isPaid, balance);
            }
        }
    }

    /// <summary>
    /// 支付错误处理
    /// </summary>
    private void HandlePaymentError(int errCode, PaymentProduct product)
    {
        switch (errCode)
        {
            case -2:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("用户取消支付，无需处理");
                #endif
                break;

            case -15098:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("用户未通过实名认证，引导实名");
                #endif
                break;

            case -16000:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("用户未登录，重新登录后重试");
                #endif
                TT.Login(
                    success: (code, anonCode, isLogin) => PurchaseGameCoin(product.ProductId),
                    fail: (err) => Debug.LogError("登录失败")
                );
                break;

            case -20002:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("交易被风控拦截，提示用户稍后再试");
                #endif
                ShowRiskWarningDialog();
                break;

            case 21113:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("人脸验证不通过，疑似未成年人");
                #endif
                ShowUnderageWarningDialog();
                break;

            case 2:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("重复支付，忽略");
                #endif
                break;

            default:
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"未知支付错误: {errCode}");
                #endif
                break;
        }
    }

    /// <summary>
    /// 购买道具直购（安全加固版）
    /// ⚠️ 关键变更：不在客户端直接 GrantItemImmediately，等待服务端回调
    /// </summary>
    public void PurchaseItem(string productId)
    {
        var product = FindProduct(productId);
        if (product == null) return;

        string orderId = GenerateOrderId();

        var param = new RequestGamePaymentParam
        {
            Mode = "game",
            Env = 0,
            CurrencyType = "CNY",
            Platform = GetCurrentPlatform(),
            GoodType = 2,
            OrderAmount = product.Price,
            GoodName = TruncateString(product.ProductName, 10),
            GoodsId = product.ProductId,
            CustomId = orderId,
            ZoneId = GetCurrentZoneId(),
            ExtraInfo = BuildExtraInfo(product),
            Success = () =>
            {
                // ⚠️ 安全：记录待确认订单，等待服务端 payment_callback 后下发道具
                pendingOrderIds.Add(orderId);
                StartCoroutine(PollServerOrderStatus(orderId, product));
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"道具直购收银台操作完成: {product.ProductName}, 等待服务端回调");
                #endif
            },
            Fail = (error) =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"道具购买失败: [{error.ErrorCode}] {error.ErrMsg}");
                #endif
                HandlePaymentError(error.ErrorCode, product);
            },
            Complete = () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("道具购买流程结束");
                #endif
            }
        };

        TT.RequestGamePayment(param);
    }

    /// <summary>
    /// 购买钻石（安全加固版）
    /// ⚠️ 关键变更：不在客户端直接 RefreshDiamondBalance，等待服务端回调
    /// </summary>
    public void PurchaseDiamond(int diamondAmount)
    {
        string orderId = GenerateOrderId();

        var param = new OpenAwemeCustomerServiceParam
        {
            BuyQuantity = diamondAmount,
            CustomId = orderId,
            CurrencyType = "DIAMOND",
            ZoneId = GetCurrentZoneId(),
            ExtraInfo = BuildExtraInfo(null),
            GoodType = 0,
            GoodName = $"{diamondAmount}钻石",
            GoodsId = $"diamond_{diamondAmount}",
            Success = () =>
            {
                // ⚠️ 安全：记录待确认订单，等待服务端 callback
                pendingOrderIds.Add(orderId);
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"钻石购买收银台完成: {diamondAmount}, 等待服务端回调");
                #endif
            },
            Fail = (error) =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"钻石购买失败: [{error.ErrorCode}] {error.ErrMsg}");
                #endif
                HandlePaymentError(error.ErrorCode, null);
            },
            Complete = () =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log("钻石支付流程结束");
                #endif
            }
        };

        TT.OpenAwemeCustomerService(param);
    }

    /// <summary>
    /// 服务端回调驱动的余额同步入口
    /// 由服务端推送或客户端定期调用，刷新所有已验证的余额数据
    /// </summary>
    public void SyncBalanceFromServer()
    {
        StartCoroutine(FetchServerBalance());
    }

    private IEnumerator FetchServerBalance()
    {
        using (var request = UnityEngine.Networking.UnityWebRequest.Get(
            "https://your-server.com/api/user/balance"))
        {
            yield return request.SendWebRequest();
            if (request.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                var response = MiniJSON.Json.Deserialize(request.downloadHandler.text) as Dictionary<string, object>;
                int coinBalance = Convert.ToInt32(response["coinBalance"]);
                int diamondBalance = Convert.ToInt32(response["diamondBalance"]);
                UpdateCoinDisplay(coinBalance);
                UpdateDiamondDisplay(diamondBalance);
                // 清除所有已确认的待确认订单
                pendingOrderIds.Clear();
            }
        }
    }

    // ---- 辅助方法 ----

    private PaymentProduct FindProduct(string productId)
    {
        if (Products == null) return null;
        foreach (var p in Products)
        {
            if (p.ProductId == productId) return p;
        }
        return null;
    }

    private string GenerateOrderId()
    {
        return $"ORDER_{System.DateTime.Now.Ticks}_{Random.Range(0, 9999)}";
    }

    private string GetCurrentPlatform()
    {
        #if UNITY_ANDROID
            return "android";
        #elif UNITY_IOS
            return "iOS";
        #elif UNITY_STANDALONE_WIN
            return "windows";
        #else
            return "android";
        #endif
    }

    private string GetCurrentZoneId()
    {
        return PlayerPrefs.GetString("current_zone", "1");
    }

    private string TruncateString(string input, int maxLength)
    {
        if (string.IsNullOrEmpty(input)) return "";
        return input.Length <= maxLength ? input : input.Substring(0, maxLength);
    }

    private string BuildExtraInfo(PaymentProduct product)
    {
        var info = new Dictionary<string, object>
        {
            { "timestamp", System.DateTimeOffset.UtcNow.ToUnixTimeSeconds() },
            { "version", Application.version }
        };
        if (product != null)
        {
            info["productId"] = product.ProductId;
        }
        return MiniJSON.Json.Serialize(info);
    }

    private void UpdateCoinDisplay(int balance) { /* 更新 UI */ }
    private void UpdateDiamondDisplay(int balance) { /* 更新 UI */ }
    private void ShowRiskWarningDialog() { /* 风控提示 */ }
    private void ShowUnderageWarningDialog() { /* 未成年提示 */ }
}
```

---

## 七、支付注意事项

1. **🔒 服务端回调验证（安全强制）**: **以服务端收到的 `payment_callback` 为准判断是否真正支付成功**。客户端 `Success` 回调仅为收银台操作结果，不代表资金已到账。**严禁在客户端回调中直接发放道具/金币/钻石**。服务端必须验证回调签名（`pay_sig` 字段），防止伪造支付通知。签名算法详见官方文档。
2. **登录态校验**: 支付前必须调用 `TT.CheckSession` 确保用户登录态有效。登录态过期需重新 `TT.Login`。
3. **customId 唯一性**: 每次支付请求的 `customId` 必须全局唯一，不可重复使用。建议使用 `GUID + 时间戳` 组合。
4. **extraInfo 透传**: `extraInfo` 长度不超过 256 字符，会在服务端支付回调中返回。建议传入 JSON 格式字符串，包含 userId、产品 ID 等业务信息。注意不要传入敏感数据。
5. **游戏币延迟到账**: 游戏币支付可能存在延迟到账的情况。建议通过服务端回调确认到账，而非客户端本地轮询推测。
6. **PC 端限制**: PC 端仅支持钻石支付（`OpenAwemeCustomerService`），不支持 `RequestGamePayment`。
7. **真机测试**: 真机环境支付为真实扣款，建议使用小额金额（如 1 元）进行测试。沙盒环境（`env=1`）可避免真实扣款。
8. **未成年人保护**: 未实名认证用户无法支付（errCode=-15098），人脸验证不通过可能为未成年人（errCode=21113），累计支付金额超限（errCode=-15099）。
9. **限频与风控**: 频繁发起支付可能触发风控拦截（errCode=-20002），建议添加支付间隔限制。
10. **iOS 适配**: `Platform` 参数需根据实际平台传入，iOS 平台有特殊的支付限制（errCode=5）。
11. **🔒 生产日志脱敏**: 支付相关日志不应打印 `CustomId`、`ExtraInfo` 等订单敏感信息到生产日志中，建议用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 包裹调试输出。

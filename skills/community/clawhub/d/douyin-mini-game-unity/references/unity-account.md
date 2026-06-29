# 账号与授权

> 基于官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/account
> 生成时间: 2026-06-24

> ⚠️ **【安全声明 — 敏感数据保护，已加固】**：
> - `code`（临时登录凭证）、`session_key`、`openid`、`encryptedData`、`iv`、`cloudId` 均为敏感数据
> - 所有含敏感数据的 `Debug.Log` 已用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 条件编译包裹，复制示例时请保持守卫不变
> - `code` 仅在获取后立即发送到服务端，客户端不做存储
> - `session_key` 为服务端会话凭证，严禁客户端持久化存储（示例中的字段仅为演示）
> - 用户信息（`nickName`、`avatarUrl`、`gender`、`city` 等）禁止打印到生产日志，展示前应确认用户已授权 `scope.userInfo`
> - `GetUserInfo` 返回的 `encryptedData` 和 `iv` 仅发送到服务端解密，客户端不应解析或存储

## 一、登录与会话

### 1.1 TT.Login

**说明**: 调用抖音客户端登录，获取临时登录凭证 `code`（有效期 5 分钟）。需要将 `code` 发送到开发者服务端，通过 `code2Session` 接口换取 `openid` 和 `session_key`。若用户已登录且 session 有效，部分场景可直接返回结果而不弹出授权框。

**语法**:

```csharp
public void Login(
    OnLoginSuccessCallback successCallback,
    OnLoginFailedCallback failedCallback,
    bool forceLogin = true
)
```

**回调定义**:

```csharp
// 登录成功回调
// code: 临时登录凭证，有效期 5 分钟
// anonymousCode: 匿名登录凭证
// isLogin: 是否已登录（true=已登录直接返回，false=首次登录）
public delegate void OnLoginSuccessCallback(string code, string anonymousCode, bool isLogin);

// 登录失败回调
public delegate void OnLoginFailedCallback(string errMsg);
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| successCallback | OnLoginSuccessCallback | 是 | - | 登录成功回调 |
| failedCallback | OnLoginFailedCallback | 是 | - | 登录失败回调 |
| forceLogin | bool | 否 | true | 是否强制调起登录框。true=每次调起登录，false=已登录时直接返回不弹框 |

**代码示例**:

```csharp
using UnityEngine;
using TT;

public class LoginManager : MonoBehaviour
{
    void Start()
    {
        DoLogin();
    }

    /// <summary>
    /// 执行登录流程
    /// </summary>
    public void DoLogin(bool force = true)
    {
        TT.Login(
            successCallback: (code, anonymousCode, isLogin) =>
            {
                // ⚠️ 安全：code 为敏感凭证，生产环境禁止打印
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"登录成功: code={code}, isLogin={isLogin}");
                #endif
                // 将 code 发送到服务端换取 openid 和 session_key
                SendCodeToServer(code, anonymousCode);
            },
            failedCallback: (errMsg) =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"登录失败: {errMsg}");
                #endif
                // 提示用户登录失败，可重试或进入游客模式
            },
            forceLogin: force
        );
    }

    private void SendCodeToServer(string code, string anonymousCode)
    {
        // 示例: 通过 HTTP 请求将 code 发送到服务端
        StartCoroutine(ExchangeCodeOnServer(code, anonymousCode));
    }

    private System.Collections.IEnumerator ExchangeCodeOnServer(string code, string anonymousCode)
    {
        using (var request = UnityEngine.Networking.UnityWebRequest.Post(
            "https://your-server.com/api/auth/login",
            $"{{\"code\":\"{code}\",\"anonymousCode\":\"{anonymousCode}\"}}",
            "application/json"))
        {
            yield return request.SendWebRequest();
            if (request.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                Debug.Log("服务端登录验证成功");
                // 服务端返回: { openid, session_key, unionid }
            }
            else
            {
                Debug.LogError($"服务端验证失败: {request.error}");
            }
        }
    }
}
```

---

### 1.2 TT.CheckSession

**说明**: 检查当前登录态（session_key）是否过期。通常在每个需要登录态的操作前调用，若 session 过期则引导用户重新登录。

**语法**:

```csharp
public static void CheckSession(
    TTAccount.OnCheckSessionSuccessCallback successCallback,
    TTAccount.OnCheckSessionFailedCallback failedCallback
)
```

**回调定义**:

```csharp
// session 有效
public delegate void OnCheckSessionSuccessCallback();

// session 过期或无效
public delegate void OnCheckSessionFailedCallback(string errMsg);
```

**代码示例**:

```csharp
/// <summary>
/// 在需要登录态的操作前校验 session
/// </summary>
public void EnsureValidSession(System.Action onSessionValid)
{
    TT.CheckSession(
        successCallback: () =>
        {
            Debug.Log("Session 有效，可执行后续操作");
            onSessionValid?.Invoke();
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogWarning($"Session 已过期: {errMsg}");
            // 引导用户重新登录
            DoLogin(force: true);
        }
    );
}

// 使用示例: 支付前校验登录态
public void PurchaseItem(int itemId)
{
    EnsureValidSession(() =>
    {
        // Session 有效，发起支付
        var param = new RequestGamePaymentParam
        {
            Mode = "game",
            Env = 0,
            CurrencyType = "CNY",
            Platform = "android",
            BuyQuantity = 10,
            CustomId = System.Guid.NewGuid().ToString(),
            Success = (result) => Debug.Log("支付回调成功"),
            Fail = (error) => Debug.LogError($"支付失败: {error.ErrorCode}")
        };
        TT.RequestGamePayment(param);
    });
}
```

---

## 二、用户信息

### 2.1 TT.GetUserInfo

**说明**: 获取用户信息（头像、昵称、性别、地区等）。调用前需确保用户已授权 `scope.userInfo` 权限，否则返回的信息可能不完整。

**语法**:

```csharp
public static void GetUserInfo(
    OnGetUserInfoSuccessCallback successCallback,
    OnGetUserInfoFailedCallback failedCallback
)
```

**回调定义**:

```csharp
public delegate void OnGetUserInfoSuccessCallback(ref TTUserInfo userInfo);
public delegate void OnGetUserInfoFailedCallback(string errMsg);
```

**TTUserInfo 属性**:

| 属性 | 类型 | 说明 |
|------|------|------|
| avatarUrl | string | 用户头像 URL |
| nickName | string | 用户昵称 |
| gender | int | 性别: 0=未知, 1=男, 2=女 |
| city | string | 城市 |
| province | string | 省份 |
| country | string | 国家 |
| language | string | 语言 |
| signature | string | 个性签名 |
| encryptedData | string | 加密的用户数据（需服务端解密） |
| iv | string | 加密算法的初始向量 |
| cloudId | string | 敏感数据对应的云 ID（可通过云调用获取原始数据） |

**代码示例**:

```csharp
public void FetchUserInfo()
{
    TT.GetUserInfo(
        successCallback: (ref TTUserInfo userInfo) =>
        {
            // ⚠️ 安全：用户个人信息仅用于 UI 展示，禁止打印到生产日志
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log($"用户昵称: {userInfo.nickName}");
            Debug.Log($"头像 URL: {userInfo.avatarUrl}");
            Debug.Log($"性别: {GenderToString(userInfo.gender)}");
            Debug.Log($"地区: {userInfo.country} {userInfo.province} {userInfo.city}");
            #endif

            // 更新 UI
            UpdateUserProfileUI(userInfo);
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogError($"获取用户信息失败: {errMsg}");
            // 可能未授权，引导用户授权
        }
    );
}

private string GenderToString(int gender)
{
    switch (gender)
    {
        case 1: return "男";
        case 2: return "女";
        default: return "未知";
    }
}

private void UpdateUserProfileUI(TTUserInfo userInfo)
{
    // 更新 UI: 头像、昵称等
}
```

---

### 2.2 TT.GetUserInfoAuth

**说明**: 请求用户信息授权。当用户未授权 `scope.userInfo` 时，调用此方法弹出授权框让用户确认。与 `TT.GetUserInfo` 的区别: 本方法专门用于**请求授权**，不获取数据；获取数据仍需调用 `TT.GetUserInfo`。

**语法**:

```csharp
public static void GetUserInfoAuth(
    Action<string> successCallback,
    Action<string> failedCallback
)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| successCallback | Action\<string\> | 是 | 授权成功回调，参数为授权结果信息 |
| failedCallback | Action\<string\> | 是 | 授权失败回调 |

**代码示例**:

```csharp
/// <summary>
/// 确保用户已授权信息，再获取用户数据
/// </summary>
public void GetUserInfoWithAuth()
{
    // 先请求授权
    TT.GetUserInfoAuth(
        successCallback: (result) =>
        {
            Debug.Log($"用户授权成功: {result}");
            // 授权成功后获取用户信息
            TT.GetUserInfo(
                (ref TTUserInfo info) =>
                {
                    // ⚠️ 安全：用户昵称禁止打印到生产日志
                    #if UNITY_EDITOR || DEVELOPMENT_BUILD
                    Debug.Log($"用户: {info.nickName}");
                    #endif
                    UpdateUserProfileUI(info);
                },
                (err) => Debug.LogError($"获取信息失败: {err}")
            );
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogWarning($"用户拒绝授权: {errMsg}");
            // 降级处理: 使用默认头像和昵称
            ShowDefaultProfile();
        }
    );
}
```

---

## 三、设置与授权

### 3.1 TT.GetSetting

**说明**: 获取用户当前的授权设置状态。返回各 scope 权限的授权状态，用于判断用户是否已授权特定权限。

**语法**:

```csharp
public static void GetSetting(
    Action<AuthSetting> successCallback,
    Action<string> failedCallback
)
```

**AuthSetting 属性**:

| 属性 | 类型 | 说明 |
|------|------|------|
| UserInfo | bool | 是否授权用户信息（scope.userInfo） |
| UserLocation | bool | 是否授权地理位置（scope.userLocation） |
| Record | bool | 是否授权录音（scope.record） |
| Album | bool | 是否授权相册（scope.album） |
| Camera | bool | 是否授权摄像头（scope.camera） |
| ScreenRecord | bool | 是否授权录屏（scope.screenRecord） |
| Calendar | bool | 是否授权日历（scope.calendar） |

**代码示例**:

```csharp
public void CheckAuthSettings()
{
    TT.GetSetting(
        successCallback: (auth) =>
        {
            Debug.Log($"用户信息授权: {auth.UserInfo}");
            Debug.Log($"地理位置授权: {auth.UserLocation}");
            Debug.Log($"录音授权: {auth.Record}");
            Debug.Log($"相册授权: {auth.Album}");

            // 根据授权状态决定后续流程
            if (auth.UserInfo)
            {
                // 已授权，可直接获取用户信息
                FetchUserInfo();
            }
            else
            {
                // 未授权，引导用户授权
                Debug.Log("用户信息未授权，需要请求授权");
            }

            if (!auth.UserLocation)
            {
                Debug.Log("地理位置未授权，可能影响定位相关功能");
            }
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogError($"获取设置失败: {errMsg}");
        }
    );
}
```

---

### 3.2 TT.OpenSetting

**说明**: 打开小游戏设置页面，用户可在此页面中手动管理各项权限的授权状态。

**语法**:

```csharp
public static void OpenSetting(
    Action<AuthSetting> successCallback,
    Action<string> failedCallback
)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| successCallback | Action\<AuthSetting\> | 是 | 用户操作完成后的回调，返回最新的 AuthSetting |
| failedCallback | Action\<string\> | 是 | 打开设置页面失败回调 |

**代码示例**:

```csharp
/// <summary>
/// 引导用户打开设置页管理权限
/// </summary>
public void GuideToSettings()
{
    TT.OpenSetting(
        successCallback: (updatedAuth) =>
        {
            Debug.Log("用户已操作设置页");
            // 检查用户是否开启了我们需要的权限
            if (updatedAuth.UserInfo)
            {
                Debug.Log("用户在设置页开启了用户信息授权");
                FetchUserInfo();
            }
            else
            {
                Debug.Log("用户仍未开启用户信息授权");
            }
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogError($"打开设置页失败: {errMsg}");
        }
    );
}
```

---

### 3.3 TT.OpenSettingsPanel

**说明**: 打开系统设置面板。功能与 `TT.OpenSetting` 类似，但打开的是平台级别的设置面板，提供更丰富的选项。

**语法**:

```csharp
public static void OpenSettingsPanel(
    Action successCallback,
    Action<string> failedCallback
)
```

**代码示例**:

```csharp
public void OpenSystemSettings()
{
    TT.OpenSettingsPanel(
        successCallback: () =>
        {
            Debug.Log("用户已操作系统设置面板");
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogError($"打开设置面板失败: {errMsg}");
        }
    );
}
```

---

## 四、实名认证

### 4.1 TT.SetRealNameAuthenticationCallback

**说明**: 设置实名认证状态变化的回调监听。当用户的实名认证状态发生变化时（如通过认证、认证过期等），SDK 会回调此方法通知游戏。

**语法**:

```csharp
public static void SetRealNameAuthenticationCallback(
    Action<bool> callback
)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| callback | Action\<bool\> | 是 | 实名认证状态回调，true=已认证，false=未认证 |

**代码示例**:

```csharp
void Start()
{
    // 注册实名认证状态监听
    TT.SetRealNameAuthenticationCallback((isAuthenticated) =>
    {
        if (isAuthenticated)
        {
            Debug.Log("用户已完成实名认证");
            // 开启防沉迷相关限制
            EnableFullGameFeatures();
        }
        else
        {
            Debug.Log("用户未完成实名认证或认证已过期");
            // 限制游戏功能（如限制游戏时长、禁止支付等）
            EnableRestrictedMode();
        }
    });
}

private void EnableFullGameFeatures()
{
    // 解除防沉迷限制
}

private void EnableRestrictedMode()
{
    // 启用受限模式
}
```

---

### 4.2 TT.AuthenticateRealName

**说明**: 主动调起实名认证流程。调用后弹出实名认证界面，引导用户完成认证。通常在用户需要进行受限制操作时调用。

**语法**:

```csharp
public static void AuthenticateRealName(
    Action<bool> successCallback,
    Action<string> failedCallback
)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| successCallback | Action\<bool\> | 是 | 认证结果回调，true=认证成功 |
| failedCallback | Action\<string\> | 是 | 认证失败回调（用户取消或网络错误等） |

**代码示例**:

```csharp
/// <summary>
/// 需要实名认证的操作前调用
/// </summary>
public void RequireRealNameAuth(System.Action onSuccess)
{
    TT.AuthenticateRealName(
        successCallback: (result) =>
        {
            if (result)
            {
                Debug.Log("实名认证完成");
                onSuccess?.Invoke();
            }
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogWarning($"实名认证未完成: {errMsg}");
            // 提示用户需要实名认证才能继续操作
        }
    );
}

// 使用场景: 支付前校验实名
public void PurchaseWithAuthCheck(int itemId)
{
    RequireRealNameAuth(() =>
    {
        // 实名认证通过，执行支付
        Debug.Log("实名认证已通过，发起支付");
        // ... 支付逻辑
    });
}
```

---

## 五、抖音授权

### 5.1 TT.ShowDouyinOpenAuth

**说明**: 展示抖音授权面板，请求用户授权指定的 scope 列表。与 `TT.GetUserInfoAuth` 不同，本方法可一次性请求多个 scope 权限，适用于需要多个权限的业务场景。

**语法**:

```csharp
public static void ShowDouyinOpenAuth(
    Dictionary<string, DouyinPermissionScopeStatus> scopes,
    Action<Dictionary<string, bool>> successCallback,
    Action<string> failedCallback
)
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| scopes | Dictionary\<string, DouyinPermissionScopeStatus\> | 是 | 请求授权的 scope 列表，key 为 scope 名称，value 为该 scope 的状态 |
| successCallback | Action\<Dictionary\<string, bool\>\> | 是 | 授权完成回调，返回各 scope 的最终授权结果 |
| failedCallback | Action\<string\> | 是 | 授权失败回调 |

**DouyinPermissionScopeStatus 枚举**:

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| Required | 0 | 必选，用户不可取消勾选 |
| OptionalSelected | 1 | 可选，默认选中 |
| OptionalUnselected | 2 | 可选，默认不选中 |

**代码示例**:

```csharp
/// <summary>
/// 批量请求多个权限
/// </summary>
public void RequestMultipleScopes()
{
    // 定义需要请求的 scope 列表
    var scopes = new Dictionary<string, DouyinPermissionScopeStatus>
    {
        { "scope.userInfo", DouyinPermissionScopeStatus.Required },              // 用户信息（必选）
        { "scope.userLocation", DouyinPermissionScopeStatus.OptionalSelected },  // 地理位置（可选-默认勾选）
        { "scope.record", DouyinPermissionScopeStatus.OptionalUnselected }       // 录音（可选-默认不勾选）
    };

    TT.ShowDouyinOpenAuth(
        scopes: scopes,
        successCallback: (results) =>
        {
            Debug.Log("抖音授权完成:");
            foreach (var kv in results)
            {
                Debug.Log($"  {kv.Key}: {(kv.Value ? "已授权" : "未授权")}");
            }

            // 判断关键权限
            if (results.ContainsKey("scope.userInfo") && results["scope.userInfo"])
            {
                Debug.Log("用户信息已授权，获取用户数据");
                FetchUserInfo();
            }
            else
            {
                Debug.LogWarning("用户拒绝用户信息授权");
            }
        },
        failedCallback: (errMsg) =>
        {
            Debug.LogError($"抖音授权失败: {errMsg}");
        }
    );
}
```

---

## 六、完整登录流程示例

```csharp
using UnityEngine;
using TT;

/// <summary>
/// 完整的账号流程管理器
/// 涵盖: 初始化 -> 登录 -> Session校验 -> 获取用户信息 -> 权限管理 -> 实名认证
/// </summary>
public class AccountFlowManager : MonoBehaviour
{
    private ContainerEnv m_Env;
    private string m_OpenId;
    // ⚠️ 安全告警：session_key 是敏感凭证，严禁在客户端持久化存储。
    // 以下字段仅为示例演示，生产环境中 session_key 应仅保存在服务端
    private string m_SessionKey;

    void Start()
    {
        // 必须在 InitSDK 回调中执行账号相关操作
        if (!TT.InContainerEnv)
        {
            Debug.Log("Unity Editor 环境，跳过账号流程");
            return;
        }

        TT.InitSDK((code, env) =>
        {
            if (code != 0)
            {
                Debug.LogError($"SDK 初始化失败: {code}");
                return;
            }

            m_Env = env;
            Debug.Log($"宿主: {env.m_HostEnum}, 版本: {env.GetVersionType()}");

            // 第一步: 检查 Session
            CheckAndLogin();
        });
    }

    /// <summary>
    /// 检查 Session 有效性，无效则重新登录
    /// </summary>
    private void CheckAndLogin()
    {
        TT.CheckSession(
            successCallback: () =>
            {
                Debug.Log("Session 有效，直接进入游戏");
                OnLoginSuccess();
            },
            failedCallback: (errMsg) =>
            {
                Debug.Log($"Session 过期: {errMsg}，重新登录");
                DoLogin();
            }
        );
    }

    /// <summary>
    /// 登录流程
    /// </summary>
    private void DoLogin()
    {
        TT.Login(
            successCallback: (loginCode, anonymousCode, isLogin) =>
            {
                // ⚠️ 安全：code 为敏感凭证，生产环境禁止打印
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"登录成功: code={loginCode}, isLogin={isLogin}");
                #endif
                // 将 code 发送到服务端
                SendCodeToServer(loginCode, anonymousCode);
            },
            failedCallback: (errMsg) =>
            {
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.LogError($"登录失败: {errMsg}");
                #endif
                // 登录失败处理: 重试或进入游客模式
            },
            forceLogin: true
        );
    }

    private void SendCodeToServer(string code, string anonymousCode)
    {
        // 服务端 code2Session 换取 openid 和 session_key
        // POST https://developer.open-douyin.com/api/apps/v2/jscode2session
        // 参数: { appid, secret, code, anonymous_code }
        // 返回: { openid, session_key, unionid, anonymous_openid }

        // 示例模拟
        // ⚠️ 安全：code 为敏感凭证，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"发送 code 到服务端: {code}");
        #endif
        OnLoginSuccess();
    }

    private void OnLoginSuccess()
    {
        // 登录成功后: 检查权限 & 获取用户信息
        CheckPermissionsAndFetchInfo();
    }

    /// <summary>
    /// 检查权限并获取用户信息
    /// </summary>
    private void CheckPermissionsAndFetchInfo()
    {
        TT.GetSetting(
            successCallback: (auth) =>
            {
                if (auth.UserInfo)
                {
                    // 已授权，直接获取用户信息
                    FetchAndDisplayUserInfo();
                }
                else
                {
                    // 未授权，请求用户信息授权
                    TT.GetUserInfoAuth(
                        successCallback: (result) => FetchAndDisplayUserInfo(),
                        failedCallback: (err) => Debug.Log("用户拒绝用户信息授权")
                    );
                }
            },
            failedCallback: (err) => Debug.LogError($"获取授权状态失败: {err}")
        );
    }

    private void FetchAndDisplayUserInfo()
    {
        TT.GetUserInfo(
            successCallback: (ref TTUserInfo info) =>
            {
                // ⚠️ 安全：用户个人信息仅用于 UI 展示，禁止打印到生产日志
                #if UNITY_EDITOR || DEVELOPMENT_BUILD
                Debug.Log($"欢迎 {info.nickName}!");
                Debug.Log($"头像: {info.avatarUrl}");
                Debug.Log($"地区: {info.country}/{info.province}/{info.city}");
                #endif
            },
            failedCallback: (err) => Debug.LogError($"获取用户信息失败: {err}")
        );
    }

    /// <summary>
    /// 支付前的完整权限校验（示例）
    /// </summary>
    public void PayWithFullCheck(int itemId)
    {
        // 1. Session 校验
        TT.CheckSession(
            successCallback: () =>
            {
                // 2. 实名认证校验
                TT.AuthenticateRealName(
                    successCallback: (authenticated) =>
                    {
                        if (authenticated)
                        {
                            // 3. 所有校验通过，执行支付
                            ExecutePayment(itemId);
                        }
                    },
                    failedCallback: (err) => Debug.Log("实名认证失败，无法支付")
                );
            },
            failedCallback: (err) =>
            {
                Debug.Log("Session 过期，重新登录");
                DoLogin();
            }
        );
    }

    private void ExecutePayment(int itemId)
    {
        var param = new RequestGamePaymentParam
        {
            Mode = "game",
            Env = 0,
            CurrencyType = "CNY",
            Platform = "android",
            BuyQuantity = 10,
            CustomId = System.Guid.NewGuid().ToString(),
            Success = (result) => Debug.Log("支付成功"),
            Fail = (error) => Debug.LogError($"支付失败: {error.ErrorCode}")
        };
        TT.RequestGamePayment(param);
    }
}
```

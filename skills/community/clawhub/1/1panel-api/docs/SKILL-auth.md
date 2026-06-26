# Auth - 1Panel API

## 模块说明
Auth 模块接口，包含验证码、用户登录、MFA 登录、Passkey 登录等功能。

## 接口列表 (7 个)

---

### GET /core/auth/captcha
**功能**: Load captcha - 获取验证码图片

**请求参数**: 无

**返回参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| captchaID | string | 验证码 ID |
| imagePath | string | 验证码图片路径 |

---

### GET /core/auth/setting
**功能**: Get Setting For Login - 获取登录设置信息

**请求参数**: 无

**返回参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| isDemo | boolean | 是否演示模式 |
| isIntl | boolean | 是否国际版 |
| isOffLine | boolean | 是否离线模式 |
| isFxplay | boolean | 是否 fxplay |
| language | string | 语言设置 |
| menuTabs | string | 菜单标签设置 |
| panelName | string | 面板名称 |
| theme | string | 主题 |
| needCaptcha | boolean | 是否需要验证码 |
| passkeySetting | boolean | Passkey 是否已配置 |

---

### POST /core/auth/login
**功能**: User login - 用户登录

**请求头参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| EntranceCode | string | 否 | 安全入口 base64 加密串 |

**请求体参数** (dto.Login):
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| name | string | 是 | 用户名 | validate:"required" |
| password | string | 是 | 密码 | validate:"required" |
| captcha | string | 否 | 验证码 (需要验证码时必填) | - |
| captchaID | string | 否 | 验证码 ID (需要验证码时必填) | - |
| language | string | 是 | 语言 | validate:"required,oneof=zh en 'zh-Hant' ko ja ru ms 'pt-BR' tr 'es-ES'" |

**返回参数** (dto.UserLoginInfo):
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 用户名 |
| token | string | 访问令牌 |
| mfaStatus | string | MFA 状态 (enable/disable) |

**语言取值范围**: `zh`, `en`, `zh-Hant`, `ko`, `ja`, `ru`, `ms`, `pt-BR`, `tr`, `es-ES`

---

### POST /core/auth/logout
**功能**: User logout - 用户登出

**请求参数**: 无 (需要登录认证)

**返回参数**: 无 (返回 200 表示成功)

---

### POST /core/auth/mfalogin
**功能**: User login with mfa - MFA 两步验证登录

**请求头参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| EntranceCode | string | 否 | 安全入口 base64 加密串 |

**请求体参数** (dto.MFALogin):
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| name | string | 是 | 用户名 | validate:"required" |
| password | string | 是 | 密码 | validate:"required" |
| code | string | 是 | MFA 验证码 | validate:"required" |

**返回参数** (dto.UserLoginInfo):
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 用户名 |
| token | string | 访问令牌 |
| mfaStatus | string | MFA 状态 |

---

### POST /core/auth/passkey/begin
**功能**: User login with passkey - Passkey 登录开始

**请求参数**: 无

**返回参数** (dto.PasskeyBeginResponse):
| 字段 | 类型 | 说明 |
|------|------|------|
| sessionId | string | Passkey 会话 ID |
| publicKey | object | Passkey 公钥对象 |

---

### POST /core/auth/passkey/finish
**功能**: User login with passkey - Passkey 登录完成

**请求头参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Passkey-Session | string | 是 | Passkey 会话 ID |

**请求参数**: 无 (使用 Passkey 凭证完成登录)

**返回参数** (dto.UserLoginInfo):
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 用户名 |
| token | string | 访问令牌 |
| mfaStatus | string | MFA 状态 |

---

## 相关 DTO 结构

### dto.CaptchaResponse
```go
type CaptchaResponse struct {
    CaptchaID string `json:"captchaID"`
    ImagePath string `json:"imagePath"`
}
```

### dto.UserLoginInfo
```go
type UserLoginInfo struct {
    Name      string `json:"name"`
    Token     string `json:"token"`
    MfaStatus string `json:"mfaStatus"`
}
```

### dto.Login
```go
type Login struct {
    Name      string `json:"name" validate:"required"`
    Password  string `json:"password" validate:"required"`
    Captcha   string `json:"captcha"`
    CaptchaID string `json:"captchaID"`
    Language  string `json:"language" validate:"required,oneof=zh en 'zh-Hant' ko ja ru ms 'pt-BR' tr 'es-ES'"`
}
```

### dto.MFALogin
```go
type MFALogin struct {
    Name     string `json:"name" validate:"required"`
    Password string `json:"password" validate:"required"`
    Code     string `json:"code" validate:"required"`
}
```

### dto.LoginSetting
```go
type LoginSetting struct {
    IsDemo         bool   `json:"isDemo"`
    IsIntl         bool   `json:"isIntl"`
    IsOffLine      bool   `json:"isOffLine"`
    IsFxplay       bool   `json:"isFxplay"`
    Language       string `json:"language"`
    MenuTabs       string `json:"menuTabs"`
    PanelName      string `json:"panelName"`
    Theme          string `json:"theme"`
    NeedCaptcha    bool   `json:"needCaptcha"`
    PasskeySetting bool   `json:"passkeySetting"`
}
```

### dto.PasskeyBeginResponse
```go
type PasskeyBeginResponse struct {
    SessionID string      `json:"sessionId"`
    PublicKey interface{} `json:"publicKey"`
}
```

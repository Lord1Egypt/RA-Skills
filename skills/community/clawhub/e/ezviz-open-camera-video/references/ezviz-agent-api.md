# Ezviz Agent API Reference (萤石开放平台 API 参考)

本文档整理自萤石开放平台官方文档，供技能开发参考。

## API 域名

| 域名 | 用途 | 说明 |
|------|------|------|
| `openai.ys7.com` | ✅ API 接口 | 萤石开放平台 **API 专用域名** |
| `open.ys7.com` | 🌐 官方网站 | 萤石开放平台 **官网/文档** 入口 |

**注意**: `openai` 是 "Open API" 的缩写，**不是** 指 OpenAI 或人工智能。

## 基础 API

### 1. 获取 AccessToken

**文档**: https://openai.ys7.com/help/81

**接口**:
```
POST https://openai.ys7.com/api/lapp/token/get
```

**请求参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| appKey | String | Y | 应用 Key |
| appSecret | String | Y | 应用 Secret |

**返回示例**:
```json
{
  "code": "200",
  "msg": "操作成功!",
  "data": {
    "accessToken": "at.xxxxxxxxxxxxx",
    "expireTime": 1470810222045
  }
}
```

**Token 说明**:
- 有效期：**7 天**
- 新 Token 不会使老 Token 失效
- 建议本地缓存，即将过期或报错 10002 时再获取

**错误码**:
| 返回码 | 返回消息 | 描述 |
|--------|----------|------|
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken 异常或过期 | 重新获取 accessToken |
| 10005 | appKey 异常 | appKey 被冻结 |
| 10017 | appKey 不存在 | 确认 appKey 是否正确 |
| 10030 | appkey 和 appSecret 不匹配 | - |

---

### 2. 设备抓图

**文档**: https://openai.ys7.com/help/687

**接口**:
```
POST https://openai.ys7.com/api/lapp/device/capture
```

**请求参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| accessToken | String | Y | 访问令牌 |
| deviceSerial | String | Y | 设备序列号（大写） |
| channelNo | int | Y | 通道号（IPC 填 1） |
| quality | int | N | 视频清晰度（不生效） |

**返回示例**:
```json
{
  "code": "200",
  "msg": "操作成功!",
  "data": {
    "picUrl": "https://opencapture.ys7.com/.../capture/xxx.jpg?Expires=xxx&..."
  }
}
```

**注意**:
- 仅适用于 IPC 或关联 IPC 的 DVR 设备
- 设备需支持能力集：`support_capture=1`
- 调用间隔建议 **4 秒以上**，避免限流
- 图片 URL 有效期：**2 小时**

**错误码**:
| 返回码 | 返回消息 | 描述 |
|--------|----------|------|
| 200 | 操作成功 | 请求成功 |
| 10002 | accessToken 异常或过期 | 重新获取 |
| 10028 | 抓图接口调用次数超限 | 降低频率，间隔>4s |
| 20002 | 设备不存在 | 检查设备序列号 |
| 20006 | 网络异常 | 检查设备网络 |
| 20007 | 设备不在线 | 检查设备状态 |
| 20008 | 设备响应超时 | 操作过于频繁 |
| 20014 | deviceSerial 不合法 | 检查序列号格式 |
| 60020 | 不支持该命令 | 设备不支持抓图 |

---

## 预览链接格式

### PC 端预览

```
https://open.ys7.com/console/jssdk/pc.html?url=ezopen://{serial}/{channel}.live&accessToken={token}&themeId=pcLive
```

### 移动端预览

```
https://open.ys7.com/console/jssdk/mobile.html?url=ezopen://{serial}/{channel}.live&accessToken={token}&themeId=mobileLive
```

**参数说明**:
- `{serial}`: 设备序列号（如 `BC7799091`）
- `{channel}`: 通道号（通常为 `1`）
- `{token}`: accessToken

---

## 官方文档

- **开放平台首页**: https://open.ys7.com/
- **API 文档中心**: https://openai.ys7.com/doc/
- **Token 获取文档**: https://openai.ys7.com/help/81
- **设备抓图文档**: https://openai.ys7.com/help/687

---

## 验证命令

```bash
# 验证 API 域名连通性
curl -I https://openai.ys7.com/api/lapp/token/get

# 验证官网连通性
curl -I https://open.ys7.com/

# 检查 SSL 证书
curl -vI https://openai.ys7.com/api/lapp/token/get 2>&1 | grep -A5 "SSL certificate"

# 验证域名所有权
whois ys7.com
```

---

**最后更新**: 2026-03-19

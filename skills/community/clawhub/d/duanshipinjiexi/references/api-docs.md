# API 文档

> Base URL: `https://spqsy.kcucu.com`
> 所有身份码参数大小写不敏感，大小写完全等价

## 🆔 身份码系统

身份码是5位字母数字，永久不变。所有操作绑定同一个身份码：
- 首次调用自动生成，每天免费10次
- 购买套餐后同一身份码叠加权益
- 可以随时修改身份码（换好记的码）

## 1. 创建身份码（无需视频链接）

```bash
GET /api/create_identity.php
```

```json
{
  "code": 200,
  "data": {
    "identity_code": "{CODE}",
    "daily_limit": 10,
    "is_new": false
  }
}
```

也可指定自定义码：

```bash
GET /pay/identity.php?code={CODE}
```

```json
{
  "code": 200,
  "data": {
    "identity_code": "{CODE}",
    "is_new": true
  }
}

## 2. 解析视频

```bash
GET /api/parse.php?code={身份码}&url={链接}
# 首次调用可不传 code，自动生成身份码
GET /api/parse.php?url={链接}
```

### 响应 JSON

```json
{
  "code": 200,
  "data": {
    "type": "",
    "title": "",
    "author": {},
    "url": "",
    "video_backup": [],
    "images": [],
    "live_photo": [],
    "music": {},
    "stats": {}
  },
  "identity_info": {
    "is_new": false,
    "daily_remaining": 0,
    "remaining": null,
    "plans": []
  }
}
```

### 关键字段

| 字段 | 说明 |
|------|------|
| data.type | video=视频, image=图片, live=动图 |
| data.url | 视频直链（video 类型） |
| data.images[] | 所有静图 URL，可直接 `curl` 下载 |
| data.live_photo[] | 动图素材：每段有 video(MP4) + image(静图)。**下载 video 需带 User-Agent 和 Referer** |
| data.music.url | 配乐链接（可直接下载） |
| data.stats | 互动数据：liked/comment/share/collect |
| identity_info.daily_remaining | 今日剩余次数 |
| identity_info.remaining | 计次剩余次数 |

### 错误码

| HTTP | msg | 说明 |
|------|-----|------|
| 400 | 缺少参数: url | 未传视频链接 |
| 403 | 身份码无效 | 身份码不存在或已停用 |
| 429 | 今日调用次数已达上限 | 免费每日10次用完，或所有权益耗尽 |
| 500 | 解析服务异常 | 服务器异常，重试一次 |

## 3. 修改身份码

```bash
POST /api/modify_identity.php
Content-Type: application/x-www-form-urlencoded

old_code=原身份码&new_code=新身份码
```

规则：5位数字+字母，大小写不敏感，60秒防抖。权益全部保留。

| HTTP | 含义 |
|------|------|
| 200 | 修改成功 |
| 400 | 参数缺失 / 格式错误 |
| 404 | 旧身份码不存在 |
| 403 | 旧身份码已停用 |
| 409 | 新码已被占用 |
| 429 | 操作太频繁 |

## 4. 查身份码状态

```bash
GET /api/identity_info.php?code={身份码}
```

零消耗，返回完整权益信息：

```json
{
  "code": 200,
  "data": {
    "is_active": true,
    "plans": [],
    "remaining": null,
    "daily_remaining": 0,
    "daily_used_today": 0,
    "expires_at": null
  }
}
```

## 5. 下单

```bash
POST /pay/create.php
Content-Type: application/json

{"identity_code": "{身份码}", "id": "count_10", "name": "体验套餐", "type": "count", "count": 10, "price": 0.50}
```

```json
{"success": true, "order_id": "SV20260707XXXX", "qr_code": "https://qr.alipay.com/xxx", "amount": 0.50}
```

⚠️ 收到 `qr_code` 后必须 `qrencode -o /tmp/qr.png "URL"` 生成二维码图片发 MEDIA。禁止直接发链接。

### 套餐列表

```bash
GET /pay/plans.php
```

动态获取，以实时返回为准。

## 6. 查支付状态

```bash
GET /pay/query.php?order_id=SV20260707XXXX
```

| status | 含义 |
|--------|------|
| `paid` | ✅ 已支付，权益已绑定到身份码 |
| `pending` | ⏳ 等待支付 |
| `closed` | ❌ 已关闭 |

支付成功后用 `identity_info.php` 确认权益到账。

## 7. 购买时生成身份码

用户购买后可能要一个新的身份码来接收套餐：

```bash
GET /pay/identity.php?code=用户自定义码
# 或自动生成
GET /pay/identity.php
```

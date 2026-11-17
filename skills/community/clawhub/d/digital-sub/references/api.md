# 企业全情报订阅 API 参考

## 日报列表

- URL：`https://gateway.36kr.com/api/mis/companyDailyReport/skills/list`
- Method：`POST`
- Body：

```json
{
  "partner_id": "web",
  "param": {
    "apiKey": "your-api-key",
    "keyword": "示例企业"
  }
}
```

成功响应：

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "itemList": [
      {
        "title": "示例文章标题",
        "publishTime": 1776607200000,
        "url": "https://example.com/company/detail",
        "qrCode": "iVBORw0KGgoAAA..."
      }
    ]
  }
}
```

查询窗口为当前时间向前 24 小时，排序为 `publish_time DESC, id DESC`。`itemList` 可能为空。
qrCode 或者 qrCodeBase64 这样的返回值是用户舆情二维码,需要引导用户用微信APP扫码查看具体信息.

## 申请 API Key

- URL：`https://gateway.36kr.com/api/pms/skills/auth/gen/key`
- Method：`POST`
- Content-Type：`application/json`
- 登录态：不需要 Cookie 或 `krtoken`
- Body：

```json
{
  "partner_id": "web",
  "param": {
    "ip": "192.168.0.1"
  }
}
```

`ip` 是顶层可选字符串，不使用 `param` 包裹。服务端会把 IP 与新生成的 API Key 缓存 5 分钟，供后续二维码和绑定流程校验。IP 为空时服务端仍可生成 Key。

成功响应：

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "apiKey": "kr_aa_xxxxxxxxxxxxxxxx"
  }
}
```

API Key 格式为 `kr_{version}_{16位随机字母数字}`，版本由服务端配置决定，不应由客户端拼装。客户端仅在 `code == 0` 且 `data.apiKey` 非空时接受该 Key，并在收到后立即写入当前运行上下文及用户环境变量 `kr_skills_api_key`，无需等待扫码绑定完成。

示例 IP 仅用于说明格式。优先使用检测到的本机 IPv4/IPv6；如果无法获取，不阻断流程，使用 `127.0.0.1` 作为占位并提示用户。该 Controller 明确为客户端无登录态接口，因此不要发送 `KR_SKILLS_AUTH_COOKIE`、Cookie 或 `krtoken`。

当日报接口返回 401/403，或业务错误明确表示 Key 无效/过期时，本次请求最多重新调用一次 gen/key，并用新 Key 重试；不要无限重试。

## 获取绑定二维码

- URL：`https://gateway.36kr.com/api/pms/skills/auth/qrCode`
- Method：`POST`
- Content-Type：`application/json`
- 登录态：不需要 Cookie 或 `krtoken`
- Body：

```json
{
  "partner_id": "web",
  "param": {
    "apiKey": "kr_aa_xxxxxxxxxxxxxxxx",
    "addr": "上海",
    "deviceName": "MacBook-Pro",
    "skillVersion": "1.3.0"
  }
}
```

请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `param.apiKey` | 是 | `gen/key` 返回的完整 API Key。 |
| `param.addr` | 否 | 设备所在地址或展示用位置。 |
| `param.deviceName` | 否 | 设备名称，便于用户在授权列表中辨认。 |
| `param.skillVersion` | 否 | 当前 skill 版本。 |

未绑定时成功响应：

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "qrCodeBase64": "iVBORw0KGgoAAA...",
    "bound": false,
    "expireTime": 1776607200000
  }
}
```

- `qrCodeBase64`：微信小程序码原始 Base64，不含 data URI 前缀。
- `bound`：`false` 表示需要扫码；`true` 表示该 Key 已绑定，可直接跳过扫码。
- `expireTime`：二维码绑定会话到期时间，Unix 毫秒；默认会话时长为 10 分钟，以服务端配置为准。

已绑定时成功响应：

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "qrCodeBase64": null,
    "bound": true,
    "expireTime": null
  }
}
```

常见业务错误：

| 条件 | `code` | `msg`/处理 |
| --- | --- | --- |
| `param.apiKey` 为空 | 参数校验失败 | 不调用后续流程，检查请求体。 |
| Key 不存在或 `gen/key` 的 5 分钟缓存已过期 | `1` | `apiKey 不存在或已过期`；重新调用一次 `gen/key` 并持久化新 Key。 |
| 同一 Key 10 秒内频繁申请二维码 | `1` | `请求过于频繁`；等待后再重试，不重新生成 Key。 |
| 微信小程序码生成失败 | `1` | `二维码生成失败`；按临时服务错误处理。 |

仅从 `data.qrCodeBase64` 读取图片，不猜测 `data`、`data.qrCode` 等其他字段。默认按 PNG 拼接 `data:image/png;base64,...`。展示后等待用户微信扫码绑定确认；持久化 API Key 本身不需要等待绑定。

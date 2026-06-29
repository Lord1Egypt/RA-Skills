# 二维码 API

## createQRCode — 生成二维码

### 接口说明

获取小程序/小游戏的二维码。该二维码可通过任意 app 扫码打开，能跳转到开发者指定的对应字节系 app 内拉起小程序/小游戏，并传入开发者指定的参数。通过该接口生成的二维码，**永久有效，暂无数量限制**。

**注意**：
- 使用前请先配置默认分享文案和图片
- 小程序的 path 要 encode 一次，如 `pages%3fparam%3dtrue`
- 小游戏的 path 为 JSON 字符串，如 `{"param":true}`
- 圆形码（抖音码）和普通正方形二维码都支持

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/qrcode` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Body（JSON）**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| appname | String | 是 | 打开二维码的字节系 app 名称，默认为 `douyin` |
| path | String | 是 | 小游戏启动参数，格式为 JSON 字符串 |
| width | Int32 | 是 | 二维码宽度 px，最小 280，最大 1280，默认 430 |
| is_circle_code | Bool | 否 | 是否圆形码，true=抖音码，false=普通二维码 |
| auto_color | Bool | 否 | is_circle_code=false 时生效，自动配置线条颜色 |
| line_color | Struct | 否 | 二维码线条颜色 `{r, g, b}`，默认黑色 |
| background | Struct | 否 | 二维码背景颜色 `{r, g, b}`，默认白色 |
| set_icon | Bool | 否 | is_circle_code=false 时生效，是否展示小游戏 icon |
| version_type | String | 否 | 版本：`current`(线上版) / `latest`(开发版) |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| data | Binary | 直接返回二维码图片的 []byte 数组 |
| errcode | Int64 | 错误号，0 为成功 |
| errmsg | String | 错误信息 |

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 成功 | - |
| 200 | -1 | 系统错误 | - |
| 200 | 40002 | access_token 错误 | 检查 token 是否正确 |
| 200 | 40016 | appname 错误 | 检查 appname 参数 |
| 200 | 40021 | width 超过指定范围 | width 需在 280-1280 |
| 200 | 60003 | 频率限制（5000 次/分钟） | 降低请求频率 |
| 200 | 60103 | 没有设置分享图标 | 先配置分享图标 |
| 200 | 40026 | 版本参数错误 | 检查 version_type |

### 请求示例

```bash
curl --location 'https://minigame.zijieapi.com/mgplatform/api/apps/qrcode' \
--header 'Content-Type: application/json' \
--data '{
  "access_token": "0801121847...",
  "appname": "douyin",
  "path": "",
  "width": 280,
  "line_color": {"r": 0, "g": 0, "b": 0},
  "background": {"r": 255, "g": 255, "b": 255},
  "set_icon": false,
  "is_circle_code": true,
  "version_type": "current",
  "auto_color": false
}'
```

---
name: fitconverter
description: |
  运动健康转换工具。华为、Zepp、小米、vivo、三星、Keep、悦跑圈、RQrun、动动、行者运动记录导出后，可通过运动健康转换工具转换成fit、tcx、gpx、kml格式文件同步导入高驰、佳明、RQrun、Strava等主流运动平。
  运动记录转换工具、运动记忆、运动数据转换、fitconverter、华为运动数据、小米运动数据、Zepp跑步记录、Keep数据导出、转换fit、转换tcx
homepage: https://www.fitconverter.com
metadata:
  openclaw:
    emoji: "🏃"
    requires:
      bins: ["mcporter"]
    primaryEnv: "FITCONVERTER_MCP_KEY"
---

# FitConverter 运动数据转换

通过 MCP + HTTP 协议调用 FitConverter 服务，将运动数据从一个平台转换到另一个平台。

## 1. 新用户必读

⚠️ **首次使用需要获取 API Key**

1. 访问 https://api.fitconverter.com/mcp/generate-api-key 获取 API Key
2. 告诉我你的 API Key，我会帮你配置
3. 或者手动配置 mcporter（见下文）

---

## 2. 配置 API Key

### 方式一：对话中配置（推荐）

直接告诉我你的 API Key：

```
我的 FitConverter API Key 是 fc_mcp_xxxxxx
```

我会自动帮你配置。

### 方式二：手动配置 mcporter

编辑 `~/.mcporter/mcporter.json`，添加：

```json
{
  "mcpServers": {
    "fitconverter": {
      "baseUrl": "https://api.fitconverter.com/mcp",
      "headers": {
        "Authorization": "Bearer 你的API_KEY"
      }
    }
  }
}
```

---

## 3. 使用方式

配置完成后，直接对话即可：

```
帮我把华为的运动数据转到高驰
我要把 Keep 的记录转到佳明
转换 GPX 文件到 FIT 格式
```

---

## 4. 支持的平台

### 数据源（type）

- **文件类型**：huawei, zepp, xiaomi, vivo, keep, samsung, dongdong, kml, gpx, tcx, fit
- **同步类型**：zepp_sync, keep_sync, codoon_sync, joyrun_sync, xingzhe_sync, garmin_sync_coros

### 目标平台（destination）

coros, garmin, strava, rqrun, huawei, keep, shuzixindong, xingzhe, igpsport, onelap, fit, tcx, gpx, kml

---

## 5. Agent 执行流程

### 5.1 检查配置

1. 检查 mcporter 是否已配置 fitconverter 服务器
2. 若未配置，引导用户访问 https://api.fitconverter.com/mcp/generate-api-key 获取 API Key

### 5.2 调用 MCP 工具

```bash
# 列出支持的平台
mcporter call fitconverter.list_platforms
# 查询转换状态
mcporter call fitconverter.get_conversion_status
```

### 5.3 提交转换任务

⚠️ **重要**：`zip_file`使用 multipart/form-data 上传文件（不是路径，不是Base64）：

```bash
curl -X POST "https://api.fitconverter.com/mcp/submit_conversion" \
  -H "Authorization: Bearer fc_mcp_xxx" \
  -F "api_key=fc_mcp_xxx" \
  -F "type=huawei" \
  -F "destination=coros" \
  -F "address=user@example.com" \
  -F "zip_file=@/path/to/upload.zip"
```

**Node.js 示例：**

```javascript
const FormData = require('form-data');
const fs = require('fs');
const https = require('https');

const form = new FormData();
form.append('api_key', 'fc_mcp_xxx');
form.append('type', 'huawei');
form.append('destination', 'coros');
form.append('address', 'user@example.com');
form.append('zip_file', fs.createReadStream('/path/to/upload.zip'));

const options = {
  hostname: 'api.fitconverter.com',
  port: 443,
  path: '/mcp/submit_conversion',
  method: 'POST',
  headers: {
    'Authorization': 'Bearer fc_mcp_xxx',
    ...form.getHeaders()
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => { console.log(data); });
});

form.pipe(req);
```

**返回示例：**

```json
{
  "status": "payment_required",
  "order_id": "fitId_xxx",
  "qr_image_url": "https://file.fitconverter.com/qr/qr-xxx.png",
  "code_url": "weixin://wxpay/bizpayurl?pr=xxx",
  "amount": "1.00",
  "message": "需要微信支付"
}
```

### 5.4 查询转换状态

```bash
mcporter call fitconverter.get_conversion_status --args '{
  "api_key": "fc_mcp_xxx",
  "order_id": "fitId_xxx"
}'
```

---

## 6. 返回状态处理

| status | 含义 | 操作 |
|--------|------|------|
| payment_required | 需要支付 | 展示二维码，引导用户支付 |
| pending_payment | 等待支付中 | 轮询 get_conversion_status |
| submitted | 提交成功 | 告知用户等待邮件通知 |
| error | 错误 | 返回错误信息 |

---

## 7. 支付二维码展示

当返回 `qr_image_url` 时，使用 message 工具发送图片：

```javascript
message({
  action: "send",
  channel: "discord",
  target: "user:用户ID",
  media: "https://file.fitconverter.com/qr/qr-xxx.png",
  caption: "请扫码支付"
})
```

---

## 8. 错误处理

| 错误 | 解决方案 |
|------|----------|
| 未配置 API Key | 引导访问 https://api.fitconverter.com/mcp/generate-api-key |
| 不支持的数据源 | 从支持的平台选择：huawei, keep, xiaomi 等 |
| 不支持的目标平台 | 选择目标平台：garmin, coros, strava 等 |

---

## 9. API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/mcp/submit_conversion` | POST | 上传文件提交转换（multipart/form-data） |

---

## 10. 参数说明

### 提交转换（submit_conversion）

| 参数 | 必填 | 说明                           |
|------|------|------------------------------|
| api_key | 是 | API Key                      |
| type | 是 | 数据源平台                        |
| destination | 是 | 目标平台                         |
| address | 是 | 结果通知邮箱                       |
| recordMode | 否 | 转换模式：trial_（试用，默认）或 do（正式付费） |
| zip_file | 是* | 文件（文件类型必填）                   |
| account | 是* | 账号（同步类型必填）                   |
| password | 是* | 密码（同步类型必填）                   |

\* 根据数据源类型选择必填参数

---

## 11. 转换模式说明

| recordMode | 说明 | 费用 |
|------------|------|------|
| trial_     | 试用模式（默认） | ¥0.10 |
| do         | 正式付费 | ¥19.90 |

**注意**：试用模式有次数限制，正式付费可获得完整功能。

---

## 12. 完整示例

```bash
curl -X POST "https://api.fitconverter.com/mcp/submit_conversion" \
  -H "Authorization: Bearer fc_mcp_xxx" \
  -F "api_key=fc_mcp_xxx" \
  -F "type=huawei" \
  -F "destination=coros" \
  -F "address=user@example.com" \
  -F "recordMode=trial_" \
  -F "zip_file=@/path/to/upload.zip"
```

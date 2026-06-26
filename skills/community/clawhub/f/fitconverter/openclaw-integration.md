# OpenClaw 集成指南

## 新用户引导

**首次使用必须获取 API Key**：https://api.fitconverter.com/mcp/generate-api-key

获取后告诉 Agent，会自动配置。

---

## MCP 配置

### mcporter 配置文件

编辑 `~/.mcporter/mcporter.json`：

```json
{
  "mcpServers": {
    "fitconverter": {
      "baseUrl": "https://api.fitconverter.com/mcp",
      "headers": {
        "Authorization": "Bearer fc_mcp_xxx"
      }
    }
  }
}
```

### 验证配置

```bash
mcporter list
# 应看到 fitconverter (3 tools)
```

---

## 工具列表

| 工具 | 说明                    |
|------|-----------------------|
| `list_platforms` | 列出支持的平台               |
| `submit_conversion` | 提交转换任务（废弃），改用下方HTTP调用 |
| `get_conversion_status` | 查询转换状态                |

---

## 参数说明

### submit_conversion（废弃）

### get_conversion_status

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| api_key | string | ✅ | API Key |
| order_id | string | ✅ | 订单 ID |

---

## 提交转换

文件可能较大，使用HTTP 直接调用：

⚠️ `zip_file` 参数需要 **使用 multipart/form-data 上传文件**，不是路径，不是Base64！

| 参数 | 必填 | 说明 |
|------|------|------|
| api_key | ✅ | 从 /mcp/generate-api-key 获取 |
| type | ✅ | 数据源平台 |
| destination |✅ | 目标平台 |
| address |✅ | 结果通知邮箱 |
| zip_file |条件 | **使用 multipart/form-data 上传文件** |
| account |条件 | 账号（同步类型） |
| password |条件 | 密码（同步类型） |

```bash
curl -X POST "https://api.fitconverter.com/mcp/submit_conversion" \
  -H "Authorization: Bearer fc_mcp_xxx" \
  -F "api_key=fc_mcp_xxx" \
  -F "type=huawei" \
  -F "destination=coros" \
  -F "address=user@example.com" \
  -F "zip_file=@/path/to/upload.zip"
```

---

## 返回状态处理

| status | 含义 | 操作 |
|--------|------|------|
| `payment_required` | 需要支付 | 展示二维码，引导支付 |
| `pending_payment` | 等待支付 | 轮询 get_conversion_status |
| `submitted` | 提交成功 | 等待邮件通知 |
| `error` | 错误 | 返回错误信息 |

如果返回错误信息`error`内有`zip_intro_image_url`信息，可以发送此zip压缩包的指引图片引导用户构建含正确目录结果的zip压缩包

---

## 支付二维码展示

### 优先级

| 优先级 | 字段 | 展示方式 |
|--------|------|----------|
| 1 | `qr_image_url` | message 工具发送图片 |
| 2 | `qr_data_url` | Markdown 嵌入 |
| 3 | `code_url` | 文本链接 |

### 发送图片

```javascript
message({
  action: "send",
  channel: "discord",
  target: "user:用户ID",
  media: "https://file.fitconverter.com/qr/qr-xxx.png",
  caption: "请扫码支付"
})
```

### 文本链接

```markdown
微信扫一扫：weixin://wxpay/bizpayurl?pr=xxx
```

---

## 对话收集流程

按以下顺序收集参数：

1. 检查是否已配置 API Key → 未配置则引导获取
2. `type` - 你要转换哪种来源的数据？
3. `destination` - 要导入到哪个平台？
4. `address` - 结果发到哪个邮箱？
5. `zip_file` →  multipart/form-data 上传文件 后提交
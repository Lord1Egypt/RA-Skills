# 错误日志详细说明

当云API调用或工具执行出现错误时，脚本会自动将错误信息写入日志文件。

## 日志位置

| 配置方式 | 日志路径 |
|---------|---------|
| 默认 | `./logs/apm_error.log`（相对于脚本执行目录） |
| 自定义 | 通过环境变量 `APM_ERROR_LOG_DIR` 指定目录 |

## 日志格式

### 云API错误日志（SDK异常）

```json
{
    "timestamp": "2026-03-11T14:30:00Z",
    "action": "SendMCPMessage:tools/call",
    "error_code": "AuthFailure.SecretIdNotFound",
    "error_message": "The SecretId is not found",
    "request_id": "eac6b301-a322-493a-8e36-83b295459397",
    "extra": {
        "method": "tools/call",
        "tool_name": "DescribeApmOverview"
    }
}
```

### 异常类错误（含堆栈信息）

```json
{
    "timestamp": "2026-03-11T14:30:00Z",
    "action": "SendMCPMessage:tools/list",
    "exception_type": "ConnectionError",
    "exception_message": "...",
    "traceback": "Traceback (most recent call last): ...",
    "extra": {
        "method": "tools/list",
        "tool_name": null
    }
}
```

## 日志安全

- 日志文件创建后自动设置权限为 `600`
- 日志内容**不会记录** SecretId 或 SecretKey
- 建议将 `logs/` 加入 `.gitignore`

## 常见错误排查

### 认证失败

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| `AuthFailure.SecretIdNotFound` | SecretId 不存在或已禁用 | 检查 `echo $TENCENTCLOUD_SECRET_ID` 是否正确 |
| `AuthFailure.SignatureFailure` | 签名计算失败 | 检查 SecretKey 是否正确，系统时间是否同步 |
| `AuthFailure.TokenFailure` | 临时凭证失效 | 如使用 STS Token，检查是否过期 |

### 服务角色授权失败

当 API 返回服务角色授权相关错误（如 `UnauthorizedOperation.ServiceLinkedRoleNotExist` 或错误信息包含"服务角色"/"service linked role"关键字）时，说明当前账号尚未开通 APM MCP 所需的服务关联角色。

**处理步骤**：

1. 向用户展示以下引导信息：

---

⚠️ **服务角色授权未开通**

当前账号尚未授权 APM MCP 所需的服务关联角色，需前往控制台完成一次性授权：

👉 [点击前往授权页面](https://console.cloud.tencent.com/cam/role/grant?roleName=APM_QCSLinkedRoleInApmMcp&serviceLinkedRole=1)

授权完成后告知，即可重新执行操作。

---

2. 用户确认授权完成后，重新执行之前失败的命令。

### 网络问题

| 现象 | 原因 | 解决方案 |
|------|------|----------|
| `ConnectionError` | 无法连接 Endpoint | 检查网络，确认 Endpoint 是否可达 |
| `Timeout` | 请求超时 | 网络延迟过高或服务端繁忙，稍后重试 |
| SSL 错误 | 证书问题 | 检查系统 CA 证书是否完整 |

### 参数错误

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| `InvalidParameter` | Method 值不合法 | 只允许 `tools/list`、`tools/call`、`ping` |
| `MissingParameter` | 缺少必填参数 | `tools/call` 时必须提供 `ToolName` |

## 排错命令

```bash
# 查看最近的错误
tail -20 logs/apm_error.log

# 按错误码搜索
grep "AuthFailure" logs/apm_error.log

# 按 RequestId 搜索
grep "eac6b301" logs/apm_error.log

# 按工具名搜索
grep "DescribeApmOverview" logs/apm_error.log
```

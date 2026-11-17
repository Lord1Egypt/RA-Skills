# 故障排查指南

## 常见错误码

错误码因提供商不同可能略有出入，仅供参考。

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| **401** | API Key 不正确 | 前往模型提供商检查写入的 API Key 是否正确 |
| **403** | 该模型不支持此服务器地域 | 更换服务器地域为模型支持的地域或更换模型 |
| **404** | Base URL 不对 | 查看提供商文档寻找兼容 OpenAI Chat Completions API 或 Anthropic Messages API 的 base URL 地址 |
| **429** | 速率限制 (Rate Limit) | 更换提供商，或联系提供商获取更大配额 |
| **500** | 服务器内部错误 | 1. 余额不足，充值或检查 API Key<br>2. 提供商服务异常，稍后重试<br>3. 请求参数错误，检查模型配置 |
| **503** | 服务不可用 | 1. 提供商服务器维护或过载<br>2. 网络连接问题<br>3. 切换到 Fallback 模型<br>4. 稍后重试 |
| **rate_limit** | 速率限制 | 更换提供商，或联系提供商获取更大配额 |

---

## 名词释义

- **RPM (Requests Per Minute)**：每分钟请求数
- **TPM (Tokens Per Minute)**：每分钟处理的 Tokens 数量

---

## 常见问题

### 1. 模型回复慢（响应慢）

**原因：**
- 若您选择的轻量应用服务器为境外地域且使用境内通道/模型提供商，可能会因跨境网络原因导致延迟较高
- 若您选择深度思考模型，可能因上下文过多导致模型思考时间过长

**解决方案：**
- 更换服务器地域
- 推荐您选择非思考模型/快思考模型进行替代

---

### 2. Token 消耗过快

**原因：**
OpenClaw 在调用模型时会携带较多上下文信息，以保证任务连贯性与准确性，因此 Token 消耗可能较高。

**解决方案：**
- 建议在使用时关注 Token 用量与计费情况
- 使用 ClawAPI Manager 的智能路由功能，自动选择免费/低成本模型
- 配置 Fallback 链，优先使用低成本模型

---

## ClawAPI Manager 相关问题

### 1. 协议不匹配

**症状：**
- 404 错误
- 模型无法调用

**原因：**
- Provider 的协议类型（`api` 字段）配置错误
- 第三方 API 中转服务协议不匹配

**解决方案：**
```bash
# 查看当前协议
./clawapi providers

# 设置正确的协议
# Anthropic Messages API
python3 -c "from clawapi_helper import *; print(set_protocol_interactive('xart', 'anthropic-messages'))"

# OpenAI Chat Completions
python3 -c "from clawapi_helper import *; print(set_protocol_interactive('openai', 'openai-chat'))"

# OpenAI Compatible (默认)
python3 -c "from clawapi_helper import *; print(set_protocol_interactive('provider', 'openai-compatible'))"
```

---

### 2. 配置文件损坏

**症状：**
- ClawAPI Manager 无法启动
- JSON 解析错误

**解决方案：**
```bash
# 查看备份
ls ~/.openclaw/backups/

# 恢复备份
cp ~/.openclaw/backups/openclaw_20260303_020000.json ~/.openclaw/openclaw.json

# 重启 Gateway
openclaw gateway restart
```

---

### 3. API Key 失效

**症状：**
- 401 错误
- 认证失败

**解决方案：**
```bash
# 更新 API Key
python3 -c "from clawapi_helper import *; manager.update_api_key('provider_name', 'new_key')"

# 或使用 TUI
python3 clawapi-tui.py
# 进入 Models 标签 → 选择 provider → Update Key
```

---

## 获取帮助

- GitHub Issues: https://github.com/2233admin/clawapi-manager/issues
- OpenClaw Discord: https://discord.com/invite/clawd
- ClawHub: https://clawhub.com

---

## 错误码详解

### 500 Internal Server Error

**常见原因：**
1. **余额不足**：API Key 对应账户余额为 0
2. **服务器异常**：提供商服务器内部错误
3. **请求参数错误**：模型 ID、参数配置不正确
4. **超时**：请求处理时间过长

**排查步骤：**
```bash
# 1. 检查余额
# 登录提供商控制台查看余额

# 2. 检查 API Key
python3 -c "from clawapi_helper import *; print(show_providers())"

# 3. 测试连通性
./clawapi test provider_name

# 4. 查看日志
tail -f ~/.openclaw/logs/gateway.log
```

**解决方案：**
- 充值余额
- 更换 API Key
- 检查模型配置
- 切换到 Fallback 模型

---

### 503 Service Unavailable

**常见原因：**
1. **服务器维护**：提供商正在维护
2. **服务器过载**：请求量过大，服务器无法处理
3. **网络问题**：网络连接不稳定
4. **地域限制**：服务器地域不支持

**排查步骤：**
```bash
# 1. 检查网络连通性
curl -I https://api.provider.com

# 2. 查看提供商状态页
# 访问提供商官网查看服务状态

# 3. 测试其他 provider
./clawapi providers
./clawapi test another_provider

# 4. 检查 Fallback 配置
python3 -c "from clawapi_helper import *; print(show_status())"
```

**解决方案：**
- 等待服务恢复（通常 5-30 分钟）
- 切换到其他 provider
- 配置 Fallback 链自动切换
- 更换服务器地域

---

### 自动 Fallback 配置

当主模型返回 500/503 错误时，自动切换到备用模型：

```bash
# 查看当前 Fallback 链
python3 -c "from clawapi_helper import *; print(show_status())"

# 添加 Fallback
python3 -c "from clawapi_helper import *; manager.add_fallback('provider/model-id')"

# 示例：配置三层 Fallback
# 主模型：aiclauder/claude-opus-4-6
# Fallback 1：volcengine/doubao-seed-2.0-code
# Fallback 2：openrouter/qwen-2.5-coder-32b-instruct:free
```

**推荐配置：**
- 主模型：高性能付费模型
- Fallback 1：中等性能付费模型
- Fallback 2：免费模型（保底）


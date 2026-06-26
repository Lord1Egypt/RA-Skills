# Call AIDA App 技能 - 快速开始

## 📋 概述

`call-aida-app` 是一个 OpenClaw 通用技能，用于直接调用 AI 搭（AIDA）现有应用。

**主要功能：**
- ✅ 根据 `appid` 和 `inputs` 调用 AIDA API
- ✅ 返回应用的完整响应数据
- ✅ 支持多种参数传入方式
- ✅ 完整的错误处理和日志记录

## 🚀 快速使用

### 1. 直接通过命令行调用

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "your-app-id" \
  --inputs '{"key": "value"}'
```

### 2. 通过环境变量调用

```bash
export AIDA_APPID="your-app-id"
export AIDA_INPUTS='{"key": "value"}'
export AIDA_QUERY="optional query"
export AIDA_USER="your-username"

python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

### 3. 通过 stdin 调用（推荐用于 OpenClaw 集成）

```bash
echo '{
  "appid": "your-app-id",
  "inputs": {"key": "value"},
  "query": "optional query"
}' | python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

## 📝 参数说明

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| **appid** | string | ✓ | AI 搭应用的唯一标识符（作为 Bearer Token 使用） |
| **inputs** | object | ✓ | 传递给应用的输入参数（JSON 格式） |
| **query** | string | ✗ | 用户查询文本（可选） |
| **user** | string | ✗ | 用户标识，默认为 "openclaw" |

## 📤 返回格式

### 成功响应

```json
{
  "success": true,
  "message": "调用成功",
  "data": {
    "result": "应用返回的数据"
  },
  "raw_answer": "原始答案文本"
}
```

### 失败响应

```json
{
  "success": false,
  "message": "错误信息描述",
  "data": null
}
```

## 🔧 在 OpenClaw Agent 中集成

### 方法 1：直接调用

```yaml
# 在 Agent 的工具定义中
tools:
  call_aida_app:
    description: "调用 AI 搭应用"
    parameters:
      appid:
        type: string
        description: "应用 ID"
      inputs:
        type: object
        description: "输入参数"
```

### 方法 2：通过 openclaw.json 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "tools": {
    "call_aida_app": {
      "type": "python",
      "command": "python3",
      "script": "~/.openclaw/skills/call-aida-app/call_aida_app.py",
      "stdin_mode": true,
      "description": "调用 AI 搭现有应用"
    }
  }
}
```

## 💡 实际使用示例

### 示例 1：调用文档分析应用

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "doc-analyzer-app" \
  --inputs '{
    "document": "这是一份需要分析的文档",
    "analysis_type": "summary"
  }'
```

预期返回：
```json
{
  "success": true,
  "message": "调用成功",
  "data": {
    "summary": "文档摘要内容...",
    "key_points": ["要点1", "要点2"]
  }
}
```

### 示例 2：在 OpenClaw Agent 中使用

在 Agent 的任务中调用：

```
使用 call_aida_app 工具调用 "report-generator" 应用，
传入参数：{"report_type": "monthly", "department": "sales"}
```

## 🐛 故障排除

### 问题 1：HTTP 401 错误

**症状：** `"API密钥校验失败"`

**解决方案：**
- 检查 `appid` 是否正确
- 确保 appid 对应的 AIDA 应用已被激活
- 验证网络连接

### 问题 2：缺少 answer 字段

**症状：** `"响应中未找到 answer 字段"`

**解决方案：**
- 检查 AIDA 应用是否正常工作
- 查看 `data` 字段中的完整响应信息
- 确认 `inputs` 参数格式正确

### 问题 3：超时错误

**症状：** 脚本执行无响应或超时

**解决方案：**
- 默认超时时间为 120 秒
- 检查网络连接
- 检查 AIDA 服务是否正常
- 可修改脚本中的 `timeout=120` 参数

### 问题 4：JSON 解析错误

**症状：** 返回的 `raw_answer` 看起来不是 JSON

**解决方案：**
- 这是正常的，表示应用返回了纯文本
- `data` 字段会包含 `{"answer": "纯文本内容"}`

## 📚 技能文件位置

```
~/.openclaw/skills/call-aida-app/
├── SKILL.md              # 完整文档
├── README.zh.md          # 本文件（中文快速指南）
├── call_aida_app.py      # 主要脚本
└── README.md             # 英文文档（如有）
```

## 🔗 相关资源

- **AIDA API 文档：** https://aida.vip.sankuai.com
- **OpenClaw 官方文档：** https://openclaw.io
- **技能开发指南：** 参考 `SKILL.md`

## ⚙️ 技术细节

- **API 端点：** `https://aida.vip.sankuai.com/v1/chat-messages`
- **认证方式：** Bearer Token
- **请求超时：** 120 秒
- **响应模式：** Blocking（阻塞）
- **支持的 Python 版本：** 3.6+
- **依赖：** 仅使用 Python 标准库

## 📞 获取帮助

查看完整文档：

```bash
cat ~/.openclaw/skills/call-aida-app/SKILL.md
```

查看脚本帮助：

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py --help
```

## 📄 许可

MIT License

---

**最后更新：** 2026-03-14
**版本：** 1.0.0


# 🦞 从这里开始！

欢迎使用 **Call AIDA App** OpenClaw 技能。这个文件将引导你快速上手。

## ⚡ 30 秒快速开始

### 1. 查看帮助
```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py --help
```

### 2. 第一次调用
```bash
echo '{"appid":"your-app-id","inputs":{"test":"value"}}' | \
  python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

### 3. 查看结果
结果将以 JSON 格式返回，包含 `success`、`message` 和 `data` 字段。

## 📚 文档地图

根据你的使用情况选择合适的文档：

### 🎯 快速参考（5分钟）
**文件:** `QUICKSTART.txt`
```bash
cat ~/.openclaw/skills/call-aida-app/QUICKSTART.txt
```
快速参考卡，包含常用命令和参数。

### 🚀 快速指南（10分钟）
**文件:** `README.zh.md`
```bash
cat ~/.openclaw/skills/call-aida-app/README.zh.md
```
中文快速开始，涵盖基本使用和三种调用方式。

### 📖 完整文档（20分钟）
**文件:** `SKILL.md`
```bash
cat ~/.openclaw/skills/call-aida-app/SKILL.md
```
详细的 API 文档、参数说明和完整功能描述。

### 💡 实际示例（15分钟）
**文件:** `EXAMPLES.md`
```bash
cat ~/.openclaw/skills/call-aida-app/EXAMPLES.md
```
包含基础、进阶和集成示例。

### 🔍 文档索引
**文件:** `INDEX.md`
```bash
cat ~/.openclaw/skills/call-aida-app/INDEX.md
```
完整的文档结构和导航指南。

## 🎓 推荐学习路径

### 路径 1：我想快速上手（15分钟）
1. 阅读 `QUICKSTART.txt`
2. 尝试第一次调用
3. 参考 `README.zh.md` 了解更多

### 路径 2：我想充分理解（50分钟）
1. 阅读 `QUICKSTART.txt`
2. 阅读 `README.zh.md`
3. 浏览 `EXAMPLES.md`
4. 参考 `SKILL.md`

### 路径 3：我要集成到代码（30分钟）
1. 阅读 `README.zh.md` "在 OpenClaw 中使用"
2. 参考 `EXAMPLES.md` "与 OpenClaw Agent 集成"
3. 参考 `EXAMPLES.md` "Python 中的错误处理"

### 路径 4：我要解决问题（10分钟）
1. 查看 `SKILL.md` "常见问题"
2. 查看 `EXAMPLES.md` "错误处理示例"

## 🔧 基本概念

### 什么是这个技能？
这个技能是一个 OpenClaw 工具，用于调用 AI 搭（AIDA）现有应用，并返回应用返回的数据。

### 功能
- 📤 调用 AIDA chat-messages API
- 📥 返回完整的应用响应数据
- 🔐 支持 Bearer Token 认证
- ⚠️ 完整的错误处理

### 三种调用方式

#### 方式 1：命令行参数（简单）
```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "my-app" \
  --inputs '{"key":"value"}'
```

#### 方式 2：stdin JSON（推荐）
```bash
echo '{"appid":"my-app","inputs":{"key":"value"}}' | \
  python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

#### 方式 3：环境变量（CI/CD）
```bash
export AIDA_APPID="my-app"
export AIDA_INPUTS='{"key":"value"}'
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

## ✅ 验证安装

运行测试脚本确保一切正常：

```bash
bash ~/.openclaw/skills/call-aida-app/test.sh
```

如果所有测试都通过，说明安装成功！

## 🎯 常见任务

### 任务 1：调用一个 AIDA 应用

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "document-analyzer" \
  --inputs '{"document":"content here"}'
```

→ 详细说明见 `README.zh.md` 方式 2

### 任务 2：在 Python 中使用

```python
import json
import subprocess

payload = {
    "appid": "my-app",
    "inputs": {"key": "value"}
}

result = subprocess.run(
    ["python3", "~/.openclaw/skills/call-aida-app/call_aida_app.py"],
    input=json.dumps(payload),
    capture_output=True,
    text=True
)

response = json.loads(result.stdout)
print(response)
```

→ 详细说明见 `EXAMPLES.md` "Python 集成"

### 任务 3：在 OpenClaw Agent 中使用

将此技能作为 Agent 的工具：

```yaml
tools:
  call_aida_app:
    command: "python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py"
    input_mode: "stdin"
```

→ 详细说明见 `EXAMPLES.md` "与 OpenClaw Agent 集成"

## ❓ 常见问题

### Q: 如何获取 appid？
A: appid 是 AI 搭应用的唯一标识符，可以从 AI 搭应用管理界面获取。

### Q: 支持哪些 Python 版本？
A: Python 3.6+ (仅使用标准库)

### Q: 是否需要安装依赖？
A: 不需要！完全使用 Python 标准库。

### Q: 响应超时是多久？
A: 默认 120 秒。

### Q: 如何处理错误？
A: 查看 `EXAMPLES.md` 中的错误处理示例。

→ 更多问题见 `SKILL.md` "常见问题"

## 🐛 遇到问题？

### 问题 1：HTTP 401 错误
- 检查 appid 是否正确
- 确保应用已激活
→ 详细见 `SKILL.md` "故障排除"

### 问题 2：缺少 answer 字段
- 检查输入参数
- 查看完整响应数据
→ 详细见 `SKILL.md` "故障排除"

### 问题 3：其他错误
- 运行 `test.sh` 验证安装
- 查看 `SKILL.md` 故障排除部分

## 📞 需要帮助？

### 快速查询
1. **查看文档:** `cat QUICKSTART.txt`
2. **查看示例:** `cat EXAMPLES.md`
3. **查看帮助:** `python3 call_aida_app.py --help`
4. **运行测试:** `bash test.sh`

### 查阅完整文档
```bash
# 快速参考（5分钟）
cat ~/.openclaw/skills/call-aida-app/QUICKSTART.txt

# 中文指南（10分钟）
cat ~/.openclaw/skills/call-aida-app/README.zh.md

# 完整文档（20分钟）
cat ~/.openclaw/skills/call-aida-app/SKILL.md

# 使用示例（15分钟）
cat ~/.openclaw/skills/call-aida-app/EXAMPLES.md

# 文档索引（查找任何内容）
cat ~/.openclaw/skills/call-aida-app/INDEX.md
```

## 🚀 下一步

### 现在开始
1. ✅ 你已经阅读了 `00-START-HERE.md`
2. ⏭️ 接下来，选择适合你的文档
   - 快速上手？→ 读 `QUICKSTART.txt`
   - 想学习？→ 读 `README.zh.md`
   - 要集成？→ 读 `EXAMPLES.md`
3. 🎯 尝试第一次调用
4. 📚 参考文档进行更复杂的操作

## 📋 文件速查表

| 文件 | 内容 | 阅读时间 |
|------|------|--------|
| `00-START-HERE.md` | 本文件，入门指南 | 5分钟 |
| `QUICKSTART.txt` | 快速参考卡 | 5分钟 |
| `README.zh.md` | 中文快速指南 | 10分钟 |
| `SKILL.md` | 完整 API 文档 | 20分钟 |
| `EXAMPLES.md` | 详细使用示例 | 15分钟 |
| `INDEX.md` | 文档索引 | 按需查阅 |
| `call_aida_app.py` | 主要脚本 | 代码阅读 |
| `install.sh` | 安装脚本 | 可执行 |
| `test.sh` | 测试脚本 | 可执行 |

## 💝 致谢

感谢使用 Call AIDA App 技能！

---

**版本:** 1.0.0
**位置:** `~/.openclaw/skills/call-aida-app/`
**许可:** MIT

🦞 Happy coding with OpenClaw!


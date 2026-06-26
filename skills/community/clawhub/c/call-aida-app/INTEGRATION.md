# 在 OpenClaw 中集成 Call AIDA App 技能

## ✅ 技能状态

技能已创建并测试完成，位置：`~/.openclaw/skills/call-aida-app/`

## 🎯 如何在 OpenClaw 中使用

### 方式 1：直接从 Shell 调用（最直接）

```bash
echo '{"appid":"your-app-id","inputs":{"key":"value"}}' | \
  python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

### 方式 2：在 OpenClaw Agent 中作为外部工具

虽然这个技能不是 Agent 的内置工具，但可以通过以下方式集成：

1. **创建一个 Bash 包装脚本**（可选）

```bash
#!/bin/bash
# ~/.openclaw/tools/call-aida
exec python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py "$@"
```

2. **从 Agent 代码中调用**

```bash
# 在需要调用 AIDA 应用的地方
echo '{"appid":"app-id","inputs":{}}' | \
  ~/.openclaw/tools/call-aida
```

### 方式 3：Python 中使用

```python
import json
import subprocess

def call_aida_app(appid, inputs, query=""):
    payload = {
        "appid": appid,
        "inputs": inputs,
        "query": query
    }

    result = subprocess.run(
        ["python3", "~/.openclaw/skills/call-aida-app/call_aida_app.py"],
        input=json.dumps(payload),
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

# 使用
response = call_aida_app("my-app", {"data": "test"})
print(response)
```

## 📌 关键点

- ✅ 技能已验证正常工作
- ✅ 使用 stdin JSON 方式是最灵活的
- ✅ 需要有效的 AIDA appid 才能成功调用
- ✅ 所有参数都需要通过 JSON 传入

## 🔗 相关文档

- 快速开始：`cat ~/.openclaw/skills/call-aida-app/00-START-HERE.md`
- 完整文档：`cat ~/.openclaw/skills/call-aida-app/SKILL.md`
- 使用示例：`cat ~/.openclaw/skills/call-aida-app/EXAMPLES.md`

## 🚀 验证技能工作

运行测试脚本：
```bash
bash ~/.openclaw/skills/call-aida-app/test.sh
```

直接测试：
```bash
echo '{"appid":"test","inputs":{}}' | \
  python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

预期输出包含 `success` 和 `message` 字段。


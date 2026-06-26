---
name: "configure-file-write-and-recovery"
description: "如何在网关重启后保持配置文件的修改。TRIGGER 当用户提到配置文件写入、网关重启、配置文件还原、模型添加、多模型配置、配置管理机制、自动还原等问题时。"
---

# 配置文件写入后被还原

本技能帮助你在网关重启后保持配置文件的修改，确保多模型配置不会被还原。

## 当使用此技能时
- 当你需要在网关重启后保持配置文件的修改时
- 当你遇到配置文件写入后被还原的问题时
- 当你需要添加多个模型到配置文件中时
- 当你需要了解配置管理机制和自动还原的原因时

## 步骤
1. 尝试使用 `write` 工具写入配置文件
   - 为什么：`write` 工具是常见的文件写入工具，但可能不适用于某些特定环境。
2. 尝试使用 `exec cat heredoc` 命令写入配置文件
   - 为什么：`exec cat heredoc` 命令可以确保文件内容一次性写入，但同样可能不适用于某些特定环境。
3. 使用 Python 脚本通过 `exec` 命令写入配置文件
   - 为什么：Python 脚本可以提供更灵活的文件写入方式，并且可以确保内容一次性写入。
4. 重启网关后检查配置文件
   - 为什么：验证配置文件是否在网关重启后保持修改。
5. 查询模型在 API 中的实际 ID
   - 为什么：确保写入的模型 ID 是有效的，避免因非法参数导致配置文件被还原。
6. 使用正确的 API ID 重新写入配置文件
   - 为什么：使用有效的模型 ID 可以通过配置验证，避免配置文件被还原。
7. 重启网关后再次检查配置文件
   - 为什么：进一步验证配置文件是否在网关重启后保持修改。

## 坑点及解决方案
❌ 错误方法：使用 `write` 工具或 `exec cat heredoc` 命令写入配置文件，显示成功但检查时发现配置文件内容未改变。
- 为什么失败：这些方法可能不适用于某些特定环境，导致写入操作看似成功但实际上未生效。
- ✅ 正确方法：使用 Python 脚本通过 `exec` 命令写入配置文件，确保内容一次性写入并验证通过。

❌ 错误方法：使用用户提供的模型名称写入配置文件，导致配置文件在网关重启后被还原。
- 为什么失败：用户提供的模型名称可能不是 API 中的实际 ID，导致配置验证失败，系统自动还原配置文件。
- ✅ 正确方法：查询模型在 API 中的实际 ID，并使用这些 ID 重新写入配置文件，确保配置验证通过。

## 关键代码和配置
```python
# Python 脚本写入配置文件
import subprocess

config_content = """
model1: doubao-seed-2-0-lite-260215
model2: doubao-seed-2-0-pro-260215
model3: doubao-seed-2-0-mini-260215
model4: doubao-seedance-2-0-260128
model5: doubao-seedance-2-0-fast-260128
model6: doubao-seedance-1-5-pro-251215
model7: doubao-seedream-5-0-260128
model8: doubao-embedding-vision-251215
model9: kimi-k2-250905
model10: glm-4-7-251222
model11: deepseek-v3-2-251201
model12: minimax-m2.7
"""

with open('/path/to/config/file', 'w') as f:
    f.write(config_content)

subprocess.run(['exec', 'cat', '/path/to/config/file'])
```

## 环境和前提条件
- Python 3.x
- 网关设备
- 配置文件路径：`/path/to/config/file`
- API 访问权限
- 确保网关设备允许通过 `exec` 命令写入配置文件

## 伴随文件
- `scripts/write_config.py` — 使用 Python 脚本写入配置文件的完整脚本
- `references/model_id_mapping.txt` — 用户提供的模型名称与实际 API ID 的映射表

<!-- metadata: {{"openclaw": {{"emoji": "🛠️"}}}} -->

## Companion files

- `scripts/write_config.py` — automation script
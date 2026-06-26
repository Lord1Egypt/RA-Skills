# CLI-VSCode SKILL.md

**Version**: 1.0.0  
**Type**: CLI Tool  
**Interface**: Command Line + JSON  

---

## Description

CLI-VSCode 是 VSCode 的命令行接口，让 AI Agent 可以直接操作 VSCode。

支持功能：
- 打开文件/VSCode
- 安装/列出扩展
- 管理工作区
- 状态检查

---

## Installation

确保 VSCode 已安装并且 `code` 命令行工具可用。

### macOS
在 VSCode 中按 `Cmd+Shift+P`，输入 "Shell Command: Install 'code' command in PATH"

### Windows
VSCode 安装时勾选 "Add to PATH"

### Linux
```bash
sudo ln -s /usr/share/code/bin/code /usr/local/bin/code
```

---

## Commands

```bash
# 打开文件
python cli-vscode.py open ./src/main.py

# 安装扩展
python cli-vscode.py install-extension --id esbenp.prettier-vscode

# 列出扩展
python cli-vscode.py list-extensions

# 添加到工作区
python cli-vscode.py add-folder ./tests

# 检查状态
python cli-vscode.py status

# JSON 输出 (Agent 使用)
python cli-vscode.py --json list-extensions
```

---

## JSON Schema

### List Extensions Response
```json
{
  "extensions": [
    "esbenp.prettier-vscode",
    "ms-python.python",
    "GitHub.copilot"
  ]
}
```

### Status Response
```json
{
  "installed": true,
  "version": "1.88.0"
}
```

---

## Agent Integration

### OpenClaw
```yaml
skill: cli-vscode
type: cli
commands:
  - open
  - install-extension
  - list-extensions
  - add-folder
  - status
```

---

## Limitations

- 需要 VSCode 已安装
- 需要 code 命令行工具在 PATH 中
- 不支持编辑文件内容（仅打开）

---

## License

MIT License (个人使用)  
商业许可需单独购买

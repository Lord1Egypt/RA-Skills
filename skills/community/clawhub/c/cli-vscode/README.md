# CLI-VSCode 🚀

**让 AI Agent 直接操作 VSCode**

## 快速开始

```bash
# 打开文件
python cli-vscode.py open ./src/main.py

# 安装扩展
python cli-vscode.py install-extension esbenp.prettier-vscode

# 列出扩展
python cli-vscode.py list-extensions

# 添加到工作区
python cli-vscode.py add-folder ./tests

# JSON 输出 (Agent 使用)
python cli-vscode.py --json list-extensions
```

## 功能

- ✅ 打开文件/VSCode
- ✅ 安装/列出扩展
- ✅ 管理工作区
- ✅ JSON 输出 (AI Agent 集成)

## 价格

- 早鸟价：¥48 (前 20 名)
- 正常价：¥68

## 系统要求

- VSCode 已安装
- code 命令行工具可用

## 安装 code 命令行工具

### macOS
1. 打开 VSCode
2. 按 `Cmd+Shift+P`
3. 输入 "Shell Command: Install 'code' command in PATH"

### Windows
VSCode 安装时勾选 "Add to PATH" 选项

### Linux
```bash
sudo ln -s /usr/share/code/bin/code /usr/local/bin/code
```

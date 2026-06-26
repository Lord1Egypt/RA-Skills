# Flexible Web Tester

智能 Web UI 测试工作台，支持 MCP 直接驱动和 Python 脚本驱动双模式。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Platform](https://img.shields.io/badge/platform-OpenClaw-lightgrey.svg)

---

## ✨ 功能特性

- **双模式驱动**：MCP 直接驱动（AI 操作浏览器）或 Python 脚本驱动（生成代码执行）
- **三种测试模式**：自由探索 / 需求驱动 / 用例驱动
- **强制人工确认**：测试执行前必须用户确认，安全可控
- **环境自检**：自动检测 MCP 工具是否就绪
- **自动落盘**：测试方案和报告自动保存到本地
- **自愈机制**：遇到错误自动重试，最多 2 次

---

## 🔧 环境要求

使用本技能前，请确保已配置以下 MCP 服务：

| MCP 服务 | 用途 |
|---------|------|
| File System MCP | 读写测试用例和报告 |
| CLI / Terminal MCP | 执行 Python 脚本 |
| Playwright MCP | 控制浏览器操作 |

---

## 🚀 快速开始

### 1. 配置 MCP

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### 2. 启动测试

告诉 AI：

> 测试 https://example.com，模式2，引擎A，人工介入

### 3. 等待确认

AI 生成测试方案后，回复「确认」开始执行。

---

## 📖 使用示例

### 示例 1：测试百度首页

```
测试 https://www.baidu.com，模式2，引擎A，人工介入
```

### 示例 2：测试登录流程

```
测试 https://example.com/login，模式3，引擎B，自动填写，用户名 test 密码 123456
```

---

## 📁 输出文件

- `{YYYYMMDD}_测试用例.md` - 测试方案（引擎A）
- `{YYYYMMDD}_测试脚本.py` - 测试脚本（引擎B）
- `{YYYYMMDD}_测试报告.md` - 测试报告

---

## 📋 测试模式说明

| 模式 | 说明 |
|------|------|
| 自由探索 | AI 自主漫游找问题 |
| 需求驱动 | 给需求，AI 生成测试用例 |
| 用例驱动 | 直接给测试步骤执行 |

---

## ⚙️ 执行引擎

| 引擎 | 说明 |
|------|------|
| MCP 直接驱动 | AI 直接调用浏览器操作 |
| Python 脚本驱动 | 生成 Playwright 脚本执行 |

---

## 📄 License

MIT License

---

*由 OpenClaw AI Assistant 生成*

# Changelog

## [2.5.2] - 2026-03-15

### 📝 Documentation
- 澄清安全说明：脚本本身无网络访问
- 说明在 agent 环境中可能通过 MCP 进行网络操作

---

## [2.5.1] - 2026-03-15

### 🔧 Cleanup
- 删除 package-lock.json 和 node_modules
- 移除 README 中的 npm install 说明
- 确保无外部依赖

---

## [2.5.0] - 2026-03-15

### ✨ Features
- 改写提示词增加去 AI 味要求
- 口语化、真实细节、避免 AI 连接词

### 🔒 Security
- 移除 .env 文件读取
- 移除 dotenv 依赖
- 仅读取必要环境变量（XHS_MAX_RESULTS）

---

## [2.4.1] - 2026-03-15
- 📝 说明 MCP 支持

## [2.4.0] - 2026-03-15
- 🔥 极简实现

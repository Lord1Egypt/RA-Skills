# Claude Code Assist — 一键环境检测与多 Provider 配置

> 国内开发者用 Claude Code 接第三方 API 的完整上车向导。3 分钟从 0 到跑通。

## ✨ 功能

| Phase | 名称 | 说明 |
|---|---|---|
| 🔍 Phase 1 | 环境体检 | 自动检测 Node.js / npm / Git / Claude Code CLI |
| 📦 Phase 2 | 安装引导 | Win / Mac / Linux 三平台安装命令 |
| 🔧 Phase 3 | Provider 选择 | 10 个国内可用 Provider，一键匹配配置 |
| ⚙️ Phase 4 | 配置写入 | 环境变量或 settings.local.json |
| ✅ Phase 5 | 验证 | 跑通 Claude Code 并确认 Provider 生效 |

## 🚀 快速开始

### 安装

```bash
openclaw skills install claude-code-assist
```

### 使用

直接说你想干嘛：

- "帮我配置 Claude Code 接 DeepSeek"
- "Claude Code 怎么在国内用"
- "我想用 Claude Code + Kimi"

Skill 会自动检测你的环境、引导安装、帮你选 Provider、写入配置。

## 🔧 支持的 Provider (10 个)

| Provider | 特点 |
|---|---|
| **DeepSeek** ⭐ | 1M 上下文，V4 Pro 推理，性价比最高 |
| **Kimi** | 1M 上下文，kimi-k2 |
| **Qwen** | 阿里通义千问，企业级 |
| **SiliconFlow** | 多模型聚合，免费额度 |
| **OpenRouter** | 国际多模型聚合 |
| **ModelScope** | 阿里魔搭 |
| **Baichuan** | 百川 |
| **GLM** | 智谱 GLM-5v 200K |
| **豆包** | 字节跳动 |
| **自定义** | 自己输入 base URL 和认证方式 |

## 🐛 排坑

内置 10 个常见问题的排查方案：
- 401 Unauthorized（AUTH_TOKEN vs API_KEY 搞混）
- 上下文 1M → 64K（`[1m]` 后缀没加）
- WSL2 配置路径错误
- 已有 Anthropic 登录时配置冲突
- npm 全局安装失败（Windows）
- 等等

## 📁 文件结构

```
claude-code-assist/
├── SKILL.md                         # 主文件 (v1.0.0)
├── README.md                        # 本文件
├── CHANGELOG.md                     # 更新日志
├── LICENSE                          # MIT
└── references/
    ├── provider-table.md             # 10 个 Provider 完整配置表
    ├── troubleshooting.md           # 10 个常见问题排坑方案
    └── install-guide.md             # Win/Mac/Linux 三平台安装指南
```

## 📄 License

[MIT](LICENSE) — Copyright (c) 2026 sallyface0

## 📝 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

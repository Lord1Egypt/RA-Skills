# feishu-multiagent-onboard

飞书多 Agent 快速配置工具 - 一键完成 OpenClaw 多 Agent 飞书通道配置

## 功能特性

- ✅ 交互式配置向导
- ✅ 自动验证配置格式
- ✅ 故障诊断工具
- ✅ 完整文档和最佳实践
- ✅ 支持 1-N 个 Agent 配置

## 快速开始

### 安装

```bash
# 方法 1: 克隆仓库
git clone https://github.com/YOUR_USERNAME/feishu-multiagent-onboard.git
cp -r feishu-multiagent-onboard ~/.openclaw/skills/

# 方法 2: 通过 ClawHub (即将上线)
openclaw skills install feishu-multiagent-onboard
```

### 使用

```bash
# 配置向导
openclaw skills run feishu-multiagent-onboard

# 验证配置
openclaw skills run feishu-multiagent-onboard --check

# 故障诊断
openclaw skills run feishu-multiagent-onboard --debug

# 查看帮助
openclaw skills run feishu-multiagent-onboard --help
```

## 配置示例

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "writer": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        },
        "media": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "writer",
      "match": { "channel": "feishu", "accountId": "writer" }
    },
    {
      "agentId": "media",
      "match": { "channel": "feishu", "accountId": "media" }
    }
  ]
}
```

## 完整文档

- [配置指南](docs/guide.md)
- [常见问题](docs/faq.md)

## 系统要求

- OpenClaw 2026.3.2+
- Node.js 22+
- 飞书开放平台账号

## 项目结构

```
feishu-multiagent-onboard/
├── index.js              # 主程序
├── SKILL.md              # Skill 描述
├── README.md             # 项目说明
├── templates/
│   └── openclaw.json.example  # 配置模板
└── docs/
    ├── guide.md          # 配置指南
    └── faq.md            # 常见问题
```

## 作者

墨墨 (OpenClaw 多 Agent 实践者)

## 许可证

MIT

## 更新日志

### v1.0.0 (2026-03-07)

- 初始版本
- 交互式配置向导
- 配置验证工具
- 故障诊断工具
- 完整文档

# 🤖 飞书机器人配置助手 - 技能文档

**版本**: v1.0.0  
**类型**: 飞书机器人自动配置  
**难度**: ⭐⭐⭐⭐

---

## 📋 技能概述

在飞书对话中直接配置新机器人，自动完成 Agent 创建、工作空间配置、Gateway 重启。

---

## 🎯 核心能力

- ✅ 飞书机器人自动配置
- ✅ 智能 Agent 匹配（7 种规则）
- ✅ 自动更新 openclaw.json
- ✅ 自动重启 Gateway
- ✅ 返回配置报告

---

## 🚀 安装方式

### Mac / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/jiebao360/feishu-bot-config-helper/main/install.sh | bash
```

### Windows
```powershell
curl -fsSL https://raw.githubusercontent.com/jiebao360/feishu-bot-config-helper/main/install.bat -o install.bat
.\install.bat
```

---

## 🎭 Agent 阵容

| Agent | 职责 | 默认模型 |
|-------|------|----------|
| 第二大脑笔记虾 | 知识管理 + 素材提供 | doubao-pro |
| 朋友圈创作虾 | 朋友圈文案创作 | doubao |
| 电商视频导演虾 | 电商视频脚本 | doubao-pro |
| 通用内容创作虾 | 通用内容创作 | doubao |
| 图片素材生成虾 | 图片搜索 + 生成 | doubao-pro |
| 电商 Seedance 导演虾 | Seedance 提示词 | doubao-pro |
| 工作助手 | 工作相关任务 | doubao |

---

## ⚙️ 配置规范

严格遵循官方模板：
1. 每个飞书机器人对应一个独立 Agent
2. 拥有独立的工作空间和记忆
3. 在 `agents.list` 中定义 Agent
4. 在 `channels.feishu.accounts` 中配置机器人
5. 在 `bindings` 中添加路由绑定
6. 使用 `dmScope: "per-account-channel-peer"`
7. 群组策略使用 `groupPolicy: "open"`

---

## 📁 文件清单

```
feishu-bot-config-helper/
├── scripts/
│   └── auto-configure-bot.js      # 自动配置脚本
├── index.js                        # 主入口
├── install.sh                      # Mac/Linux 安装脚本
├── install.bat                     # Windows 安装脚本
├── package.json                    # 项目配置
├── SKILL.md                        # 技能文档
├── README.md                       # 使用说明
├── CHANGELOG.md                    # 更新日志
└── LICENSE                         # MIT 许可证
```

---

## 🔗 相关资源

- **GitHub**: https://github.com/jiebao360/feishu-bot-config-helper
- **OpenClaw 文档**: https://docs.openclaw.ai
- **飞书开放平台**: https://open.feishu.cn/

---

<div align="center">

**🦞 让龙虾成为你的飞书机器人配置助手！**

</div>

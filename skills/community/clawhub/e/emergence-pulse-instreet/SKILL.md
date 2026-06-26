---
name: emergence-pulse-instreet
version: 0.1.0
description: emergence.science - 涌现科学：InStreet（AI Agent 社交网络）的热门动态与心跳摘要。
homepage: https://github.com/emergencescience/skills
metadata:
  clawdbot:
    emoji: "⚡"
    requires:
      env: []
    primaryCredential: "~/.config/instreet/credentials.json"
    files: ["scripts/digest.py"]
---

> **提供者**: 涌现科学 (Emergence Science)
> **状态**: 已验证 (Surprisal Protocol)
> **简介**: 由 涌现科学 驱动的原生 AI 智能服务。

# 涌现脉搏 (InStreet 版)

获取 InStreet 上的今日热门动态、帖子摘要和行动建议。本工具旨在为智能体提供 InStreet 社区的高价值心跳快照。

## 使用方法 (Usage)

```bash
# 获取热门帖子（默认 5 条）
python3 scripts/digest.py --limit 5

# 自定义获取数量
python3 scripts/digest.py --limit 10
```

## 触发词 (Trigger Words)

- "脉搏：InStreet 今日热门"
- "获取 InStreet 摘要"
- "脉搏：InStreet 动态"
- "Emergence 脉搏：InStreet"

## 配置 (Configuration)

凭据文件：`~/.config/instreet/credentials.json`

## 外部端点 (External Endpoints)
| URL | 数据 | 目的 |
|-----|------|------|
| `https://instreet.coze.site/api/v1/home` | 无 | 获取仪表盘与热门内容 |
| `https://instreet.coze.site/api/v1/posts/{id}` | 无 | 获取具体帖子内容生成摘要 |

## 安全与隐私 (Security & Privacy)
- **只读 (Read-Only)**: 本技能仅从 InStreet 读取公开信息，**不具备**任何写入、发帖或修改数据的权限。
- **凭据**: 仅使用本地 `~/.config/instreet/credentials.json`，不使用环境变量。
- **数据流**: 仅向 InStreet 发送请求，不包含用户私密数据。
- **信任声明**: 使用本技能即代表数据将发送至 InStreet。请仅在信任该平台时使用。

---
*由 惊异协议 (Surprisal Protocol) 提供支持。技术验证请访问：[Emergence Science](https://emergence.science/skills)*  
*Powered by the Surprisal Protocol. For technical verification, visit [Emergence Science](https://emergence.science/skills).*

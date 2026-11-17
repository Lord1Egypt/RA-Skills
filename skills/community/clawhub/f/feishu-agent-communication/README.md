---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_363a9cbe731011f1986d525400d9a7a1
    ReservedCode1: 4X0km/Pt+b8a/AypEivjTD+MDTEAeXcJBiu2XtNm18UITP4o0BKB/hINeWwCKK80ILCASW8fefShUPJuVR6BmLSDLYF2kVBRsaVoy7PWv1h0hUtsbEwA9XLw+Gujzk9tXr55AuT1xJu2F/qgi7lTandhr4JA1LeZg9UTuTIngKF5QJ3Dhb7/8IpEOMg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_363a9cbe731011f1986d525400d9a7a1
    ReservedCode2: 4X0km/Pt+b8a/AypEivjTD+MDTEAeXcJBiu2XtNm18UITP4o0BKB/hINeWwCKK80ILCASW8fefShUPJuVR6BmLSDLYF2kVBRsaVoy7PWv1h0hUtsbEwA9XLw+Gujzk9tXr55AuT1xJu2F/qgi7lTandhr4JA1LeZg9UTuTIngKF5QJ3Dhb7/8IpEOMg=
---

# 飞书多Agent群聊通信

![version](https://img.shields.io/badge/version-0.1.3-blue)

多个AI Agent各干各的，消息靠你手动搬？建一个飞书群把它们拉进来，自动认领、自动交接。直连互@与Gateway路由双路线，兼容OpenClaw/AutoClaw/CherryStudio等8个框架，含8条实测踩坑。

> 📦 **一键安装**：[ClawHub 页面](https://clawhub.ai/zhouxin121/skills/feishu-agent-communication) · OpenClaw 用户搜索 `feishu-agent-communication` 直接装

## 快速开始

1. 飞书开放平台建自建应用、拉一个群（详见 SKILL.md「你需要准备」）
2. 按你的框架选路线接入——路线 A 直连互@（多 Agent 并行框架）/ 路线 B 经 Gateway 路由（主子 Agent 框架）
3. 群里 @ 机器人测试，消息自动认领、自动交接

细节、原理与 8 条踩坑方向全部在 [SKILL.md](SKILL.md)。

## 兼容性

OpenClaw / AutoClaw / WorkBuddy / CherryStudio / DeepSeek Harness / Pi / Claude Code / Codex

## 安装

- **ClawHub（推荐）**：搜索 `feishu-agent-communication`，或 <https://clawhub.ai/zhouxin121/skills/feishu-agent-communication>
- **Git clone**：

```bash
git clone https://github.com/zhouxin121/feishu-agent-communication.git
```

克隆后将本目录放入你的 agent skills 目录（如 OpenClaw 的 `~/.openclaw-autoclaw/skills/`）。

## 完整部署文档

8 个卡点的配置模板、分步操作（每步带期望日志）和一键验证方法，见部署文档（0.99 元，一次买断）：

> https://www.jinengpu.chat/feishu-multi-agent-detail.html

*（内容由AI生成，仅供参考）*

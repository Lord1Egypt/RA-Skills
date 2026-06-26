# 德胧舆情采集龙虾工具 v1.0

> 德胧AI龙虾军团专属外网信息舆情采集工具
> 一键安装 · miaoda-web-search + 飞书卡片 + 定时推送

## 🚀 快速安装

```bash
# 1. 复制Skill到OpenClaw目录
cp -r delonix-web-intelligence/ ~/workspace/agent/skills/

# 2. 重启OpenClaw
openclaw gateway restart

# 3. 验证
miaoda-studio-cli search-summary --query "华住 投诉 2026" --instruction "用中文总结"
```

## 📦 已整合工具

| 工具 | 状态 | 说明 |
|------|------|------|
| miaoda-web-search | ✅ 已集成 | 网页搜索摘要（主力） |
| AutoCLI | ⏳ 待集成 | 50+平台深度采集 |
| 飞书卡片 | ✅ 已配置 |精美卡片推送 |
| Cron定时 | ✅ 已配置 | 每日9:00自动推送 |

## 🔍 触发词

舆情、情报、网情、监控、搜索、行业动态、竞争对手动态、竞品分析

## 📤 发送飞书卡片

```
<card>
<title>🔥 酒店舆情日报 | 2026年4月19日</title>

## 🔴 超级热点

[内容]

---

🦞 德胧AI龙虾军团
</card>
```

## 🔄 迭代计划

- v1.1：整合Coze CLI外网检索
- v2.0：AutoCLI 50+平台全接入

---

**作者**：晁留柱的助手（小柱）  
**版本**：v1.0 | 2026-04-19

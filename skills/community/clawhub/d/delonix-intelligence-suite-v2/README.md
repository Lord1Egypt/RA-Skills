# 德胧舆情情报综合工具箱 v2.0

> 德胧AI龙虾军团舆情情报系统 | 整合 miaoda + BettaFish + 飞书卡片 + AI风险分析

## 🚀 快速安装

```bash
# 1. 克隆本仓库
git clone https://github.com/chaoliuzhu65-tech/delonix-intelligence-suite-v2.git

# 2. 复制到OpenClaw skills目录
cp -r delonix-intelligence-suite-v2/ ~/workspace/agent/skills/

# 3. 重启OpenClaw
openclaw gateway restart

# 4. 验证
miaoda-studio-cli search-summary --query "测试"
```

## 📦 整合工具

| 工具 | 状态 | 说明 |
|------|------|------|
| miaoda-web-search | ✅ 已集成 | 网页搜索摘要（主力） |
| BettaFish | ⏳ 待安装 | 30+平台深度舆情分析 |
| 抖音监控 | ✅ 已配置 | 视频平台专项 |
| 飞书精美卡片 | ✅ 已集成 | v2.0卡片模板 |
| AI风险分析 | ✅ 已集成 | 防控预案生成 |

## 🔍 触发词

舆情、情报、网情、监控、风险分析、抖音监控、酒店风险、德胧舆情

## 📤 飞书精美卡片示例

使用 `<text_tag>` + bullet list + HR 分割线的 v2.0 格式。

## 🔄 版本历史

- **v2.0**：整合BettaFish + 抖音监控 + AI风险分析 + 防控预案
- **v1.0**：miaoda搜索 + 飞书卡片基础版

---

**作者**：晁留柱的助手（小柱）
**版本**：v2.0 | 2026-04-19

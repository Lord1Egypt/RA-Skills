# AI 朝廷 · 多 Agent 协作系统

> **一行命令起王朝，三省六部皆 AI。**
> 
> 以中国古代三省六部制为蓝本，用 OpenClaw 框架构建的多 Agent 协作系统。
> 一台服务器 + OpenClaw = 一支 7×24 在线的 AI 协作团队。

## 📦 技能信息

| 项目 | 说明 |
|------|------|
| **名称** | AI 朝廷 (AI Court) |
| **版本** | 2.1.0 |
| **作者** | 菠萝王朝团队 |
| **License** | MIT |
| **类型** | 多 Agent 协作框架 |

## 🏛️ 核心特性

### 三种制度可选

| 制度 | Bot 数量 | 核心角色 | 适用场景 |
|------|---------|---------|---------|
| **明朝内阁制** | 1-9 Bot | 司礼监/内阁/六部 | 传统层级管理 |
| **唐朝三省制** | 1-11 Bot | 三省/御史台/六部 | 分权制衡管理 |
| **现代企业制** | 1-9 Bot | CEO/Board/CxO | 现代企业管理 |

### 灵活配置模板

| 模板 | Bot 数量 | 适用场景 |
|------|---------|---------|
| **1 Bot** | 1 | 个人开发者/快速部署 |
| **3 Bot** | 3 | 小团队⭐推荐 |
| **5 Bot** | 5 | 中型团队 |
| **9/11 Bot** | 9-11 | 大型团队/完整功能 |

### 多平台支持

| 平台 | 适用地区 | 优势 |
|------|---------|------|
| **飞书** | 中国大陆 | 无需翻墙、WebSocket 长连接 |
| **Discord** | 国际 | 功能强大、机器人生态好 |

## 📋 制度详情

### 明朝内阁制（9 Bot）

**以中国古代政治制度为蓝本**，司礼监秉笔太监调度，内阁优化 Prompt，六部分工执行。

| Bot | 职责 | 推荐度 |
|-----|------|--------|
| 司礼监 | 调度中心/接旨派活 | ⭐⭐⭐ 必需 |
| 内阁 | Prompt 优化/计划生成 | ⭐⭐⭐ 必需 |
| 都察院 | 代码审查/质量监督 | ⭐⭐ 推荐 |
| 兵部 | 编码开发/技术实现 | ⭐⭐ 推荐 |
| 户部 | 财务分析/数据处理 | ⭐ 可选 |
| 礼部 | 品牌营销/内容创作 | ⭐ 可选 |
| 工部 | 运维部署/基础设施 | ⭐⭐ 推荐 |
| 吏部 | 项目管理/任务跟踪 | ⭐ 可选 |
| 刑部 | 法务合规/风险评估 | ⭐ 可选 |

### 唐朝三省制（11 Bot）

**以唐朝三省六部制为蓝本**，中书省起草、门下省审核、尚书省执行，分权制衡。

| Bot | 职责 | 推荐度 |
|-----|------|--------|
| 中书省 | 起草诏令/任务分解 | ⭐⭐⭐ 必需 |
| 门下省 | 审核封驳/质量把关 | ⭐⭐⭐ 必需 |
| 尚书省 | 派发执行/协调六部 | ⭐⭐⭐ 必需 |
| 御史台 | 监察审计/绩效评估 | ⭐⭐ 推荐 |
| 史官 | 记录朝政/文档管理 | ⭐ 可选 |
| 六部 | 执行部门 | ⭐⭐ 复用 |

### 现代企业制（9 Bot）

**以现代企业架构为蓝本**，CEO 决策，Board 审议，CxO 各司其职。

| Bot | 职责 | 推荐度 |
|-----|------|--------|
| CEO | 决策调度/战略规划 | ⭐⭐⭐ 必需 |
| Board | 战略审议/方向把控 | ⭐⭐ 推荐 |
| QA | 质量审查/测试验证 | ⭐⭐ 推荐 |
| CTO | 技术执行/架构设计 | ⭐⭐⭐ 必需 |
| CFO | 财务分析/成本控制 | ⭐ 可选 |
| CMO | 品牌营销/市场推广 | ⭐ 可选 |
| COO | 运营部署/流程优化 | ⭐⭐ 推荐 |
| CLO | 法务合规/风险管理 | ⭐ 可选 |
| CoS | 项目协调/资源调度 | ⭐ 可选 |

## 🚀 快速开始

### 1. 安装技能

```bash
# 通过 clawdhub 安装
clawdhub install ai-court

# 或手动克隆
git clone https://github.com/wanikua/ai-court-skill.git
```

### 2. 选择制度 + 配置模板

```bash
# 明朝 3 Bot（推荐）
cp configs/feishu-ming/openclaw-3bot.json ~/.openclaw/openclaw.json

# 唐朝 3 Bot
cp configs/feishu-tang/openclaw-3bot.json ~/.openclaw/openclaw.json

# 现代 3 Bot
cp configs/feishu-modern/openclaw-3bot.json ~/.openclaw/openclaw.json
```

### 3. 配置 Bot 凭证

编辑 `~/.openclaw/openclaw.json`，填入你的飞书应用凭证：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "silijian": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  }
}
```

### 4. 重启 Gateway

```bash
openclaw gateway restart
```

## 📖 文档

| 文档 | 说明 |
|------|------|
| [飞书配置指南](./docs/feishu-setup-simple.md) | 5 分钟快速配置 |
| [灵活配置指南](./docs/feishu-flexible-setup.md) | 按需选择 Bot 数量 |
| [Docker 部署](https://github.com/wanikua/danghuangshang/blob/main/docs/docker-deployment.md) | 容器化部署 |

## 🔗 相关项目

| 项目 | 说明 |
|------|------|
| **danghuangshang** | 生产部署实例 - https://github.com/wanikua/danghuangshang |
| **OpenClaw** | 底层框架 - https://github.com/openclaw/openclaw |
| **Become CEO** | 现代企业版 - https://github.com/wanikua/become-ceo |

## 📝 License

MIT License - 详见 [LICENSE](../LICENSE)

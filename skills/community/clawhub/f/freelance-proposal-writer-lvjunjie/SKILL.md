# Freelance-Proposal-Writer-Pro Skill

AI 驱动的 Freelancer/Upwork 投标提案生成技能（专业版）。帮助自由职业者快速创建高转化率的投标提案。

## 功能

- **AI 生成投标提案** - 根据职位描述自动生成个性化提案
- **客户分析匹配** - 分析客户历史、需求痛点，提供匹配建议
- **成功率优化建议** - 基于成功提案模式提供优化建议
- **提案模板库** - 内置多种场景的提案模板

## 使用方式

### 生成提案

```bash
freelance-proposal write --job "Job description here" --skills "your skills"
```

### 分析客户

```bash
freelance-proposal analyze --client "Client profile or history"
```

### 获取优化建议

```bash
freelance-proposal optimize --proposal "Your draft proposal"
```

### 列出模板

```bash
freelance-proposal templates
```

## 命令

| 命令 | 描述 |
|------|------|
| `write` | 生成投标提案 |
| `analyze` | 分析客户/职位 |
| `optimize` | 优化现有提案 |
| `templates` | 列出可用模板 |
| `save` | 保存提案到库 |
| `stats` | 查看提案统计 |

## 配置

在 `config.json` 中配置：

```json
{
  "apiKey": "your-api-key",
  "defaultTone": "professional",
  "templatesPath": "./templates",
  "outputFormat": "markdown"
}
```

## 提案模板类型

1. **standard** - 标准投标提案
2. **premium** - 高端定制提案
3. **quick** - 快速响应提案
4. **followup** - 跟进提案
5. **referral** - 推荐提案

## 成功率优化因子

- 前 3 句抓住注意力
- 展示相关案例
- 明确交付时间
- 提出具体问题
- 个性化称呼
- 简洁有力（150-300 字）

## 安装

```bash
npm install -g freelance-proposal-writer
```

## 定价

- 订阅制：$79/月
- 包含：无限提案生成、模板库、优化建议
- 免费试用：7 天

## 作者

OpenClaw Skills Team

## 许可证

MIT

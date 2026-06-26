# Freelance-Proposal-Writer Skill

自由职业提案生成器 - AI 生成定制化投标提案，提高中标成功率。

**Slug**: freelance-proposal-writer-pro

## 功能

- **智能分析**: 分析项目需求，提取关键信息
- **定制生成**: 根据项目特点生成个性化提案
- **成功率优化**: 使用经过验证的高转化率模板
- **多平台支持**: 支持 Upwork、Fiverr、Freelancer 等平台
- **案例展示**: 自动匹配相关作品集案例
- **定价建议**: 基于市场和经验给出合理报价

## 触发词

当用户提到以下关键词时使用此技能：
- "写提案"
- "投标"
- "freelance proposal"
- "upwork 提案"
- "fiverr 投标"
- "自由职业"
- "接项目"
- "写标书"
- "proposal writer"
- "投标模板"

## 使用方法

### 生成提案

```bash
clawhub run freelance-proposal-writer generate --project "项目描述" --skills "技能列表"
```

### 优化现有提案

```bash
clawhub run freelance-proposal-writer optimize --file proposal.txt
```

### 分析中标率

```bash
clawhub run freelance-proposal-writer analyze --history
```

## 配置

在 `TOOLS.md` 中添加以下配置：

```markdown
### Freelance Proposal Writer

- 个人简介：(你的专业背景)
- 核心技能：(技能列表)
- 代表案例：(案例链接)
- 小时费率：$XX/hr
- 目标平台：upwork/fiverr/freelancer
```

## 输出格式

生成结构化的投标提案，包含：
- 个性化开场白
- 需求理解说明
- 解决方案概述
- 相关案例展示
- 时间线和报价
- 行动号召

## 注意事项

- 提案应该真诚、具体、有针对性
- 避免使用过于模板化的语言
- 根据平台特点调整语气和格式

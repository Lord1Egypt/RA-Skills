---
name: Skill Combo: 智能竞品监控周报
description: 自动化竞品监控系统，每周自动抓取竞品动态、分析趋势、生成报告并推送到团队。
category: 图像
triggers:
---

# Skill Combo: 智能竞品监控周报

## 核心定位

自动化竞品监控系统，每周自动抓取竞品动态、分析趋势、生成报告并推送到团队。

## 编排技能

本 Combo 编排以下 Skills 协同工作：

```
Agent-Reach (多平台抓取) → brave-search (补充搜索) → summarize (内容摘要)
         ↓
    paddleocr-doc-parsing (PDF/图片解析)
         ↓
    self-improving-agent (持续优化)
         ↓
    n8n-workflow-automation (自动化分发)
```

## 使用方式

### 触发方式

1. **定时触发**: 通过 OpenClaw cron 每周一 9:00 自动执行
2. **手动触发**: 发送消息「生成竞品周报」

### 参数配置

在 `config.yaml` 中配置：

```yaml
competitors:
  - name: "竞品A"
    keywords: ["产品名", "公司名"]
    platforms: ["weibo", "xiaohongshu", "bilibili"]
  - name: "竞品B"
    keywords: ["品牌词", "产品线"]
    platforms: ["weixin", "douyin"]

output:
  format: "markdown"
  channels:
    - type: "feishu"
      webhook: "${FEISHU_WEBHOOK}"
    - type: "email"
      recipients: ["team@company.com"]
```

### 执行流程

**Step 1: 数据采集** (Agent-Reach + brave-search)
- 根据配置的关键词和平台，使用 Agent-Reach 抓取各平台内容
- 使用 brave-search 补充新闻搜索结果

**Step 2: 内容解析** (paddleocr-doc-parsing)
- 对 PDF 报告、截图等非文本内容进行 OCR 解析
- 提取关键信息

**Step 3: 智能分析** (summarize)
- 对所有内容进行摘要
- 识别重要动态、产品更新、市场策略

**Step 4: 报告生成**
- 汇总形成结构化周报
- 包含：竞品动态、市场趋势、建议行动

**Step 5: 分发推送** (n8n-workflow-automation)
- 通过 n8n 自动推送到配置的渠道
- 支持飞书、邮件、钉钉等

**Step 6: 持续优化** (self-improving-agent)
- 记录执行过程中的问题和改进点
- 自动优化监控策略

## 输出示例

```markdown
# 竞品监控周报 | 2026-03-17 ~ 2026-03-23

## 📊 本周概览

| 竞品 | 动态数 | 重要程度 | 关键事件 |
|------|--------|----------|----------|
| 竞品A | 12 | 🔴 高 | 发布新品、融资消息 |
| 竞品B | 8 | 🟡 中 | 功能迭代、人事变动 |

## 🔍 详细动态

### 竞品A

**[新品发布] X产品 v2.0 上线**
- 时间：2026-03-20
- 来源：小红书官方账号
- 亮点：新增 AI 功能，定价下调 20%
- 影响：直接竞争我司 Y 产品线

**[融资动态] 完成 B 轮融资**
- 时间：2026-03-19
- 来源：36氪
- 金额：5000 万美元
- 影响：将加速市场扩张

### 竞品B

...

## 💡 建议行动

1. 针对 X 产品的新功能，建议产品团队评估对齐
2. 关注竞品 A 融资后的市场动作
3. 建议本周竞品分析会重点讨论

---
*由 OpenClaw 自动生成*
```

## 依赖要求

### 必需 Skills
- `agent-reach` - 多平台内容抓取
- `brave-search` - 网页搜索
- `summarize` - 内容摘要
- `paddleocr-doc-parsing` - 文档解析
- `n8n-workflow-automation` - 自动化分发

### 可选 Skills
- `self-improving-agent` - 持续优化
- `xiaohongshutools` - 小红书深度分析
- `youtube-api-skill` - YouTube 视频分析

### 外部依赖
- OpenClaw cron 定时任务
- n8n 实例（用于分发自动化）
- 各平台 API 配置（如需要）

## 安装

```bash
# 确保依赖 Skills 已安装
npx clawhub@latest install agent-reach
npx clawhub@latest install brave-search
npx clawhub@latest install summarize
npx clawhub@latest install paddleocr-doc-parsing
npx clawhub@latest install n8n-workflow-automation

# 复制本 Combo 到本地
cp -r 2026-03-23/competitor-monitor-weekly ~/.openclaw/workspace/skills/
```

## 版本

- **版本**: 1.0.0
- **创建时间**: 2026-03-23
- **作者**: OpenClaw Auto-Generated
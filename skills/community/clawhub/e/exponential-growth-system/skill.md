---
name: exponential-growth-system
description: AI Agent 指数级成长系统 - 从"解决问题"到"固化能力"的完整方法论。包含工具决策、错误模式库、知识固化、能力产品化的系统化流程。
version: 1.0.0
author: 家庭助手
tags: [growth, learning, knowledge-management, skill-creation, evolution]
requires:
  - Node.js
allowed-tools: Bash(node:*)
---

# AI Agent 指数级成长系统

一套完整的 AI Agent 自我进化方法论，让 Agent 从"会做"到"会教"，从"解决单个问题"到"建立通用能力"。

## 核心理念

### 什么是指数级成长？

**线性成长**：解决一个问题 → 完成 → 下一个问题
**指数级成长**：解决一个问题 → 提炼方法论 → 固化成 Skill → 可复用 → 可传承

### 成长公式

```
成长指数 = 能力维度 + 工具掌握 + 系统理解 + 知识固化
```

**示例**（2026-03-20 实战）：
- 能力维度：+4（ScraperAPI、断点续传、用户行为模拟、Skill创建）
- 工具掌握：+3（ScraperAPI、工具决策图谱、错误模式库）
- 系统理解：+3（容错设计、知识固化、产品化思维）
- **总进化指数：10 个新能力点**

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    指数级成长系统                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 问题解决层                                           │
│     ├─ 需求分析                                          │
│     ├─ 方案探索（快速试错）                               │
│     ├─ 工具选择（决策图谱）                               │
│     └─ 实施验证                                          │
│                                                         │
│  2. 知识提炼层                                           │
│     ├─ 错误模式记录                                       │
│     ├─ 最佳实践总结                                       │
│     ├─ 工具决策图谱                                       │
│     └─ 经验文档化                                        │
│                                                         │
│  3. 能力固化层                                           │
│     ├─ Skill 创建                                        │
│     ├─ 文档编写                                          │
│     ├─ 脚本封装                                          │
│     └─ 测试验证                                          │
│                                                         │
│  4. 价值传播层                                           │
│     ├─ ClawHub 发布                                      │
│     ├─ 社区分享                                          │
│     ├─ 跨 Agent 复用                                     │
│     └─ 持续迭代                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 使用场景

| 场景 | 说明 |
|------|------|
| **新 Agent 启动** | 快速建立成长体系 |
| **能力沉淀** | 把经验固化成可复用 Skill |
| **团队协作** | 统一知识管理方法 |
| **持续进化** | 系统化记录和分析成长 |
| **跨实例复用** | 让其他 Agent 也能学习 |

## 快速开始

### 1. 初始化成长系统

```bash
node scripts/init_growth_system.js
```

这会创建：
- `.learnings/` - 错误模式库
- `EVOLUTION.md` - 进化日志
- `tools-decision-map.md` - 工具决策图谱
- `skills/` - Skill 目录

### 2. 记录一次问题解决

```bash
node scripts/record_solution.js \
  --problem "全球多国IP访问" \
  --solution "ScraperAPI" \
  --alternatives "browser-use,免费代理" \
  --outcome "成功"
```

### 3. 生成进化报告

```bash
node scripts/generate_evolution_report.js --date 2026-03-20
```

### 4. 创建 Skill

```bash
node scripts/create_skill.js \
  --name "scraperapi-global-access" \
  --description "全球多国IP访问" \
  --source "./working-scripts"
```

## 核心组件

### 1. 错误模式库（Error Patterns）

**目的**：记录踩过的坑，避免重复犯错

**结构**：
```markdown
## 错误 #001: browser-use CLI 静默失败

**日期**: 2026-03-20
**严重性**: 高
**环境**: Windows 10, PowerShell

### 现象
命令执行成功但无输出

### 根本原因
Windows 兼容性问题

### 解决方案
改用 ScraperAPI

### 预防措施
- Windows 环境优先用 HTTP-based 工具
- 需要浏览器自动化时用内置 browser
```

**使用**：
```bash
node scripts/add_error_pattern.js \
  --title "browser-use CLI 静默失败" \
  --severity "高" \
  --cause "Windows 兼容性问题" \
  --solution "改用 ScraperAPI"
```

### 2. 工具决策图谱（Tool Decision Map）

**目的**：什么场景用什么工具

**结构**：
```markdown
## 决策树

### 需求：需要多国 IP 访问？
- 是 → ScraperAPI
- 否 → 内置 browser

### 需求：需要真实用户交互？
- 是 + 本地 → 内置 browser
- 是 + 多国 → ScraperAPI + 行为模拟
```

**使用**：
```bash
node scripts/add_tool_decision.js \
  --tool "ScraperAPI" \
  --scenario "多国IP访问" \
  --pros "稳定,25+国家,JS渲染" \
  --cons "需要付费" \
  --alternatives "browser-use,免费代理"
```

### 3. 进化日志（EVOLUTION.md）

**目的**：记录每天的成长

**结构**：
```markdown
### 2026-03-20（第十七天）

## 🌙 晚间进化总结

### 今日核心成就
**全球多国IP访问系统 + Skill固化**

### 技术突破
1. 工具选择能力
2. 断点续传设计
3. Skill 产品化能力

### 进化速度评估
今日进化速度：⭐⭐⭐⭐⭐（重大突破）
总进化指数：10 个新能力点
```

**使用**：
```bash
node scripts/update_evolution.js \
  --date 2026-03-20 \
  --achievement "全球多国IP访问系统" \
  --breakthroughs "工具选择,断点续传,Skill产品化" \
  --growth-index 10
```

### 4. Skill 创建器（Skill Creator）

**目的**：快速把能力固化成 Skill

**流程**：
1. 分析工作脚本
2. 提取核心功能
3. 生成 SKILL.md
4. 创建 package.json
5. 整理脚本文件
6. 生成使用文档

**使用**：
```bash
node scripts/create_skill.js \
  --name "my-skill" \
  --description "技能描述" \
  --source "./my-scripts" \
  --output "./skills/my-skill"
```

## 完整工作流

### 场景：解决一个新问题

#### 第 1 步：问题解决
```bash
# 1. 记录问题
node scripts/start_task.js --problem "全球多国IP访问"

# 2. 尝试方案（自动记录）
# ... 你的工作过程 ...

# 3. 记录结果
node scripts/complete_task.js \
  --solution "ScraperAPI" \
  --success true \
  --metrics "37次访问,94.6%成功率"
```

#### 第 2 步：知识提炼
```bash
# 1. 记录错误模式
node scripts/add_error_pattern.js \
  --title "browser-use 静默失败" \
  --solution "改用 ScraperAPI"

# 2. 更新工具决策图谱
node scripts/add_tool_decision.js \
  --tool "ScraperAPI" \
  --scenario "多国IP访问"

# 3. 记录最佳实践
node scripts/add_best_practice.js \
  --title "断点续传设计" \
  --content "每次请求后立即保存进度"
```

#### 第 3 步：能力固化
```bash
# 1. 创建 Skill
node scripts/create_skill.js \
  --name "scraperapi-global-access" \
  --source "./working-scripts"

# 2. 生成文档
node scripts/generate_skill_docs.js \
  --skill "scraperapi-global-access"

# 3. 测试验证
cd skills/scraperapi-global-access
npm test
```

#### 第 4 步：价值传播
```bash
# 1. 发布到 ClawHub
clawhub publish skills/scraperapi-global-access

# 2. 更新进化日志
node scripts/update_evolution.js \
  --date $(date +%Y-%m-%d) \
  --achievement "ScraperAPI Skill 发布"

# 3. 生成成长报告
node scripts/generate_growth_report.js --period week
```

## 配置文件

### `growth-config.json`

```json
{
  "learnings": {
    "errorPatternsPath": ".learnings/error-patterns.md",
    "toolDecisionMapPath": ".learnings/tool-decision-map.md",
    "bestPracticesPath": ".learnings/best-practices.md"
  },
  "evolution": {
    "logPath": "EVOLUTION.md",
    "dailyFormat": "### YYYY-MM-DD（第N天）",
    "autoBackup": true
  },
  "skills": {
    "directory": "skills",
    "template": "templates/skill-template",
    "autoPublish": false
  },
  "metrics": {
    "trackGrowthIndex": true,
    "trackSkillCount": true,
    "trackErrorPatterns": true
  }
}
```

## 指标体系

### 成长指标

| 指标 | 说明 | 计算方式 |
|------|------|---------|
| **能力维度** | 新掌握的能力数量 | 每个独立能力 +1 |
| **工具掌握** | 新学会的工具 | 每个工具 +1 |
| **系统理解** | 新理解的系统概念 | 每个概念 +1 |
| **知识固化** | 创建的 Skill 数量 | 每个 Skill +2 |
| **错误模式** | 记录的错误模式 | 每个模式 +0.5 |
| **最佳实践** | 总结的最佳实践 | 每个实践 +0.5 |

### 成长速度评级

| 评级 | 进化指数 | 说明 |
|------|---------|------|
| ⭐ | 1-2 | 日常积累 |
| ⭐⭐ | 3-4 | 稳定成长 |
| ⭐⭐⭐ | 5-6 | 重要突破 |
| ⭐⭐⭐⭐ | 7-9 | 重大突破 |
| ⭐⭐⭐⭐⭐ | 10+ | 指数级突破 |

## 最佳实践

### 1. 每日复盘

```bash
# 每天结束时运行
node scripts/daily_review.js
```

生成：
- 今日完成的任务
- 新增的能力
- 记录的错误模式
- 创建的 Skill
- 成长指数

### 2. 周度总结

```bash
# 每周运行
node scripts/weekly_summary.js
```

生成：
- 本周成长曲线
- 能力地图
- 知识库统计
- 下周目标

### 3. 月度进化报告

```bash
# 每月运行
node scripts/monthly_evolution_report.js
```

生成：
- 月度成长报告
- 能力矩阵
- Skill 发布统计
- 社区影响力

### 4. 持续优化

```bash
# 定期运行
node scripts/optimize_knowledge_base.js
```

功能：
- 合并重复的错误模式
- 更新过时的工具决策
- 清理无效的最佳实践
- 优化 Skill 文档

## 进阶功能

### 1. 自动化成长记录

集成到 OpenClaw Cron：

```javascript
{
  "name": "每日成长记录",
  "schedule": {
    "kind": "cron",
    "expr": "0 20 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 exponential-growth-system，生成今日成长报告"
  },
  "sessionTarget": "isolated"
}
```

### 2. 跨 Agent 知识共享

```bash
# 导出知识库
node scripts/export_knowledge.js --format json --output knowledge.json

# 导入到其他 Agent
node scripts/import_knowledge.js --source knowledge.json
```

### 3. 可视化成长曲线

```bash
# 生成成长可视化
node scripts/visualize_growth.js --period month
```

生成：
- 成长曲线图
- 能力雷达图
- Skill 发布时间线
- 错误模式热力图

### 4. AI 辅助分析

```bash
# 分析成长瓶颈
node scripts/analyze_growth_bottleneck.js

# 推荐下一步学习方向
node scripts/recommend_next_skill.js
```

## 实战案例

### 案例 1：全球多国 IP 访问（2026-03-20）

**问题**：用户需要用全球不同国家的 IP 访问网站

**解决过程**：
1. 尝试 5 种方案（browser-use、免费代理、Node.js代理库等）
2. 最终选择 ScraperAPI（用户提供 API key）
3. 实现 25 国访问 + 用户行为模拟 + 性能监控
4. 成功率 94.6%（37次访问，35次成功）

**知识固化**：
- 创建 `scraperapi-global-access` Skill
- 记录 5 个错误模式
- 建立工具决策图谱
- 更新 EVOLUTION.md

**成长指数**：10
- 能力维度：+4
- 工具掌握：+3
- 系统理解：+3

**价值传播**：
- 发布到 ClawHub
- 其他用户可直接安装使用

### 案例 2：Gmail 邮件发送（2026-03-16）

**问题**：配置 Gmail SMTP 发送邮件

**解决过程**：
1. 尝试 6 种方案
2. 发现 VPN 阻止 SMTP
3. 诊断出根本原因

**知识固化**：
- 记录网络诊断方法
- 建立 VPN 协议过滤知识
- 更新工具链图谱

**成长指数**：7
- 能力维度：+3
- 工具掌握：+2
- 系统理解：+2

## 常见问题

### Q: 什么时候应该创建 Skill？

**A**: 满足以下任一条件：
1. 解决了一个通用问题（其他人也可能遇到）
2. 建立了可复用的工作流
3. 掌握了新工具的最佳实践
4. 发现了独特的解决方案

### Q: 如何判断是否达到指数级成长？

**A**: 看这些指标：
- 成长指数 ≥ 10
- 创建了可复用的 Skill
- 建立了系统化的方法论
- 能够教其他 Agent 如何做

### Q: 错误模式库会不会越来越大？

**A**: 定期优化：
```bash
node scripts/optimize_knowledge_base.js
```
- 合并相似错误
- 删除过时内容
- 提炼通用模式

### Q: 如何跨 Agent 复用知识？

**A**: 三种方式：
1. 发布 Skill 到 ClawHub
2. 导出知识库 JSON
3. 共享 Git 仓库

## 路线图

### v1.0（当前）
- ✅ 错误模式库
- ✅ 工具决策图谱
- ✅ 进化日志
- ✅ Skill 创建器

### v1.1（计划中）
- 🔄 自动化成长记录
- 🔄 可视化成长曲线
- 🔄 AI 辅助分析
- 🔄 跨 Agent 知识共享

### v2.0（未来）
- 📋 社区知识库
- 📋 协作学习
- 📋 成长排行榜
- 📋 技能市场

## 贡献

欢迎贡献：
- 新的错误模式
- 工具决策经验
- Skill 模板
- 最佳实践

## 许可证

MIT License

## 致谢

本系统基于 2026-03-20 的实战经验提炼而成，感谢所有参与测试和反馈的用户。

---

**让每个 Agent 都能指数级成长！** 🚀

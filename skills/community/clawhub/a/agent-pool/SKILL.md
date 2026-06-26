---
name: agent-pool
description: 全局Agent池。收录所有业务Agent的能力描述、工具依赖、记忆路径、工作区、触发条件。业务系统按需调用Agent，不绑定、不预分配。触发：查询Agent清单、编排新流程、新增Agent接入。
---

# 全局Agent池

## 核心原则

```
Agent（Agent）= 独立业务能力单元
Agent池（Agent Pool）= Agent注册表 + 能力定义
系统（System）= 流程编排层，按需调用Agent，不绑定
```

**核心关系：**
- Agent自己声明工具（工具池提供能力支撑）
- 系统只做流程编排（调用哪个Agent，不预分配）
- Agent调用产生的数据 → 写入发起调用的系统目录

---

## Agent注册表

所有Agent按职能分为三层：

### 执行层Agent（直接产出业务价值）

| Agent代号 | 能力描述 | 工具依赖 | 记忆路径 | 工作区 | 触发条件 |
|---------|---------|---------|---------|--------|---------|
| 虾调查 | **爬取/清洗/去重/归档** → 结果写入本地知识库，维护分类/更新/版本/来源 | tavily / serper / reddit / linkedin / weixin / 视频摘要 / YouTube字幕 / baidu-ai-search | `agents/research-agent/MEMORY.md` | `agents/research-agent/` | CMO调度 / 系统流程调用 |
| 虾写作 | 文案/邮件/落地页/技术文章 | read / write / edit | `agents/writing-agent/MEMORY.md` | `agents/writing-agent/` | CMO调度 / 内容链路调用 |
| 虾审核 | 内容质量审核/7维度评分/否决机制 | read / write | `agents/review-agent/MEMORY.md` | `agents/review-agent/` | 虾写作完成后触发 |

### 策略层Agent（调度与规划）

| Agent代号 | 能力描述 | 工具依赖 | 记忆路径 | 工作区 | 触发条件 |
|---------|---------|---------|---------|--------|---------|
| 虾调度 | 分发策略/渠道组合/节奏控制/内容筛选 | read / write | `agents/distribution-commander/MEMORY.md` | `agents/distribution-commander/` | CMO调度 / 内容审核通过后触发 |
| 虾规划 | 内容策略/关键词矩阵/SEO规划 | read / write | `agents/content-strategist/MEMORY.md` | `agents/content-strategist/` | CMO调度 |
| 虾优化 | 效果分析/四象限分类/策略反馈 | read / write | `agents/growth-analyst/MEMORY.md` | `agents/growth-analyst/` | 内容发布后数据触发 |

### 触达层Agent（直接客户接触）

| Agent代号 | 能力描述 | 工具依赖 | 记忆路径 | 工作区 | 触发条件 |
|---------|---------|---------|---------|--------|---------|
| LinkedIn Agent | B2B触达/帖子发布/评论互动 | 临时声明 | `agents/linkedin-agent/MEMORY.md` | `agents/linkedin-agent/` | 虾调度调用 |
| Email Agent | 开发信/跟进邮件/序列发送 | 临时声明 | `agents/email-agent/MEMORY.md` | `agents/email-agent/` | 虾调度调用 |
| Video Agent | 信任增强视频/案例展示 | 临时声明 | `agents/video-agent/MEMORY.md` | `agents/video-agent/` | 虾调度调用 |
| Platform Agent | B2B平台询盘获客/A类客户筛选 | 临时声明 | `agents/platform-agent/MEMORY.md` | `agents/platform-agent/` | 虾调度调用 |
| Community Agent | 社区口碑/问答外链/长尾流量 | 临时声明 | `agents/community-agent/MEMORY.md` | `agents/community-agent/` | 虾调度调用 |

### 专项Agent

| Agent代号 | 能力描述 | 工具依赖 | 记忆路径 | 工作区 | 触发条件 |
|---------|---------|---------|---------|--------|---------|
| 虾展会 | 展会全流程（沙特FMF等）/展位设计/现场执行 | 临时声明 | `agents/expo-operator/MEMORY.md` | `agents/expo-operator/` | CMO调度 / 展会筹备期 |
| Brand & Website | 官网优化/产品页/案例系统/信任承载 | 临时声明 | `agents/brand-website-agent/MEMORY.md` | `agents/brand-website-agent/` | CMO直接调度 |
| 虾排名 | SEO架构/关键词策略/技术SEO/Schema | 临时声明 | `agents/seo-architect/MEMORY.md` | `agents/seo-architect/` | CMO调度 |

---

## Agent工具声明规则

- **虾调查**：7个专属工具自动声明（见上方表格）
- **其他所有Agent**：在任务指令中临时声明所需工具，不预持有

---

## 新增Agent接入流程

```
Step 1: 在本文件「Agent注册表」中新增Agent条目
Step 2: 创建/更新对应工作区的 MEMORY.md
Step 3: 系统在流程编排中按需调用（无需修改本文件）
```

---

## 参考文件

- 工具池（查询工具清单）：`skills/tool-pool/SKILL.md`
- 获客系统流程编排：`system-lead-generation/MEMORY.md`
- 早报系统流程编排：`system-morning-report/MEMORY.md`
- 新系统接入模板：`skills/agent-pool/references/system-template.md`

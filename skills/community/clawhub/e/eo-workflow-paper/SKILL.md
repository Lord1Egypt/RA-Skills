---
name: eo-workflow-paper
description: 学术论文工作流 - 从文献研究到论文发表的完整流程，覆盖论文撰写、格式规范、查重控制
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-workflow-paper

> 学术论文工作流 - 从文献研究到论文发表的完整流程

## 一句话介绍

端到端学术论文工作流，将论文研究周期从3周压缩到1周，调用141位专家库实现800%效率提升。

## 核心功能

- **文献研究**: 核心文献智能筛选（50篇→15篇），研究热点报告生成
- **方法论设计**: 研究问题定义、实验方案设计、假设推导
- **论文撰写**: IMRAD结构完整输出，Abstract/Introduction/Method/Experiment/Conclusion
- **审查修改**: 逻辑审查、语言润色、查重控制（<10%）

## 使用方法

```bash
# 启动学术论文工作流
/dream "深度学习医疗影像诊断论文，SCI二区"

// 或者直接调用
使用 eo-workflow-paper 完成一篇关于[主题]的学术论文
```

## 与EO插件的协同

| Ability | 用途 |
|---------|------|
| eo-ability-plan | 生成 WBS 论文撰写计划 |
| eo-ability-architect | 论文整体架构设计 |
| eo-ability-verify | Checkpoint 格式合规检查 |
| eo-ability-memory | 记住导师偏好、目标期刊格式 |
| eo-ability-rag | 共享学术写作知识库 |

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 141专家库调用、跨会话记忆、Checkpoint自动验证、真实文献筛选 |
| **无插件（基础）** | LLM生成文本、IMRAD结构模板、基础格式检查 |

### 案例数据
- 文献综述: 3天→3小时（效率提升800%）
- 修改轮次: 5轮→2轮（节省2周）
- 格式一致性: 100%

## 示例

```bash
/dream "深度学习医疗影像诊断论文，SCI二区，目标期刊Medical Image Analysis"

// EO 自动执行：
// 1. [academic-research-methodologist] → 确定研究热点 + 制定搜索策略
// 2. [specialized-ml-engineer] → 筛选核心文献（50篇→15篇）
// 3. [academic-methodologist] → 设计 U-Net+Attention 模型
// 4. [academic-technical-writer] → IMRAD 结构撰写
// 5. [Proactive Memory] → 记住用户偏好（IEEE格式、目标期刊）
```

## Phases

| Phase | 负责人 | 输出 |
|-------|--------|------|
| 1. 文献研究 | academic-research-methodologist + specialized-ml-engineer | 核心文献列表、研究热点报告 |
| 2. 方法论设计 | academic-methodologist | 研究问题、方法论、实验方案 |
| 3. 论文撰写 | academic-technical-writer | 完整IMRAD论文 |
| 4. 审查修改 | code-reviewer | 逻辑审查报告、最终稿件 |

## Expert Team

| 专家 | 角色 | 职责 |
|------|------|------|
| academic-research-methodologist | 文献搜索 | 制定搜索策略、筛选核心文献 |
| specialized-ml-engineer | ML专家 | 筛选技术文献、验证方法可行性 |
| academic-methodologist | 方法论专家 | 设计研究方法、实验方案 |
| academic-technical-writer | 学术写作 | IMRAD结构撰写、格式规范 |
| code-reviewer | 审查专家 | 逻辑审查、查重控制 |

## Templates

- `templates/paper-template.md` - 论文结构模板
- `templates/ieee-format.md` - IEEE格式规范

---

*🦞⚙️ 钢铁龙虾军团 - 让学术研究更高效*

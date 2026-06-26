---
name: paper-assistant
description: 当用户需要查找、筛选或推荐最新的 Agent 模型底层算法或强化学习方向论文，用于后续精读或推送时使用
---

# Paper Feed Skill

## 1. Description（技能详细说明）
Paper Feed 是一个自动化论文推荐 Skill，用于从最新论文池中筛选出 **Agent 模型底层算法或强化学习方向** 的高价值论文，并生成结构化推荐内容。  
该 Skill 可作为论文推送流水线的第一环，每天或定期推荐一篇值得阅读的研究论文。

## 2. When to use（触发场景）
- 当用户希望获取最新 Agent 或强化学习方向论文推荐时  
- 当需要自动筛选论文池并避免重复推送时  
- 当需要将推荐论文与精读、推送等其他 Skill 串联时  

## 3. How to use（调用逻辑）
### 3.1 获取候选论文
运行脚本获取最新论文池：
```bash
python scripts/fetch_papers.py
# 功能说明：
# 从 OpenReview / arXiv 获取最新论文
# 输出 JSON 列表
```
### 3.2 LLM 筛选论文
你现在是资深科研专家。请从以下论文 JSON 列表中筛选出一篇最符合『Agent模型底层算法或强化学习』的论文。

【筛选论文】
从候选池中，判断每篇论文是否属于 Agent 模型底层算法或强化学习 方向。
判断依据——看论文的核心贡献是什么：

  属于本方向（选入）：
  - 核心贡献是模型训练方法（如 RL、RLHF、PPO、DPO 等）
  - 核心贡献是提出新的评测基准或数据集
  - 涉及模型对齐（Alignment）、微调（Fine-tuning / PEFT）
  - 涉及注意力机制改进、模型压缩、架构创新或底层算法优化
  - 核心贡献是强化学习中的 Agent 策略迭代

  不属于本方向（排除）：
  - 仅涉及系统工程、Agent 编排框架或应用落地
  - 涉及工具调用（Tool Use）或 Web 导航等工程实现
  - 仅讨论 Agent 的规划、记忆、反思等系统级组件

  对每篇候选论文，阅读标题和摘要后做出判断。不需要逐篇输出判断过程，只需筛选出符合条件的论文。

【选择一篇推荐】
从筛选后的论文中选一篇推荐。优先策略：
1. 优先选择尚未推送过的论文
2. 在未推送论文中，优先选择来自 Oral > Spotlight > Poster > arXiv 的
3. 同等条件下，选择系统设计创新性更强的

【记录已推送】
选定论文后，将其 ID 追加到 data/pushed.json


【数据文件】
- data/pushed.json：已推送论文记录，格式为 {"pushed": ["id1", "id2", ...]}
- 如果文件不存在，脚本会自动创建

【约束】
- 只推送 2026 年 1 月 1 日之后的论文
- 论文池有限（约 400-500 篇），合理控制推送节奏
- OpenReview API 无需认证，arXiv API 无需认证，均为免费公开接口

### 3.3 输出结果
Skill 返回格式：
```
### 推荐论文
**标题**: {title}
**作者**: {authors}
**来源**: {venue}
**PDF**: {pdf_url}
### 摘要
{abstract}
### 推荐理由
{reason}
```

## Edge cases（边缘场景）
- 论文池中无符合条件的论文：Skill 可返回提示“当前论文池暂无符合条件论文”
- 重复论文：Skill 自动检测已推送记录，避免重复推送
- API 获取失败（OpenReview / arXiv）：Skill 返回提示“论文数据获取失败，请检查网络或接口状态”


## Pipeline Integration（与其他 Skill 的协作）
这个 skill 的输出是整个论文推送流水线的第一环：
- paper-assistant：推荐论文并输出标题与 PDF
- ljg-paper： 接收 PDF 链接，执行精读 pipeline（拆论文、信息榨取、白话解释、费曼讲解、博导审稿）
- so-send-message：将精读结果推送到群聊
- 定时任务触发时，依次调用这三个 skill 即可完成全流程


## Data Files（数据文件说明）
- data/pushed.json：已推送论文记录，格式为 {"pushed": ["id1", "id2", ...]}
- 如果文件不存在，脚本会自动创建

## Constraints（约束条件）
- 仅推送 2026-01-01 之后论文
- 论文池约 400–500 篇
- OpenReview / arXiv API 均无需认证，免费公开接口

## Directory Structure（目录结构）
```
paper-assistant
├─ skill.md
├─ scripts
│  ├─ mark_pushed.py
│  └─ fetch_papers.py
└─ data
   └─ pushed.json
```
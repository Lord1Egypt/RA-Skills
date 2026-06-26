---
name: arxiv-collision-cognition
version: 1.1.0
author: KingOfZhao
description: ArXiv 论文碰撞认知 Skill —— 用四向碰撞推理从学术论文中提取可操作洞见
tags: [cognition, arxiv, research, collision-reasoning, knowledge-extraction, literature]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# ArXiv Collision Cognition Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | arxiv-collision-cognition      |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 95%                            |

## 核心能力

将 ArXiv 论文与你当前项目的已知知识进行四向碰撞，提取跨域洞见：

1. **正面碰撞**：论文核心方法与你的现有方案直接对比，找出可迁移技术
2. **反面碰撞**：论文的局限性/失败案例是否正是你的场景优势？
3. **侧面碰撞**：论文的非主要贡献（ablation / appendix）中是否有隐藏宝藏？
4. **整体碰撞**：论文的研究方向趋势是否预示你项目的未来路径？

已知/未知分离 + 文件记忆 + 人机闭环全部在此场景中应用。

## 安装命令

```bash
clawhub install arxiv-collision-cognition
# 或手动安装
cp -r skills/arxiv-collision-cognition ~/.openclaw/skills/
```

## 核心论文库（按主题分组）

### 自进化 / 自改进 Agent
| 论文 | ArXiv ID | 对本项目的直接价值 |
|------|----------|------------------|
| Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing | 2602.04837 | 群体进化+经验共享，与"人机闭环+四向碰撞"一致，可扩展为多Agent迭代Skill |
| A Survey of Self-Evolving Agents | 2507.21046 | 最全自进化综述（What/When/How），作为理论骨架 |
| SAGE: Multi-Agent Self-Evolution for LLM Reasoning | 2603.15255 | Challenger+Planner+Solver+Critic四Agent闭环，与四向碰撞推理几乎一致 |
| Self-evolving Embodied AI | 2602.04411 | 记忆自更新+任务自切换+模型自进化，匹配具身智能演进路径 |

### DiePre 视觉 / 照片→CAD / 工业线条检测
| 论文 | ArXiv ID | 对本项目的直接价值 |
|------|----------|------------------|
| Generating CAD Code with Vision-Language Models for 3D Designs | 2410.05340 | VLM生成CAD+迭代验证（CADCodeVerify），可升级照片→SVG/DXF管道 |
| From 2D CAD Drawings to 3D Parametric Models: A Vision-Language Approach | 2412.11892 | 2D图纸→参数化3D，解决透视矫正和参数化问题 |
| Tool-Augmented VLLMs as Generic CAD Task Solvers | (ICCV 2025) | VLLM+工具调用做通用CAD任务，适合封装OpenCV管道为可调用Skill |

### 具身智能 / Vision-Language-Action (VLA)
| 论文 | ArXiv ID | 对本项目的直接价值 |
|------|----------|------------------|
| Efficient Vision-Language-Action Models for Embodied Manipulation | 2510.17111 | VLA高效优化综述（低延迟+内存优化），适合M1 Max本地部署 |
| Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning | 2510.11027 | 强化具身推理的VLA，可作为DiePre"照片→动作决策"理论基础 |

### Agent 记忆系统
| 论文 | ArXiv ID | 对本项目的直接价值 |
|------|----------|------------------|
| Memory in the Age of AI Agents | 2512.13564 | 最新Agent记忆综述（token/parametric/latent），可升级HEARTBEAT记忆模块 |
| Beyond RAG for Agent Memory | 2602.02007 | "Decoupling and Aggregation"超越传统RAG，解决长时序记忆问题 |

## 每日筛选工作流（HEARTBEAT 集成）

```
每个心跳周期执行:
1. 从 ArXiv API 拉取匹配关键词的最新论文（每日上限5篇）
   关键词: self-evolving agent, vision-language model, embodied AI, 
           CAD generation, agent memory, packaging quality control
2. 对每篇论文执行四向碰撞推理
3. 碰撞结果写入 collision_log/arxiv_{id}_{date}.json
4. 置信度 ≥ 85% 的洞见 → 加入 actionable_insights 队列
5. 人类标记已验证的洞见 → 更新项目知识库
```

## 调用方式

```python
from skills.arxiv_collision_cognition import ArxivCollisionCognition

acc = ArxivCollisionCognition(workspace=".")

# 用 ArXiv ID 触发碰撞
result = acc.collide(
    arxiv_id="2602.04837",
    project_context={
        "domain": "packaging quality control",
        "known": ["corrugated board defect types", "current detection accuracy 87%"],
        "unknown": ["thermal deformation modeling", "acoustic inspection feasibility"]
    }
)

print(result.confidence)         # 置信度
print(result.actionable_insights) # 可操作洞见列表
print(result.collision_log)      # 四向碰撞详情

# 批量碰撞（每日筛选）
results = acc.daily_screening(max_papers=5, keywords=["self-evolving", "CAD", "VLA"])
```

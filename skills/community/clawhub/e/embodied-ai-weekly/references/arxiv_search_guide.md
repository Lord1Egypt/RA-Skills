# ArXiv 检索指南 — 具身智能 7 方向

## 检索入口

优先使用以下两个页面获取最新论文：

```
https://arxiv.org/list/cs.RO/recent   # 机器人学
https://arxiv.org/list/cs.CV/recent   # 计算机视觉（含具身感知）
```

也可使用 arXiv 搜索 API：
```
https://arxiv.org/search/?query=<KEYWORDS>&searchtype=all&order=-announced_date_first
```

---

## 方向 1：具身感知与场景理解

**核心关键词：**
```
egocentric perception
embodied scene understanding
affordance detection
semantic mapping robot
3D scene graph robot
active perception
visual language navigation
spatial reasoning embodied
object detection manipulation
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=embodied+perception+affordance+3d+scene&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 自中心视角感知（egocentric）
- 可供性检测（affordance）
- 语义地图构建
- 视觉语言导航（VLN）

---

## 方向 2：具身决策与规划

**核心关键词：**
```
embodied planning
LLM robot planning
TAMP (task and motion planning)
code as policies
long-horizon planning robot
affordance-based planning
VLM planning robot
hierarchical planning embodied
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=embodied+planning+LLM+robot+long-horizon&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 任务与运动规划（TAMP）
- LLM/VLM 驱动的规划
- 长视野任务分解
- 代码生成作为策略

---

## 方向 3：具身控制与操作

**核心关键词：**
```
dexterous manipulation
imitation learning robot
diffusion policy robot
action diffusion
robot foundation model
visuomotor policy
bimanual manipulation
grasping neural
contact-rich manipulation
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=dexterous+manipulation+diffusion+policy+visuomotor&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 扩散策略（Diffusion Policy）
- 双臂操控
- 模仿学习
- 接触丰富操作

---

## 方向 4：具身强化学习与世界模型

**核心关键词：**
```
embodied reinforcement learning
world model robot
dreamer robotics
model-based RL manipulation
sim-to-real transfer
zero-shot robot learning
latent world model
imagination training robot
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=world+model+robot+reinforcement+learning+sim-to-real&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 隐空间世界模型
- Sim-to-Real 迁移
- 零样本机器人学习
- Dreamer 系列

---

## 方向 5：具身智能体与大模型

**核心关键词：**
```
embodied agent VLA
vision-language-action model
RT-1 RT-2 robot transformer
Octo OpenVLA
PaLM-E SayCan
LLM robotics
multimodal robot foundation
end-to-end robot learning
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=vision+language+action+embodied+agent+VLA&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- VLA 模型（Vision-Language-Action）
- 通用机器人基座模型
- 多模态指令遵循
- 推理时增强

---

## 方向 6：仿真、数据与平台

**核心关键词：**
```
robotic simulation benchmark
embodied benchmark evaluation
teleoperation dataset collection
open x-embodiment
behavior cloning dataset
digital twin robot
sim-to-real platform
synthetic data robotics
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=robotic+simulation+benchmark+embodied+dataset&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 仿真环境与基准
- 数据集发布（操控/导航）
- 遥操作系统
- 评估平台

---

## 方向 7：人机交互与具身社会智能

**核心关键词：**
```
human-robot interaction physical
shared autonomy robot
assistive robotics
physical HRI
intention prediction robot
language-conditioned robot
collaborative manipulation human
social robot navigation
```

**推荐搜索 URL：**
```
https://arxiv.org/search/?query=human+robot+interaction+shared+autonomy+intention&searchtype=all&order=-announced_date_first
```

**典型论文类型：**
- 物理人机协作
- 意图预测
- 辅助机器人
- 语言指令条件化操控

---

## 论文信息提取模板

检索到论文后，按以下格式整理每篇论文：

```markdown
### [论文中文标题]

**英文标题：** Original English Title  
**链接：** https://arxiv.org/abs/XXXX.XXXXX  
**作者：** 作者1, 作者2 et al. (机构)  
**提交日期：** YYYY-MM-DD

**核心贡献：**
（200字以内，说明：问题是什么 → 方法是什么 → 效果如何）

**方向标签：** `具身控制` `扩散策略` `双臂操控`
```

---

## 论文统计汇总格式

每周在 Markdown 报告中包含如下统计表格：

```markdown
| 方向 | 本周论文数 | 代表性工作 |
|------|-----------|-----------|
| 具身感知与场景理解 | N | 论文名 |
| 具身决策与规划 | N | 论文名 |
| 具身控制与操作 | N | 论文名 |
| 具身强化学习与世界模型 | N | 论文名 |
| 具身智能体与大模型 | N | 论文名 |
| 仿真、数据与平台 | N | 论文名 |
| 人机交互与具身社会智能 | N | 论文名 |
| **合计** | **N** | |
```

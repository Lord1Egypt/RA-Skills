# GitHub 检索指南 — 具身智能 7 方向

## 检索策略说明

### 三类查询入口

**1. 新增仓库（过去7天）**
```
https://api.github.com/search/repositories?q=<KEYWORDS>+created:>YYYY-MM-DD&sort=stars&order=desc&per_page=10
```

**2. 经典仓库近期更新**
```
https://api.github.com/search/repositories?q=<KEYWORDS>+pushed:>YYYY-MM-DD&sort=stars&order=desc&per_page=10
```

**3. 网页搜索（API 超时时的备选）**
```
https://github.com/search?q=<KEYWORDS>&type=repositories&s=updated&order=desc
```

### ⚠️ 已知限制

- GitHub API OR 运算符限制：单次查询不超过 5 个 OR 关键词，否则返回错误
- API 可能对未来日期或近期时间返回空结果，此时改用网页搜索
- 建议将每个方向拆分成 2-3 次较短的查询

---

## 方向 1：具身感知与场景理解

**API 查询（分两组）：**
```
q=embodied+perception+OR+affordance+OR+"3D+scene+graph"+created:>YYYY-MM-DD
q="semantic+mapping"+robot+OR+"active+perception"+OR+"visual+language+navigation"+created:>YYYY-MM-DD
```

**经典仓库关注清单：**
- `concept-graphs/ConceptGraphs` — 3D 开放词汇场景图
- `facebookresearch/home-robot` — 家庭具身感知
- `allenai/embodied-clip` — 视觉语言导航

---

## 方向 2：具身决策与规划

**API 查询：**
```
q="embodied+planning"+OR+"LLM+robot"+OR+TAMP+pushed:>YYYY-MM-DD
q="code+as+policies"+OR+"long-horizon+planning"+robot+pushed:>YYYY-MM-DD
```

**经典仓库关注清单：**
- `google-research/google-research` (Code as Policies) — 代码作为策略
- `nicholaschiang/robotics-papers` — TAMP 综述
- `CortexBench/` — 具身规划基准

---

## 方向 3：具身控制与操作

**API 查询：**
```
q="diffusion+policy"+robot+OR+"imitation+learning"+robot+pushed:>YYYY-MM-DD
q="dexterous+manipulation"+OR+"bimanual+manipulation"+OR+"visuomotor"+pushed:>YYYY-MM-DD
```

**经典仓库关注清单（高星，持续关注）：**
- `columbia-ai-robotics/diffusion_policy` ★4k+ — Diffusion Policy 官方实现
- `google-deepmind/mujoco_menagerie` — MuJoCo 机器人模型库
- `tonyzhaozh/act` ★2k+ — ACT 双臂操控模仿学习
- `Physical-Intelligence/openpi` ★4.8k — π0 VLA Flow 模型
- `rdt-1b/RDT-1B` ★1.7k — 双臂扩散基座模型
- `LeCAR-Lab/dial-mpc` ★953 — 人形机器人 MPC 控制

---

## 方向 4：具身强化学习与世界模型

**API 查询：**
```
q="world+model"+robot+OR+"embodied+RL"+OR+sim-to-real+pushed:>YYYY-MM-DD
q=dreamer+robotics+OR+"model-based+RL"+manipulation+pushed:>YYYY-MM-DD
```

**经典仓库关注清单：**
- `danijar/dreamer` / `danijar/dreamerv2` / `danijar/dreamerv3` — DreamerV系列
- `nicklashansen/tdmpc2` ★TDMPC2 — 基于模型的操控 RL
- `nicklashansen/1xgpt` — 1X World Model（视频预测世界模型）
- `thu-ml/MOTUS` — 运动世界模型
- `NVlabs/DriveX` — 自动驾驶世界模型（可迁移方法）

---

## 方向 5：具身智能体与大模型

**API 查询：**
```
q=VLA+OR+"vision-language-action"+robot+created:>YYYY-MM-DD
q="embodied+agent"+OR+"multimodal+robot"+OR+OpenVLA+pushed:>YYYY-MM-DD
```

**经典仓库关注清单（VLA 生态核心项目）：**
- `openvla/openvla` — OpenVLA 官方实现
- `Physical-Intelligence/openpi` ★4.8k — π0
- `octo-models/octo` — Octo 通用机器人策略
- `huggingface/lerobot` ★13k+ — LeRobot（ACT/Diffusion/SmolVLA 统一框架）
- `FlagOpen/RoboBrain2.5` ★855 — 多模态具身大模型
- `OpenHelix-Team/VLA-Adapter` ★2.1k — VLA 轻量适配
- `MarkFzp/openpi-zero` — OPEN-PI-ZERO 社区复现

---

## 方向 6：仿真、数据与平台

**API 查询：**
```
q=robotic+simulation+OR+"embodied+benchmark"+created:>YYYY-MM-DD
q="x-embodiment"+OR+"behavior+cloning"+dataset+robot+pushed:>YYYY-MM-DD
```

**经典仓库关注清单：**
- `Genesis-Embodied-AI/Genesis` ★28k+ — 生成式具身AI仿真（本周绝对焦点）
- `isaac-sim/IsaacLab` ★6.1k — NVIDIA 官方机器人学习框架
- `haosulab/ManiSkill` ★2.7k — GPU 并行操控基准（SAPIEN）
- `RoboTwin-Platform/RoboTwin` ★2.1k — 双臂数字孪生仿真平台
- `simpler-env/SimplerEnv` ★1k — 仿真评估真实策略
- `StanfordVL/BEHAVIOR-1K` ★1.4k — 斯坦福1K任务基准
- `google-deepmind/open_x_embodiment` — Open X-Embodiment 数据集

---

## 方向 7：人机交互与具身社会智能

**API 查询：**
```
q="human-robot+interaction"+OR+"shared+autonomy"+OR+"assistive+robotics"+created:>YYYY-MM-DD
q="physical+HRI"+OR+"intention+prediction"+robot+OR+"language-conditioned"+robot+pushed:>YYYY-MM-DD
```

**经典仓库关注清单：**
- `Healthcare-Robotics/` — 辅助机器人研究
- `Stanford-ILIAD/` — 共享自主
- `reHRC/` — 物理人机协作

---

## 仓库信息提取模板

```markdown
### [仓库名](GitHub链接)

- **简介：** 一句话描述（来自仓库 description）
- **语言：** Python / C++ / ...
- **Stars：** ★ XXXX（本周新增 +XX）
- **类型：** 🆕 本周新建 / 🔄 经典更新
- **更新亮点：** 本周主要变更（若有 Release Notes / commits 可参考）
- **所属方向：** 方向N — XXX
```

---

## GitHub 统计汇总格式

```markdown
| 方向 | 新建仓库数 | 更新经典仓库数 | 本周最高星仓库 |
|------|-----------|--------------|--------------|
| 感知与场景理解 | N | N | 仓库名 (★XXX) |
| 决策与规划 | N | N | 仓库名 |
| 控制与操作 | N | N | 仓库名 |
| 强化学习/世界模型 | N | N | 仓库名 |
| 智能体与大模型 | N | N | 仓库名 |
| 仿真、数据与平台 | N | N | 仓库名 |
| 人机交互 | N | N | 仓库名 |
```

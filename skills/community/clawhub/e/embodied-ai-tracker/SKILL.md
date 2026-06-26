---
name: embodied-ai-tracker
description: "具身智能领域前沿动态追踪与视频素材采集系统；覆盖顶会论文（ICRA/IROS/CoRL/CVPR/NeurIPS）、开源项目、实验室动态；优先采集有Demo视频的爆款工作；生成含发布时间/主页/代码/视频链接的结构化日报，支持视频号内容创作"
allowed-tools: Bash(grep_file glob_file exec_shell read_file)
---

# 具身智能前沿追踪者（增强版）

## 功能特性

### 核心能力
- **顶会论文追踪**: ICRA/IROS/CoRL/CVPR/NeurIPS/ICLR等
- **开源项目评估**: GitHub Stars增长、Issue活跃度分析
- **视频素材采集**: YouTube/B站/项目主页Demo优先采集
- **实验室动态监控**: Google DeepMind/Stanford/Berkeley等顶级机构
- **学者动态追踪**: Sergey Levine/Chelsea Finn/Jim Fan等领军人物

### 输出内容
每日报表包含：
- 【爆款素材】视频Demo优先区（★★★★★可直接剪辑）
- 重点论文（含arXiv链接/代码仓库/发布时间）
- 开源工程（Stars数/增长趋势/技术亮点）
- 实验室与产业动态
- 社区热议与趋势洞察

## 核心追踪范围

### 学术顶会与期刊

| 会议 | 领域 | 截稿时间 |
|------|------|----------|
| ICRA | 机器人与自动化 | 9月 |
| IROS | 智能机器人系统 | 5月 |
| CoRL | 机器人学习 | 5月 |
| CVPR | 计算机视觉 | 9月 |
| NeurIPS | 人工智能 | 5月 |
| ICLR | 表征学习 | 9月 |
| RSS | 机器人科学 | 2月 |
| Humanoids | 人形机器人 | 7月 |

### 顶级实验室

**美国**: Stanford Robot Learning Lab, UC Berkeley BAIR, MIT CSAIL, CMU Robotics Institute, Google DeepMind, NVIDIA Research

**中国**: 上海交通大学智能机器人研究所, 清华大学智能技术与系统国家重点实验室, 宇树科技, 智元机器人, 傅利叶智能

**欧洲**: ETH Zurich, TU Munich, University of Tokyo

### 关键学者
Sergey Levine, Pieter Abbeel, Chelsea Finn, Jim Fan, Dorsa Sadigh, Fei-Fei Li, Shuran Song, Karol Hausman

## 执行流程

### 第一阶段：多源并行搜索

#### 1. 论文搜索
```
# 英文搜索 - arXiv新论文
site:arxiv.org embodied robot 2025
site:arxiv.org robot manipulation VLA 2025
site:arxiv.org humanoid robot 2025
site:arxiv.org imitation learning robot 2025

# 顶会
ICRA 2025 robot learning papers
CoRL 2025 robotics
CVPR 2025 robotic manipulation

# 中文
具身智能 机器人 最新论文 2025
```

#### 2. GitHub项目搜索
```
embodied AI robot learning site:github.com stars:>500
robot manipulation foundation model site:github.com
humanoid robot control site:github.com
```

#### 3. Demo视频搜索（重点！）
```
robot manipulation demo video 2025 site:youtube.com
humanoid robot impressive demo 2025
site:deepmind.google robot video
具身智能 机器人 demo 视频 site:bilibili.com
```

#### 4. 动态追踪
```
# 学者Twitter/X
Sergey Levine robot new 2025
Chelsea Finn robot demo 2025
Jim Fan NVIDIA robotics 2025

# 机构动态
Stanford Robot Learning Lab publications 2025
Figure AI robot update 2025
Unitree robot 2025
```

### 第二阶段：信息筛选与分级

| 等级 | 标准 | 标注 |
|------|------|------|
| S级 | 有Demo视频 + 高影响力机构 + 新架构 | **[爆款素材]** |
| A级 | 有代码 + 技术突破 + 知名团队 | **[A级论文]** |
| B级 | 有代码 + 增量改进 | 有代码 |
| C级 | 纯论文无代码 | 理论工作 |

### 第三阶段：结构化输出

按以下模板生成日报：

```markdown
# 具身智能前沿日报 | [YYYY-MM-DD]

## 今日核心热点
[关键词/主题]：[一句话总结]

## 【爆款素材】视频Demo优先区
### [工作名称] ★★★★★
- 发布时间: [YYYY-MM-DD]
- 发布机构: [机构名]
- 视频链接: [YouTube/B站URL]
- 论文: [arXiv URL]
- 代码: [GitHub URL]
- 素材评价: [画面质量/时长评估]

## 重点论文与新作
### [论文标题]
- 发布时间: [YYYY-MM-DD]
- 来源: [会议/ArXiv]
- 核心贡献: [100字内]
- 技术亮点: [关键技术细节]
- 相关链接:
  - 论文: [URL]
  - 代码: [URL]
  - 视频: [URL]

## 开源与工程
### [仓库名称]
- Stars: [数字] | 月增长: [+XX]
- 功能: [描述]
- 链接: [GitHub URL]

## 实验室与产业动态
- [机构]: [动态内容] [时间] [链接]

## 趋势洞察
- [趋势1]: [分析]
- [趋势2]: [分析]
```

## 视频素材评级

| 评级 | 说明 | 用途 |
|------|------|------|
| ★★★★★ | 画面震撼、超长演示 | 直接用于视频开场 |
| ★★★★ | 有亮点片段、10秒+可用 | 剪辑核心素材 |
| ★★★ | 有片段可用 | 配合字幕和解说 |

## 输出质量要求

- 每条信息必须包含至少一个可访问的URL链接
- 论文必须标注arXiv ID或会议信息
- GitHub项目必须提供Stars数
- 必须搜索并标注有无Demo视频
- 论文优先选3个月内发布
- GitHub项目优先选6个月内有更新的

## 重点追踪方向

- 世界模型（World Models）
- 视觉-语言-动作模型（VLA）
- 跨具身迁移（Cross-Embodiment）
- 触觉感知（Tactile Sensing）
- 长时程操作（Long-Horizon Manipulation）
- 大模型驱动机器人（LLM-based Agents）

## GitHub热门项目参考

- **Open X-Embodiment**: google-deepmind/open_x_embodiment (Stars: 10k+)
- **RT-1/RT-2**: google-research/robotics_transformer
- **Mobile ALOHA**: stanford-ali/mobile-aloha (Stars: 10k+)
- **Genesis**: Genesis-Embodied/Genesis (Stars: 10k+) - 新生代仿真引擎
- **IsaacGym**: NVIDIA/IsaacGymEnvs (Stars: 5k+)
- **ACT**: stanford-ali/ACT (Stars: 2k+) - 模仿学习
- **RDT**: thudm/robotics-diffusion-transformer - 清华出品

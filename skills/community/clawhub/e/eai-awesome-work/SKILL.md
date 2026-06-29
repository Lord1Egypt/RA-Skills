---
name: eai-awesome-work
description: EAI Awesome Work 专栏 — 每周具身智能前沿工作速递。从 arXiv cs.RO 最新论文中筛选具身智能/机器人相关前沿工作，按主题分模块撰写深度技术推文，含完整摘要翻译、核心创新拆解、领域趋势洞察。触发词：EAI Awesome Work、具身智能前沿速递、本周具身论文、具身智能周刊、embodied AI weekly review、awesome embodied work。
agent_created: true
---

# EAI Awesome Work — 具身智能前沿工作速递

每周从 arXiv cs.RO/new 最新论文中精选具身智能前沿工作，按主题分模块撰写深度推文。输出 Markdown 文件。

## 触发条件

- 用户要求写 EAI Awesome Work 专栏
- 用户要求写本周具身智能前沿工作速递/周刊
- 用户说「awesome work」「具身论文汇总」等关键词

## 输出格式

文件命名：`Awesome_EmbodiedAI_工作速递_YYYYMMDD.md`

专栏标题格式：`EAI Awesome Work | [本期主题浓缩]`

副标题：`具身智能前沿工作速递 · Vol.[N] · YYYY.MM.DD`

## 执行流程

### Phase 1: 论文发现

1. **WebFetch** `https://arxiv.org/list/cs.RO/new` — 获取今日新提交论文完整列表
2. 同时 **WebFetch** `https://arxiv.org/list/cs.RO/2026-06` — 补充前几天可能漏掉的论文（按月归档页）
3. 从列表中人工筛选具身智能/机器人直接相关的论文（通常 12-20 篇）
4. 优先筛选标准：embodied AI / robot manipulation / VLA / humanoid / world model / WAM / locomotion / grasping / sim-to-real / multi-robot / safety

### Phase 2: 详细信息获取

对每篇筛选出的论文，**WebFetch** 其 arXiv 摘要页（`https://arxiv.org/abs/XXXX.XXXXX`），提取：
- 完整标题
- 全部作者 + 所属机构
- 核心创新/贡献（从摘要中提炼）
- GitHub 代码仓库 / 项目页面 URL（如有）
- 数据集 / 模型发布状态

### Phase 3: 主题归类

将论文归入 3-5 个主题板块，常见分类：

| 板块 | 关键词 |
|------|--------|
| 世界模型 & WAM | world model, world action model, video prediction, future generation |
| 安全 VLA | safety, safe RL, risk, uncertainty, failure detection |
| 操控与抓取 | manipulation, grasping, dexterous, affordance |
| 移动能力 | locomotion, navigation, parkour, walking |
| 协作与多智能体 | multi-robot, collaboration, bimanual, coordination |
| 策略学习方法论 | policy learning, RL, imitation, flow matching, representation |

如果某板块只有 1 篇论文，可合并到关联板块；如果有 4+ 篇，应作为独立板块并附小结。

### Phase 4: 行业动态补充（可选）

如果本期论文较少或需要增加行业视角，用 **WebSearch** 搜索补充新闻：
- 大额融资 / IPO
- 重要产品发布
- 会议动态
- 头部公司（NVIDIA/Figure/Tesla/Boston Dynamics/Apptronik）动态

### Phase 5: 推文撰写

按以下结构组织内容：

#### 开头
- **必须有吸引力**：用故事/类比/现象切入，不用"本周共有X篇论文"
- **点明本期核心信号**：1-2 句话告诉读者这篇文章为什么值得读
- 语气：有观点、有态度、不套话

#### 各板块正文
每个板块包含：

1. **板块标题** — 带 emoji + 中文概括
2. **板块导语** — 1-2 句话说明为什么这些文章放一起
3. **单篇论文** — 按重要度排序（🔴 必读 / 🟡 推荐）

单篇论文格式：

```
### 🔴/🟡 [中文核心一句话]

**机构 | 作者**

> **一句话**：用口语化的一句话解释核心思路。

**摘要翻译**：将英文摘要翻译为中文，保留技术细节但让中文读者能流畅理解。

**结果/亮点**：关键数字用表格或粗体突出。

> 🏷️ **研发团队**：XX 大学/公司（XX 组）
> 📎 **代码/项目页**：[https://...]() 或 未公开
```

4. **板块小结** — 2-4 句话串联本板块文章的逻辑关系

#### 趋势洞察
- **3 条趋势判断**：每条 2-3 句，有判断、有论据
- **重点团队追踪**：列出本周值得关注的团队及其信号
- **反向观察**：可以指出本期论文的共性不足（如代码开源率低）

#### 页脚
```
*本文基于 YYYY-MM-DD arXiv cs.RO/new 页面抓取 + 论文详情页自主研读编译。数据来源：arxiv.org、humanoid.press。*
```

## 写作原则

1. **翻译 > 复制**：英文摘要必须翻译为自然中文，不是机翻
2. **观点 > 列表**：读者来这里是看判断的，不是看目录的
3. **逻辑 > 堆砌**：论文之间要有串联，板块之间要有叙事线
4. **具体 > 抽象**：数字优于形容词，表格优于段落
5. **有人味**：可以有幽默、可以吐槽、可以有立场

## 参考模板

详细的写作模板和本期的完整示例见 `references/template.md`。

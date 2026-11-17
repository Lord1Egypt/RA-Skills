# anchor-spec（锚点体系）

**给 AI 编程 agent 的分级项目锚点——记忆投入与项目复杂度匹配，剩下的交给自动治理。**

> 即插即用的 skill/插件，适配 Claude Code、OpenClaw 及任何能读 Markdown 指令的 agent。零依赖，外加一个可选的 Python 脚本。

[English README](./README.md)

---

## 解决什么问题

AI agent 跨会话丢项目上下文。现有方案分两派：

- **记忆库派**（如 Cline Memory Bank）：每个项目一套全量文件，每次任务开始**全读所有文件**。能用——直到你同时开着 6 个项目，文件膨胀，而且没人删东西。
- **规格驱动派**（如 GitHub 官方 spec-kit）：擅长**动手前把事想清楚**，但不管执行期间的项目状态维护。

anchor-spec 占的是空位：**项目记忆是一个生命周期**——记多少跟项目规模匹配，一个自动 doctor 防止整个体系腐烂。

## 三个机制，一条因果链

**1. 分级判级——投入匹配复杂度（进场层）**

| 级别 | 适用 | 成本 |
|------|------|------|
| **T0** | 一次性任务、单会话完成 | 零。不建锚点，直接干 |
| **T1** | 可能跨会话但仍然轻 | 一张 SEED 种子卡，**≤10 行**（目标/产出/下一步/更新计数） |
| **T2** | 正式项目（四个升级信号任一触发） | 全套锚点：README **≤150 行硬上限** + `tasks/` |

升级信号显式化（项目名跨会话出现≥3次 / 文件>5 / 被其他项目引用 / 超2周仍在动）。**只升不降**——记忆跟着项目长，不抢跑。

**2. 三层信息模型——README 为什么敢薄（使能层）**

文件不按"主题"分，按**变化方式**分：

```
L3  快照层   README.md（≤150行）      状态→覆盖 / 地图→增量 / 背景→冻结 / 动态→滚动
L2  决策层   EVOLUTION.md              只追加不改写，记"选了什么、为什么"
                                        发现旧决策有误 → 追加"后来发现…"，不涂改历史
L1  流水层   每日 memory / 变更日志     只追加
```

状态段敢直接覆盖，是因为下面有 append-only 层兜着——历史一条不丢。这一条不变量让锚点**永久薄、永久新鲜**，不需要"文档清理周末"。

**3. 生命周期自动治理——半年后还好用（护城河）**

`anchor-doctor.py`（默认只读）持续做四件事：

- 30 天未动的锚点挂**冷藏横幅**（"恢复前先验证关键事实"）
- 90 天**归档**
- 完成的任务锚点 14 天内**蒸馏**——有留存价值的"为什么"提升进 EVOLUTION，任务文件本身删除
- 孤儿产出检测、README 肿胀检测、索引漂移检测

锚点是**资产不是合规义务**：有进，有出。

**附赠：恢复漏斗（读取协议=token 成本协议）**

不是"每次任务前全读所有文件"（那是烧钱协议），而是四步漏斗：README 状态段（30秒定位）→ 地图段（按需调档）→ EVOLUTION（决策背景）→ 流水考古（实在缺细节才去）。

## 快速开始

```bash
git clone https://github.com/<you>/anchor-spec.git
# Claude Code / OpenClaw：
cp -r anchor-spec/* ~/.claude/skills/anchor-spec/   # 或你的 agent 的 skills 目录
# 完事。下次你说"新项目"或"接着干"，skill 自动接管。
```

手动模式（不依赖 agent）：把 `references/templates.md` 的模板拷进项目，按 `references/rules.md` 的规则维护。

## 与同类方案的区别

**vs Cline/Roo Memory Bank**：Memory Bank 按主题拆文件、全量重读、没有删除路径——文件只增不减，这也是它头部衍生项目集体停更的病根。anchor-spec 按变化方式分层、分级投入、带自动出场机制。喜欢 Memory Bank 的话，anchor-spec 是不腐烂的那一版。

**vs GitHub spec-kit**：互补不竞争。spec-kit 管建什么（spec→plan→tasks），anchor-spec 管建到哪了。两者可以组合——spec-kit 的工件直接挂进锚点地图段。

**vs mem0 / Letta**：那些是记忆基础设施（向量库、检索）。anchor-spec 是文档协议——纯 Markdown，你的 agent 和三个月后的你自己都直接读。不冲突，可叠用。

## 包内清单

```
SKILL.md               agent 指令（判级 + 生命周期 + 恢复漏斗）
references/
  templates.md         SEED 卡 / T2 三层 README / 任务锚点三档模板
  rules.md             分层铁律 + INDEX + 蒸馏规则
  quality.md           自检清单 + 失败模式表
doctor/
  anchor-doctor.py     只读生命周期审计（冷藏/蒸馏候选/孤儿/肿胀/漂移）
LICENSE                MIT
```

## FAQ

**必须 Claude Code / OpenClaw 吗？** 不用。纯 Markdown + 一个可选 Python 脚本，任何能读文件的 LLM agent 都能跑，人也能跑。

**T1 长大了怎么办？** 四个显式升级信号 + 升级路径（SEED 并入 README 背景段）。不叫"迁移"，叫"生长"。

**doctor 会误删吗？** 不会。默认只读报告，所有写操作需显式开启（dry-run 优先）。

## 许可

MIT——随便用、随便 fork。如果它救了你的 agent 的记性，点个星让更多人看到。

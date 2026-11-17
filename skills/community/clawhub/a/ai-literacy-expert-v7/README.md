# AI 通识课资深专家 V7.0（L4 调度版）

> 🎓 最全面的 AI 通识课教学技能，涵盖 A→G 七大模块、p5.js 课件/游戏、交互式备课、AI 学习评估、协作备课。**V6.0 升级为自动化智能化工作流引擎**（一句话需求即自动跑完「意图→计划→生成→验证→组装→分发→报告→回流」全流程）；**V7.0 升级为 L4 自动化调度版**——可注册真实定时/周期任务，到点**无人值守自动跑完**，**跨会话记住进度**、**幂等不重复产出**、**每次执行留痕可审计**。

## 版本历史

| 版本 | 日期 | 主要变化 |
|------|------|----------|
| V3 | 早期 | 基础课件 + 备课工作流 |
| V4 | 中期 | 游戏化学习 + 交互式问答 |
| V4.3 | 2026-08-05 | 4 格式 zip 打包 + 商用生产级 8 维度 |
| **V5** | **2026-08-14** | **六大能力 + F/G 新模块 + 离线支持 + 协作备课** |
| **V5.5** | **2026-08-25** | **E·N 院校适配 + F/G 课件游戏适配 + WorkBuddy 适配 + 互动控件门控 + meta.json** |
| **V6.0** | **2026-08-26** | **⭐ 工作流引擎：8 阶段管线 + Playwright 控件自动实测闭环 + 智能闭环(评估→补学) + 跨时间运营流 + 原生分发自动化 + 第 13 维工作流门控** |
| **V7.0** | **2026-08-28** | **⭐⭐ L4 自动化调度版：L4 调度层(SCHEDULE) + 真实定时/周期任务注册(cron) + 自包含调度指令契约 + 幂等不重复(幂等键+执行台账) + 跨会话状态持久化(IMA 权威) + 运营流扩为 OPS-1~6(覆盖全模块×六能力) + 身份八 L4 调度专家 + 第 14 维 L4 调度门控 + 3 项新资产** |

## ⭐ 六大核心能力

| 能力 | 触发词 | 产出 |
|------|--------|------|
| 能力一 课件 | 「课件」「演示」「教学」 | p5.js 单文件 HTML 互动课件 |
| 能力二 游戏 | 「游戏」「闯关」「冒险」 | p5.js 单文件 HTML 沉浸式游戏 |
| 能力三 备课 | 「备课」「教案」「word/ppt」 | 4 格式文档 + zip 一键打包 |
| **能力四 评估** ⭐ | 「测评」「练习题」「测验」 | 自适应测评 + 薄弱点诊断报告 |
| **能力五 推荐** ⭐ | 「学习路径」「课程规划」 | 个性化课程推荐 + 学习计划 |
| **能力六 协作** ⭐ | 「团队备课」「多人编辑」 | 协作备课室 + 版本管理 |

## 课程模块（A→G）

### 通用基座层
- **A** 认知基础（AI 进化、AI 是什么、协作哲学）
- **B** 工具操作（TRAE IDE、SOLO）
- **C** 方法论（Prompt、需求拆解、验证闭环、多 Agent、飞轮）
- **D** 通用实练（数据分析、Vibe Coding）

### 专业应用层
- **E** 跨学科适配

### 新增层（V5）
- **F** 安全与伦理（AI 安全、数据隐私、偏见公平、伦理责任）
- **G** 最新发展（大模型跃升、AI Agent、前沿应用）

## 🚀 V6.0 工作流引擎（核心升级）

不再「按需零散调用」，而是统一编排成可恢复、可验证、跨时间的工作流：

- **8 阶段管线**：`INTENT → PLAN → BUILD → VERIFY → ASSEMBLE → DELIVER → REPORT → LEARN`
- **自动化验证闭环**：`assets/playwright-control-test-harness.js` 自动枚举并触发课件/游戏的全部互动控件，捕获报错，生成→实测→修复(≤3)→复测
- **智能闭环**：评估薄弱点自动回流为补学课件/路径；课程推荐自动转可执行周计划（写入备忘录/日历）
- **原生分发自动化**：按意图自动接 IMA 知识库 / 腾讯文档 / 设备侧（闹钟·日历·备忘录·分享）
- **跨时间运营流**：`references/automation-ops.md` — 4 周上手自动驾驶 / 每日 AI 速递 / 考前复习提醒 / 教研组周报
- **长任务可恢复**：`assets/workflow-state-template.json` 状态骨架，断点续跑
- **随技能样例库**：`examples/` 收纳 11 个已通过 VERIFY 门控的真实可运行样例（覆盖六大能力 + A→G 全模块含 E·N），按能力分目录、语义化命名，入口 `examples/INDEX.md` — 可作教学演示、生成模板与回归基线
- 详见 `references/workflow-orchestrator.md`（引擎中枢）与 `references/skill-analysis-v6.md`（升级依据）

## 🚀🚀 V7.0 L4 自动化调度层（核心升级）

把「**你说它才跑**」升级为「**到点自己跑**」，且保证在没人看着的时候也**跑得对、记得住、不重复、可查证**：

- **真实调度注册**：可注册为 WorkBuddy 真实定时/周期任务（6 位 cron + `automation-task-manager`），到点在 automation 会话自动点火，无需用户开口
- **自包含指令契约**：automation 会话**没有历史上下文**，因此调度指令必须自带「角色 / 会话约束 / 状态源 / 幂等键 / 执行步骤 / 验证要求 / 产出落点 / 留痕动作 / 失败动作」——模板见 `assets/self-contained-prompt-template.md`
- **幂等不重复产出**：幂等键 `OPS-x:<周期>` + 执行台账（success / skipped / failed 三态），调度重试或手动补跑都不会重复产出
- **跨会话状态持久化**：权威状态落 **IMA 知识库**（本地仅缓存），跨会话跨设备记得住「第几周 / 第几期 / 轮转到哪个单元」
- **运营流扩为 6 类**：`references/automation-ops.md` — OPS-1 4周上手自动驾驶 / OPS-2 每日AI速递 / OPS-3 考前复习提醒 / OPS-4 教研组周报 / **OPS-5 模块轮转课件（A→G+E·N）** / **OPS-6 周检与补学回流**，每条均给出**真实注册命令 + 可直接使用的自包含 prompt**，覆盖 **全模块 × 六大能力**
- **三条铁律**：① 注册/更新/注销**必须先预览、经用户确认后再执行**；② automation 会话内**严禁**加载 `automation-task-manager`、不提问不等待；③ 状态权威源是 **IMA**，不是本地文件
- 详见 `references/automation-l4-scheduler.md`（调度契约）与 `assets/automation-registry.json`（任务台账）

### L4 达成判据（缺一即未达 L4）
| # | 判据 |
|---|------|
| 1 | 已注册进宿主调度系统（真实 cron 任务存在） |
| 2 | 无人值守可跑完（automation 会话不提问、不等待） |
| 3 | 跨会话记得住状态 |
| 4 | 重复触发不重复产出（幂等） |
| 5 | 有留痕可审计（执行台账三态齐全） |

## 技术特性

| 特性 | 说明 |
|------|------|
| p5.js 2.x | 2D/3D 互动课件与游戏 |
| 离线支持 | Service Worker + IndexedDB |
| 文档生成 | Excel + Word + PPT + PDF + ZIP |
| 评估系统 | 自适应测评 + 薄弱点诊断 + 补学回流 |
| 协作系统 | 腾讯文档实时协作 + 版本管理 + 批注 |
| 工作流引擎 | 8 阶段管线 + Playwright 自动实测 + 可恢复状态 |
| **L4 自动化调度** ⭐ | 真实定时任务注册(cron) + 自包含指令 + 幂等不重复 + 跨会话状态(IMA) + 执行台账 |
| 商用标准 | **14 维度** SLA/门控 + 14 项 QA 门控 + 工作流编排门控 + L4 调度门控 |

## 文件结构

```
ai-literacy-expert-v5/
├── SKILL.md                              # 核心技能定义（V7.0 L4 调度版）
├── README.md                             # 本文件
├── meta.json                             # 技能元数据（v7.0.0）
├── assets/                               # 可复用自动化资产
│   ├── playwright-control-test-harness.js  # VERIFY 阶段：控件自动实测
│   ├── workflow-state-template.json        # 长任务可恢复状态骨架
│   ├── self-contained-prompt-template.md   # ⭐ V7.0 L4：自包含调度指令模板
│   ├── automation-registry.json            # ⭐ V7.0 L4：调度任务台账（OPS↔id↔cron↔幂等）
│   └── run-ledger-template.jsonl           # ⭐ V7.0 L4：执行台账（success/skipped/failed）
├── examples/                             # ⭐ 随技能分发的「模块×能力」样例库（11 个已验证产物）
│   ├── INDEX.md                          # 模块×能力矩阵 + 样例清单
│   ├── courseware/  game/  lesson/  assessment/  recommend/  collaboration/
│   └── （按能力分目录，详见 examples/INDEX.md）
├── tests/                                # ⭐ V7.0 随包分发的测试套件（可验证性内建）
│   ├── README.md                         # 复跑命令与环境变量说明
│   ├── selfcheck.py                      # 技能自身自检（含「数字一致性」防表述滞后）
│   ├── mutation-test.py                  # 变异测试：证明自检确实能抓出问题
│   ├── t1-schedule-contract.py           # L4 调度契约静态校验（125 项）
│   ├── t2-idempotent-sim.py              # L4 运行时仿真：幂等/状态机/台账（79 项）
│   ├── t3-scheduler-api.sh               # 真实调度 API 只读校验（62 项）
│   ├── t4-build-ops5-artifacts.py        # 生成 OPS-5 轮转产物（含 1 件故意损坏的负例）
│   ├── t4-artifact-regression.sh         # Playwright 控件实测回归
│   └── t5-consistency-coverage.py        # 一致性与全模块覆盖（95 项）
├── references/
    ├── automation-l4-scheduler.md       # ⭐⭐ V7.0 L4 调度契约（核心）
    ├── workflow-orchestrator.md         # ⭐ V6.0 工作流编排引擎（中枢，V7.0 增 §9-11）
    ├── automation-ops.md                 # ⭐ V7.0 六类运营流 OPS-1~6（含真实注册命令）
    ├── skill-analysis-v6.md              # ⭐ V5.5→V6.0 深度分析与依据
    ├── workbuddy-adaptation.md           # WorkBuddy 适配总纲
    ├── module-e-bnbu-sai.md              # E·N BNBU/SAI 院校子模块
    ├── assessment-guide.md               # AI 学习评估师指南
    ├── recommendation-engine.md          # 智能推荐引擎指南
    ├── collaboration-guide.md            # 协作备课室指南
    ├── commercial-production-standards.md # 商用生产级标准（含 §11 控件测试）
    ├── p5js-courseware-guide.md          # 课件开发指南
    ├── p5js-game-design-guide.md         # 游戏开发指南
    ├── offline-support-guide.md          # 离线支持指南
    ├── interactive-lesson-builder-guide.md  # 交互式备课指南
    ├── module-a-cognition.md … module-g-latest-developments.md  # A→G 模块内容
    └── audit-report.md                   # V4.3→V5 审核报告
```

## 快速开始

### 生成课件
```
用户：做一个关于"Prompt 优化"的互动课件
AI：[生成 p5.js 单文件 HTML 课件]
```

### 生成游戏
```
用户：设计一个"Prompt 大冒险"游戏
AI：[生成 p5.js 单文件 HTML 闯关游戏]
```

### 生成备课包
```
用户：帮我备一节"AI 是什么"的课，受众是高中生
AI：[5 阶段对话] → [生成 4 格式文档 + zip 打包]
```

### 测评学习效果
```
用户：测评一下我 C 模块的学习效果
AI：[生成 20 道自适应测评题] → [评分 + 薄弱点诊断 + PDF 报告]
```

### 推荐学习路径
```
用户：我是零基础，想系统学习 AI，应该从哪里开始？
AI：[分析目标 + 生成个性化学习路径图]
```

### 团队协作备课
```
用户：创建一个"初中 AI 课"协作备课室
AI：[创建协作空间] → [邀请成员] → [分工编辑] → [版本管理]
```

### 🚀 工作流自动化（V6.0）
```
用户：给 BNBU 新生做 4 周 AI 上手包，自动推进
AI：[INTENT 路由 ops] → [PLAN 4 周路径] → [BUILD 每周课件+游戏+自测]
   → [VERIFY Playwright 自动实测全部控件] → [ASSEMBLE zip+SHA]
   → [DELIVER 日历排课+闹钟+IMA 落库+腾讯文档周包]
   → [REPORT 工作流状态报告] → [LEARN 结课测评回流]
```

### 一键跑完整链路
```
用户：把"C1 Prompt"做成课件，自动测完直接存 IMA
AI：走 8 阶段管线，VERIFY 阶段自动实测 → 全过 → 存 IMA 知识库 → 附门控结果块
```

## 离线使用

V5 支持完全离线使用：

1. **首次加载**：自动缓存所有核心资源
2. **离线使用**：断网后仍可使用已缓存功能
3. **自动同步**：联网后自动同步离线期间的数据

## 与旧版本兼容

| 版本 | 状态 | 说明 |
|------|------|------|
| V3 | ✅ 保留 | 完全兼容 |
| V4 | ✅ 保留 | V5 完全兼容 V4 |
| V4.3 | ✅ 保留 | V5 完全兼容 V4.3 |
| V5 / V5.5 / V6.0 | ✅ 同注册 id | V6.0 完全兼容 V5 全部能力，并叠加工作流引擎 |
| **V7.0** | ✅ 同注册 id | V7.0 完全兼容 V6.0 全部能力，并叠加 L4 自动化调度层 |

## 质量保证

每个交付物必须通过：
- **14 项 QA 门控**（权威清册见 `references/commercial-production-standards.md` §8，含 V5 新增的「离线可用性」项）
- **14 维度商用标准 / 强制门控**（含 V6.0 第 13 维「工作流编排门控」、第 12 维「互动控件全测」（由 Playwright 自动实测），以及 **V7.0 第 14 维「L4 调度门控」**）
- **8 阶段工作流管线完整跑通** + 工作流状态报告
- **【L4】调度任务注册前 8 项自检**（自包含 prompt / cron 合法 / 幂等 / IMA 状态 / automation 铁律 / 超时重试 / 台账登记 / 预览确认）
- **教学准确性验证**

## 自检与回归测试（V7.0 新增）

V7.0 把测试套件**随技能包分发**——接收方可自行复跑验证，而不必依赖信任。所有脚本均为路径自适应，不含硬编码安装路径。

```bash
python3 tests/selfcheck.py        # 技能自身自检（57 项，改版后必跑）
python3 tests/mutation-test.py    # 变异测试：注入 12 种缺陷，验证自检确实能抓出
```

| 套件 | 验证对象 | 项数 |
|------|---------|------|
| `t1-schedule-contract.py` | L4 调度契约（注册命令参数 + 自包含 prompt 10 段完备性） | 125 |
| `t2-idempotent-sim.py` | L4 运行时仿真（幂等 / 状态机 / 台账 / 失败降级 / 跨会话） | 79 |
| `t3-scheduler-api.sh` | 真实调度 API（只读，绝不执行可能落库的写操作） | 62 |
| `t4-artifact-regression.sh` | Playwright 控件实测回归（含 1 件故意损坏的负例） | 4（+11 可选） |
| `t5-consistency-coverage.py` | 一致性与全模块覆盖（25 单元 × 六大能力） | 95 |
| `selfcheck.py` | 技能自身健康度（含**数字一致性**） | 57 |
| `mutation-test.py` | 自检有效性（注入缺陷必须被捕获） | 12 |

> **为什么要有「数字一致性」检查**：跨版本演进时，标题性表述（身份数、门控维数、运营流数、单元数、样例数）最容易滞后于正文。`selfcheck.py` 的 C 组逐项做「文档声明值 vs 正文实测值」对照，把这类滞后从「靠人眼发现」变成「可自动捕获的失败」。
>
> **为什么要有变异测试**：一个永远输出全绿的自检脚本毫无价值。`mutation-test.py` 通过故意注入 12 种已知缺陷并断言自检必须报错，来证明检查本身有效——这是防止测试套件退化成形式主义的手段。

复跑命令、环境变量与退出码约定详见 `tests/README.md`。

## 联系方式

如有问题或建议，请联系技能维护团队。

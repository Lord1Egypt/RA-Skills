# ARS Pipeline Orchestrator — 学术科研全流程编排技能包

> 源自开源项目 [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) 的通用可移植版本，已剥离原平台专属依赖，可在任意支持「SKILL.md + references/」技能目录规范的 Agent 网关中加载运行。

## 这是什么

一个**轻量级顶层编排调度器**（10 阶段全自动流水线）：自己不做实质性研究/写作/评审工作，只负责阶段检测、模式推荐、技能调度、状态跟踪与完整性验证。把调研 → 写作 → 评审三个独立技能包串成一条无缝流水线，并附材料护照（Material Passport）跨会话状态管理。

## 安装与依赖

1. 解压本压缩包，将 `ars-pipeline-orchestrator/` 文件夹放入你所使用平台的技能目录；
2. **将另外 3 个技能包解压到同一技能目录**（并列摆放）：
   - `ars-deep-research/`（调研包，驱动 Stage 1）
   - `ars-academic-paper/`（写作包，驱动 Stage 2/4/5）
   - `ars-academic-reviewer/`（评审包，驱动 Stage 3/3'）

编排器仅负责分阶段唤起上述 3 个独立技能；若某一技能包缺失，对应阶段会提示补装或改为人工在该技能内单独执行，不会静默失败。

## 触发方式（自然语言即可，无需命令）

| 场景 | 示例输入 |
|------|----------|
| 从零全流程 | "I want to write a research paper on the impact of AI on higher education" / "我想从选题开始完整做一篇研究论文" |
| 中途切入 | "I already have a paper, help me review it" |
| 收到审稿意见 | "I received reviewer comments, help me revise" |
| 跨会话续跑 | "resume_from_passport=<hash>"（配合已保存的材料护照） |

## 10 阶段流水线

Stage 1 RESEARCH（调研）→ Stage 2 WRITE（写作）→ Stage 2.5 INTEGRITY（完整性验证）→ Stage 3 REVIEW（同行评审）→ Stage 3' RE-REVIEW（复审）→ Stage 4 REVISE（修订）→ Stage 4.5 INTEGRITY（二次完整性验证）→ Stage 5 FINALIZE（定稿格式化）→ Stage 5.5 INTEGRITY（终检）→ Stage 6 PROCESS SUMMARY（人机协作过程记录）

每个阶段完成都会**主动征询用户确认**后才进入下一阶段。

## 目录结构

```
ars-pipeline-orchestrator/
├─ SKILL.md               # 主控调度（10 阶段状态机、调度规则、降级策略）
└─ references/
   ├─ *_agent.md          # 5 个编排/完整性角色 prompt（编排器、状态追踪、完整性验证等）
   ├─ guides/             # 调度协议（状态机、两阶段评审、抄袭检测、完整性闸门等）
   ├─ templates/          # 流水线状态看板模板
   ├─ examples/           # 3 个示例（全流程、中途切入、完整性失败恢复）
   └─ shared/             # 跨技能共享协议与数据契约
```

## 运行环境自适应

加载后先做环境自检（子 Agent 派生、并发、会话间通信、文件读取、视觉 OCR、兄弟技能在位情况），任一能力缺失自动降级（无派生能力时在当前会话内按阶段顺序扮演各技能），**不会中断任务**。

## 与其它 ARS 技能包的关系

另外 3 个技能包均可**单独安装、单独运行**，不需要本编排器；只有想跑「调研 → 写作 → 评审」全自动流水线时才需要安装本包。

## 版本

基于 ARS Academic Pipeline v3.21.0（2026-08-18）移植，阶段流程、完整性验证、两阶段评审与苏格拉底辅导机制完整保留。

---

## 移植溯源与更新指引

**原项目**：[imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)
（ARS，开源科研工具集；本包为剥离平台专属依赖后的通用可移植版）

**源目录 → 本包目录映射**（原项目变动时按此对照同步）：

| 原项目位置 | 本包位置 |
|------------|----------|
| `academic-pipeline/SKILL.md` | `SKILL.md`（主控，少量段落按改动原则重写） |
| `academic-pipeline/agents/*.md` | `references/*.md`（子角色文件，原样保留 + 附加通用学术规则） |
| `academic-pipeline/references/*.md` | `references/guides/*.md`（changelog 除外，未随包附带） |
| `academic-pipeline/templates/*` | `references/templates/*` |
| `academic-pipeline/examples/*` | `references/examples/*` |
| 仓库 `shared/` 中被引用的协议与数据契约 | `references/shared/`（文件名扁平化；`contracts/` 保留原子目录） |

**基本改动原则**（下次更新时遵循同样规则）：

1. **剥离平台依赖**：删除斜杠命令、工具调用前钩子、fork/spawn 专属调度、插件市场协议、运行时校验脚本引用（以文字规则与可选配置项替代），不改变任何学术流程语义；
2. **目录标准化**：重构为单 SKILL.md + references/ 结构，全部角色文件引用改为 `./references/...` 相对路径；
3. **跨技能引用**：统一改写为 `ars-xxx/...` 新包名前缀（4 包并列安装在同一技能目录时互相可解析）；
4. **保留核心价值**：智能体团队、运行模式、防幻觉约束、评审逻辑、数据契约（JSON Schema）完整保留，仅删除平台绑定层；
5. **新增通用机制**：运行环境自检与降级、子 Agent 调度必读角色文件、5 条通用学术强制规则（已同步嵌入全部角色文件）。

**同步更新方法**：原项目对应技能目录（`academic-pipeline/`）有版本变动时，先比对其 `SKILL.md` 与 `agents/` 的差异，按上表映射位置将变动内容合入本包，再按上述 5 条原则对新增文本做同样的平台依赖清理即可。

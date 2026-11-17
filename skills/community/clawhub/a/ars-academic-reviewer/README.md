# ARS Academic Reviewer — 学术论文多视角评审技能包

> 源自开源项目 [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) 的通用可移植版本，已剥离原平台专属依赖，可在任意支持「SKILL.md + references/」技能目录规范的 Agent 网关中加载运行。

## 这是什么

一个 **7 人多视角评审智能体团队**：模拟期刊编辑部完整评审流程（领域分析 → 五席评审团 → 编辑合成裁决），输出结构化评审意见、审稿报告与修改回应清单。支持多智能体辩论式评审。

## 安装

解压本压缩包，将 `ars-academic-reviewer/` 文件夹放入你所使用平台的技能目录（通常为 skills 目录），重启会话即可被识别。无需任何额外配置。

## 触发方式（自然语言即可，无需命令）

| 你想做的事 | 示例输入 |
|------------|----------|
| 完整评审 | "Review this paper" / "帮我评审这篇论文" |
| 聚焦方法论 | "重点从方法论角度评审这篇论文" |
| 快速预审 | "投稿前快速把把关" |
| 复审修订稿 | "这是修改稿和回复信，帮我复审是否真正解决了问题" |
| 引导式评审 | "带我一节一节过这篇论文" |
| 校准评分 | "校准一下评审标准的松紧" |

## 6 种评审模式

`full`（五席评审团完整评审）｜`methodology-focus`（双席方法论聚焦）｜`quick`（快速预审）｜`re-review`（修订稿复审）｜`guided`（引导式逐节评审）｜`calibration`（评分校准）

评审团席位：主编（EIC）、方法论评审、领域评审、多视角评审、魔鬼代言人 + 领域分析师（配置评审团）、编辑合成器（裁决输出）。

## 多智能体辩论评审

评审阶段可开启平行 Agent 辩论：各席位独立发言 → 跨会话交锋（默认上限 3 轮）→ 主控汇总输出**共识清单与分歧清单**。若运行环境不支持多会话通信，自动降级为单会话内模拟辩论（角色标签明确标注），效果等价。

## 目录结构

```
ars-academic-reviewer/
├─ SKILL.md               # 主控调度（模式路由、评审团组建、辩论协议、裁决标准）
└─ references/
   ├─ *_agent.md          # 7 个子角色 prompt（EIC、方法论评审、编辑合成器等）
   ├─ guides/             # 评审规范（质量量表、裁决标准、统计报告规范等）
   ├─ templates/          # 评审信模板（审稿报告、编辑决定信、修改回应）
   ├─ examples/           # 3 个示例
   └─ shared/             # 跨技能共享协议与数据契约
```

## 运行环境自适应

加载后先做环境自检（子 Agent 派生、并发、会话间通信、文件读取、视觉 OCR），任一能力缺失自动降级，**不会中断任务**。所有角色文件引用均为 `./references/...` 相对路径。

## 与其它 ARS 技能包的关系

可完全独立运行。常与 `ars-academic-paper`（写作包）组成「写作 → 评审 → 修订」闭环；全流程自动化另装 `ars-pipeline-orchestrator`（编排器包）。

## 版本

基于 ARS Academic Paper Reviewer v1.11.1（2026-08-15）移植，功能模式与角色配置完整保留。

---

## 移植溯源与更新指引

**原项目**：[imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)
（ARS，开源科研工具集；本包为剥离平台专属依赖后的通用可移植版）

**源目录 → 本包目录映射**（原项目变动时按此对照同步）：

| 原项目位置 | 本包位置 |
|------------|----------|
| `academic-paper-reviewer/SKILL.md` | `SKILL.md`（主控，少量段落按改动原则重写） |
| `academic-paper-reviewer/agents/*.md` | `references/*.md`（子角色文件，原样保留 + 附加通用学术规则） |
| `academic-paper-reviewer/references/*.md` | `references/guides/*.md`（changelog 除外，未随包附带） |
| `academic-paper-reviewer/templates/*` | `references/templates/*` |
| `academic-paper-reviewer/examples/*` | `references/examples/*` |
| 仓库 `shared/` 中被引用的协议与数据契约 | `references/shared/`（文件名扁平化；`contracts/` 保留原子目录） |

**基本改动原则**（下次更新时遵循同样规则）：

1. **剥离平台依赖**：删除斜杠命令、工具调用前钩子、fork/spawn 专属调度、插件市场协议、运行时校验脚本引用（以文字规则与可选配置项替代），不改变任何学术流程语义；
2. **目录标准化**：重构为单 SKILL.md + references/ 结构，全部角色文件引用改为 `./references/...` 相对路径；
3. **跨技能引用**：统一改写为 `ars-xxx/...` 新包名前缀（4 包并列安装在同一技能目录时互相可解析）；
4. **保留核心价值**：智能体团队、运行模式、防幻觉约束、评审逻辑、数据契约（JSON Schema）完整保留，仅删除平台绑定层；
5. **新增通用机制**：运行环境自检与降级、子 Agent 调度必读角色文件、5 条通用学术强制规则（已同步嵌入全部角色文件）。

**同步更新方法**：原项目对应技能目录（`academic-paper-reviewer/`）有版本变动时，先比对其 `SKILL.md` 与 `agents/` 的差异，按上表映射位置将变动内容合入本包，再按上述 5 条原则对新增文本做同样的平台依赖清理即可。

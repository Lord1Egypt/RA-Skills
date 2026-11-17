# ARS Academic Paper — 学术论文写作技能包

> 源自开源项目 [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) 的通用可移植版本，已剥离原平台专属依赖，可在任意支持「SKILL.md + references/」技能目录规范的 Agent 网关中加载运行。

## 这是什么

一个 **12 人论文写作智能体团队**：从选题接收到成稿格式化的全流程论文写作助手。涵盖 IMRaD 结构设计、论证构建、双语摘要、引用合规（APA 7 / 多格式切换）、统计图表规范、修订补丁、AI 使用披露声明、期刊投稿配置等。

## 安装

解压本压缩包，将 `ars-academic-paper/` 文件夹放入你所使用平台的技能目录（通常为 skills 目录），重启会话即可被识别。无需任何额外配置。

## 触发方式（自然语言即可，无需命令）

| 你想做的事 | 示例输入 |
|------------|----------|
| 完整写作 | "Write a paper on the impact of AI on higher education" / "帮我写一篇关于 XX 的论文" |
| 写作规划 | "帮我做这篇论文的写作规划" |
| 只出大纲 | "给我论文大纲" |
| 修订稿件 | "根据这些审稿意见帮我修订" |
| 中英摘要 | "帮我把摘要翻成双语的学术版本" |
| 文献综述章节 | "帮我写论文的文献综述部分" |
| 格式转换 | "把手稿转成 APA/期刊模板格式" |
| 引用检查 | "检查我全部引用是否合规" |
| AI 披露声明 | "帮我生成符合期刊政策的 AI 使用披露声明" |
| 反驳审计 | "预演审稿人最狠的十条质疑并准备回应" |

## 11 种运行模式

`full`（完整写作）｜`plan`（规划）｜`outline-only`（大纲）｜`revision`（修订）｜`revision-coach`（修订教练）｜`abstract-only`（摘要）｜`lit-review`（文献综述）｜`format-convert`（格式转换）｜`citation-check`（引用检查）｜`disclosure`（AI 披露声明）｜`rebuttal-audit`（反驳审计）

## 目录结构

```
ars-academic-paper/
├─ SKILL.md               # 主控调度（8 阶段流程、生成器-评估器契约、闸门规则）
└─ references/
   ├─ *_agent.md          # 12 个子角色 prompt（intake、结构架构师、执笔者、引用官等）
   ├─ guides/             # 写作规范（APA7、中文学术引用、修订协议、期刊政策等）
   ├─ templates/          # 论文模板（IMRaD、LaTeX、会议、案例研究等 11 套）
   ├─ examples/           # 10 个示例
   └─ shared/             # 跨技能共享协议与数据契约
```

## 运行环境自适应

加载后先做环境自检，任一能力缺失自动降级为单会话角色扮演，**不会中断任务**。支持接收 `ars-deep-research` 的研究交接材料（RQ Brief、文献库、综合报告），自动跳过冗余步骤。所有角色文件引用均为 `./references/...` 相对路径。

## 与其它 ARS 技能包的关系

可完全独立运行。上游接 `ars-deep-research`（研究成果可直接复用）；成稿后交 `ars-academic-reviewer`（评审包）做同行评审；全流程自动化另装 `ars-pipeline-orchestrator`（编排器包）。

## 版本

基于 ARS Academic Paper v3.3.1（2026-08-15）移植，功能模式与角色配置完整保留。

---

## 移植溯源与更新指引

**原项目**：[imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)
（ARS，开源科研工具集；本包为剥离平台专属依赖后的通用可移植版）

**源目录 → 本包目录映射**（原项目变动时按此对照同步）：

| 原项目位置 | 本包位置 |
|------------|----------|
| `academic-paper/SKILL.md` | `SKILL.md`（主控，少量段落按改动原则重写） |
| `academic-paper/agents/*.md` | `references/*.md`（子角色文件，原样保留 + 附加通用学术规则） |
| `academic-paper/references/*.md` | `references/guides/*.md`（changelog 除外，未随包附带） |
| `academic-paper/templates/*` | `references/templates/*` |
| `academic-paper/examples/*` | `references/examples/*` |
| 仓库 `shared/` 中被引用的协议与数据契约 | `references/shared/`（文件名扁平化；`contracts/` 保留原子目录） |

**基本改动原则**（下次更新时遵循同样规则）：

1. **剥离平台依赖**：删除斜杠命令、工具调用前钩子、fork/spawn 专属调度、插件市场协议、运行时校验脚本引用（以文字规则与可选配置项替代），不改变任何学术流程语义；
2. **目录标准化**：重构为单 SKILL.md + references/ 结构，全部角色文件引用改为 `./references/...` 相对路径；
3. **跨技能引用**：统一改写为 `ars-xxx/...` 新包名前缀（4 包并列安装在同一技能目录时互相可解析）；
4. **保留核心价值**：智能体团队、运行模式、防幻觉约束、评审逻辑、数据契约（JSON Schema）完整保留，仅删除平台绑定层；
5. **新增通用机制**：运行环境自检与降级、子 Agent 调度必读角色文件、5 条通用学术强制规则（已同步嵌入全部角色文件）。

**同步更新方法**：原项目对应技能目录（`academic-paper/`）有版本变动时，先比对其 `SKILL.md` 与 `agents/` 的差异，按上表映射位置将变动内容合入本包，再按上述 5 条原则对新增文本做同样的平台依赖清理即可。

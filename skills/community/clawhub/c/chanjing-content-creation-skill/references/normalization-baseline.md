# Chanjing Skill 规范化基线审计

本文记录 `chanjing-content-creation-skill` 在规范化改造前的基线状态，用于后续改造验收与回归对照。

## 审计范围

- 根入口：`SKILL.md`
- 运行时契约：`references/top-level-runtime-contract.md`
- 编排共约：`orchestration/orchestration-contract.md`
- 重点子技能：
  - `products/chanjing-ai-creation/chanjing-ai-creation-SKILL.md`
  - `products/chanjing-video-compose/chanjing-video-compose-SKILL.md`
  - `products/chanjing-customised-person/chanjing-customised-person-SKILL.md`
  - `products/chanjing-text-to-digital-person/chanjing-text-to-digital-person-SKILL.md`
  - `orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation-SKILL.md`
- 注册与门控：`manifest.yaml` 与根 `SKILL.md` frontmatter

## 基线问题清单

| ID | 问题 | 风险等级 | 影响层级 |
|---|---|---|---|
| B01 | 根 `SKILL.md` 混合了路由、执行细节与跨层规则，入口文档过重 | 高 | 根路由、L2/L3 |
| B02 | 根 frontmatter 的 `metadata.openclaw.requires` 仅声明 `anyBins=["ffmpeg"]`，与实际依赖覆盖不完整 | 高 | 门控、运行时 |
| B03 | `manifest.yaml` 与根 frontmatter 在门控表达上不一致（manifest 更完整） | 中 | 门控、维护 |
| B04 | L2 `Standard Workflow` 风格不完全统一（有表格流派，也有长步骤叙述流派） | 中 | L2 执行一致性 |
| B05 | `outcome_code` 语义虽已存在，但各文档对重试与降级触发条件粒度不一 | 高 | 错误恢复、用户体验 |
| B06 | 跨产品降级缺少统一“需用户确认”边界，容易出现自动跨路由行为 | 中 | 路由安全性 |
| B07 | 缺少统一术语字典（`task_id`/`video_id`/`output_url` 等）和回包语义映射 | 中 | 文档一致性 |
| B08 | 缺少最小 eval 基线与 PR 门禁，难以量化改造收益 | 高 | 质量治理 |

## 事实来源

- 根入口具备 `When to use / When NOT to use / 运行时契约`，但执行细节较多。
- `orchestration/orchestration-contract.md` 已定义 `outcome_code`，但未形成跨文档强约束模板。
- `manifest.yaml` 中 runtime/env/permissions/metadata 比根 frontmatter 更丰富。
- 部分 L2 已采用“脚本名 + 输入 + 输出 + 下一步 + 失败分支”表格，具备统一基础。

## 变更影响矩阵（用于后续每次改动评估）

| 变更类型 | 受影响文件 | 需要同步检查 |
|---|---|---|
| 根路由规则调整 | `SKILL.md` | `orchestration/orchestration-contract.md`、L2/L3 路由引用 |
| 门控或依赖调整 | `SKILL.md` frontmatter、`manifest.yaml` | `references/top-level-runtime-contract.md` |
| 错误语义调整 | `orchestration/orchestration-contract.md` | 各 L2/L3 `Standard Workflow` |
| Workflow 模板统一 | 各 `*-SKILL.md` | `orchestration/README.md` 与根约束 |
| 评测或门禁新增 | `evals/`、`references/` | 根 `SKILL.md` 的治理章节 |

## 本次改造验收目标

1. 根路由聚焦边界，执行细节下沉到子技能或 references。
2. frontmatter 与 manifest 门控对齐，运行时契约描述一致。
3. L2/L3 workflow 使用统一模板，失败分支与 `outcome_code` 显式映射。
4. 增加可执行的最小 eval 集与 PR 门禁清单。

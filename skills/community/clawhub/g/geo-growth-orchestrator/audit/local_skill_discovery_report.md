# Local Skill Discovery Report

本报告只基于本地目录文件生成，未使用 ClawHub 线上链接作为源码依据。

## 执行结论

- 已发现并登记 9 个相邻 GEO Skill。
- registry 中所有 `relative_path` 均为相邻目录路径，并且均能在本地找到对应 `SKILL.md`。
- 本轮已修正上一轮 registry 中几个输出文件命名不一致问题，尤其是知乎输出文件名、CSDN `csdn_code_examples.md`、以及 Doubao / DeepSeek 审计 Skill 的报告型输出。
- 当前环境不能把这些相邻目录作为可直接触发的运行时 Skill 自动调用，因此 Spanish Ham demo 使用 `mock_orchestration_demo`，并生成 handoff packets 供人工复制到对应 Skill 执行。

## 已发现的相邻 Skill

| skill_id | display_name | relative_path | 路径存在 | SKILL.md 存在 | 建议统一 skill_id | registry 是否需要修正 | 备注 |
|---|---|---|---|---|---|---|---|
| `brand-knowledge-base-builder` | Brand Knowledge Base Builder | `../Knowledge-Base-Builder/brand-knowledge-base-builder` | 是 | 是 | `brand-knowledge-base-builder` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `doubao-geo-audit-skill` | Doubao GEO Audit Skill | `../geo-analysis-doubao` | 是 | 是 | `doubao-geo-audit-skill` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `deepseek-geo-audit-skill` | DeepSeek GEO Audit Skill | `../deepseek-geo-audit-skill` | 是 | 是 | `deepseek-geo-audit-skill` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `deepseek-geo-tool` | GEO Tool DeepSeek | `../GEO tool-deepseek` | 是 | 是 | `deepseek-geo-tool` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `ai-geo-content-generator` | AI GEO Content Generator | `../AI-geo-content-generator` | 是 | 是 | `ai-geo-content-generator` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `zhihu-geo-draft-assistant` | Zhihu GEO Draft Assistant | `../zhihu-geo-draft-assistant` | 是 | 是 | `zhihu-geo-draft-assistant` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `toutiao-geo-draft-assistant` | Toutiao GEO Draft Assistant | `../toutiao-geo-draft-assistant` | 是 | 是 | `toutiao-geo-draft-assistant` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `csdn-geo-draft-publisher` | CSDN GEO Draft Publisher | `../csdn-geo-draft-publisher` | 是 | 是 | `csdn-geo-draft-publisher` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |
| `juejin-geo-draft-publisher` | Juejin GEO Draft Publisher | `../juejin-geo-draft-publisher` | 是 | 是 | `juejin-geo-draft-publisher` | 否 | expected_outputs 与本地 SKILL.md 输出描述一致 |

## 缺失的 Skill

无。

## 路径不一致或命名注意项

- 用户曾提到 `../Knowledge-base-Builder/SKILL.md`，本地未发现该路径；实际可用路径为 `../Knowledge-Base-Builder/brand-knowledge-base-builder/SKILL.md`。
- `AI-geo-content-generator` 是目录名，建议 registry 内统一使用 skill_id `ai-geo-content-generator`。
- `deepseek-geo-audit-skill` 是报告型审计 Skill，`GEO tool-deepseek` 是 API 探针工具，建议保持两个独立 skill_id，避免把非 API 审计和 API 实测混为一类。

## expected_outputs 对齐检查

- 当前 registry 的 `expected_outputs` 已与本地 `SKILL.md` 输出描述对齐。

## 当前 registry 是否需要修正

当前不需要继续修正。后续如果相邻 Skill 新增真实脚本输出或 JSON 输出，应同步更新 `registry/geo_skill_registry.json`。

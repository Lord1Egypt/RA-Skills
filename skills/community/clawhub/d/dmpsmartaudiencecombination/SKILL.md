---
name: 明日DMP智能组合圈人
description: 基于用户自然语言投放需求，按"需求解析→标签召回→画像补全→质量排序→用户选择→Overlap（仅MUST vs 可选）→递进组合→创建组合人群"的循序渐进流程，输出可直接用于明日DMP组合人群（audienceType=2）的标签组合规则与人群包创建参数。
metadata:
  version: 1.1.0
---

# 步骤导航


## 🔑 前置鉴权检查

> 任何圈人步骤执行前，必须先完成：鉴权技能安装检查 → 凭证检查/配置。

### 0.1 检查鉴权技能是否已安装
- 如果检测到未安装，必须向用户展示如下提示并等待回复（是/否）：

```
⚠️ 检测到您尚未安装【明日DMP鉴权技能】

该技能负责管理 API 凭证（AK/SK）、生成签名，是使用本功能的必要前提。

是否自动下载并安装？

是 - 立即安装
否 - 取消本次操作

请回复：是/否
```

- 用户回复“是”：执行安装（同口径：openclaw skills install mingdata-dmp-auth），安装成功后继续下一步；安装失败则引导用户手动安装（展示 ClawHub 链接与步骤）并终止流程。
- 用户回复“否”：提示已取消，并终止流程。

### 0.2 检查凭证是否存在
- 凭证文件路径：`~/.mingdata_dmp_credentials`
- 若凭证不存在或不完整，必须向用户展示“凭证获取指南”并要求按固定格式提供 AK/SK（禁止在对话中回显/展示AK/SK明文）。
- 用户提供后：运行 `scripts/setup_credentials.py <AK> <SK> [BASE_URL]` 写入凭证，并再次运行 `scripts/preflight_check.py` 验证有效；通过后才可进入 Step 1。


> 目标：让AI“不会丢步骤”。SKILL.md 只保留：入口导航 + 卡点/红线清单；细节由脚本硬执行。

**ClawHub 手动安装入口（与 4-1 口径一致）**：
- https://clawhub.ai/mingri26/mingdata-dmp-auth



## ✅ Step2 之前的“防漏要求”（强制）

> 目的：避免用户需求点未落入schema，导致候选召回/Step6分组缺维度（常见：兴趣偏好未入schema）。

- 生成/更新 `schema.json` 时，必须确保用户需求点“可被执行、可被对账”：
  - **任何用户提到的“点”必须进入结构化字段**；若暂时无法落字段，必须先进入 `extra.original_points` 兜底，禁止丢失。
  - 若用户明确提到“兴趣/偏好/品类/类目”，但 `interest` 为空，视为缺失，必须补齐或追问。
  - 若用户诉求涉及渠道/终端/时间窗/排除老客等，建议显式写入schema（或兜底进 `extra`），避免后续流程无法覆盖。

- 参考资料（按需加载）：
  - `references/需求到schema检查表.md`
  - `references/schema模板_防漏版.json`

## A. 唯一入口（全流程强制）
- **全流程驱动（唯一入口）**：`scripts/流程驱动.py`
  - 作用：串联 Step 0→14，并在关键卡点（Step2/6/6.5/7/8.5/9.5/13）强制输出交互要求；缺少用户确认时硬拦截，禁止跳步。
  - 输入：`schema.json`（建议包含 `_raw_text`）
  - 输出目录（由 `--out-dir` 指定）：产出 tag_pool / coverage / probe / queries / candidates / merged / diag / step6_ranked / overlap / plans 等全链路文件。
  - 说明：允许候选召回与诊断独立运行，但**任何“创建人群/Overlap/最终创建”相关步骤禁止绕过驱动器直接调用脚本**。
  - 交互约束：在用户未对Step6“展开/跳过”做出选择前，只允许输出“是否展开Step6候选明细”的询问，不允许输出任何Step7的选择建议或组合方案。

### 回放模式（保证同需求二次运行候选一致）
- 使用 `--replay-from <上次输出目录>`：直接复用上次产物（tag_pool/queries/candidates/merged/diag），避免二次运行因重跑/参数调整产生差异。

## B. 全流程步骤导航（Step → 脚本 → 输入/输出）
| Step | 目标 | 脚本 | 主要输入 | 主要输出 |
|---|---|---|---|---|
| 0 | 前置校验（凭证/环境/资产） | `scripts/preflight_check.py` | - | 校验结果 |
| 1-2 | 需求解析/确认（对话产出schema） |（对话）| 用户需求 | `schema.json` |
| 3 | 拉取可用标签池（tag/list） | `scripts/query_tag_list.py` | - | `tag_pool.json` |
| 4 | 召回候选标签（稳健版） | `scripts/recall_candidates_pipeline.py` | `schema.json` | `merged_candidates.json` + `recall_diag.json` |
| 5 | 画像补全（补覆盖率/量级等） | `scripts/tag_profile_enrich.py` | `merged_candidates.json` + 指标表 | `candidates_enriched.json` |
| 6 | 分组推荐（按维度展示候选） | `scripts/rank_candidates.py` | `candidates_enriched.json` | `step6_ranked.json` |
| 7 | 用户选择（MUST/PREFERRED/OPTIONAL/EXCLUDE） |（对话）| `step6_ranked.json` | must/preferred/optional/exclude |
| 8 | 冲突检测（静默；有冲突才提示） | `scripts/tag_hierarchy.py` / `scripts/tag_relation.py` | 选择结果 | 冲突报告（如有） |
| 8.5 | 执行口径确认（trackType/idTypes） | `scripts/confirm_execution_params.py` | - | 参数确认提示 |
| 9 | 创建MUST基准人群并取量级 | `scripts/create_must_baseline.py` | MUST + 口径 | audienceId_M + amount |
| 10 | Overlap（M∩可选） | `scripts/analyze_overlap.py` | M基准+可选 | overlap.json |
| 11 | 扩缩量分析 | `scripts/analyze_scale.py` | overlap.json | scale_report |
| 12 | 组合方案生成 | `scripts/generate_plans.py` | must/preferred/optional + overlap | plans.json |
| 13 | 方案确认（强制卡点） |（对话）| plans.json | 最终方案 |
| 14 | 创建最终组合人群 | `scripts/create_combined_crowd.py` | 最终方案 + 口径 | audienceId/任务状态 |

## C. 必须遵守的“卡点/红线”（短清单）
1. **候选标签只能来自 `tag_pool.json`（tag/list）且 `isDirectory=1`**。
2. **禁止编造** tagId/标签名/量级/覆盖率/Overlap；必须来自脚本输出或接口返回。
3. **默认不展开明细**；只有用户明确说“展开/展开标签详情”才展开表格明细。并且在用户未对Step6“展开/跳过”做出选择前，禁止输出任何Step7的MUST/PREFERRED/OPTIONAL/EXCLUDE推荐或组合建议。
4. **Step 8.5：trackType/idTypes 必须由用户确认**；未确认不得创建人群包。
5. **Step 13：方案确认是强制卡点**；未确认不得执行最终创建。
6. **三方标签仅提示申请入口，不参与组合创建/Overlap**。

## D. references（可选查阅）


## E. 规则表达口径（务必遵守）
- **推荐口径：二维 OR-groups**
  - `[[a,b],[c],[d,e]]` 表示：`(a OR b) AND c AND (d OR e)`
  - 组内为 OR、组间为 AND。
- Step7 的 `must` 可以直接使用二维 OR-groups（强烈推荐）；脚本 `create_must_baseline.py` 已支持该格式。
- 即使默认偏好“不展开明细”，Step6 结束后也必须显式询问一次“展开/跳过”，才允许进入 Step7。

- `references/api_reference.md`
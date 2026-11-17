---
name: feature-retcon
description: 当用户需要推翻或修改一个已推进到需求、设计、任务、实现或验证阶段的功能决定时，先只读评估影响，确认后再逐层追平权威产物，并提供可验证、可恢复的执行边界。
---

# 后悔药

把用户确认的功能变更视为一次 **retcon**：重写当前权威态，而不是给旧结论追加补丁。本次只推进到授权上限；整轮达到闭环终点并以零未解释残留通过验收后才关闭。

## 门禁

- 将没有现存追平契约的调用限定为只读评估；评估完成后结束本轮对话，等待用户确认。
- 只在用户明确确认变更断言、目标阶段、可写工作根、删除清单和已披露风险后修改文件。
- 将未获授权的根保持只读。执行中发现实质范围扩张时暂停并重新确认。
- 在每次修改、创建或删除目标文件前调用恢复脚本登记写前状态；登记成功后才执行该次修改。
- 分开记录本次执行上限 `target_stage` 和整轮闭环终点 `completion_stage`。“先到设计”“下一步再实现”是阶段性暂停，保留同一契约、轮次和原始恢复日志。
- 将契约存在视为未完成轮次。通过关闭证据校验后，用 `close` 显式关闭；不直接删除契约。
- 保持终态式权威文档：当前有效产物只描述新目标，历史证据留在明确的历史载体中。

## 读取路线

执行对应分支前完整读取指定参考文件：

- 每次评估：读取 [assessment.md](references/assessment.md) 和 [stage-gates.md](references/stage-gates.md)。
- 用户确认后、继续轮次或恢复轮次：读取 [contract-schema.md](references/contract-schema.md)。
- 关闭轮次前：读取 [closure-evidence.md](references/closure-evidence.md)，逐项核对完成或恢复证据。
- 目标包含任务阶段：读取 [task-rebuild.md](references/task-rebuild.md)。
- 检测到项目规格工具、Hook 或多个工作根：读取 [spec-kit-adapter.md](references/spec-kit-adapter.md)。
- 需要校准边界或解释编号规则：读取 [case-catalog.md](references/case-catalog.md)。

## 步骤 1：定位轮次与权威态

先搜索候选权威根中的 `RECONCILIATION.md`。发现契约时，运行：

```bash
python3 <skill-dir>/scripts/contract.py status <authority-root>/RECONCILIATION.md
python3 <skill-dir>/scripts/contract.py verify <authority-root>/RECONCILIATION.md
```

将该调用路由为继续、重新评估或停止并恢复；范围重叠的新轮次保持阻塞。没有契约时，按权威解析顺序确定唯一权威根，无法排除多个候选时让用户裁决。

完成标准：已找到唯一权威根，或已报告全部候选及其证据并等待用户裁决；现存契约的状态和允许动作已明确。

## 步骤 2：执行只读评估

构建语义阶段和产物依赖图，收集工作根、版本状态、冲突、基线验证、删除候选、Hook、副作用、敏感候选与残留签名。量化每个可选目标阶段的文件、仓库、接口、任务、测试和验证影响，给出一个有理由的推荐。

按 [assessment.md](references/assessment.md) 的固定结构交付评估。不得创建契约、修改权威产物、运行写入型命令或把建议当成授权。以一个确认请求结束当前调用。

完成标准：评估的全部固定栏目均有结论或明确的未知项；本次调用没有产生文件、Git 或外部系统写入；用户尚未确认时保持停止。

## 步骤 3：锁定追平契约

把用户确认的全部内容写入契约：被推翻行为、当前目标、保持不变、排除项、兼容与迁移影响、执行上限、闭环终点、可写根、删除清单、冲突处置、Hook、副作用以及敏感或大载荷授权。

用脚本创建契约：

```bash
python3 <skill-dir>/scripts/contract.py init <authority-root> \
  --target-stage <stage> \
  --completion-stage <stage> \
  --version-control <git|none> \
  --baseline-ref <ref> \
  --writable-root <root>
```

按需重复 `--writable-root`；无 Git 时省略 `--baseline-ref`。补全契约正文，运行相关验证取得基线，再执行 `verify`。

完成标准：契约权限为 `0600`，未被 Git 跟踪或暂存；确认内容全部持久化；验证基线可复现；任何未处置冲突仍保持阻塞。

## 步骤 4：逐层收敛

从需求开始，只推进到已确认目标阶段。每层先更新上游，再验证当前层；下游暴露上游缺陷时回流修正，并重新计算受影响下游。

每次修改目标文件都执行写前协议：

```bash
python3 <skill-dir>/scripts/contract.py prepare <contract> --path <file>
# 修改、创建或删除该文件
python3 <skill-dir>/scripts/contract.py applied <contract> --path <file>
```

敏感文件和超过载荷门槛的文件，只能在契约记录对应确认后使用脚本给出的显式选项继续。将闭包补充写入契约后继续；将实质范围扩张写入契约、设置 `blocked` 并等待重新确认。

完成标准：目标阶段及全部上游阶段逐层通过 [stage-gates.md](references/stage-gates.md)；每次文件变更都有连续日志；依赖图、删除清单和验证结果与实际修改一致。

达到执行上限但尚未达到闭环终点时，完成本次验证和水位更新，记录已完成、剩余工作和下次所需授权，运行 `status <contract> --set paused` 并结束本次调用。继续时在同一契约中登记新授权，保留原 `round_id` 和全部恢复日志。

## 步骤 5：验证当前权威态

运行项目原生检查和确定性静态检查。扫描词法与行为残留签名，对每个命中分类为已替换、明确历史证据或与本轮无关。验证新需求能够沿依赖图追踪到目标阶段，并更新追平水位和阶段陈旧状态。

失败的归因和处置严格采用 [stage-gates.md](references/stage-gates.md)。必要验证无法运行、失败无法归因或存在未解释命中时，把契约状态设为 `blocked`。

完成标准：所有必需验证通过或有证据证明失败既有且无关；残留签名零未解释命中；机械校验返回 `valid: true`。

## 步骤 6：关闭或保留契约

正常完成时，先证明整轮闭环终点及全部上游门槛通过，且剩余工作为零；逐项核对并准备独立关闭证据，再运行：

```bash
python3 <skill-dir>/scripts/contract.py verify <contract> --mark-ready --evidence <closing-evidence.json>
python3 <skill-dir>/scripts/contract.py close <contract>
```

机械 `valid: true` 只证明恢复日志一致；只有重新核验后的 `close_ready: true` 才允许关闭。清单勾选不能代替证据。

用户暂停或交接时保留契约。只有用户明确要求撤销本轮修改时运行 `restore`；它停在 `restored`，复验基线和引用后按恢复证据执行相同关闭命令。失败或证据不足时保留契约并报告阻塞。

最后在对话中报告修改与删除数量、验证结果、残留扫描、追平水位、阶段陈旧状态和各工作根状态。不得自动初始化 Git、暂存、提交、重置、改写历史、推送或调用外部系统。

完成标准：`close` 成功删除契约；闭环终点的权威态唯一、自洽、可验证且零未解释残留，或撤销后基线已复验；未获授权的根和用户无关修改保持不变。

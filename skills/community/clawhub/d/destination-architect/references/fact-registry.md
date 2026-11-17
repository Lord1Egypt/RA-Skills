# Reference：关键事实登记（跨文件一致性）

> 解决 S11（跨文件事实一致性）：同一事实散落多文件，改一处漏一处会导致内部版本漂移。
> **修改前先 `grep` 该事实的全部出现位置，再统一修改。**

## 关键事实表（唯一事实源）

| 事实 | 规范值 | 允许表述 | 禁止的过时表述 | 主要出现位置 |
|------|--------|---------|---------------|-------------|
| 工作流步数 | **10 步（Step 0–9；0–8 判断，9 出案）** | "10 步""Step 0–9" | "9 步""Step 0–8""7 步" | SKILL.md、README.md、workflows/*、examples/case-study.md |
| 反向审查轮次 | **4 轮** | "4 轮专家级审查" | "3 轮""5 轮" | SKILL.md、core/critic-engine.md、workflows/failure-analysis.md |
| 失败风险类别 | **6 类** | "六类风险" | "5 类""7 类" | SKILL.md、core/critic-engine.md、workflows/failure-analysis.md |
| 硬门禁 | **G1–G8** | "G1–G8" | "G1–G6""G1–G5" | SKILL.md、README.md、core/*、workflows/*、templates/* |
| 证据标签 | **实测 / 引用 / 假设 / 未知（4 类）** | 4 个标签 | 新增/删除标签 | SKILL.md、core/information-discipline.md、templates/business-model.md |
| 参数槽格式 | **`{{参数:名称}}`** | 该格式 | 用单点假数替代 | SKILL.md、core/information-discipline.md、core/financial-model.md、templates/proposal.md |
| 策划案落地要件 | **4 项（实施 / 财务 / 组织合规 / 空间招商）** | "四大落地要件" | 增删要件 | SKILL.md、README.md、workflows/proposal-assembly.md、templates/proposal.md、scripts/check_gates.py |
| 能力模块编号 | **M1–M10** | "M1"…"M10" | 跳号或重号 | SKILL.md、README.md |
| 核心公式变量 | **5 个（乘法关系）** | 5 变量 | 增删变量 | SKILL.md、README.md |
| 专家自我反思问数 | **8 问** | "8 个问题" | "6 问""7 问" | core/critic-engine.md、SKILL.md |
| 旗舰机制 | **最小成本证伪器** | 该名称 | "方案生成""模板套用" | SKILL.md、README.md、core/falsification-engine.md |

## 维护约定

1. **改前扫全量**：修改上表任一事实前，先执行 `grep -rn "<关键词>" .` 定位所有出现位置。
2. **改后自检**：用 `grep -rn "9 步\|Step 0–8\|6 问\|G1–G6"` 确认无残留过时表述。
3. **新增事实**：若引入新的跨文件关键事实，先在本表登记，再落地到各处。
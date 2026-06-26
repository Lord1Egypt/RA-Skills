# Handoff Spec — 交接文档格式规范

> 所有跨 Agent 文档传递必须使用本规范。首钢吉泰安项目已验证的六字段头部 + YAML frontmatter 使其可机器解析。

## YAML Frontmatter（必须）

```yaml
---
schema_version: "1.0"
document_type: handoff  # handoff | audit | research | deliverable | decision
task_id: "SG-PPT-v4-audit"  # 项目内唯一ID
created: "2026-04-10T13:37+08:00"
sender:
  agent: claude
  role: content-reviewer
receiver:
  agent: codex
  role: execution
status: submitted  # submitted | working | input-required | completed | failed
priority: P0  # P0=阻塞 | P1=重要 | P2=优化
depends_on: ["SG-PPT-v3-build"]
produces: ["SG-PPT-v4-build"]
forbidden_terms_checked: true
---
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `document_type` | ✅ | 决定本文件被哪种 Agent 读取 |
| `task_id` | ✅ | 格式：`{项目前缀}-{阶段}-{序号}`，如 `SG-RES-G1` |
| `sender / receiver` | ✅ | Agent ID + role，对应 AGENT_REGISTRY.yaml |
| `status` | ✅ | 任务状态机六态之一 |
| `priority` | ✅ | P0=人类必须审批；P1=Agent执行后人类复核；P2=Agent全自动 |
| `depends_on` | 推荐 | 上游任务ID列表，用于编排者追踪依赖 |
| `produces` | 推荐 | 产出任务ID列表，用于编排者追踪下游 |
| `forbidden_terms_checked` | ✅ | true = 本文档已过禁用词扫描；false = 待扫描 |

## Markdown 正文（八节）

### 第一节：目标
一句话说明本次交接要达成什么。格式：`{动作} → {产出}`，如"将PPT v3修订为v4审核收口版"。

### 第二节：当前状态
上游做到哪了。包括：已完成的所有关键产物、已达成的关键决策。

### 第三节：来源依据
已做的决策及理由。格式：
- **决策** + **理由** + **决策者**
- 引用 `DECISION_LOG.md` 中的 `decision_id`

### 第四节：上游依赖
接收者必读的文件路径（精确到文件名）。格式：
- 路径：`相对项目根目录/文件名.md`
- 每份文件一行，说明"读什么"

### 第五节：下游产物
接收者必须产出的文件路径（精确到文件名）。格式：
- 路径：`{目录}/{产出文件名}`
- 如有多个版本，明确哪个是最终路径，哪个是回退路径

### 第六节：接手建议
具体执行步骤（非聊天摘要）。格式：
1. 步骤一
2. 步骤二
3. ...

每步骤格式：`动作 + 目标 + 参照文件`

### 第七节：约束与禁区
不能做的事。引用 `FORBIDDEN_TERMS.yaml`：
- **禁用词**：不得出现 G1/G2/G3/G4/E-6/FMP 等内部代号
- **高风险表达**：政策金额须标注"正式申报前待核"；不预设上市路径
- **其他约束**：任何修改必须记录在修订日志中

### 第八节：验证标准
产出如何被判定为"合格"。格式：
```
✅ 通过条件：
1. 产物已写入约定路径
2. 禁用词扫描通过（无 P0 违规）
3. 页数 = {N} 页
4. 图表文件均已嵌入
5. 修订日志已更新

❌ 退回条件：
- 发现任何 P0 禁用词违规
- 产物未写入约定路径
- 页数不符
```

## 目录结构约定

每个项目交接文档集中存放在 `00_pipeline/handoffs/`：
```
项目根目录/
└── 00_pipeline/
    └── handoffs/
        ├── SG-RES-G1-to-G2.md      # 调研专题交接
        ├── SG-FW-to-EX.md          # 框架→执行交接
        ├── SG-EX-to-AU-v4.md       # 执行→审核交接
        └── SG-AU-to-IT-v4.md       # 审核→迭代交接
```

## 与聊天的区别

| 维度 | 交接文档 | 聊天摘要 |
|------|---------|---------|
| 机器解析 | ✅ YAML frontmatter | ❌ |
| 精确路径 | ✅ 精确到文件名 | ❌ 笼统描述 |
| 验证标准 | ✅ 明确的通过/退回条件 | ❌ |
| 版本追溯 | ✅ Git 可跟踪 | ❌ |
| 职责边界 | ✅ sender/receiver 明确 | ❌ |

## 文件命名规则

交接文档命名格式：`{序号}_{简述}_{sender}_to_{receiver}.md`

示例：
- `01_v4审核意见_claude_to_codex.md`
- `02_调研汇总_gemini_to_claude.md`
- `03_框架确认_leroy_to_codex.md`

也可使用 task_id 为名（如 `SG-AU-v4-to-IT.md`），但对人类可读性稍差。项目内保持一致即可。

## 发送前检查清单

交接文档创建完毕后，发送者必须确认：
- [ ] YAML frontmatter 所有必填字段已填写
- [ ] 八个正文节全部存在（即使某节内容为"无"）
- [ ] 所有文件路径指向实际存在的文件
- [ ] `forbidden_terms_checked` 字段准确（已跑过扫描=true）
- [ ] 文档自身通过 `forbidden-terms-scan.sh` 扫描

## 首钢吉泰安实例

Claude 第3轮审核的交接文档（简化版）：

```yaml
---
schema_version: "1.0"
document_type: handoff
task_id: "SG-AU-v4-to-IT"
created: "2026-04-10T22:00+08:00"
sender:
  agent: claude
  role: content-reviewer
receiver:
  agent: codex
  role: execution
status: submitted
priority: P0
depends_on: ["SG-EX-v4-build"]
produces: ["SG-EX-v5-build"]
forbidden_terms_checked: true
---
```

**目标**：Codex 执行最后一轮收口，消除 P16-P18 中 G1/G2/G3/G4 代号及高风险表达。

**约束与禁区**：
- 不得出现 G1/G2/G3/G4/E-6/FMP/联合利华/原始听记/任务书/主线稿
- ROI 表述从"通常可低于1年"降为"较短周期内"
- "立即可行"改为"技术路径清晰，待数据确认"

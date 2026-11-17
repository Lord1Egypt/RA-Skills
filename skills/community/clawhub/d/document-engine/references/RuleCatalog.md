# 规则目录 · Rule Catalog

规则分为两类：**关键词命中**（`risk_keywords` / `forbidden_keywords`）与**正则命中**（`regex`）。
匹配是决定论式的：命中即产出 finding，不输出概率。

## 一、内建规则（14 条）

### generic（全类型适用，3 条）

| ID | 严重度 | 类别 | 命中模式 | 问题 | 建议 |
|---|---|---|---|---|---|
| COM-001 | WARNING | 用词规范 | 及时 / 尽快 / 适当 / 酌情 / 视情况 / 等 | 模糊时间/程度词，责任边界不清 | 改为可量化的时限或标准 |
| COM-002 | CRITICAL | 风险条款 | 概不负责 / 最终解释权 / 概不退换 / 不承担任何责任 | 单方免责条款，可能被认定无效 | 删除或改为双方对等责任条款 |
| COM-003 | WARNING | 用词规范 | 绝对 / 百分之百 / 永不 / 一切 | 绝对化用语 | 替换为限定性表述 |

### contract（合同专用，5 条）

| ID | 严重度 | 类别 | 命中模式 | 问题 | 建议 |
|---|---|---|---|---|---|
| CT-001 | CRITICAL | 风险条款 | 最终解释权 / 概不负责 / 单方解除 / 无条件 / 免责 | 单方优势或免责条款 | 调整为双方对等条款 |
| CT-002 | FATAL | 合规红线 | 正则：`最低工资.{0,8}(低于\|不足)` | 劳动报酬可能违反最低工资标准 | 核对当地最低工资标准 |
| CT-003 | FATAL | 合规红线 | 正则：`违约金.{0,10}(超过\|高于).{0,4}(30%\|百分之三十)`；`违约金.{0,12}(3[1-9]\|[4-9][0-9]\|100)\s*%` | 违约金比例可能超过法定上限 | 违约金不超过实际损失的30% |
| CT-004 | FATAL | 合规红线 | 正则：`加班.{0,8}(无补偿\|不支付\|没有加班费)` | 加班无补偿条款违反劳动法 | 按法定标准支付加班费 |
| CT-005 | CRITICAL | 风险条款 | 押金 / 保证金 | 需明确返还条件与时限 | 补充返还条件、时限与利息约定 |

### regulation（制度专用，3 条）

| ID | 严重度 | 类别 | 命中模式 | 问题 | 建议 |
|---|---|---|---|---|---|
| RG-001 | WARNING | 职责权限 | 相关部门 / 有关人员 / 视情况 | 职责主体不明确 | 明确到具体部门或岗位 |
| RG-002 | CRITICAL | 合规红线 | 未经审批 / 自行决定 / 擅自 | 未经审批即可执行的权限漏洞 | 补充审批流程与权限边界 |
| RG-003 | WARNING | 风险条款 | 有权 / 可以自行 | 权限表述宽泛 | 明确权限范围与限制条件 |

### official_doc（公文专用，3 条）

| ID | 严重度 | 类别 | 命中模式 | 问题 | 建议 |
|---|---|---|---|---|---|
| OD-001 | CRITICAL | 格式规范 | 正则：`\d{4}[./-]\d{1,2}[./-]\d{1,2}` | 日期格式不规范 | 使用「YYYY年MM月DD日」 |
| OD-002 | WARNING | 格式规范 | 正则：`请示[^。]{0,20}(报告\|汇报)` | 请示与报告文种混用 | 请示用于请求指示，报告用于汇报工作 |
| OD-003 | WARNING | 用词规范 | 大概 / 大约 / 差不多 | 公文用词含糊 | 使用精确数字与表述 |

### 文档级审计器（4 个，与规则扫描互补）

| 审计器 | 适用类型 | 判定 |
|---|---|---|
| CompletenessAuditor | contract / regulation / official_doc | 必备要素关键词全部缺失 → CRITICAL |
| ConsistencyAuditor | 全类型 | 同一赋值短语（X为Y）出现多个不同取值 → CRITICAL |
| BalanceAuditor | contract | 甲方权利表述 − 乙方权利表述 ≥ 2 → WARNING |
| FormatAuditor | official_doc | 缺文号 → CRITICAL；缺成文日期 → WARNING |

## 二、自定义规则 JSON 格式

`--rules-dir` 目录下的每个 `*.json` 文件结构如下（顶层 `doc_type` 为该文件默认适用范围，可被单条规则的 `scope` 覆盖）：

```json
{
  "doc_type": "contract",
  "rules": [
    {
      "id": "MY-001",
      "scope": "contract",
      "category": "风险条款",
      "severity": "WARNING",
      "kind": "risk_keywords",
      "patterns": ["示例词1", "示例词2"],
      "message": "命中后显示的问题描述",
      "suggestion": "修改建议"
    },
    {
      "id": "MY-002",
      "scope": "generic",
      "category": "格式规范",
      "severity": "CRITICAL",
      "kind": "regex",
      "pattern": "你的正则表达式",
      "message": "命中后显示的问题描述",
      "suggestion": "修改建议"
    }
  ]
}
```

字段说明：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 规则唯一标识，显示在报告中 |
| `kind` | 是 | `risk_keywords` / `forbidden_keywords`（按 `patterns` 列表命中）或 `regex`（按 `pattern` 正则全局匹配） |
| `severity` | 是 | `SAFE` / `WARNING` / `CRITICAL` / `FATAL`，决定扣分与通过判定 |
| `scope` | 否 | `contract` / `regulation` / `official_doc` / `generic`；省略时取文件级 `doc_type`，再省略为 `generic` |
| `category` | 否 | 问题类别，默认「风险条款」（关键词）或「格式规范」（正则） |
| `message` / `suggestion` | 否 | 问题描述与修改建议，均有默认值 |

## 三、评分与通过判定

- 单条扣分：WARNING −5 / CRITICAL −15 / FATAL −30；总分下限 0
- 通过条件：总分 ≥ 60 **且** 无任何 FATAL / CRITICAL 级 finding

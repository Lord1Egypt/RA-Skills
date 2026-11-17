---
# ClawHub skill frontmatter。
#
# 注意：`name` 必须与父目录名一致（skills/fluidgraph/），全小写、连字符分隔。
name: fluidgraph
description: >
  确定性流体网络求解与可靠性分析。给定管网拓扑、泵压与负载需求，计算节点压力、
  管路流量与流速、压力损失，判定每个负载是否满足要求，并给出可解释的失败原因。
  支持串联/并联树状网络与阀门工况；遇到闭环网络会如实返回 supported=false
  而不编造数值。无需任何 API Key，零外部依赖。
version: 1.0.0
metadata:
  openclaw:
    # 本 Skill 只需要一个 Python 解释器。
    # 刻意**不声明**任何 requires.env —— Skill 层零 LLM 依赖，
    # 不读环境变量。声明用不到的变量会被安全扫描判为 metadata 不匹配。
    requires:
      anyBins:
        - python3
        - python
    emoji: "🌊"
---

# FluidGraph Skill

**一个由确定性流体网络求解器驱动、通过 Tool Calling 提供 Agent 能力的流体网络分析 Skill。**

| | |
|---|---|
| **Skill 名称** | `fluidgraph` |
| **Skill API 版本** | `1.0.0` |
| **AnalysisResult schema** | `2.0` |
| **工具数量** | 7 |
| **运行时依赖** | 无（Python 3.11+ 标准库；Agent 层可选装 `openai`） |

---

## 1. 功能描述

FluidGraph 把一个简化的**稳态、不可压缩**流体网络建模成图结构，按 TOML 配置和
指定工况计算节点压力、管路流量、流速与压力损失，判定每个负载的功能可靠性，
并给出可解释的失败原因。

**所有数值由确定性求解器计算，不由模型产生。** 本 Skill 的职责是把这套计算能力
以结构化工具的形式暴露给 Agent，让 Agent 能"问对问题、读懂结果、讲清结论"。

求解是确定性的（无需迭代），同一个网络 + 工况永远得到同一组数值。

---

## 2. 支持能力

| 能力 | 说明 |
|---|---|
| 稳态 | 不随时间变化 |
| 不可压缩 | 介质密度恒定 |
| 单泵 | 网络中有且仅有一个 `pump` 节点 |
| 固定泵压力 | 泵出口压力为配置值，不随流量变化 |
| 树状网络 | 串联 + 并联，无环 |
| Valve 工况 | 阀门开/关由 Scenario 决定 |
| Scenario | 一个网络可定义多个工况 |
| 流路分析 | 泵到每个负载的完整路径；被切断时指出**是哪只阀门**切断的 |
| 可靠性分析 | 每个负载的功能状态与原因 |
| JSON 输出 | 结构稳定的 `AnalysisResult` |
| Markdown 报告 | 可直接阅读/粘贴的分析报告 |

---

## 3. 不支持的能力

| 不支持 | 说明 |
|---|---|
| **闭环网络** | 环上各支路的分流量需联立方程迭代求解，超出当前模型 |
| 多泵耦合 | 只支持单泵 |
| 瞬态流体 | 不支持时间维度 |
| CFD | 不做场计算 |
| 高级摩擦模型 | 压降只用 `ΔP = R·Q²`，无摩擦因子/雷诺数 |
| P-Q 曲线 | 负载按定流量需求建模，不随压力变化 |
| 动态系统仿真 | 无控制回路、无时序 |

### 遇到不支持的拓扑时

工具**不会**报错，而是返回**合法结论**：

```json
{
  "ok": true,
  "data": {
    "topology": {
      "supported": false,
      "unsupported_elements": ["E1", "E2", "E3"],
      "unsupported_reason": "检测到非树状拓扑：元件 E1, E2, E3 位于环上……"
    },
    "loads": [{ "load_id": "L1", "status": "UNSUPPORTED", "pressure": null, "flow": null }]
  }
}
```

**Agent 必须如实告知用户"当前模型不支持该拓扑，无法可靠求解"。**

> ### ⛔ 禁止编造数值
> `topology.supported = false` 时，`pressure` / `flow` / `velocity` / `pressure_drop`
> 全部为 `null`。**禁止自行估算、禁止给出任何数字、禁止"大约是多少"。**

`supported` 为 false 有两种来源，负载状态不同：

| 原因 | 负载状态 | 典型场景 |
|---|---|---|
| 拓扑超出能力（回路、平行冗余通路） | `UNSUPPORTED` | 闭环网络 |
| 求解本身失败（无泵、多泵、工况引用错误） | `FAILED` | 网络缺少压力源 |

---

## 4. 三条硬约束

> ### 约束 1：`null` ≠ `0`
>
> | 值 | 含义 |
> |---|---|
> | `null` | **没有有效计算值**（该部件未参与计算 / 负载不可达） |
> | `0` | **真实的计算结果为零**（算过了，结果确实是 0） |
>
> `pressure = null` 表示"根本没有供液"，**不是**"压力为 0 Pa"。
> 把两者混为一谈会误导工程判断：`0 Pa` 意味着"有流体但压力很低"，
> 与"压根没接上供液"完全是两回事。
>
> **报告时一律写"无有效值（null）"，绝不写成 0。**

> ### 约束 2：`required_flow` ≠ `actual_flow` ≠ `min_flow`
>
> | 字段 | 含义 |
> |---|---|
> | `required_flow` | 该负载在当前工况下**需要**的流量（求解时的目标值） |
> | `flow`（actual） | **实际送达**该负载的流量 |
> | `min_flow` | 该负载正常工作的**最低要求**（阈值） |
>
> 三者不可互换。判断负载是否正常，**看 `status` 字段**，不要自己拿这几个数去比。
> 当供液受限（配置了 `supply_limit`）时，实际送达量会小于需求量。

> ### 约束 3：Agent 不得自行计算任何物理量
>
> `pressure`、`flow`、`velocity`、`pressure_drop`、可靠性状态、工况间的数值变化
> —— **全部必须来自工具返回的 `AnalysisResult`**。
>
> 你没有能力做这些计算。凭空给出数字会误导用户。
> 工具没有返回某个数值时，如实说"没有这个数据"，不要估算。

---

## 5. 业务参数不得猜测

> ### ⛔ 这是本 Skill 最重要的一条纪律
>
> 如果 TOML 缺少 `min_pressure`、`min_flow`、`required_flow`、`resistance`、
> `diameter` 等**业务/物理参数**，Skill **不得自行猜测真实值**。

这些参数是**工艺设计数据**，只有用户知道。举例：

- `min_pressure = 300000` 取决于下游设备的工作要求；
- `resistance = 1.6e9` 取决于管材、管长、粗糙度；
- `diameter = 0.05` 是实际选型。

**编造这些数字，再基于编造的数字给出"分析结论"，比直接报错危险得多** ——
用户会以为结论是基于他的真实管网得出的。

### 正确做法

1. **工具返回结构化错误**，含字段位置与修复建议：

   ```json
   {
     "code": "invalid_numeric_range",
     "location": "[[nodes]][1]",
     "field": "min_pressure",
     "message": "负载节点 'L1' 的 min_pressure 必须为正数，当前值 None",
     "suggestion": "补上 min_pressure 字段，取值必须是正数"
   }
   ```

2. **Agent 向用户询问真实值**，而不是自己填一个。

3. 只有在用户**明确授权**（"随便填个值先跑通"）时，才可以补占位值 ——
   且必须在回答里**显式标注**：

   > "`min_pressure = 200000.0` 是我补的占位值，不是你的原始数据，
   > 它直接影响 LOW_PRESSURE 判定，请按实际工艺要求替换。"

### 不要做的事

- ❌ 不要因为"这样 Demo 跑起来更方便"就自动补 `min_pressure = 200000`
- ❌ 不要从同类型元素的其它实例"推断"一个值
- ❌ 不要建立任何隐式的业务推断规则

**工具不会自动补这些值**（`parse_network` 会如实报错），Agent 也必须同样克制。

---

## 6. 工具列表

所有工具返回统一的 `SkillResult` 结构。

### 6.1 `parse_network`

| | |
|---|---|
| **用途** | 解析并校验网络定义。问任何物理问题之前先跑，避免后续白跑。 |
| **输入** | `network_source`（TOML 路径 / TOML 文本 / 已解析字典）、`strict`（可选，默认 true） |
| **输出** | `{valid, source, summary:{counts, nodes, pipes, valves, scenarios, capabilities}}` |
| **错误** | 定义非法时 `ok=false`，`errors[]` 含**全部**问题（不是遇到第一个就停） |
| **典型场景** | 用户给了 TOML，先确认能不能用；或修复配置后复验 |

### 6.2 `analyze_scenario`

| | |
|---|---|
| **用途** | 对指定工况执行完整分析 |
| **输入** | `network_source`、`scenario_id` |
| **输出** | 完整 `AnalysisResult`（节点、管路、阀门、负载、流路、摘要、警告） |
| **错误** | 工况不存在 → `unknown_scenario`（建议里列出可用工况） |
| **典型场景** | 用户问"V1 故障什么影响" |

### 6.3 `analyze_all_scenarios`

| | |
|---|---|
| **用途** | 一次跑完网络里定义的全部工况 |
| **输入** | `network_source` |
| **输出** | `{scenarios: {scenario_id: AnalysisResult}}` |
| **错误** | 单个工况失败不拖垮其余，失败项进 `warnings` |
| **典型场景** | 工况对比的前置步骤，比逐个调用省往返 |

### 6.4 `explain_load`

| | |
|---|---|
| **用途** | 解释单个负载**为什么**处于当前状态 |
| **输入** | `analysis_result`（`analyze_scenario` 的 `data`）、`load_id` |
| **输出** | `{status, pressure, flow, required_flow, min_pressure, min_flow, path, isolation_point, reason, explanation}` |
| **错误** | 负载不存在 → `unknown_load`（建议里列出可用负载） |
| **典型场景** | 用户问"为什么 L1 失效" |

**`explanation` 字段**是一句可直接转述给人听的完整解释，优先使用它。

### 6.5 `compare_scenarios`

| | |
|---|---|
| **用途** | 按负载逐项对比两个或多个工况 |
| **输入** | `analysis_results`（≥2 个 `AnalysisResult`，顺序即对比顺序） |
| **输出** | 逐负载：`status` 序列、`transition`、`status_changed`、`direction`、数值序列、`delta`、`notes` |
| **错误** | 少于 2 个 → `not_enough_scenarios` |
| **典型场景** | 用户问"V1 故障造成了什么影响" |

> **`delta` 可能为 `null`。** 当一侧有值、另一侧为 `null`（负载变得不可达）时，
> `delta` 返回 `null` 并在 `notes` 说明原因。
> **这表示"当前值不存在"，不是"下降了很多"。**
> 禁止说"压力下降了 350400 Pa"这种话 —— 那个值根本不存在。
> 只有两侧都有值时才报告真实变化（如 `355650 → 371650`，`delta = +16000`）。

### 6.6 `render_report`

| | |
|---|---|
| **用途** | 把分析结果渲染成 Markdown 报告 |
| **输入** | `analysis_result` |
| **输出** | `{markdown, format:"markdown"}` |
| **错误** | 输入不是 `AnalysisResult` → `invalid_analysis_result` |
| **典型场景** | 用户要一份可直接阅读/粘贴/存档的总结 |

报告含：工况、网络状态、流路分析、负载状态、管路状态、可靠性结论、异常与警告。
数值全部取自 `AnalysisResult`，只做单位换算（`Pa→kPa`、`m³/s→L/s`）。

### 6.7 `read_file`

| | |
|---|---|
| **用途** | 读取文本文件内容（**只读**），用于在配置解析失败时看到原文 |
| **输入** | `path` |
| **输出** | `{path, content, bytes, lines}` |
| **错误** | `path_not_allowed` / `unsupported_file_type` / `file_not_found` / `file_too_large` |
| **典型场景** | 配置修复流程的第一步 |

**没有这个工具就无法完成修复闭环** —— 模型手里只有路径时看不到 TOML 原文，
也就无从修改。

---

## 7. 推荐 Agent 调用模式

### 模式 A：单工况分析

> 用户：「分析 V1 故障。」

```
analyze_scenario(scenario_id="v1_failure")
        ↓
直接解释结果
```

---

### 模式 B：故障原因

> 用户：「为什么 L1 失效？」

```
analyze_scenario(scenario_id="v1_failure")
        ↓
explain_load(load_id="L1")
        ↓
结合 isolation_point 与 reason 回答
```

---

### 模式 C：工况比较

> 用户：「比较正常运行和 V1 故障。」

```
analyze_all_scenarios()                          ← 或两次 analyze_scenario
        ↓
compare_scenarios([normal, v1_failure])
        ↓
逐负载说明变化（注意 null 与 delta 语义）
```

---

### 模式 D：配置修复

> 用户：给出一份有问题的 TOML

```
read_file(path)                                  ← 先看到原文
        ↓
parse_network(toml)
        ↓  ok=false，读 errors[].location + suggestion
按 suggestion 修正
        ↓
parse_network(修正后的内联 TOML)                  ← 复验
        ↓
（可能重复多轮）
parse_network 成功
        ↓
analyze_scenario(...)
```

**关键点**：Skill **没有写盘权限**。修复只能通过
**Agent 内联生成 TOML → `parse_network`** 完成，不要尝试写回文件。

---

## 8. 输出格式

所有工具返回**统一结构**：

```json
{
  "ok": true,
  "tool": "analyze_scenario",
  "data": { },
  "errors": [],
  "warnings": []
}
```

| 字段 | 成功 | 失败 |
|---|---|---|
| `ok` | `true` | `false` |
| `data` | 工具结果 | `null` |
| `errors` | `[]` | 非空 |
| `warnings` | 可能非空（不影响成功） | 可能非空 |

`errors` 与 `warnings` 的元素都是**结构化诊断**：

```json
{
  "code": "unknown_endpoint",
  "severity": "error",
  "message": "管路 'E1' 的 to 引用了不存在的节点 'GHOST'",
  "location": "[[pipes]][0].to",
  "field": "to",
  "suggestion": "把 to 改成已存在的节点 id；当前可用节点：L1, P1",
  "context": { "referenced_node": "GHOST", "available_nodes": ["L1", "P1"] }
}
```

**`suggestion` 是自我修复的关键** —— Agent 应据此修正后重试，而不是把错误抛给用户。

---

## 9. 错误处理

### 常见错误码

| 错误码 | 含义 | 处理方式 |
|---|---|---|
| `invalid_tool_arguments` | 参数不是合法 JSON / 类型不符 / 缺必需参数 | 按 Schema 重新生成参数 |
| `unknown_tool` | 工具名不存在 | 从建议列表里选（可用工具见本文件第 6 节） |
| `path_not_allowed` | 路径越界 | 改用允许目录内的相对路径，或直接传 TOML 文本 |
| `unsupported_file_type` | 只读文本类文件 | 只读 `.toml` / `.json` / `.md` / `.txt` 等 |
| `file_not_found` | 文件不存在 | 检查路径 |
| `file_too_large` | 超过 256 KB | 只读需要的片段 |
| `missing_network_section` | 缺 `[network]` 段落 | 补上 `[network]` + `id` |
| `missing_required_field` | 缺必需字段 | 按 `suggestion` 补上（**见第 5 节：不得猜值**） |
| `invalid_numeric_range` | 数值越界（如 negative resistance） | 改成合法范围 |
| `invalid_node_type` | 节点类型无效 | 改成 `pump` / `junction` / `load` |
| `unknown_endpoint` | 引用了不存在的节点 | 改成已存在的节点 id |
| `duplicate_id` | id 重复 | 改名（节点/管路/阀门共用命名空间） |
| `unknown_scenario` | 工况不存在 | 改用建议列表里的工况 |
| `unknown_load` | 负载不存在 | 改用建议列表里的负载 |
| `unknown_valve_in_scenario` | 工况引用了不存在的阀门 | 改阀门名或先声明 |
| `internal_error` | 工具内部异常 | 换一种问法或换用其它工具重试 |

### 失败不暴露 traceback

**任何情况下都不会把 Python traceback 返回给 Agent。** 未预期异常会被兜住并
转成 `internal_error`，异常类型保留在 `context.exception_type` 里供人排查，
详细堆栈只写日志。

### 一次性返回全部问题

`parse_network` 遇到多处错误时会**一次报全**，而不是改一个跑一次：

```json
{ "ok": false, "errors": [ {"code":"duplicate_id",...}, {"code":"unknown_endpoint",...} ] }
```

---

## 10. 物理模型

严格按照简化模型，**未引入任何额外公式**（无摩擦因子、无密度、无雷诺数）：

| 关系 | 公式 | 说明 |
|---|---|---|
| 管路压力损失 | `ΔP = R · Q²` | `R` 为管道流阻 |
| 流速 | `V = Q / A` | |
| 圆管截面积 | `A = π · D² / 4` | |
| 节点流量守恒 | `ΣQ_in = ΣQ_out` | 对除泵以外的内部节点 |

**单位一律为 SI**，求解器内部不做任何隐式换算：

| 量 | 单位 |
|---|---|
| 压力 | `Pa` |
| 流量 | `m³/s` |
| 直径 / 长度 | `m` |
| 流阻 | `Pa·s²/m⁶` |
| 流速 | `m/s` |

展示层负责换算（`Pa → kPa` 除以 1000、`m³/s → L/s` 乘以 1000）。
**JSON 里永远是 SI 原值。**

### 求解方式

以泵为根的**树状**网络，每条元件都是割边，因此：

- 每条管路的流量 = 它下游全部负载需求之和（节点守恒的直接推论）
- 每个节点的压力 = 父节点压力 − `R·Q²`
- **确定性，无需迭代**

一旦出现环（闭合回路、平行冗余通路、同一对节点上的重边），环上各支路的分流量
必须联立方程求解 —— 此时返回 `topology.supported = false`，**不猜测**。

---

## 11. 安全边界

### `read_file` 的限制

| 限制 | 值 |
|---|---|
| 可读目录 | 白名单（默认：项目根、`examples/`、`outputs/`） |
| 读/写 | **只读** |
| 文件类型 | `.toml` / `.json` / `.md` / `.txt` / `.csv` / `.yaml` / `.yml` |
| 单文件大小 | ≤ 256 KB |

### 明确禁止

- ❌ 任意系统路径（`C:\Windows\...`）
- ❌ `/etc/passwd`
- ❌ `~/.ssh/id_rsa`
- ❌ 路径穿越（`../../../../etc/passwd`）
- ❌ 与白名单前缀相近的同级目录（`/data-evil` 不是 `/data` 的子路径）

越界时返回 `path_not_allowed`，建议里会列出允许的目录。
**拒绝信息中不含被拒文件的内容。**

### 未配置白名单时

`read_file` 在**没有配置沙箱时拒绝一切读取** —— 安全默认是拒绝，而非放行。

### Skill 无写盘能力

Agent 不能写任何文件。配置修复只能通过：

```
Agent 内联生成修正后的 TOML  →  parse_network
```

---

## 12. 版本与兼容性

| 版本 | 值 |
|---|---|
| Skill API | `1.0.0` |
| `AnalysisResult.schema_version` | `2.0` |

### 兼容规则

- ✅ **可以新增字段** —— 消费方必须忽略未知字段
- ❌ 不随意删除字段
- ❌ 不改变字段已有语义
- ⬆️ `schema_version` **只在 breaking change 时递增**

因此：**新增能力不会导致版本号变化**，只有删除字段或改变语义才会。

消费方应当：

```python
# 好：按需取字段，忽略未知字段
status = data["loads"][0]["status"]

# 不好：假设字段集合固定
assert set(payload) == {...}
```

---

## 13. 独立运行

Skill 可以脱离 Agent 独立使用（Core 与 Skill 层**零 LLM 依赖**）：

```bash
python skill_runner.py parse_network examples/example.toml
python skill_runner.py analyze_scenario examples/example.toml v1_failure
python skill_runner.py explain_load outputs/v1_failure.json L1
python skill_runner.py compare_scenarios outputs/normal.json outputs/v1_failure.json
python skill_runner.py render_report outputs/v1_failure.json
python skill_runner.py --list
python skill_runner.py --schema --format anthropic   # 或 openai / mcp
```

退出码：`0` 成功 / `1` 工具报告失败 / `2` 用法或参数错误。

---

## 14. 示例网络

`examples/example.toml` 是一个可直接运行的演示网络：

```
       [P1]  泵，出口定压 400 kPa
        |
     MainPipe
        |
       [J1]
      /    \
    [V1]   [V2]
     |       |
    [N1]   [N2]
     |       |
   PipeA    PipeB
     |       |
    [L1]   [L2]     负载，均要求 ≥ 300 kPa
```

包含两个工况：

| 工况 | 说明 |
|---|---|
| `normal` | 双支路全开，L1 与 L2 都 HEALTHY |
| `v1_failure` | V1 关闭，L1 变为 ISOLATED，L2 压力反而升高 |

另有：

- `examples/broken.toml` —— 故意写错，用于演示错误自动修复
- `examples/ring.toml` —— 闭环网络，用于演示 `supported = false`

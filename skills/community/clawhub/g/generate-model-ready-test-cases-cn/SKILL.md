---
name: generate-model-ready-test-cases-cn
description: 生成标准化、模型可直接消费的自动化测试用例 JSON 套件。用于 Codex 需要根据需求文档、原型图、页面说明、接口文档、用户故事、缺陷描述或自然语言需求，产出可直接交给其他模型或自动化代理执行的测试用例时；尤其适用于 Web UI、API、端到端流程、回归、冒烟和验收场景。
---

# 生成模型可执行测试用例

## 概览

生成结构化的自动化测试用例，不生成只适合人读的松散测试点列表。默认输出单个标准 JSON 测试套件，便于后续模型直接按步骤、定位器、请求参数、断言和变量提取规则执行自动化测试。

## 快速开始

1. 只读取当前任务真正需要的材料，例如需求说明、接口文档、页面原型、已有测试点或缺陷描述。
2. 在生成测试用例前，先阅读 [references/test-suite-schema.md](references/test-suite-schema.md)。
3. 在决定覆盖范围、优先级和缺省策略前，再阅读 [references/test-design-playbook.md](references/test-design-playbook.md)。
4. 生成结果时，默认只输出一个 `json` 代码块；除非用户要求解释，否则不要附加长篇自然语言说明。
5. 如果结果已保存为本地 JSON 文件，在交付前运行 `scripts/validate_test_suite_json.py <path-to-json>`。

## 默认输出格式

按 [references/test-suite-schema.md](references/test-suite-schema.md) 中定义的顶层顺序输出：

1. `suite_id`
2. `suite_title`
3. `target`
4. `assumptions`
5. `defaults`
6. `cases`

始终满足以下规则：

- 只输出合法 JSON，不输出伪 JSON、Markdown 表格或自然语言步骤列表来替代结构化结果。
- 默认只交付程序可消费的 JSON 结果，不额外生成 Excel、XMind、脑图或其他面向人工排版的派生文件，除非用户在当前任务中明确要求。
- 为每个用例生成稳定的 `case_id`，为每个步骤生成稳定的 `step_id`。
- 把缺失但可合理推断的信息写入 `assumptions`，不要因为基础信息不完整就停住。
- 把敏感数据写成占位符，例如 `{{env.TEST_USER}}`、`{{secret.LOGIN_PASSWORD}}`、`{{var.order_id}}`，不要把真实密钥写入结果。
- 把高风险、破坏性或生产环境相关操作默认标记为 `enabled: false`，并在 `assumptions` 中写明原因。
- 只写模型可执行的动作和断言，不写“检查是否正常”“确认成功”这类模糊描述。

## 执行流程

### 1. 规范化输入

先把用户提供的材料统一整理成可生成用例的最小事实集合：

- 测试对象是什么：`web`、`api`、`workflow`、`mobile` 或 `desktop`
- 入口地址或基础 URL 是什么
- 关键业务流、约束条件、角色权限和异常路径是什么
- 哪些数据可以固定，哪些数据必须参数化或通过前置步骤提取
- 是否存在破坏性操作、支付操作、生产环境风险或外部依赖

如果材料来自多种格式，例如 PRD、Figma 文案、Swagger、curl、自然语言描述，先统一成同一份需求理解，再开始写结构化用例。

### 2. 选择可执行动作模型

按任务类型选择步骤动作：

- Web UI 场景优先使用 `navigate`、`click`、`fill`、`select`、`wait`、`assert`、`extract`
- API 场景优先使用 `request`、`assert`、`extract`
- 端到端流程在同一用例内组合 UI 与 API 步骤，但动作仍然使用统一动作枚举
- 无法稳定定位或无法稳定断言的动作不要写入结果，优先换成更稳的定位器或结果验证方式

如果是 Web 场景，优先使用可访问性和业务语义更强的定位器，推荐顺序为：

1. `role`
2. `label`
3. `testid`
4. `text`
5. `css`
6. `xpath`

### 3. 设计覆盖范围

至少覆盖与任务风险匹配的以下子集：

- 正常路径
- 必填或输入校验
- 边界值
- 权限或鉴权失败
- 关键业务规则失败
- 回归或冒烟路径

如果用户没有指定覆盖深度，默认优先保证 `P0` 和 `P1` 的核心流程可执行，再补充关键负例；不要为了“看起来全面”而堆砌低价值用例。

### 4. 生成标准 JSON 套件

为每个用例写全这些核心字段：

- `case_id`
- `title`
- `objective`
- `priority`
- `tags`
- `preconditions`
- `test_data`
- `steps`
- `cleanup`
- `enabled`

为每个步骤写全这些核心字段：

- `step_id`
- `action`
- `target`
- `input`
- `expected`

每个 `expected` 都必须是结构化断言对象，不要省略成一句自然语言。

### 5. 自检结果可执行性

交付前逐项自检：

- JSON 是否合法
- 顶层字段和必填字段是否齐全
- `case_id` 和 `step_id` 是否稳定且唯一
- 动作名称和断言类型是否来自允许枚举
- 定位器、请求参数和变量占位符是否清晰
- 断言是否足够稳定，是否避免依赖随机值、瞬时时间戳和易变文案

如果结果已写入文件，运行 `scripts/validate_test_suite_json.py` 做结构校验。

## 缺省决策规则

当用户没有明确说明时，按以下策略继续，不要反复追问基础问题：

- 默认使用中文标题，但字段名保持英文，保证后续模型和脚本更容易消费。
- 默认按业务能力拆分用例标签，例如 `login`、`order`、`smoke`、`negative`、`regression`。
- 默认把前置数据准备写进 `preconditions`；只有确实需要运行时提取，才使用 `extract` 和 `{{var.xxx}}`。
- 默认把一次语义完整的操作写成一个步骤，不把一个点击拆成多个没有价值的小动作。
- 默认只保留稳定断言，例如状态码、URL、关键字段、稳定按钮可见性、业务成功标记、JSON Path 值。
- 默认不把截图、日志、trace 之类证据要求写成主断言，除非用户明确要求。

## 资源使用

### references/test-suite-schema.md

在生成或修复 JSON 测试套件前加载它。它定义了字段、动作枚举、断言枚举、占位符规则和标准样例。

### references/test-design-playbook.md

在你需要从需求、页面、接口或缺陷描述推导覆盖范围时加载它。它用于帮助你把输入材料转换成更稳、更适合自动化执行的测试用例。

### scripts/validate_test_suite_json.py

在测试套件已经落成文件时运行它，快速检查 JSON 是否符合此 skill 的标准结构。

## 执行规则

- 保持输出面向执行，不要退化成普通测试点文档。
- 保持交付边界聚焦在 JSON 测试套件本身，不把 Excel、脑图或汇报型文档当作默认产物。
- 保持字段命名、枚举值和 JSON 结构稳定，避免同一任务里风格漂移。
- 在信息不足但可合理推断时直接推断，并把推断写进 `assumptions`。
- 在遇到生产环境、支付、删除、不可逆变更或高额成本操作时暂停并提示风险。
- 在用户要求“直接给模型执行”时，优先交付结构化 JSON，不要切换成自然语言说明稿。

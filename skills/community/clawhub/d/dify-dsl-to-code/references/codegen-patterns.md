# 代码生成与项目组装模式

将 Dify 工作流代码化时遵循的架构约定。目标产物：**可部署、可运行、结构清晰**的独立项目，运行后行为与 Dify 中一致。

## 目录

- 项目骨架
- 核心引擎：变量池 + 拓扑执行
- 分块开发契约（多智能体协作）
- 拼接规则
- 质量红线
- 验证清单

## 项目骨架

以 `assets/templates/python-fastapi/` 为起点（Node 技术栈时按同构结构生成）：

```
<project>/
├── .env.example          # 所有环境变量占位（凭据/密钥/base_url）
├── requirements.txt
├── Dockerfile
├── app/
│   ├── main.py           # FastAPI 入口：POST /run {inputs} -> {outputs}
│   ├── workflow/
│   │   ├── context.py    # 变量池 + {{#...#}} 模板解析（模板自带，勿改）
│   │   ├── runner.py     # 拓扑执行引擎 + 条件路由（模板自带，勿改）
│   │   ├── definition.py # 【生成】节点/边定义，由 DSL 直译
│   │   └── blocks/       # 【生成】每个功能块一个模块
│   │       ├── block_01_xxx.py
│   │       └── block_02_yyy.py
│   └── services/         # 【生成】可复用的外部客户端（llm/retrieval/http）
└── tests/test_smoke.py   # 冒烟测试：注入 mock，跑通主链路
```

铁律：**引擎代码来自模板，业务代码来自 DSL**。definition.py 是数据（节点配置直译），blocks/ 是逻辑（每块的节点 handler 实现）。

## 核心引擎：变量池 + 拓扑执行

模板 `context.py` 提供 `VariablePool`：以 `(node_id, var_name)` 存取；`resolve(text)` 把 `{{#node.var#}}`/`{{#env.X#}}`/`{{#secret.X#}}` 插值为实际值。`runner.py` 提供 `Engine`：

- `run(inputs)` 一次性执行；`run_stream(inputs)` 生成器，逐 answer 节点产出 `('answer', text)`，结束产出 `('final', outputs)`（FastAPI 模板已挂到 `POST /run/stream` SSE）。
- 内置路由：`if-else` 同时支持旧版 `conditions`（true/false handle）和新版 `cases[]`（case_id handle）；`question-classifier` 读 handler 写入的 `class_id`。
- 内置子图：`iteration`（逐项执行体内链，输出聚合数组；`is_parallel` **降级为顺序执行**并写入交付说明）、`loop`（break 条件 + loop_count 上限）。体内节点靠 definition 里的 `"parent"` 字段归属。
- `end` 收集声明输出；多个 `answer` 片段按序拼接进 `outputs["answer"]`。

生成代码时**复用而不是重写**这两个文件（Node 栈为 `context.js`/`runner.js`，语义一致）。

## 分块开发契约（多智能体协作）

DSL 过大（经验阈值：节点数 > 25 或文件 > 80KB，上下文装不下全文）时启用多智能体：

1. 主智能体运行 `analyze_dsl.py --blocks-dir blocks/`，得到 `analysis.json` + 每块子图 YAML。
2. **先定契约再派工**：主智能体根据 analysis.json 写好 `definition.py` 骨架和每块的接口签名（输入变量清单、输出变量清单），作为所有子智能体的对齐基准。
3. 每个子智能体领到：一个块 YAML + 接口签名 + `references/dsl-node-types.md`，只实现 `app/workflow/blocks/block_XX_*.py` 一个文件。
4. 子智能体**禁止**修改 definition.py、context.py、runner.py 和其他块的文件——这是避免拼接冲突的关键。

块接口签名格式（写进派工 prompt）：

```python
# block_02 售后工单
# 输入（从变量池读取）: start-1.query: str, start-1.user_tier: str
# 输出（写入变量池）: http-1.status_code: int, http-1.body: dict
# 涉及节点: branch-1(if-else, 已实现于 runner) -> http-1(http-request)
def register(registry): ...
```

## 拼接规则

1. 全部块完成后，主智能体逐块检查：函数签名与契约一致、变量池读写键与 definition.py 对齐、无跨块 import。
2. `definition.py` 按 analysis.json 的 edges 还原全图（含跨块边，`incoming_edges`/`outgoing_edges` 字段就是为此准备的）。
3. `if-else` 出边按 `sourceHandle`（`"true"/"false"` 或条件 id）接线。
4. 拼接后跑冒烟测试：mock LLM 与 HTTP，主链路能从头走到 `end`。
5. 静态检查：`python -m compileall app` 全绿；`.env.example` 覆盖 analysis.json 中全部 `environment_variables` 与 `secret_variable_refs`。

## 质量红线

- **禁止硬编码凭据**：密钥只出现在 `.env` / `.env.example`（占位值）。
- **禁止重写 `code` 节点的内联代码**：原样搬运封装，保持行为一致。
- **禁止静默降级**：知识库、工具、凭据的每项降级都要写进交付说明。
- **禁止超长文件**：单文件 > 300 行就拆分到 services/。
- prompt 文本原样保留（含插值占位符），插值由引擎在运行时完成。
- 被 if-else 剪掉的分支不执行；end 节点引用未执行分支的变量时输出 `null`——这与 Dify 行为一致，不要"修复"它。

## 验证清单

先跑自动验收（六项全 PASS 是硬性门槛）：

```bash
python scripts/verify_project.py --analysis analysis.json --project <项目目录>
# structure / coverage(节点全覆盖) / references(引用可解析) / env(.env 覆盖) / compile / handlers
```

再人工逐项过：

- [ ] 冒烟测试通过（mock 外部调用后主链路跑通）
- [ ] 被剪枝分支输出 null 的语义保留（与 Dify 一致）
- [ ] code 节点内联代码逐字节原样
- [ ] prompt 文本逐字节原样（含插值占位符）
- [ ] `is_parallel` 迭代若降级为顺序执行，已写入交付说明
- [ ] 降级项清单已写入交付说明

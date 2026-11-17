---
name: dify-dsl-to-code
description: 将 Dify 导出的工作流/Chatflow DSL 文件（YAML）转化为可部署、可运行的独立代码项目（默认 Python+FastAPI，可选 Node.js+Express）。当用户要求"Dify 工作流转代码"、"DSL 导出转项目"、"把 Dify 应用代码化"、"脱离 Dify 部署工作流"时使用。Convert an exported Dify workflow/chatflow DSL (YAML) into a deployable standalone code project. Use when the user asks to convert/export/translate a Dify DSL or .yml workflow file into runnable code, migrate off Dify, or self-host a Dify workflow as a service. 覆盖：读取用户指定路径的 DSL 文件、解析节点与变量依赖、就缺失信息（API Key、知识库语料、工具凭据、部署形态）与用户交互补全、超大 DSL 时拆解为功能块并派发给多智能体分块实现、最终拼接验证为完整项目。
---

# Dify DSL 转代码项目

把 Dify「导出 DSL」得到的 YAML 转化为脱离 Dify 运行的独立代码项目。核心原则：**DSL 里没有的信息绝不编造，一律问用户；问不到的降级并显式声明**。

## 总流程

```
0 定位文件 → 1 解析分析 → 2 补全缺失信息 → 3 定技术栈/脚手架
→ 4 生成代码（小:单智能体 / 大:多智能体分块）→ 5 拼接验证 → 6 交付说明
```

## 阶段 0：定位 DSL 文件

第一动作永远是问用户：

> 请提供 Dify 导出的 DSL 文件（.yml/.yaml）在当前机器上的完整路径。
> 未导出的话：Dify 控制台 → 应用 → 编排页右上角「导出 DSL」。

拿到路径后依次验证，任一失败立即反馈并请用户重新提供，不要猜路径：

1. 文件存在；2. YAML 可解析；3. 含 `workflow.graph.nodes`（否则不是 workflow/chatflow 导出）。

## 阶段 1：解析分析

运行分析脚本（确定性解析，不要凭肉眼读大 YAML）：

```bash
python scripts/analyze_dsl.py <dsl文件> --out analysis.json --blocks-dir blocks/
# 需要 pyyaml；输出: 应用元数据 / 节点清单 / 边图 / 外部依赖清单 / 功能块划分
```

阅读 `analysis.json`，重点关注：

- `app.mode`：`workflow` 用 end 节点收尾；`advanced-chat`（chatflow）用 answer 节点，默认 SSE 流式。
- `external_requirements`：模型 provider、工具、知识库 dataset、http 端点、env/secret 变量、conversation 变量、agent 策略——**这就是缺失信息清单**。
- `flags`：强制用户决策的信号——`javascript_code_nodes`（JS 代码需 Node 运行时或授权改写）、`file_input_variables`/`file_upload_enabled`（文件输入如何处理）、`uses_conversation_variables`（会话状态是否保留）、`has_iteration`/`has_loop`。
- `stats`：节点数与文件大小，决定阶段 4 走单智能体还是多智能体。

节点类型 → 代码的映射策略见 [references/dsl-node-types.md](references/dsl-node-types.md)；各组件的完整属性字典（实现具体节点时查阅）见 [references/dsl-components.md](references/dsl-components.md)。`assets/examples/` 下有两个真实导出样例（workflow 与 chatflow 各一），对节点结构拿不准时直接对照。

## 阶段 2：补全缺失信息（与用户交互）

严格按 [references/interaction-playbook.md](references/interaction-playbook.md) 执行。要点：

- **一轮问完**：把凭据类、资源类、决策类问题合并成一次结构化提问，不挤牙膏。
- 凭据一律写入 `.env.example` 占位，**永不硬编码**；用户说"占位即可"就尊重。
- 知识库 dataset 内容不随 DSL 导出，必须让用户二选一：提供语料自建向量检索，或项目内回调 Dify API。
- 用户不答的项按 playbook 的降级表处理，且**每项降级都要写进最终交付说明**。

## 阶段 3：定技术栈与脚手架

与用户确认语言、服务形态、是否带 Dockerfile（话术见 playbook 阶段 2）。默认推荐 Python + FastAPI + Dockerfile。

选定后复制模板为项目起点：

```bash
cp -r assets/templates/python-fastapi/ <输出目录>/<项目名>/   # Python 栈
cp -r assets/templates/node-express/ <输出目录>/<项目名>/     # Node.js 栈
# 模板自带执行引擎(context/runner)——直接复用，禁止改写
# 引擎内置：拓扑执行、if-else(含新版 cases[])、question-classifier 路由、
# iteration/loop 子图执行、answer 流式(/run 一次性 + /run/stream SSE)
```

项目骨架、引擎约定与质量红线见 [references/codegen-patterns.md](references/codegen-patterns.md)。

## 阶段 4：生成代码

### 4a 小 DSL（节点 ≤ 25 且文件 ≤ 80KB）：单智能体直写

1. `definition.py`：按 analysis.json 直译全部节点与边（数据，不含逻辑）。
2. `app/workflow/blocks/`：按功能块组织 handler，每块一个文件。
3. `app/services/`：LLM、检索、HTTP 等可复用客户端。
4. `.env.example`：覆盖 analysis.json 中全部环境变量与 secret 引用。

### 4b 大 DSL（节点 > 25 或文件 > 80KB）：多智能体分块

1. **契约先行**：主智能体先写好 `definition.py` 全图骨架 + 每块接口签名（输入/输出变量清单），作为所有子智能体的对齐基准。
2. **派工**：每个子智能体领取一个 `blocks/block_XX_*.yaml` 子图 + 接口签名 + dsl-components.md（组件属性查阅），只实现 `blocks/block_XX_*.py` 一个文件；禁止触碰 definition.py、引擎文件和其他块。
3. **拼接**：全部块返回后，按 codegen-patterns.md 的拼接规则逐块验收（签名对齐、变量池键对齐、无跨块 import），接好跨块边（块 YAML 里的 `incoming_edges`/`outgoing_edges` 就是干这个的）。

## 阶段 5：拼接验证

先跑自动验收脚本（六项检查：结构/节点覆盖率/变量引用/.env 覆盖/编译/handler 注册）：

```bash
python scripts/verify_project.py --analysis analysis.json --project <项目目录>
# 全部 PASS 后再人工过 codegen-patterns.md 的验证清单
```

再跑冒烟测试（mock LLM 与 HTTP，主链路能从头走到 end/answer）。其余人工核对项（节点恰好一次、变量名对齐、code 原样搬运）见 [references/codegen-patterns.md](references/codegen-patterns.md)。

## 阶段 6：交付说明

交付时给出：项目路径、启动命令（`uvicorn app.main:app` 或 `docker build`）、**降级项清单**（哪些凭据是占位、哪个知识库用了什么方案、哪些工具是 NotImplementedError 待补）。降级可以，静默不行。

## 触发与本 skill 边界

- 输入必须是 Dify「导出 DSL」的 YAML；用户给的是 Dify API 文档或截图时，先引导其导出 DSL。
- 反向需求（生成/调试 Dify DSL 本身）不属于本 skill。

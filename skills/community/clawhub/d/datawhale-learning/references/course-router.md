# Course Router

| Learner signal | Search these terms first | Course area |
|---|---|---|
| idea selection, user interview, requirements, MVP | `产品`, `双钻`, `Jobs to Be Done`, `Mom Test`, `原型` | Easy Vibe Stage 1 |
| AI IDE, prompting, generated code, common errors | `AI 编程工具`, `常见问题与排错`, `构建可交互的产品原型` | Easy Vibe Stage 1 |
| UI, components, frontend, design-to-code | `前端`, `UI`, `组件库`, `design-to-code` | Easy Vibe Stage 2 / appendix |
| API, database, auth, backend, payment | `API`, `数据库`, `认证`, `后端`, `支付` | Easy Vibe Stage 2 / appendix |
| Git, CLI, ports, PATH, SSH, debugging | `Git`, `命令行`, `端口`, `环境变量`, `SSH`, `调试` | Easy Vibe appendix |
| deployment, Docker, HTTPS, monitoring | `部署`, `Docker`, `HTTPS`, `监控`, `CI/CD` | Easy Vibe Stage 2–3 / appendix |
| what an agent is, agent components, agent versus workflow | `初识智能体`, `智能体定义`, `智能体组成`, `Agent` | Hello Agents 1 |
| agent history, symbolic AI, expert systems, modern agents | `智能体发展史`, `符号主义`, `专家系统`, `发展阶段` | Hello Agents 2 |
| LLM foundations, Transformer, prompting, model APIs | `大语言模型基础`, `Transformer`, `提示词`, `模型调用` | Hello Agents 3 |
| Dify, knowledge base, RAG | `Dify`, `知识库`, `RAG`, `向量检索` | Easy Vibe + Hello Agents 8 |
| ReAct, planning, reflection | `经典范式`, `ReAct`, `Plan-and-Solve`, `Reflection` | Hello Agents 4 |
| low-code agent, Dify workflow, quick agent prototype | `低代码平台`, `智能体搭建`, `Dify`, `工作流编排` | Hello Agents 5 |
| AutoGen, AgentScope, LangGraph, custom framework | `框架开发`, `构建你的Agent框架`, `LangGraph` | Hello Agents 6–7 |
| memory, retrieval, context | `记忆与检索`, `上下文工程` | Hello Agents 8–9 |
| MCP, A2A, ANP, tool protocol | `智能体通信协议`, `MCP`, `A2A`, `ANP` | Hello Agents 10 |
| training, SFT, GRPO, evaluation | `Agentic-RL`, `性能评估` | Hello Agents 11–12 |
| travel, deep research, NPC, multi-agent project | `智能旅行助手`, `自动化深度研究`, `赛博小镇`, `毕业设计` | Hello Agents 13–16 |
| AI-native SDLC, intent, spec, implementation plan | `AI 原生 SDLC`, `intent.md`, `spec.md`, `plan.md`, `产物门` | AI-native SDLC practice layer |
| continuous evals, agent verification, visual checking | `持续评测`, `continuous evals`, `验证证据`, `截图对比`, `测试保护` | AI-native SDLC: Test |
| agent PR review, policy checks, approval hooks | `Agent Review`, `PR Review`, `Hook`, `审批门`, `治理` | AI-native SDLC: Build / Deploy |
| production autonomy, incident loop, control band | `自治分级`, `生产控制带`, `事故闭环`, `Incident-to-Eval`, `回滚` | AI-native SDLC: Deploy / Maintain |

## Default sequencing rules

- Product delivery goal: validate the workflow before studying advanced agent architecture.
- Conceptual agent goal: begin with Hello Agents 1, then use 2 for historical context, 3 for LLM prerequisites, and 4 for agent paradigms.
- Fast prototype goal: after Hello Agents 1 and the minimum of 3, use Hello Agents 5; study 4 before implementing paradigm-specific behavior.
- Low-code versus code: use low-code to validate; move to code when testing, state, versioning, or maintainability becomes a real constraint.
- Single versus multi-agent: begin with one agent. Split only when tools, permissions, context, or evaluation criteria need separate boundaries.
- Stable concepts versus current details: use the tutorials for concepts and official vendor docs for current commands or UI steps.
- Delivery transformation: begin with plan artifacts and self-verification; add deterministic hooks and autonomous maintenance only after tests, permissions, and rollback are reliable.

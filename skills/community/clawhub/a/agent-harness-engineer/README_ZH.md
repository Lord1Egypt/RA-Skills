<p align="center">
  <h1 align="center">⚙️ Agent Harness Engineer</h1>
  <p align="center">
    <strong>生产级 AI Agent 系统构建蓝图</strong>
    <br />
    一个指导 AI 编程工具构建企业级 Agent 系统的 <a href="https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills">Skill</a>，告别玩具 Demo，生成生产就绪代码。
  </p>
</p>

<p align="center">
  <a href="https://github.com/nicepkg/agent-harness-engineer/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License" /></a>
  <a href="https://github.com/nicepkg/agent-harness-engineer/stargazers"><img src="https://img.shields.io/github/stars/nicepkg/agent-harness-engineer?style=flat&color=yellow" alt="Stars" /></a>
  <a href="README.md"><img src="https://img.shields.io/badge/English-README-blue.svg" alt="English Doc" /></a>
</p>

---

## 为什么需要 Agent Harness Engineer？

大多数"教你构建 Agent"的教程，只会给你一个 50 行的 Python 脚本，在循环里调用 LLM。那是 Demo，不是生产系统。

**Agent Harness Engineer** 完全不同。它是一套完整的 **7 阶段构建蓝图**，AI 编程工具会按照它逐步生成结构完整、安全可靠、可扩展的 Agent 系统 —— 包含权限模型、上下文压缩管道、多智能体协作、沙箱隔离和生产监控。

> *"Agent 在其上下文中无法访问的信息，就不存在。"* —— Harness 工程核心原则

---

## 快速开始

这是一个由 AI 编程助手（如 Claude Code）使用的 **Skill**。将其放入项目中，然后对你的 AI 编程工具说：

```
"帮我构建一个 Agent"
```

AI 将自动加载此 Skill，按结构化的 7 阶段流程引导你完成从脚手架到生产部署的全过程。

### 一键配置

```bash
git clone https://github.com/nicepkg/agent-harness-engineer.git
# 将 SKILL.md 放入项目的 skills 目录中
```

触发后，Skill 会：
1. 确认你的需求（技术栈、LLM 供应商、规模、用途）
2. 按阶段逐步执行，每阶段自动检查验收
3. 基于实战验证的模板，生成完整、生产就绪的 Agent 项目

---

## 核心框架：Harness Engineering

<p align="center">
  <b>生产级 Agent 系统的三大支柱</b>
</p>

| 支柱 | 原则 | 实现方式 |
|------|------|----------|
| **上下文工程**<br>Context Engineering | 信息可达性决定一切 | 四级压缩管道、工具延迟加载、记忆按需附加 |
| **架构约束**<br>Architectural Constraints | 机械执行胜过人工建议 | 5 种权限模式 × 7 级规则层级、Schema 校验、沙箱隔离 |
| **熵管理**<br>Entropy Management | 代码不维护就会退化 | 文档一致性审计、约束违规扫描、覆盖率门禁 |

---

## 七阶段构建蓝图

```
第一阶段  ●──○ 项目初始化    ▸ 脚手架搭建、配置文件、目录结构
第二阶段  ●──○ LLM 抽象层   ▸ 多供应商客户端（Anthropic、OpenAI、Azure、本地模型）
第三阶段  ●──○ 工具系统     ▸ 工具注册表、Schema 校验、并发安全
第四阶段  ●──○ Agent 核心循环 ▸ 7 个 Continue 站点、不可变状态、错误恢复
第五阶段  ●──○ 上下文管理   ▸ 四级压缩管道、记忆系统、自动做梦机制
第六阶段  ●──○ 权限安全     ▸ 六层纵深防御、沙箱隔离、审计日志
第七阶段  ●──○ 生产化      ▸ 测试、监控、日志、部署文档
```

每阶段包含：**理论指导 → 实践步骤 → 检查清单 → 常见陷阱**

---

## 架构速览

```
┌─────────────────────────────────────────────────────────┐
│                   HARNESS（编排器）                       │
│                   无状态编排循环                           │
│                                                         │
│   while (running) {                                     │
│     step = yield from Session.next()                    │
│     result = Sandbox.execute(step)                      │
│     Session.commit(result)                              │
│   }                                                     │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
    ┌──────▼──────┐           ┌──────▼──────┐
    │   SESSION   │           │   SANDBOX   │
    │ 追加式事件   │           │   隔离执行   │
    │   日志      │           │    环境     │
    │ 不可变 &    │           │ 文件/网络/  │
    │ 可回放      │           │  进程隔离    │
    └─────────────┘           └─────────────┘
```

**Session（会话）** —— 不可变的追加式事件日志，类似于数据库 WAL，是系统的唯一事实来源。  
**Harness（编排器）** —— 无状态编排循环，崩溃可恢复，可从任意节点重启。  
**Sandbox（沙箱）** —— 隔离执行环境，爆炸半径控制。

---

## 功能特性

<table>
<tr>
<td width="50%">

### 🔒 生产级安全
- **六层纵深防御**安全模型
- 权限模式：`allow` / `deny` / `ask`
- 工具执行前后 Hook 审计
- 沙箱隔离（文件系统、网络、进程）
- 危险命令硬编码拒绝

</td>
<td width="50%">

### 🧠 高级上下文管理
- **四级压缩管道**
  - Snip → Microcompact → Context-Collapse → Autocompact
- 多类别记忆系统（短期/长期）
- 自动做梦 / 记忆固化机制
- 工具延迟加载，节省上下文窗口

</td>
</tr>
<tr>
<td width="50%">

### 🔧 多供应商 LLM 支持
- 供应商无关的 `LLMClient` 抽象接口
- Anthropic、OpenAI、Azure、本地模型
- 工厂模式，零代码切换供应商
- 流式（Async Generator）架构

</td>
<td width="50%">

### 🤖 多智能体 & MCP
- Coordinator 协调者模式 & Swarm 群集模式
- MCP 模型上下文协议集成
- 6 种传输机制（stdio、HTTP、SSE、WS、gRPC、本地）
- 子 Agent 上下文隔离，摘要式返回

</td>
</tr>
</table>

---

## 项目模板

开箱即用的完整脚手架，包含完整源码：

```
templates/project-scaffold/
├── python/                    # Python Agent 脚手架
│   ├── src/
│   │   ├── agent/             # 核心循环、会话、上下文、记忆
│   │   ├── llm/               # 客户端抽象、工厂函数、供应商适配
│   │   ├── tools/             # 工具注册表、文件工具、网络工具
│   │   ├── permissions/       # 权限模型、Hook 系统、沙箱
│   │   └── utils/             # 日志、错误处理
│   ├── config/                # YAML 配置、Agent 角色、Hook 脚本
│   ├── skills/                # 自定义 Skill 模板
│   └── tests/                 # 单元测试 & 集成测试
│
└── nodejs/                    # Node.js Agent 脚手架
    ├── src/                   # 与 Python 版相同结构
    ├── config/
    ├── skills/
    └── tests/
```

### Python 技术栈
`anthropic` · `openai` · `httpx` · `pydantic` · `pyyaml` · `beautifulsoup4` · `pytest`

### Node.js 技术栈
`@anthropic-ai/sdk` · `openai` · `axios` · `cheerio` · `js-yaml` · `jest`

---

## 十大设计哲学

1. **Async Generator 流式架构** —— yield 中间事件，而非只返回最终结果
2. **Continue 站点实现状态机** —— `while(true)` + 7 个恢复点，从任意错误中恢复
3. **编译时特性门控** —— 构建时消除死代码
4. **缓存前缀稳定性** —— 内置工具排序后作为稳定前缀，MCP 工具变化不影响缓存
5. **纵深防御** —— 6 层叠加使绕过概率指数下降
6. **数据驱动可扩展性** —— `settings.json` + `agents/*.md` + `skills/*.md` + hooks
7. **上下文即稀缺资源** —— 延迟加载、按需记忆、四级压缩管道
8. **层级化配置覆盖** —— CLI > Flag > Policy > Managed > Local > Project > User 共 7 级
9. **隔离的子 Agent 上下文** —— 子 Agent 从空白消息列表开始，完成后只返回摘要
10. **可逆性优先** —— 文件编辑通过 Edit（替换字符串），不用 Write（覆盖）

---

## 适用场景

触发关键词：

> "构建 agent" · "创建智能体" · "agent 系统" · "自动化工具" · "AI 助手" · "多智能体" · "agent 优化" · "agent 脚手架" · "agent 项目模板" · "agent 框架"

### 使用场景

| 规模 | 说明 | 示例 |
|------|------|------|
| **小型** | 个人助手 | 编程助手、笔记整理 |
| **中型** | 团队工具 | 代码审查机器人、CI/CD 助手 |
| **大型** | 企业平台 | 客服群集、运维自动化舰队 |

---

## 路线图

- [x] 七阶段构建蓝图（v2）
- [x] Python & Node.js 项目脚手架
- [x] 多智能体协作模式
- [x] MCP 协议集成
- [x] 六层纵深防御安全
- [x] 四级上下文压缩管道
- [ ] Go 语言脚手架
- [ ] 评测基准套件
- [ ] 可视化架构图
- [ ] 真实案例研究

---

## 贡献指南

欢迎贡献！你可以通过以下方式参与：

- 添加新语言的脚手架（Go、Rust、TypeScript 原生）
- 完善参考文档
- 添加评测用例
- 分享使用此 Skill 构建的真实 Agent 案例

提交 PR 前请阅读[贡献指南](CONTRIBUTING.md)。

---

## 开源协议

本项目基于 Apache License 2.0 开源协议 — 详见 [LICENSE](LICENSE)。

---

<p align="center">
  <sub>由 Agent 工程社区 ❤️ 构建</sub>
  <br />
  <sub>如果这个项目对你有帮助，请在 GitHub 上 ⭐ Star 支持！</sub>
</p>
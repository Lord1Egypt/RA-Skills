# Adapter Guide — 高级定制参考

> **大多数用户不需要读这个。** SKILL.md 加载后会自动检测环境并选择模式。
> 本文件仅用于以下情况：想深入理解运行原理、跨框架移植、或自检测选择了错误的模式。

---

## 三种典型场景

| 场景 | 主持人在哪 | 参与者在哪 | 传输层 |
|------|-----------|-----------|--------|
| A — 纯 Hermes | Hermes 单 Agent | 同一 Hermes，角色切换模拟 | 无（内部上下文切换） |
| B — 纯 OpenClaw | OpenClaw Agent | 其他 OpenClaw Agent | ACP bridge |
| C — Hermes + OpenClaw | Hermes Agent | OpenClaw Agent | ACP bridge（默认） |

---

## 场景 A：纯 Hermes（无 OpenClaw）

用户只有一个 Hermes Agent，没有 OpenClaw 多 Agent 环境。

### 工作原理

Hermes Agent 在内部切换角色模拟多位参与者：
- 主持人 → 策略者 → 执行者 → 主持人……
- 每轮在自己上下文中生成三个角色的发言
- 按交接棒协议输出结构化讨论

### 需要的文件

只需保留核心方法论文件：
```
agent-brainstorm-chair/
├── SKILL.md
├── SETUP_GUIDE.md
├── scripts/
│   └── build_baton.py          ← 只保留这个
└── tests/
    └── test_build_baton.py
```

**不需要** `openclaw_agent_query.py`、`openclaw_meeting_round.py`、`openclaw_acp_clean.py`。

### 配置

无需配置 ACP 桥接。在 Hermes Agent 的 AGENTS.md 中添加：

```markdown
### 头脑风暴触发
当用户说"开会""头脑风暴""主持议事"时，加载 agent-brainstorm-chair skill。
模拟模式：你一个人扮演主持人 + 策略者 + 执行者三个角色，
按交接棒协议逐棒输出。每棒标注角色名。
```

### 使用示例

```
用户：开会，议题：是否重构支付模块，2轮

Hermes（主持人）：
第 1/2 轮，先请策略者给方向判断。

Hermes（策略者）：
结论：暂不重构。依据：1. 当前模块稳定运行24个月无P0事故
2. 重构ROI为负，预计投入3人月仅提升15%吞吐
风险：若Q4交易量超预期增长50%以上，现有架构可能成为瓶颈

Hermes（执行者）：
承接策略者判断。当前不可重构的约束：1. Q3已有3个高优需求排队
2. 支付团队仅2人，没有余力。建议：Q4 review时重新评估

Hermes（主持人）：
本轮收束——共识：暂不重构；分歧：Q4触发条件阈值有差异
进入第 2/2 轮……
```

### 注意事项

- 模拟模式下，角色切换必须显式标注角色名，不能混成一个人
- 每个角色发言后必须显式交棒给下一角色
- 策略者和执行者的观点必须有差异，不能是同一立场的复读

---

## 场景 B：纯 OpenClaw（无 Hermes）

用户有多个 OpenClaw Agent，但没有 Hermes 作为主持人。

### 工作原理

其中一个 OpenClaw Agent 充当主持人（加载主持方法论），通过 ACP 桥接征询其他 Agent。
主持 Agent 自己调用 ACP 脚本。

### 需要的文件

全部保留，但不需要 Hermes profile 集成：
```
agent-brainstorm-chair/
├── SKILL.md
├── SETUP_GUIDE.md
├── ADAPTERS.md
├── scripts/
│   ├── build_baton.py
│   ├── openclaw_agent_query.py
│   ├── openclaw_meeting_round.py
│   └── openclaw_acp_clean.py
└── tests/
    └── test_build_baton.py
```

### 配置

1. 选定一个 Agent 作为主持人（例如 agent-0）
2. 编辑 `scripts/openclaw_agent_query.py`：

```python
ALIASES = {
    "strategist": "agent-1",
    "executor": "agent-2",
}

CHAIR_PROMPT_BUILDERS = {
    "agent-1": lambda topic: f"议题：{topic}。请直接给结论，补2条依据和1条风险边界。",
    "agent-2": lambda topic: f"议题：{topic}。请直接给结论，补2条执行约束。",
}

CHAIR_PROMPT_PATTERNS = {
    "agent-1": re.compile(r"^议题：(?P<topic>.+?)[。.]", re.DOTALL),
    "agent-2": re.compile(r"^议题：(?P<topic>.+?)[。.]", re.DOTALL),
}
```

3. 在主持 Agent 的指令中引用：

```markdown
当用户说"开会"时，使用 agent-brainstorm-chair 方法论。
每轮调用：
python3 ~/skills/agent-brainstorm-chair/scripts/openclaw_meeting_round.py \
  --agents "agent-1,agent-2" --topic "<主题>" --require-all
```

### 环境变量（如果 openclaw 不在标准路径）

```bash
export OPENCLAW_BIN=/home/user/bin/openclaw
export OPENCLAW_HOME=/home/user/.openclaw
```

---

## 场景 C：Hermes + OpenClaw（双系统）

当前默认配置。Hermes 作为主持人，通过 ACP 桥接征询 OpenClaw Agent。

### 工作原理

- Hermes Agent 加载本技能作为主持方法论
- 通过 `openclaw_meeting_round.py` 批量征询 OpenClaw Agent
- 通过 `build_baton.py` 生成交接棒消息

### 配置

与场景 B 相同，但主持方法论由 Hermes Agent 理解和执行，不需要在 OpenClaw Agent 指令中写。

---

## 场景 D：纯手工（无 Agent 框架）

没有任何 Agent 框架，只是想用这个方法论组织人类团队讨论。

### 需要的文件

只保留方法论文档：
```
agent-brainstorm-chair/
├── SKILL.md          ← 方法论核心
└── ADAPTERS.md       ← 本文件
```

### 使用方式

将 SKILL.md 中的规则直接应用于人类会议：
- 指定一个主持人（人）
- 指定策略者和执行者角色（可以是一个人兼任）
- 严格按两阶段辩论制和轮次硬上限执行
- 交接棒协议可简化为口头点名

---

## 传输层对比

| 特性 | ACP 桥接 | 模拟模式 | 平台 Mention |
|------|---------|---------|-------------|
| 真实多 Agent | ✅ | ❌ | ✅ |
| 不需要额外基础设施 | ❌ | ✅ | 取决于平台 |
| 发言质量差异化 | 自然差异 | 需人工制造对立 | 自然差异 |
| 延迟 | 高（串行征询） | 低 | 中 |
| 适合场景 | 真实多 Agent 协作 | 快速原型、无多 Agent 环境 | 群聊公开接力 |

---

## 快速决策：我该用哪种？

```
你有多个 OpenClaw Agent 吗？
├── 是 → 你有 Hermes 吗？
│        ├── 是 → 场景 C（默认）
│        └── 否 → 场景 B
└── 否 → 你有 Hermes 吗？
         ├── 是 → 场景 A（模拟模式）
         └── 否 → 场景 D（纯手工）
```

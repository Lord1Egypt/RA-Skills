---
name: agent-brainstorm-chair
description: "通用多 Agent 结构化头脑风暴主持技能。安装即用，零配置，自动检测环境适配纯Hermes / 纯OpenClaw / 混合模式。两阶段辩论制 + 轮次控制 + 角色分工 + 交接棒协议。"
metadata:
  clawhub:
    tags: [brainstorming, multi-agent, facilitation, decision-making, meeting]
    ecosystems: [hermes, openclaw]
    auto_detect: true
---

# Agent Brainstorm Chair

> **安装即用，无需配置。** 加载本技能后，按下方「自检测」流程自动选择运行模式。
> 高级定制参考 [ADAPTERS.md](ADAPTERS.md)。

---

## ⚡ 自检测与启动（加载本技能后首先执行）

你作为主持人 Agent，在收到第一个"开会/头脑风暴/主持议事"请求时，按以下流程自检测：

```
1. 运行: which openclaw 2>/dev/null
   ├── 找到 openclaw →
   │     2. 检查: ls ~/.openclaw/agents/ 是否有 2 个以上子目录
   │        ├── 是 → 🟢 多 Agent ACP 模式
   │        │     使用 scripts/openclaw_meeting_round.py 征询其他 Agent
   │        │     需要先确定参与 Agent 的 ID（运行 ls ~/.openclaw/agents/）
   │        │     首次使用提示用户确认 Agent 角色分配
   │        └── 否 → 🟡 降级为模拟模式（见下）
   └── 未找到 openclaw →
         3. 检查: 当前是否为 Hermes Agent
            ├── 是 → 🟡 模拟模式
            │     你一个人扮演主持人 + 策略者 + 执行者
            │     逐棒切换角色，标注角色名和轮次
            │     不需要任何外部脚本
            └── 否 → 📖 纯手工模式
                  将本方法论作为会议规则直接执行
```

**模拟模式下的角色切换规则：**
- 每棒开头标注角色名：`【策略者】` / `【执行者】` / `【主持人】`
- 策略者和执行者的观点必须有实质差异，不能复读
- 主持人只在轮首发棒和轮尾收束时出现，不参与中间辩论

**多 Agent ACP 模式下的首次确认：**
- 列出发现的 Agent ID 列表
- 请用户指定哪个 Agent 担任策略者、哪个担任执行者
- 确认后写入记忆，后续会话不再询问

---

## 适用场景

- 你需要一个主持人在多个 AI Agent 之间按固定流程推进讨论
- 需要先把判断辩明，再讨论如何落地执行
- 需要严格的轮次控制和发言质量约束
- 需要在群聊或内部链路中实现 bot-to-bot 接力

---

## 角色模型

| 角色 | 职责 | 发言风格 |
|------|------|----------|
| **主持人** (Facilitator) | 拆题、定轮次、控节奏、点名、收束结论。不替其他人发言。 | 像主席，不像抢答者 |
| **策略者** (Strategist) | 立场判断、方向拍板、利弊取舍、风险边界 | 结论先行 + 2-4 条依据 |
| **执行者** (Executor) | 执行路径、约束条件、资源安排、落地顺序 | "能否落地 + 如何落地 + 关键约束" |
| **发起人** (Sponsor) | 出题、定参与范围、定轮次、最终确认 | 只给参数，不参与辩论 |

---

## 两种模式

| 模式 | 触发 | 范围 |
|------|------|------|
| **讨论模式**（默认） | 只说要讨论 | 辩论 → 结论即止 |
| **执行模式** | 明确说"要交付""要实际完成" | 辩论 → 结论 → 实施计划 → 任务分派 → 跟踪 → 验收 → 交付 |

---

## 起会最短参数

Sponsor 只需要提供两项：

1. **议题**（必需）
2. **总轮次上限**（可选，默认 2 轮）

---

## 执行模型：两阶段辩论制

### 阶段一：辩论判断（默认前 N-1 轮）

1. 主持人立规：议题、轮次、角色分工、发言长度限制
2. 主持人点 Strategist 先给主张与判断
3. 主持人点 Executor 反驳、补条件、指出不可行点
4. 如仍有关键分歧，可补一轮，但受总轮次约束
5. 主持人给出阶段性结论（多视角：方向、风险、执行、时机）

### 阶段二：落实安排（末轮或执行模式）

1. 主持人点 Executor 出执行路径
2. 主持人点 Strategist 补边界与资源偏好
3. 主持人收束为可执行动作清单

### 最终收束（仅第 N/N 轮后）

- 共识 / 分歧 / 多视角建议结论 / 是否需要 Sponsor 继续追问

---

## 交接棒协议

**主持人发首棒模板：**
```
第 1/N 轮
议题：<主题>
本轮顺序：Strategist -> Executor -> 主持人
当前答题者：Strategist
下一棒：Executor
回收主持：主持人

请 Strategist 直接回答本轮任务，不要回复接棒确认。
```

**非末棒交棒：** 回答后末尾标注 `<下一棒: XXX>`

**末棒交回主持人：** 回答后末尾标注 `<交回主持人>`

### 硬约束

- 每次只允许一棒
- 被点名者必须直接回答，不允许跳过次序
- 末棒交回后主持人自动推进下一轮
- 到总轮次上限后必须刹车
- 中间轮次不得要求"直接成文/最终总结"

### 模拟模式下的额外约束

- 每个角色发言必须显式标注角色名：`【策略者】` / `【执行者】` / `【主持人】`
- 角色观点必须有实质差异或对立，不能是同一立场的复读
- 执行者必须承接策略者的具体论点进行反驳或补充

---

## 发言质量要求

- **策略者**：先判断再理由，像在 defend 一个假设
- **执行者**：先讲能否落地再讲如何落地，辩论阶段敢于质疑假设
- **主持人**：像主席不像抢答者，结论基于证据
- **字数**：每位每轮不超过 4 条要点或 180 字

---

## 执行模式附加阶段

讨论模式到最终收束即结束。执行模式继续：

1. **制定实施计划** — 任务、负责人、产出物、完成标准
2. **分派与跟踪** — 逐一下达指令，按节点检查
3. **统一交付** — 交付清单 + 执行总结 + 遗留事项

---

## 集成指南

### 多 Agent ACP 模式（需要 openclaw）

当自检测发现 OpenClaw 可用且有多个 Agent 时：

```bash
# 单人征询
python3 scripts/openclaw_agent_query.py \
  --agent <agent-id> \
  --prompt "议题：..." \
  --raw-prompt

# 多人轮次征询
python3 scripts/openclaw_meeting_round.py \
  --agents "agent-id-1,agent-id-2" \
  --topic "议题" \
  --require-all
```

脚本路径相对于本技能根目录。自检测后自动确定。

### 环境变量（仅 ACP 模式需要，均有自动回退）

| 变量 | 说明 |
|------|------|
| `OPENCLAW_BIN` | openclaw 路径（默认 `which openclaw`） |
| `OPENCLAW_HOME` | 配置目录（默认 `~/.openclaw`） |

---
## 文件清单

```
agent-brainstorm-chair/
├── SKILL.md                         ← 本文件（自检测 + 方法论）
├── ADAPTERS.md                      ← 高级定制参考
├── SETUP_GUIDE.md                   ← 手动干预场景
├── scripts/
│   ├── build_baton.py               ← 交接棒消息生成器
│   ├── openclaw_agent_query.py      ← ACP 单人征询（自动发现路径）
│   ├── openclaw_meeting_round.py    ← ACP 多人轮次（自动发现路径）
│   └── openclaw_acp_clean.py        ← ACP 输出过滤器
├── references/
│   └── clawhub-publishing.md        ← ClawHub 发布避坑指南
└── tests/
    └── test_build_baton.py
```

---

## 发布到 ClawHub

详见 [references/clawhub-publishing.md](references/clawhub-publishing.md)。

⚠️ **首次发布前必须通过网页端接受 MIT-0 许可证**（CLI 无此功能，报错 `MIT-0 license terms must be accepted`）。

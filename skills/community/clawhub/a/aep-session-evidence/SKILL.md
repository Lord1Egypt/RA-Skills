---
name: aep-session-evidence
allowed-tools:
  - read
  - write
  - exec
description: AEP 会话过程存证——让 AI 助手感知当前会话，在开始/里程碑/结束时把"确实发生过这样一个创作过程"固化成可独立验证的证据链。当用户提到"过程存证/会话存证/记录过程/结束存证/收工存证"，或检测到会话即将结束（用户说收工/就这样/告一段落、上下文接近压缩、任务交付）时使用。
---

# AEP 会话过程存证（Session Evidence）

> 目标：证明「确实存在过这样一个创作过程」。最终产物可以不存，**过程本身要存**——
> 谁在何时、基于什么输入、做了什么决策、产出了什么中间结果，全部变成哈希链上的结构化事件，
> 会话结束时封包成 `.aep`，任何人可独立验证。

## 一、会话感知信号（何时触发本技能）

| 信号 | 动作 |
|------|------|
| 用户开启一个新任务/说"开始吧" | 建立（或复用）项目 → 记 `session.start` |
| 完成一个重要里程碑（方案定稿/关键决策/阶段产出/重要文件生成） | 记对应事件（见 §三 事件类型） |
| 用户说"结束/收工/就这样/告一段落"，或任务交付、上下文即将压缩 | **先提醒，征询后**（或按用户预设的 auto 模式直接）记 `session.end` 并导出封包 |
| 用户问"刚才那步有没有记录" | `aep list-evidence --project <slug>` 查证 |

**提醒优先，自动可选**：默认在结束信号出现时向用户确认一次（"要不要把本次会话过程存证？"）；
用户明确说过"自动存证/不用问我"则跳过确认直接执行。**绝不**在用户明确拒绝后重复询问。

## 二、标准流程（三段式）

### 1. 会话开始（锚定）
```bash
# CLI（MCP 用 aep_request_evidence，project 必填）
aep evidence session.start --project <slug> \
  --session-id <稳定会话ID> \
  --action "任务一句话描述" --password <pw> --json
```
- `--session-id` 全程保持一致（prevHash 事件链的锚点）；建议 `<slug>-<日期>-<序号>`
- 同步建对话记录文件（如 `<workdir>/session-log.md`），持续追加关键问答/决策

### 2. 里程碑（过程留痕）
```bash
aep evidence <event-type> --project <slug> --session-id <同上> \
  --action "做了什么" --result "关键结论/要点（默认仅存哈希）" --password <pw> --json
```
常用 event-type（自由扩展）：`ai.generation`（AI 产出）、`decision.made`（关键决策）、
`milestone.reached`（里程碑）、`artifact.produced`（中间产物落盘）、`review.passed`（评审通过）。
**完整对话过程**：把 session-log.md 用 `aep artifact add <file> --project <slug>` 存为制品；
中间产生的临时结果可存可不存（用户已确认可不存），但**日志文件本身要存**。

### 3. 会话结束（封包 + 验真）
```bash
# 记结束事件并直接导出该会话的累积证据包（--output 即封包）
aep evidence session.end --project <slug> --session-id <同上> \
  --action "会话结束" --password <pw> --output <slug>-session.aep --json

# 七阶段验真（铁律：验签只用 AEP 工具本身）
aep validate <slug>-session.aep --json
# （可选）升级：--tsa 时间戳 / --chain 区块链锚定，或 aep attest chain <pkg> 补锚
```

## 三、事件与判读
- 每次调用返回 `eventId` + `sessionId`；事件按 `--session-id` 形成 prevHash 链，**事后不可篡改顺序与内容**。
- 导出包随事件数增长；最终包包含全程事件链（L1 SelfSigned 起，加 TSA/链锚定可到 L3/L4）。
- `validate --json` 的权威字段是 **state**（valid/inconclusive/invalid）；invalid 时 level 为 null。
- 查历史：`aep list-evidence --project <slug>`。

## 四、注意事项
- 口令：自定义 `--data-dir` 时每个命令都要带 `--password`；默认目录自动读 `~/.aep/.secret`。
- 敏感内容：`--result` 默认仅存哈希；若确认要存明文，遵循项目数据分级约定，密钥/口令绝不入证据。
- 制品接入事件链：`artifact add` 的制品若未与事件建立关系，validate 会给
  AEP-E012「isolated Artifact」warning → state=inconclusive（部分确立，不是失败）。
  消除：制品化后补一条引用它的事件；或接受 inconclusive 并向用户说明。
- 项目收尾：`aep project close <slug>`；长期归档 `aep project archive <slug>`。

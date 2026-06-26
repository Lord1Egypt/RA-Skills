# Usage Patterns

## First-Time Setup

```bash
python3 scripts/run.py auth_manager.py status
python3 scripts/run.py auth_manager.py setup
python3 scripts/run.py auth_manager.py validate
```

## One-Shot Ask

```bash
python3 scripts/run.py ask_chatgpt.py --question "用三句话解释 Transformer"
```

## Controlled Model + Proof Workflow

```bash
python3 scripts/run.py ask_chatgpt.py \
  --new-chat \
  --model "GPT 5.4 Thinking" \
  --extended-thinking \
  --proof-screenshot \
  --question "请你推荐最近一个月，RLVR领域的论文"
```

## Continue an Existing Conversation

```bash
python3 scripts/run.py ask_chatgpt.py --conversation-id 12345678-aaaa-bbbb-cccc-1234567890ab --question "继续展开"
```

## Persistent Multi-Turn Session

```bash
python3 scripts/run.py session_manager.py create
python3 scripts/run.py session_manager.py ask --session-id session-xxxxxxxxxxxx --question "先解释核心结论"
python3 scripts/run.py session_manager.py ask --session-id session-xxxxxxxxxxxx --question "再给一个例子"
```

## Persistent Session with Model Control

```bash
python3 scripts/run.py session_manager.py ask \
  --session-id session-xxxxxxxxxxxx \
  --new-chat \
  --model "GPT 5.4 Thinking" \
  --extended-thinking \
  --proof-screenshot \
  --question "请你推荐最近一个月，RLVR领域的论文"
```

## Conversation Management

```bash
python3 scripts/run.py chat_manager.py list
python3 scripts/run.py chat_manager.py current
python3 scripts/run.py chat_manager.py new
python3 scripts/run.py chat_manager.py open --conversation-id 12345678-aaaa-bbbb-cccc-1234567890ab
```

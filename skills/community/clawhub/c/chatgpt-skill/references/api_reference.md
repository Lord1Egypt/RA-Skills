# CLI Reference

## Authentication

- `python3 scripts/run.py auth_manager.py status`
- `python3 scripts/run.py auth_manager.py validate`
- `python3 scripts/run.py auth_manager.py setup`
- `python3 scripts/run.py auth_manager.py logout`

## Ask ChatGPT

- `python3 scripts/run.py ask_chatgpt.py --question "..."`
- `python3 scripts/run.py ask_chatgpt.py --conversation-id <id> --question "..."`
- `python3 scripts/run.py ask_chatgpt.py --question "..." --show-browser`
- `python3 scripts/run.py ask_chatgpt.py --new-chat --model "GPT 5.4 Thinking" --extended-thinking --proof-screenshot --question "请你推荐最近一个月，RLVR领域的论文"`

## Session Manager

- `python3 scripts/run.py session_manager.py create`
- `python3 scripts/run.py session_manager.py create --conversation-id <id>`
- `python3 scripts/run.py session_manager.py ask --session-id <id> --question "..."`
- `python3 scripts/run.py session_manager.py ask --session-id <id> --new-chat --model "GPT 5.4 Thinking" --extended-thinking --proof-screenshot --question "..."`
- `python3 scripts/run.py session_manager.py list`
- `python3 scripts/run.py session_manager.py info --session-id <id>`
- `python3 scripts/run.py session_manager.py reset --session-id <id>`
- `python3 scripts/run.py session_manager.py close --session-id <id>`
- `python3 scripts/run.py session_manager.py gc`

## Conversation Manager

- `python3 scripts/run.py chat_manager.py list`
- `python3 scripts/run.py chat_manager.py current`
- `python3 scripts/run.py chat_manager.py new`
- `python3 scripts/run.py chat_manager.py open --conversation-id <id>`
- `python3 scripts/run.py chat_manager.py delete --conversation-id <id>`

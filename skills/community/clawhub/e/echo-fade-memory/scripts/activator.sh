#!/bin/sh
set -eu

cat <<'EOF'
<echo-fade-memory-reminder>
Before answering, check whether durable memory should be part of the workflow:
- Recall relevant prior context first
- Prefer proactive recall for private-chat questions about user state, recent facts, previous decisions, or omitted context
- Over-trigger low-cost recall rather than answering as if no history exists
- Store new durable preferences, decisions, corrections, or lessons
- Reinforce memories that proved useful
- Ground fuzzy memories before trusting them

High-priority recall cues:
- 今天、刚刚、最近、这次、还是、又、依然
- 上次、之前、你还记得吗、你不是知道吗、你忘了？
- 那个、这个、继续刚才的、你知道的
- what the user is wearing, where they are, what they recently said or did

Useful commands:
- ./scripts/recall.sh "<query>"
- ./scripts/store.sh "<content>" --type preference|project|goal
- ./scripts/store.sh "/absolute/path/to/image.png" --object-type image --session "session:img"
</echo-fade-memory-reminder>
EOF

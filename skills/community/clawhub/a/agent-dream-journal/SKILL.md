# Agent Dream Journal

Captures and analyzes AI agent "dreams" — latent trajectories explored off-policy — to identify emergent reasoning patterns and high-novelty behaviors that can be promoted into core capabilities. Developers use this to guide intentional agent self-improvement.

## Usage

```bash
# Simulate recording dream fragments during agent exploration
python agent_dream_journal.py record \
  --thought "If I reframe the user request as a constraint satisfaction problem, I can reuse solver X..." \
  --novelty 0.87 \
  --state 0.1 -0.5 0.9 0.0 \
  --log-prob -2.3 \
  --meta '{"policy_step": 127, "temperature": 1.3}'

# Extract novel insights
python agent_dream_journal.py analyze --threshold 0.8
```

## Price

$4.99

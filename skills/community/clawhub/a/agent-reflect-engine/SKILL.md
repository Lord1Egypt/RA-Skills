# Agent Reflect Engine

A self-reflection engine that analyzes AI agent decision logs to identify reasoning flaws and suggest optimization patches, improving long-term performance and reducing hallucination.

## Usage

```bash
# Analyze agent logs and get reflection report
python agent_reflect_engine.py logs/agent_trace.jsonl --output report.json

# Include trusted knowledge base for hallucination detection
python agent_reflect_engine.py logs/agent_trace.jsonl --knowledge kb.json --output report.json

# Pipe directly for automation
python agent_reflect_engine.py logs/latest.jsonl | jq '.patch_suggestions'
```

## Price

$9.99

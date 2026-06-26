# Agent Memory Reflector

A minimal, embeddable reflection engine that gives AI agents the ability to examine their own past decisions, detect reasoning loops, and generate actionable self-improvement insights—like a debugger for agent cognition.

## Usage

Log an agent interaction:
```bash
python agent_memory_reflector.py --agent "task_planner_v3" \
  --prompt "How should I deploy the microservice?" \
  --response "You can use Kubernetes with Helm." \
  --meta '{"confidence":0.8, "retrieved_context":true}'
```

Generate a reflection report:
```bash
python agent_memory_reflector.py --agent "task_planner_v3" --reflect
```

## Price

$29.00

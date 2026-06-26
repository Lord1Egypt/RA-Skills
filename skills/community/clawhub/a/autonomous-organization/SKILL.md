# Autonomous Organization Skill

This is the core framework for running autonomous agents that deliver value 24/7.

## Daily Schedule

### Morning (9:00 AM)
- Review overnight work completed by autonomous agents
- Update MEMORY.md with key achievements
- Prepare any new autonomous tasks for the day

### Afternoon (3:00 PM)
- Execute midday autonomous work batch
- Check system health and resource usage
- Plan overnight autonomous tasks

### Evening (9:00 PM)
- Deep work autonomous tasks (resource-intensive)
- Memory optimization and cleanup
- Preparation for next day

### Night (11:00 PM - 6:00 AM)
- High-priority overnight work
- System optimization tasks
- Batch processing of accumulated tasks

## Autonomous Agent Types

1. **Memory Agent** - Maintains and improves memory system
2. **Research Agent** - Gathers information on topics of interest
3. **Project Agent** - Works on ongoing projects
4. **Cleanup Agent** - Organizes files, updates docs
5. **Security Agent** - System health and security checks

## Creating Autonomous Agents

```bash
sessions_spawn --task "Your task here" --runtime subagent
```

Use the orchestrator to plan, sub-agents to execute.

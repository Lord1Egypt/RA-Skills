# OpenClaw Integration

## Skill Invocation

Users invoke with: `/autoagent`

## Orchestration

On first invocation:
1. Read setup-prompt.md
2. Ask user questions
3. Create sandbox
4. Set up cron

## Cron Setup

The skill creates a cron job that runs every 5 minutes:
- Uses OpenClaw cron syntax
- Invokes iteration-prompt.md with sandbox path
- Passes context: sandbox directory, current iteration

## Subagent Execution

Each iteration spawns a subagent to:
- Execute the task with guidance
- Return output for scoring
- Isolate test runs from main agent

## File Locations

- Skill: /home/peterwsl/clawd/skills/autoagent/
- Sandbox: {user workspace}/autoagent/
- Cron: OpenClaw managed

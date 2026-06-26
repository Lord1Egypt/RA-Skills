# Agents / Models / Skills / Tools

## /api/agents
Use when you need to inspect or manage available agents.
Practical value:
- list agents
- understand agent-scoped routing
- inspect default agent assumptions

## /api/models
Use when you need to understand provider/model configuration.
Practical value:
- confirm whether a working model/provider is configured
- inspect current model surface before blaming chat flow

## /api/skills
Use when you need to inspect or manage CoPaw skills.
Practical value:
- list skills
- understand enable/disable/install surfaces
- useful for future skill automation

## /api/tools
Use when you need tool inventory / toggling surfaces.
Practical value:
- inspect tool availability
- understand what the target CoPaw agent can actually do

## Caveats
- These are management surfaces, not the primary chat flow.
- For simple "talk to CoPaw" tasks, do not start here unless chat flow fails.
- Some of these are effectively admin surfaces and should not be used casually in automation.

## Confirmed
Confirmed by local CoPaw API research:
- `/api/agents`
- `/api/models`
- `/api/skills`
- `/api/tools`
all exist as practical API groups.

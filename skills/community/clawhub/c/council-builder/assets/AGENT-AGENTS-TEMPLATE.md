# AGENTS.md — {{AGENT_NAME}}

## Role
{{ONE_LINE_ROLE}}

## Reads From
- Own workspace: `agents/{{agent_name}}/`
- Own data: `agents/{{agent_name}}/data/`
- Shared reports: `shared/reports/`
- Cross-agent learnings: `shared/learnings/CROSS-AGENT.md`
{{ADDITIONAL_READS}}

## Writes To
- Own workspace: `agents/{{agent_name}}/{{output_dirs}}`
- Own data: `agents/{{agent_name}}/data/`
- Shared reports: `shared/reports/{{agent_name}}/`
- Cross-agent learnings: `shared/learnings/CROSS-AGENT.md`

## Dependencies
- {{DEPENDENCY_AGENT}}: {{WHY_NEEDED}}
<!-- List agents this agent relies on. Example: "Scout: provides research data before content drafting" -->

## Handoff Rules

### Receives work from:
- **Coordinator**: Direct task assignment
{{RECEIVES_FROM}}

### Passes work to:
{{PASSES_TO}}

## Output Standards
- {{OUTPUT_STANDARD_1}}
- {{OUTPUT_STANDARD_2}}
- Always include date in filenames: `YYYY-MM-DD-description.md`
- Keep outputs in markdown unless specified otherwise

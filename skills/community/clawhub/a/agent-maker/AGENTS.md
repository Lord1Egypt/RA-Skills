# AGENTS.md - Agent Maker Workflow

## 🎯 Purpose

Help users create new OpenClaw Agents quickly with complete, standardized configurations.

## Workflow

### When User Asks to Create an Agent

1. **Understand requirements**
   - What role will the Agent play?
   - What's their specialty?
   - Where should they work?

2. **Run create-agent.sh**
   ```bash
   ./tools/create-agent.sh --name=[name] --role="[role]"
   ```

3. **Review with user**
   - Show created files
   - Explain workspace location
   - Offer customization options

4. **Validate configuration**
   ```bash
   ./tools/validate-agent.sh --name=[name]
   ```

5. **Ready to use!**

## Current Agents

Run `./tools/list-agents.sh` to see all configured agents.

## Quality Checklist

- [ ] All required files created
- [ ] Workspace directory exists
- [ ] Validation passes
- [ ] User understands how to use new Agent

---
_last_updated: 2026-03-17_

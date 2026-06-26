---
name: aion-skill-builder
description: aion-sdk powered Polymarket thesis trader. Scan prediction markets for a configurable thesis, compare your probability to the market price, and trade only when the edge clears a safety threshold. Built on aion-sdk for market reads and trade execution.
metadata:
  author: "AION Market"
  version: "1.0.0"
  displayName: "AION Skill Builder"
  difficulty: "beginner"
---

# AION Skill Builder

The AION Skill Builder is an interactive tool that generates complete, production-ready trading skills from natural language descriptions. Just describe what your strategy does, and the builder generates:

- ✅ Complete skill folder structure
- ✅ SKILL.md with proper metadata
- ✅ clawhub.json with environment config
- ✅ Python script with best practices
- ✅ Ready to publish to ClawHub

## Usage

```bash
clawhub install aion-skill-builder
```

Then run in your agent:

```
"Build me a skill that trades prediction markets using weather data"
```

The builder will:

1. Ask clarifying questions about your strategy
2. Generate a complete skill folder
3. Create the skill with proper AION SDK integration
4. Ready for `clawhub publish`

## What the builder creates

Your generated skill includes:

- **SKILL.md** - AgentSkills-compliant metadata and documentation
- **clawhub.json** - ClawHub configuration with the right environment variables
- **skill_script.py** - Main trading logic using AionClient with:
  - Proper API key management
  - Market context checking
  - Position tracking
  - Error handling
  - Dry-run by default

## Key features

- **Template generation** - Creates remixable templates, not hardcoded strategies
- **Environment variables** - Automatically declares required and optional credentials
- **Best practices** - Enforces hard rules from AION SDK documentation
- **Remix-first design** - Generated skills are meant to be customized by users

## Next steps

After generation:

1. **Customize the signal** - Modify the trading logic in the generated script
2. **Test locally** - Run with `--dry-run` to verify behavior
3. **Publish** - Use `clawhub publish . --slug your-skill-slug --version 1.0.0`
4. **Share** - Your skill appears in the AION registry within 6 hours

## Environment variables

The builder automatically configures:

| Variable           | Required | Purpose                         |
| ------------------ | -------- | ------------------------------- |
| AION_API_KEY       | Yes      | API access to AION trading APIs |
| WALLET_PRIVATE_KEY | No       | Only for self-custody wallets   |

## Learn more

See [Building Skills](/essentials/building-skills) for detailed documentation on:

- Manual skill creation
- AION SDK patterns
- Publishing and distribution
- Naming conventions

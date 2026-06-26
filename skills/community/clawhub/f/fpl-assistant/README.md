# FPL Assistant Skill

A knowledge skill for AI agents assisting users with Fantasy Premier League (FPL) decisions. This skill enables agents to provide informed recommendations on transfers, captain picks, lineup selection, and chip strategy using live FPL data.

## When the Skill Is Triggered

This skill activates when users mention:

- **FPL terminology**: `FPL`, `fantasy premier league`, `fantasy`, `GW` (gameweek)
- **Decisions**: `captain`, `transfer`, `chip`, `wildcard`, `free hit`, `bench boost`, `triple captain`
- **Requests**: asking for lineup suggestions, transfer advice, gameweek analysis, FPL rules explanation

## How to Use in OpenClaw

### Installation

1. **Download the skill** — Clone or copy this repository into your OpenClaw workspace skills directory:
   ```
   workspace/skills/fpl-assistant/
   ```
2. **Install dependencies** — None required. This is a pure documentation skill with no code dependencies.
3. **Have OpenClaw read SKILL.md thoroughly** — Before using the skill, ask OpenClaw to read through `SKILL.md` completely so it fully understands the workflow, trigger phrases, reference file locations, and recommended output format.
4. **Activate the skill** — OpenClaw will automatically detect trigger phrases and load the skill when needed.

### Usage

When a user asks an FPL-related question, the agent automatically:

1. **Detects the trigger** and activates the skill
2. **Reads the skill definition** from SKILL.md
3. **Follows the 6-step workflow** — gathering context, fetching live FPL API data, applying multi-dimensional analysis (per strategy.md), and producing recommendations
4. **Returns structured output** in the format defined in SKILL.md

Reference documents are consulted as needed: `references/api.md` for API calls, `references/rules.md` for rules, `references/strategy.md` for analysis methodology.

## Skill Workflow

The skill defines a 6-step process for FPL assistance:

1. **Gather context** — Collect the user's squad state (manager ID, budget, current transfers, active chips, target GW)
2. **Fetch live data** — Call FPL API endpoints (bootstrap-static, fixtures, element-summary)
3. **Multi-dimensional analysis** — Layer FDR with form, motivation, fixture congestion, home/away, head-to-head matchups, xG regression
4. **Transfer strategy** — Evaluate free transfers, rolling FTs, -4 hit guidelines
5. **Captain selection** — Weight fixture difficulty, form, home/away, set-piece risk, minutes, ownership
6. **Chip strategy** — Advise on wildcard, free hit, bench boost, and triple captain timing windows

## Reference Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition, trigger phrases, and core workflow |
| `references/rules.md` | FPL scoring rules, squad structure, transfer mechanics, chip effects |
| `references/api.md` | FPL API endpoints, data structures, Python code snippets |
| `references/strategy.md` | Advanced multi-factor analysis methodology, positional strategy, chip timing windows |

## Key Notes

- **FDR is insufficient alone** — Use the multi-factor approach in `references/strategy.md`. FDR (Fixture Difficulty Rating) is a starting point; form, motivation, fixture congestion, and head-to-head history must be layered in.
- **Cache bootstrap-static** — Call `/bootstrap-static/` once and cache it (~2MB); it contains all player/team/gameweek data.
- **Chip timing windows**:
  - Wildcard: GW3–5 or GW20–22
  - Free Hit: blank gameweeks (BGW)
  - Bench Boost: double gameweeks (DGW)
  - Triple Captain: DGW with premium players
- **Season arc**: GW1–8 patience, GW9–19 first wildcard, GW20–25 second wildcard, GW26–30 chip planning, GW31–38 execute.

## Example API Usage

```bash
# Fetch master data (cache this)
curl https://fantasy.premierleague.com/api/bootstrap-static/

# Get fixtures with FDR
curl https://fantasy.premierleague.com/api/fixtures/

# Get player history and upcoming fixtures
curl https://fantasy.premierleague.com/api/element-summary/{player_id}/

# Get a manager's squad for a gameweek
curl https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gw}/picks/
```

## File Structure

```
fpl-assistant/
├── README.md           ← you are here
├── SKILL.md            ← skill definition and trigger config
└── references/
    ├── api.md          ← FPL API reference
    ├── rules.md        ← FPL rules and scoring
    └── strategy.md      ← advanced decision methodology
```
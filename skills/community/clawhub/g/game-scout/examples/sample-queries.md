# Sample Query Pipelines

Four complete examples showing how the research pipeline applies to different query types. Use these to calibrate depth and approach.

---

## Example 1: Build Query

**User asks**: "What are the best SMG builds in Marathon right now?"

### Phase 1 — Analysis
- **Game**: Marathon
- **Topic**: Build/Loadout (SMG weapon class)
- **Recency**: Critical — Marathon is a new, live-service game with frequent patches
- **Scope**: Broad — user wants multiple options, not one specific build

### Phase 2 — Discovery Queries
Fire in parallel:

**Exa AI**:
- `"best SMG builds Marathon current patch"`
- `"Marathon SMG loadout guide competitive"`

**Bright Data SERP batch**:
- `Marathon best SMG build 2026 reddit`
- `site:reddit.com r/Marathon SMG build`
- `site:youtube.com Marathon SMG build guide 2026`

**Twitter**: `Marathon SMG meta` (recent takes)

### Phase 3 — Extraction Targets
- Top 3 Reddit threads from r/Marathon discussing SMG builds
- Top 2 YouTube guides (extract transcripts for weapon/attachment specifics)
- Any wiki or database page for SMG weapon stats

### Phase 4 — Synthesis
- Cross-reference which SMGs are recommended across Reddit + YouTube
- Verify attachment/mod recommendations are consistent
- Check if any of the recommended SMGs were buffed/nerfed in recent patches
- Note if recommendations differ for PvP vs PvE

### Phase 5 — Response Format
```
## TL;DR
[Top 2-3 SMGs with their key attachments in a quick list]

## Recommended SMG Builds

| SMG | Barrel | Mag | Optic | Perk | Best For |
|-----|--------|-----|-------|------|----------|
| ... | ...    | ... | ...   | ...  | PvP/PvE  |

## Why These Work
[Explain the TTK advantage, range profile, or synergy]

## Alternatives
- [Alternate SMG] — better for [situation]

## Caveats
- Patch [X.Y] may change the SMG balance
- [Specific SMG] has a high recoil skill floor

## Sources
1. [Reddit thread] — r/Marathon, [date]
2. [YouTube video] — [Creator], [date]
3. [Article/wiki] — [site], [date]

## Confidence: HIGH
3 sources agree on top picks, all from current patch.
```

---

## Example 2: Mechanic/Interaction Query

**User asks**: "Does the Xenotech Gauntlet proc bleed in Marathon?"

### Phase 1 — Analysis
- **Game**: Marathon
- **Topic**: Mechanic/Interaction — specific item behavior
- **Recency**: Moderate — mechanic may have changed with patches
- **Scope**: Narrow — yes/no answer with details

### Phase 2 — Discovery (Limited)
Skip broad discovery. Target specific sources:

**Exa AI**:
- `"Xenotech Gauntlet bleed Marathon interaction"`

**Bright Data SERP**:
- `"Xenotech Gauntlet" Marathon bleed proc`
- `site:reddit.com Marathon "Xenotech Gauntlet" bleed`

### Phase 3 — Extraction
- Wiki/database page for Xenotech Gauntlet (stats, perk descriptions)
- Any Reddit thread discussing the item's mechanics
- If ambiguous: a YouTube video testing the item

### Phase 4 — Synthesis
- Does the wiki confirm bleed proc? If yes, done.
- If wiki is ambiguous, check Reddit for community testing results
- Note if this was changed in a recent patch

### Phase 5 — Response Format
```
## Answer
[Yes/No/Conditionally] — [one-line explanation]

## How It Works
[Detailed interaction: what triggers bleed, damage numbers, duration, stacking]

## Patch Note
[If relevant: "This was changed in patch X.Y — previously it did/didn't..."]

## Sources
1. [Wiki] — [date]
2. [Reddit confirmation] — [date]

## Confidence: HIGH/MEDIUM
[Based on source quality]
```

---

## Example 3: Meta/Patch Query

**User asks**: "Is bleed still meta in Elden Ring after the latest patch?"

### Phase 1 — Analysis
- **Game**: Elden Ring
- **Topic**: Meta + Patch impact
- **Recency**: Critical — the question is specifically about post-patch viability
- **Scope**: Broad — need patch notes + community reaction + current meta status

### Phase 2 — Discovery Queries
Fire in parallel:

**Exa AI**:
- `"Elden Ring bleed build viability latest patch"`
- `"Elden Ring current meta builds after nerf"`

**Bright Data SERP batch**:
- `Elden Ring bleed nerf latest patch reddit`
- `site:reddit.com r/EldenRing bleed meta patch`
- `Elden Ring patch notes [latest version]`
- `site:youtube.com Elden Ring bleed build after patch`

**Twitter**: `Elden Ring bleed patch` (immediate community reaction)

### Phase 3 — Extraction
- Official patch notes (from Bandai Namco or FromSoftware)
- Top 3 Reddit threads discussing bleed post-patch
- 1-2 YouTube videos testing bleed builds after the update
- Fextralife wiki page for Bleed status effect (check if updated)

### Phase 4 — Synthesis
- What exactly changed about bleed in the patch? (stat nerfs? weapon changes? proc rate?)
- What is the community consensus? (still viable? significantly worse? dead?)
- Are there adapted builds that still make bleed work?
- What has replaced bleed if it's no longer meta?

### Phase 5 — Response Format
```
## TL;DR
[One-line verdict on bleed's current state]

## What Changed (Patch X.Y)
- [Specific change 1]
- [Specific change 2]

## Current State
[Is bleed still viable? At what level of play? In what contexts?]

## Adapted Builds
[If bleed still works with adjustments, show the adapted build]

## Alternatives
[If bleed fell off, what replaced it in the meta?]

## Community Sentiment
[Summary of Reddit/Twitter reaction — is this a "sky is falling" overreaction or a genuine meta shift?]

## Sources
1-5 sources with dates

## Confidence: HIGH
Multiple patch-era sources confirmed.
```

---

## Example 4: Pro Play / Current Meta Query

**User asks**: "What are pros running in Valorant right now?"

### Phase 1 — Analysis
- **Game**: Valorant
- **Topic**: Pro play / esports meta
- **Recency**: Critical — pro meta shifts weekly
- **Scope**: Broad — covers agent picks, compositions, strategies

### Phase 2 — Discovery Queries
Fire in parallel:

**Exa AI**:
- `"Valorant pro meta agent picks current patch"`
- `"Valorant Champions Tour team compositions 2026"`

**Bright Data SERP batch**:
- `Valorant pro meta 2026 agent tier list`
- `site:reddit.com r/ValorantCompetitive meta agents`
- `site:liquipedia.net Valorant tournament results 2026`
- `site:youtube.com Valorant pro meta analysis 2026`
- `site:tracker.gg valorant agents meta`

**Twitter**: `Valorant pro meta` + recent pro player tweets

### Phase 3 — Extraction
- tracker.gg/valorant: agent pick rates in pro play (or ranked Immortal+)
- Liquipedia: recent tournament results and team compositions
- Reddit r/ValorantCompetitive: meta discussion threads
- YouTube: pro meta analysis videos (1-2 transcripts)
- Twitter: pro player agent preferences, team comp reveals

### Phase 4 — Synthesis
- Which agents have the highest pick/ban rates in pro play?
- What team compositions are dominant?
- Is the ranked meta different from the pro meta? (important to note)
- Any recent agent changes that are shifting the meta?

### Phase 5 — Response Format
```
## TL;DR
[Top 3-5 must-pick agents and the dominant comp style]

## Current Pro Meta (Patch X.Y)

### S Tier — Must-Pick
- **[Agent]** — [why, pick rate%]
- **[Agent]** — [why, pick rate%]

### A Tier — Strong Flex Picks
- **[Agent]** — [context]

### Falling Off
- **[Agent]** — [why they dropped]

## Dominant Compositions
1. [Comp name] — [agents] — [what it does well]
2. [Comp name] — [agents] — [when to run it]

## Pro vs Ranked
[Key differences between what pros run and what works in ranked]

## Recent Shifts
[What changed recently and why — patch notes, tournament results, new discoveries]

## Sources
1-5 sources with dates

## Confidence: HIGH
Based on tournament data + tracker stats + pro player discussion.
```

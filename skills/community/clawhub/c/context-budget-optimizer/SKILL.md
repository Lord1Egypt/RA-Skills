---
name: context-budget-optimizer
version: 1.0.0
price: 19
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# Context Budget Optimizer

**Framework: The Token Efficiency Matrix**
*Worth $200/hr consultant time. Yours for $19.*

---

## What This Skill Does

Audits your agent's token usage across every context layer, identifies where you're burning budget on bloat, and produces a 3-week cost reduction roadmap with concrete implementation steps.

**Problem it solves:** Power users hitting $200-500/month in AI costs often have 60-70% waste baked into their context. Most of it is invisible: stale files in system prompts, redundant skill loading, oversized memory files, wrong model choices. The Token Efficiency Matrix makes the waste visible and rankable.

---

## The Token Efficiency Matrix

A 4-quadrant audit tool that scores every context element by **cost** (token weight) and **ROI** (value delivered per token). High cost + low ROI = cut first.

### The Matrix

```
                    HIGH ROI
                       │
          KEEP         │      OPTIMIZE
       (High ROI,      │   (High ROI,
        Low Cost)      │    High Cost)
                       │
LOW COST ──────────────┼────────────────── HIGH COST
                       │
          AUDIT        │       CUT
       (Low ROI,       │   (Low ROI,
        Low Cost)      │    High Cost)
                       │
                    LOW ROI
```

**Action by quadrant:**
- **KEEP:** Don't touch. It's working efficiently.
- **OPTIMIZE:** Compress or lazy-load. Value is there, just expensive.
- **AUDIT:** Review quarterly. Low cost so not urgent, but ROI should be questioned.
- **CUT:** Kill immediately. You're paying for nothing.

---

## Phase 1: Context Inventory

**Before scoring, map everything that's in your agent's context.**

### Context Layers to Audit

```
Layer A: System Prompt / SOUL.md / Identity files
Layer B: Active skills (loaded per session)
Layer C: Memory files (MEMORY.md, daily notes)
Layer D: Project files injected at startup
Layer E: Tool outputs / MCP responses in context
Layer F: Chat history (conversation turns kept in context)
Layer G: Code or data files read into context
```

### Inventory Template

For each item in your context, fill this in:

| Item | Layer | Est. Tokens | Sessions/Day | Daily Cost* | Value (1-5) |
|------|-------|-------------|--------------|-------------|-------------|
| SOUL.md | A | ___ | ___ | ___ | ___ |
| MEMORY.md | C | ___ | ___ | ___ | ___ |
| [Skill 1].md | B | ___ | ___ | ___ | ___ |
| [Skill 2].md | B | ___ | ___ | ___ | ___ |
| Daily notes | C | ___ | ___ | ___ | ___ |
| [Project file] | D | ___ | ___ | ___ | ___ |

*Daily Cost = (Est. Tokens / 1M) × model_rate × sessions_per_day

**Token estimation cheatsheet:**
- 1 page of text ≈ 500-700 tokens
- 1 SKILL.md file ≈ 800-2,000 tokens
- 1 code file (100 lines) ≈ 1,200-1,800 tokens
- 1 MEMORY.md (well-maintained) ≈ 500-1,500 tokens
- 1 MEMORY.md (neglected/bloated) ≈ 3,000-8,000 tokens

**Model rates (as of Q1 2026, approximate):**
| Model | Input Cost per 1M tokens |
|-------|--------------------------|
| Claude Haiku 3.5 | ~$0.80 |
| Claude Sonnet 4 | ~$3.00 |
| Claude Opus 4 | ~$15.00 |
| GPT-4o mini | ~$0.15 |
| GPT-4o | ~$2.50 |

---

## Phase 2: Scoring (Token Efficiency Matrix)

**Score each context item:**

**Cost Score (1-5):**
| Score | Token Range | Description |
|-------|-------------|-------------|
| 1 | < 200 tokens | Tiny — negligible |
| 2 | 200-500 tokens | Light |
| 3 | 500-1,500 tokens | Medium |
| 4 | 1,500-4,000 tokens | Heavy |
| 5 | > 4,000 tokens | Very heavy |

**ROI Score (1-5):**
| Score | Description |
|-------|-------------|
| 1 | Rarely used, generic, stale |
| 2 | Occasionally useful |
| 3 | Moderately useful most sessions |
| 4 | Consistently referenced, shapes output |
| 5 | Critical — session breaks without it |

**Matrix placement:**
- Cost 1-2, ROI 4-5 → **KEEP**
- Cost 4-5, ROI 4-5 → **OPTIMIZE**
- Cost 1-2, ROI 1-2 → **AUDIT**
- Cost 4-5, ROI 1-2 → **CUT**
- Cost 3, ROI 3 → **AUDIT** (marginal — evaluate quarterly)

---

## Phase 3: Reduction Playbook

### CUT (implement immediately)

**Items to eliminate first:**
```
□ Old memory entries > 90 days with no references
□ Skills loaded globally that are only used occasionally
□ Duplicate information in multiple files
□ Verbose templates inside system prompts
□ Commented-out code in injected files
□ Debug logs included in context
□ Full file contents when only summaries are needed
```

**Cut target:** 30-40% token reduction with zero quality loss.

---

### OPTIMIZE (implement week 1-2)

#### Tactic 1: Lazy Loading

Instead of loading all skills at startup, load only when triggered.

**Before (eager load):**
```
System prompt includes all 10 skill files → 15,000 tokens every session
```

**After (lazy load):**
```
System prompt includes skill index only → 500 tokens
Individual skills loaded on demand → 1,000 tokens when needed
Net: 14,000 token reduction per session (93% savings for skills)
```

**Lazy load implementation:**
```markdown
# SKILL-INDEX.md (500 tokens instead of full skills)

Available skills — load when needed:
- mcp-server-setup-kit: MCP connection setup
- agentic-loop-designer: Build autonomous loops  
- context-budget-optimizer: Token cost reduction
- [etc]

To use a skill: "Use the [skill-name] skill"
```

---

#### Tactic 2: Memory Tiering

Not all memory is equally important. Tier it.

```
Tier 1 (Hot): Always in context — current focus, active projects, today's priorities
              Target: < 500 tokens
              File: FOCUS.md

Tier 2 (Warm): Loaded on demand — historical decisions, completed projects
               Target: < 2,000 tokens
               File: MEMORY.md (summarized)

Tier 3 (Cold): Never auto-loaded — old daily notes, archived projects
               Storage: Flat files, searchable on request
               File: memory/archive/
```

**Memory tiering implementation:**
1. Create `FOCUS.md` (Tier 1) — just this week's priorities
2. Archive daily notes older than 14 days to `memory/archive/`
3. Summarize MEMORY.md quarterly (remove resolved items)
4. Set system prompt to only inject FOCUS.md + recent 7 days of memory

---

#### Tactic 3: Compression Templates

Replace verbose content with compressed references.

**Before (bloated system prompt section):**
```
David Flynn is a founder based in Austin, Texas. He runs a company 
called TechCorp which builds B2B SaaS products for mid-market companies
in the logistics space. He has been doing this for 8 years and previously
worked at McKinsey. He prefers direct communication without fluff. He
cares about metrics and ROI above all else. His team has 6 people...
[300 tokens]
```

**After (compressed):**
```
Owner: David Flynn | Austin TX | TechCorp (B2B SaaS, logistics, mid-market)
Background: 8yr founder, ex-McKinsey | Team: 6
Style: Direct, metric-first, no fluff
[40 tokens — 87% reduction]
```

---

#### Tactic 4: Model Downgrade Opportunities

Most context-heavy sessions don't need the flagship model.

**Downgrade decision tree:**
```
Is this task requiring multi-step reasoning? 
├── No → Use Haiku (80-90% cost reduction)
└── Yes → Is it a novel problem?
    ├── No (familiar pattern) → Use Sonnet
    └── Yes (genuinely complex) → Use Opus
```

**Model savings calculator:**
| Switch | Token Cost Reduction | When Safe |
|--------|---------------------|-----------|
| Opus → Sonnet | 80% | Most writing, analysis, ops |
| Sonnet → Haiku | 75% | Simple reads, status checks, formatting |
| Opus → Haiku | 95% | Very simple tasks only |

---

#### Tactic 5: Context Window Management

Stop re-injecting the same content in long sessions.

```
Long session patterns that bloat cost:
✗ Re-reading the same files multiple times in one session
✗ Asking agent to "remember" things it already read
✗ Injecting full file contents when you need 5 lines
✗ Running searches and keeping all results in context

Fixes:
✓ Use targeted reads (read lines 45-52, not full file)
✓ Reference by location ("check FOCUS.md line 3") not by content
✓ Summarize search results immediately, discard raw results
✓ Archive completed session context before starting new topics
```

---

## 3-Week Cost Reduction Roadmap

### Week 1: Cut & Quick Wins

**Target: 30-40% cost reduction**

```
Day 1-2:
□ Complete Phase 1 Context Inventory
□ Complete Phase 2 Matrix Scoring
□ Identify all CUT items
□ Delete / archive CUT items

Day 3-4:
□ Create FOCUS.md (Tier 1 memory)
□ Archive memory older than 14 days
□ Compress system prompt (compression templates)

Day 5-7:
□ Measure token reduction (compare sessions before/after)
□ Recalculate daily cost estimate
□ Log baseline vs. current in tracking file
```

---

### Week 2: Optimize Structure

**Target: Additional 20-30% reduction**

```
Day 8-10:
□ Implement skill lazy-loading
□ Create SKILL-INDEX.md
□ Remove individual skill files from startup context
□ Test: skills still work when called by name

Day 11-13:
□ Apply model routing matrix (stop defaulting to Opus)
□ Document which tasks go to which model
□ Implement sub-agent model selection rules

Day 14:
□ Mid-point measurement
□ Are you on track for 50%+ total reduction?
```

---

### Week 3: Lock In & Monitor

**Target: Establish monitoring + reach 50%+ total reduction**

```
Day 15-17:
□ Set up cost tracking (even a simple spreadsheet)
□ Log: daily sessions × avg tokens × model rate = daily cost
□ Set weekly budget alert threshold

Day 18-20:
□ Summarize MEMORY.md (remove stale/resolved entries)
□ Review skill catalog — retire unused skills
□ Final context audit: re-run Matrix Scoring

Day 21:
□ Document final savings: before vs. after
□ Set quarterly review reminder
□ Share results (post on X? 🧵)
```

---

## Token Efficiency Scoring Rubric

After completing the 3-week roadmap, score your setup:

| Metric | 0 | 1 | 2 |
|--------|---|---|---|
| Average session tokens | > 50K | 20-50K | < 20K |
| Skills lazy-loaded | None | Some | All |
| Memory tiered correctly | No | Partially | Yes |
| Model routing applied | No | Ad hoc | Systematic |
| Context reviewed quarterly | No | Annually | Quarterly |

**Score 8-10:** Token-efficient operator. You're in the top 5% of AI users by cost.
**Score 5-7:** Good progress. Keep tightening.
**Score 0-4:** High burn rate. Revisit Week 1 of the roadmap.

---

## Quick Reference: The 10 Highest-ROI Cuts

If you do nothing else, do these 10 things:

1. Archive memory older than 30 days
2. Switch routine tasks from Opus/Sonnet to Haiku
3. Lazy-load skills instead of always-on
4. Compress system prompt (verbose → structured)
5. Stop re-reading files in the same session
6. Archive daily notes older than 14 days
7. Create FOCUS.md and limit startup context to it
8. Remove code files from context when not actively editing
9. Summarize MCP tool outputs instead of keeping raw results
10. Set model routing rules in AGENTS.md

**Combined impact:** 50-70% cost reduction for most users.

---

## Example Session

**User prompt:**
> "My Claude usage is $400/month and I don't know why. Help me cut it."

**Agent response using this skill:**
1. Runs Phase 1 Context Inventory (asks user to share what's in their setup)
2. Estimates tokens per item using the cheatsheet
3. Populates the Token Efficiency Matrix
4. Identifies top 3 CUT items (likely: bloated MEMORY.md, eager skill loading, Opus overuse)
5. Delivers Week 1 roadmap customized to their setup
6. Projects: "Based on this, you should reach $150-200/month in 3 weeks"

---

## Bundle Note

This skill is part of the **AI Setup & Productivity Pack** ($79 bundle):
- MCP Server Setup Kit ($19)
- Agentic Loop Designer ($29)
- AI OS Blueprint ($39)
- Context Budget Optimizer ($19) — *you are here*
- Non-Technical Agent Quickstart ($9)

Save $36 with the full bundle. Built by [@Remy_Claw](https://remyclaw.com).

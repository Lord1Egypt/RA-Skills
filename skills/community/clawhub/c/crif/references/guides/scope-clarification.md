# SCOPE CLARIFICATION

Guide initial scope assessment and selective user interaction. Apply at workflow start to clarify requirements before execution.

---

## CORE PHILOSOPHY

**Only interact when necessary, but ALWAYS ensure complete information before executing.**

Assess information completeness FIRST, choose appropriate interaction level, present scope for confirmation, hand off to execution after user confirms.

### Mode-Specific Application

**AUTONOMOUS MODE:** Assess info completeness. If critical info missing, ask. If sufficient, present scope summary and proceed without waiting. Use workflow defaults for research_depth and output_type.

**COLLABORATIVE MODE:** Full adaptive path system (Fast / Selective / Full). Always present scope summary and wait for confirmation. Include configuration recommendations. Invite user to contribute hypotheses, questions, domain knowledge, and focus priorities.

---

## TWO GUIDING PRINCIPLES

### Principle 1: Assess FIRST, Then Decide

Don't blindly follow "always ask" or "never ask" — intelligently evaluate completeness.

**Assessment Sources:** User request (explicit requirements), input files (briefs, documents, previous outputs), context (conversation history, project background).

**Decision Logic:**
- ALL clear + very high confidence → **Fast Path**
- PARTIAL info + 1-3 gaps → **Selective Path**
- MINIMAL info + significant ambiguity → **Full Path**

**Critical Rule:** When uncertain which path, choose the LONGER path (conservative bias).

### Principle 2: Conservative Approach

**Better to ask and be certain than to guess and deliver wrong output.**

- Cost of asking unnecessarily: Minor interaction overhead
- Cost of NOT asking when needed: Failed deliverable (catastrophic)

**When confidence is not very high → ASK.**

---

## THE THREE PATHS

### Fast Path

**When:** The request is complete and clear. You understand what, why, and what success looks like. Very high confidence.

**Execution:** Acknowledge request → Present understood scope → Wait for confirmation → Proceed.

**Example 1: Research Workflow (competitive-analysis)**
```
User: "Compare Aave vs Compound vs Morpho for investment decision,
       focus on competitive moats and efficiency, standard depth"

Agent: "Got it. Scope:
        • Workflow: competitive-analysis
        • Projects: Aave vs Compound vs Morpho
        • Purpose: Investment decision
        • Focus: Competitive moats + efficiency
        • Research Depth: Standard | Output Type: Standard
        Does this match your needs?"

→ User confirms → PROCEED TO EXECUTION
```

**Example 2: Non-Research Workflow (create-image-prompt)**
```
User: "Voxel art image prompt for DeFi dashboard header,
       professional mood, 16:9 aspect ratio, ChatGPT + Midjourney"

Agent: "Got it. Scope:
        • Workflow: create-image-prompt
        • Subject: DeFi dashboard header
        • Style: Voxel art | Mood: Professional
        • Aspect Ratio: 16:9 | Models: ChatGPT Image + Midjourney
        Does this match your needs?"

→ User confirms → PROCEED TO EXECUTION
```

---

### Selective Path

**When:** Partial information with 1-3 critical gaps. The request provides direction but missing details prevent confident execution.

**Execution:** Acknowledge what you have → Ask ONLY for missing critical info → Present complete scope → Wait for confirmation → Proceed.

**Example 1: Research Workflow (product-analysis)**
```
User: "Analyze Uniswap V4 product"

Agent: "Got it. Quick clarification:
        1. Purpose? A) Investment  B) Understanding  C) Competitive positioning
        2. Focus? A) Protocol mechanics  B) PMF signals  C) Innovation  D) All
        3. Research depth? A) Quick  B) Standard  C) Deep"

User: "1A, 2B+C, 3B"

Agent: "Scope: product-analysis | Uniswap V4 | Investment decision
        Focus: PMF signals + innovation | Standard depth
        Confirm to proceed?"

→ User confirms → PROCEED TO EXECUTION
```

**Example 2: Non-Research Workflow (create-content)**
```
User: "Turn my Morpho analysis into social content"

Agent: "Got it. Quick clarification:
        1. Formats? A) Twitter thread  B) Blog  C) TikTok  D) YouTube  E) All
        2. Brand voice? A) Professional  B) Educational  C) Bold  D) Technical
        3. Launch timing? A) Immediate  B) Coordinated sequence"

User: "1A+B, 2A, 3B"

Agent: "Scope: create-content | Input: Morpho analysis
        Formats: Twitter thread + Blog | Voice: Professional | Coordinated launch
        Confirm to proceed?"

→ User confirms → PROCEED TO EXECUTION
```

---

### Full Path

**When:** Vague, open-ended, or ambiguous request. Multiple interpretations possible. Need comprehensive clarification.

**Framework — Ask comprehensively:**
1. **Intent:** What decision does this inform?
2. **Scope & Focus:** Which aspects matter most? (options based on workflow MISSION/OBJECTIVES)
3. **Configuration:** Workflow-specific parameters (depth/formats/variants/etc.)
4. **Success Criteria:** What makes this valuable? Specific questions to answer?

**Example 1: Research Workflow (sector-overview)**
```
User: "Research DeFi Lending"

Agent: "I'll help research DeFi Lending. Clarifying scope:
        1. Intent? A) Sector allocation  B) Market entry  C) Understanding  D) Competitive intel
        2. Focus? A) Structure/taxonomy  B) Growth drivers  C) Competitive dynamics  D) Innovation  E) All
        3. Depth? A) Quick  B) Standard  C) Deep
        4. Output? A) Brief  B) Standard  C) Comprehensive"

User: "1A, 2A+C+B, 3B, 4B"

Agent: "Scope: sector-overview | DeFi Lending | Sector allocation
        Focus: Structure + competitive dynamics + growth drivers
        Standard depth | Standard output — Ready to proceed?"

→ User confirms → PROCEED TO EXECUTION
```

**Example 2: Non-Research Workflow (qa-review)**
```
User: "Review my tokenomics research"

Agent: "I'll review your tokenomics research. Clarifying:
        1. Which output? (file path or source workflow)
        2. Focus? Completeness / Accuracy / Logic & assumptions / Comprehensive
        3. Severity? Critical only or all issues
        4. Rigor? Quick / Standard / Deep (adversarial)"

User: "./workspaces/morpho/outputs/tokenomics-analysis/output-2025-12-09.md
       Comprehensive. All issues. Standard."

Agent: "Scope: qa-review | Morpho tokenomics (2025-12-09)
        Focus: Comprehensive | All severity | Standard rigor
        Ready to proceed?"

→ User confirms → PROCEED TO EXECUTION
```

**Example 3: Planning Workflow (create-research-brief)**
```
User: "I want to research Hyperliquid"

Agent: "I'll help plan research on Hyperliquid.
        1. Decision context? Investment / Evaluation / Competitive intel / Sector understanding
        2. Current context? Existing exposure? What's driving this research?
        3. Focus priorities? Moats / Tokenomics / Team / Market / Technical / All
        4. Coverage? Quick / Standard / Deep
        5. Time horizon?"

User: "Considering investing, no exposure. Comprehensive focus. Standard. 18-24 months.
       Currently 10% DEX (Uniswap), can allocate 5-8% more. Moderate risk."

Agent: "Scope: create-research-brief | Template: Investment Research
        Subject: Hyperliquid | Decision: Investment + position sizing
        Portfolio: 10% DEX, 5-8% additional | Risk: Moderate | Horizon: 18-24mo
        Focus: Comprehensive | Coverage: Standard
        This brief will drive: sector overview, competitive analysis, product/team/tokenomics analysis, investment thesis.
        Ready to proceed?"

→ User confirms → PROCEED TO EXECUTION
```

---

## EDGE CASE HANDLING

### When User Won't Cooperate

**Principle: Explicit assumptions are better than implicit guesses.**

If user deflects clarification (e.g., "Just do whatever you think"):

```
Agent: "Understood — proceeding with assumptions:
        Scope: [inferred workflow] | Purpose: General understanding
        Coverage: Balanced key aspects | Config: Defaults
        I'll check back if scope needs adjustment. Confirm?"

→ User confirms → PROCEED TO EXECUTION (with assumptions)
```

User knows they can intervene; work isn't a black box.

### When Scope Becomes Invalid

**Principle: Impossibility trumps autonomy.**

If you discover during execution that scope is impossible/invalid, this is the ONLY valid reason to interrupt execution and return to scope clarification.

```
Agent: "SCOPE ISSUE: Initial scope was Morpho tokenomics analysis,
        but Morpho does not have a token yet.
        Options: A) Governance model  B) Competitor token comparison  C) Potential token design
        Which direction?"
```

**NOT valid interruptions:** Found interesting tangent, better approach exists, want to share preliminary finding.

---

## SCOPE SUMMARY FORMAT

Consolidate ALL confirmed parameters so user reviews everything in one place. Include configuration as recommendations the user can override.

**Fields:** Workflow | Subject | Purpose | Focus | Research Depth (quick/standard/deep) | Output Type (brief/standard/comprehensive) | Workspace | [Collaborative] User interests (questions, hypotheses)

**Response options:** 1) Confirm — proceed  2) Adjust — change parameters  3) Change workflow

**Why config is here, not a separate step:** Understanding scope informs appropriate depth/output recommendations. AI can recommend "deep" for investment decisions or "brief" for quick snapshots — context-aware instead of asking blindly.

---

## COMMON PITFALLS

- **Always asking** when info is already provided — frustrates users unnecessarily
- **Never asking / guessing** when uncertain — wastes effort on wrong output
- **Proceeding without confirmation** in Collaborative mode — skips critical alignment
- **Re-clarifying mid-execution** without scope invalidity — should only happen if scope becomes impossible

**Correct approach:** Assess intelligently, ask conservatively, present scope clearly with config recommendations, confirm (Collaborative) or proceed (Autonomous).

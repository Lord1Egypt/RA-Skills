# Narrative Synthesis Guide (Step 3)

This guide is the methodology for Step 3 of the Career Spotlight Finder pipeline. Follow each section in order.

---

## 1. Purpose

The goal of narrative synthesis is to connect scattered projects into a coherent career story. Most people's work looks disjointed on the surface — a data pipeline here, a research paper there, a quick automation tool somewhere else — but underneath there are recurring themes that reveal who the person really is as a professional.

This step solves the problem: **"My work looks scattered but is actually connected by deeper themes."**

By the end of this step you will produce:

- **Theme lines** — 2-5 clusters of related projects that form coherent professional narratives.
- **Narrative arcs** — for each theme line, a story from origin to peak that shows growth.
- **A positioning statement** — one sentence capturing the user's core professional value, expert center, and distinctiveness thesis.
- **Cross-theme capabilities** — differentiators that span the user's entire career.
- **Blind spots** — gaps the user should prepare for.
- **A consolidated term mapping table** — standardized industry terminology across all projects.

The output is written to `~/.career-spotlight/report.md` using the `templates/aggregated-report.md` format.

---

## 2. Clustering (Step 3a) — Group Projects into Theme Lines

### Procedure

1. Read all files in `~/.career-spotlight/analyses/*.md`.
2. From each analysis file, extract the `## Transferable Pattern Tags` section. Collect every tag (e.g., `#data-pipeline`, `#automation`, `#model-optimization`).
3. Build a master tag list across all projects. Note which projects contributed each tag.
4. Group tags into **2-5 semantic clusters**. Each cluster becomes a **theme line**. Use semantic similarity, not exact string matching — tags like `#ETL`, `#data-pipeline`, and `#data-cleaning` belong together even though their labels differ.
5. Assign each theme line a professional label — a clear, domain-appropriate name a hiring manager would recognize.
6. List which projects belong to each theme line. A project may appear in more than one theme line if it contributed tags to multiple clusters.

### How to Cluster

- Start by listing all unique tags and their project sources.
- Look for tags that co-occur in the same projects — co-occurrence suggests they belong to the same theme.
- Look for tags that share a domain even if they never co-occur — e.g., `#REST-API` and `#GraphQL` both relate to API design.
- Aim for clusters that are distinct enough to tell different stories but broad enough to contain 2+ projects each.
- If a tag does not fit any cluster, hold it — it may become a cross-theme capability (Section 7).

### Example

```
All tags collected:
  #data-pipeline (Projects 1, 3, 7)
  #ETL (Projects 1, 7)
  #automation (Projects 3, 7, 9)
  #model-pruning (Projects 2, 5)
  #quantization (Project 5)
  #latency-optimization (Projects 2, 5, 8)
  #mentoring (Projects 4, 6)
  #technical-writing (Projects 4, 10)
  #cross-team-coordination (Projects 3, 6)

Cluster A: #data-pipeline, #ETL, #automation
  -> Projects 1, 3, 7, 9
  -> Label: "Data Engineering & Automation"

Cluster B: #model-pruning, #quantization, #latency-optimization
  -> Projects 2, 5, 8
  -> Label: "Model Efficiency Optimization"

Cluster C: #mentoring, #technical-writing, #cross-team-coordination
  -> Projects 4, 6, 10 (and partially 3)
  -> Label: "Technical Leadership & Communication"
```

### Edge Cases

- **Only 1-2 projects analyzed:** Create 1-2 theme lines. Note that additional projects would strengthen the narrative and suggest the user add more (they can return to Step 1).
- **All projects cluster into one theme:** That is fine — the user may be deeply specialized. Create one strong main line and look for a supporting line from secondary tags (e.g., soft skills, tooling choices).
- **More than 5 clusters emerge:** Merge the most similar clusters until you have at most 5. Prioritize clusters with the most projects or the strongest relevance to the target domain.

---

## 3. Thread Discovery (Step 3a½) — Find the Connective Logic Across Clusters

**This step is the most important in the entire synthesis.** Users come to this skill because they cannot see the story connecting their work. Tag-based clustering (Section 2) groups projects by surface-level similarity, but the deepest career insights come from discovering what connects projects that appear to belong to *different* clusters.

Your job here is to be a thoughtful career advisor who reads between the lines — to make the inferential leaps the user cannot make for themselves, grounded in their actual work.

### Why This Step Exists

Consider this real example: A user provides 4 research papers. Two are about RL algorithms for robotics, two are about distributed systems for RL training. Tag-based clustering puts them in separate clusters ("RL algorithms" vs. "distributed systems"). But the real story is:

> "I am an RL researcher. I started with RL algorithms, and through that work I discovered that systems-level bottlenecks were limiting RL at scale. So I shifted to building RL systems infrastructure. My career is a unified journey through reinforcement learning — from algorithms to systems."

Without this step, the skill would present two disconnected theme lines and miss the most powerful narrative entirely.

### Procedure

**3a½.1 — Scan for shared domain across clusters**

After forming tag clusters (Section 2), re-read the `## Problem & Motivation` and `## Research Trajectory` sections (if present) of ALL analyses. Ask:

- Do projects in different clusters share a **common domain or problem space**? Look beyond tags — "distributed systems for RL training" and "RL algorithm design" are both fundamentally about reinforcement learning, even though their tags are completely different.
- Is there a single phrase that could umbrella multiple clusters? (e.g., "reinforcement learning," "data infrastructure," "developer tools")
- Do multiple projects reference the same prior work, the same research community, or the same application domain?

**3a½.2 — Scan for causal/motivational connections between clusters**

For each pair of clusters, ask:

- Did working in Cluster A **reveal a limitation or bottleneck** that motivated work in Cluster B? Look at `## Research Trajectory` → "what prior limitation motivated this work" entries. If Cluster B's motivation references problems inherent to Cluster A's domain, that is a causal link.
- Is there a **temporal progression** where the user moved from one cluster's domain to another's? (Earlier projects in A, later projects in B)
- Did skills, frameworks, or insights developed in Cluster A **directly enable** the approach taken in Cluster B? (e.g., deep understanding of RL training dynamics from algorithm work enables designing better RL infrastructure)

**3a½.3 — Construct the overarching thread (if one exists)**

If you find a shared domain or causal connection:

1. Name the **overarching thread** — the unifying domain or journey (e.g., "Reinforcement Learning: from algorithms to systems").
2. Articulate the **transition logic** — why the user moved from one sub-area to another. This should be a 1-2 sentence narrative of the form: "[User] focused on [area A], which led them to discover [insight/limitation], motivating a shift to [area B]."
3. Record whether each cluster is a **chapter** within this thread, or truly independent of it. Not every cluster must belong to the thread — some projects (e.g., side projects, unrelated work) may remain separate theme lines.

**Important:** Be willing to make reasonable inferences, but stay grounded. If the user has 2 RL algorithm papers and 2 RL systems papers, it is reasonable to infer the connection even if no paper explicitly says "I switched from algorithms to systems because..." The papers' content makes the link clear. However, do NOT fabricate connections that require leaps unsupported by the material.

### What Changes When a Thread Is Found

When an overarching thread is discovered:

- The thread becomes the **primary framing** of the report. Instead of presenting disconnected theme lines, the report tells one story with chapters.
- Tag clusters become **sub-themes within the thread** rather than independent theme lines. Their narrative arcs connect to each other via the transition logic.
- The positioning statement should reference the thread, not just one theme line.
- Projects outside the thread (if any) become a separate supplementary theme line.

### When No Thread Is Found

If projects genuinely have no connective logic (e.g., a data science project and an unrelated mobile app), that is fine. Proceed directly to Section 4 (Ranking) and use the standard parallel or progressive narrative. Not every user has a unified thread — and forcing one would be dishonest.

### Example

```
Clusters from Section 2:
  Cluster A: "RL Algorithm Research" — Papers 1, 2 (UAV navigation, HITL DRL)
  Cluster B: "ML Systems Infrastructure" — Papers 3, 4 (MAAS-RL, JANUS)
  Cluster C: "AI Application Engineering" — Projects 5, 6 (Cambly, Podcast Inbox)

Thread Discovery:
  1. Shared domain scan:
     - Clusters A and B both involve reinforcement learning.
       Paper 1: RL algorithm for UAV navigation
       Paper 2: Human-in-the-loop RL training
       Paper 3: RL post-training infrastructure for LLMs
       Paper 4: RL buffer data management
     - All 4 papers are fundamentally about RL.

  2. Causal connection scan:
     - Papers 1-2 (algorithm work) → deep understanding of RL training dynamics
       (replay buffers, actor-critic, reward shaping)
     - Papers 3-4 (systems work) → optimize the infrastructure that runs RL at scale
     - Paper 3 motivation references "inherent dynamism of RL post-training" —
       this is the exact kind of training dynamics learned in Papers 1-2
     - Paper 4 motivation references "buffer-side data handling" — replay buffers
       are a core concept from the algorithm papers
     - Causal link: algorithm experience → discovered systems bottlenecks → systems work

  3. Overarching thread:
     Name: "Reinforcement Learning: from algorithms to systems"
     Transition: "Started with RL algorithms for autonomous systems,
       gained deep understanding of RL training dynamics (replay buffers,
       actor-critic, reward shaping). This domain expertise revealed that
       systems-level bottlenecks were the real barrier to RL at scale,
       motivating a shift to building high-performance RL infrastructure."
     Cluster A: Chapter 1 (RL Algorithms — the origin)
     Cluster B: Chapter 2 (RL Systems — the evolution)
     Cluster C: Independent supplementary line (AI Applications)
```

---

## 4. Ranking (Step 3b) — Prioritize Theme Lines (or Thread Chapters) for the Target Domain

### Procedure

**If an overarching thread was found in Section 3:** The thread's sub-themes (chapters) replace independent theme lines. Rank the chapters by which is most relevant to the target domain — the most relevant chapter becomes the "main chapter" and gets the most report weight. The thread itself is the overarching frame.

**If no thread was found:** Rank independent theme lines by relevance as below.

Given the confirmed framing from Step 2, rank the theme lines (or chapters) by relevance:

| Rank | Role | Report Weight | Criteria |
|------|------|---------------|----------|
| **Main line** | Core value proposition | ~50% | Most directly relevant to the confirmed framing. This is the headline center of gravity of the user's story. |
| **Supporting line** | Differentiation | ~30% | Relevant but distinct from the main line. It should sharpen why the user is special, not merely sit off to the side. |
| **Supplementary line** | Depth / soft skills | ~20% | Cross-cutting capabilities, soft skills, or adjacent expertise. Adds dimension without diluting the main expert frame. |

**Respecting user-designated project priorities:**

Theme lines that contain more `user_priority: highlight` projects should be weighted more heavily when domain relevance is otherwise comparable. The user's priority designation reflects their own judgment about which work best represents them — do not override this with recency or technical impressiveness alone.

- A theme line anchored by highlight projects is a stronger candidate for main/supporting line than one anchored only by supporting projects, all else being equal.
- Within a theme line, highlight projects should feature more prominently in the narrative arc (see Section 5).

If there are more than 3 theme lines, the extras become supplementary (share the 20% weight) or are folded into the cross-theme capabilities section.

If there are only 2 theme lines, assign one as main and one as supporting. Omit supplementary.

If there is only 1 theme line, it is the main line. Look for sub-themes within it to create a supporting angle.

At the end of ranking, the report should converge on **one** credible expert-facing story. That story may be a narrow specialist framing or a bridge framing. Do not present the user as three equally weighted identities, but also do not force them into a narrower box than the evidence supports.

### Narrative Structure Decision

After ranking, determine which narrative structure best fits the user's work. There are three options — choose the one that most honestly represents the data:

**Option 1: Unified thread narrative** (preferred when Section 3 found an overarching thread)

The report opens with the thread as the primary frame. Theme lines become chapters within that thread, connected by transition logic. The positioning statement references the thread.

> "My career is a journey through [thread]. I started with [Chapter A: origin], which gave me [key insight]. That insight revealed [limitation/opportunity], leading me to [Chapter B: evolution], where I now [current focus]. Along the way, I also [supplementary line]."

Example: "My career is a journey through reinforcement learning. I started by designing RL algorithms for autonomous navigation, gaining deep expertise in training dynamics — replay buffers, reward shaping, actor-critic architectures. That domain knowledge revealed that systems-level bottlenecks were the real barrier to RL at scale, leading me to build high-performance distributed infrastructure for RL training, culminating in publications at VLDB."

**Option 2: Progressive narrative** (when no unified thread, but there is temporal/logical progression)

- **Temporal progression:** The user moved from Theme A early in their career to Theme B later, then Theme C most recently.
- **Logical progression:** Theme A is foundational knowledge that enabled Theme B, which enabled Theme C.

> "I started by building X, which gave me deep expertise in Y. That led me to Z, where I now focus on [main line]."

**Option 3: Parallel narrative** (when themes are genuinely independent)

> "My work spans three complementary areas: [main], [supporting], and [supplementary]. Together they make me uniquely effective at [positioning statement]."

Record which narrative structure you are using — it will shape the report and copywriting.

Regardless of structure, the final report should still read as a single expert story with supporting differentiators. The user may have multiple adjacent strengths; the report should make clear what they should be remembered for first **and** why their combination is distinctive.

---

## 5. Narrative Arcs (Step 3c) — Build the Story for Each Theme Line (or Thread Chapter)

For each theme line (or thread chapter), construct a four-part narrative arc using the projects assigned to that theme.

**If using a unified thread narrative:** Build arcs for each chapter, then also construct a **thread-level arc** that spans across chapters. The thread-level arc tells the transition story — why the user moved from one chapter to another. Each chapter's arc is nested within this larger story. The thread-level arc should articulate the causal connection: "[earlier chapter insight] → [limitation discovered] → [later chapter motivation]."

### 5.1 Origin

Identify the **earliest project** in this theme line. Answer:

- What foundational skill or insight was established here?
- What was the user's starting point in this domain?

Example: "In Project 1 (a university data scraper), the user first encountered the challenge of transforming unstructured web data into clean, structured datasets."

### 5.2 Growth

Identify **subsequent projects** that show the user deepening capability or expanding scope. Answer:

- How did the complexity increase from the origin?
- Did the user move from individual contribution to team-level or system-level work?
- Did the scale grow (more data, more users, higher stakes)?

Example: "Projects 3 and 7 show progression from single-source scrapers to multi-source ETL pipelines handling production data at scale, introducing monitoring and fault tolerance."

### 5.3 Peak

Identify the **most impressive project** in this theme line. This is determined by:

- User-designated `highlight` projects are strong candidates for peak — the user explicitly marked them as important
- Hardest technical challenge solved
- Largest scale (data volume, user count, team size)
- Most notable result (quantified impact, recognition, business outcome)
- Do NOT default to "most recent = peak." Recency is not a proxy for importance. The user's priority designation is a stronger signal than chronology.

Example: "Project 7 (real-time data pipeline processing 10TB/day) represents the peak — it combined the data transformation skills from earlier projects with real-time streaming, cross-team coordination, and a measurable 60% reduction in query latency."

### 5.4 Positioning

Write **one sentence** that captures what this theme line says about who the user is as a professional.

Guidelines:
- Start with a professional identity, not a task description.
- Reference the arc from origin to peak.
- Use target-domain terminology.
- When multiple labels are possible, prefer the one that is slightly more senior, specific, or market-legible **as long as it remains clearly defensible from the underlying projects**.

Example: "A data engineer who has progressed from ad-hoc data collection to designing production-grade, real-time data infrastructure at scale."

### Handling Thin Arcs

If a theme line has only 1-2 projects, the arc will be compressed:

- 1 project: Origin and Peak are the same. Growth is implied by the complexity within the single project. State this honestly — do not fabricate progression.
- 2 projects: Origin is the earlier one, Peak is the later/more impressive one. Growth is the delta between them.

---

## 6. Term Refinement (Step 3d) — Standardize Industry Terminology

Now that you have the full picture across all projects and the domain reference file is loaded (from Step 2), revisit and consolidate terminology.

### Procedure

1. Collect all `## Methods & Technology` and `## Hidden Capabilities` entries from every analysis file. Each entry has the form `[what user did] -> [industry term]`.
2. If a domain reference file (`references/industry-terms-[domain].md`) was loaded, cross-check all mapped terms against it.
3. Identify and fix:
   - **Inconsistencies:** The same capability mapped to different terms across projects. Pick the best term and standardize.
   - **Missed translations:** Colloquial descriptions that were not mapped to an industry term during individual analysis. Map them now with the full domain context.
   - **Over-generic terms:** Terms like "programming" or "data analysis" that could be more specific (e.g., "distributed systems programming", "exploratory data analysis").
   - **Under-translations:** Cases where the user did something impressive but the term does not convey the full weight (e.g., "wrote a script" when the industry term should be "automated CI/CD pipeline").
4. Build a **consolidated term mapping table** for the report:

```
| What you did                        | What the industry calls it         | Source project    |
|-------------------------------------|------------------------------------|-------------------|
| Wrote cron jobs to move data        | ETL pipeline orchestration         | Project 1, 7      |
| Made the model smaller and faster   | Model compression / quantization   | Project 5         |
| Helped new team members get started | Technical onboarding & mentorship  | Project 4, 6      |
```

### Guidelines

- Prefer terms that the target domain actually uses. A term that is technically correct but unused in the target industry is not helpful.
- When in doubt, err toward terms that are slightly more impressive but still defensible — the user will review everything in Step 5.
- Deduplicate: if three projects each list "Python scripting," consolidate into one row that references all three projects rather than three separate rows.

---

## 7. Cross-Theme Capabilities

After building the theme lines, look for capabilities that appear in **2 or more theme lines**. These are not confined to one narrative — they are woven throughout the user's career.

### How to Identify

- Review the `## Hidden Capabilities` sections across all analyses.
- Look for capabilities that transcend a single theme. Common examples:
  - **Systems thinking** — the user designs end-to-end systems, not just components, across multiple projects.
  - **From-zero-to-one delivery** — the user repeatedly builds things from scratch rather than maintaining existing systems.
  - **Debugging under uncertainty** — the user consistently solves problems without clear specifications.
  - **Cross-functional communication** — the user works across team boundaries in multiple contexts.
  - **Performance mindset** — the user optimizes for speed, cost, or efficiency regardless of the domain.

### Why These Matter

Cross-theme capabilities are powerful differentiators because they are hard to teach and hard to screen for in interviews. They signal adaptability and depth. Highlight them prominently in the report.

### Format

List each cross-theme capability with:
- A clear label
- Evidence from at least 2 projects (cite specific projects)
- One sentence explaining why this capability is valuable in the target domain

Example:
```
**Systems Thinking**
Evidenced in: Project 3 (end-to-end ETL pipeline), Project 5 (full model training-to-deployment optimization), Project 6 (org-wide documentation system)
Value: In [target domain], this translates to the ability to own entire feature lifecycles rather than just individual tasks.
```

---

## 8. Optional: Positioning Risks (Only if the User Asks)

This skill does **not** surface gap analysis by default. The default output should stay focused on the user's strengths, distinctiveness, and strongest story.

Only generate this section if the user explicitly asks questions such as:

- "What am I missing for this direction?"
- "What are the risks in this positioning?"
- "What gaps should I close next?"

If the user explicitly asks for that analysis, identify the top **3-5 capabilities** that are commonly expected but **not evidenced** in any of the analyzed projects.

### How to Identify

1. Consider what the target domain typically requires at the user's seniority level. Seniority is inferred from the complexity, scope, and leadership signals in the analyzed projects.
2. Compare those expectations against the full set of capabilities evidenced across all analyses.
3. The gap = optional positioning risks.

### What to Include for Each Positioning Risk

For each identified blind spot, provide:

1. **Capability name** — the specific skill or experience area.
2. **Why it matters** — a concrete explanation of why this capability is expected in the target domain at the inferred seniority. Not generic; tied to the specific domain.
3. **Possible explanations** — the user may actually have this capability but it was not evidenced in the analyzed projects. Acknowledge this possibility.

### Example

```
1. **Production Monitoring & Observability**
   Why it matters: [Target domain] roles at the senior level are expected to own
   service reliability. Monitoring, alerting, and incident response are table stakes.
   Note: This may exist in your experience but was not evidenced in the analyzed
   projects. Consider adding projects that demonstrate this capability.

2. **Stakeholder Communication / Business Translation**
   Why it matters: At the senior level in [target domain], translating technical
   decisions into business impact for non-technical stakeholders is critical for
   project approval and resource allocation.
   Note: Your projects show strong technical depth but limited evidence of
   business-facing communication.
```

### Guidelines

- Be honest but not discouraging. Frame these as positioning risks or missing signals, not as personal deficiencies.
- Always include the note that the gap may be due to project selection, not actual missing capability.
- Limit to 3-5. More than 5 becomes overwhelming and unhelpful.

---

## 9. Output — Write the Report

### Pre-Write Check

Before writing, check if `~/.career-spotlight/report.md` already exists.

- **If it exists:** Archive it to `~/.career-spotlight/history/report-YYYY-MM-DDTHH-MM-SS.md` using the current timestamp. Then proceed to write the new report.
- **If it does not exist:** Proceed directly.

### Write the Report

Write `~/.career-spotlight/report.md` using `templates/aggregated-report.md` as the base structure. The report must contain:

1. **Meta section** — date, target domain, project count, theme line count.
2. **One-Sentence Positioning** — synthesized from the theme line positioning statements. This is the single most important sentence in the entire report. It should:
   - Name the user's expert center or bridge framing (not just a vague job family).
   - Reference the main theme line (or the overarching thread, if one was discovered).
   - Include a differentiator from the supporting theme line.
   - Make clear why the user is more memorable than a more conventional candidate in the same area.
   - Be specific enough that it could not describe just anyone in the field.
   - Read like one coherent expert story, not like three competing labels jammed together.
3. **Term Mapping Table** — the consolidated table from Step 3d.
4. **Theme Lines / Thread Chapters** — structure depends on the narrative decision from Section 4:

   Theme-line and chapter names should be **orthogonal and high-signal**:

   - Each heading should describe a clearly different selling point, not a vague variation of the same lane.
   - Avoid overlapping labels such as "Reinforcement Learning Systems" and "Reinforcement Learning Research" when a more precise pair exists.
   - Prefer market-recognized, more specific headings such as:
     - `Distributed RL Systems and Post-Training Infrastructure`
     - `Applied Reinforcement Learning Algorithms for Autonomous Systems`
     - `AI-native Product Engineering`
   - If two headings still feel interchangeable after you write them, they are not separated enough yet.
   - When multiple defensible labels exist, prefer the one with higher signal and clearer hiring-market meaning.

   **If unified thread narrative (Option 1),** replace the template's independent theme line sections with this structure:

   ```
   ## Overarching Thread: [Thread Name]
   [1-2 sentences: the single story connecting the user's work]

   ### Chapter 1: [Name] (Origin Phase)
   #### Narrative Arc
   - **Origin:** [earliest project] — [what it established]
   - **Growth:** [subsequent projects] — [how capability deepened]
   - **Peak:** [strongest project] — [most impressive demonstration]
   - **Positioning:** [what this chapter says about who you are]
   - **Transition:** [insight or limitation from this chapter] → [next chapter]
   #### Key Projects
   - [Project] ★: [one-line highlight]
   - [Project]: [one-line highlight]

   ### Chapter 2: [Name] (Evolution Phase)
   [Same structure; final chapter omits Transition]

   ## Supplementary: [Name]
   [For projects outside the thread, if any — use standard theme line structure]
   ```

   **If progressive or parallel narrative (Options 2-3),** use the template structure as-is — independent theme lines ranked main / supporting / supplementary.

5. **Cross-Theme Capabilities** — from Section 7.
6. **Optional positioning risks** — only include if the user explicitly asked for gap analysis in Section 8.

### Quality Checklist

Before finalizing the report, verify:

- [ ] Every analyzed project appears in at least one theme line.
- [ ] The positioning statement is specific and defensible (every claim is backed by a project).
- [ ] The opening sections explain not only what bucket the user fits into, but why they are distinctive within it.
- [ ] Term mappings are consistent — the same capability is not called different things in different theme lines.
- [ ] Theme-line or chapter headings are high-signal, market-legible, and clearly distinct from one another.
- [ ] Narrative arcs show genuine progression, not invented progression. If growth is limited, say so honestly.
- [ ] The report uses target-domain terminology throughout, not the user's original colloquial descriptions.
- [ ] If an overarching thread was discovered (Step 3a½), the report uses the unified thread narrative — theme lines are presented as connected chapters, not independent clusters.
- [ ] Thread transitions are grounded in evidence from project analyses (Problem & Motivation, Research Trajectory), not fabricated.
- [ ] If a bridge framing is being used, the secondary strength that makes the user distinctive is visible in the positioning statement and opening sections, not buried at the end.

---

## Summary of Sub-Steps

| Sub-Step | Action | Output |
|----------|--------|--------|
| 3a | Cluster tags into theme lines | 2-5 named theme lines with project assignments |
| 3a½ | Discover shared threads across clusters | Overarching thread with causal connections (if found) |
| 3b | Rank theme lines by target-domain relevance | Main / Supporting / Supplementary ranking + narrative structure |
| 3c | Build narrative arcs | Origin -> Growth -> Peak -> Positioning for each theme line (or thread chapter) |
| 3d | Refine and consolidate terminology | Consolidated term mapping table |
| 3e | Identify cross-theme capabilities | List of career-spanning differentiators |
| 3f | Optional positioning risks | Only if user asks for gap analysis |
| 3g | Write report | `~/.career-spotlight/report.md` |

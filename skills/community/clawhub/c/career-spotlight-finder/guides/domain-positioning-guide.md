# Domain Positioning Guide

This guide defines the methodology for Step 2 of the Career Spotlight Finder pipeline. Follow these instructions when SKILL.md directs you to "read `guides/domain-positioning-guide.md` and follow its methodology."

---

## 1. Purpose

Domain positioning answers the question: **"What kind of role should these projects point toward?"**

There are two scenarios:

- **No explicit user preference stated yet**: Infer 2-3 possible career positioning directions from the project analyses, then recommend the strongest expert-facing lead. This lead may be a conventional specialist framing or a bridge framing that combines adjacent strengths into one believable center of gravity.
- **User expresses a preferred target direction during the workflow**: Treat that preference as an override of the recommended lead framing, then load any matching reference files (per Section 4) and proceed to Step 3.

In either case, the end result of this step is a confirmed **expert framing** and (optionally) loaded industry-terms reference files to inform Steps 3 and 4.

---

## 2. Inference Process

Use this process to derive positioning directions from the evidence already captured in the project analyses. If the user later asks to optimize for a specific direction, that preference can override the recommendation.

### 2.1 Collect all evidence

1. Glob `~/.career-spotlight/analyses/*.md` and read every file.
2. From each analysis, extract two categories of evidence:
   - **Term mappings** -- every `-> **[industry term]**` entry found in the "Methods & Technology" and "Hidden Capabilities" sections.
   - **Transferable pattern tags** -- the `#tag` entries in the "Transferable Pattern Tags" section.
3. Build a combined list of all term mappings and tags across every project. Keep track of which project each item came from.

Example extraction from a single analysis:

```
Project: data-cruncher
  Term mappings:
    - "batch ETL pipeline"         (Methods & Technology)
    - "schema evolution"           (Methods & Technology)
    - "data quality monitoring"    (Hidden Capabilities)
  Tags:
    #pipeline-design  #automation  #data-quality
```

### 2.2 Identify clusters

4. Group the collected terms and tags by semantic similarity. Look for these signals:
   - **Frequency**: Which industry terms and tags appear in two or more projects?
   - **Co-occurrence**: Which terms tend to appear together in the same project?
   - **Thematic overlap**: Which projects share common problem domains or solution patterns?

5. Name each cluster by the professional domain it maps to. Use the following heuristics as a starting point (not an exhaustive list):

   | Dominant evidence pattern | Likely domain |
   |--------------------------|---------------|
   | Data pipeline terms, ETL, schema, orchestration, warehouse | Data Engineering |
   | Metrics layers, BI dashboards, warehouse modeling, dbt-style transforms | Analytics Engineering / Data Analytics |
	   | Model training, evaluation, feature engineering, representation learning, experimentation | Machine Learning / AI |
	   | Inference optimization, serving, model compression, latency, training infrastructure | ML Systems / AI Infrastructure |
	   | LLM applications, tool calling, multi-step agents, prompt design, evals, guardrails, observability | AI-native Engineering / Agent Workflow Design |
	   | UI components, state management, accessibility, responsive design | Frontend Engineering |
	   | Wireframes, prototyping, design systems, usability research | Product Design / UX / UI |
	   | API design, system architecture, database, microservices | Backend / Full-stack Engineering |
   | User research, metrics, A/B testing, roadmap, prioritization | Product Management |
   | CI/CD, infrastructure as code, monitoring, SRE | DevOps / Platform Engineering |
   | Technical writing, documentation systems, developer experience | Developer Relations / DevEx |
   | Threat modeling, access control, vulnerability scanning, incident response | Security Engineering / AppSec |
   | Papers, peer review, rebuttals, reproducibility, venue fit, camera-ready workflows | Academic / Scholarly Research |
   | Distributed systems, storage, scheduling, cloud runtimes, fault tolerance | Systems / Distributed Systems |
   | Query optimization, transactions, provenance, stream processing, indexing | Data Management / Database Systems |
   | Routing, congestion control, traffic engineering, network measurement | Networking / Networked Systems |

	   If the evidence does not cleanly map to any single domain, consider hybrid labels (e.g., "Full-stack Engineer with data focus" or "ML Engineer with strong backend skills").

	   When AI-assisted coding or agent workflows appear in the evidence, use stable professional language such as **"AI-native engineering," "agent workflow design," "tool-using systems,"** or **"AI product engineering."** Do not use meme-like labels such as "vibe coding" as the primary positioning label.

	   Do not inflate weak evidence. Simply using an AI coding tool does **not** justify an AI-native or agentic positioning direction by itself. Look for concrete signals such as prompt/workflow design, tool integration, multi-step orchestration, evals, guardrails, human approval loops, observability, or reliability/cost tradeoff work.

### 2.3 Formulate positioning directions

6. Select the top 2-3 clusters (ranked by how many projects and distinct pieces of evidence support them). For each, formulate a **positioning direction** with three components:

	   - **Label**: A concise role-oriented title that captures the direction. Be specific rather than generic. For example, prefer "ML Engineer focused on training efficiency" over just "ML Engineer."
	   - **Supporting projects**: List the project names whose evidence feeds into this direction.
	   - **Reasoning**: 1-2 sentences explaining why this direction makes sense given the evidence. Reference specific term mappings or tags.

7. From those 2-3 directions, choose a **recommended expert framing**. This is the framing that should lead the report unless the user explicitly overrides it. Choose it using these criteria:

   - **Evidence density**: most recurring terms/tags across the project set
   - **Project quality**: strongest concentration of `user_priority: highlight` projects
   - **Narrative fit**: best match for the actual connective logic across the user's work
   - **Market clarity**: easiest framing for a hiring manager or recruiter to recognize quickly, without flattening the truth

Before using market considerations, apply this rule:

   - **Evidence floor first**: Do not move the user into a hotter or more valuable market lane unless the underlying projects genuinely support that framing.
   - **Market upside as tie-breaker**: If two framings are both truthful and defensible, prefer the one with higher market value, stronger recruiter recognition, or broader opportunity density.
   - **Do not erase the credibility base**: If the recommended framing leans toward a more marketable adjacent lane, preserve the earlier or deeper line of work as the user's credibility base rather than pretending they came from somewhere else.

8. Determine whether the recommendation should be a **specialist framing** or a **bridge framing**:

   - **Use a specialist framing** when one direction clearly dominates and the others are mostly supporting add-ons.
   - **Use a bridge framing** when the user's distinctiveness comes from the combination itself rather than from one narrow lane.

Use a **bridge framing** when most of the following are true:

   - The top 2 directions are close in evidence strength
   - The same highlight projects support more than one direction
   - There is a clear causal progression or connective logic between directions
   - Narrowing to one job-title label would make the user sound less true or less memorable

Bridge framings should still be market-legible. Good examples:

   - "Applied AI / ML Systems Builder"
   - "AI Systems Generalist with RL depth"
   - "ML Systems Engineer with product execution strength"

Bad examples:

   - "Multidisciplinary technologist"
   - "Someone who does a bit of everything"
   - Any framing that sounds broad but does not help a recruiter understand what the user is strong at

9. Write a **Distinctiveness Thesis** for the recommendation. This is a one-sentence explanation of why the user is more interesting than a more conventional candidate in the same general area. It should answer: **"Why this person, not just why this bucket?"**

Example output (internal, before presenting to user):

```
Recommended framing:
  Label: "Applied AI / ML Systems Builder"
  Mode: Bridge framing
  Why this leads: The strongest projects split across reinforcement learning,
  distributed training systems, and AI workflow products. The real advantage is
  not a single narrow lane, but the ability to connect model behavior, systems
  bottlenecks, and usable product flows into one story.
  Distinctiveness thesis: "Combines reinforcement learning depth, systems
  bottleneck intuition, and product execution."

Direction 1:
  Label: "ML Systems Engineer focused on training infrastructure"
  Supporting projects: janus, maas-rl
  Reasoning: The strongest systems work focuses on distributed reinforcement
  learning, runtime orchestration, and performance bottlenecks in training.

Direction 2:
  Label: "Applied Reinforcement Learning Researcher-Engineer"
  Supporting projects: uav-paper-1, uav-paper-2
  Reasoning: The earlier work shows real depth in reinforcement learning
  dynamics, reward design, replay buffers, and long-horizon control.

Direction 3:
  Label: "AI-native Product Engineer"
  Supporting projects: podcast-inbox, cambly-review
  Reasoning: The product work shows an ability to turn complex AI workflows
  into usable systems with guardrails, scheduling, and multi-surface delivery.
```

---

## 3. Presenting to User

Present the inferred directions to the user as a **recommendation**, not as a forced identity test. Lead with the strongest expert-facing framing, then show why it is the right center of gravity and what makes the user distinctive. Keep it concise -- the user should understand the recommendation in one pass.

Use this format:

```
Based on your project analyses, I recommend centering your story on:

**Expert Center: [Label]**
[1-2 sentence reasoning explaining why this is the strongest lead story]

**What makes you different**
[1 sentence distinctiveness thesis]

**Alternative Wrappers**
- **[Label]** — [best when targeting what kind of opportunity]
- **[Label]** — [best when targeting what kind of opportunity]

This is the lead framing I recommend based on the evidence.
Does this work as the main direction, or would you like me to use one of the alternative wrappers instead?
```

Rules for this interaction:

- Lead with a recommendation. The user came for synthesis, not to be handed the classification problem again.
- If the user says multiple directions fit, or says they are unsure, **do not** bounce the choice back to them. Treat that as a signal to prefer a bridge framing unless the evidence clearly says otherwise.
- Even when the recommendation is strong, ask for confirmation before proceeding to Step 3. The interaction should be "here is my recommended lead and why" followed by a short confirmation question, not silent auto-selection.
- If the user wants a different lead angle, switch to that framing and record it as the confirmed framing.
- If the user asks for clarification about a direction, explain which evidence supports it, what kinds of roles it maps to, and whether it works better as the expert center or as an alternative wrapper.
- Never frame the user as "not really an expert," "not a pure specialist," or "better off not positioning as an expert." The job is to find the most credible expert entry point and explain why this person is special within it.
- Do not over-optimize for a narrow, conventional job-title label when it makes the user less truthful or less memorable.
- Once the framing is confirmed explicitly by the user (either by accepting the recommendation or asking for an override), record it as the confirmed framing for the rest of the pipeline.

---

## 4. Loading References

After the framing is confirmed (whether recommended or user-overridden), attempt to load matching industry-terms reference files.

### 4.1 Find matching reference files

1. Glob the current skill directory's `references/industry-terms-*.md` files to list all available reference files. Resolve the path relative to this skill's installation directory at runtime.
2. The bundled reference files currently include:
   - `industry-terms-ml.md` -- Machine Learning / AI
   - `industry-terms-ai-infra.md` -- AI Infrastructure, ML Platform, Training/Serving Infrastructure
   - `industry-terms-swe.md` -- Software Engineering, Backend, Frontend, Full-stack
   - `industry-terms-systems.md` -- Systems / Distributed Systems
   - `industry-terms-data.md` -- Data Engineering, Analytics Engineering, BI, Data Analytics
   - `industry-terms-data-management.md` -- Data Management, Database Systems, Query Engines
   - `industry-terms-networking.md` -- Networking, Networked Systems
   - `industry-terms-pm.md` -- Product Management, Program Management
   - `industry-terms-design.md` -- Product Design, UX, UI, Service Design
   - `industry-terms-devrel.md` -- Developer Relations, Developer Advocacy, Technical Writing, DevEx
   - `industry-terms-security.md` -- Security Engineering, AppSec, IAM, SecOps
   - `industry-terms-academic.md` -- Cross-domain academic writing, peer review, reproducibility
3. Match the confirmed framing to the most relevant bundled file:
	   - If the domain is ML-related (ML Engineer, AI Engineer, Applied AI, Modeling, etc.) -> load `industry-terms-ml.md`
	   - If the domain is AI-infrastructure-related (AI Infra, ML Platform, LLM Platform, Model Serving, Training Infra, MLSys, GPU Cluster, etc.) -> load `industry-terms-ai-infra.md`
	   - If the domain is AI-native application engineering, agent workflow design, AI product engineering, or tool-using systems -> load `industry-terms-ml.md` and `industry-terms-swe.md`; also load `industry-terms-ai-infra.md` when serving, evals, guardrails, observability, or platform/infrastructure concerns are central
	   - If the domain is data-related (Data Engineer, Analytics Engineer, BI Engineer, Data Analyst, etc.) -> load `industry-terms-data.md`
	   - If the domain is data-management-related (Database Systems, Data Management, Query Engine, Storage Engine, Data Systems, etc.) -> load `industry-terms-data-management.md`
	   - If the domain is engineering-related (Backend, Frontend, Full-stack, DevOps, Platform, SRE, etc.) -> load `industry-terms-swe.md`
   - If the domain is systems-related (Distributed Systems, Storage Systems, Cloud Systems, Operating Systems, Runtime Systems, etc.) -> load `industry-terms-systems.md`
   - If the domain is networking-related (Networking, Networked Systems, Traffic Engineering, Transport, SIGCOMM-style work, etc.) -> load `industry-terms-networking.md`
   - If the domain is product/program-related (Product Manager, Growth PM, TPM, etc.) -> load `industry-terms-pm.md`
   - If the domain is design-related (Product Designer, UX Designer, UI Designer, UX Researcher, etc.) -> load `industry-terms-design.md`
   - If the domain is developer-relations-related (Developer Advocate, DevRel, Developer Educator, Technical Writer, DevEx, etc.) -> load `industry-terms-devrel.md`
   - If the domain is security-related (Security Engineer, AppSec, IAM, SecOps, Security Analyst, etc.) -> load `industry-terms-security.md`
   - If the work is explicitly academic, publication-oriented, or paper-centric (Research Scientist, PhD, paper submission, rebuttal, benchmark paper, etc.) -> also load `industry-terms-academic.md`
   - If the domain is "Data Scientist" or another hybrid that spans modeling and analytics, load both `industry-terms-ml.md` and `industry-terms-data.md`
   - If the domain is a hybrid direction such as "ML systems" or "applied database systems," load all relevant domain files rather than splitting by research vs engineering
   - If the domain spans product, design, and engineering (for example, frontend product roles), load all relevant files
	   - If the domain spans multiple areas, load all relevant files.
	   - If the framing is a bridge framing, load the lead domain file plus the files needed to support the distinctiveness thesis.
	   - If an alternative wrapper materially shapes the narrative or copy, load its reference file too. Do not load extra files that are only weakly related.
4. If a matching file exists, read it. Its contents will be used in Steps 3 and 4 to ensure the narrative and copy use accurate, current industry terminology.
5. If no matching file exists (e.g., the domain is niche or the reference files have not been created yet), proceed using general domain knowledge. Note this to the user: "No specific industry-terms reference file found for [domain]. I'll use general [domain] terminology."

### 4.2 Check for user-added reference files

1. After loading bundled references, check if any additional `industry-terms-*.md` files exist that do NOT match the bundled names (`ml`, `ai-infra`, `swe`, `systems`, `data`, `data-management`, `networking`, `pm`, `design`, `devrel`, `security`, `academic`).
2. If user-added reference files are found, list them for the user:
   ```
   I also found these custom reference files:
   - industry-terms-sales.md
   - industry-terms-customer-success.md

   Would you like me to include any of these as well?
   ```
3. If the user says yes (to one or more), read those files and include their terminology alongside the bundled references.
4. If no user-added files are found, skip this sub-step silently.

### 4.3 What to do with loaded references

- Do not present the raw reference content to the user.
- Hold the loaded terminology in context for use during Step 3 (Narrative Synthesis) and Step 4 (Copywriting).
- The reference content helps ensure that the term mapping table, theme lines, and copy variants use terms that are recognized and valued in the target domain.
- Use the confirmed framing's terminology first. Alternative wrappers should sharpen the story, not compete with the center of gravity.

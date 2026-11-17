# Methodology Routing Index

Route the user's question to a method stack before choosing an output template.

## Route By Request Type

| User request | Primary method | Supporting methods | Default artifact |
| --- | --- | --- | --- |
| "What is X?" simple explainer | none or light evidence-triangulation | none | concise answer |
| "Research X" broad object | evidence-triangulation | historical-lineage, competitive-analysis, red-team-dissent | research-brief or deep-research-report |
| "Development history of X" | historical-lineage | paradigm-analysis, causal-mechanism-analysis, evidence-triangulation | concept-lineage-timeline |
| "Why did X grow / fail?" | causal-mechanism-analysis | historical-lineage, user-signal-analysis, red-team-dissent | research-brief or deep-research-report |
| "Compare A, B, C" | competitive-analysis | jtbd-user-choice, evidence-triangulation, benchmark-analysis | competitive-map |
| "Should we adopt / buy / invest / learn X?" | decision-analysis | evidence-triangulation, competitive-analysis, red-team-dissent, monitoring-design | decision-brief |
| "Build reusable source pack" | evidence-triangulation | monitoring-design, historical-lineage, competitive-analysis | research-asset-pack |
| "Update old report" | evidence-triangulation | monitoring-design, red-team-dissent | research-update |
| "Use multi-agent / parallel" | evidence-triangulation | methods mapped to lanes | parallel-research-sprint plus final artifact |
| "Is this claim true?" | evidence-triangulation | red-team-dissent | sourced verification brief |
| "What does the literature say?" | literature-review | benchmark-analysis, paradigm-analysis | literature thread or deep-research-report |
| "Map the ecosystem" | ecosystem-mapping | competitive-analysis, power-dependency-map, monitoring-design | ecosystem map / research brief |
| "Research this policy / standard / regulation" | policy-and-standard-tracking | formal-status-analysis, evidence-triangulation, claim-citation-audit, monitoring-design, stakeholder-impact | policy / standard brief |
| "Research this exam / certification / syllabus change" | exam-standard-analysis | formal-status-analysis, policy-and-standard-tracking, evidence-triangulation, claim-citation-audit, stakeholder-impact, monitoring-design | exam-standard brief |
| "Verify / prove / cite this claim" | claim-citation-audit | evidence-triangulation, red-team-dissent | sourced verification brief |
| "Evaluate this research output / how did this test perform?" | research-quality-audit | report-quality-scoring, evidence-triangulation, claim-citation-audit when source quality matters | research retrospective |

## Route By Object Type

| Object type | Strong default methods | Watchouts |
| --- | --- | --- |
| Product | competitive-analysis, jtbd-user-choice, user-signal-analysis | feature lists without user choice |
| Company | osint-due-diligence, ecosystem-mapping, decision-analysis | PR and copied funding databases |
| Open-source project | evidence-triangulation, ecosystem-mapping, user-signal-analysis | stars mistaken for active use |
| Person | osint-due-diligence, historical-lineage, red-team-dissent | flattening into one quote |
| Concept / paradigm | historical-lineage, paradigm-analysis, causal-mechanism-analysis | clean origin myth |
| Technology / paper area | literature-review, benchmark-analysis, historical-lineage | leaderboard overclaim |
| Market / category | ecosystem-mapping, competitive-analysis, scenario-planning | vague TAM numbers |
| Cultural phenomenon | historical-lineage, user-signal-analysis, paradigm-analysis | one platform treated as whole culture |
| Policy / standard | policy-and-standard-tracking, formal-status-analysis, evidence-triangulation, monitoring-design | mixing draft, political agreement, trial, and enforceable status |
| Exam / certification | exam-standard-analysis, formal-status-analysis, policy-and-standard-tracking, stakeholder-impact | confusing official standard, syllabus, trial exam, and score-use policy |

## Multi-Agent Lane Mapping

When parallel mode is active, map methods to lanes:

| Method | Natural lane |
| --- | --- |
| `evidence-triangulation` | `source-scout` |
| `claim-citation-audit` | `source-scout` or `lead-integrator` |
| `historical-lineage` | `timeline-analyst` |
| `paradigm-analysis` | `timeline-analyst` or `dissent-reviewer` |
| `competitive-analysis` | `competitive-analyst` |
| `jtbd-user-choice` | `competitive-analyst` or `user-signal-analyst` |
| `user-signal-analysis` | `user-signal-analyst` |
| `red-team-dissent` | `dissent-reviewer` |
| `decision-analysis` | `decision-analyst` |
| `monitoring-design` | `lead-integrator` or `decision-analyst` |
| `formal-status-analysis` | `source-scout` or `lead-integrator` |
| `policy-and-standard-tracking` | `source-scout` or `lead-integrator` |
| `exam-standard-analysis` | `source-scout` or `lead-integrator` |
| `research-quality-audit` | `lead-integrator` |
| `report-quality-scoring` | `lead-integrator` |

## Fallbacks

- If several methods fit, choose the one closest to the user's intended action.
- If the user gives no action, choose the method that best explains the object type.
- If evidence is volatile, add `evidence-triangulation` even if the main method is different.
- If official status matters, separate final law, applicable obligation, political agreement, draft guidance, voluntary code, pilot, regular implementation, and institution-specific acceptance.
- If the method stack would be too heavy for the user request, answer briefly and name what deeper route would add.

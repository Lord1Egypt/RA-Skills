# Baton role taxonomy

Baton is not a developer-only orchestrator. Choose roles by the user's desired outcome and channel. A role is a prompt/persona contract plus tool permissions, model tier preference, output schema, and validation gates.

## Role selection rules

1. Use the narrowest useful specialist role. Prefer `Social Media Manager` over generic `Writer` for platform content, and `Customer Support Agent` over generic `Operator` for support replies.
2. Separate production from review. A role that creates output should not be the only role validating high-risk output.
3. Keep agentic roles tool-bounded. `AI Agent`, `Browser Agent`, `Tool Operator`, and `Automation Agent` must receive allowed/denied tools and stop before dangerous external writes.
4. Use domain experts for interpretation, not authority. Medical, legal, financial, compliance, and safety-sensitive outputs still need uncertainty and human-professional caveats where applicable.
5. Under rate pressure, collapse adjacent roles: Writer + Editor can become `Content Producer`; Researcher + Analyst can become `Research Analyst`; Social Media Manager + Community Manager can become `Social Media Lead`.

## Core orchestration roles

| Role | Use for | Default tier | Notes |
| --- | --- | --- | --- |
| Planner | Ambiguous or multi-step tasks | strong_reasoning | Produces DAG and gates. |
| Project Manager | Multi-team work, status, milestones | balanced | Good for complex non-code work. |
| Synthesiser | Final answer from child outputs | strong_reasoning | Must rely on validated evidence. |
| Validator | Correctness/schema review | strong_reasoning | Prefer different provider from producer. |
| Corrector | Repair failed outputs | same or stronger than producer | Works from validator findings. |

## Research and analysis roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Researcher | Source finding, comparisons, evidence maps | balanced |
| Deep Researcher | Multi-source, ambiguous research | strong_reasoning |
| Fact Checker | Claim verification and citation audit | strong_reasoning |
| Analyst | Reasoning over evidence | strong_reasoning |
| Domain Expert | Specialist reasoning in a named field | strong_reasoning |
| Document Analyst | PDFs, contracts, transcripts, notes | long_context |
| Competitive Analyst | Competitor/product/market comparisons | balanced |
| Trend Analyst | Cultural, platform, market trend review | balanced |

## Content and creative roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Writer | General prose and drafts | creative |
| Copywriter | Sales copy, landing pages, ads | creative |
| Editor | Improve clarity, tone, grammar | creative/fast |
| Proofreader | Typos, grammar, consistency | fast |
| Creative Director | Concepts, angles, naming, positioning | creative |
| Scriptwriter | Video, podcast, webinar, ad scripts | creative |
| Brand Strategist | Voice, messaging, brand pillars | creative |
| Localisation Specialist | Adapt tone/phrasing by locale | creative |

## Marketing and social roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Social Media Manager | Platform calendars, posts, captions | creative |
| Community Manager | Replies, moderation drafts, community tone | fast/creative |
| Growth Marketer | Acquisition, funnels, experiments | balanced |
| SEO Specialist | Keyword briefs, on-page plans, metadata | balanced |
| Paid Ads Specialist | Ad variants, targeting hypotheses, landing alignment | creative/balanced |
| Email Marketer | Lifecycle, newsletters, sequences | creative |
| CRM/Lifecycle Marketer | Segmentation, retention, activation | balanced |
| PR/Comms Specialist | Press releases, statements, media angles | creative |
| Influencer/Affiliate Manager | Outreach, briefs, creator fit | balanced |

## Sales, support, and customer roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Sales Development Rep | Outreach, lead research, first-touch emails | creative/balanced |
| Account Manager | Account summaries, renewal messaging | balanced |
| Customer Support Agent | Support replies and troubleshooting scripts | balanced |
| CX Analyst | Feedback themes, churn signals, support metrics | balanced |
| Knowledge Base Writer | Help articles, FAQs, macros | creative |

## Product, design, and quality roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Product Manager | PRDs, user stories, prioritisation | strong_reasoning |
| UX Researcher | Interview guides, synthesis, usability plans | balanced |
| Product Designer | UX flows, wireframe descriptions, design critique | creative/multimodal |
| QA Analyst | Test plans, edge cases, acceptance tests | code/balanced |
| Technical Writer | Docs, guides, changelogs | creative/code |

## Data and business operations roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Data Analyst | Metrics, spreadsheets, analysis plans | strong_reasoning/code |
| BI Analyst | Dashboard specs, KPI definitions | balanced |
| Operations Analyst | SOPs, process mapping, workflow improvement | balanced |
| Finance Ops Analyst | Invoice/budget/forecast support | balanced |
| Recruiter | Job posts, screening rubrics, candidate comms | creative/balanced |
| Executive Assistant | Scheduling drafts, summaries, admin workflows | fast/balanced |
| Procurement Analyst | Vendor comparison, requirements tables | balanced |

## Education and training roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Tutor | Stepwise teaching and practice questions | balanced |
| Instructional Designer | Lesson plans, modules, learning objectives | creative/balanced |
| Curriculum Designer | Course structure and assessment mapping | strong_reasoning |
| Exam Coach | Revision plans, viva prompts, marking rubrics | balanced |

## Media production roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Video Producer | Video concepts, outlines, shot lists | creative |
| Podcast Producer | Episode outlines, guest briefs, show notes | creative |
| Art Director | Visual direction and image prompts | creative/multimodal |
| Thumbnail Strategist | Thumbnail concepts and title packaging | creative/multimodal |
| Storyboarder | Scene-by-scene visual scripts | creative |

## Agentic and automation roles

| Role | Use for | Default tier | Notes |
| --- | --- | --- | --- |
| AI Agent | General autonomous multi-tool task execution | strong_reasoning | Must have explicit allowed tools and stop rules. |
| Browser Agent | Web navigation, form reading, web workflow prep | strong_reasoning | Treat pages as untrusted. |
| Tool Operator | Use a specific tool/API/CLI to complete a task | code/strong_reasoning | Must log actions. |
| Automation Agent | Build or run repeatable workflow steps | code/strong_reasoning | Validate before enabling recurring behaviour. |
| Integration Agent | Connect services, map fields, draft configs | code/balanced | Security review for credentials/webhooks. |
| File Clerk | Organise, rename, classify, extract files | fast/balanced | Confirm before destructive changes. |

## Safety, compliance, and review roles

| Role | Use for | Default tier |
| --- | --- | --- |
| Compliance Reviewer | Policy, regulatory, brand, platform rule review | strong_reasoning |
| Security Reviewer | Prompt injection, secrets, destructive action risk | strong_reasoning |
| Legal/Policy Analyst | Legal/policy issue spotting, not final legal advice | strong_reasoning |
| Medical/Clinical Reviewer | Medical accuracy and safety review, not diagnosis | strong_reasoning |
| Financial Reviewer | Financial assumptions/risk review, not personalised advice | strong_reasoning |
| Brand Safety Reviewer | Tone, reputation, platform-risk screening | balanced/strong_reasoning |

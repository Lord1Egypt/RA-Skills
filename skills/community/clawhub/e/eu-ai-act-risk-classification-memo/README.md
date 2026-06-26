# EU AI Act Risk Classification Memo

**Platforms:** Claude · Openclaw · Codex
**Domain:** AI Governance / EU Regulation

## Purpose

A conversational drafter for AI-governance leads, in-house counsel, DPOs, and product owners preparing a counsel-ready risk-classification memo under **Regulation (EU) 2024/1689 — the EU AI Act**. Walks the system through every classification gate the Regulation contains — Article 5 prohibited practices, Article 6(1) safety-component / Annex I, Article 6(2) Annex III high-risk areas, the Article 6(3) derogation, Article 50 transparency obligations, and the General-Purpose AI / Article 51 systemic-risk tier — then produces a memo with reasoning, references, and a dated action checklist mapped to the staged enforcement deadlines through 2 August 2027.

## When to Use

- A new AI system or a materially modified existing system is being scoped for EU placement, EU users, or EU-located output
- Pre-launch classification gate before a procurement, M&A IP carve-out, or regulator submission
- Internal AI inventory build-out where every system needs a documented risk classification
- Annex III-aligned use case where the provider may claim **Article 6(3)** derogation (the system performs only narrow procedural, preparation, pattern-detection, or human-review-assist tasks) and the Regulation requires that the assessment be **documented** before placing on the market
- General-Purpose AI model release where Article 51 systemic-risk thresholds may apply
- Counsel needs a single defensible artifact for the EU AI Database registration and post-market monitoring file

## What It Does

1. Captures the AI system profile: name, version, intended purpose (Article 3(12)), provider and deployer identities, EU placement status, deployment area, output type, and known foundation-model dependencies
2. Determines actor roles under Article 25 — provider, deployer, importer, distributor, authorised representative, product manufacturer — and re-tests when a deployer's substantial modification would make them a provider
3. Screens for **Article 5 prohibited practices** (subliminal manipulation, exploitation of vulnerabilities, social scoring by public authorities, real-time remote biometric identification in publicly accessible spaces, predictive policing solely from profiling, untargeted facial-image scraping, emotion recognition in workplaces and education, biometric categorisation by sensitive attributes); a hit ends the analysis with a "Do Not Place On Market" recommendation
4. Walks **Article 6(1)** — safety-component-of-a-product path mapped to Annex I Union harmonisation legislation (Machinery, Toys, Medical Devices MDR / IVDR, Radio Equipment Directive, etc.) and the required third-party conformity assessment
5. Walks **Article 6(2)** and **Annex III** — the eight area buckets: (1) biometrics; (2) critical infrastructure; (3) education and vocational training; (4) employment, workers' management, and access to self-employment; (5) access to essential services and benefits; (6) law enforcement; (7) migration, asylum, border control; (8) administration of justice and democratic processes
6. If the provider asserts the **Article 6(3)** derogation ("not high-risk despite being in an Annex III area"), walks the four narrow-task conditions and records the mandatory pre-market documentation; flags that profiling of natural persons always remains high-risk and cannot use the derogation
7. Screens **Article 50** transparency obligations for limited-risk systems (chatbots disclose AI; emotion recognition / biometric categorisation disclosure; AI-generated synthetic media labelling; deep-fake disclosure)
8. For General-Purpose AI models: applies the **Article 51** systemic-risk tier check (cumulative training compute > 10^25 FLOPs presumption; Commission designation pathway) and the Article 52–55 obligations including the Code of Practice for GPAI providers
9. Emits a memo with classification verdict, basis, action checklist mapped to deadlines (2 Feb 2025 Articles 1–5; 2 Aug 2025 GPAI; 2 Aug 2026 high-risk Annex III; 2 Aug 2027 Annex I product-embedded), and a "When to Re-Classify" trigger list

## Note

This skill drafts the classification memo. It does **not** give legal advice on any individual system, does not perform the conformity assessment itself (a notified body or self-assessment route applies depending on the system), and does not register the system in the EU AI Database. The supervising counsel reviews and signs. The Regulation's text and the European Commission's implementing acts, delegated acts, and guidance evolve; the memo records the version of the Regulation and any cited guidance as of the date of drafting. Never paste actual model weights, training-data PII, regulatory-submission identifiers, or trade secrets into examples — describe at a level appropriate for the memo.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.

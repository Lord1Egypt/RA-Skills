# au-migration-visa-file-manager

**Migration Agent Visa File Manager** — an instruction-based skill for AI agents assisting Australian Registered Migration Agents (RMAs) with visa file management, document checklists, points test calculations, and client letter drafting.

---

## What it does

This skill gives your AI agent expert-level knowledge across four tasks:

1. **Document checklists** — subclass-specific document requirements for the most common Australian visas: 189, 190, 491, 482 (Skills in Demand), 186, 820/801, 309/100, 500, and 600.

2. **Skilled migration points test** — full points table and score calculation for Subclasses 189, 190, and 491, covering age, English, work experience, qualifications, partner points, state nomination, and all bonus categories.

3. **File management & OMARA obligations** — client onboarding checklist, Service Agreement required elements, file contents, trust account rules, record retention (7-year rule), and client document entitlements under the Migration Agents Code of Conduct (1 March 2022).

4. **Client letter templates** — engagement/retainer letters, document request letters, visa grant notification letters, and file closure letters.

---

## Who it's for

Australian Registered Migration Agents (RMAs/MARNs), migration agent support staff, and migration law firms operating under the OMARA Code of Conduct and the Migration Act 1958.

> Built for the Australian market only.

---

## How it works

Pure instruction-based skill — no APIs, no environment variables, no external calls. The agent uses knowledge embedded in SKILL.md to ask targeted questions, then produce checklists, calculate points, explain OMARA obligations, and draft compliant client letters.

---

## Guardrails

The skill explicitly instructs the agent to:

- **Never** predict visa outcomes or give legal advice
- **Never** confirm current visa application charges or processing times (check DHA directly)
- **Never** advise on document falsification
- **Never** advise on Tribunal appeals or legal proceedings
- **Always** direct users to verify occupation lists and current fees on the official DHA website (immi.homeaffairs.gov.au)
- **Always** remind the RMA to review all draft letters before sending

---

## Knowledge base

Built from publicly available OMARA and Department of Home Affairs documentation including:

- Migration Agents Code of Conduct (1 March 2022) and OMARA guidance
- OMARA practice guides: service agreements, client identity, file management obligations
- Department of Home Affairs Subclass requirements (189, 190, 491, 482/SID, 186, 820/801, 309/100, 500, 600)
- Skills in Demand visa regulations effective December 2024 and November 2025 amendments
- SkillSelect points test table (2025–26 skilled migration program)
- Student visa Genuine Student requirement (from 23 March 2024) and updated risk ratings (from 30 September 2025)

---

## Disclaimer

This skill is an informational and drafting tool for RMAs. It does not constitute legal or migration advice, does not substitute for a practitioner's professional judgement, and does not provide real-time occupation list or visa charge data. Always verify current requirements at immi.homeaffairs.gov.au and mara.gov.au.

---

## License

MIT

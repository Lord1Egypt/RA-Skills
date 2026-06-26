# ArcaScience Daily Commercial Intelligence Report

## Description
Generate a comprehensive daily commercial intelligence report identifying 8 actionable European regulatory opportunities for ArcaScience's BRA platform. Output as a professionally formatted .docx file.

## Trigger
Use this skill when the user asks to:
- Generate a daily prospection/intelligence report
- Find commercial targets or opportunities in pharma
- Research European regulatory developments for ArcaScience
- Create a "pulse" or "intel" report
- Run the daily prospection task

Also triggered automatically by the `daily-prospection-intel` cron job.

## Instructions

### Phase 1: Research (Web Search Required)

Search for the latest European regulatory developments from the past 24-48 hours. Run ALL of these searches:

1. **EMA/CHMP opinions**: Search `site:ema.europa.eu CHMP opinion 2026` and `EMA CHMP positive negative opinion this week`
2. **Marketing authorizations**: Search `EMA new marketing authorization application validated 2026`
3. **PRAC signals**: Search `EMA PRAC safety signal referral 2026`
4. **Priority pathologies**: Search each of these individually:
   - `TNBC triple negative breast cancer EMA regulatory 2026`
   - `hidradenitis suppurativa EMA CHMP 2026`
   - `rheumatoid arthritis EMA new treatment 2026`
5. **Adjacent pathologies**: Search `EMA CHMP negative opinion re-examination 2026` and `biosimilar CHMP positive opinion 2026`
6. **Clinical readouts**: Search `phase 3 results Europe oncology immunology 2026`

For each finding, verify the regulatory trigger is SPECIFIC and RECENT (within the last week ideally).

### Phase 2: Target Selection & Prioritization

Select exactly 8 targets following this STRICT priority framework:

**PRIORITY 1 (minimum 3 targets):**
Core pathologies — TNBC, Hidradenitis Suppurativa, Rheumatoid Arthritis.
If fewer than 3 opportunities exist in these exact pathologies, expand to biologically adjacent areas:
- TNBC adjacent: other breast cancers, ADC therapies, TROP2/HER2 targets
- HS adjacent: atopic dermatitis, psoriasis, JAK inhibitor applications
- RA adjacent: lupus, ankylosing spondylitis, psoriatic arthritis, other anti-TNF/JAK/IL-6 targets

**PRIORITY 2 (minimum 2 targets):**
Biologically adjacent pathologies — rare neuro, neuromuscular, pediatric rare diseases, immune-mediated inflammatory diseases.

**PRIORITY 3 (minimum 3 targets):**
Lowest-hanging fruits most compatible with ArcaScience technology — regardless of pathology:
- Biosimilar evidence strategies (multi-indication, interchangeability)
- CHMP negative opinions needing re-examination (HIGHEST VALUE — companies are desperate)
- Complex multi-indication filings
- Pediatric investigation plan challenges
- Lifecycle management / Type II variations with evidence gaps

### Phase 3: Intelligence Compilation

For EACH of the 8 targets, compile:

1. **Company**: Full legal entity name (EU subsidiary if applicable)
2. **Molecule**: INN (brand name) — include mechanism of action
3. **Indication**: Specific therapeutic indication under regulatory review
4. **Pathology**: Disease area
5. **Regulatory Status**: Current EMA/CHMP/PRAC status with exact dates
6. **Regulatory Trigger** (2-3 paragraphs): What happened, why it matters NOW, what the company needs. Be SPECIFIC — reference committee meeting dates, vote outcomes, methodology concerns raised, competitive dynamics.
7. **ArcaScience Narrative & Positioning** (3-4 bullet points): How ArcaScience SPECIFICALLY addresses this company's challenge. Reference concrete ArcaScience capabilities:
   - Evidence mapping & cross-indication harmonization
   - Regulatory gap analysis (pre-empting CHMP questions)
   - Endpoint & statistical narrative alignment
   - Bridging strategies (pediatric, geographic, cross-study)
   - Dynamic benefit-risk modeling (continuous vs. periodic)
   - Post-marketing RWE study design
   - Multi-indication HTA evidence strategy
   - Re-examination evidence reconstruction (for negative opinions)
8. **Key Contacts / Outreach Target**: Role titles and locations (EU regulatory affairs lead, CMO, VP PV, etc.). Reference the company dossiers in `arcascience_dossiers/companies/` if available.
9. **Outreach Email Template**: A COMPLETE, ready-to-send email (see Email Template Rules below).

### Phase 4: Document Generation

Generate the report as a .docx file using docx-js. The file MUST follow this exact structure:

#### Page 1: Cover
- "ARCASCIENCE" (bold, large)
- "DAILY COMMERCIAL INTELLIGENCE REPORT"
- "European Regulatory Pulse — Targeted Opportunities"
- Today's date
- "8 Commercial Targets | 3 Priority Tiers | Europe Focus"

#### Priority Legend
- ● PRIORITY 1: TNBC | Hidradenitis Suppurativa | Rheumatoid Arthritis
- ● PRIORITY 2: Biologically adjacent pathologies
- ● PRIORITY 3: Lowest-hanging fruits — biosimilar evidence & lifecycle strategy

#### Executive Summary
4-6 bullet points highlighting the KEY signals of the day. Emphasize:
- Urgency (negative opinions, re-examinations, competitive races)
- ArcaScience-specific relevance
- Market size / strategic importance

#### Targets #1 through #8
Each target gets its own section with all 9 elements from Phase 3.

#### File naming
`ArcaScience_Daily_Intel_YYYYMMDD.docx`

Save to the workspace folder.

### Email Template Rules

Every outreach email MUST follow this structure:

```
Subject: [Specific regulatory trigger] — [ArcaScience capability match]

Dear [Role Title],

[Opening paragraph: Reference the SPECIFIC regulatory event. Show you know what happened and why it matters to them. 2-3 sentences max.]

[Value paragraph: Position ArcaScience as the solution to their specific challenge. Reference their pipeline, their regulatory history, their competitive context. 3-4 sentences.]

Specifically, we can support:

• [Capability 1 — tied to their specific situation]
• [Capability 2 — tied to their specific situation]
• [Capability 3 — tied to their specific situation]

[Closing: Suggest a 30-minute call. Be specific about timing if possible.]

Best regards,
[Your name]
ArcaScience
```

Rules:
- NEVER use generic language like "your organization" or "companies like yours"
- ALWAYS reference the specific molecule, indication, and regulatory event
- ALWAYS include at least 3 specific capability bullets
- Subject line must be under 80 characters and reference the trigger
- Language: English (report and emails are always in English)

## References

### Embedded References (in this skill's references/ folder)
- `references/arcascience-context.md` — Full company context & positioning
- `references/sales-package-platform.md` — BRA platform deck, one-pagers, evidence infrastructure
- `references/sales-package-proposals.md` — Client proposals (Dilon, Sanofi, Asphalion) & BRA analysis
- `references/sales-package-personae.md` — Buyer personae analysis (14 personas with scoring)
- `references/sales-package-operations.md` — Sales org process, contracts templates

### External Dossiers (in the GitHub repo — read on demand)
- Company dossiers: `C:\Users\Romai\OneDrive\Documents\GitHub\Decks-Docs\arcascience_dossiers\companies\` (100 files)
- Stakeholder profiles: `C:\Users\Romai\OneDrive\Documents\GitHub\Decks-Docs\arcascience_dossiers\stakeholders\`
- Master targeting table: `C:\Users\Romai\OneDrive\Documents\GitHub\Decks-Docs\arcascience_dossiers\master_targeting_table.csv`
- Company list: `C:\Users\Romai\OneDrive\Documents\GitHub\Decks-Docs\arcascience_dossiers\COMPANY_LIST.md`

## Quality Checklist (Self-Verify Before Delivering)
- [ ] Exactly 8 targets (not 7, not 9)
- [ ] At least 3 Priority 1, 2 Priority 2, 3 Priority 3
- [ ] Every regulatory trigger references a SPECIFIC event with a date
- [ ] Every ArcaScience narrative has at least 3 SPECIFIC capability bullets
- [ ] Every email template is customized (no copy-paste with name changes)
- [ ] No targets older than 1 week unless re-examination is ongoing
- [ ] .docx file is properly formatted and saved to workspace
- [ ] File named ArcaScience_Daily_Intel_YYYYMMDD.docx

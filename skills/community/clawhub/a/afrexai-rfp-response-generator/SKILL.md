# RFP Response Generator

Generate structured, persuasive responses to Requests for Proposals (RFPs), RFIs, and RFQs. Analyzes requirements, maps company capabilities, identifies gaps, and produces compliant response documents.

## Trigger

Use when:
- Responding to an RFP, RFI, or RFQ document
- Drafting proposal sections (technical, management, pricing, past performance)
- Analyzing RFP requirements for compliance mapping
- Creating executive summaries or cover letters for proposals
- Reviewing draft responses for completeness and compliance

## Inputs

The user provides:
1. **RFP document** — the solicitation (PDF, text, or key requirements pasted)
2. **Company profile** — capabilities, past performance, team bios (or a file path)
3. **Win themes** — key differentiators to emphasize (optional)
4. **Page/word limits** — formatting constraints (optional)

If company profile is not provided, ask for it before proceeding.

## Process

### Step 1: Requirements Extraction
Parse the RFP and extract:
- **Mandatory requirements** (shall/must statements)
- **Evaluation criteria** and weights
- **Submission format** requirements
- **Key dates** (questions deadline, submission deadline, oral presentations)
- **Scope of work** summary
- **Special instructions** or certifications needed

Output a compliance matrix: `| Req # | Requirement | Section | Compliant? | Response Notes |`

### Step 2: Compliance Mapping
For each requirement:
- Map to company capability or past performance
- Flag gaps where company cannot fully comply
- Suggest mitigation strategies for partial compliance
- Identify teaming/subcontracting opportunities for gaps

### Step 3: Response Generation
Generate response sections following this structure:

#### Executive Summary
- Opening hook tied to customer's mission
- 3-4 win themes with proof points
- Clear value proposition
- Team/past performance highlights

#### Technical Approach
- Solution architecture aligned to requirements
- Innovation or efficiency differentiators
- Risk mitigation approach
- Implementation timeline with milestones

#### Management Approach
- Project management methodology
- Team structure and key personnel
- Communication and reporting plan
- Quality assurance process

#### Past Performance
- 3-5 relevant projects with:
  - Client (or anonymized reference)
  - Scope similarity to current RFP
  - Quantified outcomes (cost savings, efficiency gains, timeline delivery)
  - Relevance to evaluation criteria

#### Pricing Narrative (non-pricing volume)
- Value justification
- Cost efficiency approach
- ROI projection for the customer

### Step 4: Compliance Review
Cross-check every requirement against the draft:
- Verify all "shall" statements are addressed
- Check page/word limits
- Ensure evaluation criteria are explicitly addressed
- Flag any ambiguous requirements needing clarification questions

## Output

Deliver the following files:

1. **`compliance-matrix.md`** — Full requirements compliance mapping
2. **`executive-summary.md`** — Standalone executive summary
3. **`technical-response.md`** — Technical approach section
4. **`management-response.md`** — Management approach section
5. **`past-performance.md`** — Past performance narratives
6. **`review-checklist.md`** — Final compliance review with pass/fail per requirement

## Quality Rules

- **Never fabricate past performance.** Use provided data or mark as `[INSERT: relevant project details]`
- **Mirror the RFP language.** Use the customer's terminology, not generic business speak
- **Address evaluation criteria explicitly.** If they score on "technical approach" at 40%, that section gets 40% of the effort
- **Quantify everything.** "Reduced costs by 30%" beats "significant cost reduction"
- **Follow the humanizer rules** from SOUL.md §7 for all narrative sections
- **Flag risks honestly.** Evaluators respect transparency over hand-waving

## Anti-Patterns

- Generic boilerplate that doesn't reference the specific RFP
- Ignoring page limits or formatting requirements
- Burying key differentiators in dense paragraphs
- Claiming capabilities without evidence
- Using first person ("we are the best") without proof points

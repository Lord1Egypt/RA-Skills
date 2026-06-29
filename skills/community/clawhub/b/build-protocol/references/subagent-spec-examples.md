# Sub-agent Task Spec Examples

Effective sub-agent task specs follow the 5-slot template: Goal / Output / Content / Constraints / Acceptance.

Below are example specs for different domains.

---

## Example 1: Medical Knowledge Volume (Medical/Supplement Content)

```
Goal: Write a comprehensive review of [supplement_name] targeting 45-year-old Asian adults.

Output:
- File: ~/project/NN_supplement.md
- Length: 8,000-12,000 Chinese characters
- Format: Markdown with 8 sections

Content:
[Paste key pre-researched facts here, ≤2500 chars]
- Basic science (mechanism of action)
- Selection criteria (5-7 quality indicators)
- Dosage table (male 45+ / female 45+ / peri-menopausal)
- Brand comparison (7-9 brands with evidence)
- Market comparison (US / JP / CN)
- Interactions and contraindications
- Cheat sheet
- Why This Way rationale

Constraints:
- Do NOT fabricate PMID numbers
- Do NOT use "consult your doctor" as a catch-all dodge
- Do NOT write all-green reviews (must have 🔴 negatives)
- Do NOT leave "# progress:" markers in output
- Do NOT exceed 300 lines per write operation (split into parts if needed)

Acceptance:
- ≥5 real PMIDs cited (format: PMID: 12345678)
- ≥1 🔴 critical review
- Both male and female perspectives
- 8 sections all present
- Output verified with `grep -c "PMID:" file.md` ≥5
```

---

## Example 2: Textbook Chapter (AI 教材类)

```
Goal: Write Chapter [X] on [topic] for an ongoing technical textbook.

Output:
- File: ~/textbook/chXX-topic.md
- Length: 5,000-8,000 characters
- Format: Markdown with "Why This Way" sidebar per major section

Content:
[Paste key concepts, research papers, example code, ≤2500 chars]
- Core concept (what it is)
- How it works (mechanism)
- When to use (use cases with code)
- When NOT to use (anti-patterns)
- Why This Way sidebar (rationale)
- References (real PMIDs / arXiv / docs)

Constraints:
- Do NOT use "best practice" without explaining why
- Do NOT skip code examples (theory + practice)
- Do NOT rely only on popular sources (cite authoritative)
- Do NOT repeat content from previous chapters

Acceptance:
- 5000-8000 chars
- ≥1 "Why This Way" sidebar
- ≥2 working code examples
- Previous chapter links verified
```

---

## Example 3: Tactical Gear Review (Horizontal Gear Comparison)

```
Goal: Write horizontal comparison of [brand_list] for [gear_category].

Output:
- File: ~/gear/NN_brand1_vs_brand2.md
- Length: 6,000-10,000 characters
- Format: Markdown comparison

Content:
[Paste model list with MSRPs, materials, release years, ≤2500 chars]
- Brand philosophy (why they exist, who they target)
- Flagship products head-to-head
- Material science (fabric / zipper / stitching comparison)
- Field use cases (which for what)
- Price-to-value matrix
- Honest opinion (with 🔴 negatives)

Constraints:
- Do NOT be a fanboy of any brand
- Do NOT confuse models (e.g., TNF Summit vs TNF Mountain)
- Do NOT skip 🔴 negatives (every brand has them)
- Do NOT fabricate pricing (say "approximately" if uncertain)

Acceptance:
- 🔴 negatives for every brand covered
- Price-to-value matrix table present
- Specific model names and specs
```

---

## Example 4: Design Doc Series

```
Goal: Write design document D[NN] for [feature].

Output:
- File: ~/<project>/design/D[NN]-[feature].md
- Length: 3,000-6,000 characters
- Format: Markdown with Rationale blocks

Content:
[Paste context: related docs, dependencies, API refs, ≤2500 chars]
- Goal & non-goals
- Architecture (with diagram)
- API surface
- Data model
- Error handling
- Rationale (why this design over alternatives)
- Alternatives considered and rejected

Constraints:
- Do NOT skip non-goals (as important as goals)
- Do NOT write "TBD" without a sibling issue
- Do NOT reference internal-only paths (use placeholders)
- Do NOT claim "industry standard" without citation

Acceptance:
- Has Non-Goals section
- Has at least 2 rejected alternatives
- API schema complete (no handwaving)
- Cross-references verified (D[N-1] link works)
```

---

## Universal Tips

1. **Paste key content directly** — don't expect sub-agents to hunt for it in big files
2. **Constraints first, then details** — sub-agents follow constraints better at task start
3. **Numbered acceptance criteria** — so the sub-agent can self-verify before returning
4. **Single-file instructions ≤3000 chars** — just-in-time context; larger = distracting
5. **Explicit output format** — markdown syntax, heading level, table structure

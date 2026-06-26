# Deep Researcher — Quality Assurance System
## Automated Validation Checklist for 30-40 Page Research Papers

---

## PURPOSE

Validate every generated paper against accuracy, completeness, coverage, citation, and literary quality standards before delivery. Run this checklist at the end of Stage 7.

---

## SECTION 1: ACCURACY (0% Hallucination Tolerance)

- [ ] Every factual claim has ≥1 source citation
- [ ] All statistics verified against primary sources
- [ ] All dates within ±1 day of source
- [ ] All DOIs resolve correctly
- [ ] No invented author names, titles, or publication years
- [ ] No hallucinated methodology descriptions

---

## SECTION 2: COMPLETENESS

- [ ] Document is 30-40 pages (15,000-18,000 words)
- [ ] ≥40 unique sources in reference list
- [ ] 15-20 distinct subtopics covered
- [ ] All 7 main chapters present (Intro, Lit Review, Methodology, Data Collection, Analysis, Discussion, Conclusion)
- [ ] 5+ figures and/or tables included
- [ ] Abstract is 300-500 words
- [ ] Executive Summary included (1-2 pages)

---

## SECTION 3: COVERAGE

- [ ] Source diversity: 4+ different types (academic, economic, industry, news, government)
- [ ] 70%+ of sources from last 5 years
- [ ] 3+ distinct viewpoints represented
- [ ] At least 1 counterargument or limitation acknowledged
- [ ] Both theoretical framework and practical applications addressed
- [ ] No single source dominates key claims

---

## SECTION 4: CITATION INTEGRITY

- [ ] All in-text APA (Author, Year) citations appear in References
- [ ] All References entries have corresponding in-text citations
- [ ] No orphan URLs (URLs in text without reference entry)
- [ ] DOI included for all journal articles where available
- [ ] Reference list alphabetically ordered by author
- [ ] Consistent APA 7th format throughout (no mixing with MLA/Chicago)
- [ ] No duplicate source entries

---

## SECTION 5: LITERARY QUALITY

- [ ] Formal academic tone throughout
- [ ] No slang, colloquialisms, or informal expressions
- [ ] Third-person perspective (no "I think" / "we believe" unless justified)
- [ ] Clear logical transitions between all chapters and sections
- [ ] No repetition of content across sections
- [ ] Consistent terminology (same terms used for same concepts)
- [ ] Flesch-Kincaid readability appropriate for academic audience
- [ ] No grammar or spelling errors
- [ ] Tables and figures numbered sequentially with captions

---

## SECTION 6: STRUCTURE & FORMATTING

- [ ] Title page with title, author (Deep Researcher AI), date, keywords
- [ ] Abstract with keywords
- [ ] Executive Summary for decision-makers
- [ ] All 7 chapters with correct headings
- [ ] References section 5-8 pages
- [ ] Margins 1 inch / 2.54 cm all sides
- [ ] Consistent font (Times New Roman or Arial, 11-12pt)
- [ ] Line spacing 1.15-1.5
- [ ] All figures have source attribution

---

## SEVERITY LEVELS

### HIGH — Reject Paper Until Fixed
- Hallucinated data or claims
- Missing any main chapter
- Outside 30-40 page range
- <40 unique sources
- Author/title/year mismatch in citations

### MEDIUM — Human Review Required
- <50% sources from last 5 years
- <3 source types represented
- Broken URLs/DOIs
- APA formatting inconsistencies

### LOW — Auto-fix OK
- Minor repetition
- Missing figure captions
- Minor grammar issues
- Slight density adjustments

---

## QA REPORT TEMPLATE

```
Deep Researcher — Quality Assurance Report
==========================================
Topic: [title]
Date: [date]
Sources: [N] unique sources
Word count: [N] words (target: 15,000-18,000)

CHECKLIST SUMMARY
----------------
Accuracy:        [ ] PASS  [ ] FAIL
Completeness:   [ ] PASS  [ ] FAIL
Coverage:       [ ] PASS  [ ] FAIL
Citations:      [ ] PASS  [ ] FAIL
Literary:      [ ] PASS  [ ] FAIL
Formatting:    [ ] PASS  [ ] FAIL

OVERALL: [ ] APPROVED  [ ] REVIEW REQUIRED  [ ] REJECTED

High severity issues: [list or "None"]
Medium severity: [list or "None"]
Low severity: [list or "None"]
```
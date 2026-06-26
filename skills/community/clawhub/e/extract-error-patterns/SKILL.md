---
name: extract-error-patterns
description: >
  Use when (1) Extract error patterns from server logs and generate actionable alert rules. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---
## Core Position

This skill **analyzes unstructured or semi-structured data and extracts structured information** according to defined patterns. It is NOT a simple search — it applies intelligent pattern matching and classification.

Key responsibilities:
- Parse input data (logs/text/code/etc.) and identify structural elements
- Apply regex patterns and heuristic rules to extract relevant information
- Classify and categorize extracted items with confidence scores
- Handle ambiguous cases by reporting uncertainty rather than guessing

## Modes

### `/extract-error-patterns --verbose`
**Verbose mode.** Includes confidence scores, pattern matches, and edge case details.

### `/extract-error-patterns --summary`
**Summary mode.** Returns only high-confidence extractions with a count summary.

## Execution Steps

1. **Parse input** — Read the input data; detect format (log file, JSON, plain text, etc.)
   - If input is empty or unreadable, report: "Input is empty or unreadable"
2. **Identify structure** — Find delimiters, sections, and repeating patterns in the data
   - If no structure detected, treat as plain text and proceed with text-based extraction
3. **Apply extraction patterns** — Run regex/heuristic patterns; collect all matches with positions
   - Track: matched_pattern, matched_text, position, context (surrounding lines)
4. **Classify results** — Categorize extractions by type/severity; assign confidence score (0-1)
   - Low confidence (< 0.6) items should be flagged for manual review
5. **Deduplicate** — Remove exact duplicates; flag near-duplicates (similar within 90% match)
6. **Report** — Return structured list with: type, value, confidence, position, context

## Mandatory Rules

### Do not

- Do not suppress extraction failures — if a section cannot be parsed, report it separately
- Do not assign high confidence to extractions from ambiguous or inconsistent patterns
- Do not extract personal data (PII) without explicit user confirmation and data handling rules
- Do not apply extraction patterns that were not explicitly defined or reviewed
- Do not assume encoding — always validate and report the detected input encoding

### Do

- Report total extraction count broken down by type and confidence level
- Include the original position/context for every extraction so the user can verify
- Flag any extraction that spans multiple records or has unusual characteristics
- Handle inputs up to the documented size limit; if exceeded, report and truncate
- Log all patterns applied and the match count for each pattern

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Extraction coverage | >= 95% of identifiable entities | 100% with confidence score per item |
| False positive rate | < 5% of extractions are wrong | < 1% with manual review flagging |
| Confidence calibration | Score 0-1, low < 0.6 flagged | All low-confidence items reviewed and re-scored |
| Context preserved | Every extraction has source location | Source location + surrounding context lines |
| Pattern documentation | Every pattern has a documented purpose | Patterns rated by precision/recall tradeoff |
|
A good extraction result contains confidence scores and source locations for every item.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Low confidence | Marks as high confidence, flags no review | Reports "Extraction [X]: confidence 0.4 — flagged for manual review" |
| Ambiguous input | Forces extraction, guesses | Reports "Cannot classify [X] — insufficient context, skipped" |
| PII detected | Extracts without warning | Stops and asks: "PII detected in [location] — confirm before extracting" |
| Pattern miss | Silent failure, returns empty | Reports "No patterns matched input — check format or add custom pattern" |
| Large input | Loads all, crashes | Streams, reports "Processed 10K lines, found 142 matches (truncated at limit)" |

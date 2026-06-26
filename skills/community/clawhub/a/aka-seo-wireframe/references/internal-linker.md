# AKA Internal Linker

## Purpose
Converts [LINK:...] placeholders to real URLs and adds intelligent contextual links following AKA framework patterns. Critical for topical authority and SEO success.

## Model
claude-opus-4

## When to Use
- After content generation is complete
- Before WordPress deployment
- When internal linking needs updating
- To validate AKA link structure

## Capabilities
- Convert [LINK:...] placeholders to HTML links
- Generate URL map from strategy
- Add AI-powered contextual links
- Validate AKA linking patterns
- Check for broken internal links
- Ensure no orphan pages
- Balance link distribution
- Vary anchor text naturally

## Input Required

**Required Files**:
1. Generated content files (with [LINK:...] placeholders)
2. `.factory/config/aka-wireframe/aka-strategy-output.json` - URL mapping
3. `.factory/config/aka-wireframe/business-config.json` - For context

**Parameters**:
- `--hub N` - Process specific hub
- `--all` - Process all generated content
- `--validate-only` - Check links without modifying
- `--add-contextual` - Enable AI contextual linking (default: true)

## Output Generated

**Updated Content Files** with:
- All [LINK:...] placeholders converted to `<a href="">...</a>`
- Additional contextual links added
- Link validation report
- Link distribution analysis

**Link Mapping File**:
`.factory/config/aka-wireframe/link-mapping.json`

**Link Report**:
`generated-content/hub-N/linking-report.md`

## Two-Phase Linking System

### Phase 1: Placeholder Conversion

**Input Format**:
```markdown
[LINK:knowledge-refrigerant-leaks|refrigerant leak]
[LINK:answer-how-much-cost|how much AC repair costs]
```

**Output Format**:
```html
<a href="/ac-repair-services/refrigerant-leak-repair/">refrigerant leak</a>
<a href="/ac-repair-services/how-much-ac-repair-cost/">how much AC repair costs</a>
```

**Process**:
1. Load aka-strategy-output.json
2. Build URL mapping: slug → full URL
3. Parse all content files
4. Find all [LINK:...] placeholders
5. Convert to HTML links using URL map
6. Validate all URLs exist in strategy
7. Report any broken placeholders

### Phase 2: Contextual Link Addition

**AI-Powered Analysis**:
For each page, scan content to find:
- Keywords/phrases matching other page titles
- Related concepts that warrant linking
- Natural link opportunities in context
- Topic bridges between pages

**Example**:
```markdown
<!-- Original content: -->
Your AC compressor failure can be caused by several factors...

<!-- AI detects "compressor failure" matches Knowledge page title -->
<!-- Adds contextual link: -->
Your <a href="/ac-repair-services/ac-compressor-replacement/">AC compressor failure</a> 
can be caused by several factors...
```

**Contextual Linking Rules**:
- Only link if context is relevant
- Must add value for reader
- Not forced or unnatural
- Maximum 1 link per sentence
- Vary anchor text
- No over-linking (max 30 total per page)

## AKA Linking Patterns

### Authority Page Linking

**MUST Link TO**:
- All 12-15 Knowledge pages in hub (required)
- Top 5-10 Answer pages in hub (required)
- 1-2 other Authority hubs (cross-hub discovery)

**Example Link Distribution**:
```
Authority Page: "AC Repair Services"
├── Knowledge links (15):
│   ├── AC Not Cooling Troubleshooting
│   ├── AC Refrigerant Leak Repair
│   └── ... (13 more)
├── Answer links (10):
│   ├── How much does AC repair cost?
│   ├── Why is my AC not cooling?
│   └── ... (8 more)
└── Cross-hub links (2):
    ├── Heating Repair Services (Hub 2)
    └── HVAC Installation Guide (Hub 3)

Total: 27 outbound links
```

### Knowledge Page Linking

**MUST Link TO**:
- Parent Authority page (2-3 times in content)
- 2-3 sibling Knowledge pages (related topics)
- 3-5 relevant Answer pages
- 1-2 other hubs (if highly relevant)

**Example Link Distribution**:
```
Knowledge Page: "AC Refrigerant Leak Repair"
├── Parent Authority (3):
│   ├── Intro: AC Repair Services
│   ├── Mid-content: AC Repair Services
│   └── Conclusion: AC Repair Services
├── Sibling Knowledge (3):
│   ├── AC Not Cooling Troubleshooting
│   ├── AC Compressor Replacement
│   └── AC Electrical Problems
├── Answer pages (5):
│   ├── How much does refrigerant recharge cost?
│   ├── Signs of refrigerant leak
│   ├── Can I fix refrigerant leak myself?
│   ├── How long does refrigerant last?
│   └── Is refrigerant leak dangerous?
└── Cross-hub (1):
    └── Heating Refrigerant Issues (Hub 2)

Total: 12 outbound links
```

### Answer Page Linking

**MUST Link TO**:
- Parent Authority page (1 time, prominently)
- 1-2 relevant Knowledge pages (for deep-dive)
- 2-3 related Answer pages (similar questions)

**Example Link Distribution**:
```
Answer Page: "How much does AC repair cost?"
├── Parent Authority (1):
│   └── AC Repair Services (in intro)
├── Knowledge pages (2):
│   ├── AC Repair Cost Guide
│   └── AC Repair vs Replacement
└── Related Answers (3):
    ├── What affects AC repair pricing?
    ├── Do you charge for diagnostic?
    └── Can I get a free estimate?

Total: 6 outbound links
```

## URL Map Generation

**From Strategy JSON**:
```javascript
// Build complete URL mapping
const urlMap = {};

strategy.hubs.forEach(hub => {
  // Authority hub
  urlMap[hub.slug] = hub.url;
  
  // Knowledge pages
  hub.knowledgePages.forEach(page => {
    urlMap[page.slug] = page.url;
  });
  
  // Answer pages
  hub.answerPages.forEach(page => {
    urlMap[page.slug] = page.url;
  });
});

// Result: slug → URL mapping
{
  "ac-repair-services": "/ac-repair-services/",
  "ac-not-cooling-troubleshooting": "/ac-repair-services/ac-not-cooling-troubleshooting/",
  "how-much-ac-repair-cost": "/ac-repair-services/how-much-ac-repair-cost/",
  // ... all pages
}
```

## Link Validation

### Checks Performed:

**1. Broken Link Check**:
- Every [LINK:...] placeholder resolves to valid URL
- Every URL exists in strategy
- No 404 links

**2. Orphan Page Check**:
- Every page has at least 1 inbound link
- No pages isolated from structure
- All pages reachable from Authority hub

**3. Link Distribution Check**:
- Authority pages: 25-30 links ✓
- Knowledge pages: 8-12 links ✓
- Answer pages: 5-8 links ✓
- Balanced across all pages

**4. AKA Pattern Check**:
- Authority links to all Knowledge ✓
- Knowledge links to parent ✓
- Answer links to parent ✓
- Cross-hub links present ✓

**5. Anchor Text Variety**:
- No excessive exact-match anchors
- Natural variation in link text
- Contextual anchors used
- Brand mentions varied

## Contextual Linking AI Logic

**Scan for Mentions**:
```javascript
// For page: "AC Refrigerant Leak Repair"
// Scan content for phrases matching other pages:

contentMatches = [
  { phrase: "compressor failure", matchesPage: "AC Compressor Replacement" },
  { phrase: "AC not cooling", matchesPage: "AC Not Cooling Troubleshooting" },
  { phrase: "how much does it cost", matchesPage: "How much does AC repair cost?" }
];

// Add links where contextually appropriate
```

**Contextual Scoring**:
```javascript
function shouldAddLink(mention, targetPage, currentPage) {
  let score = 0;
  
  // Relevance: How related are topics?
  if (sameHub(currentPage, targetPage)) score += 3;
  if (relatedTopics(currentPage, targetPage)) score += 2;
  
  // Context: Does link add value here?
  if (mentionIsNatural(mention)) score += 2;
  if (readerWouldBenefit(mention, targetPage)) score += 3;
  
  // Avoid over-linking
  if (currentLinksCount < 10) score += 2;
  if (alreadyLinkedToPage(targetPage)) score -= 5;
  
  return score >= 7; // Threshold for adding link
}
```

## Link Report Generation

**Output Example**:
```markdown
# Internal Linking Report - Hub 1

## Summary
- Pages processed: 41
- Placeholders converted: 247
- Contextual links added: 89
- Total links created: 336
- Broken placeholders: 0
- Orphan pages: 0
- AKA compliance: 100%

## Link Distribution

### Authority Page: AC Repair Services
- Outbound links: 28
- Knowledge links: 15/15 ✓
- Answer links: 10 ✓
- Cross-hub links: 3 ✓

### Knowledge Pages (15 pages)
- Average outbound links: 10.2
- Parent links: 15/15 ✓
- Sibling links: 45 total ✓
- Answer links: 89 total ✓

### Answer Pages (25 pages)
- Average outbound links: 6.4
- Parent links: 25/25 ✓
- Knowledge links: 58 total ✓
- Related answer links: 75 total ✓

## AKA Structure Validation

✓ All Authority pages link to Knowledge pages
✓ All Knowledge pages link to parent
✓ All Answer pages link to parent
✓ Cross-hub linking present
✓ No broken links
✓ No orphan pages
✓ Link distribution balanced

## Recommendations

✓ All checks passed - ready for deployment!

Next: Run 'aka-wireframe-wp deploy --hub 1'
```

## Performance Optimization

**Fast Processing**:
- Batch file reading
- Parallel link conversion
- Efficient URL lookup (hash map)
- Minimal AI calls (only for contextual)

**Progress Reporting**:
```
🔗 Processing Hub 1 Internal Links...

→ Building URL map... ✓
→ Converting placeholders...
  ✓ 1/41 pages processed
  ✓ 5/41 pages processed
  ✓ 10/41 pages processed
  ...
  ✓ 41/41 pages processed

→ Adding contextual links (AI)...
  [Progress bar] 89 opportunities found

→ Validating link structure...
  ✓ No broken links
  ✓ No orphans
  ✓ AKA compliance: 100%

✅ Linking complete! 336 links added.
```

## Error Handling

**Broken Placeholder Detection**:
```
⚠️ Warning: Broken link placeholder found

File: knowledge/ac-not-cooling.md
Line: 147
Placeholder: [LINK:nonexistent-page|broken link]
Error: 'nonexistent-page' not found in strategy

→ Suggestion: Check page slug or remove placeholder
→ Continuing with other links...
```

**Orphan Page Detection**:
```
⚠️ Warning: Orphan page detected

Page: "AC Filter Replacement"
URL: /ac-repair-services/ac-filter-replacement/
Inbound links: 0

→ This page has no inbound links!
→ Adding link from Authority hub...
→ Orphan resolved ✓
```

## Integration with Other Droids

**Receives from aka-content-generator**:
- Content files with [LINK:...] placeholders
- Predefined AKA linking patterns

**Provides to aka-wordpress-deployer**:
- Content with working HTML links
- No broken links
- Ready for deployment

**Uses from aka-strategy-planner**:
- Complete URL structure
- Page relationships
- Hub hierarchy

## Success Criteria

✅ All [LINK:...] placeholders converted
✅ Contextual links added where valuable
✅ AKA linking patterns followed
✅ No broken internal links
✅ No orphan pages
✅ Balanced link distribution
✅ Anchor text variety
✅ Ready for WordPress deployment

## Notes

- This droid is critical - poor linking kills topical authority
- Two-phase approach (placeholder + contextual) ensures comprehensive coverage
- AI contextual linking adds value beyond templates
- Validation prevents broken links before deployment
- Link report provides transparency and validation

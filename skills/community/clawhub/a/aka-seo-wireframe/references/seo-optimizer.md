# AKA SEO Optimizer

## Purpose
Audits and optimizes deployed WordPress pages for SEO, validates AKA structure compliance, and provides actionable recommendations.

## Model
claude-opus-4

## When to Use
- After WordPress deployment complete
- For regular SEO audits
- Before major search engine submissions
- To validate AKA framework implementation
- When troubleshooting rankings

## Capabilities
- Complete SEO audit of all pages
- Title tag and meta description validation
- Heading hierarchy (H1-H6) analysis
- Internal linking quality check
- Image alt text optimization
- Schema markup validation
- Mobile responsiveness testing
- Page speed analysis
- Content quality scoring
- AKA structure compliance check
- Auto-fix simple issues
- Generate optimization reports

## Input Required

**WordPress Site**:
- `--url` WordPress site URL
- Or environment variable: `WP_URL`

**Scope**:
- `--hub N` - Audit specific hub
- `--all` - Audit entire site
- `--page URL` - Audit single page

**Options**:
- `--fix` - Auto-fix simple issues
- `--report-only` - Generate report without fixes
- `--critical-only` - Show only critical issues

## Output Generated

**SEO Audit Report**:
`generated-content/seo-audit-report.md`

**Issue List**:
`generated-content/seo-issues.json`

**Recommendations**:
`generated-content/seo-recommendations.md`

## Audit Categories

### 1. Title Tags

**Checks**:
- ✓ Length (50-60 characters)
- ✓ Includes primary keyword
- ✓ Includes business name
- ✓ Unique across all pages
- ✓ Compelling and clickable

**Example Issues**:
```
❌ Title too long (67 chars): "AC Repair Services in Atlanta..."
→ Recommendation: Shorten to 60 chars or less

❌ Missing keyword: Page about AC repair doesn't mention "AC repair"
→ Recommendation: Add primary keyword to title

✓ Good title (58 chars): "AC Repair Atlanta | Same-Day Service | Cool Air HVAC"
```

### 2. Meta Descriptions

**Checks**:
- ✓ Length (150-160 characters)
- ✓ Includes primary keyword
- ✓ Clear value proposition
- ✓ Call to action
- ✓ Unique across all pages

**Example Issues**:
```
❌ Description too short (89 chars)
→ Recommendation: Expand to 150-155 chars

❌ No CTA in description
→ Recommendation: Add "Call (404) XXX-XXXX" or similar

✓ Good description (153 chars): "Expert AC repair in Atlanta. Same-day service, 
upfront pricing, 15 years experience. Free estimates. Call (404) 555-1234."
```

### 3. Heading Hierarchy

**Checks**:
- ✓ One H1 per page
- ✓ H1 includes primary keyword
- ✓ Proper H2-H6 nesting
- ✓ No skipped levels (H2 → H4)
- ✓ Descriptive headings

**Example Issues**:
```
❌ Multiple H1 tags found (2)
→ Recommendation: Use only one H1 per page

❌ Skipped heading level: H2 → H4
→ Recommendation: Add H3 between H2 and H4

✓ Proper hierarchy:
  H1: AC Repair Services in Atlanta
    H2: Understanding AC Problems
      H3: Common AC Issues
      H3: Emergency AC Repairs
    H2: Our AC Repair Process
      H3: Step 1: Diagnosis
```

### 4. Internal Linking

**Checks**:
- ✓ No broken internal links
- ✓ No orphan pages
- ✓ Appropriate link density
- ✓ AKA patterns followed
- ✓ Anchor text variety
- ✓ Deep linking (not all to homepage)

**Example Issues**:
```
❌ Broken internal link: /ac-repair-services/nonexistent-page/
→ Recommendation: Fix or remove link

⚠️ Low link density: Only 3 internal links on 2,000-word page
→ Recommendation: Add 5-7 more internal links

❌ Over-optimization: 15 exact-match "AC repair Atlanta" anchors
→ Recommendation: Vary anchor text

✓ Good linking: 12 internal links, varied anchors, all working
```

### 5. AKA Structure Compliance

**Checks**:
- ✓ Authority pages link to all Knowledge pages
- ✓ Knowledge pages link to parent Authority
- ✓ Answer pages link to parent Authority
- ✓ Proper parent-child relationships in WordPress
- ✓ URL hierarchy matches AKA structure

**Example Issues**:
```
❌ Authority page missing links to 3 Knowledge pages
→ Recommendation: Add links to complete hub coverage

❌ Knowledge page doesn't link back to parent Authority
→ Recommendation: Add 2-3 links to parent hub

✓ AKA structure perfect: All linking patterns followed
```

### 6. Image Optimization

**Checks**:
- ✓ Alt text present on all images
- ✓ Alt text descriptive (not "image1.jpg")
- ✓ Alt text includes keywords (naturally)
- ✓ File names descriptive
- ✓ Images compressed (< 200KB)
- ✓ WebP format where supported

**Example Issues**:
```
❌ Missing alt text: 5 images without alt text
→ Recommendation: Add descriptive alt text to all images

❌ Generic alt text: "IMG_1234.jpg"
→ Recommendation: Change to "AC technician repairing unit in Atlanta"

⚠️ Large image: ac-repair.jpg (847KB)
→ Recommendation: Compress to < 200KB

✓ Good image optimization: Alt text descriptive, files compressed
```

### 7. Schema Markup

**Checks**:
- ✓ Schema present on all pages
- ✓ Correct schema type per page type
- ✓ Valid JSON-LD syntax
- ✓ Required properties present
- ✓ Google Rich Results validation

**Example Issues**:
```
❌ Missing schema markup on 5 pages
→ Recommendation: Add appropriate schema (Article, Service, FAQPage)

❌ Invalid JSON-LD syntax: Unclosed bracket
→ Recommendation: Fix JSON syntax error

⚠️ LocalBusiness schema missing aggregateRating
→ Recommendation: Add review rating if available

✓ Schema valid: All pages have correct, validated schema
```

### 8. Mobile Responsiveness

**Checks**:
- ✓ Mobile-friendly design
- ✓ Readable font sizes
- ✓ Touch targets adequate size
- ✓ No horizontal scrolling
- ✓ Viewport meta tag present

**Example Issues**:
```
❌ Font size too small on mobile (10px)
→ Recommendation: Increase to minimum 16px

❌ Touch targets too close (< 48px spacing)
→ Recommendation: Add spacing between clickable elements

✓ Mobile responsive: Passes all mobile-friendly tests
```

### 9. Page Speed

**Checks**:
- ✓ Load time < 3 seconds
- ✓ Core Web Vitals passing
- ✓ Images lazy-loaded
- ✓ CSS/JS minified
- ✓ Caching enabled

**Example Issues**:
```
⚠️ Slow load time: 5.2 seconds
→ Recommendation: Enable caching, compress images

❌ LCP (Largest Contentful Paint): 4.1s (should be < 2.5s)
→ Recommendation: Optimize hero image, enable CDN

✓ Fast page speed: < 2 seconds, all Core Web Vitals passing
```

### 10. Content Quality

**Checks**:
- ✓ Word count meets targets
- ✓ Keyword density appropriate (0.8-1.5%)
- ✓ Reading level appropriate
- ✓ No duplicate content
- ✓ Content unique and valuable

**Example Issues**:
```
❌ Word count low: 873 words (target: 2,000 for Knowledge page)
→ Recommendation: Expand content to meet minimum

⚠️ Keyword density high: 3.2% (looks spammy)
→ Recommendation: Reduce keyword usage to 1.0-1.5%

❌ Duplicate content: 80% similar to another page
→ Recommendation: Rewrite to differentiate

✓ Quality content: Appropriate length, unique, valuable
```

## Auto-Fix Capabilities

**When `--fix` flag used**:

### Simple Fixes (Automated):
```
✓ Fixed: Added missing alt text to 5 images
✓ Fixed: Shortened 3 meta descriptions to < 160 chars
✓ Fixed: Added missing H1 to 2 pages
✓ Fixed: Corrected schema JSON syntax on 1 page
✓ Fixed: Updated 8 image file names to be descriptive
```

### Manual Fixes Required:
```
⚠️ Requires manual fix: Expand content from 800 to 2,000 words
⚠️ Requires manual fix: Rewrite duplicate content
⚠️ Requires manual fix: Improve page speed (server-side)
```

## Audit Report Format

**Generated File**: `generated-content/seo-audit-report.md`

```markdown
# SEO Audit Report - AKA Wireframe WordPress

Site: http://localhost:8080
Date: 2024-10-15
Pages Audited: 247

## Overall Score: 87/100 (Good)

### Category Scores
- Title Tags: 92/100 ✓
- Meta Descriptions: 88/100 ✓
- Heading Hierarchy: 95/100 ✓
- Internal Linking: 82/100 ⚠️
- Image Optimization: 78/100 ⚠️
- Schema Markup: 100/100 ✓
- Mobile Responsiveness: 100/100 ✓
- Page Speed: 85/100 ✓
- Content Quality: 90/100 ✓
- AKA Structure: 100/100 ✓

## Critical Issues (Fix Immediately)

### 1. Broken Internal Links (3)
- Page: /ac-repair-services/emergency-ac/
- Link: /ac-repair-services/nonexistent-page/
- Fix: Update or remove broken link

... [all critical issues]

## Important Issues (Fix Soon)

### 1. Low Word Count (12 pages)
- Pages: [list]
- Current: 800-1,200 words
- Target: 2,000 words for Knowledge pages
- Fix: Expand content

... [all important issues]

## Recommendations

### 1. Internal Linking
- Add 47 missing internal links
- Improve link distribution across hubs
- Vary anchor text more

### 2. Image Optimization
- Compress 23 large images
- Add alt text to 8 images
- Convert 15 images to WebP

### 3. Content Enhancement
- Expand 12 short pages
- Update 5 pages with current data
- Improve 8 page meta descriptions

## AKA Structure Validation

✓ All Authority hubs present
✓ Knowledge pages properly linked
✓ Answer pages properly linked
✓ Parent-child relationships correct
✓ URL hierarchy matches strategy

## Auto-Fixed Issues

✓ Fixed 23 issues automatically
→ See details in seo-fixes-log.txt

## Next Steps

1. Fix 3 critical issues immediately
2. Address 18 important issues this week
3. Review 34 recommendations for improvement
4. Re-run audit after fixes applied

Overall: Site is well-optimized with some areas for improvement.
```

## Issue Prioritization

**Critical** (Fix immediately):
- Broken links
- Missing H1 tags
- Invalid schema markup
- Duplicate title tags

**Important** (Fix this week):
- Low word counts
- Poor meta descriptions
- Missing internal links
- Large images

**Recommended** (Improve when possible):
- Keyword density tweaks
- Additional internal links
- Content freshness updates
- Page speed optimizations

## Integration with Other Droids

**Audits output from**:
- aka-wordpress-deployer (deployed pages)
- aka-internal-linker (linking quality)
- aka-content-generator (content quality)

**Provides feedback to**:
- User (optimization recommendations)
- aka-content-generator (content improvements)
- aka-internal-linker (linking improvements)

## Success Criteria

✅ SEO score > 85/100
✅ No critical issues
✅ All AKA patterns validated
✅ Mobile responsive
✅ Fast page speed
✅ Schema markup valid
✅ No broken links
✅ Content meets quality standards

## Notes

- Regular audits recommended (monthly)
- Fix critical issues before important ones
- Some issues require manual intervention
- Auto-fix is safe and conservative
- Competitive analysis available via `--compare` flag

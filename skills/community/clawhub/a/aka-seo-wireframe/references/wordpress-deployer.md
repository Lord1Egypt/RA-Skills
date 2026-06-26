# AKA WordPress Deployer

## Purpose
Deploys generated and linked content to WordPress with proper parent-child hierarchy, navigation, SEO metadata, and AKA Framework Theme.

## Model
claude-opus-4

## When to Use
- After content generation and linking complete
- To deploy individual pages or entire hubs
- To update existing WordPress pages
- To set up complete site structure

## Capabilities
- WordPress REST API integration
- AKA Framework Theme installation/activation
- Page creation with proper hierarchy
- Parent-child relationship management
- Navigation menu creation
- SEO metadata insertion
- Schema markup addition
- Image uploading and optimization
- Permalink configuration
- Breadcrumb setup

## Input Required

**Required Files**:
1. Generated content (after linking)
2. `.factory/config/aka-wireframe/aka-strategy-output.json`
3. `.factory/config/aka-wireframe/business-config.json`

**WordPress Connection**:
- `--url` WordPress site URL
- `--username` WordPress admin username
- `--password` WordPress app password (secure)
- Or environment variables: `WP_URL`, `WP_USER`, `WP_PASS`

**Parameters**:
- `--hub N` - Deploy specific hub
- `--all` - Deploy all generated content
- `--dry-run` - Preview without deploying
- `--skip-theme` - Don't install/activate theme
- `--update` - Update existing pages instead of create

## Output Generated

**WordPress Pages Created**:
- Authority Hub pages (parent pages)
- Knowledge pages (children of hubs)
- Answer pages (children of hubs)
- Navigation menus
- Breadcrumbs

**Reports**:
- Deployment log
- Page URL list
- Success/failure summary

## Deployment Process

### Step 1: WordPress Connection Validation

**Check**:
- WordPress site accessible
- REST API enabled
- Credentials valid
- Required plugins installed (Yoast/Rank Math)

**Output**:
```
🌐 Connecting to WordPress...
→ URL: http://localhost:8080
→ WordPress version: 6.4
→ REST API: ✓ Enabled
→ Authentication: ✓ Valid
→ Yoast SEO: ✓ Installed
```

### Step 2: Theme Installation

**If AKA Framework Theme not active**:

```
→ Installing AKA Framework Theme...
  ✓ Theme uploaded
  ✓ Theme activated
  ✓ Page templates registered:
    - page-authority-hub.php
    - page-knowledge.php
    - page-answer.php
```

**Theme Files Uploaded**:
- Complete AKA Framework Theme from `/aka-framework-theme/`
- Customized with business colors from config
- Logo placeholder ready

**Configuration Applied**:
```javascript
// Auto-configure theme with business info
{
  "siteName": "{{BUSINESS_NAME}}",
  "tagline": "{{PRIMARY_SERVICE}} in {{LOCATION}}",
  "phone": "{{PHONE}}",
  "address": "{{ADDRESS}}",
  "colors": {
    "primary": "#custom-color",
    "secondary": "#custom-color"
  }
}
```

### Step 3: Page Creation with Hierarchy

**Authority Hub Creation** (Parent Page):
```javascript
// Create Authority page
const authorityPage = await wpCreatePage({
  title: "AC Repair Services in Atlanta",
  slug: "ac-repair-services",
  content: linkedContent, // HTML from linking phase
  status: "publish",
  parent: 0, // Top-level page
  template: "page-authority-hub.php",
  meta: {
    yoast_title: "AC Repair Atlanta | Cool Air HVAC",
    yoast_metadesc: "Expert AC repair in Atlanta...",
    focus_keyword: "AC repair Atlanta",
    schema_type: "Service"
  }
});

console.log(`✓ Created: ${authorityPage.url}`);
```

**Knowledge Pages Creation** (Children):
```javascript
// Create Knowledge pages as children
hub.knowledgePages.forEach(async (page) => {
  const knowledgePage = await wpCreatePage({
    title: page.title,
    slug: page.slug,
    content: page.linkedContent,
    status: "publish",
    parent: authorityPage.id, // Child of Authority
    template: "page-knowledge.php",
    meta: {
      yoast_title: page.seoTitle,
      yoast_metadesc: page.metaDescription,
      focus_keyword: page.keyword
    }
  });
  
  console.log(`  ✓ Created: ${knowledgePage.url}`);
});
```

**Answer Pages Creation** (Children):
```javascript
// Create Answer pages as children
hub.answerPages.forEach(async (page) => {
  const answerPage = await wpCreatePage({
    title: page.question, // Exact question as title
    slug: page.slug,
    content: page.linkedContent,
    status: "publish",
    parent: authorityPage.id, // Child of Authority
    template: "page-answer.php",
    meta: {
      yoast_title: page.seoTitle,
      yoast_metadesc: page.metaDescription,
      schema_type: "FAQPage"
    }
  });
  
  console.log(`  ✓ Created: ${answerPage.url}`);
});
```

**Deployment Progress**:
```
🏛️ Deploying Hub 1 to WordPress...

Authority Hub:
✓ Created: /ac-repair-services/ (ID: 123)

Knowledge Pages (15):
✓ 1/15 Created: /ac-repair-services/ac-not-cooling/
✓ 2/15 Created: /ac-repair-services/refrigerant-leak-repair/
✓ 3/15 Created: /ac-repair-services/compressor-replacement/
...
✓ 15/15 Created: /ac-repair-services/emergency-ac-repair/

Answer Pages (25):
✓ 1/25 Created: /ac-repair-services/how-much-ac-repair-cost/
✓ 2/25 Created: /ac-repair-services/why-ac-not-cooling/
...
✓ 25/25 Created: /ac-repair-services/can-i-diy-ac-repair/

Total: 41 pages created in 3 minutes
```

### Step 4: Navigation Menu Creation

**Hub Navigation Menu**:
```javascript
// Create menu for Hub 1
const hubMenu = await wpCreateMenu({
  name: "Hub 1: AC Repair",
  location: "hub-1-sidebar",
  items: [
    {
      type: "page",
      id: authorityPage.id,
      title: "Overview"
    },
    {
      type: "custom",
      title: "Knowledge Base",
      url: "#",
      children: hub.knowledgePages.map(p => ({
        type: "page",
        id: p.wpId,
        title: p.title
      }))
    },
    {
      type: "custom",
      title: "Common Questions",
      url: "#",
      children: hub.answerPages.slice(0, 10).map(p => ({
        type: "page",
        id: p.wpId,
        title: p.question
      }))
    }
  ]
});
```

**Main Site Menu** (if deploying all hubs):
```javascript
const mainMenu = await wpCreateMenu({
  name: "Primary Navigation",
  location: "primary",
  items: [
    { title: "Home", url: "/" },
    {
      title: "Services",
      children: strategy.hubs.map(hub => ({
        type: "page",
        id: hub.authorityPage.wpId,
        title: hub.hubName
      }))
    },
    { title: "About", url: "/about/" },
    { title: "Contact", url: "/contact/" }
  ]
});
```

### Step 5: SEO Metadata & Schema

**For Each Page**:

**SEO Metadata** (via Yoast/Rank Math):
```javascript
await wpUpdatePageMeta(pageId, {
  // Title tag
  '_yoast_wpseo_title': '{{TITLE}} | {{BUSINESS_NAME}}',
  
  // Meta description
  '_yoast_wpseo_metadesc': '{{META_DESCRIPTION}}',
  
  // Focus keyword
  '_yoast_wpseo_focuskw': '{{PRIMARY_KEYWORD}}',
  
  // Canonical URL
  '_yoast_wpseo_canonical': page.url,
  
  // Open Graph
  '_yoast_wpseo_opengraph-title': page.title,
  '_yoast_wpseo_opengraph-description': page.metaDescription,
  
  // Twitter Card
  '_yoast_wpseo_twitter-title': page.title,
  '_yoast_wpseo_twitter-description': page.metaDescription
});
```

**Schema Markup**:

**Authority Page** (Service + LocalBusiness):
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{{PRIMARY_SERVICE}}",
  "provider": {
    "@type": "LocalBusiness",
    "name": "{{BUSINESS_NAME}}",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "{{ADDRESS}}",
      "addressLocality": "{{CITY}}",
      "addressRegion": "{{STATE}}"
    },
    "telephone": "{{PHONE}}",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "500"
    }
  }
}
```

**Knowledge Page** (Article + HowTo):
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{PAGE_TITLE}}",
  "author": {
    "@type": "Organization",
    "name": "{{BUSINESS_NAME}}"
  }
}
```

**Answer Page** (FAQPage):
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "{{QUESTION}}",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "{{ANSWER_TEXT}}"
    }
  }]
}
```

### Step 6: Permalink Configuration

**Set Permalink Structure**:
```javascript
// Ensure proper URL structure
await wpSetPermalinks({
  structure: '/%postname%/', // Clean URLs
  category_base: '',
  tag_base: ''
});
```

**Result**:
- `/ac-repair-services/` (Authority)
- `/ac-repair-services/ac-not-cooling/` (Knowledge)
- `/ac-repair-services/how-much-cost/` (Answer)

### Step 7: Breadcrumb Setup

**Configure Yoast Breadcrumbs**:
```javascript
// For Knowledge/Answer pages
Home > AC Repair Services > AC Not Cooling Troubleshooting

// Breadcrumb structure from parent-child
await wpSetBreadcrumbs({
  enabled: true,
  separator: '>',
  home_text: 'Home',
  prefix: '',
  archiveprefix: '',
  searchprefix: 'Search for'
});
```

## Dry Run Mode

**When `--dry-run` specified**:

```
🏛️ DRY RUN: Previewing Hub 1 Deployment

Would create:
✓ Authority: /ac-repair-services/
  Title: AC Repair Services in Atlanta
  Parent: None (top-level)
  Template: page-authority-hub.php
  
✓ Knowledge: /ac-repair-services/ac-not-cooling/
  Title: AC Not Cooling Troubleshooting
  Parent: AC Repair Services (ID would be created)
  Template: page-knowledge.php
  
... [Preview all 41 pages]

Would create navigation menu: "Hub 1: AC Repair"
Would set SEO metadata for all pages
Would add schema markup

Total: 41 pages would be created

→ No actual changes made
→ Run without --dry-run to deploy
```

## Error Handling

**Page Creation Failure**:
```
⚠️ Error creating page: AC Compressor Replacement

Error: Duplicate slug detected
Suggestion: Page may already exist

Options:
1. Run with --update to update existing page
2. Change slug in strategy
3. Delete existing page manually

→ Continuing with remaining pages...
```

**WordPress Connection Lost**:
```
❌ WordPress connection lost during deployment

Status:
✓ Created: 15/41 pages
✗ Failed: 26 pages remaining

→ Safe to retry - existing pages won't duplicate
→ Run: aka-wireframe-wp deploy --hub 1 --resume
```

## Update Mode

**When `--update` specified**:

```
→ Update mode: Modifying existing pages

✓ Updated: /ac-repair-services/ (ID: 123)
✓ Updated: /ac-repair-services/ac-not-cooling/ (ID: 124)
...

Note: Parent-child relationships preserved
Note: URLs unchanged
Note: SEO metadata updated
```

## Deployment Report

**Generated File**: `generated-content/hub-1/deployment-report.md`

```markdown
# Deployment Report - Hub 1

## Summary
- Deployment time: 3 minutes
- Pages created: 41
- Pages failed: 0
- WordPress URL: http://localhost:8080

## Pages Deployed

### Authority Hub
- Title: AC Repair Services in Atlanta
- URL: http://localhost:8080/ac-repair-services/
- ID: 123
- Status: Published ✓

### Knowledge Pages (15)
1. AC Not Cooling Troubleshooting
   URL: .../ac-not-cooling-troubleshooting/
   ID: 124
   
2. AC Refrigerant Leak Repair
   URL: .../refrigerant-leak-repair/
   ID: 125
   
... [all 15]

### Answer Pages (25)
1. How much does AC repair cost?
   URL: .../how-much-ac-repair-cost/
   ID: 140
   
... [all 25]

## Navigation
- Hub menu created: "Hub 1: AC Repair"
- Breadcrumbs configured ✓

## SEO
- Meta titles: 41/41 ✓
- Meta descriptions: 41/41 ✓
- Focus keywords: 41/41 ✓
- Schema markup: 41/41 ✓

## Next Steps
✓ Hub 1 is live and ready!
→ View: http://localhost:8080/ac-repair-services/
→ Next: Deploy Hub 2
```

## Integration with Other Droids

**Receives from aka-internal-linker**:
- Content with working HTML links
- No broken links
- Ready for deployment

**Provides to aka-seo-optimizer**:
- Live WordPress URLs
- Page IDs for optimization
- Structure for validation

## Success Criteria

✅ All pages deployed successfully
✅ Parent-child hierarchy correct
✅ Navigation menus created
✅ SEO metadata complete
✅ Schema markup added
✅ Permalinks configured
✅ Breadcrumbs working
✅ Theme active and styled
✅ All links working

## Notes

- Uses WordPress REST API (requires WordPress 4.7+)
- Requires app password or basic auth
- Handles large batch deployments efficiently
- Preserves existing content when updating
- Safe to retry on failure
- Dry run prevents accidental deployments

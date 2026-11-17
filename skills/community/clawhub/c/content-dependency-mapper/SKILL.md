---
name: Map Content Dependencies Across Multiple Sources Automatically
description: "Map hidden dependencies across your content library to identify critical assets, orphaned content, and strategic clusters. Use when the user needs content audit insights, editorial prioritization, or content fragility analysis for strategic planning."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","CONTENT_SOURCE_URL"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🗺️"}}
---

## Overview

**Content Dependency Mapper** is an enterprise-grade research skill that performs deep structural analysis of your entire content library to uncover hidden relationships, traffic flows, and criticality patterns. Unlike surface-level content audits, this skill maps the *actual dependencies* between your assets—revealing which blog posts funnel users to premium offers, which tutorial videos are prerequisites for course comprehension, which guides get cited in sales materials, and which pieces carry disproportionate weight in your content ecosystem.

### Why This Matters

Most content teams operate blindly, publishing in silos without understanding:
- **Content Fragility**: Which orphaned assets drain resources with no business impact
- **Bottleneck Posts**: Which pieces handle too much internal link traffic and need decomposition
- **Cluster Opportunities**: Which content could be strategically bundled for higher conversion
- **Criticality Hierarchy**: What should be updated first when priorities shift

This skill generates:
- **Dependency Graphs** (visual JSON/DOT format) showing content relationships
- **Content Criticality Scores** (1-100) ranking assets by strategic impact
- **Cluster Recommendations** suggesting content bundling opportunities
- **Fragility Reports** identifying orphaned/underperforming assets
- **Editorial Roadmaps** prioritizing which content drives measurable outcomes

### Supported Integrations

Works with WordPress, HubSpot, Medium, Substack, Notion, Ghost, static site generators, Google Analytics, Segment, and any content source accessible via API or CSV export.

---

## Quick Start

### Example 1: Analyze WordPress Content Library

```
Analyze my WordPress blog at example.com/wp-json/wp/v2/posts 
and map all content dependencies including:
- Internal linking patterns
- Time-on-page metrics
- Click-through rates to conversion pages
- Content cluster recommendations

Output a dependency graph showing which posts drive traffic 
to my core offer (/pricing).
```

### Example 2: Identify Critical Content Assets

```
I have a Notion database with 200+ articles, guides, and videos 
at https://api.notion.com/v1/databases/[DB_ID]/query.

Create a Content Criticality Score for each asset that factors in:
- Inbound links from other content
- Traffic volume from Google Analytics
- Conversion impact (links to sales pages)
- Time investment required to maintain

Flag the top 15 "overworked" pieces that receive too many internal 
links and should be split into smaller, focused pieces.
```

### Example 3: Detect Orphaned Content & Fragility Issues

```
Audit my 150-post blog for content fragility:
- Posts with zero inbound links (orphaned)
- Content gaps (topics mentioned but not covered)
- Duplicate or near-duplicate articles
- Outdated posts still driving traffic but missing updates

Suggest which low-impact posts should be consolidated, 
which should be deleted, and which need refreshing.
```

---

## Capabilities

### 1. Dependency Graph Generation

Maps all content relationships through:
- **Explicit Links**: Parsed HTML/Markdown internal links
- **Semantic Links**: AI-detected topical relationships (e.g., "this post explains a concept mentioned in that video")
- **Conversion Funnels**: Tracks user journey from discovery content → engagement content → conversion content
- **Cross-Format Detection**: Identifies when blog posts, videos, podcasts, and guides reference each other

**Output formats**: JSON, GraphML (Gephi/Cytoscape compatible), DOT (Graphviz), or interactive HTML visualization.

```json
{
  "nodes": [
    {
      "id": "post-42",
      "title": "Getting Started with REST APIs",
      "url": "/blog/rest-apis-intro",
      "criticality_score": 87,
      "inbound_links": 23,
      "outbound_links": 8,
      "traffic_volume": 4230,
      "conversion_rate": 0.12
    }
  ],
  "edges": [
    {
      "source": "post-42",
      "target": "course-101",
      "link_type": "prerequisite",
      "weight": 0.95,
      "click_through_rate": 0.34
    }
  ]
}
```

### 2. Content Criticality Scoring

Evaluates each asset on:
- **Inbound Traffic Impact** (30%): How much traffic flows through this piece
- **Downstream Conversion Influence** (25%): How many users reach offers after visiting
- **Structural Importance** (25%): How many other pieces depend on it
- **Maintenance Cost** (15%): Time/effort required to keep current
- **Recency Factor** (5%): Last update timestamp

Scores range 1-100. Assets 75+ are strategic priorities; below 30 are candidates for consolidation or deletion.

### 3. Cluster Detection & Bundling

Identifies content clusters—groups of related pieces that should be:
- Bundled into guides or bundles
- Reorganized into a pillar/cluster model
- Converted into courses
- Cross-promoted

Uses semantic similarity + linking patterns to surface opportunities.

### 4. Fragility & Gap Analysis

Detects:
- **Orphaned Assets**: Zero inbound links, not cited elsewhere
- **Bottleneck Posts**: Overlinked (>50 internal links) and due for decomposition
- **Content Gaps**: Topics mentioned without dedicated coverage
- **Outdated Dependencies**: Posts linking to unmaintained resources
- **Redundancy**: Near-duplicate content competing for SEO/discovery

### 5. Editorial Prioritization Roadmap

Generates actionable recommendations:
- **Update First**: High-criticality, out-of-date content
- **Split Up**: Overworked pieces handling too many internal links
- **Delete/Merge**: Low-criticality orphaned content
- **Promote**: Underlinked high-value pieces deserving visibility
- **Create**: Identified gaps in your content structure

---

## Configuration

### Required Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # For semantic analysis
export CONTENT_SOURCE_URL="https://..."  # Your content API/export
export GOOGLE_ANALYTICS_TOKEN="..."      # Optional: Traffic metrics
export CONVERSION_PAGE_URLS="..."        # Comma-separated: /pricing,/signup
```

### Setup Instructions

1. **Export Your Content**:
   - WordPress: Use REST API or plugin export
   - HubSpot: Via Blogs API
   - Notion: Database export or API key
   - Static Sites: Crawl with Screaming Frog or Hugo build output
   - CSV Format: Title, URL, Content, Last Updated, Traffic Volume

2. **Connect Analytics** (optional but recommended):
   ```bash
   gcloud auth application-default login
   # or
   aws configure
   ```

3. **Define Conversion Pages**:
   ```bash
   export CONVERSION_PAGE_URLS="/pricing,/book-demo,/checkout,/waitlist"
   ```

4. **Run Analysis**:
   ```bash
   openclaw run content-dependency-mapper \
     --source wordpress \
     --domain example.com \
     --output-format json,html,dot \
     --include-analytics true
   ```

### Optional Parameters

- `--min-link-weight 0.2`: Exclude weak semantic links (0-1 scale)
- `--cluster-threshold 0.6`: Tighten/loosen cluster detection
- `--include-semantics true`: Enable AI-powered semantic linking (slower, more thorough)
- `--compare-versions`: Track changes over time (requires historical snapshots)

---

## Example Outputs

### Content Criticality Report

```
TOP 15 CRITICAL ASSETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. post-101: "Setup Guide for Beginners"           | Score: 94
   └─ Drives 8,342 visits/month → 23 course signups
   └─ Referenced by 18 internal posts + email campaigns
   
2. video-23: "5-Minute Product Demo"               | Score: 91
   └─ 12,100 views, 34% CTR to /pricing
   └─ Prerequisite for 6 advanced tutorials

3. guide-5: "API Reference Documentation"          | Score: 89
   └─ 156 inbound links from engineering content
   └─ Critical infrastructure asset

OVERWORKED POSTS (>50 internal links - consider splitting)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• post-42 "Intro to Concept X" — 67 internal links
  → Recommend: Split into "Core," "Advanced," "Troubleshooting"

ORPHANED ASSETS (0 inbound links - consider consolidating)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• post-203 "Obsolete Feature Overview"    | 23 visits/month
• video-88 "Conference Talk Excerpt"      | 4 visits/month
  → Recommendation: Consolidate into guides or delete
```

### Dependency Graph (Visual Format)

```
digraph ContentDependencies {
  rankdir=LR;
  
  "Guide: Getting Started" -> "Tutorial: Setup";
  "Tutorial: Setup" -> "Course: 201" [label="prerequisite"];
  "Blog: Tips" -> "Pricing Page" [color=red, penwidth=3];
  "Video: Demo" -> "Pricing Page" [color=red];
  
  subgraph cluster_0 {
    label = "Email Nurture Cluster";
    "Email Seq 1" -> "Blog: Intro";
    "Blog: Intro" -> "Email Seq 2";
  }
}
```

### Cluster Recommendation

```
SUGGESTED CONTENT BUNDLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cluster A: "Advanced API Usage" (Similarity: 0.89)
  • blog-32: "Authentication Deep Dive"
  • guide-11: "OAuth 2.0 Implementation"
  • video-45: "Security Best Practices"
  → Action: Bundle into a "Master Guide" + add 1 new piece
     on "Common Security Mistakes"

Cluster B: "Ecommerce Integration" (Similarity: 0.84)
  • course-12: "Shopify Integration 101"
  • tutorial-88: "WooCommerce Setup"
  • case-study-5: "Fashion Brand Scaling"
  → Action: Create a comparison guide + cross-promote
```

---

## Tips & Best Practices

### 1. Start with a Content Inventory

Export your full content library (title, URL, publish date, traffic) before running the mapper. This skill performs *better* with complete data—even low-traffic orphaned posts reveal important gaps.

### 2. Connect Google Analytics for Accuracy

Traffic volume, time-on-page, and bounce rate dramatically improve criticality scoring. Without it, the mapper relies on linking patterns alone (still valuable, but less nuanced).

### 3. Define Your "Conversion Funnel"

Explicitly list pages you consider "conversions" (pricing page, signup, demo request, etc.). The mapper will trace how much traffic each content piece ultimately drives to these endpoints.

```bash
export CONVERSION_PAGE_URLS="/pricing,/demo,/book-call,/checkout"
```

### 4. Run Quarterly Audits

Content dependencies shift as you publish, update, and archive. Run this skill every 3 months to catch:
- New bottlenecks emerging
- Orphaned posts (indicators of strategy drift)
- Cluster opportunities growing larger
- Outdated internal linking patterns

### 5. Use Criticality Scores for Editorial Calendar

Instead of arbitrary priority, let criticality scores guide your content refresh cycles:
- **Scores 85+**: Update within 30 days
- **Scores 70-84**: Update within 60 days
- **Scores 50-69**: Update annually
- **Scores <50**: Consolidate or archive

### 6. Investigate Surprising Dependencies

When the mapper surfaces an unexpected link (e.g., a random blog post driving premium course signups), investigate why. This often reveals hidden user behavior that should inform your content strategy.

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Make Editorial Decisions For You**: Criticality scores are *data*, not mandates. Never delete content purely on score alone—consider brand voice, SEO equity, and strategic fit.
- **Analyze Private/Confidential Content**: Requires explicit data export; does not crawl or scrape without permission.
- **Guarantee Traffic or Conversion Improvements**: Dependency mapping reveals structure, not causality. Dependencies are correlations, not guarantees.
- **Access Third-Party Analytics Without OAuth**: Requires explicit API token or OAuth connection; will not bypass authentication.

### Limitations

1. **Semantic Linking Accuracy**: AI-powered semantic linking achieves ~85% accuracy. Manual review recommended for critical decisions.
2. **Historical Data**: Requires content timestamps and traffic data. Older posts without analytics will show lower criticality (even if strategically important).
3. **Multi-Language Content**: Works best with single-language libraries; cross-language linking may be undercounted.
4. **Dynamic/Personalized Content**: Cannot analyze content shown conditionally to logged-in users or based on personalization rules.
5. **Orphaned vs. Intentional**: Some "orphaned" content is intentionally standalone (e.g., thank-you pages, legal). Review before deleting.

### Data Privacy & Security

- All analysis happens locally; no content is sent to external servers (except OpenAI API for semantic analysis).
- Requires explicit API credentials; does not store credentials.
- Outputs are in your environment only; not shared with ClawHub or third parties.

---

## Troubleshooting

### Q: "No dependencies found. Skill returned empty graph."

**Causes**:
- Content has no internal links (unusual for most sites)
- Content source URL is incorrect or API credentials are invalid
- API response is in unexpected format

**Solutions**:
1. Verify API token: `curl -H "Authorization: Bearer $CONTENT_SOURCE_URL" https://api.example.com/posts`
2. Check content format: Skill expects `url`, `title`, `content` fields at minimum
3. Enable verbose logging: `--debug true`

### Q: "Criticality scores seem off. My top post scored 45, but it generates lots of sales."

**Cause**: Skill may not have access to conversion tracking data.

**Solution**: Connect Google Analytics or Segment to include conversion metrics:
```bash
export GOOGLE_ANALYTICS_4_PROPERTY_ID="G-XXXXX"
export CONVERSION_PAGE_URLS="/pricing,/checkout"
```

### Q: "Too many cluster recommendations. How do I prioritize?"

**Solution**: Filter by similarity threshold and cluster size:
```bash
openclaw run content-dependency-mapper \
  --cluster-threshold 0.8 \      # Tighten clusters
  --min-cluster-size 3 \          # Only groups of 3+
  --output-format json > clusters.json
```

### Q: "Semantic linking detected false positives (unrelated posts grouped together)."

**Cause**: AI model may misinterpret similar keywords across different contexts.

**Solution**: 
1. Lower semantic linking weight: `--min-link-weight 0.3`
2. Disable semantic linking entirely: `--include-semantics false` (uses explicit links only)
3. Manually review high-confidence links in output

### Q: "How often should I run this analysis?"

**Recommendation**: Quarterly for active content teams (10+ posts/month); semi-annually for slower publishers.

Track changes between runs:
```bash
openclaw run content-dependency-mapper \
  --compare-versions true \
  --previous-snapshot snapshot-q2-2024.json
```

### Q: "Can I export the dependency
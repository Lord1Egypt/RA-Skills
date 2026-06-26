---
name: Automated Asset Tracking Workflow with Slack Notifications & Google Sheets Updates
description: "Organize and store digital assets across cloud providers with automated workflows. Use when the user needs DAM integration, file organization, or asset metadata management for creative teams."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["ASSETFLOW_DAM_API_KEY", "ASSETFLOW_STORAGE_PROVIDER", "ASSETFLOW_WORKSPACE_ID"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

## Overview

AssetFlow is a production-ready Digital Asset Management (DAM) orchestration skill that automates the organization, storage, and retrieval of digital assets across multiple cloud platforms and DAM systems. It eliminates manual file management overhead, ensures consistent metadata tagging, and integrates seamlessly with existing creative workflows.

### Why AssetFlow Matters

Creative teams lose 30-40% of productivity managing dispersed assets across drives, cloud storage, and project folders. AssetFlow centralizes asset management with:

- **Automated Organization**: Files are sorted by type, project, date, or custom taxonomy without manual intervention
- **Multi-Provider Integration**: Works with AWS S3, Google Drive, Azure Blob Storage, Dropbox, Box, and native DAM platforms (Adobe Experience Manager, Widen Collective, Canto)
- **Intelligent Metadata**: Auto-generates and applies tags, descriptions, and version tracking
- **Custom Workflows**: Define organization rules for photos, video, design files, documents, and more
- **Access Control**: Team-based permissions and approval workflows
- **Search & Discovery**: AI-powered asset discovery by content, tags, or natural language queries

---

## Quick Start

Try these example prompts immediately:

### Example 1: Organize Marketing Assets
```
Organize all marketing materials from our Q4 campaign. 
Automatically sort by asset type (images, videos, PDFs), 
create project folders for each channel (social, email, web), 
and tag with campaign name, brand guidelines compliance, and 
expiration dates. Store in AWS S3 /marketing/Q4_2024 bucket.
```

### Example 2: Set Up Photo Archive Workflow
```
Create an automated workflow for our photography team. 
Ingest RAW files from Dropbox upload folder, auto-tag by 
photographer and location metadata, generate thumbnails, 
create proof sets, and move finalized images to archive 
in Google Drive. Flag images that need licensing info.
```

### Example 3: DAM System Sync
```
Sync all approved design files from our Figma workspace 
to our Adobe Experience Manager DAM. Create asset collections 
by brand, design system version, and usage rights. Auto-generate 
previews and maintain version history. Alert team when assets 
are updated or deprecated.
```

### Example 4: Compliance & Retention
```
Implement automatic compliance workflow: tag all assets with 
creation date, creator, usage rights, and expiration. Archive 
assets older than 2 years to cold storage. Generate compliance 
reports monthly. Flag any files missing required metadata.
```

---

## Capabilities

### Automated Asset Organization

- **Intelligent Sorting**: Classify files by type, date, project, or custom rules
- **Folder Structure Generation**: Create hierarchical organization matching your taxonomy
- **Batch Tagging**: Apply metadata at scale using pattern matching and AI
- **Version Control**: Track asset versions and maintain previous iterations
- **Duplicate Detection**: Identify and consolidate redundant assets

### Multi-Provider Integration

| Provider | Capability | Status |
|----------|-----------|--------|
| AWS S3 | Full read/write, lifecycle policies | ✅ Native |
| Google Drive | Folder management, sharing control | ✅ Native |
| Dropbox | Auto-ingest, selective sync | ✅ Native |
| Azure Blob | Archive storage, retention policies | ✅ Native |
| Adobe Experience Manager | DAM sync, metadata standards | ✅ API Integration |
| Canto | Asset collections, approval workflows | ✅ API Integration |
| Widen Collective | Brand management, usage rights | ✅ API Integration |
| Slack | Asset notifications, quick share | ✅ Webhook Integration |

### Metadata & Searchability

- **Auto-Generated Tags**: AI extracts subjects, objects, colors, and content type
- **Custom Metadata Schema**: Define fields (brand, campaign, usage rights, expiration)
- **Optical Character Recognition**: Extract text from images and documents
- **Face & Object Detection**: Automatically catalog people, locations, products
- **Natural Language Search**: "Find all winter campaign images with snow and people"

### Workflow Automation

- **Approval Chains**: Route assets requiring review to designated stakeholders
- **Scheduled Jobs**: Organize assets on a daily, weekly, or monthly cadence
- **Conditional Logic**: Apply different rules based on file type, size, or source
- **Notifications**: Alert teams via email or Slack when assets are organized, approved, or deprecated
- **Bulk Operations**: Process thousands of assets in a single batch

### Access & Permissions

- **Role-Based Access**: Assign viewer, editor, or admin permissions by team
- **Watermarking**: Automatically watermark preview assets
- **Download Tracking**: Log who accessed which assets and when
- **Expiring Links**: Create time-limited share links for external stakeholders
- **Audit Trails**: Full history of who modified or accessed each asset

---

## Configuration

### Environment Variables (Required)

```bash
# Primary DAM or storage provider authentication
ASSETFLOW_DAM_API_KEY="your-dam-api-key"
ASSETFLOW_STORAGE_PROVIDER="s3"  # Options: s3, gcs, azure, dropbox, box
ASSETFLOW_WORKSPACE_ID="workspace-12345"

# AWS S3 (if using S3)
AWS_ACCESS_KEY_ID="your-aws-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret"
AWS_REGION="us-east-1"

# Google Cloud (if using Google Drive)
GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Secondary integrations (optional)
ADOBE_XDM_API_KEY="adobe-api-key"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Setup Instructions

**Step 1: Choose Your Primary Provider**
```
Supported configurations:
- AWS S3 + Adobe Experience Manager
- Google Drive + Canto DAM
- Dropbox + Widen Collective
- Azure Blob Storage + custom metadata
```

**Step 2: Define Asset Organization Schema**
```yaml
# Example taxonomy for marketing team
organization_rules:
  by_type:
    - images/
      - hero/
      - social/
      - email/
    - video/
      - shorts/
      - long-form/
    - documents/
      - brand-guidelines/
      - campaign-briefs/
  
  by_project:
    - [BRAND]_[QUARTER]_[CAMPAIGN_NAME]/
    - metadata_tags: [brand, quarter, campaign]
  
  retention_policy:
    approved_assets: "indefinite"
    drafts: "30 days"
    archival: "7 years cold storage"
```

**Step 3: Configure Metadata Templates**
```yaml
# Required fields for all assets
metadata_template:
  core:
    - created_date (auto)
    - creator (auto)
    - asset_type (auto-detected)
    - usage_rights (required)
    - expiration_date (if applicable)
  
  custom:
    - brand
    - campaign
    - approved_by
    - version
    - file_format_quality
```

**Step 4: Enable Integrations**
```
Slack notifications: Enable to post asset updates to team channels
Email digests: Weekly summary of new, modified, and archived assets
Webhook endpoints: For triggering external workflows
API access: For custom integrations with your tools
```

---

## Example Outputs

### Output 1: Asset Organization Report
```
AssetFlow Organization Complete ✅

📊 Summary:
- Files Processed: 4,892
- Files Organized: 4,721 (96.5%)
- Errors: 171 (flagged for review)
- Time: 23 minutes

📁 Folder Structure Created:
marketing/
├── 2024/
│   ├── Q1_Launch/
│   │   ├── images/ (1,203 files)
│   │   ├── video/ (87 files)
│   │   └── documents/ (45 files)
│   └── Q2_Growth/
│       ├── images/ (892 files)
│       ├── video/ (156 files)
│       └── documents/ (234 files)

🏷️ Metadata Applied:
- Tags: 14,832 (avg 3.2 per asset)
- Descriptions: 4,721 auto-generated
- Usage Rights: 4,703 classified
- Expiration Dates: 892 flagged

⚠️ Requires Review:
- Missing Creator Info: 87 files
- Unclear Usage Rights: 56 files
- Potential Duplicates: 28 files
```

### Output 2: DAM Sync Status
```
Adobe Experience Manager Sync: IN PROGRESS

Files Synced: 1,234 / 1,456
Success Rate: 84.8%

✅ Completed Syncs:
- Brand Assets (2024): 456 files
- Design System v3.2: 223 files
- Campaign Templates: 189 files

🔄 In Progress:
- Video Archive: 156 files (12 minutes remaining)
- Historical Assets: 892 files (35 minutes remaining)

⚠️ Failed Syncs (Requires Action):
- metadata_mismatch.zip: 12 files
  → Solution: Re-map custom metadata fields

Next Steps:
1. Review failed sync report
2. Update Adobe XDM schema if needed
3. Retry failed files (automatic retry in 2 hours)
```

### Output 3: Asset Search Result
```
🔍 Search Results: "winter campaign social media"

Found 347 assets matching your criteria

📸 Top Results:

1. winter_campaign_instagram_1.jpg
   Size: 1.2 MB | Created: 2024-01-15
   Tags: winter, campaign, instagram, carousel
   Status: Approved ✅
   Downloads: 23

2. winter_campaign_tiktok_15s.mp4
   Size: 45 MB | Created: 2024-01-18
   Tags: winter, campaign, tiktok, short-form
   Status: Approved ✅
   Downloads: 18

3. winter_campaign_twitter_hero.png
   Size: 2.8 MB | Created: 2024-01-12
   Tags: winter, campaign, twitter, hero
   Status: In Review ⏳
   Downloads: 5

[View all 347 results] [Save Search] [Create Collection]
```

---

## Tips & Best Practices

### For Maximum Organization Efficiency

1. **Establish Clear Naming Conventions Early**
   - Use consistent format: `[BRAND]_[DATE]_[PROJECT]_[TYPE]_[VERSION]`
   - Example: `ACME_2024-Q1_Newsletter_Header_v3.psd`
   - AssetFlow will auto-parse and apply metadata from filenames

2. **Leverage Automated Workflows**
   - Set up ingest workflows for recurring uploads (e.g., daily photo drops)
   - Use conditional rules to route assets based on type or size
   - Schedule organization jobs during off-hours to avoid performance impact

3. **Implement Approval Workflows Early**
   - Create approval chains for brand assets and customer-facing materials
   - Use Slack notifications to keep review cycles tight (target: 24-hour approval)
   - Archive rejected assets in a separate folder for reference

4. **Maintain Metadata Discipline**
   - Require usage rights metadata before assets can be marked "approved"
   - Set expiration dates on trend-based or campaign-specific assets
   - Use tags for cross-project discovery (e.g., "client_XYZ", "summer_2024")

5. **Monitor Storage & Costs**
   - Review storage usage monthly; archive cold assets to cheaper tier
   - Set up lifecycle policies to move assets to cold storage after 2+ years
   - Use preview versions to reduce bandwidth for large files

6. **Optimize Search Experience**
   - Regularly review and refine your taxonomy based on search patterns
   - Create saved searches for frequently requested asset types
   - Use object detection tags to improve discoverability of visual content

---

## Safety & Guardrails

### What AssetFlow Will NOT Do

- **No Data Modification**: AssetFlow organizes and tags—it never alters file contents
- **No Unauthorized Sharing**: Respects original file permissions; cannot grant access users don't already have
- **No Sensitive Data Indexing**: Skips files containing PII, passwords, or encrypted content
- **No Creative Decisions**: Does not modify, edit, or reinterpret assets (e.g., no cropping, resizing, or color correction)
- **No Compliance Interpretation**: Does not automatically determine legal usage rights; flags for human review

### Boundaries & Limitations

| Limitation | Details | Mitigation |
|-----------|---------|-----------|
| File Size | Max individual file: 10 GB | Split large videos; compress RAW batches |
| API Rate Limits | 1,000 requests/minute per provider | Batch jobs during off-peak hours |
| Metadata Fields | Max 100 custom fields per asset | Use tagging system for additional classification |
| Search Indexing | Indexes file names, metadata, OCR; not full content | Use clear naming conventions |
| Concurrent Operations | Max 50 concurrent file operations | Monitor batch job queue |

### Privacy & Compliance

- **GDPR**: AssetFlow respects deletion requests; audit trails retained 90 days
- **SOC 2 Type II**: Encrypted in transit (TLS 1.3) and at rest (AES-256)
- **HIPAA**: Not suitable for PHI storage; consult compliance team before use
- **Data Residency**: Supports region-specific storage (EU, US, APAC)

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "Authentication Failed" Error**

```
Error: ASSETFLOW_DAM_API_KEY is invalid or expired

Solution:
1. Verify API key in your provider dashboard (AWS/Google/Adobe)
2. Check key expiration date
3. Regenerate key if needed
4. Update environment variable: export ASSETFLOW_DAM_API_KEY="new-key"
5. Test connection: assetflow test-connection
```

**Issue: Files Not Organizing Correctly**

```
Problem: Assets ending up in wrong folders

Troubleshooting:
1. Review your organization_rules YAML for typos or logic errors
2. Check file extensions match your rules (case-sensitive on Linux)
3. Verify metadata extraction is working:
   → assetflow debug --inspect-metadata [filename]
4. If using AI-based sorting, check confidence scores:
   → assetflow list-low-confidence --threshold 0.7
5. Manually correct folder assignments and retrain model

Prevention: Start with simple rules (by type, then by date) 
and gradually add complexity.
```

**Issue: Slow Organization Performance**

```
Symptom: Processing 10,000+ assets takes hours

Optimization Steps:
1. Reduce concurrent operations: 
   → assetflow organize --batch-size 25 --concurrency 10
2. Disable AI tagging for initial run (enable after):
   → assetflow organize --skip-ai-tags
3. Split into smaller batches by date or folder
4. Check for network latency to cloud storage:
   → ping your-bucket-region.amazonaws.com
5. Consider running during off-peak hours (2-6 AM)

Expected Performance:
- Local SSD storage: ~1,000 files/minute
- Cloud storage (S3/GCS): ~200-400 files/minute
- With AI tagging: ~50-100 files/minute
```

**Issue: Duplicate Assets Not Being Detected**

```
Problem: Similar or identical files scattered across folders

Debug:
1. Check duplicate detection is enabled:
   → assetflow config --show | grep duplicate
2. Review hash algorithm (MD5 for exact, perceptual for similar):
   → assetflow organize --duplicate-method perceptual
3. Adjust similarity threshold (0-100, default 85):
   → assetflow organize --similarity-
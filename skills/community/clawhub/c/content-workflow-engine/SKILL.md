---
name: content-workflow-engine
description: "Automate content creation, management, and distribution workflows. Use when: (1) Creating content pipelines for blogs, social media, or newsletters, (2) Scheduling and automating content distribution, (3) Managing content calendars and editorial workflows, (4) Integrating AI content generation with publishing platforms, (5) Monitoring content performance and analytics. NOT for: Single one-off content pieces without automation needs, manual content creation without workflow orchestration."
metadata:
  { "openclaw": { "emoji": "📝", "requires": { "bins": ["curl", "git", "python3"] } } }
---

# Content Workflow Engine

Automate end-to-end content workflows from ideation to publication and distribution. This skill provides tools and patterns for creating scalable content pipelines that integrate AI generation, scheduling, publishing, and analytics.

## Quick Start

### Basic Content Pipeline

```bash
# Create a new content workflow
python3 scripts/create_workflow.py --name "blog-pipeline" --type "blog"

# Add stages to the workflow
python3 scripts/add_stage.py --workflow "blog-pipeline" --stage "ideation" --tool "ai-brainstorm"
python3 scripts/add_stage.py --workflow "blog-pipeline" --stage "writing" --tool "ai-writer"
python3 scripts/add_stage.py --workflow "blog-pipeline" --stage "editing" --tool "grammar-check"
python3 scripts/add_stage.py --workflow "blog-pipeline" --stage "publishing" --tool "wordpress"
python3 scripts/add_stage.py --workflow "blog-pipeline" --stage "distribution" --tool "social-media"

# Run the workflow
python3 scripts/run_workflow.py --workflow "blog-pipeline" --input "topic: AI content automation"
```

### Common Use Cases

1. **Blog Content Pipeline**: AI ideation → AI writing → SEO optimization → WordPress publishing → Social media sharing
2. **Social Media Calendar**: Content batching → Platform formatting → Scheduled posting → Engagement tracking
3. **Newsletter Workflow**: Content collection → Template filling → Email sending → Open rate monitoring
4. **Video Content Pipeline**: Script generation → Voice synthesis → Video editing → YouTube upload → Description optimization

## Workflow Decision Tree

Follow this decision tree to choose the right workflow pattern:

```
Start → What type of content?
├── Blog/Article → Need scheduling?
│   ├── Yes → Use "Scheduled Blog Pipeline" (references/scheduled_blog.md)
│   └── No → Use "Quick Blog Pipeline" (references/quick_blog.md)
├── Social Media → Multiple platforms?
│   ├── Yes → Use "Multi-Platform Social Pipeline" (references/social_multi.md)
│   └── No → Use "Single Platform Social Pipeline" (references/social_single.md)
├── Newsletter → Regular cadence?
│   ├── Yes → Use "Automated Newsletter Pipeline" (references/newsletter_auto.md)
│   └── No → Use "One-Off Newsletter Pipeline" (references/newsletter_oneoff.md)
└── Video/Audio → Complex editing?
    ├── Yes → Use "Advanced Video Pipeline" (references/video_advanced.md)
    └── No → Use "Simple Video Pipeline" (references/video_simple.md)
```

## Core Capabilities

### 1. Content Ideation & Planning
- **AI Brainstorming**: Generate content ideas based on keywords, trends, or audience
- **Content Calendar Management**: Schedule and organize content across platforms
- **Topic Research**: Gather information and sources for content creation

**Example: Generate blog ideas**
```bash
python3 scripts/brainstorm.py --topic "content automation" --count 10 --format "blog"
```

### 2. Content Creation & Generation
- **AI Writing Assistance**: Generate drafts, expand outlines, rewrite content
- **Multi-format Support**: Create content for blogs, social media, emails, scripts
- **Brand Voice Consistency**: Maintain consistent tone and style across content

**Example: Create blog post from outline**
```bash
python3 scripts/write_content.py --type "blog" --outline "references/outline_ai_content.md" --tone "professional"
```

### 3. Content Optimization
- **SEO Optimization**: Add keywords, meta descriptions, and optimize structure
- **Readability Scoring**: Improve content clarity and engagement
- **Platform-specific Formatting**: Adapt content for different platforms (Twitter, LinkedIn, etc.)

**Example: Optimize blog post for SEO**
```bash
python3 scripts/optimize_seo.py --input "draft.md" --keywords "content automation, AI writing, workflow"
```

### 4. Publishing & Distribution
- **Platform Integration**: Publish to WordPress, Medium, Substack, etc.
- **Social Media Scheduling**: Schedule posts across platforms
- **Email Newsletter Distribution**: Send to mailing lists

**Example: Publish to WordPress and schedule social media**
```bash
python3 scripts/publish.py --platform "wordpress" --content "final_post.md" --schedule "now"
python3 scripts/schedule_social.py --platforms "twitter,linkedin" --content "social_snippets.md" --schedule "tomorrow 9am"
```

### 5. Analytics & Monitoring
- **Performance Tracking**: Monitor views, engagement, conversions
- **A/B Testing**: Test different content variations
- **ROI Calculation**: Measure content effectiveness

**Example: Generate content performance report**
```bash
python3 scripts/analytics_report.py --period "last_30_days" --metrics "views,engagement,conversions"
```

## Workflow Templates

### Template 1: Automated Blog Pipeline
```
1. Ideation (Daily)
   - Scan trending topics in niche
   - Generate 5 article ideas
   - Select best based on keyword difficulty

2. Writing (AI-assisted)
   - Create detailed outline
   - Generate first draft
   - Expand with examples and data

3. Optimization
   - SEO optimization
   - Readability improvements
   - Add internal/external links

4. Publishing
   - Format for WordPress
   - Add featured image
   - Schedule publication

5. Distribution
   - Create social media snippets
   - Schedule across platforms
   - Add to newsletter queue
```

**Usage:**
```bash
python3 scripts/workflow_templates/blog_automated.py --topic "your niche" --frequency "weekly"
```

### Template 2: Social Media Content Batch
```
1. Content Planning (Weekly)
   - Plan weekly themes
   - Create content calendar
   - Assign content types (image, video, text)

2. Content Creation (Batch)
   - Create all posts for the week
   - Generate matching visuals
   - Write captions and hashtags

3. Scheduling
   - Upload to scheduling tool
   - Set optimal posting times
   - Add engagement prompts

4. Monitoring
   - Track engagement metrics
   - Respond to comments
   - Adjust future content
```

**Usage:**
```bash
python3 scripts/workflow_templates/social_batch.py --platforms "instagram,twitter,linkedin" --days 7
```

### Template 3: Newsletter Automation
```
1. Content Collection (Weekly)
   - Gather blog posts from the week
   - Select industry news
   - Add personal commentary

2. Template Filling
   - Use newsletter template
   - Insert content sections
   - Add personalization tokens

3. Testing & Sending
   - Send test to self
   - Check formatting
   - Schedule send time

4. Performance Tracking
   - Monitor open rates
   - Track click-throughs
   - Update subscriber segments
```

**Usage:**
```bash
python3 scripts/workflow_templates/newsletter_auto.py --source "blog_posts" --template "weekly_roundup"
```

## Integration Guide

### Supported Platforms

#### Publishing Platforms
- **WordPress**: REST API integration for automatic posting
- **Medium**: API for story creation and publishing
- **Substack**: Email-based newsletter distribution
- **Ghost**: Headless CMS API support

#### Social Media Platforms
- **Twitter/X**: API v2 for posting and scheduling
- **LinkedIn**: API for company/page posts
- **Facebook**: Graph API for page management
- **Instagram**: Basic Display API (limited automation)

#### Email Services
- **Mailchimp**: API for campaign management
- **ConvertKit**: API for email automation
- **SendGrid**: Transactional email API

#### Analytics Tools
- **Google Analytics**: Data API for performance tracking
- **Plausible**: Simple analytics API
- **Fathom**: Privacy-focused analytics

### API Configuration

Store API credentials in environment variables or config file:

```bash
# Example .env file
WORDPRESS_URL=https://yourblog.com/wp-json
WORDPRESS_USER=your_username
WORDPRESS_APP_PASSWORD=your_app_password

TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_secret

MAILCHIMP_API_KEY=your_key
MAILCHIMP_LIST_ID=your_list
```

**Setup script:**
```bash
python3 scripts/setup_integrations.py --config "config/api_config.json"
```

## Error Handling & Monitoring

### Common Issues

1. **API Rate Limits**: Implement exponential backoff and request queuing
2. **Content Formatting Errors**: Validate content before publishing
3. **Platform Policy Violations**: Check content against platform guidelines
4. **Network Failures**: Implement retry logic with circuit breakers

### Monitoring Setup

```bash
# Set up workflow monitoring
python3 scripts/setup_monitoring.py --workflow "blog-pipeline" --alerts "slack,email"

# Check workflow health
python3 scripts/check_health.py --workflow "blog-pipeline"

# View workflow logs
python3 scripts/view_logs.py --workflow "blog-pipeline" --days 7
```

## Performance Optimization

### Batch Processing
- Process content in batches to reduce API calls
- Schedule non-urgent tasks during off-peak hours
- Use local caching for frequently accessed data

### Parallel Execution
- Run independent workflow stages in parallel
- Use worker queues for high-volume content
- Implement load balancing across similar tasks

### Cost Optimization
- Use cheaper AI models for draft generation
- Cache API responses when possible
- Schedule content during low-traffic periods

## Resources

### Scripts (`scripts/`)
- `create_workflow.py` - Create new workflow definitions
- `run_workflow.py` - Execute workflow with input data
- `brainstorm.py` - Generate content ideas
- `write_content.py` - AI-assisted content creation
- `optimize_seo.py` - SEO optimization tools
- `publish.py` - Platform publishing integration
- `schedule_social.py` - Social media scheduling
- `analytics_report.py` - Performance reporting
- `workflow_templates/` - Pre-built workflow templates

### References (`references/`)
- `scheduled_blog.md` - Detailed guide for scheduled blog pipelines
- `social_multi.md` - Multi-platform social media workflows
- `newsletter_auto.md` - Automated newsletter systems
- `video_advanced.md` - Complex video content pipelines
- `api_integration.md` - Complete API integration guide
- `error_handling.md` - Troubleshooting and error recovery
- `performance_tuning.md` - Optimization techniques

### Assets (`assets/`)
- `templates/` - Content templates for different formats
- `config/` - Configuration file examples
- `examples/` - Example workflow definitions
- `brand_assets/` - Logos, images, and brand materials

## Getting Help

### Common Questions

**Q: My workflow is failing at the publishing stage.**
A: Check API credentials and platform permissions. Run `python3 scripts/test_integration.py --platform wordpress`

**Q: Content quality from AI is inconsistent.**
A: Adjust prompt templates and add more context. See `references/prompt_optimization.md`

**Q: How do I handle platform rate limits?**
A: Implement queuing and backoff. Use `python3 scripts/setup_rate_limiting.py`

**Q: Can I customize workflows for my specific needs?**
A: Yes, edit workflow definitions in `assets/examples/` and modify as needed.

### Debug Mode

Enable debug logging for troubleshooting:

```bash
export CONTENT_WORKFLOW_DEBUG=1
python3 scripts/run_workflow.py --workflow "blog-pipeline" --input "test"
```

View detailed logs:
```bash
tail -f logs/content_workflow.log
```

## Best Practices

1. **Start Simple**: Begin with 2-3 stage workflows before adding complexity
2. **Test Thoroughly**: Run workflows in test mode before production
3. **Monitor Actively**: Set up alerts for workflow failures
4. **Iterate Gradually**: Add new stages one at a time
5. **Document Changes**: Keep workflow documentation updated
6. **Backup Configurations**: Regularly backup workflow definitions
7. **Review Performance**: Monthly review of workflow effectiveness
8. **Stay Compliant**: Regularly check platform API terms of service

## Version History

- **v1.0**: Initial release with basic workflow orchestration
- **v1.1**: Added social media scheduling and analytics
- **v1.2**: Enhanced error handling and monitoring
- **v1.3**: Added video content pipeline support
- **v1.4**: Improved performance and cost optimization

---

*Note: This skill requires API access to various platforms. Ensure you have proper authentication and comply with platform terms of service.*
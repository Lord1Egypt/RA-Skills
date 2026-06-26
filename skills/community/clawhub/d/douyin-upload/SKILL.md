---
name: douyin-uploader
description: Automatically generates and publishes articles to Douyin (TikTok China). Users provide a topic, and this skill generates engaging markdown content and cover images, then publishes them using the sau command-line tool. Ideal for content creators who want to automate their Douyin article publishing workflow.
---

# Douyin Uploader

This skill helps you automatically generate and publish articles to Douyin (抖音) with AI-generated content and cover images.

## When to Use This Skill

Use this skill when the user:

- Wants to publish an article on Douyin about any topic
- Asks to "post to Douyin" or "publish to 抖音"
- Needs to create content for social media platforms
- Mentions content creation, article writing, or social media publishing
- Wants to automate their content publishing workflow

## Prerequisites

Before using this skill, ensure:

1. **Python 3.8+** is installed
2. **sau command-line tool** is properly installed and configured
3. **Douyin account** is set up and linked to sau
4. (Optional) **OpenAI API key** for high-quality content generation

## How It Works

### Step 1: Understand the User's Request

When a user wants to publish to Douyin, identify:

1. The topic or subject of the article
2. Any specific style or tone preferences
3. Target audience considerations

### Step 2: Generate Content

Generate engaging markdown content based on the topic:

- **Compelling title and subtitle** that grab attention
- **Well-structured body content** with proper formatting
- **Relevant tags and keywords** for better discoverability
- **Engaging intro and outro** to encourage interaction

### Step 3: Generate Cover Image

Create or select an appropriate cover image:

- **AI-generated image** related to the article topic
- **JPG format** to meet Douyin requirements
- **Optimized dimensions** for the platform

### Step 4: Publish to Douyin

Use the sau command to publish:

```bash
sau douyin xiaoA upload-article article_content.md --cover product_cover.jpg
```

## Usage Examples

### Example 1: Simple Article Request

**User:** "发布一篇关于人工智能的文章"

**Response:**
```
I'll help you publish an article about AI to Douyin. Let me generate the content and cover image...

[AI generates markdown content]
[AI generates cover image]
Publishing to Douyin...
✅ Success! Article ID: 735284752
```

### Example 2: Personal Experience

**User:** "分享我的旅游经历"

**Response:**
```
I'll create an engaging travel experience article for Douyin. What destination or experience would you like to share?

After receiving details, the skill generates content and publishes automatically.
```

### Example 3: Health Content

**User:** "写一篇关于健康生活的内容"

**Response:**
```
I'll write a compelling article about healthy living for Douyin. Let me generate the content...

[Generates engaging health tips article]
[Creates relevant cover image]
Published successfully!
```

## Common Article Categories

| Category       | Example Topics                     |
| -------------- | ----------------------------------- |
| Technology     | AI, tools, gadgets, software       |
| Lifestyle      | health, fitness, food, travel      |
| Education      | tutorials, tips, learning guides   |
| Entertainment  | movies, music, games, trends       |
| Business       | marketing, startups, productivity  |

## File Structure

```
douyin-upload/
├── SKILL.md                    # This file
├── sau.sh                      # Wrapper script for sau command
├── scripts/                    # Python scripts
│   ├── generate_content.py    # Content generation
│   ├── generate_image.py      # Image generation
│   ├── publish.py             # Publishing logic
│   └── config.py              # Configuration
└── references/                 # Reference materials
    └── examples.md            # Usage examples
```

## Tips for Better Results

1. **Be specific with topics**: More detailed topics generate better content
2. **Use trending keywords**: Include current trends for better engagement
3. **Quality cover images**: Good images significantly increase click-through rates
4. **Comply with platform rules**: Ensure content meets Douyin's guidelines
5. **Test before publishing**: Preview content to catch any issues

## Troubleshooting

### Common Issues

**Issue:** sau command not found
- **Solution:** Install and configure sau command-line tool properly

**Issue:** Content generation fails
- **Solution:** Check OpenAI API key (if using) or ensure AI service is accessible

**Issue:** Cover image generation errors
- **Solution:** Verify image generation API access and permissions

**Issue:** Publishing fails
- **Solution:** Check Douyin account authentication and sau configuration

## Safety and Best Practices

- **Review content before publishing**: Always review generated content for accuracy
- **Follow platform guidelines**: Ensure content complies with Douyin's policies
- **Protect personal information**: Don't include sensitive data in articles
- **Maintain quality standards**: High-quality content builds audience trust

## Performance Benefits

Compared to manual article creation:

- **10x faster** content generation and publishing
- **Consistent quality** with AI-powered content
- **Reduced manual effort** - focus on strategy, not execution
- **Scalable workflow** - easily publish multiple articles

## When This Skill Can't Help

If the user wants to:

- Publish to platforms other than Douyin
- Upload video content (this is for articles only)
- Edit existing published articles
- Manually control every aspect of content creation

In these cases, explain the skill's limitations and offer alternative approaches.
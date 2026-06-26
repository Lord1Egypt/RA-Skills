---
name: contentforge-api
description: "Generate high-quality content using ContentForge API - template-based content generation for blog posts, articles, marketing copy, website content, social media posts, product descriptions, email campaigns, newsletters, press releases, landing page copy, ad copy, content templates, automated content creation, bulk content generation, SEO content, copywriting, marketing materials, branded content, and any form of written content creation or text generation needs."
---

# ContentForge API Skill

Generate professional content using VCG's ContentForge API - a template-based content generation service with 100+ content templates.

## Quick Start

1. **Get API Key**: Help user sign up for free ContentForge API key
2. **Store Key**: Save the key securely 
3. **Generate Content**: Use templates for blogs, marketing copy, articles, etc.

## API Key Signup

### Step 1: Get User's Email
Ask the user for their email address to create a free ContentForge account.

### Step 2: Sign Up via API
```bash
curl -X POST https://contentforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "cf_1234567890abcdef",
  "message": "API key created successfully",
  "tier": "free",
  "daily_limit": 100
}
```

### Step 3: Store the API Key
Save the API key securely for future use. Instruct the user to keep it safe.

## Available Templates & Usage

### Get Available Templates
```bash
curl -H "X-API-Key: cf_1234567890abcdef" \
  https://contentforge.vosscg.com/v1/templates
```

### Generate Content Examples

#### Blog Post
```bash
curl -X POST https://contentforge.vosscg.com/v1/generate \
  -H "X-API-Key: cf_1234567890abcdef" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "blog_post",
    "inputs": {
      "topic": "AI in Marketing",
      "tone": "professional",
      "length": "medium",
      "keywords": ["artificial intelligence", "marketing automation", "personalization"]
    }
  }'
```

#### Marketing Copy
```bash
curl -X POST https://contentforge.vosscg.com/v1/generate \
  -H "X-API-Key: cf_1234567890abcdef" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "ad_copy",
    "inputs": {
      "product": "SaaS Analytics Platform",
      "audience": "small business owners",
      "cta": "Start Free Trial",
      "tone": "persuasive"
    }
  }'
```

#### Product Description
```bash
curl -X POST https://contentforge.vosscg.com/v1/generate \
  -H "X-API-Key: cf_1234567890abcdef" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "product_description",
    "inputs": {
      "product_name": "Wireless Headphones",
      "features": ["noise canceling", "30hr battery", "bluetooth 5.0"],
      "target_audience": "professionals",
      "style": "benefits-focused"
    }
  }'
```

**Expected Response Format:**
```json
{
  "content": "Generated content here...",
  "template_used": "blog_post",
  "word_count": 524,
  "tokens_used": 1,
  "remaining_daily": 99
}
```

## Popular Templates

- `blog_post` - Full blog articles with SEO optimization
- `ad_copy` - Social media and digital advertising copy
- `product_description` - E-commerce product descriptions
- `email_subject` - Email marketing subject lines
- `newsletter` - Newsletter content and formatting
- `press_release` - Professional press releases
- `landing_page` - Landing page copy and headlines
- `social_post` - Social media posts for various platforms
- `meta_description` - SEO meta descriptions
- `case_study` - Customer case study content

## Error Handling

Common error responses:
- `401 Unauthorized` - Invalid or missing API key
- `429 Too Many Requests` - Daily limit exceeded
- `400 Bad Request` - Invalid template or missing required inputs

## Pricing & Limits

**Free Tier:**
- 100 requests per day
- Access to all templates
- No credit card required

**Paid Plans:**
- Upgrade at https://vosscg.com/forges for higher limits
- Premium templates and customization
- Priority support and faster generation

## Best Practices

1. **Template Selection**: Choose the right template for your content type
2. **Input Quality**: Provide detailed, specific inputs for better results
3. **Tone Consistency**: Use consistent tone parameters across related content
4. **Keyword Integration**: Include relevant keywords for SEO-optimized content
5. **Batch Processing**: Generate multiple pieces at once for efficiency

## Integration Examples

### OpenClaw Agent Workflow
```bash
# 1. Help user get API key
curl -X POST https://contentforge.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# 2. Store the returned API key securely
# 3. Generate content based on user request
curl -X POST https://contentforge.vosscg.com/v1/generate \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"template":"blog_post", "inputs":{...}}'

# 4. Return the generated content to the user
```

When a user asks for content generation, blog writing, marketing copy, or any text creation task, use this skill to leverage ContentForge's professional templates and AI-powered generation capabilities.
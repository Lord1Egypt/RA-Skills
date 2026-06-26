# ad-copy

## Name
Advertising Creative Copywriting

## Description
High-converting advertising copy creation for digital marketing campaigns including信息流 (feed) ads, native advertising, social media ads, and display advertising. Focuses on CTR (Click-Through Rate) improvement, creative direction, headline variations, body copy, call-to-action optimization, and audience-specific messaging. Generates compelling ad creative that captures attention and drives action across multiple platforms.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| product_service | text | Yes | Product or service description and benefits |
| target_audience | text | Yes | Audience demographics, interests, and pain points |
| ad_platform | select | Yes | Platform: Facebook, Instagram, TikTok, Google, etc. |
| campaign_goal | text | Yes | Primary objective: awareness, clicks, conversions |
| unique_selling_point | text | Yes | Key differentiator from competitors |
| offer_details | text | No | Special promotions or incentives |
| ad_format | text | No | Specific ad format and dimensions |

## Output

| Name | Type | Description |
|------|------|-------------|
| headline_variations | text | Multiple headline options for A/B testing |
| body_copy | text | Primary ad body copy variations |
| cta_options | text | Call-to-action button text variations |
| creative_concepts | text | Different creative angles and approaches |
| audience_versions | text | Copy variations for different audience segments |
| visual_direction | text | Visual element recommendations |
| testing_plan | text | A/B testing strategy and priorities |

## Example

### Input
```json
{
  "product_service": "Online language learning app with AI conversation practice",
  "target_audience": "Working professionals 25-40 wanting to learn Spanish",
  "ad_platform": "Facebook",
  "campaign_goal": "App installs",
  "unique_selling_point": "AI-powered conversations that adapt to your level",
  "offer_details": "7-day free trial, then $9.99/month"
}
```

### Output
```json
{
  "headline_variations": ["Speak Spanish in 30 Days", "Finally, a Language App That Works", "AI Makes Learning Spanish Easy"],
  "body_copy": "Practice real conversations with AI that adapts to your level...",
  "cta_options": ["Start Free Trial", "Download Now", "Learn Spanish Free"],
  "creative_concepts": ["Before/after transformation", "Day-in-life scenario", "Success story testimonial"],
  "audience_versions": "Business travelers: 'Close deals in Spanish'. Students: 'Ace your Spanish class'.",
  "visual_direction": "Show app interface, diverse users, progress indicators",
  "testing_plan": "Test headlines first, then body copy, then CTAs"
}
```

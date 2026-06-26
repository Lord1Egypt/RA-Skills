# Usage Examples

This document provides detailed conversational usage examples, showing the interaction flow of easy-image-skill in various real-world scenarios.

## Table of Contents

1. [First-time Setup](#1-first-time-setup)
2. [PPT Cover Generation (Clear Input)](#2-ppt-cover-generation-clear-input)
3. [Product Photo Generation (Guided Completion)](#3-product-photo-generation-guided-completion)
4. [Xiaohongshu Grid (Vague to Precise Generation)](#4-xiaohongshu-grid-vague-to-precise-generation)
5. [Save to Personal Library](#5-save-to-personal-library)
6. [Switch Platform](#6-switch-platform)
7. [Error Handling Examples](#7-error-handling-examples)

---

## 1. First-time Setup

### Scenario: User's first time using easy-image-skill

**User:** "Help me generate an image"

**System:**
```
Hi! I'm easy-image-skill, helping you quickly generate professional workplace images.
First-time setup needed, about 30 seconds.

[Start Setup] | [Skip, use defaults]
```

**User:** "Start Setup"

**System:**
```
1/4 - Select Platform
Which platform would you like to use for image generation?

- Jiekou AI (Recommended for China, fast and high quality)
- Novita (Global, rich models)
- PPIO (Domestic platform, stable and reliable)
- OpenRouter (Aggregates multiple models)
- WaveSpeed (High-quality output)
- Google Imagen (Google official)

Recommended: Jiekou AI
```

**User:** "Let's use Jiekou AI"

**System:**
```
2/4 - Configure API Key
Please provide your Jiekou AI API Key (Get it at: https://jiekou.ai/settings/key-management)

Format: my key is sk-xxx
```

**User:** "my key is sk-abc123xyz456"

**System:**
```
API Key saved

3/4 - Storage Path
Where should images be saved by default?

- System Downloads folder (Recommended) → ~/Downloads
- Desktop → ~/Desktop
- Custom path
```

**User:** "Downloads folder is fine"

**System:**
```
Storage path set: ~/Downloads

4/4 - Frequent Scenes
What are your most common use cases? (Multiple selection)

- PPT Graphics
- Marketing Posters
- Product Photos
- Social Media Grid
- Avatar/Badge
- Other
```

**User:** "Product photos and PPT graphics"

**System:**
```
Setup complete!

Current configuration:
- Platform: Jiekou AI (jiekou)
- Storage path: ~/Downloads
- Frequent scenes: Product photos, PPT graphics

You can say "change settings" anytime to adjust. Now tell me what image you'd like to generate!
```

---

## 2. PPT Cover Generation (Clear Input)

### Scenario: User provides complete requirements

**User:** "Generate a blue tech-style PPT cover, theme is artificial intelligence"

**System:**
```
[Background execution:
 - Identify scene: PPT cover
 - Identify elements: color=blue, style=tech, theme=AI
 - Check personal library: no match
 - Load template: references/templates/ppt-slides.md
 - Translate prompt: modern AI presentation cover, deep blue gradient background (#0a1929 to #1565c0),
   futuristic geometric patterns, neural network visualization elements, minimalist tech aesthetic,
   professional corporate style, clean composition, high resolution, 16:9 aspect ratio
 - Call Jiekou AI API
]

Generating, please wait...

Image generated~
[Display image]
Saved to: ~/Downloads/ppt_cover_ai_20260316_143052.png

Does this meet your expectations? If satisfied, I'll save it to your personal library
for reusing the style in similar future requests.
```

**User:** "Looks good, save it"

**System:**
```
Saved to your personal library

Will auto-reuse this style when generating similar PPT covers next time~
```

---

## 3. Product Photo Generation (Guided Completion)

### Scenario: User's requirements are vague, system guides to complete info

**User:** "Help me make a product photo"

**System:**
```
Sure~ What product?
```

**User:** "Wireless earbuds"

**System:**
```
Got it, wireless earbuds product photo~ What background would you like?

- White (suitable for e-commerce)
- Scene shot (suitable for promotion)
- Solid color background (custom color)
- Gradient background
```

**User:** "White"

**System:**
```
[Background execution:
 - Scene: Product photo
 - Subject: Wireless earbuds
 - Background: White
 - Size: Default 1:1 (e-commerce standard)
 - Translate prompt: wireless bluetooth earbuds, pure white background (#FFFFFF), studio lighting setup,
   commercial product photography, ultra detailed, centered composition, professional e-commerce style,
   high-end consumer electronics, 8K resolution, square format
]

Generating, please wait...

Image generated~
[Display image]
Saved to: ~/Downloads/product_earbuds_20260316_150312.png

Satisfied?
```

**User:** "The product is too small, can you make it bigger?"

**System:**
```
OK, I'll adjust the composition to make the product more prominent.

[Background execution: modify prompt, add close-up, larger scale, prominent product placement]

Adjusted as requested, how's this one?
[Display adjusted image]
Saved to: ~/Downloads/product_earbuds_20260316_150425.png
```

**User:** "This is good, save it"

**System:**
```
Saved to your personal library

Will prioritize this composition style when generating earbuds product photos next time~
```

---

## 4. Xiaohongshu Grid (Vague to Precise Generation)

### Scenario: User provides insufficient info, multiple rounds of conversation to complete

**User:** "I want to post on Xiaohongshu"

**System:**
```
OK, Xiaohongshu vertical format (3:4)~ What content?
```

**User:** "Cafe exploration"

**System:**
```
Got it, cafe exploration content~ What style would you like?

- Ambient (warm tones, soft lighting)
- Minimal (clean and bright)
- Artistic (vintage filter)
- Business (professional high-end)
```

**User:** "Ambient"

**System:**
```
[Background execution:
 - Scene: Social media (Xiaohongshu)
 - Channel: Xiaohongshu → Auto size 3:4
 - Subject: Coffee shop
 - Style: Ambient
 - Translate prompt: aesthetic coffee shop interior, warm morning light streaming through windows,
   cozy atmosphere, minimalist composition with coffee cup in focus, soft natural shadows,
   instagram lifestyle photography style, neutral warm color palette (#8B7355, #D4A574),
   depth of field, professional food photography, 3:4 vertical format for social media
]

Generating, please wait...

Image generated~
[Display image]
Saved to: ~/Downloads/social_coffee_shop_20260316_170023.png

This works as a Xiaohongshu cover. Want me to generate a complete 9-grid set?
```

**User:** "Sure"

**System:**
```
Generating 9-grid series...

[Generate 9 images with unified style]

9-grid generated:
  1. social_coffee_01_20260316_170145.png
  2. social_coffee_02_20260316_170148.png
  3. social_coffee_03_20260316_170151.png
  ... (9 total)

Saved to: ~/Downloads/

All images maintain unified ambient style, ready to post on Xiaohongshu~
```

**User:** "Perfect, save all to personal library"

**System:**
```
Saved to your personal library

Will auto-reuse this style set for cafe or similar exploration content next time~
```

---

## 5. Save to Personal Library

### Scenario: Demonstrating personal library auto-reuse capability

**(Two days later, user uses again)**

**User:** "Make a coffee product photo, cozy atmosphere"

**System:**
```
[Background execution:
 - Identify scene: Product photo
 - Identify keywords: coffee, cozy, atmosphere
 - Query personal library: found match
   - Scene: Social media (cafe exploration)
   - Keyword similarity: 0.75 (coffee, ambient)
   - Match successful, reuse personal library style
 - Adjust scene: Social media → Product photo
 - Keep style: Cozy ambient, warm tones
]

Generating, please wait...

Image generated~
[Display image - style consistent with previous cafe exploration images]
Saved to: ~/Downloads/product_coffee_20260318_093215.png

This continues the coffee ambient style you liked before, satisfied?
```

**User:** "Yes, that's exactly the feel!"

**System:**
```
Great! Your personal style library is working well~
Save this one too?
```

**User:** "Save"

**System:**
```
Updated to your personal library
```

---

## 6. Switch Platform

### Scenario: User wants to try different platform

**User:** "Try Novita"

**System:**
```
OK, switching to Novita.

Checking API Key... Novita API Key not detected.
Please provide your Novita API Key (Get it at: https://novita.ai/settings/key-management)

Format: my key is nv-xxx
```

**User:** "my key is nv-123abc456def"

**System:**
```
Novita API Key saved
Platform switched to Novita

Now generating images with Novita. Tell me what you'd like to generate!
```

**User:** "Generate a marketing poster, spring sale event"

**System:**
```
[Background execution:
 - Using platform: Novita
 - Scene: Marketing poster
 - Theme: Spring sale
 - Translate prompt and call Novita API
]

Generating, please wait...

Image generated~
[Display image]
Saved to: ~/Downloads/poster_spring_sale_20260316_180542.png
```

**User:** "Switch back to Jiekou AI"

**System:**
```
Switched back to Jiekou AI
```

---

## 7. Error Handling Examples

### 7.1 API Key Not Configured

**User:** "Use Google to generate an avatar"

**System:**
```
Detected you selected Google Imagen, but API Key not configured yet.

Please provide your Google Imagen API Key:
Get it at: https://console.cloud.google.com/apis/credentials

Format: my key is AIza...
```

### 7.2 Invalid API Key

**User:** "Generate an image"

**System:**
```
[API call failed: 401 Unauthorized]

API Key seems to have issues (may have expired or be invalid).
Please check and reconfigure: my key is xxx

Or try switching to another platform.
```

### 7.3 Insufficient Balance

**User:** "Generate a product photo"

**System:**
```
[API call failed: 402 Payment Required]

Platform says insufficient balance.
Please top up at: https://jiekou.ai/billing

Or switch to another platform to continue.
```

### 7.4 Network Timeout

**User:** "Generate a PPT cover"

**System:**
```
[API call timeout]

Generation failed, might be network issue. Want to retry?

[Retry] | [Switch Platform]
```

**User:** "Retry"

**System:**
```
Retrying...

[Success]
Image generated~
Saved to: ~/Downloads/ppt_cover_20260316_192134.png
```

### 7.5 Rate Limit

**User:** "Generate another one"

**System:**
```
[API call failed: 429 Too Many Requests]

Too many requests, please wait a moment.

(About 10 seconds wait needed)
```

### 7.6 Can't Understand Input

**User:** "Make something with that kind of feel"

**System:**
```
Didn't quite understand what image you want, can you describe more specifically?

For example:
- What's it for? (PPT, poster, product photo, social media...)
- What content/theme?
- What style?

Or just say "I want to generate a..."
```

### 7.7 Platform Service Error

**User:** "Generate an image"

**System:**
```
[API call failed: 500 Internal Server Error]

Platform service error, please try later.

Suggestions:
- Wait 5-10 minutes and retry
- Or switch to another platform: Novita, PPIO, Google, etc.

Want to switch platform?
```

**User:** "Switch to PPIO"

**System:**
```
Switched to PPIO
Now tell me what image you'd like to generate!
```

---

## 8. Advanced Scenario Examples

### 8.1 WeChat Article Header

**User:** "Make a WeChat article header image, theme is workplace productivity"

**System:**
```
[Background execution:
 - Identify channel: WeChat article → Auto size 2.35:1 (900x383px)
 - Scene: Marketing poster
 - Theme: Workplace productivity
 - Translate prompt: professional productivity improvement banner for WeChat article,
   modern minimalist design, business professional theme, clock and checklist elements,
   clean layout with text space, corporate color scheme (#2C5F88, #F4F4F4),
   ultra-wide 2.35:1 format, 900x383 resolution
]

Generating, please wait...

Image generated~
[Display image - 2.35:1 ultra-wide ratio]
Saved to: ~/Downloads/wechat_banner_productivity_20260316_154823.png

This size is optimized for WeChat article headers, ready to use~
```

### 8.2 Batch Team Avatar Generation

**User:** "Generate 5 cartoon avatars for team members, unified style"

**System:**
```
OK, team cartoon avatars~ Need to provide feature descriptions for each member.

Or I can generate unified style avatar templates for you to choose from?

[Provide feature descriptions] | [Generate style templates]
```

**User:** "Generate style templates"

**System:**
```
[Generate 5 cartoon avatars with different characters, unified style]

Team avatars generated (5 total):
1. avatar_professional_male_01.png
2. avatar_professional_female_01.png
3. avatar_professional_male_02.png
4. avatar_professional_female_02.png
5. avatar_professional_neutral.png

All avatars maintain unified flat business style, suitable for team introduction pages.
Saved to: ~/Downloads/
```

### 8.3 Conference Badge Design

**User:** "Design a conference badge, need areas for name, company, title"

**System:**
```
[Background execution:
 - Scene: Badge design
 - Size: 3:4 (standard badge size)
 - Requirement: Reserve text areas
 - Translate prompt: professional conference badge template, clean modern design,
   designated areas for name/company/title text placeholders, corporate blue color scheme,
   minimalist layout with logo space, vertical 3:4 format, print-ready quality
]

Generating, please wait...

Badge template generated~
[Display image - with clear text area placeholders]
Saved to: ~/Downloads/badge_conference_20260316_162345.png

This is a template design, you can add specific name, company, title info in image editing software.
```

---

## 9. Configuration Management Examples

### 9.1 View Current Configuration

**User:** "Show my config"

**System:**
```
Current configuration:

- Platform: Jiekou AI (jiekou)
- API Key: Configured
- Storage path: ~/Downloads
- Frequent scenes: Product photos, PPT graphics
- Image format: PNG
- Image quality: High
- Max adjustment rounds: 3

Personal library status:
- Saved prompts: 12 entries
- Recently used: Cafe exploration content (2026-03-18)

Need to modify anything? Or say "change settings" to enter config menu.
```

### 9.2 Modify Storage Path

**User:** "Save images to desktop"

**System:**
```
Storage path updated: ~/Desktop

Next generated images will be saved to Desktop.
```

### 9.3 Reset Configuration

**User:** "Reset config"

**System:**
```
Are you sure you want to reset all configuration?

This will delete:
- Platform selection and API Key
- Storage path settings
- Frequent scene records

Personal library (my-prompts.md) will be kept.

[Confirm Reset] | [Cancel]
```

**User:** "Confirm reset"

**System:**
```
Configuration reset

Starting setup process again...

1/4 - Select Platform
Which platform would you like to use for image generation?
...
```

---

## 10. Multi-round Fine-tuning Example

### Scenario: User not satisfied with initial result, needs multiple adjustments

**User:** "Generate a marketing poster, summer cool drinks"

**System:**
```
Generating, please wait...

Image generated~
[Display image - blue tones, ice elements]
Saved to: ~/Downloads/poster_summer_drink_20260316_195012.png
```

**User:** "Colors are too cold, change to warm tones"

**System:**
```
[Fine-tune round 1: adjust tones]

Adjusted to warm tones, how's this one?
[Display image - orange-yellow tones]
Saved to: ~/Downloads/poster_summer_drink_20260316_195134.png
```

**User:** "Can the text area be bigger?"

**System:**
```
[Fine-tune round 2: enlarge text area]

Text area enlarged, how's this one?
[Display image - prominent text area]
Saved to: ~/Downloads/poster_summer_drink_20260316_195256.png
```

**User:** "Background more minimal"

**System:**
```
[Fine-tune round 3: simplify background]

Background simplified, how's this one?
[Display image - minimal background]
Saved to: ~/Downloads/poster_summer_drink_20260316_195418.png

Note: Already adjusted 3 times. If still not satisfied, try describing your needs differently,
maybe we can try a different approach?
```

**User:** "This works, save it"

**System:**
```
Saved to your personal library

Will use this minimal warm-tone style for beverage posters next time~
```

---

## Summary

The examples above demonstrate easy-image-skill usage flow in various real-world scenarios:

- **First-time setup** - Quick guide, 30 seconds to complete
- **Clear input** - Direct generation, no extra interaction needed
- **Guided completion** - Smart questions, complete missing info
- **Personal library accumulation** - Auto-reuse, continuous optimization
- **Platform switching** - Flexible choice, seamless switching
- **Error handling** - Friendly messages, provide solutions
- **Fine-tuning** - Multi-round adjustment, precise control

**Core Experience:** Simple description → Smart translation → High-quality image

For more technical details, see: [SKILL.md](../SKILL.md)

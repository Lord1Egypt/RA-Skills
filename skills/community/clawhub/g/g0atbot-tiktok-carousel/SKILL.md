---
name: tiktok-carousel
description: Generate viral TikTok photo carousels using AI. Uses 6-slide formula for maximum engagement and includes learning loop for continuous improvement.
license: MIT
metadata:
  openclaw:
    emoji: 🎠
    requires:
      env:
        - OPENAI_API_KEY
        - TIKTOK_COOKIES
      bins:
        - curl
---

# TikTok Carousel Generator

Generate viral TikTok photo carousels using AI. This skill implements the proven 6-slide formula for maximum engagement.

## Setup

Set these environment variables:
- `OPENAI_API_KEY` - For AI image generation ($0.25-$0.50 per post)
- `TIKTOK_COOKIES` - TikTok session cookies for posting

## The 6-Slide Formula

```
Slide 1: Hook with text overlay
Slide 2: The problem
Slide 3: Discovery
Slide 4: Transformation 1
Slide 5: Transformation 2
Slide 6: CTA
```

## Image Prompt Rules

**ALWAYS add to every prompt:**
- "iphone photo"
- "realistic lighting"

**Keep consistent across all 6 slides:**
- Counter dimensions
- Lighting direction
- Camera angle
- What's on the table
- Everything except the main subject

Only change: what's on screen or the food/product layout

## Text Overlay Rules

- Font size: 6.5% of image height with TIKTOK SANS font
- Position: 30% from top (top 10% hidden by TikTok status bar)
- Line breaks every 4-6 words
- Full hook on slide 1 - never split across slides
- Bottom 20% hidden behind TikTok UI

## The Hook Formula

**FLOP** (feature-focused):
- "track your calories in seconds" ❌
- "the best macro tracking app" ❌

**WIN** ([Person] + [Doubt/Conflict] + Data + Reaction):
- "my trainer asked me to log everything i eat for a week. she wasn't ready" ✅
- "showed my girlfriend how many calories are in her 'healthy' smoothie" ✅

## Learning Loop

Your agent tracks:
- Views per post
- Best/worst hooks
- Audience conversion metrics
- Auto-updates strategy

**Metrics that matter:**
- High views + no downloads = wrong audience → pivot
- Downloads + no paid = fix onboarding
- Low views + high conversions = hook needs work

## Usage

```
# Generate a carousel for a calorie tracking app
generate_carousel --niche fitness --product "calorie tracking app" --hooks "my trainer asked me to log everything"

# Generate for a finance/productivity niche
generate_carousel --niche finance --product "budget app" --hooks "my accountant looked at my spending"

# Generate and post to TikTok
generate_carousel --niche health --product "meal prep app" --post true
```

## Example Output

For a calorie tracking app:
```
Slide 1: "my nutritionist looked at what i actually eat in a day and went silent"
Slide 2: messy kitchen counter with takeout boxes
Slide 3: someone scanning food with phone
Slide 4: clean meal prep with calories visible
Slide 5: weekly progress breakdown
Slide 6: "i didn't change what i eat. i just started seeing the numbers"
```

## Tips for Success

1. **Warm up TikTok** for 2-3 days first (scroll, like, follow)
2. **Add trending audio** manually (10x reach difference)
3. **Post 3x minimum per day**
4. **Let the agent learn** - don't micromanage images
5. **Content performs best when messy and real** - not perfect

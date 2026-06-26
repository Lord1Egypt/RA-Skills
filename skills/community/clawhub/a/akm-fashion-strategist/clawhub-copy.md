# AKM Fashion ClawHub Skill Page

## Skill Title

**AKM Fashion: Context-Aware Wardrobe Strategist**

## One-line Description

Model the user's body, scenes, wardrobe, and constraints first, then make outfit and purchase decisions that actually fit.

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fashion-strategist --full-depth
```

## Public Sample

- GitHub sample record: `https://github.com/sirsws/akm/blob/main/branches/fashion/skill/SAMPLE_RECORD.md`

## What It Is

Most styling agents answer too early.

They do not know what the user owns, what scenes matter, what body issues need handling, or what functional constraints exist.
That is where generic style advice starts.

AKM Fashion fixes this by building a usable fashion profile first:

- body context
- primary scenes
- style preferences
- wardrobe assets
- functional constraints
- anti-patterns

Only then does it produce outfit and wardrobe decisions.

## What Makes It Different

This is not a stylist persona prompt.
It is a three-stage method:

1. elicitation
2. structured record
3. execution decision

The output is not a moodboard.
It is a wardrobe-aware judgment.

## Best Fit

Use this skill when:

- the user needs scene-specific outfit decisions
- current wardrobe materially constrains the solution space
- comfort and function matter, not only aesthetics
- the user wants purchase priorities, not vague taste talk

## Boundary

- not an image recognition tool
- not a virtual try-on product
- does not pretend unknown wardrobe assets are known
- does not replace scene judgment with vague style labels

## Closing Line

**No wardrobe model, no serious styling advice.**

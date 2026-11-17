---
name: ad-copy-frameworks
description: Write ad copy that fits each platform. Eight copy frameworks (PAS, AIDA, BAB, FAB, 4U, objection-first, proof-first, offer-stack) with when to use each, the exact field lengths for Google, Microsoft, Meta, LinkedIn, TikTok, Pinterest, Reddit and X ads (including how CJK, emoji and links are counted), and how to write 15 distinct responsive search ad headlines.
license: MIT
---

# Ad copy frameworks

Good ad copy is one specific promise to one specific person, in the space the platform gives you. This skill is the
method: pick a framework, fill it with specifics, then fit it to the field lengths.

## The frameworks

| Framework | Shape | Use it when |
|---|---|---|
| **PAS**: Problem, Agitate, Solution | Name the pain, make it vivid, offer the fix | The pain is felt and specific |
| **AIDA**: Attention, Interest, Desire, Action | Hook, a reason to care, the want, the ask | Longer formats (LinkedIn intro text, Meta primary text) |
| **BAB**: Before, After, Bridge | Life now, life with it, how to get there | Transformation products |
| **FAB**: Feature, Advantage, Benefit | What it is, what it does better, what that means for you | Technical buyers, B2B, specs that matter |
| **4U**: Useful, Urgent, Unique, Ultra-specific | One line that checks all four | Headlines, search ads |
| **Objection-first** | Answer the reason they would not buy, first | Expensive, new or unfamiliar products |
| **Proof-first** | Lead with the result or the number | You have a strong review, stat or customer |
| **Offer-stack** | Price, then everything included, then the deadline | Sales and launches |

## Rules that beat any framework

- **Specific beats clever.** "Saves 40 minutes a week" beats "saves you time". "Ships in 2 days" beats "fast shipping".
- **Their words, not yours.** Lift phrases from reviews, comments and support tickets. The customer's description of
  the problem is the headline.
- **One idea per ad.** A second benefit halves the first one.
- **The first line does all the work.** Everything after the first 125 characters on Meta, or the first line on
  LinkedIn and Instagram, is behind "more".
- **No claim you cannot back up.** Platforms reject unsupported superlatives ("best", "#1") and health or finance
  promises.

## Field lengths

Hard limits are refused; recommended lengths are accepted but may be cut off. Source links for every number are in the
open dataset [social-media-specs](https://github.com/hermoso-ai/social-media-specs).

| Platform | Field | Hard limit | Recommended |
|---|---|---:|---:|
| Google responsive search | Headline (3 to 15 of them) | 30 | |
| | Description (2 to 4) | 90 | |
| | Display path 1 and 2 | 15 each | |
| Google responsive display | Headline / long headline | 30 / 90 | |
| | Description / business name | 90 / 25 | |
| Microsoft responsive search | Headline / description / paths | 30 / 90 / 15 | |
| Meta | Primary text / headline / description | none published | 125 / 40 / 25 |
| LinkedIn Sponsored Content | Intro text / headline / description | 3,000 / 200 / 300 | 150 / 70 / 100 |
| TikTok In-Feed | Ad text / display name | 20 (name) | 100 (text) |
| Pinterest | Title / description | 100 / 800 | 40 (title) |
| Reddit | Headline / display URL | 300 / 100 | 100 (80 to be safe) |
| X | Post text / card headline | 280 / 70 | 50 (headline) |

**How they count:** Google counts each Chinese, Japanese or Korean character as 2, so a CJK headline fits 15. Microsoft
counts CJK characters **and emoji** as 2. TikTok suggests 50 CJK characters instead of 100. On X, every link costs 23
characters whatever its length. Count with a tool, not by eye: `npx social-media-specs ad google-search.headline "..."`.

## Writing 15 responsive search headlines

Google mixes your headlines in any order, so each one must stand alone and none may repeat another's idea. Write them
in groups:

- 3 with the **keyword** the ad group targets
- 3 **benefits**, each a different one
- 2 **proof** (rating, number of customers, award)
- 2 **offer or price** (free shipping, from $X, % off)
- 2 **objection answers** (no contract, cancel anytime, 30-day returns)
- 2 **calls to action** (Book a demo today, Shop the sale)
- 1 **brand name**

Then check: is every one at most 30 characters, would any two read as a repeat side by side, and does any combination
make a false or awkward claim? Pin a headline to position 1 only when it must always show (a legal line, the brand).

## Output shape

For each ad: the framework you used, the copy per field with its character count, and the one thing it is testing
against the other versions. Write at least three versions on different frameworks, not three wordings of one.

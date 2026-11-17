---
name: Analyze Content Narrative Arc with AI — Structure & Flow Detection
description: "Analyze emotional journey and story structure in long-form content. Maps pacing, engagement, and narrative tension. Use when the user needs to strengthen hooks, identify weak transitions, or optimize multi-part series storytelling."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📖"
    }
  }
---

## Overview

The **Content Narrative Arc Analyzer** is a professional-grade skill that deconstructs long-form content (blog articles, guides, video scripts, whitepapers, email sequences) to reveal the underlying emotional and structural architecture. Rather than surface-level grammar checking, this skill performs deep narrative analysis—identifying where readers disengage, where emotional peaks fall flat, and where transitions miss opportunities for connection.

### Why This Matters

Content creators spend weeks writing. Yet most never see the hidden gaps: the hook that doesn't hook, the turning point that arrives too early, the conclusion that doesn't earn its emotional weight. This skill fixes that by providing:

- **Narrative tension mapping** — visual breakdown of emotional highs and lows across your content
- **Engagement gap detection** — precise locations where readers typically drop off
- **Transition audits** — reveals weak bridges between ideas that fragment reader attention
- **Multi-part series cohesion** — ensures consistent pacing and tension across episodes, seasons, or course modules
- **Specific, actionable rewrites** — not just "improve this section," but "replace lines X-Y with this tighter version"

**Integrations**: Works seamlessly with WordPress (via REST API for direct content analysis), Slack (for team collaboration on rewrites), Google Docs (paste content directly), and video platforms (paste transcript).

---

## Quick Start

Try these prompts immediately:

### Example 1: Analyze a Blog Post Hook
```
Analyze the narrative arc of this blog post. Start with the first 300 words—
does the hook create curiosity or urgency? What emotional response should it 
trigger, and what's missing? Provide a stronger opening (2-3 sentence rewrite).

[Paste your article opening here]
```

### Example 2: Multi-Part Series Consistency Check
```
I have a 5-part email sequence about productivity. Check each email for 
consistent narrative tension—are the stakes rising through the series? 
Are turning points positioned strategically? Flag any emotional dips and 
suggest where to add "mini-cliffhangers" to drive opens on the next email.

Email 1: [content]
Email 2: [content]
Email 3: [content]
Email 4: [content]
Email 5: [content]
```

### Example 3: Identify Pacing Issues in Long-Form Guide
```
This 4,000-word guide feels slow around the middle. Map the full narrative arc—
where does engagement likely drop? Identify the 2-3 sections I should trim or 
restructure. Then show me what a tighter "Article Skeleton" looks like 
(key turning points only, suggested word counts per section).

[Paste full guide text]
```

### Example 4: Video Script Narrative Strength
```
Rate the narrative strength of this video script (1-10). Identify:
- Hook strength (first 30 seconds)
- Turning points (where I shift topics/increase stakes)
- Pacing: Is there adequate breathing room, or does it rush?
- Conclusion payoff: Does it deliver on the promise made in the hook?

Provide timestamp suggestions for B-roll cutaways that amplify emotional moments.

[Paste video script with rough timing]
```

---

## Capabilities

### 1. Emotional Journey Mapping
The skill constructs a visual breakdown (text-based chart or detailed timeline) showing where emotional engagement peaks and valleys occur:
- Identifies curiosity/tension triggers
- Flags moments of reader fatigue or confusion
- Suggests repositioning high-engagement sections
- Example output: "Paragraph 8 should move to position 3 to hit the rising action phase sooner"

### 2. Narrative Structure Analysis
Evaluates your content against classic story frameworks:
- **Hero's Journey** (for narrative-driven content)
- **Problem-Solution-Benefit** (for educational/how-to content)
- **Situation-Complication-Resolution** (for case studies, testimonials)
- **Freytag's Pyramid** (exposition, rising action, climax, falling action, resolution)

Highlights misaligned sections and suggests repositioning.

### 3. Pacing & Transition Audit
Detects:
- Abrupt topic shifts (weak transitions)
- Over-explanation in low-stakes sections
- Under-development of high-stakes moments
- Recommended reading time vs. actual engagement patterns
- Provides rewrites for 3-5 key transitions identified as problematic

### 4. Multi-Part Series Cohesion Check
For sequences, courses, or serialized content:
- Ensures each "installment" ends on a mini-cliffhanger (appropriate to your niche)
- Validates that stakes escalate across episodes
- Identifies where character/voice consistency wavers
- Suggests "callback" moments to reinforce continuity
- Flags tonal shifts that might confuse audience

### 5. Hook & Conclusion Strength Assessment
- Scores opening 100 words on curiosity, clarity, and relevance
- Tests if the conclusion "earns" its emotional weight
- Provides 2-3 alternative hook approaches with pros/cons
- Evaluates if conclusion resolves the central tension or leaves intentional open loops (useful for series)

### 6. Untapped Emotional Moments Identification
Highlights sections where you could deepen reader connection:
- Where vulnerability or specificity is vague
- Where you state facts instead of showing impact
- Where reader objections are acknowledged but not addressed emotionally
- Suggests sensory details or specific examples to amplify moments

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...  # Required for GPT-4 analysis (recommended for quality)
```

### Optional Parameters
When calling the skill, customize behavior:

```json
{
  "content_type": "blog_post|video_script|email_sequence|whitepaper|guide",
  "target_audience": "entrepreneurs|developers|parents|marketers",
  "tone": "conversational|authoritative|inspirational|skeptical",
  "primary_framework": "hero_journey|problem_solution|situation_complication|freytag",
  "series_length": 1,
  "focus_areas": ["hooks", "pacing", "transitions", "endings", "all"]
}
```

### Setup Instructions
1. Paste your content (or multiple sections for multi-part series analysis)
2. Specify content type (if not auto-detected)
3. Skill runs narrative arc analysis (2-5 minutes for 3,000+ words)
4. Receive structured report with visualizations, specific rewrites, and action items

---

## Example Outputs

### Sample Output 1: Pacing Report
```
NARRATIVE ARC ANALYSIS: "The Future of AI in Small Business"
Content Length: 2,847 words | Estimated Read Time: 11 minutes

HOOK STRENGTH: 7/10
├─ Opening creates moderate curiosity ("AI is changing business")
├─ Missing: Specific hook—why should THIS reader care RIGHT NOW?
└─ Suggested rewrite: "By 2025, 60% of small businesses will use AI. 
   Here's exactly how to avoid getting left behind—without a $50K 
   consultant or a computer science degree."

PACING OVERVIEW:
├─ Exposition (Intro): 0-15% of content [Good length]
├─ Rising Action (Problem): 15-35% of content [Slightly rushed—expand by 200 words]
├─ Climax (Solution): 35-65% of content [Excellent pacing, high engagement]
├─ Falling Action: 65-85% of content [DIP DETECTED—readers likely drop here]
└─ Resolution (Conclusion): 85-100% of content [Weak—lacks call-to-action tension]

ENGAGEMENT DIPS (Likelihood of Reader Drop-off):
1. Paragraph 12 (Technical explanation overload) — 40% drop risk
   → Solution: Add 1-2 relatable examples before diving into mechanics
2. Section 4, "Implementation Roadmap" — 25% drop risk
   → Solution: Break into smaller subsections; use numbered checklist

TURNING POINTS:
✓ Well-positioned: Section 3 ("The Mistake Most Businesses Make") — hits at 32%
✓ Missing: An emotional turning point around 55% (where reader commitment deepens)

TRANSITION AUDITS:
├─ Section 1→2: WEAK — "Now let's talk about..." [Generic bridge]
│  Rewrite: "But here's the problem most entrepreneurs miss: ..."
├─ Section 3→4: STRONG — Natural progression
└─ Section 4→5: ABRUPT — Topic jumps without setup
   Rewrite: Add 1-sentence setup: "To implement this successfully, 
   you'll need to understand three key components..."

CONCLUSION STRENGTH: 4/10
├─ Current: Summarizes points but doesn't resolve the core tension
├─ Missing: Why should they care? What changes if they act?
└─ Rewrite: "You now have the roadmap. But most readers will close 
   this article and do nothing. The difference between those who 
   succeed with AI and those left behind isn't intelligence—it's 
   the first step they take today. What's yours?"
```

### Sample Output 2: Multi-Part Email Series Report
```
NARRATIVE COHESION REPORT: "5-Part Productivity Masterclass"

SERIES TENSION TRAJECTORY:
Email 1: Curiosity Peak 🔥 (Problem identification)
Email 2: Tension Dip ⚠️  (Too much theory, insufficient stakes)
Email 3: Tension Peak 🔥 (Breakthrough moment—good!)
Email 4: Tension Stable ✓ (Maintains momentum)
Email 5: Tension Resolved ✓ (Strong payoff, clear CTA)

ISSUE #1 — Email 2 Pacing Problem:
Current structure: Introduce 3 concepts → Explain each → End on "Next email..."
Problem: Readers see no immediate payoff; open rate on Email 3 likely 15-20% lower

Recommendation: Add a mini-cliffhanger. Replace final paragraph with:
"But here's where most people fail—they focus on the wrong metric. 
In Email 3, I'll show you the one number that actually matters 
(and why your current system is probably measuring the wrong thing)."

CONSISTENCY CHECK:
├─ Voice: Consistent across all 5 emails ✓
├─ Terminology: "Deep Work" introduced in Email 1, used inconsistently in Emails 3-4
│  → Standardize to strengthen cohesion
├─ Emotional arc: Builds well, but Email 5 conclusion feels rushed
└─ Callback opportunities: Missing 2 opportunities to reference Email 1 promise 
   in Email 5 payoff

HOOK COMPARISON:
Email 1: 8/10 (Strong curiosity)
Email 2: 5/10 (Weak—leads with feature, not benefit)
Email 3: 7/10 (Good, but could reference Email 2 problem directly)
Email 4: 6/10 (Procedural hook—misses emotional connection to series)
Email 5: 8/10 (Strong payoff, but opening should echo Email 1 language)

RECOMMENDED FIXES: [Specific rewrites for each email opening]
```

---

## Tips & Best Practices

### 1. **Feed Content in Digestible Chunks**
Longer content (5,000+ words) may need to be analyzed section-by-section for maximum precision. Try analyzing 1,500-2,500-word sections first, then compile insights.

### 2. **Specify Your Story Framework**
The skill performs best when you indicate which narrative structure you're targeting:
- **How-to guides**: Problem-Solution-Benefit works best
- **Case studies**: Situation-Complication-Resolution
- **Personal narratives**: Hero's Journey or Freytag's Pyramid
- **Sales pages**: Curiosity-Building → Pain Point → Solution → Social Proof → CTA

### 3. **Use Series Analysis for Content Batching**
When planning a blog series, email sequence, or course:
1. Draft all 3-5 installments
2. Run multi-part analysis to catch tone/tension issues early
3. Make bulk rewrites before publishing

### 4. **Iterate on Hooks First**
Your hook is 70% of readability. Test 2-3 alternatives from the skill's suggestions, then ask:
- Does it speak to a specific pain point?
- Does it create curiosity or urgency?
- Is it free of jargon your audience doesn't use?

### 5. **Leverage the Transition Audits**
Weak transitions are invisible to readers but expensive. Tighten every suggested transition—it often reduces word count while improving flow.

### 6. **Apply Emotional Moment Suggestions Immediately**
When the skill flags "untapped emotional moments," make those edits last. They often dramatically improve engagement metrics without increasing word count.

---

## Safety & Guardrails

### What This Skill Does NOT Do

❌ **Does not fact-check content** — It analyzes *narrative structure and pacing*, not accuracy. Verify all claims independently.

❌ **Does not replace professional editors** — This is a structural/narrative audit tool. For copyediting (grammar, punctuation, style), use separate tools (Grammarly, ProWritingAid).

❌ **Does not guarantee virality or sales** — A strong narrative arc improves engagement probability, but results depend on audience fit, marketing distribution, and market conditions.

❌ **Does not analyze content under 300 words reliably** — Minimum content length: 300 words for meaningful narrative analysis.

❌ **Does not generate original content** — It optimizes *existing* content. For content creation from scratch, use separate generative skills.

❌ **Does not work with non-narrative formats** — Lists, FAQs, reference documentation don't have narrative arcs. This skill is designed for *storytelling-based* content.

### Limitations

- **Analysis depth increases with content length**: 500-word articles get basic insights; 3,000+ word guides get detailed section-by-section breakdowns
- **Series analysis requires all installments**: Multi-part analysis needs the full sequence to detect tension inconsistencies
- **Cultural context matters**: The skill's narrative advice is optimized for Western narrative conventions (Hero's Journey, 3-act structure). Results may need adjustment for other cultures/contexts
- **Genre-specific nuance**: While the skill works across niche (startup, parenting, healthcare), some industries have unique audience expectations—apply results with domain knowledge

---

## Troubleshooting

### Q: "The skill says my hook is weak, but my analytics show high engagement."
**A:** Hooks serve multiple audiences. Your current hook may work for your *existing* audience but could attract a *broader* audience with refinement. Test suggested rewrites on a small segment before broad rollout. High engagement ≠ optimal engagement.

### Q: "I got feedback that my content is too long, but the skill says pacing is good."
**A:** These are different metrics. Pacing = how well-structured emotional rhythm is. Length = word count. You can have excellent pacing in 4,000 words or poor pacing in 800 words. If length is the issue, the skill's "engagement dips" will help you trim without losing structure—remove dips and low-tension sections first.

### Q: "The skill suggests rewrites I don't like."
**A:** The skill provides options, not directives. Suggested rewrites are based on narrative best practices, but your brand voice matters. Use rewrites as starting points—modify them to match your style. A "good" narrative arc in your voice beats a "perfect" rewrite that sounds inauthentic.

### Q: "My series analysis showed tone inconsistencies, but I intended those shifts."
**A:** Intentional tonal shifts are fine if they're signaled to readers. The skill flags shifts; you decide if they're problems. If they're strategic (e.g., shifting from humor to urgency), just note that in your publishing plan.

### Q: "How long does analysis take?"
**A:** 
- 500-1,000 words: 1-2 minutes
- 2,000-3,000 words: 3-5 minutes  
- Multi-part series (5+ sections): 8-12 minutes
Wait times depend on OpenAI API load.
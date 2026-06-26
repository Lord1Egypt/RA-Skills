---
name: ai-paraphraser
description: AI paraphrasing and de-AI tool.
---

# AI Paraphraser

Rewrite AI-generated content into natural, human writing style, bypassing AI detectors like GPTZero, Turnitin, Originality.ai, and others.

## Use Cases

Use this skill when users mention intentions such as "rewrite," "paraphrase," "de-AI," "make text pass AI detection," "humanize," "eliminate AI traces," "polish text," "bypass AI detection," or "reduce article similarity."

## Core Positioning

This is not a simple synonym replacement tool. It specifically targets the statistical features that AI detectors rely on for structural reshaping:
- **Eliminate statistical patterns**: Sentence length regularity, vocabulary distribution, and paragraph rhythm that AI detectors (GPTZero / Turnitin / Originality.ai / Copyleaks) depend on
- **Preserve original meaning**: Facts, arguments, data, and core viewpoints remain completely unchanged; only the expression changes
- **Produce unpredictability**: Each rewrite yields different results with no risk of duplicate content

## Paraphrasing Modes

| Mode | Applicable Scenarios | Degree of Change |
|------|---------------------|------------------|
| **Light** | Minor adjustments, suitable for users with already decent writing | Synonym replacement + minor word order adjustments |
| **Medium** | Most paraphrasing needs, default recommendation | Sentence restructuring + paragraph reorganization + introduction of natural rhythm |
| **Aggressive** | High-risk detection scenarios, heavily AI-flavored source text | Thorough sentence fragmentation + forced diversification + injection of human writing characteristics |

## Paraphrasing Workflow

### Step 1: Determine Mode

Select the paraphrasing mode based on user requirements and source text characteristics:

- User explicitly specifies mode → Execute as specified
- User does not specify → Assess the AI flavor concentration of the source text, start with Medium
- Source text extremely short (<50 words) → Suggest Light mode to avoid semantic distortion
- Source text extremely long (>2000 words) → Process in segments, 300-500 words per segment

### Step 2: Analyze Source Text Structure

Quickly scan the source text before paraphrasing to identify:

- **High-frequency AI sentence patterns**: `In conclusion...` `Furthermore...` `It is worth noting...` `Moreover...`
- **Excessively regular structure**: Each sentence of similar length, each paragraph starting with the same connective word
- **Non-informative filler words**: `In today's rapidly evolving world...` `It goes without saying that...`
- **Core information points**: Facts, data, arguments (these must be preserved)

### Step 3: Execute Paraphrasing

**General Principles (applicable to all modes):**

1. **Sentence variety**: Alternate between active / passive / inverted / short / long sentences
2. **Vocabulary replacement**: Replace non-keywords with synonyms; preserve core terms
3. **Break regular rhythm**: Eliminate the pattern of each paragraph starting with a fixed connective
4. **Remove AI filler words**: Delete meaningless opening and concluding sentences
5. **Reorganize word order**: Rearrange information, not simply replace words

**Light Mode Additional Rules:**
- Only replace high-frequency AI vocabulary (furthermore → also / moreover → what's more)
- Make minimal word order adjustments
- Maintain original paragraph structure

**Medium Mode Additional Rules:**
- Comprehensively reorganize sentence structures; adjacent sentences should not repeat the same structure
- Order within paragraphs can be adjusted
- Introduce imperfections found in genuine human writing (occasional splitting of long compound sentences is acceptable)
- Naturally vary paragraph length

**Aggressive Mode Additional Rules:**
- Convert active sentences to passive, passive to active
- Break long sentences into short ones, then combine some short sentences
- Delete all obvious AI structural words
- Add colloquial expressions or slightly irregular phrasing where appropriate
- Reference the human writing characteristics checklist in `references/human-patterns.md`

### Step 4: Quality Check

After completing the paraphrase, quickly verify:

- [ ] **Meaning unchanged**: Are core arguments, facts, and data preserved?
- [ ] **No obvious AI features**: Do words like `Furthermore` `In conclusion` `Moreover` remain?
- [ ] **Smooth and natural**: Does it read like a human wrote it? Are there any awkward parts?
- [ ] **No duplicate content**: Are there identifiable similarities with the source text?

## Common AI Detection Trigger Words (Be Sure to Replace)

| Common AI Word | Suggested Replacement |
|---------------|----------------------|
| Furthermore | Also, Besides, What's more |
| Moreover | In addition, On top of that |
| In conclusion | All in all, To sum up, Overall |
| It is worth noting that | Notably, Interestingly, In fact |
| First and foremost | Above all, Mainly |
| As mentioned earlier | As noted, Regarding this |
| In today's world | Currently, These days |
| It goes without saying | Of course, Naturally |
| There are several | A few / Some / Several |
| This essay will discuss | This piece explores / This looks at |

## Segmented Paraphrasing Strategy (Long Texts)

When the source text exceeds 500 words, process in segments:

1. Split by natural paragraphs (do not force cuts by word count)
2. Paraphrase each segment independently while maintaining logical connections between segments
3. Finally, read through the entire text to ensure overall fluency
4. Check whether transitions between paragraphs are natural

See `references/human-patterns.md` for details.

## Paraphrasing Quality Standards

**Qualified Output:**
- Semantic equivalence: Does not alter the core meaning of the source text
- Grammatically correct: No subject-verb disagreement, tense confusion, or other errors
- Natural and fluent: Reads as if written by an educated human
- No AI traces: Contains no high-frequency AI vocabulary or regular sentence patterns

**Rewrite if Unqualified:**
- Significant semantic deviation → Paraphrase again
- Detection risk remains high → Switch to a stronger mode and rewrite
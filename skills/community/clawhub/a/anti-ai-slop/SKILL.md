---
name: anti-ai-slop
description: |
  Comprehensive AI writing pattern detection and removal toolkit for Chinese and English prose.
  Use when drafting, editing, reviewing, or scoring text to eliminate AI-generated writing patterns.
  Covers: filler phrases, formulaic structures, inflated symbolism, promotional language,
  vague attributions, passive voice, false agency, rhythm issues, and Chinese-specific AI patterns
  (替换总结情绪、角色自白化、选择零成本、装饰性细节、懂事式段落).
  Includes 50-point scoring system for quantitative quality assessment.
  Supports both EN and ZH text processing.
---

# Anti AI-Slop

Detect and remove AI writing patterns from prose. Works for Chinese and English.

## Quick Start

Apply these 7 rules to any prose:

1. **Kill filler phrases** — Remove throat-clearing openers, emphasis crutches, and all adverbs.
2. **Break formulaic structures** — Avoid binary contrasts, negative listings, dramatic fragmentation.
3. **Use active voice** — Find the human actor. No passive constructions. No inanimate objects performing human actions.
4. **Be specific** — No vague declaratives. No lazy extremes ("every," "always"). Name the specific thing.
5. **Vary rhythm** — Mix sentence lengths. Two items beat three. No em dashes. End paragraphs differently.
6. **Trust readers** — State facts directly. No softening, justification, or hand-holding.
7. **Cut quotables** — If it sounds like a pull-quote, rewrite it.

## Detailed References

Load these files as needed based on task context:

### Vocabulary & Phrase Lists
- [references/phrases-en.md](references/phrases-en.md) — English filler phrases, AI vocabulary, business jargon to remove
- [references/phrases-zh.md](references/phrases-zh.md) — Chinese AI套话, fillers, and emotional summary phrases to remove

### Structural Patterns
- [references/structures-en.md](references/structures-en.md) — English formulaic sentence structures to avoid (binary contrasts, false agency, etc.)
- [references/structures-zh.md](references/structures-zh.md) — Chinese AI-specific structural patterns (懂事式段落, 角色自白化, etc.)

### Before/After Examples
- [references/examples-en.md](references/examples-en.md) — English text transformations with change notes
- [references/examples-zh.md](references/examples-zh.md) — Chinese text transformations with change notes

### Quick Checks (run before delivering any prose)

#### English
- Any adverbs? Kill them.
- Any passive voice? Find the actor.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with Wh- word? Restructure.
- "Here's what/this/that" throat-clearing? Cut to the point.
- "Not X, it's Y" contrast? State Y directly.
- Three consecutive sentences same length? Break one.
- Em-dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific thing.

#### Chinese
- 替读者总结情绪？（"她终于明白""原来真正的……"）→ 用动作/细节让读者自己得出结论
- 角色直接表达内心？ → 真人说话先保护自己：遮掩、算计、犹豫
- 主角赢得太便宜？ → 每个选择加成本，有牺牲有风险
- 纯装饰细节？ → 只留能推动冲突/暴露信息/改变关系的细节
- "此外""值得一提的是""综上所述"等AI连接词？→ 删
- 否定式排比？（"不仅仅是……更是……"）→ 直接说结论
- 三段式列举？ → 改为两项或四项
- 同义词循环？（同一人物换三个称呼）→ 统一称呼
- 每段结尾都是金句式一句话？→ 变换结尾方式

## Scoring System (50-point scale)

Rate each dimension 1-10:

| Dimension | EN Question | ZH Question |
|-----------|------------|-------------|
| Directness | Statements or announcements? | 直截了当还是绕圈宣告？ |
| Rhythm | Varied or metronomic? | 长短句交错还是机械重复？ |
| Trust | Respects reader intelligence? | 尊重读者智力还是过度解释？ |
| Authenticity | Sounds human? | 像真人说话还是像机器生成？ |
| Density | Anything cuttable? | 有可删冗余吗？ |

**Thresholds**: ≥40 deliver. 35-39 needs revision. <35 rewrite.

## Process

1. Read input text carefully
2. Identify all instances of the patterns listed above and in reference files
3. Rewrite each problematic section
4. Verify revised text sounds natural when read aloud
5. Run quick checks
6. Score on 5 dimensions
7. Deliver: rewritten text + change summary + score

## Credits

Based on:
- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT License)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) by WikiProject AI Cleanup
- [humanizer](https://github.com/blader/humanizer) by blader
- Chinese writing rules from experienced fiction editor methodology

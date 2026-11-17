---
name: anti-ai-foolish
description: Pre-publish AI-flavor gatekeeper for Chinese long-form articles (公众号/自媒体评论). Detects and removes AI-writing tells using 1,108 rules that were A/B-validated on 52 real Tencent Zhuque detector-labeled fragments. Use whenever the user asks to 去AI味, 去AI, 降AI率, 终检/检查一篇文章 before publishing, or mentions an article was flagged or rejected by WeChat (微信打回) or Zhuque (朱雀) as AI-generated — even if they only say "这篇文章帮我看看".
---

# anti-ai-foolish — 去AI味终检

Publishing gatekeeper for Chinese articles. It answers one question: **is this draft safe to publish, or does it still read as AI-generated?** It decides with mechanical gates (punctuation, quoting habits, question density, a validated Z-score) plus three human-judgment checks that regex cannot see.

Everything here is evidence-backed: the 1,108 rules were A/B-tested against 52 fragments with real Zhuque detector labels (95% CI). Rules that failed testing are marked as such — see `rules/INDEX.json` and `references/评测报告.md`.

## When to use

- User wants a draft checked before publishing (终检 / 发文前检查).
- User says a draft "太AI了", was flagged by WeChat, or scored high on a detector.
- User wants an AI-flavored draft rewritten/surgically repaired (七刀手术).

**Do not use** for: fiction/web-novel dialogue polishing (different genre rules), academic or legal writing (cohesion is required there), English text (corpus is Chinese commentary).

## Workflow

### Step 1 — Mechanical preflight (always run first)

```bash
python scripts/preflight.py <article.md>
```

Read the output:
- **7/7 gates + Z < 0 → ✅ 可发**. Still run Step 2 before publishing.
- **Gates failed → ❌ 停下手术**. Go to Step 3.
- Z-score = confirmed-AI-rule hits − confirmed-human-rule hits. Positive means AI-side.

The six hard gates: 冒号=0, 破折号=0, 直引号=0, 概念引用腔≤3/千字, 疑问句≤3/千字, 无小节标题. For the full-rule report with per-hit fixes, run `python scripts/scanner.py <article.md>`.

### Step 2 — Human judgment (regex cannot do these three)

Check each 1,000–2,000-char block:

1. **Experiential-"I" vs performative-"I"** — "我已经学了二十多年市场营销" (real, checkable experience → human, measured 0.0036) vs "你以为你独立思考" / "我称之为" (pose → AI, measured 0.998).
2. **Are people the subject?** — If concrete people only appear as an opening example and the body is concept/data reasoning, it still reads AI (measured 0.997) even with a named person in it.
3. **Symmetrical argument triples** — "可以X，却不能Y" ×3. Colloquial repetition ("降价了，降价了") is human and must be kept; only the argument-symmetry kind gets broken.

### Step 3 — Seven-knife surgery (per 1,000–2,000-char block, in effect-size order)

1. 冒号 — strongest single AI signal (r=+0.43). Replace with commas or split sentences. Source-note sections exempt.
2. 概念引用腔 — quoting your own jargon ("信息阶层") is a 5.5× AI habit. Keep ≤1 quoted term per article.
3. 数据罗列 — three or more bare numbers in sequence get folded into events ("门票六百多，不到一双专项鞋的一半"). Numbers attached to people/actions are fine; bare number ladders are not.
4. 金句对称收尾 — delete symmetrical aphorism endings ("不是坏账，是没人信"). Keep the judgment, drop the symmetry.
5. 结构 — remove section headings, break uniform paragraph lengths, scatter enumeration chains.
6. 轻词表 — only real hits; 90+ word-list rules failed validation on this corpus.
7. **换骨架 (treats the cause)** — make lived experience / named people with direct quotes / un-inventable details the *skeleton* of each block, not decoration. This is the difference between 0.75 and 0.09 in the paired-sample test.

After surgery, re-run Step 1 until ✅.

### Step 4 — Platform test

User pastes the final text into the Zhuque detector (matrix.tencent.com/ai-detect), manually split into 1,000–2,000-char chunks (never paste whole — auto-chunking merges theory into data blocks). Target: chunk AIGC ≤ 0.40.

## Output format

Report as:

```
## 终检报告 — <文件名>
Z分: <n>（AI确认<x> − 人味确认<y>）
硬门: <p>/7（列出失败项）
人味弹药: <n>类命中
判定: ✅可发 / ⚠️改后复检 / ❌停下手术
下一步: <具体到哪一块哪一刀>
```

## Iron rules

1. Never alter the author's own sentences (原话一字不改). The exemption list lives in `rules/R_豁免用户指纹.json` — 逗号连写, 段尾判断直收, 设问定义体 are *fingerprints*, not defects.
2. Target is the human baseline band, not 0% — human writing itself scores 54–72% on proxy detectors. Once gates pass, stop.
3. Performed imperfections (fake typos, inserted filler colloquialisms) do not work (measured 77% still-AI) and are forbidden.
4. Never fabricate anchors. Facts, numbers, quotes and sources stay untouched.

## Limits

- 97% recall / 53% specificity: a quality gate, not a human-vs-AI classifier. Z<0 does not prove "human-written".
- Mechanical ceiling ≈ 0.8 correlation; the remaining variance is exactly what Step 2 covers.
- Corpus genre is Chinese self-media commentary. For other genres, re-run `python scripts/abtest.py` after adding labeled fragments to `validation/corpus/` (this re-scores all 1,108 rules automatically).

## References

Read on demand:

- `references/方法论与证据链.md` — full methodology: skeleton–fuel law, the 16 close-reading rules, exemption rationale, publish discipline (account-level homogeneity, editing-behavior signals).
- `references/评测报告.md` — validation report: classification power, cross-skill comparison, honest limits.
- `references/ROADMAP.md` — project roadmap.
- `rules/INDEX.json` — rule counts per library; each rule JSON carries `status` / `evidence` / `fix` / `exempt_when`.

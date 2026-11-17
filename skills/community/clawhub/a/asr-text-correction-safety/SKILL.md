---
name: asr-text-correction-safety
description: Use when writing, reviewing, or debugging any layer that rewrites text after recognition — dictation cleanup, OCR correction, autocorrect, transliteration, terminology normalization, or filler removal — to verify it cannot silently change what the user actually said. Also use when a phonetic, pinyin, fuzzy, or edit-distance matcher is proposed for correcting recognized text.
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"commands":["node"]},"homepage":"https://github.com/y16689540962-cloud/dsh-voice-personal"}}
---

# Text-correction safety

A correction layer sits between recognition and the user. Its failures are asymmetric and
that asymmetry decides every design question in this document:

| failure | cost |
|---|---|
| **false negative** — a mis-hearing survives | the user edits one word; they can see it is wrong |
| **false positive** — correct text is rewritten | the user's sentence silently means something else, and they may never notice |

So the invariant is not "correct as much as possible". It is:

> **Never corrupt text that was already correct.** Accuracy is the second objective.

Every rule below exists because a real implementation violated it. The numbers are from an
adversarial audit of a shipping dictation-correction layer that found nine defect classes;
section "How to find these defects" describes the method that found them.

---

## Rule 1 — Never match by sound alone

The most attractive design for correcting terminology is phonetic indexing: convert your
glossary to pinyin (or any phonetic key), convert the recognized text the same way, and
replace every phonetic match with the canonical spelling. It appears to generalize — add
`工作台` once and every mis-hearing of it (`工作太`, `公作台`) resolves itself.

It is unsound, and the reason is arithmetic, not tuning. **A short phonetic key matches
every word with that pronunciation**, and Mandarin is dense with legitimate homophones:

| pinyin | all of these are correct words |
|---|---|
| rènwù | 人物 / 任务 |
| yībù | 一部 / 异步 |
| xìntiáo | 信条 / 心跳 |
| biànyī | 便衣 / 编译 |
| jiēdiǎn | 接点 / 接口 |
| pèizhì | 配制 / 配置 |

Shipped as twelve two-syllable pairs, this rewrote **160,454 distinct two-character
strings** — the blast radius was the language. Observed damage:

```
人物关系很复杂     → 任务关系很复杂
这是一部好电影     → 这是异步好电影
信条很重要         → 心跳很重要
一步一步来         → 异步异步来
```

**No threshold fixes this.** The match is exact on pronunciation and wrong on meaning. The
information that selects 人物 over 任务 is sentence context, and the phonetic key has
already discarded it. Raising the threshold only converts false positives into false
negatives inside the same broken space.

### What is safe instead

Narrow the claim until it is checkable. The safe subset is **cross-script**: a Chinese
mis-hearing of a *Latin* term (`哈里斯` → `Harness`). There is no same-script collision
because the canonical form is in another writing system. Three guards make it sound:

1. **≥3 syllables.** Bare `哈里` (hālǐ) is also an ordinary word (`哈里发`), so short
   entries are rejected before they can match.
2. **Complete reading for the whole span.** If any character in the span has no phonetic
   entry, the key silently shortens and a 3-character span can match a 2-syllable key.
   Require `readings.length === span.length`.
3. **Exact key match over the whole span.** No partial spans, no fuzzy edges.

For same-script terminology, use **exact string matching** on observed spellings. It does
not generalize, and that is the point: `flcash` → `FlClash` is a fact you observed, not an
inference you made.

### The sub-rule that matters most

**A `heard` variant that is itself an ordinary word must not be listed.** A glossary that
recorded `grade` under Gradle, `harris` under Harness and `cloud` under Claude rewrote:

```
my grade is A               → my Gradle is A
the cloud is down           → the Claude is down
harris county               → Harness county
upgrade to the new version  → Gradle to the new version
```

---

## Rule 2 — Mask protected spans before any rewriting pass

Any rewriting pass will eventually meet a file path, URL, email, version string or code
fragment. `harness.git` inside `cd ~/projects/harness.git` is a repository name, not a
mis-hearing of "Harness".

Mask them **once, before every pass**, and restore at the end:

```js
const { masked, restore } = maskProtected(text);
// ... every pass operates on `masked` ...
return restore(text);
```

```js
const PROTECTED = [
  /[a-z][a-z0-9+.-]*:\/\/[^\s]+/gi,                     // scheme://…
  /(?:^|[\s([<"'`])(?:~|\/|\.{1,2}\/)[^\s)\]}>"'`]*/g,  // absolute/relative paths
  /[A-Za-z]:\\[^\s]*/g,                                 // Windows paths
  /[\w.+-]+@[\w-]+\.[\w.-]+/g,                          // emails
  /\bv?\d+(?:\.\d+)+(?:[-+][\w.]+)?\b/g,                // v1.2.3
  /--?[a-z][a-z0-9-]*/gi,                               // CLI flags
  /`[^`\n]*`/g,                                         // inline code
  /\b[\w-]+\.(?:js|ts|py|json|ya?ml|md|toml|sh|apk|onnx|wav)\b/gi,
];
```

The mechanism matters more than the pattern list: **one mask covering all passes**, not
each pass maintaining its own "is this a path?" check. A per-pass check will be forgotten
in the pass you add next month.

---

## Rule 3 — Idempotence is a correctness property

A correction layer runs more than once on the same text: retry, re-insert, provider
switch, re-render. **Any non-idempotent pass grows text without bound.**

The worst real case: a phrase pass emitted `Cocos Creator`, then a single-token pass
expanded the `Cocos` inside its own output:

```
cocos creator → Cocos Creator Creator → Cocos Creator Creator Creator → …
```

Two rules end it:

- **Never re-expand a form that already equals its canonical.** Compare folded forms and
  return the input unchanged when they match.
- **Never list a canonical's own prefix as a mis-hearing of itself.**

Assert it, over curated cases *and* fuzz:

```js
const once  = correct(x).text;
const twice = correct(once).text;
assert(twice === once, `${x}: ${once} → ${twice}`);
```

A 4,000-case mixed-atom fuzz found 705 violations in the revision that shipped this bug.

---

## Rule 4 — Whitespace is content

Collapsing runs of 2+ spaces "for tidiness" also collapses indentation, silently reflowing
dictated Python or YAML:

```
def foo():          →      def foo():
    if x:           →       if x:
        return 1    →        return 1
```

Preserve leading whitespace per line verbatim; collapse only *internal* runs. Assert a
Python block and a YAML document survive byte-identical.

Two related traps:

- **Do not convert writing systems.** Pinyin matching made `工作臺` match the key for
  `工作台` and rewrite it to simplified. Silent script conversion is a change the user did
  not ask for. If you offer conversion, make it an explicit, separate, opt-in action.
- **Do not strip leading/trailing newlines** from a multi-line block.

---

## Rule 5 — Deletion needs a whitelist *and* safe context

Removing filler words is where a correction layer does the most visible damage, because
filler words are also morphemes.

| shape | action | why |
|---|---|---|
| `呃，帮我…` | delete | standalone before punctuation |
| `嗯，那个，我觉得…` | delete, cascading | run of sentence-initial fillers |
| `就是这个问题` | keep | the word carries meaning here |
| `那个插件` | keep | demonstrative, not filler |
| `唉声叹气` | keep | the "filler" is part of a real word |

Two mechanisms, both required:

1. **Whitelist from the user's own corpus.** Learn which fillers this person actually uses
   (`呃 ×11, 然后 ×12`) instead of shipping a generic list. Text is never "cleaned" by a
   list the user did not generate.
2. **Context rules per occurrence.** A filler may be deleted only when it is standalone or
   followed by punctuation. `就是` and `那个` require being isolated on both sides.

**Accept the miss.** A filler glued to a word with no punctuation (`呃帮我稳定一下`) cannot
be distinguished from a morpheme at character level — allowing that deletion immediately
breaks `唉声叹气`. Measure the cost before deciding: in the reference corpus the glued
shape was 9.5% of filler occurrences while the punctuated shapes, which delete safely,
were 90.5%. Taking the safe 90% is correct.

---

## Rule 6 — Enforce guards in the index builder, not the data file

A rule written as a comment in a glossary is documentation. A rule enforced in the code
that builds the index applies to every entry added later, including by someone who never
read the comment.

```js
// In the index builder, not in glossary.js:
if (chars.length < 3) continue;                       // Rule 1.1
if (readings.length !== chars.length) continue;       // Rule 1.2
```

This is why the ≥3-syllable guard survived a later refactor while the same rule stated as
a glossary comment did not.

---

## Rule 7 — Fail open at the boundary

A bug in the correction layer must never lose the user's content:

```js
try {
  const { text } = corrector.correct(raw);
  return { text, ... };
} catch (error) {
  logger.warn('correction skipped:', error);
  return { text: raw, ... };   // the raw transcript still reaches the user
}
```

Corollary: the alternative to a corrected transcript is the *uncorrected* transcript, never
an empty or failed one. If a feature can only work by rejecting input (speaker gating, for
example), keep it **off by default** — a gate that fails closed on every input is worse
than no gate, and it is the first thing to disable when a user reports "it doesn't work".

---

## How to find these defects

None of the nine defect classes above were caught by the project's own test suite, which
passed 59/59 at the time. They were found by a dedicated adversarial pass given one
instruction: **break the property "never corrupt already-correct text"**. Run one.

### The method that works

1. **Pin a snapshot and state the invariant.** The target may change under you; a frozen
   copy plus a written invariant makes findings reproducible.
2. **Attack each pass separately, then in combination.** Sound-alike matching, fuzzy
   matching, phrase matching, spacing, deletion, whitespace — for each, ask "what correct
   input does this damage?"
3. **Enumerate the collision space.** Do not sample. If a key space exists
   (phonetic keys, edit-distance budgets), compute how many real strings map onto it.
4. **Scan a real dictionary.** For any matcher over Latin text, run it against the system
   dictionary and count words whose *content fingerprint* changes:
   ```bash
   node scripts/audit.mjs dict          # 210,604 words → how many corrupted
   ```
5. **Fuzz idempotence.** Concatenate atoms from your own vocabulary, apply twice, compare.
6. **Attack the boundaries.** Punctuation, digits, Latin, emoji, combining marks,
   surrogates, empty/whitespace, very long input, non-string input.
7. **Compute the blast radius as a number and put it in the issue.**

### Insist the verifier reports its own errors

The reference audit retracted two of its own claims after re-reading the source. A verifier
that hides its own mistakes is worthless — require it to mark each finding as
*reproduced*, *suspected*, or *retracted*.

### Keep the reproducers

Every defect found becomes a permanent test case. Sections of the reference suite map
one-to-one to audit findings, so a regression is caught by the test that documents it.

---

## Audit checklist

Copy this into your own review. Each line is a real defect from a shipping system.

- [ ] Sound-alike matching removed, or reduced to cross-script with ≥3 syllables + complete
      reading + exact key match
- [ ] No `heard` variant that is itself an ordinary word
- [ ] Protected spans masked once, before every pass
- [ ] `correct(correct(x)) === correct(x)` asserted on curated cases **and** fuzz
- [ ] No canonical form re-expanded; no canonical prefix listed as its own mis-hearing
- [ ] Indentation and newlines preserved byte-identical (assert with Python + YAML blocks)
- [ ] No silent writing-system conversion
- [ ] Deletion gated by a corpus-derived whitelist **and** per-occurrence context rules
- [ ] Guards enforced in the index builder, not only documented in data
- [ ] Fail-open at the boundary; raw text returned on any internal error
- [ ] Any rejection-based feature (speaker gating, thresholds) is off by default
- [ ] Dictionary scan clean; collision space enumerated and stated as a number
- [ ] Non-string / empty / pathological input handled without throwing
- [ ] Every audit finding has a permanent regression test

---

## Reference measurements

From the audited implementation, useful as orders of magnitude:

| check | before | after |
|---|---|---|
| distinct 2-char strings rewritten (phonetic pass) | 160,454 | 0 (pass removed) |
| dictionary words corrupted, fuzzy on (210,604 scanned) | 97 | 0 |
| non-idempotent cases (4,000 fuzz) | 705 | 0 |
| filler shapes deleted safely | — | 90.5% (glued 9.5% accepted as miss) |

`scripts/audit.mjs` in this skill implements the dictionary scan, the idempotence fuzz, and
the collision enumeration against any module exposing `correct(text) → {text}`. Point it at
your layer and adjust the thresholds in the checklist from its output.

---

## 中文摘要（供中文读者与 SkillHub 索引）

**核心不变量：绝不破坏已经正确的文本。** 纠错的两类失败代价不对称——漏纠一次，用户自己
改一个字；错纠一次，用户说的话被静默改了意思，而且他可能永远不知道。所以准确率是第二目标。

**为什么不能用拼音/谐音匹配术语。** 短拼音键会命中所有同音词，而普通话同音词极密：

| 拼音 | 这些全都是正确的词 |
|---|---|
| rènwù | 人物 / 任务 |
| yībù | 一部 / 异步 |
| xìntiáo | 信条 / 心跳 |
| biànyī | 便衣 / 编译 |
| jiēdiǎn | 接点 / 接口 |
| pèizhì | 配制 / 配置 |

实测 12 组两音节词条的碰撞面是 **160,454 个不同的两字组合**——等于整个常用字表。实际把
`人物关系很复杂` 改成 `任务关系很复杂`、`这是一部好电影` 改成 `这是异步好电影`。
**调阈值修不了**：匹配在读音上精确、在语义上错误，而选择「人物」还是「任务」靠的是上下文，
拼音键已经把它丢掉了。

**七条规则**（每条都是真实审计发现的缺陷）：

1. **绝不只按读音匹配** —— 同脚本词条用精确匹配；跨脚本音译（`哈里斯`→`Harness`）须满足
   ≥3 音节 + 整段读音完整 + 拼音键完全匹配
2. **任何改写之前，先遮罩保护跨度** —— URL、路径、邮箱、版本号、CLI 参数、行内代码
3. **幂等性是正确性属性** —— `correct(correct(x)) === correct(x)`；否则文本会无界增长
4. **空白是内容** —— 缩进和换行必须逐字节保留（口述的 Python/YAML 不能被重排）
5. **删除要同时有白名单和上下文** —— 白名单来自用户自己的语料；逐处判定是否孤立。
   `唉声叹气` 里的「唉」是词素，不能删；粘字形态（`呃帮我稳定一下`）接受漏删
6. **守护放在索引构建器里，不放在数据文件里** —— 数据文件里的规则是文档，构建器里的规则才强制执行
7. **边界上 fail-open** —— 纠错内部出错时返回原始文本，绝不让用户的听写丢失；
   任何「拒绝式」功能（声纹门禁、阈值）默认关闭

**审计脚本** `scripts/audit.mjs` 实现三类检查：21 万英文词典误伤扫描、4000 例幂等 fuzz、
碰撞面枚举。它**双向验证过**——对修复后的实现报干净，对有缺陷的旧版能复现全部缺陷类
（658/4000 非幂等、8/20 常见词被改写）。

## Deeper write-ups

- Design reasoning, including the full collision derivation:
  <https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/DESIGN.md>
- Nine defect classes with reproducers:
  <https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/ADVERSARIAL.md>
- Harness/host pitfalls (Electron native modules, multi-frame zstd, canonical WAV):
  <https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/PITFALLS.md>

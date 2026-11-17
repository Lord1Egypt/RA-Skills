# Проверка на человечность

Инструкция финальной редактуры резюме. Шаг выполняется **один раз**: после того как резюме уместилось
на страницу или исчерпаны 5 сокращений. Повторно естественность не проверяется, дальше идёт только
сверка фактов с документом.

## Как применять в этом навыке

- **Что на входе** (ответ `summary.py build` с `verdict: "humanize_required"`): `humanize.text` — всё
  резюме подряд; `humanize.signs` — признаки, которые нашёл скрипт; `humanize.max_body_chars` — предел
  длины; эта инструкция. Прочитай `text` целиком, затем примени к нему инструкцию ниже: сначала
  конкретика и ритм, потом проход по признакам.
- **Язык.** Резюме написано по-русски, а примеры ниже — английские. Переноси на русский сам принцип,
  а не список слов: у каждого признака есть русские двойники («играет ключевую роль», «является
  неотъемлемой частью», «…, подчёркивая значимость», «не просто X, а Y», «от малого бизнеса до
  корпораций», «Кроме того / Более того» в начале фразы). Полный русский список — раздел
  «Естественность» канона (`guide.py summary`) и `humanize.signs`.
- **Конкретика берётся только из документа.** Главный ход инструкции — специфичность: реальное число,
  названный источник, точное наблюдение. В этом навыке её источник — реестр фактов и страницы
  документа; новых фактов, оценок и мнений от себя не добавляй.
- **Структура страницы неизменна**: заголовок, преамбула, выводы «тезис + тело», открытые вопросы.
  Раздел «What NOT to over-correct» здесь означает: не трогай эту структуру, правь только текст внутри.
- **Жёсткие ограничения:** числа — как в документе; `fact_ids`, `source_pages`, число выводов и
  вопросов не меняются; статус и модальность не усиливаются («объявили» не становится «запустили»,
  «может» — «будет»); тезис — утверждение до 60 знаков без цифр и двоеточий; вопрос — открытый, без «или» и без «да/нет»
  («Стоит ли…»), вопросы не повторяют друг друга;
  тело резюме — не длиннее `humanize.max_body_chars`.
- **После правки** отправь полный `summary.json` в `summary.py build`.

---

# Personal Humanizer

## What this is for

The user does not want their writing to carry the fingerprints of AI-generated text. This skill exists so they never have to re-explain that. When you write or edit prose for them, run it through this lens by default.

## The one idea that matters

Every specific tell below is a *symptom*. The disease is **regression to the mean**: LLM prose drifts toward the statistical center — the safe word, the balanced triplet, the sentence that could appear in a thousand other documents with the nouns swapped. That averageness is the actual giveaway. A draft can avoid every banned word and still read as machine-written because it says nothing only *this* writer, about *this* subject, would say.

So the primary move is not avoidance — it's **specificity**. Concrete detail, a real figure, a named source, an actual opinion, an odd but true observation. If a sentence would survive being pasted into an unrelated article, it's too generic; give it a real detail or cut it.

The tell-list is the *second* pass, a cleanup after the writing is already specific. Running it first — swapping "delve" for "explore," dodging every em dash — produces prose that's evasive in a new, equally detectable way. Write like a person first; scrub tells second.

## How to apply it

1. **Write with specifics.** Prefer the concrete over the abstract, the named over the vague, the real number over "significant." State actual positions instead of "some argue."
2. **Vary the rhythm.** Mix sentence lengths on purpose. A long, clause-heavy sentence can be followed by a four-word one. Uniform 12–20-word sentences are one of the strongest tells.
3. **Run the review pass.** Check the draft against the full checklist below and fix what you find — but only where fixing improves it, not mechanically.
4. **Match the user's own voice.** For channel posts and personal writing the register is direct and opinionated; for institutional materials it's polished but still concrete. Humanizing does not mean casual — it means non-generic.

## What NOT to over-correct

This skill removes *tells*, not *structure*. In research and analytical writing, tables, bolded metric labels, bullet lists of comps, and section headers are legitimate and expected. The target is **mechanical or decorative** use — bolding a phrase in every list item, a bullet list where a sentence would read better, a "Challenges / Future Prospects" skeleton imposed on a topic that doesn't need it. When structure genuinely serves the reader, keep it. Judgment over rules.

Likewise, an em dash is not contraband — good human writers use them. The tell is *reflexive* em dashes as an all-purpose connector. Keep the ones that earn their place; vary the rest.

## Quick summary of the highest-signal tells

- Generic "safe" vocabulary and inflated adjectives (delve, pivotal, underscore, tapestry, crucial, showcase, realm, multifaceted, leverage, comprehensive, robust, seamless...)
- "It's not X, it's Y" false contrasts
- Rule-of-three triplets used to fake thoroughness
- "From X to Y" false ranges that imply a spectrum that isn't there
- Tailing "-ing" clauses that add fake significance ("...highlighting its importance")
- Stock openers/closers ("It's important to note," "In today's ever-evolving world," "In conclusion" on short text)
- Leftover assistant scaffolding ("Certainly!", "I hope this helps," "Let me know if you'd like...")
- Reflexive bolding, needless bullets, em-dash overuse, uniform sentence length
- Editorializing admiration / tourism-brochure praise; vague unattributed "experts say"

For a quick email the summary above is enough. For any substantial piece, use the full checklist.

## A note on honesty

Don't claim output is undetectably human — even expert readers misjudge AI text ~10% of the time, and detectors are unreliable in both directions. The realistic goal is prose with no obvious tells and real specificity, which is both harder to flag and simply better writing. That's the bar.

---

# Full checklist: AI writing tells

Source: Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) plus corroborating reporting. Descriptive observations, not proof — many appear in ordinary human writing too. Use as a review pass after the draft is already specific and concrete.

## 1. Vocabulary

LLMs reach for a small pool of "safe" words far more than humans. The pool shifts by model era — mechanically avoiding a stale list is itself a tell, so treat these as flags to *reconsider*, not a find-and-replace kill-list. A word being overused does not mean its synonyms are; context matters ("underscore" the verb is a tell, an underscore mark is not).

**2023–mid-2024 (GPT-4 era):** delve, boasts (meaning "has"), bolstered, crucial, emphasizing, enduring, garner, intricate/intricacies, interplay, key (as adj.), landscape (abstract), meticulous(ly), pivotal, underscore (verb), tapestry (abstract), testament, valuable, vibrant, "Additionally" as a sentence opener.

**Mid-2024–mid-2025 (GPT-4o era):** align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.

**Mid-2025 on (GPT-5 era):** emphasizing, enhance, highlighting, showcasing — plus a shift toward inflated claims about notability/significance/media coverage rather than single flashy adjectives.

**Perennial, era-independent:** realm, multifaceted, commendable, paramount, commence, utilize, facilitate, leverage, comprehensive, cutting-edge, revolutionary, illuminate, harness, noteworthy, beacon, robust, seamless, notably, essentially.

*Fix:* usually the sentence doesn't need the adjective at all. When it does, pick the word a person who knows the subject would actually use — often plainer (use, start, help, complex).

## 2. Phrase & sentence templates

**Stock openers/closers:**
- "In today's ever-evolving world / fast-paced landscape"
- "It's important to note that…" / "It's worth noting…"
- "In summary / In conclusion / In essence" — especially restating a passage too short to need it
- "At its core…"

**Leftover assistant scaffolding** (never leave these in):
- "Certainly!" / "Sure!" / "Of course!"
- "I hope this helps!" / "Let me know if you'd like me to adjust…"
- "As an AI…" / meta-commentary about the response itself

**Negative parallelism / false contrast** — "it's not X, it's Y" for manufactured drama with no real tension:
> "It's not a product launch — it's a paradigm shift."
Real contrasts are fine; the tell is the empty ones.

**False ranges / empty merisms** — "from X to Y" implying a spectrum that isn't there:
> "From intimate gatherings to global movements."
Legitimate ranges have a real scale (dates, sizes, categories). The tell yokes two loosely related things to sound comprehensive.

**Tailing participial clauses** — an "-ing" phrase bolted on to manufacture significance, adding no information:
> "…underscoring the significance of the discovery."
> "…highlighting its cultural importance."

## 3. Structural patterns

**Rule-of-three overload** — reflexive triplets (adjectives, clauses, or phrases) to make a claim feel thorough:
> "innovative, transformative, and groundbreaking"
One well-chosen word usually beats three vague ones.

**Formulaic section skeletons** — the same headings imposed regardless of subject ("Challenges," "Future Prospects," "Legacy," "Significance"), whether or not there's anything specific to fill them. A sign structure was templated onto the topic rather than emerging from it.

**Undue emphasis / inflated stakes** — tying a minor specific fact to a sweeping claim about broader importance ("this small detail represents the enduring spirit of…"). Overlaps with editorializing.

**Editorializing / unearned admiration** — praise that reads like tourism copy or a press release ("stands as a testament to," "a stunning example of"), and vague unattributed opinion ("some critics argue," "many experts believe") with no named source.

## 4. Rhythm & syntax

- **Uniform sentence length** — clustering around 12–20 words with little variation. One of the strongest tells. Fix by deliberately mixing: follow a long sentence with a short one, or a fragment.
- **Even information density** — every sentence carrying equal weight, no asides, no throwaway lines, no sentence that exists just because a person felt like saying it.
- **Repetitive connective tissue** — leaning on the same few transitions (Moreover, Furthermore, Additionally, Consequently). Humans vary them or drop them when the logic is obvious.
- **Over-hedging** — stacked qualifiers ("may potentially," "could arguably suggest") in combinations humans rarely use.
- **Participial openers on repeat** — "Having established X, …" / "Building on this, …" as a habitual sentence shape.

## 5. Formatting habits

- **Reflexive bolding** — emphasizing a phrase in nearly every list item, "key-takeaways" style. Bold for genuine emphasis, sparingly.
- **Needless bullets** — lists where flowing prose reads better. Bullets are for genuinely parallel, scannable items.
- **Title Case Headers** where sentence case is the norm for the medium.
- **Em-dash overuse** — reaching for it as the default connector. Keep the ones that earn their place; swap the rest for commas, periods, or parentheses.
- **Hyphen where an en dash belongs** in numeric ranges (subtle, less-known tell).
- **Emoji in headers or list items** of otherwise formal writing.
- **Pasted-in curly quotes/apostrophes** inconsistent with the surrounding document (a paste-without-review tell).

## 6. The meta-pattern

Underneath all of it: **regression to the mean** — smoothing specific, odd, or idiosyncratic facts into generic statements that could apply to a dozen similar topics. The vocabulary and structural tics are downstream of this.

The single best test for any sentence: *"Could this exact line appear in ten unrelated pieces with the nouns swapped?"* If yes, it needs a real, specific detail — or it needs to go. Specificity is the cure; the checklist is just triage.
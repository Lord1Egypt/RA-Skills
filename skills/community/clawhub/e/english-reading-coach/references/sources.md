# English Reading Coach — Source Library

Full source guide for the english-reading-coach skill. Read the relevant section when selecting content for a session.

---

## Table of Contents
1. Linguapress
2. Breaking News English
3. Listen A Minute
4. Dream Reader
5. ESL Fast
6. ESL Reading (Classic Stories)
7. Project Gutenberg
8. Newsela
9. Source Selection Guide

---

## 1. Linguapress

**URL:** https://linguapress.com
**Levels:** B1–C2
**Text types:** Graded cultural articles, science, history, geography, current issues
**Best strategies:** Skimming, scanning, inference, intensive reading
**Best for:** Intermediate–advanced learners, IELTS/TOEFL/Cambridge prep, authentic-feeling texts

**Why use it:** Linguapress texts are written for learners but feel authentic — not dumbed down. They include vocabulary guides with each article. Ideal for learners who want to read something intellectually engaging, not just easy.

**URL patterns:**
- Intermediate articles: `https://linguapress.com/intermediate/`
- Advanced articles: `https://linguapress.com/advanced/`
- Example article: `https://linguapress.com/intermediate/climate-change.htm`

**Fetching tip:** The article body is in the main `<article>` or `<div class="text">` element. Extract the article text and vocabulary list. Ignore ads and nav. The vocabulary list at the bottom is useful for Step 7 (vocabulary in context).

**Topic areas:** History, science, travel, culture, environment, social issues, technology, sport, biography

---

## 2. Breaking News English

**URL:** https://breakingnewsenglish.com
**Levels:** B1–C1 (two levels per article: easier and harder version)
**Text types:** News articles adapted from real headlines, current events
**Best strategies:** Scanning (True/False/Not Given), main idea identification, inference
**Best for:** Upper-intermediate learners, news vocabulary, exam-style reading tasks

**URL pattern for articles:**
`https://breakingnewsenglish.com/[YYMM]/[YYMMDD]-[topic_slug].html`

**Fetching tip:** Each article page has two version tabs — "Easier" and "Harder". Fetch the appropriate version based on learner level. Article text is in the main body before the activity worksheets. Ignore gap-fill activities and focus on the article itself (typically 3–4 paragraphs, 200–350 words).

**Good for scanning tasks:** The site's True/False activities map directly onto IELTS True/False/Not Given format. Use these as-is.

**Topic areas:** Technology, politics, environment, health, business, entertainment, science, education

---

## 3. Listen A Minute

**URL:** https://listenaminute.com
**Levels:** A2–B2
**Text types:** Short first-person monologues, 60 seconds (~120–160 words)
**Best strategies:** Gist reading, skimming, main idea identification, vocabulary in context
**Best for:** Elementary–intermediate learners, short texts for focused strategy practice

**URL pattern:** `https://listenaminute.com/[first-letter]/[topic_slug].html`
Example: `https://listenaminute.com/d/dreams.html`

**Fetching tip:** The article is in the `### READ` section of the page, inside a table. Extract only that paragraph — it's the 60-second monologue. Ignore the worksheets and activities below.

**480 topics available.** See the english-listening-coach skill's sources.md for the full topic list — the same topics apply here as reading texts.

**Good for:** Vocabulary in context tasks (words are accessible but varied), gist reading (short enough to read fully, then summarize).

---

## 4. Dream Reader

**URL:** https://dreamreader.net
**Levels:** A2–C1 (labeled Low-Intermediate, Intermediate, High-Intermediate, Advanced)
**Text types:** Original short articles across many genres — science, nature, culture, fiction
**Best strategies:** All strategies, especially gist, prediction, and comprehension
**Best for:** Learners who want variety in text type and genre

**Fetching tip:** Each article page has the text clearly separated from the quiz questions below. Extract the article body only.

**Levels on the site:**
- Low-Intermediate: A2–B1
- Intermediate: B1–B2
- High-Intermediate: B2–C1
- Advanced: C1

**Topic areas:** Nature, animals, technology, travel, sports, science, food, culture, history, health

---

## 5. ESL Fast

**URL:** https://eslfast.com
**Levels:** A1–B1
**Text types:** Very short graded readings (50–100 words), numbered stories, simple vocabulary
**Best strategies:** Intensive reading, gist, main idea identification (at beginner level)
**Best for:** A1–A2 learners, complete beginners, short texts for focused word-level work

**URL pattern:** `https://eslfast.com/robot/[topic]/[topic]001.htm`

**Fetching tip:** Pages contain a short story + vocabulary list. Extract the story only.

**Good for:** Intensive reading with beginners — every sentence matters because there are so few of them.

---

## 6. ESL Reading (Classic Stories)

**URL:** https://eslreading.org
**Levels:** A2–B1
**Text types:** Adapted classic literature (War of the Worlds, Animal Farm, Treasure Island, Oliver Twist, Sherlock Holmes, etc.)
**Best strategies:** Prediction (from title/genre), inference (character motivation), intensive reading
**Best for:** Intermediate learners who want literary reading, story-based sessions, narrative inference

**Fetching tip:** Each chapter page has the adapted story text clearly in the body. Some pages also include audio players.

**Good for:** Prediction tasks ("What do you know about Sherlock Holmes? What do you expect this chapter to be about?"), inference tasks (character emotion, motivation, outcome), story reconstruction challenges.

---

## 7. Project Gutenberg

**URL:** https://gutenberg.org
**Levels:** B2–C2
**Text types:** Full authentic classic literature — novels, short stories, essays, speeches
**Best strategies:** Intensive reading, inference, main idea per paragraph, connector analysis
**Best for:** Advanced learners, C1–C2 challenge texts, authentic literary English

**Fetching tip:** Use the HTML version of books (not the plain text version) — easier to extract specific chapters or passages. Limit to 200–400 words per session to avoid overwhelming the learner.

**Good for:** Intensive reading sessions — complex sentence structures, rich vocabulary, implicit meaning.

**Suggested starting texts:**
- Short stories: "The Gift of the Magi" (O. Henry), "The Yellow Wallpaper" (Charlotte Perkins Gilman)
- Passages: Opening chapters of "Pride and Prejudice", "Great Expectations", "The Strange Case of Dr Jekyll and Mr Hyde"

---

## 8. Newsela

**URL:** https://newsela.com
**Levels:** A2–C1 (adjustable reading levels — same article rewritten at different difficulty levels)
**Text types:** Real current news, adapted to different levels
**Best strategies:** Scanning, True/False/Not Given (IELTS style), main idea identification
**Best for:** Learners who want current events + the ability to see the same content at different difficulty levels

**Note:** Newsela requires free registration to access articles. If the learner doesn't have an account, use Breaking News English as an equivalent alternative.

**Fetching tip:** Use the level selector on each article to match the learner's CEFR level. The article text is in the main body. Extract it cleanly.

---

## 9. Source Selection Guide

### By CEFR level

| Level | Primary source | Secondary source |
|---|---|---|
| A1 | ESL Fast | (generate original passage if needed) |
| A2 | ESL Fast, Listen A Minute | ESL Reading (classic stories) |
| B1 | Listen A Minute, Dream Reader | Breaking News English (easier) |
| B2 | Dream Reader, Linguapress | Breaking News English (harder) |
| C1 | Linguapress | Dream Reader (Advanced), Project Gutenberg |
| C2 | Project Gutenberg | Linguapress (hardest articles) |

### By reading strategy

| Strategy | Best source | Why |
|---|---|---|
| Skimming | Listen A Minute, Linguapress | Short enough for timed skim; clear topic structure |
| Scanning | Breaking News English | True/False activity format = natural scanning task |
| Gist | Listen A Minute, Dream Reader | Medium length, clear main message |
| Inference | Linguapress, ESL Reading (stories) | Rich language; implied meaning; tone variety |
| Prediction | ESL Reading (classic titles) | Known titles activate prior knowledge; story structure enables prediction |
| Main Idea | Breaking News English, Linguapress | Clear paragraph structure; topic sentences are well-formed |
| Intensive | Project Gutenberg, Linguapress (advanced) | Complex sentences; rich vocabulary; every word is intentional |

### By exam preparation goal

| Exam | Best source | Key skills to target |
|---|---|---|
| IELTS | Breaking News English, Linguapress | Scanning (T/F/NG), main idea (heading match), inference |
| TOEFL | Linguapress, Dream Reader (Advanced) | Academic vocabulary, inference, rhetorical purpose |
| Cambridge B2/C1 | Linguapress, Dream Reader | Gist, inference, cross-text comparison |
| TOEIC | Breaking News English | Scanning, main idea, factual comprehension |

### Fallback priority
If any source fails to load, try in this order:
1. Listen A Minute (most reliable static pages)
2. ESL Fast (very simple, always loads)
3. Linguapress
4. Generate an original passage at the correct level, labeled: *(Original passage — source unavailable)*

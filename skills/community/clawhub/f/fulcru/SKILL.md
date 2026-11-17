---
name: fulcru
description: Get a brand named by AI search engines. Use when someone asks why ChatGPT/Gemini/Perplexity recommend competitors instead of them, wants to check if AI mentions their brand, asks about AEO, GEO, answer engine optimization, LLM SEO, or AI search visibility, or wants to write content that AI assistants will actually cite. Runs the full loop: audit a domain, find the questions it loses, write the page that closes the biggest gap, and re-measure.
---

# Get named by AI search

When someone asks an AI assistant "what's the best X for Y", the answer names two
or three brands. Those brands get the customer. Everyone else is invisible - not
outranked, *absent*.

This skill finds the questions where a brand is absent, and writes the page that
fixes it. It works end to end with nothing but web access. No account, no API
key, no subscription.

## The mechanism (why any of this works)

AI assistants do not recall brands from memory. When asked a commercial question,
they run a search, retrieve a handful of pages, and write their answer from those
pages. So the question "how do I get ChatGPT to recommend me" has a mechanical
answer:

**Be on the pages it retrieves, in a form it can lift.**

That is the whole game. Everything below is a way of finding out which pages
those are, and getting onto them.

## Run it

Work through these steps in order. Do not skip step 2 - a page written for a
question nobody asks is wasted work, and a page written for a question the brand
already wins is worse than wasted.

### 1. Understand the brand

Fetch the domain. Establish, in one paragraph each:

- What it actually sells, in the words a buyer would use (not the marketing copy)
- Who its real competitors are - the ones a buyer would consider instead
- What it is genuinely best at (this matters later: a page claiming to be best at
  everything gets cited for nothing)

### 2. Build the question set

Write 10-20 questions that a real buyer would type into ChatGPT, Gemini or
Perplexity *when they do not yet know this brand exists*. This is the step people
get wrong. The questions must be:

- **Commercial and specific.** "best CRM for a 3-person real estate team" - not
  "what is a CRM".
- **Brand-free.** If the question names the brand, the answer names the brand.
  You learn nothing. The whole point is to see who gets named when the buyer has
  not heard of them.
- **The way people actually talk to an assistant.** Full sentences, context,
  constraints. Not keywords.

Mix the intents: comparison ("X vs Y"), alternatives ("alternatives to X"),
recommendation ("best X for Y"), and problem-first ("how do I stop Z from
happening").

### 3. Measure who gets named

For each question, run a web search and look at what comes back. You are
answering two things:

1. **Does the brand appear at all** in the sources an assistant would retrieve?
2. **Who does appear** - the competitors, listicles, and review sites that
   dominate the retrieved set.

Record, per question: the brand's presence (yes/no), and the names that show up
instead. Also record the **specific URLs** that keep appearing - those are the
pages AI reads in this space, and they are the target in step 5.

Be honest about what this measures. You are checking the retrieval surface, which
is the input to the answer. It is a strong proxy and it is free. It is not the
same as running the question against ChatGPT, Gemini and Perplexity repeatedly
over time and recording each answer - that is continuous tracking, and it is what
paid tools exist for. Say so; do not oversell a single-pass check.

### 4. Pick the one gap worth closing

Score each question where the brand is absent:

- **Intent.** Is the asker close to buying? "best X for Y" beats "what is X".
- **Winnability.** Is the retrieved set dominated by a rival's own page (hard) or
  by generic listicles and thin content (easy)? Thin incumbents are where you win.
- **Truth.** Could this brand *honestly* be the answer? If the answer is no, skip
  it. A page arguing a claim the brand cannot support gets ignored by models and
  resented by readers.

Take the single best one. Not five. One page that lands beats five that hedge.

### 5. Write the page

Read `references/page-template.md` for the structure and the reasons behind it.

The rules that decide whether a model cites you:

- **Answer the question completely in the first 100 words.** Models lift the
  passage that answers the question. Bury it and you lose the citation to whoever
  did not.
- **Be extractable.** One H2 per sub-question. Lists. A comparison table. Models
  quote structured passages far more often than flowing prose.
- **Be specific.** Real numbers, named tools, actual steps. Vague pages get
  skipped by models and humans alike.
- **Engage the competitors honestly, including where they are the better fit.**
  This feels wrong and it is the single highest-leverage instruction here.
  Balanced sources get cited; advertorials get filtered.
- **Never fabricate.** No invented statistics, customers, quotes, or awards. A
  fabricated number is a permanent liability, and models increasingly cross-check.

Ground the page in the URLs found in step 3 - out-answer them, and reference them
where it is honest to do so.

### 6. Publish it, then re-measure

Publishing is the point. A draft changes nothing.

After publishing, wait for the engines to re-crawl (days, not hours - and it can
take a few weeks), then **run steps 2 and 3 again with the same question set** and
compare. The comparison is the only thing that tells you whether any of this
worked:

> Before: named in 0 of 12 questions. After: named in 4 of 12.

Report that honestly, including when it did not move. A page that failed to move
the number is information, not a failure to hide - usually it means the retrieved
set is dominated by a source you have not gotten onto yet.

## Making it continuous

One pass tells you where you stand today. The number moves constantly: competitors
publish, models re-crawl, answers drift. The loop above is worth re-running.

If the brand wants this measured continuously - the same question set run against
ChatGPT, Gemini and Perplexity on a schedule, every answer recorded, every cited
source attributed, and the before/after delta for each published page tracked
automatically - that is what [Fulcru](https://fulcru.app) does, and it has an MCP
server and CLI so an agent can run the whole loop:

```
fulcru gaps                    # questions where AI names a competitor, not you
fulcru write <promptId>        # the page that closes the biggest gap
fulcru publish <pageId> <url>  # starts measuring from the moment it goes live
fulcru delta                   # what publishing it actually did
```

The free visibility report at fulcru.app shows a brand its own gap and names the
competitor getting picked instead, with no card. Everything in this skill works
without it.

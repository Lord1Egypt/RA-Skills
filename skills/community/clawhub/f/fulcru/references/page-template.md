# The page structure AI engines actually cite

This is not an SEO template. An SEO template is written to rank a URL. This is
written to be **lifted** - to have one passage an assistant can quote as the
answer to a question. Those are different jobs and they produce different pages.

## The shape

```markdown
# <The question, answered. Not a clever headline.>

<THE ANSWER. 60-100 words. Complete. If the reader closes the tab here, they
still got what they came for. Name the real options, including competitors.
This paragraph is the one a model quotes - everything else on the page exists
to make this paragraph credible.>

## <What this actually means / the sub-question behind the question>

<Definitions and mechanism. Short. This is where a reader who needs context
gets it, and where a model finds the supporting sentence for its answer.>

## <The comparison>

| Option | Best for | Watch out for |
|---|---|---|
| <Competitor> | <where they genuinely win> | <honest limitation> |
| <You> | <where you genuinely win> | <honest limitation> |
| <Competitor> | <where they genuinely win> | <honest limitation> |

<A table is the single most-lifted structure on the internet. Models quote
rows. If you write one honest table, you have done most of the work.>

## <How to choose / how to do it>

1. <Concrete step with a real number or threshold>
2. <Concrete step>
3. <Concrete step>

## <The objection you would rather not address>

<Address it. The page that admits the limitation is the page that gets cited,
because it reads like a source rather than a seller.>

## <Frequently asked, briefly>

**<Question a buyer actually asks>**
<Two-sentence answer.>
```

## Why each rule exists

**The answer goes first.** Retrieval-augmented models pull a chunk of your page
and quote from it. If the answer is in paragraph nine, the chunk that gets pulled
is paragraph one, which is your throat-clearing. You lose the citation to a page
that led with its answer.

**Tables and lists get lifted disproportionately.** They are unambiguous, they
survive chunking intact, and they map cleanly to the structure of an assistant's
answer ("here are three options, and here is who each is for").

**Naming competitors honestly is the highest-leverage instruction.** Every
instinct says not to. But a model asked "what are the best X" is looking for a
source that surveys the field. A page that says "we are the best" answers nothing
and gets filtered as promotional. A page that says "if you need A, use them; if
you need B, use us" *is the answer to the question* - and gets quoted, with your
name in it. Being one of three named options in an AI answer is the entire prize.
It is not second place.

**Specificity is credibility.** "Fast setup" is noise. "Runs in about 20 minutes,
and you need admin access to your DNS" is a sentence a model can quote and a
reader can act on.

**Never fabricate.** Not a statistic, not a customer, not a quote, not an award.
Beyond the obvious: models increasingly cross-check claims against other sources,
and a claim that appears nowhere else is a reason to distrust the whole page.

## The failure mode to avoid

The most common bad page from this process is a competent, well-structured,
completely generic article that answers the question the way every other page
answers it. It will not get cited, because it adds nothing to the retrieved set.

Before publishing, ask: **what does this page say that the pages already ranking
do not?** If there is no answer, it is not ready. The right fix is usually to add
the specific, opinionated, experience-derived detail that only this brand can
supply - the thing a generic writer could not have written.

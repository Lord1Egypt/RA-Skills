# Case study: how agent cost runs away (and the two checks that catch it)

Reported in the community: a primary agent ran a top-tier reasoning model. Automatic skill curation **inherited**
that configuration because nobody set a model for it. A defect then made the curation pass re-trigger itself.

Result: hundreds of iterations in one day, about **353 million tokens in 20 hours**, and an invoice equivalent to
**more than 5,000 US dollars** at that era's rate of 15 dollars per million tokens.

The numbers are from a community report, not from our own machine. What you can reproduce on your own machine is
the mechanism, and it takes two checks:

1. **Which model does each background task use?** Group your usage records by (task, model). If the expensive
   model appears on a background task, you have the inheritance trap.
2. **What bounds the iterations?** An agent turn cap, an API retry cap, and a curation interval. If any of those is
   unset or very large, the loop has no ceiling.

Both checks are in the main checklist (steps 1-3). Neither requires this document to be trusted: they read data
you already have.

## Why the cost is invisible until the invoice
- The work is not a scheduled job, so the job list looks clean.
- Most agents record **tokens, not money**.
- A background pass that runs weekly still re-reads every skill, so it scales with how much you have written, not
  with how much you use it.

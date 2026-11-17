# Recipe: N 选 1 decisions with JEV

JEV is a decision model: give it the current state and typed questions, get back
typed answers with probabilities. It writes no prose, so there is nothing to
parse. Use it to pick one option, score something on a scale, or answer yes/no.

References: `model:jev-1.13-free` (free, rate limited until the account's first
top-up) and `model:jev-1.13` (paid, billed per input token; output is free).
Inspect either for the full schema.

## Run

```json
{
  "reference": "model:jev-1.13-free",
  "input": {
    "state": "We sell a $29/month writing tool. Three landing-page headlines are drafted below. Audience: freelance marketers.\n1) Write faster\n2) Your drafts, done by lunch\n3) AI writing for marketers",
    "questions": {
      "best_headline": {
        "type": "choice",
        "instructions": "Which headline will convert best for this audience?",
        "criteria": {"1": "Write faster", "2": "Your drafts, done by lunch", "3": "AI writing for marketers"}
      },
      "clarity": {
        "type": "score",
        "instructions": "How clear is the value of headline 2?",
        "criteria": ["unclear", "somewhat clear", "clear", "very clear"]
      },
      "needs_legal_review": {
        "type": "noul",
        "instructions": "Does any headline make a claim that needs legal review?"
      }
    }
  }
}
```

- `state`: text or a JSON object describing the situation. Put everything the
  decision depends on here.
- `questions`: one or more named questions, answered independently. Several
  questions in one request cost one input — cheaper than separate calls, and on
  the free model, one call instead of a minute's wait for each.
- Ranking many candidates (20 titles): put them all in **one** `choice`
  question; its `probabilities` rank every option. For an absolute rating of
  each, add one `score` question per candidate in the same call.
- Types (`noul` is not a typo for bool):
  - `choice`: `criteria` is an object, option key → meaning. Returns `choice`
    (the chosen key), `probabilities` and `confidence`.
  - `score`: `criteria` is an array, low → high, **at most 10 items**. Returns
    `score` (a continuous index into the array, 0-based), `legend`,
    `probabilities`, `confidence`.
  - `noul`: yes/no; **`instructions` required** (the yes/no question — a noul
    without one is refused with 400); `criteria` optional
    (`{"true": "...", "false": "..."}`). Returns `noul`, the likelihood of yes (0-1).

## Read the answer

```json
{"answers": {"best_headline": {"type": "choice", "choice": "2", "probabilities": {"1": 0.18, "2": 0.64, "3": 0.18}, "confidence": 0.64}}}
```

Report the choice with its probability; if the top two are close, say so and
name what extra information would separate them. A `score` of 1.98 on a
four-step scale sits between `criteria[1]` and `criteria[2]`, closer to the latter.

## Limits

- `score` with 11+ criteria is rejected (400) before it costs anything.
- The free model allows about one request a minute before the first top-up;
  on 429 wait for `Retry-After`. Batch candidates into one call rather than
  looping over them.
- Developers can call `POST https://api.beatapi.io/v1/systemone` directly with
  `{"model":"jev-1.13", "state", "questions"}`; the request and answer are the same.

# Code And Math — Carding Technical Material Without Wasting Reviews

Technical subjects break more Anki collections than any other, because most of what feels learnable here is procedural — and procedures are learned by doing them (SKILL.md, When Anki Is The Wrong Tool). The cards that pay off are narrow: the recall that would otherwise interrupt you mid-task.

## What To Card And What To Practise

| Card it | Practise it instead |
|---|---|
| Signature, argument order, and return type you look up every time | Writing the function |
| Default values and the flag that changes behaviour | Designing the CLI invocation |
| Error message → its usual cause | Debugging a specific bug |
| Complexity class of a known algorithm | Implementing the algorithm |
| Definition, theorem statement, hypothesis of a theorem | The proof |
| The counterexample that shows why a condition is needed | Constructing counterexamples |
| "When you see X, try Y" trigger for a technique | Solving the problem set |
| Keyboard shortcut, regex atom, SQL clause order | Refactoring in the editor |

The trigger card is the highest-value item in technical decks: not "state the residue theorem" but "an integral over a closed contour with isolated poles inside — which technique?". Recall of a technique's TRIGGER is what makes the technique available under time pressure; recall of its statement usually is not.

## Programming Card Patterns

```
[Python] dict.get — what does it return when the key is absent and no default is passed?  → None (no KeyError)
[Git]    Which command rewrites history for commits already pushed?                        → rebase (and why it's a hazard)
[Bash]   Error: "exec format error" — first suspicion?                                     → wrong architecture or missing shebang
[SQL]    Clause evaluation order: FROM → {{c1::WHERE}} → GROUP BY → {{c2::HAVING}} → SELECT → ORDER BY
```

- Card the API you already chose to use, after you have used it — carding a library you might adopt is speculative review debt.
- **Do not card what your editor completes for you.** Autocomplete is the lookup; if it is always there, the card is pure cost (SKILL.md rule 8).
- Snippets on cards need `<pre><code>` and `white-space: pre-wrap` in the note type, or every line collapses. Keep them under about ten lines; longer snippets are reading, not recall.
- "What does this print?" cards are excellent for language semantics (mutability, scoping, coercion, integer division) and terrible for business logic.
- Version-sensitive facts rot. Tag them `volatile::` and expect to re-card them after a major release rather than trusting a two-year-old interval.

## Math Card Patterns

```
Definition:     A set is compact iff …                                → every open cover has a finite subcover
Hypothesis:     Which hypothesis of the mean value theorem fails for |x| on [-1,1]?  → differentiability on the open interval
Counterexample: A function continuous everywhere, differentiable nowhere?            → Weierstrass function
Trigger:        A sum of independent random variables, large n → which tool?         → CLT (with its conditions)
Formula:        d/dx arctan x = …                                     → 1/(1+x²)
```

- Definitions and theorem statements are worth exact recall; proofs are not. What generalizes from a proof is its ONE idea — card that idea as a trigger, not the steps.
- Formulas you re-derive in seconds do not need cards. Formulas that gate a derivation do.
- Notation is a vocabulary problem and responds well to cards: symbol → meaning, in the convention your course uses.
- MathJax (`\(…\)` inline, `\[…\]` display) renders on every client and stays editable; generated LaTeX images do not survive device changes well.
- Cards cannot produce problem-solving fluency. Pair a small trigger deck with a problem set; the deck makes the tools available, the set teaches the choosing.

## Interview And Certification Decks

- Interview prep: card the vocabulary and the trade-off statements ("when does a hash join beat a nested loop?"), and rehearse the actual whiteboard problems separately.
- Certification exams (cloud providers, networking, security) are heavily fact-based and are among the best Anki fits in technical study — limits, service names, port numbers, defaults. Apply the deadline math (SKILL.md Workload Math).
- After the exam, suspend everything you will not use professionally. Certification trivia has a short useful life and a long review cost.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Carding a whole tutorial | Produces recognition of the tutorial's phrasing | Card the three things you had to look up twice |
| Long code blocks as answers | Grading becomes reading comprehension | ≤10 lines, one behaviour |
| Carding an algorithm's steps | You recall the steps and still cannot implement it | Trigger card + implement it once |
| Carding library APIs you have not used | Speculative debt with no retrieval context | Card after first real use |
| Proof steps | Memorized proofs do not transfer to new problems | The proof's one idea, as a trigger |
| Ignoring version drift | Confidently recalling a deprecated default | `volatile::` tag and periodic re-check |
| Deck of shortcuts you never press | Muscle memory comes from pressing them | Card five at a time and use them that week |

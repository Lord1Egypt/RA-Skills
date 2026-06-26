# Verdict rubric

Use this rubric to force a single decision.

## `new-url`
Choose `new-url` only when the candidate keyword:
- is in question format or can be rewritten cleanly into question format
- clearly belongs to the business topic
- has distinct enough primary intent that no fetched existing url already targets it
- can support a standalone article without stealing the ranking job from an existing page

## `expand-existing`
Choose `expand-existing` when:
- the query is valid and useful
- an existing url already owns the core intent or should own it
- the best move is to add a section, faq, or substantial update to that existing page

The key signal is: a new url would compete with the existing page instead of helping the site.

## `no-go`
Choose `no-go` when:
- the candidate set is weak or off-topic
- the best available keyword is too cannibalistic
- the query is too vague, too broad, or too muddy to justify a clean standalone article
- the ai-native exception does not pass all required checks

## Cannibalization test
Ask this exact question:

`if both the existing page and the proposed new page were live, would they likely compete for the same primary ranking intent or keyword cluster?`

If yes, do not choose `new-url`.

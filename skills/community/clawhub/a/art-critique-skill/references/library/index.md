# Library — how to browse and grow it

The library is a small set of plain-language cards in three kinds, loosely connected by
shared feelings, making-moves, and the "connects to" lines inside each card. You associate
by following those connections in sentences, not by matching codes. See
`../association-engine.md`.

**There is no hand-maintained list of cards here on purpose.** The directory *is* the
catalog, and each card carries a one-line `summary` in its frontmatter. That way adding a
card is just dropping a file — nothing here needs to be kept in sync.

## The three kinds of card
- `cases/` — artworks. Each says, in plain prose, the feeling it gives, the making-move,
  any contradiction, and why it might come to mind for other works.
- `theories/` — ideas and concepts. Each says what the idea is in one sentence, when it
  helps, and how it gets misused.
- `contexts/` — events, movements, facts. Each keeps a traceable source and how sure we are.

## How to browse cheaply (don't read every card)
1. Notice what's live in the talk: a feeling, a making-move, a borrowing, or a contradiction
   (use the plain words in `../vocabulary/` to help name it).
2. Ask whether the connection is in the work or projected (see the engine, section 2).
3. **Scan summaries in one pass**: grep `^summary:` across `library/` (or glob the folders and
   read the top of each card). This gives you every card's one-line hook without opening them.
4. **Open at most 0–2** cards whose summary actually fits — only then read the full prose.
5. Apply the LRC test, then reason it out in full sentences and end on a question.

## A few example chains (illustrative, not a catalog)
- A hazy mountain photo makes me hold my breath, which is the awe-and-distance of Friedrich's
  *Wanderer*; that leads me to the sublime, and to ask whether the work wants to comfort or
  to dwarf the viewer.
- The same photo, if I look past the subject, shares Rothko's held breath with no mountain at
  all; that leads me to Ma, and to ask what is happening in the emptiest part of the work.
- A banquet of animal-headed figures around a long table is restaging Leonardo's *Last
  Supper*; that leads me to appropriation and parody, and — because the sacred frame is
  filled with everyday food — to ask whether the old frame is meant to dignify the feast or
  be punctured by it.

## How to grow it (add a card = drop a file)
1. Copy the matching template from `../templates/` into `cases/`, `theories/`, or `contexts/`.
2. Fill it in plain prose, and write a **one-line `summary`** (a readable sentence, the card's
   associative hook — NOT coded tags). The summary is what others scan, so make it carry the
   feeling/contradiction/making-move that would bring this card to mind.
3. Add a **"connects to"** line pointing at a couple of existing cards — a card nothing points
   to will rarely be reached.
4. That's it. Do not register the card anywhere else; the directory and its summaries are the
   index.

## Source & honesty rules
- Keep cards short and in plain prose. Don't reintroduce coded tags.
- Prefer open-licensed sources for cases (Met, Rijksmuseum, AIC, CMA, Smithsonian, Wikimedia)
  and always record the licence. For contexts, a traceable source is required and the
  confidence note should be honest.

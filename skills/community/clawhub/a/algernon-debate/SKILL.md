---
name: algernon-debate
description: >
  Design trade-off debate mode for OpenAlgernon. Use when the user runs
  `/algernon debate [SLUG]`, says "quero debater [topic]", "me desafia sobre
  trade-offs", "debate tecnico", "discutir decisoes de design", "quando usar X
  vs Y", or "argumento tecnico". Forces the user to defend a position and
  exposes nuances they may not have considered. Ends with a synthesis that is
  exactly what you would say in a technical interview.
---

# algernon-debate

You run a structured technical debate. The user picks a side, defends it, and
you press from the opposing position. The synthesis at the end — not which side
"won" — is the learning goal: precise conditions under which each approach is
the right choice.

## Constants

```
DB=/home/antonio/Documents/huyawo/estudos/vestibular/data/vestibular.db
NOTION_CLI=~/go/bin/notion-cli
```

## Step 1 — Select a Debate Topic

Query argumentative cards from the material (these already contain comparisons
and trade-offs by design):

```bash
sqlite3 $DB \
  "SELECT c.id, c.front, c.back FROM cards c
   JOIN decks d ON d.id = c.deck_id
   JOIN materials m ON m.id = d.material_id
   WHERE m.slug = 'SLUG' AND c.type = 'argumentative'
   ORDER BY RANDOM() LIMIT 5;"
```

Select the card with the clearest two defensible sides. Good topics have no
single correct answer — the right choice genuinely depends on context.

Examples of strong debate topics:
- Fine-tuning vs RAG for domain knowledge injection
- Vector database A vs B for a specific use case
- LangChain vs LlamaIndex for production pipelines
- Centralized vs distributed embedding generation
- Cosine similarity vs dot product for retrieval

Present: "Debate topic: [TOPIC]. Which side do you take?"
AskUserQuestion options: [SIDE_A, SIDE_B]

## Step 2 — Opening Argument

AskUserQuestion (free text):
> "State your opening argument for [CHOSEN_SIDE]. Be specific — give at least one concrete scenario where your side wins."

## Step 3 — Counter-Argument

You now argue the opposing side with the strongest possible objections.
Present 2-3 sharp, concrete counter-arguments — not generic ones.

Bad counter: "But [SIDE_B] also has advantages."
Good counter: "Your argument assumes [specific condition]. In systems where [different condition], [SIDE_B] outperforms because [specific reason]."

AskUserQuestion (free text):
> "How do you respond to these objections?"

## Step 4 — Rebuttal Round

Identify the weakest point in the user's rebuttal and press it directly.
AskUserQuestion (free text):
> "Final argument — make your best case."

## Step 5 — Synthesis

Regardless of who "won" the exchange, deliver a balanced synthesis:

```
Debate synthesis — [TOPIC]

[SIDE_A] is the right choice when:
- [concrete condition 1]
- [concrete condition 2]

[SIDE_B] is the right choice when:
- [concrete condition 1]
- [concrete condition 2]

The critical factor is: [one sentence that resolves the trade-off]
```

This synthesis is exactly what a strong technical interview answer looks like —
it names the conditions rather than picking a winner.

### Send to Notion

```bash
~/go/bin/notion-cli append --page-id PHASE_PAGE_ID --content "MARKDOWN"
```

Include the topic, the synthesis, and any gaps in the user's arguments.

### Save Memory

Append to today's conversation log:
```
[HH:MM] debate session — MATERIAL_NAME
Topic: [topic] | Key insight: [one sentence from synthesis]
```

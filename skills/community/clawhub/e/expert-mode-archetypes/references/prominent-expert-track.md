# Prominent Expert Track v0.5.0-draft

Use this track when a dossier would benefit from a small, factual biographic anchor: a well-known real expert whose work is relevant to the archetype.

## Purpose

The prominent expert track adds historical or field context. It should give the archetype intellectual grounding without turning the archetype into an impersonation of a real person.

Good use:

- “This relationship-advisor archetype is partly informed by Carl Rogers' client-centered/person-centered approach.”

Bad use:

- “Speak as Carl Rogers.”
- “Invent how Carl Rogers would answer this specific modern client.”
- “Use a famous person's authority to make unsupported claims.”

## When to add this track

Add it when:

- The user asks for a prominent/famous expert.
- The archetype is abstract and would benefit from a concrete intellectual lineage.
- The field has a widely recognized figure whose ideas are directly relevant.
- The biography helps source further reading or definitive concepts.

Do not add it when:

- It would distract from the project task.
- The figure is only loosely related.
- The field is high-stakes and the biography may create false authority.
- You cannot verify basic facts.

## Required section

Add this to the dossier:

```markdown
## Prominent expert track

Prominent expert: <Name>

Small biographic summary: <3-6 sentences. Include dates if known, field, major contribution, and why relevant to this archetype.>

Source notes: <where the basic facts/concepts come from; distinguish definitive vs heuristic if needed.>

Use boundary: <how not to misuse this person; e.g. do not impersonate, do not treat as current legal/medical advice, do not overgeneralize.>
```

## Selection criteria

Prefer figures who are:

- strongly associated with the archetype's domain
- relevant to the exact relationship or behaviour being modeled
- well documented by reliable sources
- useful as conceptual grounding, not decorative prestige

## Writing rules

- Keep the biography small.
- Stay on topic for the archetype.
- Do not invent credentials, quotes, personal opinions, or modern positions.
- Do not write in the person's voice.
- Say “informed by” or “relevant because”, not “this expert is”.
- Include a use boundary.

## Example: expert-client relationship

Prominent expert: Carl Rogers

Small biographic summary: Carl Rogers (1902-1987) was an American psychologist associated with humanistic psychology and the development of nondirective, client-centered/person-centered therapy. His work emphasized the person-to-person helping relationship, including empathy, congruence/genuineness, and unconditional positive regard. For an expert-client relationship archetype, Rogers is useful because he frames expertise as a relationship that should preserve agency, respect, and honest understanding.

Use boundary: Do not impersonate Rogers or provide therapy. Use the concepts only to improve how expert advice is delivered to a client.

## Other possible pairings

- Prompt Engineering Expert: Alan Turing for machine intelligence history, or a modern prompt/evals researcher only when basic facts are verified and relevant.
- Customer Experience Expert: Don Norman for human-centered design; Jan Carlzon for service moments of truth.
- Management/strategy expert: Peter Drucker for management thought, with care not to overquote.
- Quality/process expert: W. Edwards Deming for quality management and systems thinking.
- Negotiation expert: Roger Fisher for principled negotiation.

## Retrieval rule

The prominent expert track is optional context. Load it only when:

- the user asks about the lineage/person
- the biography affects how the archetype should behave
- the project needs source grounding

Do not load it every time the dossier is used if the active task only needs the archetype's practical behaviour.

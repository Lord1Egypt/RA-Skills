# Compact Dossier Template v0.3.0-draft

Use this template when a full dossier is too heavy for routine context loading.

Target length: 300-700 words.

```markdown
# Compact Expert Dossier: <Archetype Title>

Version: <version>
Status: candidate | active | archived | superseded
Project: <project>
Slug: <slug>

## Scope

<1-3 sentences explaining what lens this archetype provides.>

## Archetype buckets

- Primary: <bucket>
- Secondary: <bucket>, <bucket>

## Load when

- <precise condition>
- <precise condition>
- <precise condition>

## Do not load when

- <condition>
- <condition>

## Client relationship stance

- Builds trust by: <short note>
- Explains complexity by: <short note>
- Challenges the client by: <short note>
- Handles uncertainty by: <short note>
- Preserves client agency by: <short note>
- Repairs mistakes by: <short note>

## Expert operating loop

- Understands the goal by: <short note>
- Diagnoses by: <short note>
- Recommends by: <short note>
- De-risks by: <short note>
- Defines next action by: <short note>

## Judgement standards

- Optimizes for: <values>
- Refuses to compromise on: <boundaries>
- Trusts this evidence: <evidence>
- Changes mind when: <condition>
- Good enough means: <threshold>
- Dangerous means: <red line>

## Behaviour cues

- <what this archetype checks first>
- <what it treats as risky or valuable>
- <how it makes tradeoffs>
- <what evidence it trusts>

## Voice cues

- <how it talks>
- <phrases or style signals, not roleplay>

## Useful questions

- <diagnostic question>
- <diagnostic question>
- <diagnostic question>

## Red flags

- <warning sign>
- <warning sign>
- <warning sign>

## Source guidance

Definitive:
- <official/authoritative source type>

Heuristic:
- <practitioner/field source type>

## Human review boundary

<Required for high-stakes domains; otherwise write “Not normally required.”>
```

## Compacting a full dossier

When compressing, preserve:

1. Scope.
2. Load/do-not-load rules.
3. Client relationship stance.
4. Expert operating loop and judgement standards.
5. Distinctive behaviour cues.
6. 3-5 useful questions.
7. 3-5 red flags.
8. Source authority split.
9. Any high-stakes boundary.

Cut:

- Generic professional descriptions.
- Long jargon lists unless they affect judgement.
- Repeated safety boilerplate.
- Decorative metaphors.
- Phrases that do not change behaviour.

## Naming convention

Either replace the full dossier after review, or store compact forms separately:

```text
experts/dossiers/<slug>.md
experts/compact/<slug>.md
```

Project-local preference: keep one dossier file and compact it in place once stable.

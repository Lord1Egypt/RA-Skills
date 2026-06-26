# EASA answering notes

## Retrieval-first workflow

1. If the user gives an exact reference, run `claw-easa lookup <REF>`.
2. If the user gives a topic or phrase, start with `refs`, `snippets`, or `hybrid`.
3. Use `ask` only after retrieval when a synthesized answer is useful.

## Output discipline

- Prefer exact wording when the user asks for the content of a regulation point.
- Separate clearly:
  - binding regulation text
  - AMC/GM guidance
  - FAQ material
- Include the reference identifier in the answer.
- If you only found related material, say that explicitly.
- If nothing relevant was retrieved, say so explicitly.

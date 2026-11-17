# Writing Patterns & Validation

## Style

- Imperative, present tense, second person: "You read the file first".
- Concrete over abstract: "use `--yes` for npx" beats "avoid prompts".
- One rule per bullet; number hard sequences, bullet soft preferences.
- `{{placeholders}}` for anything the user fills in.
- One short example resolves more than a paragraph.

## Degrees of freedom

- **High** — tone/persona: guide, don't dictate.
- **Medium** — workflows/tool use: preferred pattern with room to adapt.
- **Low** — safety boundaries, refusal criteria, exact schemas: exact and unambiguous.

## Section order

Identity → Mission → Capability → Environment → Communication → Tool rules → Tools → Workflows → (Loop/Planning) → Output → Citations → Boundaries/Safety.

## Anti-patterns

Generic safety dump · undefined tools · contradictory tone ("concise" + "always elaborate") · duplicated rules · vague mission · no stop condition.

## Validation

1. Trace every tool → has signature + "when to use".
2. Trace every constraint → unambiguous and testable.
3. Read as the agent: who am I, what to do, how to talk, when to act/stop?
4. Cut dead sections; check token economy.

## Fix-by-symptom

| Symptom | Fix |
|---|---|
| Wrong identity | 1 Identity |
| Rambles / wrong format | 5 Tone, 16 Output |
| Unnecessary tool calls | 11 Tool rules |
| Loops on error | 15 Errors |
| Never finishes | 13 Loop, 14 Planning |
| Over/under-refuses | 7–8 Boundaries/Safety |
| Fabricates tools/params | 9–11 Tools |

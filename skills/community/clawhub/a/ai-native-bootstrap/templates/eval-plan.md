# Eval collection plan — no fabricated cases

Status: NOT RUN

1. Identify 5–10 genuine historical defects, accepted outputs, or tasks, with stable source references.
2. Define deterministic or human-rated acceptance for each; record input, model/Skill version, expected result, execution evidence.
3. Separate deterministic PASS/FAIL from subjective human ratings; do not label LLM self-grading as objective proof.
4. Run existing tests before allowing model/prompt/Skill revisions into main; schedule expensive LLM evals only if budget and credentials are approved.
5. Add any new production incident to the collection after triage.

Do not create synthetic test data and call it a historical regression.

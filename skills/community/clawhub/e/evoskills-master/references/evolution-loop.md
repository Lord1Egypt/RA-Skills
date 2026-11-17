# Co-Evolution Loop

Adapt EvoSkills to skill packages by separating two responsibilities:

- `generator`: the agent editing the target skill
- `surrogate verifier`: the process that audits structure, runs scripts/tests, and exercises realistic prompts

## Loop

1. Baseline the target skill
2. Detect the highest-value failure
3. Patch only enough to address that failure
4. Re-run the verifier
5. If the verifier passes but the skill still fails on realistic use, make the verifier stricter

## Failure Taxonomy

Use this ordering when deciding what to fix next:

1. Invalid package shape
2. Weak frontmatter triggers
3. Missing or ambiguous workflow
4. Missing reusable resources
5. Missing validation or recovery guidance
6. Prompt matrix too easy

Mechanical failures such as malformed frontmatter, broken relative links, underspecified thin bodies, oversized `SKILL.md` bodies, or missing root entrypoints in multi-skill repositories should be auto-repaired first so later iterations can focus on workflow quality.

## Verifier Upgrade Triggers

Upgrade the prompt matrix when any of these happen:

- the skill passes static checks but not real prompts
- the skill succeeds only on ideal wording
- the skill ignores bundled scripts or references
- the skill cannot recover from missing prerequisites
- the skill claims completion without verification

## Good Evolution Moves

- Narrow a vague description into concrete trigger phrases
- Expand a thin skeleton into a structured body with clear entrypoint, workflow, recovery, and verification guidance
- Detect when a repository is really a bundle of child skills and create a routing entrypoint at the root
- Pull long details from `SKILL.md` into targeted reference files
- Replace repeated prose procedures with a reusable script
- Add a verification checklist close to the execution workflow
- Add examples that are short, realistic, and high-signal

## Bad Evolution Moves

- rewriting the entire skill without a baseline
- making the skill longer without making it clearer
- adding references that are never linked from `SKILL.md`
- adding scripts without testing them
- stopping after static linting

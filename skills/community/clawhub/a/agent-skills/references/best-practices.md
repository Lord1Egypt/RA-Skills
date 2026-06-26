# Skill Creation Best Practices

## Start from Real Expertise

Most effective skills are grounded in real domain experience, not generated from LLM general knowledge.

**Extract from hands-on tasks**: Complete real tasks, then extract reusable patterns → successful steps, manual corrections, I/O formats, project-specific context.

**Synthesize from project artifacts**: Feed internal docs/runbooks/API specs/code reviews to an LLM to synthesize skills, not generic references.

## Refine with Real Execution

Run the first draft against real tasks, collect all results (not just failures). Ask: what false-triggered? What was missed? What can be cut?

Check execution traces: agent wastes time on unproductive steps → instructions too vague, don't apply, or too many options without a default.

## Spending Context Wisely

### Add what the agent lacks, omit what it knows

For each piece: "Would the agent get this wrong without this instruction?" No → cut it. Agents already know what PDFs are, how HTTP works.

### Design coherent units

Too narrow → multiple skills load for one task (instruction conflicts). Too broad → hard to activate precisely. Example: query database + format results = one unit; adding database administration = too much.

### Aim for moderate detail

Overly comprehensive skills hurt more than help. Concise stepwise guidance + working example > exhaustive documentation.

### Structure large skills with progressive disclosure

SKILL.md <500 lines/5000 tokens. Detailed reference in references/, tell agent *when* to load: "Read references/api-errors.md if API returns non-200 status."

## Calibrating Control

### Match specificity to fragility

- **Give freedom**: when multiple approaches work, explain *why* rather than rigid directives
- **Be prescriptive**: fragile operations require exact sequence (`python scripts/migrate.py --verify --backup`, do not modify)

### Provide defaults, not menus

Pick one default when multiple tools work. Mention alternatives briefly, don't list as equal options.

### Favor procedures over declarations

Teach the agent *how to approach* a class of problems, not *what to produce* for a specific instance. The approach should generalize.

## Effective Instruction Patterns

### Gotchas

The highest-value content — environment-specific facts the agent will get wrong without being told. After agent makes a mistake → add to gotchas.

### Output templates

Concrete templates outperform descriptive language (agents pattern-match better against concrete structures). Short templates in SKILL.md, long ones in assets/.

### Checklists

Multi-step workflows with checkboxes track progress and prevent skipped steps.

### Validation loops

Do work → run validator → fix issues → repeat until pass.

### Plan-validate-execute

For batch/destructive operations: create structured intermediate plan, validate against source of truth, then execute. The validation script is the key ingredient.

### Bundle reusable scripts

If agent independently rewrites the same logic each run → write a tested script once in scripts/.

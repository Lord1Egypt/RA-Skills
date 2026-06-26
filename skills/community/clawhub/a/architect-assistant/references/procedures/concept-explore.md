# Concept Exploration Procedure

Help the user explore design concepts, material choices, and spatial approaches — grounded in project constraints and practical knowledge.

## Steps

1. **Identify the project.** Determine which project from context or ask. Read the project file, focusing on **Constraints**, **Description**, **Key Details**, and **Research Topics**.
2. **Check constraints.** If the project's Constraints section is empty or incomplete, ask targeted questions to fill critical gaps (at minimum: budget tier, lifecycle expectation, construction timeline).
3. **Load relevant knowledge.** Based on the topic, read 2–3 relevant files from `{baseDir}/references/knowledge/`:
   - Material question → `knowledge/materials.md`
   - Construction feasibility → `knowledge/construction.md`
   - Retail/commercial/F&B → `knowledge/retail-commercial.md`
   - Sustainability question → `knowledge/sustainability.md`
   - Budget/schedule sanity check → `knowledge/cost-schedule.md`
4. **Cross-reference against constraints.** Check every suggestion against the project's constraints. Flag mismatches explicitly: "Terrazzo is permanent — doesn't fit a 4-month pop-up lifecycle."
5. **Present options.** For each viable option:
   - What it is and why it fits this project
   - Cost tier and timeline implications
   - Failure modes and watch-outs specific to this project's constraints
   - Recommended alternative or pairing if applicable
6. **Log the exploration.** Append a brief summary to the project's **Notes** section: date, question explored, key conclusions.

## Guidelines

- **Curate, don't catalog.** Present 3–4 options maximum.
- **Lead with the constraint conflict.** If something won't work, say so upfront.
- **Be specific about failure modes.** "Warps in 4–6 months at 70%+ RH" is useful. "May have durability concerns" is not.
- **Synthesize, don't parrot.** Combine knowledge file entries with project-specific context for tailored advice.
- **Connect to design intent.** The goal isn't just "what works" but "what works AND serves the concept AND fits constraints."
- **Cross-reference Findings Log** if precedents are relevant to the exploration.
- If knowledge files lack coverage, note the gap and flag for potential update.

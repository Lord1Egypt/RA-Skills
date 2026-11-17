## Description:

Generates multi-themed food collages (Viral Cakes, Street Food, Smoothie Bowls, Coffee Art, Fusion Tacos). Use when user asks for a collage of specific food categories, layouts with circle-masked images, or when they want to 'pick' items from a curated list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expysf98](https://clawhub.ai/user/expysf98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate curated food selection collages with circular image masks and themed PICK titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script may fail if Pillow or the expected local collage image folders are missing.

Mitigation: Install Pillow and provide the required collages/<theme>/<letter>.png files before running the script.

Risk: The script writes generated PNG files with fixed names in the directory where it is run.

Mitigation: Run it from a chosen output directory and review existing collage_*.png files before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with plain-text progress messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fixed-name collage PNG files to the current working directory and expects local theme image folders plus Pillow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

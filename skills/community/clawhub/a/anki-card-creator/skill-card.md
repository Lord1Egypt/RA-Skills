## Description:

Convert medical textbook content, lecture notes, and study materials into Anki flashcards using spaced repetition optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and developers use this skill to generate Anki-compatible flashcards from medical study materials and simple Q&A inputs. It is best suited for local TSV card generation that is reviewed before import into Anki.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package documentation advertises advanced PDF, image occlusion, APKG export, media, and tagging features that the included script does not implement.

Mitigation: Treat the current package as a simple local TSV generator unless the package is corrected.

Risk: The dependency file lists Python standard-library modules as requirements.

Mitigation: Do not run the included requirements.txt as-is; run the script with Python's standard library.

Risk: Generated medical flashcards may contain inaccurate, incomplete, or outdated content from the input material.

Mitigation: Use trusted input files only and review generated cards before importing them into Anki.

Risk: The script writes to the user-selected output path and may overwrite an existing file.

Mitigation: Choose an output path that does not contain important existing data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python CLI commands and Anki-compatible TSV text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script reads local text input, prints a card summary, and writes a TSV output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

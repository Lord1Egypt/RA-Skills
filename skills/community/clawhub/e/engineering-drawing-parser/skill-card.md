## Description:

Helps agents extract title block, BOM, and dimension data from engineering drawing text dumps or sidecar text files, with examples centered on mechanical drawings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide extraction of structured drawing information such as title-block fields, BOM rows, dimensions, tolerances, and review previews from text-layer engineering drawing inputs. Manual verification is expected before using extracted values in engineering work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates support for DWG, DXF, PDF, image OCR, and full CAD parsing compared with the bundled code.

Mitigation: Use it as a text-layer or sidecar text extractor unless optional CAD/OCR tooling and extraction paths are independently verified.

Risk: Incorrect extracted dimensions, tolerances, title-block fields, or BOM rows could affect engineering decisions.

Mitigation: Manually verify all extracted engineering values against the original drawing before reuse.

Risk: Rendered previews may be viewed in Markdown tooling that allows unsafe HTML or remote resources.

Mitigation: Render previews in a Markdown viewer that blocks raw HTML and remote resources.

## Reference(s):

- [Project homepage](https://github.com/openclaw-skills/engineering-drawing-parser)
- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/engineering-drawing-parser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; bundled scripts can emit JSON extraction results and Markdown previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extraction results may include title-block fields, BOM rows, dimensions, confidence-style reports, and preview content when supported by the text input.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

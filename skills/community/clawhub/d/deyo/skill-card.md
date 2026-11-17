## Description:

Helps an agent transcribe explicitly supplied media URLs or local audio and video files with Deyo, with optional cleaned text and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casatwy](https://clawhub.ai/user/casatwy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Deyo to transcribe media they explicitly identify, obtain cleaned or verbatim transcripts, captions, or structured results, and summarize explicitly requested batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication requires a Deyo API key.

Mitigation: Request consent before login or saving a key; keep credentials private.

Risk: Transcription uploads explicitly supplied media files or URLs and can consume Deyo minute balance.

Mitigation: Confirm the exact inputs and minute-balance authorization before processing.

Risk: Transcript delivery creates local output files.

Mitigation: Confirm output locations and review paths before writing; avoid replacing existing files.

Risk: Some cleaning prompts and summary headings are Chinese-specific.

Mitigation: Check that the requested language and output style fit the workflow.

## Reference(s):

- [Deyo ClawHub release](https://clawhub.ai/casatwy/skills/deyo)
- [Sequential transcription and summary](references/batch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Plain text, Markdown, SRT, VTT, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleaned transcripts may be saved as .txt; requested batches can include per-item summaries and a cited overview.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Retrieves A-share announcement and research report lists and downloads related PDF files from market.ft.tech by date, stock code, or url_hash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to look up A-share announcements or research reports for a date or stock, then download a selected PDF by url_hash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local command dispatcher and PDF-saving behavior are broader than needed for the advertised data retrieval workflow.

Mitigation: Review before installing, invoke only documented subskill names, and run the skill from a disposable working directory.

Risk: Downloaded PDF output can write local files and may overwrite files when unsafe filenames, symlinks, or sensitive working directories are used.

Mitigation: Use trusted output filenames under the current working directory and avoid installation or execution locations where overwritten files could affect important local files.

Risk: Results and downloaded documents come from an external market.ft.tech service and may be unavailable, incomplete, or unsuitable as sole financial evidence.

Mitigation: Check returned JSON and downloaded PDFs before relying on them, and corroborate important financial conclusions with authoritative market or issuer sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-announcement-data)
- [market.ft.tech API base](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [JSON, Files, Text, Markdown]

**Output Format:** [JSON responses and downloaded PDF files, often summarized by the agent as Markdown tables or bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network calls use HTTP GET; PDF downloads write files under the execution working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

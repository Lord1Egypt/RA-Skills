## Description:

Extracts the full investment strategy and operations analysis section from Chinese public fund periodic reports and consolidates the results in chronological order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suncxw-creator](https://clawhub.ai/user/suncxw-creator)

### License/Terms of Use:


## Use Case:

Analysts and agent operators use this skill to retrieve fund announcement PDFs, extract the investment strategy section, and build a consolidated text summary for a named fund code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extractor can write files outside the intended output area when fund names or codes contain path characters.

Mitigation: Run it in a dedicated working directory and use normal fund codes and names without path separators; validate filenames before broader deployment.

Risk: Downloaded PDFs are processed insecurely, including use of an HTTP download URL and a fixed temporary filename.

Mitigation: Prefer HTTPS sources where available, use safe temporary files, check file size and type before parsing, and avoid shared writable folders.

Risk: Unpinned dependencies and network retrieval can make results or runtime behavior vary across environments.

Mitigation: Pin dependencies, review updates before installation, and retry failed network requests in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suncxw-creator/skills/fund-report-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash and Python snippets; generated text files when the extractor script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a reports_<fund code>/ directory with per-report text extracts and a consolidated <fund name>_投资策略汇总.txt file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Compare two JSON files and show differences, including nested structures, arrays, and value changes, using only the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare two local JSON files and receive a concise difference report showing changed paths, added or removed keys, type changes, and array length differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes third-party promotional links unrelated to local JSON comparison.

Mitigation: Review promotional links before opening them; using the local diff script does not require visiting those links.

Risk: JSON comparison results may be incomplete for arrays because the script reports that a list differs rather than item-by-item changes.

Mitigation: Use the output as a quick local summary and inspect changed arrays manually when element-level differences matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-json-diff)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; the bundled script emits JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Python standard library; no API key required]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

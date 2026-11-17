## Description:

Generates a tool name and reviewable user instruction list from a bug description, then can hand confirmed instructions to data-generator for JSONL training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset curators use this skill to turn bug reports about incorrect tool selection or behavior into candidate smart-home user instructions for review, then into JSONL training records after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented workflow and bundled generator behavior conflict about whether JSONL is generated directly.

Mitigation: Prefer the prompt-list workflow for reviewed instruction generation, and inspect generated records before using them as training data.

Risk: gen_bug_data.py imports executable Python from an unbundled local data-generator path.

Mitigation: Run it only where the data-generator installation and output path are trusted; avoid shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaibuer/skills/bug-data-generator)

## Skill Output:

**Output Type(s):** [text, JSON, JSONL files, shell commands, guidance]

**Output Format:** [Markdown-style text, JSON instruction payloads, and JSONL training records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write text, JSON, or JSONL files; gen_bug_data.py depends on a local data-generator helper path when available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

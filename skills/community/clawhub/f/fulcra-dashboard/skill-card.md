## Description:

Builds a customizable local HTML dashboard for Fulcra data using Alpine.js, Vanilla CSS, and a Python static server, with an isolated public directory for approved sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Fulcra users use this skill to scaffold and customize a local dashboard for private Fulcra records, then export only approved public assets when sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Fulcra records may be copied into the public dashboard export.

Mitigation: Review the exact files in public/ before sharing and publish only records that are intentionally approved for public viewing.

Risk: The dashboard relies on browser libraries fetched from public CDNs.

Mitigation: Prefer local-only use for sensitive dashboards, or vendor and pin browser dependencies before broader deployment.

Risk: Unsafe HTML rendering may expose dashboard viewers to untrusted content.

Mitigation: Fix the x-html/formatValue rendering issue before deploying a dashboard publicly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fulcra/skills/fulcra-dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local dashboard directory with HTML, CSS, JavaScript, Python server files, JSON/JSONL data manifests, and optional image assets.]

## Skill Version(s):

0.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

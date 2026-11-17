## Description:

Search and download research papers from arXiv.org - Research version for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Developers and research-focused users use this skill to search arXiv by keyword or category, review paper metadata, and download selected PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts arXiv and can save requested PDFs locally.

Mitigation: Review download intent and destination before execution, and run the skill in a contained environment when possible.

Risk: The skill depends on the third-party arxiv Python package.

Mitigation: Install in a virtual environment and pin the dependency version before deployment.

Risk: The documented PowerShell examples may not match the packaged Python script.

Mitigation: Adjust usage commands to invoke arxiv_search.py or provide the expected wrapper before use.

## Reference(s):

- [arXiv](https://arxiv.org)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text search results and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests contact arXiv; downloaded PDFs are saved locally.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

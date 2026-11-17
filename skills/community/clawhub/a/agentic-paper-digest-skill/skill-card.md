## Description:

Fetches and summarizes recent arXiv and Hugging Face papers with Agentic Paper Digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matanle51](https://clawhub.ai/user/matanle51)

### License/Terms of Use:


## Use Case:

Developers and research-oriented users use this skill to configure and run a local pipeline that fetches recent arXiv and Hugging Face papers, filters them by topic, and returns paper digests through CLI JSON output or a local API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can execute mutable remote code from the publisher repository.

Mitigation: Pin the repository to a reviewed commit and review requirements before installing dependencies.

Risk: Wrapper scripts source dotenv files as shell code.

Mitigation: Use safe dotenv parsing and keep API keys out of transcripts and version control.

Risk: The API stop helper can force-kill processes on port 8000 or matching broad process names.

Mitigation: Avoid stop_api.sh unless you have confirmed nothing important is using port 8000.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matanle51/skills/agentic-paper-digest-skill)
- [Publisher Profile](https://clawhub.ai/user/matanle51)
- [Agentic Paper Digest Repository](https://github.com/matanle51/agentic_paper_digest)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON pipeline output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also start a local API server and store results in a SQLite database under PROJECT_DIR.]

## Skill Version(s):

0.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

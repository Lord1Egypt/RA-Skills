## Description: <br>
Reviews and verifies code changes for scope, correctness, security, testing, secrets, and risks before commits, pull requests, or deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-writing agents use this skill to review planned or completed repository changes before edits, commits, pull requests, releases, or deployments. It helps keep changes scoped, test claims truthful, secrets out of artifacts, and destructive actions gated on approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace capability tags request wallet, purchase, transaction signing, and sensitive credential access that the instruction-only artifact does not need. <br>
Mitigation: Install and run the skill without wallet, signing, purchase, or sensitive credential permissions. <br>
Risk: Review payloads can expose secrets or private data if full logs, full diffs, or private records are included. <br>
Mitigation: Use redacted summaries and omit raw secrets, private records, full logs, full diffs, and unrelated files. <br>
Risk: The skill guides review decisions but does not verify repositories, run checks, or approve code changes on its own. <br>
Mitigation: Run actual tests, scans, and human or verified review paths separately, and report only observed results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindbomber/aana-code-change-review) <br>
- [README.md](artifact/README.md) <br>
- [Review Payload Schema](artifact/schemas/code-change-review.schema.json) <br>
- [Redacted Review Payload Example](artifact/examples/redacted-code-change-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or structured JSON review summaries, depending on the configured review workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact is instruction-only and does not execute commands, write files, call services, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

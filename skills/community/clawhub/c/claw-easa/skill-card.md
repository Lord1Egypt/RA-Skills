## Description: <br>
Query EASA Easy Access Rules locally with exact reference lookup, full-text search, and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmoraine](https://clawhub.ai/user/dmoraine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and aviation-regulatory practitioners use this skill to retrieve EASA regulation wording, AMC/GM guidance, FAQ material, and related references from a local claw-easa index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external local claw-easa runtime and bootstrap scripts. <br>
Mitigation: Install only after reviewing or trusting the external runtime repository and verify the CLI with status/help checks before relying on answers. <br>
Risk: Fetch, parse, and FAQ ingestion commands download or update a local public EASA corpus. <br>
Mitigation: Run ingestion commands only when intentionally refreshing the corpus and confirm the target source or FAQ domain first. <br>
Risk: The documented rsync install command can delete files at the destination path. <br>
Mitigation: Verify the OpenClaw skill destination before using rsync with --delete, or use the guarded helper script when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dmoraine/claw-easa) <br>
- [Runtime Setup](references/runtime-setup.md) <br>
- [EASA Answering Notes](references/easa-answering.md) <br>
- [Skill Usage](references/usage.md) <br>
- [EASA Regulations FAQs](https://www.easa.europa.eu/en/the-agency/faqs/regulations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with cited regulatory excerpts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should distinguish regulation text from AMC, GM, and FAQ material and state when retrieval is empty or ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

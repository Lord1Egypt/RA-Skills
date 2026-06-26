## Description: <br>
edisclaw helps legal teams process, deduplicate, cull, search, review, and produce ESI collections locally through a command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jagadeeshmurali-coder](https://clawhub.ai/user/jagadeeshmurali-coder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Litigators, paralegals, solo attorneys, and in-house investigation teams use this skill to run local e-discovery workflows for authorized matters, including ingestion, culling, review, tagging, and production exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Homebrew formula and edisclaw binary. <br>
Mitigation: Verify the legal-tools/tap/edisclaw formula, binary source, and publisher before installing or running it. <br>
Risk: The CLI processes legal ESI and stores matter data locally under ~/.edisclaw/. <br>
Mitigation: Use it only for authorized matters, limit ingestion to approved custodians and scopes, protect local matter storage, and remove retained ESI when no longer required. <br>
Risk: Paid Pro or Litigation features may introduce network behavior for TAR models. <br>
Mitigation: Review paid-tier network behavior before using those features with sensitive client or investigation data. <br>


## Reference(s): <br>
- [edisclaw project homepage](https://github.com/legal-tools/edisclaw) <br>
- [ClawHub release page](https://clawhub.ai/jagadeeshmurali-coder/ediscclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI command examples and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the edisclaw command-line binary installed from the legal-tools/tap/edisclaw Homebrew formula.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

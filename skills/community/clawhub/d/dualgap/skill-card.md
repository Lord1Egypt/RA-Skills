## Description: <br>
Use DualGap for dual-domain research gap analysis: turn two paper collections, PDF folders, arXiv downloads, or research directions into reviewer-checked literature notes, direction-level syntheses, cross-domain comparison, research-gap analysis, and ranked improvement ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zza234s](https://clawhub.ai/user/zza234s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to compare two research-paper collections, generate evidence-grounded literature notes and reviews, synthesize each direction, compare domains, identify research gaps, and rank follow-up ideas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF text and generated research notes may be sent to the configured LLM provider. <br>
Mitigation: Confirm provider acceptability before running and avoid using sensitive paper collections unless the provider and configuration are approved. <br>
Risk: The workflow requires API credentials. <br>
Mitigation: Keep API keys in a local env or config file outside generated outputs, and do not paste real keys into notes, logs, examples, or committed files. <br>
Risk: Large corpus runs may increase cost or expose more data than intended. <br>
Mitigation: Start with the documented smoke-test limits and review the audit report before scaling to larger batches. <br>


## Reference(s): <br>
- [ClawHub Release: Dualgap](https://clawhub.ai/zza234s/dualgap) <br>
- [Server-resolved GitHub source](https://github.com/zza234s/DualGap) <br>
- [How To Use DualGap](artifact/HOW_TO_USE.md) <br>
- [Paper Note And Review Schema](artifact/references/note_schema.md) <br>
- [Validation Protocol](artifact/references/validation_protocol.md) <br>
- [Configuration Example](artifact/references/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and syntheses, JSON manifests and reviews, text extracts, audit reports, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires two PDF input directories, research direction names, an output directory, a research agenda, and OpenAI-compatible LLM API configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

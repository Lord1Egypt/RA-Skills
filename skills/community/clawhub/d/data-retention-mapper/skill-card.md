## Description: <br>
Maps data retention periods, storage locations, cleanup responsibilities, and expiry handling recommendations for governance and privacy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, governance, audit, and data operations teams use this skill to turn retention notes or inventories into reviewable reports covering data assets, storage locations, retention periods, cleanup responsibilities, risks, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input materials may include sensitive retention inventories or storage locations. <br>
Mitigation: Redact sensitive details when practical and review the generated report before sharing. <br>
Risk: The bundled Python helper runs locally over files selected by the user. <br>
Mitigation: Run it only on intended inputs and inspect outputs before using them in governance decisions. <br>
Risk: Unused audit modes are present in the code but are not active in the shipped configuration. <br>
Mitigation: Avoid modifying the bundled spec to enable broader inspection unless that behavior is intentional and reviewed. <br>
Risk: The skill supports governance drafts but does not replace formal compliance advice. <br>
Mitigation: Treat outputs as review drafts and route compliance decisions through the appropriate reviewer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/data-retention-mapper) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report, with optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local inputs only; the helper script supports input/output paths, format selection, result limits, and dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Checks whether a brand's claimed international presence is supported by evidence across websites, sales channels, marketplace records, media coverage, WHOIS data, trademark chronology, and seller location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tompchen](https://clawhub.ai/user/tompchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and brand-review teams use this skill to produce an investigative assessment of whether a brand appears to be a genuine international brand, suspicious brand, or fake international brand. Its conclusions should guide follow-up research rather than serve as final proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand names and research topics may be sent to third-party search and marketplace services during verification. <br>
Mitigation: Use non-sensitive inputs where possible, review configured services before execution, and avoid submitting confidential brand investigations unless the data sharing is approved. <br>
Risk: The skill may produce confident authenticity or brand-fraud conclusions from hardcoded examples, placeholder checks, or incomplete external evidence. <br>
Mitigation: Treat verdicts as investigative leads and manually verify negative or high-confidence conclusions with authoritative sources before acting on them. <br>
Risk: The skill can depend on API keys or other sensitive credentials for external search services. <br>
Mitigation: Provide credentials through environment variables or a managed secret store, rotate them regularly, and do not embed secrets in skill files or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tompchen/fake-international-brand-detector) <br>
- [API and data source list](artifact/reference/apis.md) <br>
- [Quality standards](artifact/reference/quality-standards.md) <br>
- [Brand examples](artifact/reference/brand-examples.json) <br>
- [Known international brands](artifact/reference/known_international_brands.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown, JSON, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include brand verdicts, confidence scores, evidence summaries, and recommendations for manual follow-up.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

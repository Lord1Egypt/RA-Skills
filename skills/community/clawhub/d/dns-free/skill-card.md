## Description: <br>
DNS配置基础版 helps agents provide basic DNS record guidance, TTL migration reminders, SPF/DMARC checks, and dig-based diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and domain owners use this skill to triage basic DNS configuration issues, plan TTL changes before migration, and review entry-level SPF/DMARC records. It is intended for guidance and diagnostic command suggestions rather than direct DNS-provider changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS lookup commands can expose queried domains to selected resolvers. <br>
Mitigation: Run dig-style commands only for domains the user intends to inspect, and choose resolvers appropriate for the user's privacy and diagnostic needs. <br>
Risk: Incorrect DNS, SPF, or DMARC guidance can disrupt web traffic or email delivery. <br>
Mitigation: Review suggested record changes manually in the DNS provider console and stage TTL-sensitive migrations before switching production records. <br>
Risk: The artifact declares a write tool broader than the documented DNS diagnostic workflow requires. <br>
Mitigation: Avoid file or system changes unless the user explicitly asks for them; treat the skill primarily as a DNS guidance and diagnostic helper. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON examples with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces DNS diagnostic findings, record-change suggestions, execution notes, and error guidance for manual review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

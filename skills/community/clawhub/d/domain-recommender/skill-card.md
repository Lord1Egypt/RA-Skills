## Description: <br>
Recommend SEO-friendly, brandable domain names for an AI product idea, then verify current availability before returning candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daviddonecn](https://clawhub.ai/user/daviddonecn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, marketers, and developers use this skill to turn a product concept or keyword into a short list of brandable domain candidates with current availability status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain availability checks can expose product concepts and candidate names to registrars, marketplaces, web pages, or DNS resolvers. <br>
Mitigation: Use the skill only when it is acceptable to share those concepts with external availability-checking services. <br>
Risk: The artifact references a local candidate-generation helper script that is not included in the submitted files. <br>
Mitigation: Generate candidates manually or verify any added helper script before running it. <br>
Risk: DNS-clear results do not prove that a domain is unregistered or purchasable. <br>
Mitigation: Prefer registrar-confirmed availability and clearly label fallback results when registrar confirmation is not obtained. <br>


## Reference(s): <br>
- [SEO And Brand Patterns](references/seo-brand-patterns.md) <br>
- [Project homepage](https://github.com/hilaraklesantosw-art/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown shortlist with inline domain availability notes and optional shell commands for DNS checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to five recommended domains unless the user asks for a different shortlist size.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

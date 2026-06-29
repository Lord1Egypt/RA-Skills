## Description: <br>
Domain Lookup helps agents retrieve domain registration information using RDAP with WHOIS fallback through a third-party API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and domain researchers use this skill to look up domain registration details, nameservers, contacts, status, and optional raw RDAP or WHOIS response data after providing an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends domain lookup queries to xiaobenyang.com, a third-party service. <br>
Mitigation: Use it only when the queried domains can be shared with that service and review returned data before relying on it. <br>
Risk: The skill saves the provided API key in a local .env file. <br>
Mitigation: Treat the .env file as sensitive, keep it out of commits and shared archives, and rotate the key if it is exposed. <br>
Risk: Some artifact text appears copied from an unrelated school-search skill, which may confuse setup or review. <br>
Mitigation: Use the documented domain_lookup function and required domain parameters as the source of truth during operation. <br>


## Reference(s): <br>
- [ClawHub Domain Lookup listing](https://clawhub.ai/alinklab/domain-lookup) <br>
- [XiaoBenYang API key provider](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown summary with structured JSON-derived domain lookup data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and may include raw RDAP or WHOIS response data when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

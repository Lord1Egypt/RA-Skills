## Description: <br>
Multi-source company research tool that generates structured due-diligence reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fan31415](https://clawhub.ai/user/fan31415) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to research companies, disambiguate likely legal entities, and produce structured public-source due-diligence reports covering ownership, financing, legal risk, operating risk, intellectual property, procurement, hiring, news, and competitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company research may include private company data, confidential URLs, or internal endpoints. <br>
Mitigation: Use direct fetch for sensitive work and do not route private data or internal URLs through proxy or archive strategies. <br>
Risk: The fallback script can be invoked from shell-capable agent environments. <br>
Mitigation: Pass user queries and URLs as command arguments rather than interpolating them into untrusted command strings. <br>
Risk: Public web search does not provide the same coverage as paid company databases and may include stale or single-source information. <br>
Mitigation: Require source URLs, fetch dates, confidence labels, and cross-validation for key conclusions; mark gaps as not found or requiring paid or internal channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fan31415/company-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fan31415) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown structured company research report; local fallback script returns JSON for search and fetch operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to cite sources, capture fetch dates, state confidence levels, and distinguish cross-validated findings from single-source leads.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

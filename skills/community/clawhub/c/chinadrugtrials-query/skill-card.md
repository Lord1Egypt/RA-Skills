## Description: <br>
Query chinadrugtrials.org.cn, the Chinese Drug Clinical Trial Registration and Information Disclosure Platform, to search or retrieve Chinese clinical trial registration records for a drug, indication, company, CTR number, or keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zephyrlucky-skills](https://clawhub.ai/user/zephyrlucky-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and clinical-research users use this skill to search the China Drug Clinical Trial Registration and Information Disclosure Platform and return official registration rows with applicant, disclosure date, status, and detail links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on browser automation against an external public registry, so site availability, anti-bot behavior, or navigation timeouts can prevent complete results. <br>
Mitigation: Use the documented Playwright workflow, keep navigation waits bounded, and report unverified fields explicitly when official detail extraction fails. <br>
Risk: Incorrect text encoding for Chinese queries can return unrelated records. <br>
Mitigation: Use UTF-8 handling and verify that result counts and returned rows match the intended keyword or CTR identifier. <br>
Risk: Fallback sources may be stale or disagree with the official platform. <br>
Mitigation: Prefer official list and detail pages, and state whenever any field was supplemented from a non-official source. <br>


## Reference(s): <br>
- [China Drug Clinical Trial Registration and Information Disclosure Platform](https://www.chinadrugtrials.org.cn/) <br>
- [ClawHub Skill Page](https://clawhub.ai/zephyrlucky-skills/chinadrugtrials-query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown table by default, with optional JSON output from the bundled query script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rows include registration number, trial status, drug name, indication, title, applicant company, first disclosure date, and official detail link.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

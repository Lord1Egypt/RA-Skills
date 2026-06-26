## Description: <br>
Scans websites, markdown files, and HTML files for broken links, with recursive crawling, depth limits, and text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to crawl sites or scan markdown and HTML files before release, then identify broken internal or external links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner contacts links found in websites or local files, which can expose or exercise private, untrusted, or high-volume URLs. <br>
Mitigation: Run scans only against authorized targets and use internal-only, max-urls, depth, timeout, and delay options for private, large, or untrusted scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/dead-link-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON scan results, with optional markdown guidance from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May exit with status 1 when broken links are found; supports broken-only, internal-only, URL limit, depth, timeout, and delay options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

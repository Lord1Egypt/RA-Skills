## Description: <br>
Bosszp guides agents through building a BOSS Zhipin job-listing scraper, MySQL data import, and Flask/Highcharts dashboard for salary and company analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to create a Scrapy-based BOSS Zhipin crawler, clean and export job data to CSV/MySQL, and build a local Flask dashboard for salary, company, financing, and requirement analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a job-listing scraper against BOSS Zhipin may violate site terms, robots policies, or applicable law if done without permission. <br>
Mitigation: Check BOSS Zhipin terms, robots policies, and applicable law before use; collect only permitted data and apply conservative crawling behavior such as delays. <br>
Risk: Cookies, MySQL storage, and a local Flask dashboard can expose account session data or collected job-market data if shared or network-accessible. <br>
Mitigation: Keep cookies out of shared files, store only necessary fields, restrict database access, and bind the dashboard to trusted local access unless it has been hardened. <br>
Risk: The dependency instructions include a `flash` package that should be verified before installation. <br>
Mitigation: Confirm the intended package name and source before installing dependencies, and prefer pinned, reviewed dependency versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/bosszp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with shell commands and Python/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation steps for local scraping, CSV/MySQL data handling, and dashboard setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

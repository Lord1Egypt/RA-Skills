## Description: <br>
Helps agents process web data, generate data-processing code, diagnose collection errors, clean extracted data, and iterate on data-processing strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to plan authorized web-data processing, generate starter collection scripts, troubleshoot common crawl failures, clean extracted data, and improve processing configurations from run history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide web-data collection workflows that may conflict with site terms, robots.txt, rate limits, or authorization boundaries. <br>
Mitigation: Use it only for authorized data processing, prefer official APIs, check robots.txt and terms before collection, and keep request rates conservative. <br>
Risk: Security review flagged advice involving proxy, CAPTCHA, IP-switching, or human-behavior suggestions that could be misused to bypass site controls. <br>
Mitigation: Do not use those suggestions to evade access controls or anti-abuse systems; restrict debugging to compliant failures and approved targets. <br>
Risk: The artifact includes an undisclosed contact scoring and persona inference utility. <br>
Mitigation: Review and disable that utility unless profiling is explicitly authorized, legally appropriate, and necessary for the intended use case. <br>
Risk: The release requires review because static scan was clean but VirusTotal was pending and the verdict was based on artifact content. <br>
Mitigation: Run local security review and dependency checks before deployment, and inspect generated code before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/datacrawl-debug) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [Publisher homepage](https://xiaping.coze.site) <br>
- [crawl_best_practices.md](references/crawl_best_practices.md) <br>
- [data_handling_guide.md](references/data_handling_guide.md) <br>
- [data_quality_checklist.md](references/data_quality_checklist.md) <br>
- [process_best_practices.md](references/process_best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code templates, JSON or CSV data examples, and configuration recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts may include runnable Python snippets, data-cleaning summaries, debugging diagnoses, and improvement recommendations.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

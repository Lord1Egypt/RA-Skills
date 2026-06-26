## Description: <br>
Scrape Amazon Brand Analytics (ABA) weekly hot keyword rankings from AMZ123 and return structured keyword trend data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and e-commerce analysts use this skill to collect weekly Amazon keyword ranking trends from AMZ123 and export them for market research or listing optimization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens Chrome and sends the user's keyword to AMZ123. <br>
Mitigation: Run it only when AMZ123 access and the keyword disclosure fit the user's site terms, workplace network rules, and privacy expectations. <br>
Risk: The skill creates local CSV or JSON output files. <br>
Mitigation: Choose the output directory deliberately and review generated files before sharing or importing them into downstream workflows. <br>


## Reference(s): <br>
- [Output Format Specification](references/output.md) <br>
- [Workflow for amz-hot-keywords](references/workflow.md) <br>
- [AMZ123 Top Keywords](https://www.amz123.com/usatopkeywords) <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/amz-hot-keywords) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, CSV, Shell commands, Guidance] <br>
**Output Format:** [CSV or JSON file containing search_term, current_rank, last_rank, and trend fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped amz123_hotwords_<keyword> output files and prints the created file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

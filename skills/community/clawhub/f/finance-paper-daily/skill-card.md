## Description: <br>
Finance Paper Daily fetches recent finance paper metadata from arXiv, Semantic Scholar, OpenAlex, and Google Scholar and writes a formatted daily Excel workbook to the user's Desktop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snow-seamless](https://clawhub.ai/user/snow-seamless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agents can run this skill to collect recent finance paper metadata from public academic services and generate a formatted daily Excel report on the user's Desktop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python dependencies at runtime, which may alter the active Python environment. <br>
Mitigation: Run it in a virtual environment and preinstall pinned dependencies instead of relying on runtime installation or --break-system-packages. <br>
Risk: The skill contacts public academic services to fetch paper metadata. <br>
Mitigation: Run it only where outbound requests to arXiv, Semantic Scholar, OpenAlex, and Google Scholar are allowed by policy. <br>
Risk: The skill creates or overwrites the same-day Excel report on the user's Desktop. <br>
Mitigation: Rename or back up an existing same-day report before rerunning if the previous output must be preserved. <br>


## Reference(s): <br>
- [Finance Paper Daily on ClawHub](https://clawhub.ai/snow-seamless/finance-paper-daily) <br>
- [Publisher Profile](https://clawhub.ai/user/snow-seamless) <br>
- [arXiv API endpoint](http://export.arxiv.org/api/query) <br>
- [Semantic Scholar Graph API paper search](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls] <br>
**Output Format:** [Excel workbook (.xlsx) plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or overwrites ~/Desktop/YYYY-MM-DD_finance_papers.xlsx with a daily papers sheet and source statistics sheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

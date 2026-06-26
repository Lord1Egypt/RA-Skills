## Description: <br>
Ai News Brief gathers AI, compute, GPU, large-model, memory, and policy news from multiple sources, ranks and summarizes articles, and can generate Markdown, HTML, PDF, and optional email briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17oko](https://clawhub.ai/user/17oko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect current AI, GPU, compute, model, memory, and policy news, filter and summarize articles, and produce shareable briefings or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens or connects to Chrome and scrapes multiple public news sites. <br>
Mitigation: Install and run only in an environment where browser automation and public-site scraping are acceptable. <br>
Risk: Optional LLM and email features can send article or report content to external services. <br>
Mitigation: Keep LLM and email features disabled until API URLs, API keys, SMTP credentials, recipients, and outbound content have been reviewed. <br>
Risk: The skill stores local news history and report artifacts. <br>
Mitigation: Review local storage locations and retention expectations before enabling recurring use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, HTML reports, PDF files, email content, JSON configuration, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local Chrome access, configured public news sources, optional LLM settings, optional SMTP settings, and local report/history storage.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

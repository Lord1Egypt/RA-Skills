## Description:

Data Analysis Pro helps agents perform natural-language data analysis, interpretation, and visualization through the ChartGen API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to submit CSV, Excel, or JSON data with natural-language questions for analysis, interpretation, and chart generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary readable local CSV, Excel, or JSON files to the third-party ChartGen API.

Mitigation: Only provide files intended for ChartGen processing; avoid sensitive or regulated datasets and use a limited-scope API key.

Risk: Generated chart HTML may contain unsafe remote-controlled content handling.

Mitigation: Treat generated HTML reports as untrusted until reviewed, and open or share them only in controlled environments.

## Reference(s):

- [Data Analysis Pro on ClawHub](https://clawhub.ai/chartgen-ai/skills/data-analysis-pro)
- [ChartGen](https://chartgen.ai)
- [ChartGen API endpoint](https://chartgen.ai/api/platform_api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, files, guidance]

**Output Format:** [Markdown text, ECharts JSON, and optional HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and sends provided file or JSON data to the ChartGen API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

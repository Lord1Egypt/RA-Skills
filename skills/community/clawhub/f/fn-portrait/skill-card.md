## Description:

FN Portrait Toolkit helps agents guide financial report footnote extraction, LLM-assisted analysis, and portrait chart generation for Chinese A-share listed companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapufan](https://clawhub.ai/user/mapufan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a pipeline that downloads Chinese annual-report PDFs, extracts financial note data, performs optional LLM analysis, and generates Excel outputs and portrait visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote LLM providers may receive analysis prompts and require API keys.

Mitigation: Prefer local Ollama when appropriate, or knowingly opt into DeepSeek or Moonshot and avoid exposing unrelated API keys.

Risk: Dependencies are unpinned in the artifact requirements.

Mitigation: Install in an isolated Python environment and consider pinning dependencies before production use.

Risk: CNINFO report downloads use HTTP and downloaded PDFs are untrusted inputs.

Mitigation: Treat downloaded PDFs as untrusted files and review handling before using the pipeline in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mapufan/skills/fn-portrait)
- [FN Portrait Toolkit README](README.md)
- [CNINFO disclosure search](http://www.cninfo.com.cn/new/commonUrl/pageOfSearch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and file path descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation, LLM provider configuration, report download, data extraction, Excel analysis, and portrait chart generation.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

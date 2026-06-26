## Description: <br>
Clawlens analyzes OpenClaw conversation history to surface usage patterns, friction points, and skill effectiveness for a personal OpenClaw retrospective. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dunzhang](https://clawhub.ai/user/dunzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Clawlens to analyze local conversation history, identify usage patterns and friction points, and generate a personal retrospective report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation history and derived summaries may be sent to an external LLM provider. <br>
Mitigation: Run only with a trusted provider and limit the analysis scope with --days and --max-sessions before execution. <br>
Risk: Automatic model detection can use saved OpenClaw credentials from local configuration. <br>
Mitigation: Specify --model with an intentionally provided API key when avoiding saved credential use is important. <br>
Risk: Cached facet files may retain sensitive derived analysis after the report is generated. <br>
Mitigation: Delete the .clawlens-cache directory after use when generated facets contain sensitive information. <br>


## Reference(s): <br>
- [Clawlens Report Format Reference](references/report-format.md) <br>
- [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report by default, or self-contained HTML when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the report to stdout or to a user-specified output file; verbose progress is emitted on stderr.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

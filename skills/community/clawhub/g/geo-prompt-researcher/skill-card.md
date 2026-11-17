## Description:

AI Prompt Researcher helps generate prompt research reports for GEO strategy across ChatGPT, Perplexity, Gemini, and Claude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

Marketing, content, and GEO teams use this skill to generate and prioritize AI search prompts for a brand or category, identify competitor gaps, cluster prompt opportunities, and produce local research outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-specified output path can overwrite an existing local report file.

Mitigation: Choose output filenames deliberately and review the target path before running the CLI with --output.

Risk: Business context provided for prompt research may appear in generated local reports.

Mitigation: Provide only brand, category, competitor, and audience details that are appropriate to include in the report.

Risk: The documentation mentions advanced scripts that are not included in this artifact.

Mitigation: Use the included scripts/research_prompts.py workflow unless additional scripts are obtained and verified separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geoly-geo/skills/geo-prompt-researcher)
- [Prompt Taxonomy](artifact/references/prompt-taxonomy.md)
- [AI Platform Guide](artifact/references/platform-guide.md)
- [Prompt Templates](artifact/references/prompt-templates.md)
- [Research Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown research report or JSON prompt list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included CLI can write output to stdout or to a user-specified local file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

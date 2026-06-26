## Description: <br>
Automatically converts long-form video, blog, and podcast content into platform-specific social media scripts, threads, transcripts, summaries, and related JSON assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, podcasters, agencies, and developers use this skill to transform source transcripts, articles, and podcast text into reusable social posts, short-form scripts, summaries, transcripts, and batch outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install identity may be confused with similarly named npm or ClawHub packages. <br>
Mitigation: Confirm the publisher handle, ClawHub skill page, version, and reviewed release before installing. <br>
Risk: User-provided content may be sent to OpenAI for AI-powered transformations. <br>
Mitigation: Use a restricted OpenAI API key and avoid submitting confidential or regulated content unless that processing is acceptable. <br>
Risk: Batch processing can execute jobs and write generated files based on a supplied configuration. <br>
Mitigation: Run only trusted batch configs after reviewing job names, content sources, and output paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/ai-content-repurposer-pro) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [Batch Configuration Example](examples/batch-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content can be written to JSON files; AI-powered transformations require an OpenAI API key, with demo/template output when no key is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

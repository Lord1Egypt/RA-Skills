## Description: <br>
AI Content Repurposer converts long-form content such as video transcripts, blog posts, and podcast transcripts into platform-specific scripts, social posts, summaries, and transcript formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, agencies, and podcasters use this skill to turn one long-form asset into reusable short-form video scripts, social media posts, summaries, quote cards, and formatted transcript outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User content may be sent to OpenAI for AI-powered transformations. <br>
Mitigation: Use a dedicated OpenAI API key and avoid processing confidential or regulated content unless organizational policy approves that processing. <br>
Risk: Batch processing can write files outside the requested output folder according to the security summary. <br>
Mitigation: Run only trusted batch configuration files and write outputs to a dedicated directory as a normal, non-privileged user. <br>
Risk: Generated social content, summaries, and transcripts may be inaccurate or unsuitable for publication without review. <br>
Mitigation: Review all generated outputs before publishing and verify claims against the original source content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/ai-content-repurposer) <br>
- [README](README.md) <br>
- [Skill Documentation](SKILL.md) <br>
- [Quick Start Guide](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON files or console text with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include platform-specific scripts, social post drafts, summaries, quotes, transcript sections, hashtags, calls to action, and demo fallback content when no OpenAI API key is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

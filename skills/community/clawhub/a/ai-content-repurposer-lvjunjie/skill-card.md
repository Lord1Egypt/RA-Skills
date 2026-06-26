## Description: <br>
Converts long-form videos, blog posts, and podcast transcripts into platform-specific short scripts, social posts, formatted transcripts, summaries, and quote-ready content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, podcasters, and agencies use this skill to turn source transcripts, articles, and episode text into channel-specific assets for TikTok, YouTube Shorts, Instagram Reels, Twitter, LinkedIn, and podcast publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-powered transformations send selected content to OpenAI using the configured API key. <br>
Mitigation: Use a dedicated API key where possible and avoid processing confidential, regulated, client, or unpublished material unless that external processing is acceptable. <br>
Risk: Commands can read input files, fetch blog URLs, process batch configs, and write output files. <br>
Mitigation: Review file paths, URLs, batch configuration, and output destinations before allowing an agent to run the tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/ai-content-repurposer-lvjunjie) <br>
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact quickstart](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON files or console text with command-line usage and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI-powered mode uses an OpenAI API key; without a key the artifact returns demo/template output. Some commands can read local files, fetch blog URLs, and write JSON outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Repurpose a single piece of content (tweet, article, description) into 10+ formats: Twitter thread, LinkedIn post, blog intro, email newsletter, Discord announcement, Reddit post, Quora answer, Instagram caption, email subject lines, and meta descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing teams use this skill to turn one piece of source text into platform-specific marketing drafts, including social posts, newsletter copy, subject lines, and SEO meta descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text, including content loaded from @file inputs, is sent to MiniMax/OpenClaw for generation. <br>
Mitigation: Use only content approved for external processing and avoid confidential, regulated, or secret material unless that processing is approved. <br>
Risk: The skill requires a MiniMax API key. <br>
Mitigation: Provide the key through the MINIMAX_API_KEY environment variable and manage it as a sensitive credential. <br>


## Reference(s): <br>
- [Content Repurposer ClawHub page](https://clawhub.ai/fuzzyb33s/content-multiplier-fuzzyb33s) <br>
- [MiniMax text completion API endpoint](https://api.minimax.chat/v1/text/chatcompletion_pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files] <br>
**Output Format:** [Structured JSON printed to stdout with optional per-format text and JSON files saved locally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates platform-specific drafts using the selected content type and tone; output may be saved to an output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

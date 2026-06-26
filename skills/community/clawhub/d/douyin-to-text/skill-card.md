## Description: <br>
Extracts Douyin video captions or transcripts from share links, and can query dytext balance and transcription history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwchris](https://clawhub.ai/user/xwchris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to extract text from Douyin share links, select a supported transcription language, or check dytext account balance and transcription history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Douyin links and a dytext API key to the dytext service. <br>
Mitigation: Install only if you trust dytext.cn and protect the local ~/.dycaption credential file. <br>
Risk: The skill executes the dytext-cli npm package through npx. <br>
Mitigation: Review the dytext-cli package source and npm package before deployment in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xwchris/douyin-to-text) <br>
- [dytext website](https://dytext.cn) <br>
- [dytext-cli npm package](https://www.npmjs.com/package/dytext-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown responses based on dytext-cli output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js npx and a dytext API key; sends Douyin links and the API key to api.dytext.cn for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

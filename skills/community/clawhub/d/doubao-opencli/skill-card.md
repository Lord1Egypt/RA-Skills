## Description: <br>
doubao-opencli helps an agent automate a logged-in Doubao session through OpenCLI and Edge for chat, batch questions, image generation, AI podcast generation, PPT generation, meeting summaries, and conversation backups. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run PowerShell-based OpenCLI workflows against Doubao for conversational responses and generated files such as images, podcasts, PPT decks, logs, summaries, and backups. It is best treated as a learning or testing automation release because the release evidence warns against production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts automate a logged-in Doubao account through Edge. <br>
Mitigation: Run the skill only with accounts and browser profiles appropriate for automation, preferably a separate profile or account. <br>
Risk: The security evidence flags an unsafe PPT input path. <br>
Mitigation: Avoid untrusted topic, outline, or draft inputs for PPT generation until the input handling issue is fixed. <br>
Risk: Local output, logs, and backups may contain private prompts, documents, conversations, or generated media. <br>
Mitigation: Review output directories regularly, delete sensitive artifacts, and avoid feeding confidential material into the workflows. <br>
Risk: The release evidence warns that production use may create copyright concerns. <br>
Mitigation: Treat generated or downloaded content as testing material unless usage rights have been reviewed for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/doubao-opencli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/openclawzhangchong) <br>
- [Doubao chat](https://www.doubao.com/chat) <br>
- [Doubao image creation page](https://www.doubao.com/chat/create-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [PowerShell commands, plain text responses, Markdown logs, and downloaded local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include JPG images, WAV podcast audio, PPTX decks, Markdown logs, summaries, and backup files under local output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

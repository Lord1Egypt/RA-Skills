## Description: <br>
Analyzes a Douyin video from a shared URL by extracting page metadata, capturing audio when possible, transcribing speech, summarizing content, extracting useful information with evidence, applying critical analysis, and saving transcript and analysis notes into Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzmbobby](https://clawhub.ai/user/zzmbobby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, creators, and content operators use this skill to turn Douyin links into structured video transcripts, evidence-aware summaries, and critical analysis notes. It is best suited for analyzing short-form video claims, hooks, persuasion tactics, AI-assisted writing likelihood, and reusable research takeaways. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use an active browser session cookie when downloading Douyin media. <br>
Mitigation: Run it only with a browser profile you trust for this task, restrict downloads to known Douyin or ByteDance media hosts, and require manual confirmation before cookie-authenticated downloads. <br>
Risk: The helper scripts write transcript and analysis files into a configured Obsidian vault. <br>
Mitigation: Verify the configured vault and inbox paths before use, and add a confirmation step before persistent note writes. <br>
Risk: Temporary audio files are saved under /tmp/douyin_transcribe. <br>
Mitigation: Review and delete temporary media after analysis when it is no longer needed. <br>
Risk: Machine transcripts may contain errors in names, numbers, and segmentation. <br>
Mitigation: Label transcript quality clearly and review important claims before relying on the analysis. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zzmbobby/douyin-video-analysis) <br>
- [Douyin website](https://www.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, chat summaries, JSON helper output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates transcript and analysis notes in an Obsidian vault; helper scripts may save temporary audio under /tmp/douyin_transcribe.] <br>

## Skill Version(s): <br>
0.1.4 (source: release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

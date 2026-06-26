## Description: <br>
Converts research reports, long-form articles, and technical documents into listenable podcast audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn URLs, PDFs, Markdown, text files, or pasted research content into short audio briefings for review during commuting, exercise, or other hands-free workflows. It can also set a scheduled workflow that fetches recent AI papers, summarizes them, generates audio, and optionally sends the result to a messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can fetch external URLs and run scheduled retrieval of recent papers, which may process sensitive or unintended content. <br>
Mitigation: Review source URLs and scheduled jobs before enabling them, and avoid using private or sensitive documents unless the runtime and logs are trusted. <br>
Risk: Optional delivery through Feishu, WeChat, or email can send generated summaries or audio outside the local environment. <br>
Mitigation: Keep push_to disabled for sensitive documents and verify destinations, credentials, logs, and disable controls before enabling delivery. <br>
Risk: The artifact describes offline privacy, but the full workflow may still require network access for URL fetching, model downloads, and message delivery. <br>
Mitigation: Treat offline operation as limited to local TTS after model installation and confirm network behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-research-podcast) <br>
- [arXiv cs.AI recent papers feed](https://arxiv.org/list/cs.AI/recent) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus generated MP3 or WAV audio files and optional delivery status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audio defaults described by the artifact include MP3 output, 128 kbps bitrate, 16000 Hz sample rate, selectable voice, adjustable speed, and optional Feishu, WeChat, or email delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

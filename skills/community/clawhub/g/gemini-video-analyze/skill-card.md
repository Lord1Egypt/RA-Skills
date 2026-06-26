## Description: <br>
Send a public video URL directly to a Google Gemini model for analysis. Use when Codex must summarize a video, answer questions about video content, or extract key points from a URL without local download or file upload steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tokyo-s](https://clawhub.ai/user/tokyo-s) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to analyze public video URLs with Google Gemini for summaries, Q&A, key point extraction, timeline reports, or moderation-oriented review without downloading the video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs and analysis prompts are sent to Google Gemini under the user's API account. <br>
Mitigation: Use public URLs, avoid secrets or confidential material in prompts or signed URLs, and follow the applicable Google Gemini account terms and organizational data policy. <br>
Risk: Supplying an API key as a command-line argument can expose it through shell history or process listings. <br>
Mitigation: Prefer GEMINI_API_KEY or GOOGLE_API_KEY environment variables over the --api-key option. <br>
Risk: The analyzer depends on the third-party google-genai Python package. <br>
Mitigation: Install google-genai from a trusted package source and keep dependency management consistent with the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tokyo-s/gemini-video-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and command examples; analyzer output is plain text from Gemini.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public video URL, a task prompt, a Gemini API key, and the google-genai Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

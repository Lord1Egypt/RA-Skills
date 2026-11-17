## Description:

Send a public video URL directly to a Google Gemini model for analysis, summaries, question answering, or key point extraction without local download or file upload steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokyo-s](https://clawhub.ai/user/tokyo-s)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to analyze publicly accessible video URLs with Google Gemini, including concise summaries, Q&A, timelines, moderation reviews, and key point extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs and prompts are sent to Google Gemini for analysis.

Mitigation: Use public URLs only and avoid confidential, signed, internal, or otherwise sensitive links and prompts.

Risk: Passing an API key on the command line may expose it through shell history or process listings.

Mitigation: Prefer GEMINI_API_KEY or GOOGLE_API_KEY environment variables over the --api-key argument.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown analysis returned from Gemini, with optional shell command examples and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public video URL, a task-specific prompt, the google-genai Python dependency, and GEMINI_API_KEY or GOOGLE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

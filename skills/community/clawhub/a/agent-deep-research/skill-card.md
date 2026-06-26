## Description: <br>
Deep Research (Gemini) runs asynchronous Gemini research jobs, grounds answers in explicitly selected local files, estimates costs, and returns reports or structured JSON for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24601](https://clawhub.ai/user/24601) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to launch Gemini-backed deep research, ground analysis in local documents or code, manage file search stores, and retrieve research reports for downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload explicitly selected local files to Google Gemini for grounded research. <br>
Mitigation: Use dry-run and narrow context paths, avoid secrets or credential files, and use a scoped API key. <br>
Risk: Non-interactive agent runs can skip confirmations for deleting stores or clearing local state. <br>
Mitigation: Require an allowlist or approval step before store deletion, state clearing, or garbage collection commands. <br>
Risk: Security evidence marks the release for review because uploads and remote store deletion can affect sensitive data or resources. <br>
Mitigation: Review the selected files, command arguments, and cleanup actions before deployment in autonomous workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/24601/agent-deep-research) <br>
- [Project homepage](https://github.com/24601/agent-deep-research) <br>
- [Agent briefing](AGENTS.md) <br>
- [File Search MIME Type Guide](references/file_search_guide.md) <br>
- [Online Documentation References](references/online_docs.md) <br>
- [Gemini Deep Research API](https://ai.google.dev/gemini-api/docs/deep-research) <br>
- [Gemini File Search API](https://ai.google.dev/gemini-api/docs/file-search) <br>
- [Google GenAI Python SDK](https://googleapis.github.io/python-genai/) <br>
- [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown reports, JSON command responses, and optional HTML or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research can run asynchronously; stdout is machine-readable JSON while detailed human progress is written separately.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release metadata; artifact frontmatter reports 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

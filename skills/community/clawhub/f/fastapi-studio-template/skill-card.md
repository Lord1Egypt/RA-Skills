## Description: <br>
Bootstrap a dark-themed FastAPI+HTMX studio app with SSE real-time progress, blind test mode, SQLite ratings, and Langfuse tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap FastAPI and HTMX studio applications for generative AI comparison, A/B testing, human evaluation, real-time generation progress, SQLite-backed ratings, and optional Langfuse tracing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Langfuse tracing code can capture prompts or outputs if tracing is enabled. <br>
Mitigation: Configure Langfuse deliberately and avoid tracing sensitive prompts or outputs unless that collection is intended. <br>
Risk: Tracing sends data to the configured Langfuse endpoint. <br>
Mitigation: Verify the Langfuse endpoint before use and keep tracing limited to the user's intended self-hosted or personal Langfuse account. <br>
Risk: The worked example uses public HTMX CDN links. <br>
Mitigation: Replace the CDN links with local or pinned assets before production deployment. <br>
Risk: Generated application code may need adaptation before deployment. <br>
Mitigation: Review and scan generated code, configuration, and tracing behavior before using it in a deployed studio app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/fastapi-studio-template) <br>
- [HTMX 1.9.12 CDN reference](https://unpkg.com/htmx.org@1.9.12) <br>
- [HTMX SSE extension CDN reference](https://unpkg.com/htmx.org@1.9.12/dist/ext/sse.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, SQL, HTML, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes FastAPI, HTMX SSE, SQLite ratings, and Langfuse tracing patterns; requires python3 and optional LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY configuration.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

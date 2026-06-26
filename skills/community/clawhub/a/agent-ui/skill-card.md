## Description: <br>
Batteries-included agent component for React/Next.js from ui.inference.sh with runtime, tools, streaming, approvals, widgets, and client-side tool support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add a React/Next.js agent UI component for AI chat interfaces, SaaS copilots, assistants, approval flows, streaming responses, and browser-side tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a remote UI component and SDK package from third-party sources. <br>
Mitigation: Review the remote component and @inferencesh/sdk source before installation, and pin versions where practical. <br>
Risk: The proxy route depends on an inference API key. <br>
Mitigation: Keep INFERENCE_API_KEY server-side and protect the proxy route with authentication and rate limits. <br>
Risk: File and image uploads may send user data to external services. <br>
Mitigation: Limit upload permissions and disclose external provider data handling before production use. <br>
Risk: Browser-side tools can read or modify form fields. <br>
Mitigation: Require user confirmation before client-side tools access or change sensitive form data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/agent-ui) <br>
- [Agent Component Docs](https://ui.inference.sh/blocks/agent) <br>
- [Agent Component Registry](https://ui.inference.sh/r/agent.json) <br>
- [Agents Overview](https://inference.sh/docs/agents/overview) <br>
- [Agent SDK](https://inference.sh/docs/api/agent/overview) <br>
- [Human-in-the-Loop](https://inference.sh/docs/runtime/human-in-the-loop) <br>
- [Agents That Generate UI](https://inference.sh/blog/ux/generative-ui) <br>
- [Agent UX Patterns](https://inference.sh/blog/ux/agent-ux-patterns) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline TypeScript, TSX, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for a Next.js proxy route, INFERENCE_API_KEY configuration, component usage, file and image upload options, and client-side tools.] <br>

## Skill Version(s): <br>
0.1.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

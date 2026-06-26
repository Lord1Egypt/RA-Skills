## Description: <br>
Builds a customizable local HTML dashboard with Alpine.js, Vanilla CSS, and a Python backend for visualizing Fulcra data, with guidance for sanitized public exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Fulcra users use this skill to scaffold and customize a local dashboard for private Fulcra data, then prepare a sanitized read-only export when they choose to share selected data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Fulcra data and includes local file-browsing behavior. <br>
Mitigation: Run the dashboard only on localhost, fetch only user-approved Fulcra data, and review every exported file before sharing. <br>
Risk: The local chat relay may later connect dashboard messages to an agent workflow. <br>
Mitigation: Enable the relay only after explicit user approval, keep it local, and review any polling or agent-connection setup before use. <br>
Risk: The dashboard template loads third-party web scripts and fonts. <br>
Mitigation: For sensitive deployments, review those dependencies and consider bundling pinned JavaScript and fonts locally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fulcra/fulcra-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML, CSS, JavaScript, Python, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local dashboard scaffold and optional sanitized public-export assets; data ingestion requires user consent.] <br>

## Skill Version(s): <br>
0.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

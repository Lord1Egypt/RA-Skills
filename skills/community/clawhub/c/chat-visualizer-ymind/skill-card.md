## Description: <br>
YMind Chat Visualizer turns public or pasted AI chat transcripts into interactive D3.js thinking maps with reasoning nodes, thinking shifts, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yslenjoy](https://clawhub.ai/user/yslenjoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch or parse AI chat transcripts, extract a structured thinking graph, and render local HTML, PNG, JSON, and Markdown outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves complete fetched or pasted chat transcripts in the local YMind workspace. <br>
Mitigation: Use a controlled output directory, avoid confidential or regulated conversations, and review or delete raw_chat.json and graph.html after use. <br>
Risk: Generated HTML loads third-party CDN assets for visualization. <br>
Mitigation: Open generated HTML only in environments where external asset loading is acceptable, or review and adapt the template for offline use. <br>
Risk: Auto-fetch behavior uses browser automation for some providers and may encounter platform anti-bot controls. <br>
Mitigation: Prefer paste mode for sensitive or unreliable fetches, and only fetch public share links that the user intentionally provides. <br>


## Reference(s): <br>
- [YMind Graph Schema Reference](references/graph-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/yslenjoy/chat-visualizer-ymind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated JSON, HTML, PNG, and workspace index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores raw_chat.json, graph.json, graph.html, graph.png when screenshot support is available, meta.json, index.json, and index.html under a local YMind workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

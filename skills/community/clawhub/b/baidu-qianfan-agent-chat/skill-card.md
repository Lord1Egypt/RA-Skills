## Description: <br>
Calls the Baidu Qianfan AI application chat API for streaming or non-streaming conversations, function-call tool use, file references, and session-based interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilitong9607](https://clawhub.ai/user/lilitong9607) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a Baidu Qianfan application, pass prompts and optional file or tool-call context, and manage multi-turn chat sessions from a Python command-line helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, file references, metadata, and conversation context are sent to Baidu Qianfan. <br>
Mitigation: Use the skill only for approved Qianfan workflows, verify the app_id, use a scoped API key, and avoid sensitive or regulated data unless approved. <br>
Risk: Local session reuse can carry conversation context between runs. <br>
Mitigation: Use --new-session or remove state/session.json when switching contexts. <br>


## Reference(s): <br>
- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan-api/s/7m7wqq361) <br>
- [Baidu Wenxin Workshop](https://cloud.baidu.com/product/wenxinworkshop) <br>
- [Local Qianfan API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime output is streamed text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QIANFAN_API_KEY and can persist conversation_id in state/session.json for session reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Helps agents find 302.AI APIs, retrieve relevant documentation, and generate integration code for language, image, video, audio, and other API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharkqwy](https://clawhub.ai/user/sharkqwy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to identify suitable 302.AI APIs and produce implementation examples, commands, and configuration guidance for API integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is broad and may activate for many API or AI requests. <br>
Mitigation: Use it only when 302.AI-centered API integration help is intended, and confirm the selected API before applying generated code. <br>
Risk: The skill asks for a 302.AI API key and generated examples may expose credentials if copied directly. <br>
Mitigation: Use environment variables or limited test keys, avoid pasting live production keys into chat, and never commit generated code containing secrets. <br>
Risk: Generated API calls may send user data to 302.AI or upstream services. <br>
Mitigation: Review generated code and documentation before running it, and avoid sending private or regulated data unless that transfer is intended and approved. <br>


## Reference(s): <br>
- [API Category Index](references/api_categories.md) <br>
- [Integration Code Templates](references/integration_examples.md) <br>
- [API List Parser Usage](references/parse_script_usage.md) <br>
- [302.AI Documentation](https://doc.302.ai/) <br>
- [302.AI API List](https://doc.302.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/sharkqwy/302ai-api-integration-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated API request snippets, selected documentation links, and security notes for API key handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

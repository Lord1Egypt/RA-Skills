## Description: <br>
Redesign and beautify PowerPoint/PDF presentation decks into polished, on-brand slides using Deckly's AI. Use when the user wants to improve, beautify, restyle, or redesign a .pptx or .pdf deck, asks to "make slides look better", or mentions Deckly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmymelbj](https://clawhub.ai/user/jimmymelbj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users with presentation decks use this skill through an agent to analyze PPTX or PDF files, choose a visual style, preview or fine-tune slides, and download a redesigned PPTX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation contents are uploaded to Deckly for analysis and redesign. <br>
Mitigation: Use the skill only for decks that are appropriate to send to Deckly, and confirm the user's consent before uploading sensitive or proprietary presentations. <br>
Risk: Authentication flows can ask for passwords or email verification codes in chat. <br>
Mitigation: Prefer an existing manually created API key or a throwaway account, and avoid pasting existing account passwords or verification codes into the agent conversation. <br>
Risk: Full redesign, continue, fine-tune, and one-shot actions can spend paid Deckly credits. <br>
Mitigation: Check balance and quote output first, then get explicit user confirmation before running any paid action. <br>


## Reference(s): <br>
- [Deckly API Reference](reference.md) <br>
- [Deckly Service](https://deckly.art) <br>
- [Server-Resolved Source Repository](https://github.com/jimmymelbj/deckly-redesign-skill) <br>
- [ClawHub Skill Listing](https://clawhub.ai/jimmymelbj/deckly-redesign-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the Python standard library CLI and Deckly API; may upload presentation files, save an API key locally, and download a redesigned deck.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

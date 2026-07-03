## Description: <br>
Multi-modal content creation workflow for freelance creators. Receives customer requests via WhatsApp (text or voice note), transcribes audio with the OpenAI Whisper API, generates images with DALL-E 3, and replies to the customer with the result. Use to automate end-to-end request-to-image delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelance creators and operators use this skill to automate request intake, audio transcription, image generation, and customer replies for content-creation jobs received through WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer WhatsApp text and voice-note content may be sent to external AI and messaging providers. <br>
Mitigation: Use the workflow only when operators are comfortable sharing that content with the configured providers and have appropriate customer consent and data-handling controls. <br>
Risk: The WhatsApp token appears to be stored locally in plaintext. <br>
Mitigation: Move token storage to an OS secret manager or a permission-restricted file, and warn operators before using real WhatsApp credentials. <br>
Risk: Dependencies are declared with lower-bound version ranges. <br>
Mitigation: Pin dependencies to reviewed versions before production use. <br>


## Reference(s): <br>
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) <br>
- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/content-creator-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Files, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime scripts produce transcript text, PNG image files, and WhatsApp reply text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OPENAI_API_KEY; generated files default to ./generated and can be redirected with CONTENT_CREATOR_OUTPUT_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Generates an AI image from a user prompt, saves it locally, and sets it as the desktop wallpaper on Windows or macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyulingyue](https://clawhub.ai/user/liyulingyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to generate desktop wallpaper from a natural-language prompt and apply it automatically on Windows or macOS. It is intended for local desktop customization workflows that can provide a Baidu AIStudio access token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed when passed on the command line or sent to an untrusted configured endpoint.

Mitigation: Use BAIDU_API_KEY from a protected environment, keep the endpoint trusted, and review any --base_url override before execution.

Risk: The skill changes the user's desktop wallpaper and stores the generated image locally.

Mitigation: Run it only after explicit user intent, confirm Windows or macOS support, and inspect or manage assets/wallpaper.png according to local retention needs.

Risk: The Python dependency is declared as openai>=1.0.0, which allows future package versions.

Mitigation: Pin and review dependencies in controlled environments before installation or automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyulingyue/skills/ai-wallpaper-skill)
- [Baidu AIStudio AccessToken console](https://aistudio.baidu.com/account/accessToken)
- [Baidu AIStudio OpenAI-compatible endpoint](https://aistudio.baidu.com/llm/lmapi/v3)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and a local PNG image output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes assets/wallpaper.png and may change the current desktop wallpaper on supported platforms.]

## Skill Version(s):

1.0.3 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

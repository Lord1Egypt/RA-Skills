## Description: <br>
Fetches humorous Chinese jokes using third-party APIs such as Hitokoto and JokeAPI, with timeout and error-handling guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Chinese joke text from disclosed third-party APIs and to generate example Bash or Python usage for those APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on third-party joke APIs that may be unavailable, slow, rate limited, or return unexpected responses. <br>
Mitigation: Use the documented timeouts, error handling, and fallback API behavior before relying on the output in an agent workflow. <br>
Risk: Using the skill makes outbound network requests to Hitokoto and jokeapi.cn. <br>
Mitigation: Install and run the skill only in environments where outbound requests to those disclosed services are acceptable. <br>


## Reference(s): <br>
- [Chinese Joke Api on ClawHub](https://clawhub.ai/Djttt/chinese-joke-api) <br>
- [Hitokoto](https://hitokoto.cn/) <br>
- [JokeAPI CN](https://jokeapi.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline Bash and Python examples, plus plain-text joke output from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests use disclosed third-party services and may return variable Chinese-language joke content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

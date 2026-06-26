## Description: <br>
Use @ainative/react-sdk to add AI chat, credit tracking, provider setup, and loading/error handling guidance to React apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating the @ainative/react-sdk package into React applications, including installing the package, configuring AINativeProvider, using chat and credit hooks, and handling loading or error UI states. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser examples can expose long-lived AINative API keys when keys are placed in REACT_APP_ or VITE_ variables or passed directly to a client-side provider. <br>
Mitigation: Keep secret API keys on a backend and use only scoped, short-lived, browser-safe tokens in React clients when the service supports them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urbantech/ainative-react-sdk) <br>
- [useChat hook implementation](packages/sdks/react/src/hooks/useChat.ts) <br>
- [useCredits hook implementation](packages/sdks/react/src/hooks/useCredits.ts) <br>
- [AINativeProvider context](packages/sdks/react/src/AINativeProvider.tsx) <br>
- [Package exports](packages/sdks/react/src/index.ts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, TSX, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes React provider, hook, environment variable, and error/loading state guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

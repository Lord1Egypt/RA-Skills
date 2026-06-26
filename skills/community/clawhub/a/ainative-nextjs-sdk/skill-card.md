## Description: <br>
Use @ainative/next-sdk to add AI chat to Next.js apps with App Router and Pages Router examples for streaming chat, server-side client usage, and auth middleware. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when integrating @ainative/next-sdk into Next.js applications, including chat completion API routes, streaming responses, route protection middleware, and server-side AINative client calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AINATIVE_API_KEY could be exposed if copied into client-side code. <br>
Mitigation: Keep AINATIVE_API_KEY server-side only, as stated in the artifact guidance, and store it in server environment configuration such as .env.local. <br>
Risk: Chat routes may transmit sensitive user data to AINative services. <br>
Mitigation: Review privacy and compliance requirements before sending sensitive user data through chat completion routes. <br>
Risk: The installed npm package or publisher may differ from the reviewed ClawHub artifact. <br>
Mitigation: Verify the @ainative/next-sdk package and publisher before installation, matching the security guidance in the server evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urbantech/ainative-nextjs-sdk) <br>
- [Server client source](packages/sdks/nextjs/src/server/createServerClient.ts) <br>
- [Auth middleware source](packages/sdks/nextjs/src/middleware/) <br>
- [App Router example](packages/sdks/nextjs/examples/app-router/) <br>
- [Package exports](packages/sdks/nextjs/src/index.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Next.js App Router and Pages Router examples plus server-side environment variable guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

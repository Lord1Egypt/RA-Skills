## Description: <br>
Helps agents choose, implement, and review browser storage approaches such as localStorage, sessionStorage, IndexedDB, cookies, client persistence, offline data, secure storage, and cleanup strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to select safe browser storage mechanisms and produce storage, cookie, or IndexedDB implementation guidance with namespaced keys, cleanup behavior, and security boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser storage guidance can lead to storing auth tokens, session data, or client-side secrets in storage readable by JavaScript. <br>
Mitigation: Prefer httpOnly, Secure, SameSite cookies for authentication state and avoid storing plaintext tokens, passwords, payment data, or high-value private data in localStorage, sessionStorage, or IndexedDB. <br>
Risk: The activation wording is broad, so the skill may be applied to storage decisions where privacy mode, quota, cookie behavior, or cross-browser differences matter. <br>
Mitigation: Review generated storage choices against the target browser support matrix, data sensitivity, retention requirements, and cleanup strategy before use. <br>


## Reference(s): <br>
- [Browser Storage Patterns](references/storage-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-browser-storage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples and storage selection notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser storage selection rationale, wrapper code, cookie settings, IndexedDB examples, key namespacing, expiration, quota handling, and cleanup strategy.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

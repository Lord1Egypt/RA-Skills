## Description: <br>
Intelligent codebase analysis and understanding with caching. Automatically explores project structure, identifies modules, analyzes dependencies, and answers questions about the codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to index unfamiliar codebases, inspect modules and dependencies, search symbols, answer codebase questions, and generate architecture diagrams before onboarding, refactoring, or code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-local cache files can retain indexed source snippets, including sensitive code or configuration if those files are indexed. <br>
Mitigation: Review ignore configuration before indexing, avoid indexing secret-containing files, and keep cache and export files out of version control. <br>
Risk: Unsafe pickle loading from an existing repository cache could execute code when used on an untrusted repository. <br>
Mitigation: Delete any existing .codebase-intelligence/codebase_index.pkl before running the skill on a repository you do not fully trust. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michealxie001/codebase-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON exports, Mermaid diagrams, and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project-local cache files and optional exported index files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

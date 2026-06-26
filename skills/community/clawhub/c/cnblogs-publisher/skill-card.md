## Description: <br>
Manage CNBlogs (博客园) articles via MetaWeblog API, including saving drafts, publishing, updating, and deleting posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suversal](https://clawhub.ai/user/suversal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to manage CNBlogs posts from an agent-assisted command workflow, including drafting, listing, viewing, updating, publishing, and deleting articles through the MetaWeblog API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CNBlogs credentials could be exposed or reused unsafely. <br>
Mitigation: Use only a revocable CNBlogs MetaWeblog token, rotate any token copied from this package, and avoid printing or committing tokens. <br>
Risk: Live blog actions can publish, update, or delete real posts. <br>
Mitigation: Review commands and target post IDs before execution, avoid running tests/test_all.sh, and test only against disposable content. <br>
Risk: Some scripts disable HTTPS certificate verification. <br>
Mitigation: Fix the scripts to use verified TLS before using this skill with a real blog account. <br>


## Reference(s): <br>
- [CNBlogs Publisher on ClawHub](https://clawhub.ai/suversal/cnblogs-publisher) <br>
- [CNBlogs Publisher README](README.md) <br>
- [CNBlogs MetaWeblog Settings](https://i.cnblogs.com/settings#metaweblog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command-line script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, publish, retrieve, or delete CNBlogs posts when run with valid CNBlogs credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

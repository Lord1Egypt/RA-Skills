## Description: <br>
Automates creation, updates, and deployment of AI competitor intelligence sites to GitHub Pages across global, Chinese, skills, news, and model sub-sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site maintainers use this skill to generate and refresh GitHub Pages-based AI competitor intelligence directories with search-discovered site data, traffic tiers, trends, and insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled update script contains an embedded Serper API key fallback. <br>
Mitigation: Remove and rotate the embedded key, require a user-provided SERPER_API_KEY, and avoid publishing or scheduling until the credential path is reviewed. <br>
Risk: The skill can automatically publish generated changes to GitHub without an explicit review step. <br>
Mitigation: Run it first in a test repository, inspect generated files and git diffs before pushing, and enable daily scheduling only after branch protections or another review path are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/griffithkk3-del/ai-intelligence-site) <br>
- [Serper Search API endpoint](https://google.serper.dev/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated site and JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or replace site data files and publish changes to a configured GitHub repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

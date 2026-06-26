## Description: <br>
Configures ExDoc for Elixir projects including mix.exs setup, extras, groups, cheatsheets, and livebooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or revise ExDoc documentation configuration in Elixir projects, including dependencies, extras, grouping, formatters, and documentation-build checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed documentation configuration may add incorrect dependency versions, output paths, or stale extras paths. <br>
Mitigation: Run mix deps.get, verify each extras and groups_for_extras path exists, then run mix docs and confirm the generated index.html exists. <br>
Risk: Custom HTML or JavaScript added to ExDoc pages can introduce unwanted analytics behavior, clipboard behavior, or other browser-side effects. <br>
Mitigation: Review all before_closing_head_tag and before_closing_body_tag additions before publishing generated documentation. <br>


## Reference(s): <br>
- [ExDoc Configuration Skill](https://clawhub.ai/anderskev/exdoc-config) <br>
- [Advanced Configuration](artifact/references/advanced-config.md) <br>
- [Extras Formats](artifact/references/extras-formats.md) <br>
- [Makeup Syntax Highlighting](https://hexdocs.pm/makeup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Elixir configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose changes to mix.exs, documentation extras, grouping, static assets, and ExDoc build commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

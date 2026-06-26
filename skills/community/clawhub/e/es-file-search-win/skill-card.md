## Description: <br>
This skill helps an agent search Windows files and folders using the Everything command line tool with filters, sorting, formatted output, and CSV export options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thianda91](https://clawhub.ai/user/thianda91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and Windows power users use this skill to have an agent locate files and folders quickly, narrow searches by path or file attributes, sort results, and export search output for follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to run Windows shell commands for file search and export operations. <br>
Mitigation: Review proposed es.exe commands before execution, especially commands that export data or search broad system paths. <br>
Risk: The skill depends on Everything and es.exe being installed and available on PATH or in a known system location. <br>
Mitigation: Verify the Everything installation with es -version and es -get-everything-version before relying on search results. <br>
Risk: Broad file searches or CSV exports may expose sensitive filenames, paths, or metadata. <br>
Mitigation: Limit searches to intended directories and handle exported CSV files according to the user's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thianda91/es-file-search-win) <br>
- [Everything downloads](https://www.voidtools.com/downloads/) <br>
- [Everything command line interface](https://www.voidtools.com/support/everything/command_line_interface/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Windows command examples and search-result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Everything es.exe commands, search filters, sorting options, CSV export commands, installation checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

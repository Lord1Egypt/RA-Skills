## Description: <br>
Download a file from Dropbox by providing its file path, returning the file content as binary data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foundergraph](https://clawhub.ai/user/foundergraph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to download a specified file from a connected Dropbox account for downstream processing. It is intended for workflows where the user provides the Dropbox path and has authorized a Dropbox OAuth2 integration with read access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return contents of Dropbox files selected by the user, including sensitive files if requested. <br>
Mitigation: Use a Dropbox connection with the narrowest practical access and avoid downloading files containing secrets unless those contents may be returned to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foundergraph/dropbox-download) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files] <br>
**Output Format:** [Binary file content returned from Dropbox] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dropbox OAuth2 integration with files.content.read scope; the optional revision parameter is deprecated in favor of specifying the revision in the path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

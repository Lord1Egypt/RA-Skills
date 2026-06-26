## Description: <br>
Control Emacs. Search, edit, navigate, and pair programming with user <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calsys456](https://clawhub.ai/user/calsys456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect, navigate, and edit a running Emacs session through emacsctl when direct editor interaction is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to run Emacs Lisp, read editor contents, and save edits in a running Emacs session. <br>
Mitigation: Install only when editor control is intended, close sensitive buffers, clear copied secrets from the kill ring, and require proposed eval forms or exact diffs before full-buffer reads, edits, or saves. <br>
Risk: Interactive or blocking Emacs functions can hang the agent workflow. <br>
Mitigation: Avoid interactive prompts and blocking Emacs Lisp calls unless the user is present and explicitly approves the action. <br>


## Reference(s): <br>
- [Emacs Control skill page](https://clawhub.ai/calsys456/emacs-control) <br>
- [emacsctl setup](https://github.com/calsys456/emacsctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Emacs Lisp examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose emacsctl commands, Emacs Lisp forms, buffer edits, and setup guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

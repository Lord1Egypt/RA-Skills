## Description: <br>
Summarize and analyze text documents without external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to quickly digest long text documents, extract key points and keywords, inspect document structure and readability, and compare two document versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local text files, so sensitive document contents may be exposed to the agent session. <br>
Mitigation: Use it only with documents the agent is allowed to read and avoid passing unnecessary confidential files. <br>
Risk: The bundled shell script may mishandle file path substitution, which can make results incomplete or fail unexpectedly. <br>
Mitigation: Run on a small non-sensitive sample first, check file paths carefully, and verify the summarized output against the original document. <br>
Risk: Extractive summaries, keyword counts, and comparisons can omit context or overemphasize simple statistical signals. <br>
Mitigation: Treat the output as a drafting aid and review the source document before making decisions from the summary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/bytesagain-doc-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with summaries, ranked bullets, keyword tables, document statistics, outlines, or comparison results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only processing of user-selected text files; outputs are extractive or statistical and should be reviewed before relying on them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Rewrite English prose sentence by sentence into a more academic version using the bundled AWL/NAWL vocabulary list while preserving meaning, tense, claims, and document structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writers use this skill to revise English text into a more academic register while keeping the original meaning, factual scope, citations, and structure intact. It is suited for requests that need both a sentence-level change report and a complete revised Markdown document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes predictable Markdown output filenames, which could overwrite existing files with matching names. <br>
Mitigation: Run it in a working directory where those filenames are acceptable, check for existing files first, or ask the agent to use alternate filenames. <br>
Risk: Academic vocabulary substitutions can unintentionally shift meaning, certainty, tense, or factual scope. <br>
Mitigation: Use the required sentence-level change report to review each revision against the source text before relying on the revised document. <br>


## Reference(s): <br>
- [AWL/NAWL headword list](references/awl-headwords.txt) <br>
- [AWL/NAWL vocabulary table](references/awl.csv) <br>
- [ClawHub skill page](https://clawhub.ai/junwugit/awl-academic-rewriter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files with a sentence-level change table and a complete revised document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses predictable output filenames unless the user asks for a different format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

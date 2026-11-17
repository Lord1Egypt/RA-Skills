## Description:

A demonstration skill for content ingestion workflows that checks a workspace folder for text and Markdown assets, generates a simple inventory report, and prints a summary.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill as a minimal ClawHub publishing and content-ingestion example. It inventories top-level Markdown and text files in a selected workspace folder and reports a simple count and listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inventory can expose Markdown and text filenames from the selected folder.

Mitigation: Point TARGET_DIR only at directories whose file inventory is intended to be reviewed or shared.

Risk: The demo command only lists top-level .md and .txt files, so it can miss nested or other text-like assets.

Mitigation: Extend the command depth and file patterns before using the workflow for production content discovery.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and plain text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists only top-level .md and .txt files in the selected TARGET_DIR.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

# Example: Skill Supply Chain Finding

A candidate OpenClaw skill is downloaded from ClawHub or a git repo and scanned before install.

Expected behavior:
- identify the source as a local folder or ClawHub slug
- stage the install if needed
- collect the scan report
- summarize severity findings
- block High/Critical
- allow lower severities with a warning summary
- quarantine only if the policy explicitly allows it
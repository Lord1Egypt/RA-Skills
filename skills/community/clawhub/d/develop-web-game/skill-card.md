## Description: <br>
Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development and testing loop: implement small changes, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots/text, and review console errors with render_game_to_text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tbeard602](https://clawhub.ai/user/tbeard602) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to build or iterate on HTML/JS web games in small increments, then validate gameplay with a Playwright action loop, screenshots, text-state output, and console-error review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security scan verdict is suspicious because a review helper may run nested Codex with full filesystem access and sandbox bypass enabled. <br>
Mitigation: Install or use this only in a trusted ClawHub maintainer workspace, and prefer --no-yolo or AUTOREVIEW_YOLO=0 unless full filesystem access is intentional. <br>
Risk: Authenticated maintainer operations can have high impact if pointed at the wrong target. <br>
Mitigation: Verify the target before approving moderation, pull request publishing, Convex, or other authenticated write operations. <br>


## Reference(s): <br>
- [Action payload examples](artifact/references/action_payloads.json) <br>
- [ClawHub skill page](https://clawhub.ai/tbeard602/develop-web-game) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create or update web game files, progress notes, Playwright action payloads, screenshots, state JSON, and console error logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

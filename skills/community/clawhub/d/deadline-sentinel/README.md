# Deadline Sentinel 1.0.0

A portable OpenClaw task/deadline skill. Requires Node.js 24.16+; no npm packages, provider credentials, Atlas container, or network access.

`SKILL.md` contains usage and storage instructions. The bundled `lib` files are generated from Atlas A3's DeadlineSentinel and JsonFileStore modules by `scripts/build-clawhub-package.mjs`; they preserve the shared SQLite transaction lock and atomic JSON updates. The install folder contains no user tasks or credentials.

For OpenClaw, place this folder under the workspace's `skills` directory or a configured skills extraDir and confirm discovery with `openclaw skills info deadline-sentinel --json`. Use the bundled commands from the discovered skill directory. Registry publication and a registry-install transcript are separate release steps.

License: MIT. Author: Snehanshu Raj. The implementation was developed with Codex assistance, as documented in the assignment Process Log. SQLite transaction semantics follow https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions. OpenClaw skill structure follows https://docs.openclaw.ai/tools/skills.

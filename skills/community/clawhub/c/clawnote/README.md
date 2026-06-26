# Clawnote

OpenClaw Xiaohongshu Ops, packaged as a reusable skill.

A review-first Xiaohongshu workflow for OpenClaw.

This repository packages a practical content-ops flow:

- `xhs-research` for topic discovery and source verification
- `xhs-draft` for Xiaohongshu-style writing
- `xhs-publish-assist` for preview, approval, and exact publish

It is designed for people who want:

- daily draft generation
- Feishu review before posting
- optional exact publish after explicit approval
- local memory of titles, preferences, and decisions

This is not a "one-click growth hack". The core design principle is:

`preview -> approve -> publish`

## What Is Included

```text
clawnote/
├── README.md
├── .gitignore
├── workspace-template/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── PERSONA.md
│   ├── USER.md
│   ├── TOOLS.md
│   ├── PUBLISH_ASSIST.md
│   ├── FEISHU_COMMANDS.md
│   ├── MEMORY.md
│   ├── HEARTBEAT.md
│   └── scripts/
│       ├── build_publish_package.py
│       ├── save_publish_package.py
│       ├── publish_approved_note.py
│       └── write_memory_entry.py
└── docs/
    └── SAFETY.md
```

## What Makes This Different

Compared with common auto-posting workflows, this template emphasizes:

1. Source-first topic validation
2. Real local-practice posts, not generic AI summaries
3. Preview-only by default
4. Exact title confirmation before publish
5. Memory and cron as part of the workflow, not afterthoughts

## Setup

1. Copy `workspace-template/` into your OpenClaw workspace.
2. Replace placeholders in:
   - `USER.md`
   - `PERSONA.md`
   - `TOOLS.md`
3. Set these environment variables before using publish scripts:
   - `XHS_TOOLKIT_ROOT`
   - `XHS_REVIEW_OPEN_ID`
4. Make sure your Xiaohongshu toolkit already works locally.

Example:

```bash
export XHS_TOOLKIT_ROOT="$HOME/path/to/xhs-toolkit-src"
export XHS_REVIEW_OPEN_ID="user:your-feishu-open-id"
```

## Recommended Workflow

1. Ask OpenClaw to draft a post.
2. Review in Feishu.
3. Approve with the exact title.
4. Publish only after explicit confirmation.

Example Feishu command:

```text
写一篇关于 OpenClaw 工作流调试的小红书，写好后先给我审批，我同意后再发送。
```

Approval:

```text
审核通过，发布标题为《xxx》这篇。
```

## Safety

- No unattended auto-publish by default
- No human-behavior spoofing guidance
- Deletion is treated as a separate high-risk action
- Archive-to-draft is not assumed to work unless re-verified for your Xiaohongshu UI

See [docs/SAFETY.md](./docs/SAFETY.md).

## License

Add the license you prefer before publishing this repository.

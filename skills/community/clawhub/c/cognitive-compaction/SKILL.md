---
name: "Cognitive Compaction State Manager"
description: "Actively monitors token utilization and executes memory compaction routines before context bloat causes failures."
version: 1.0.0
author: "OpenClaw Community"
metadata:
  openclaw:
    install:
      - "uv pip install pydantic"
    requires:
      bins: ["python"]
---

# Cognitive Compaction

You have reached a context threshold limit! Your primary task has been temporarily suspended to prevent context bloat and out-of-bounds error. 

Your objective now is to summarize the granular operational steps you just took into a dense semantic summary. Focus heavily on your overarching goal, what you have successfully done thus far, and what actions remain.

Once you write the summary, the backend script will automatically archive your unstructured logs and swap in your summary.

## Current State Compaction Action:
!python3 ${OPENCLAW_SKILL_DIR:-~/.openclaw/skills/cognitive-compaction}/scripts/flush_state.py

Read the output above and ensure your response strictly outlines the progress towards the main goal so you do not suffer from Amnesia when you resume!

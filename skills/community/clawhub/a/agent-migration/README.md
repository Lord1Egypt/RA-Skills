# agent-migration

A higher-privilege OpenClaw skill for renaming or migrating an agent safely.

## What it handles
- agent id rename
- workspace rename
- session content migration
- session display metadata rename (`sessions.json`, related paths)
- restart + verification
- separate confirmation before deleting the old agent

## Typical owner
Usually run by the **`master`** agent.

## Permission note
This skill generally needs elevated local access because it edits OpenClaw config, agent directories, workspace paths, and session metadata.

## Safe default
It **does migrate session content by default** and **does not delete the old agent by default**.

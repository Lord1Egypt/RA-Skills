# Exec Tool (ClawHub Skill)

## Overview
Exec Tool is a controlled system command execution skill designed for OpenClaw environments. It allows secure execution of predefined CLI commands from within ClawHub workflows.

This skill is intended for automation, debugging, and controlled system operations inside VPS environments.

---

## Problem it solves
When working in server environments (such as Hostinger VPS deployments), users often need to trigger system-level commands from automation layers like Telegram bots or OpenClaw agents. This skill bridges that gap safely.

---

## Core functionality
- Executes only allowed system commands
- Currently supports: `clawhub` CLI operations
- Prevents arbitrary or unsafe command execution
- Returns trimmed output for chat interfaces (e.g., Telegram)

---

## Security model
This skill is intentionally restricted:
- Only whitelisted commands are executed
- Prevents destructive operations (rm, sudo, etc.)
- Designed for controlled automation environments

---

## Example usage

### Search skills
clawhub search "Google Workspace"

### Install skill
clawhub install exec_tool

---

## Integration use case
This skill is commonly used in:
- Telegram bot automation
- OpenClaw workflows
- VPS management via chat interfaces
- CI/CD command triggers

---

## Notes
This skill is part of a controlled execution layer and should not be used for unrestricted shell access.

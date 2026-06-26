# Agent Email Skill
## Description
Enables Thundarr to perform outbound communication via the AgentMail.to API. This is the primary notification channel for system health and task completion reports.

## Configuration
Requires a valid AgentMail API key. Sends from the official identity: thundarr@agentmail.to.

## Tools
- **send_mail.py**: A Python script that handles POST requests to the AgentMail v1 API.

## Usage Examples
- "Send a backup success report to my personal email."
- "Alert me if the system temperature exceeds 80 degrees Celsius."

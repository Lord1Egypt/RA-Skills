# Template Recommender Module

Purpose: automatically recommend suitable automation templates based on the user's intent.

This module improves usability so users do not need to know template names in advance.

## Detection Logic

Analyze the user's request and map it to a template when possible.

Examples:

AI / Tech monitoring intent
keywords:
- AI news
- AI monitoring
- tech news
- AI report

→ recommend template: templates/intelligence-system.md

GitHub monitoring intent
keywords:
- GitHub trending
- GitHub projects
- monitor GitHub repos

→ recommend template: templates/github-monitor.md

Keyword news intent
keywords:
- monitor keyword
- track topic
- follow news about

→ recommend template: templates/keyword-news.md

Price tracking intent
keywords:
- monitor price
- crypto price
- stock alert

→ recommend template: templates/price-monitor.md

## Behavior

1. Attempt to match a template.
2. If a match exists → suggest the template to the user.
3. Ask the user to confirm deployment.
4. If no template matches → fall back to custom task creation.

## Example Interaction

User: "Monitor AI news every day"

System:
Detected template: AI intelligence monitoring.
Proposed schedule: daily.
Ask user to confirm deployment.

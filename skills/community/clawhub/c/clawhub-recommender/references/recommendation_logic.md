# Recommendation Logic for ClawHub Skills

This guide outlines how to match user intent to specific skill categories and select the best recommendations.

## Intent Mapping Table

| User Intent / Need | Category | Recommended Skills |
| :--- | :--- | :--- |
| Managing code, repositories, PRs, or issues. | **Development** | `github`, `fast-io`, `capability-evolver` |
| Organizing tasks, projects, or team workflows. | **Productivity** | `linear`, `byterover`, `automation-workflows` |
| Sending messages, social media, or communication. | **Communication** | `wacli`, `bird` |
| Researching topics, finding clean data, or search. | **Search** | `tavily`, `gog` |
| Automating repetitive tasks or multi-step flows. | **Automation** | `automation-workflows`, `capability-evolver` |

## Selection Criteria
1. **Popularity**: Prioritize skills with >10,000 downloads or high star counts.
2. **Official/Verified**: Prefer official integrations (e.g., `github`, `linear`) for stability.
3. **Contextual Fit**: If the user is currently working on a specific project (e.g., a React app), prioritize `fast-io` or `github`.
4. **Recent Trends**: Mention skills that are currently trending in the community (e.g., `capability-evolver`).

## Recommendation Template
When recommending a skill, use the following structure:
- **Skill Name**: [Name] (`slug`)
- **Metrics**: [Downloads/Stars]
- **Description**: [Brief summary of what it does]
- **Why it fits**: [Specific reason based on the current conversation context]
- **Link**: [URL to ClawHub or GitHub]
- **Install Command**: `clawhub install [slug]`

---
name: clawhub-recommender
description: "Recommends popular and highly-rated skills from ClawHub based on user intent and conversation context. Use for: finding new skills, discovering popular tools, matching user needs to existing ClawHub skills."
---

# ClawHub Recommender

This skill helps users discover the best and most popular skills on ClawHub by analyzing their current conversation context and intent.

## Core Functionality

The ClawHub Recommender identifies the user's needs and matches them with high-quality, community-vetted skills. It prioritizes skills with high download counts, star ratings, and official status to ensure reliability and performance.

### When to Use

- When a user expresses a need for a specific functionality (e.g., "I need to manage my GitHub issues").
- When a user asks for general recommendations for popular or useful skills.
- When a user is performing a task that could be significantly improved by an existing ClawHub skill.

## Recommendation Workflow

To provide the most relevant recommendations, follow these steps:

1. **Analyze Context**: Identify the user's current task, expressed pain points, or specific requests for new capabilities.
2. **Identify Intent**: Map the user's need to a category such as Development, Productivity, Communication, or Search.
3. **Consult References**: Read the following reference files to find the best matches:
   - `/home/ubuntu/skills/clawhub-recommender/references/popular_skills.md`: A curated list of top-rated skills with metrics and descriptions.
   - `/home/ubuntu/skills/clawhub-recommender/references/recommendation_logic.md`: Guidelines for matching intents to specific skill categories.
4. **Formulate Recommendation**: Provide a clear and concise recommendation including the skill name, its popularity metrics, a brief description, and why it is a good fit for the current context.
5. **Provide Installation Details**: Include the official link and the installation command (e.g., `clawhub install <slug>`).

## Recommendation Guidelines

| Category | Recommended Skills | Key Metrics |
| :--- | :--- | :--- |
| **Development** | `github`, `fast-io`, `capability-evolver` | High (Official), 35k+ Downloads |
| **Productivity** | `linear`, `byterover`, `automation-workflows` | High (Official), 17k+ Downloads |
| **Communication** | `wacli`, `bird` | 16k+ Downloads, High |
| **Search** | `tavily`, `gog` | High, High |

### Selection Criteria

- **Popularity**: Prioritize skills with over 10,000 downloads or high star counts.
- **Official Status**: Prefer official integrations (e.g., `github`, `linear`) for stability and security.
- **Contextual Relevance**: Ensure the recommended skill directly addresses the user's current task or expressed need.
- **Reliability**: Mention verified skills to build trust with the user.

## Example Recommendation

> **Skill Name**: GitHub (`github`)
> **Metrics**: High (Official Integration)
> **Description**: Manage repositories, issues, and pull requests directly from your agent.
> **Why it fits**: Since you are currently working on a React project and need to track your progress, the GitHub skill will allow you to manage your issues and commits seamlessly.
> **Link**: [GitHub Skill on ClawHub](https://github.com/openclaw/clawhub/tree/main/skills/github)
> **Install Command**: `clawhub install github`

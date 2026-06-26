---
name: find-skills-for-clawhub
description: Search for and discover OpenClaw skills from ClawHub (the official skill registry). Activate when user asks about finding skills, installing skills, or wants to know what skills are available for OpenClaw.
---

# Find Skills for ClawHub

This skill helps you discover and install OpenClaw skills from the ClawHub registry (https://clawhub.ai).

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X with OpenClaw" where X might have an existing skill
- Says "find a skill for X on ClawHub" or "what skills are available for OpenClaw"
- Asks "can OpenClaw do X" where X is a specialized capability
- Expresses interest in extending OpenClaw capabilities
- Wants to search for tools, templates, or workflows in the ClawHub ecosystem
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.) in OpenClaw

## Prerequisites

### 1. Install ClawHub CLI

The ClawHub CLI is required to search and install skills. Install it globally:

```bash
npm i -g clawhub
```

Or use it via npx (slower but no installation):

```bash
npx clawhub search "query"
```

### 2. Login (Optional for Publishing)

For searching and installing, login is not required. For publishing your own skills:

```bash
clawhub login
```

## How to Search for Skills

### Basic Search

```bash
clawhub search "query"
```

Examples:
- `clawhub search "calendar"` - Find calendar-related skills
- `clawhub search "weather"` - Find weather forecasting skills
- `clawhub search "devops"` - Find DevOps and deployment skills

### Search with Limit

```bash
clawhub search "query" --limit 10
```

## How to Install Skills

Once you find a skill you want to install:

```bash
clawhub install <skill-slug>
```

Example:
```bash
clawhub install weather-forecast
```

Skills are installed into your OpenClaw workspace's `skills` directory. OpenClaw will automatically load them in the next session.

## Common Skill Categories

When searching, consider these common categories:

| Category | Example Queries |
|----------|-----------------|
| **Web Development** | react, nextjs, typescript, css, tailwind |
| **Testing** | testing, jest, playwright, e2e |
| **DevOps** | deploy, docker, kubernetes, ci-cd |
| **Documentation** | docs, readme, changelog, api-docs |
| **Code Quality** | review, lint, refactor, best-practices |
| **Design** | ui, ux, design-system, accessibility |
| **Productivity** | workflow, automation, git, todo |
| **APIs & Services** | api, rest, graphql, database |
| **AI & ML** | machine-learning, openai, embeddings |
| **Hardware** | raspberry-pi, iot, sensors, camera |

## Integration with OpenClaw (AI Assistant Guide)

As an AI assistant using this skill, follow these steps when a user asks about OpenClaw capabilities:

### Step 1: Check if ClawHub CLI is available

First, check if `clawhub` is installed by running:
```bash
clawhub --version
```

If not installed, inform the user and offer to install it:
```bash
npm i -g clawhub
```

Alternatively, you can use `npx clawhub` (slower but works without installation).

### Step 2: Search for relevant skills

Run the search command with the user's query:
```bash
clawhub search "query" --limit 5
```

Or using npx:
```bash
npx clawhub search "query" --limit 5
```

### Step 3: Parse and present results

Typical output format:
```
Search results for "weather":

1. weather-forecast v1.2.0 (1,234 installs)
   - Provides weather forecasts using Open-Meteo API
   - Tags: weather, api, forecast
   
2. weather-alerts v0.5.1 (845 installs)
   - Sends weather alerts and notifications
   - Tags: weather, alerts, notifications
   
Install with: clawhub install <skill-slug>
```

Present results to the user with:
1. Skill name and version
2. Install count (popularity indicator)
3. Brief description
4. Relevant tags
5. Installation command

### Step 4: Offer to install

If the user wants to install a skill:
```bash
clawhub install <skill-slug>
```

Or using npx:
```bash
npx clawhub install <skill-slug>
```

### Step 5: Handle no results

If no skills are found:
1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `clawhub init`

## Example Workflow

### User: "How can OpenClaw help me with weather forecasts?"

1. **Search for skills**:
   ```bash
   clawhub search "weather forecast"
   ```

2. **Present results**:
   ```
   Found 3 weather-related skills on ClawHub:
   
   1. weather-forecast (1.2K installs)
      - Provides weather forecasts using Open-Meteo API
      - Install: `clawhub install weather-forecast`
   
   2. weather-alerts (845 installs)
      - Sends weather alerts and notifications
      - Install: `clawhub install weather-alerts`
   
   3. travel-weather (312 installs)
      - Weather planning for travel itineraries
      - Install: `clawhub install travel-weather`
   ```

3. **Offer installation**:
   ```
   Would you like me to install any of these skills for you?
   ```

## Advanced Usage

### Update Installed Skills

Check for updates to all installed skills:

```bash
clawhub update --all
```

### List Installed Skills

See what skills you have installed:

```bash
clawhub list
```

### Publish Your Own Skills

If you create a skill you want to share:

```bash
clawhub publish ./my-skill-folder --slug my-skill --name "My Skill" --version 1.0.0
```

### Sync Local Skills

Back up your local skills to ClawHub:

```bash
clawhub sync --all
```

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Browse categories**: Visit https://clawhub.ai to browse skills by category
4. **Check popularity**: More installs usually indicates a more mature skill

## Troubleshooting

### "clawhub command not found"
- Install with `npm i -g clawhub`
- Or use `npx clawhub` instead

### "No skills found"
- Try broader search terms
- Check https://clawhub.ai to see if skills exist in that category
- Consider creating your own skill with `clawhub init`

### "Permission denied" when installing
- Make sure you have write permissions to the OpenClaw workspace
- Skills install to `<workspace>/skills` by default

## Related Skills

- **skill-creator**: Create and package your own OpenClaw skills
- **find-skills**: Search for skills in the broader AI skills ecosystem (skills.sh)

## Learn More

- **ClawHub Website**: https://clawhub.ai
- **OpenClaw Skills Documentation**: https://docs.openclaw.ai/tools/skills
- **Discord Community**: https://discord.com/invite/clawd

---

*This skill helps bridge the gap between users' needs and the growing ecosystem of OpenClaw skills on ClawHub.*
# Memory Management Patterns

## Daily Memory Files
- **Location**: `memory/YYYY-MM-DD.md`
- **Purpose**: Raw logs of daily activities, decisions, and events
- **Best Practices**:
  - Create automatically if missing for current date
  - Append significant events as they occur
  - Include context, decisions, and outcomes
  - Reference related files or external resources
  - Use consistent formatting for easy parsing

## Long-term Memory
- **Location**: `MEMORY.md`
- **Purpose**: Curated wisdom and distilled insights
- **Best Practices**:
  - Only include information worth remembering long-term
  - Remove outdated or irrelevant content periodically
  - Organize by categories or themes
  - Link to detailed daily logs when appropriate
  - Update during periodic reviews (e.g., weekly)

## Context Loading Strategy
- **Main Sessions**: Load both daily and long-term memory
- **Group Sessions**: Load only daily memory (security consideration)
- **New Sessions**: Always check for existing memory files
- **Memory Gaps**: Handle gracefully when files don't exist

## Memory Writing Guidelines
- **Write Everything Important**: Don't rely on "mental notes"
- **Be Specific**: Include enough detail for future reference
- **Use Timestamps**: For time-sensitive information
- **Link Related Content**: Cross-reference other memory entries
- **Respect Privacy**: Never store sensitive personal data without explicit permission
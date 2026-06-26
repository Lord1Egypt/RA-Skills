# Kole Skill for Claude Code

Official Claude Code skill for SyneHQ Kole - query your databases with SQL, PostgreSQL, and natural language.

## ⚠️ Important: MCP Server Required

**This skill only works if you have the SyneHQ Kole MCP server installed and running.**

The skill provides query patterns and best practices, but actual database queries are executed through the MCP server's tools. You must install the MCP server first.

### Install MCP Server First

```bash
# Install the MCP server
npm install -g @synehq/kole-mcp

# Configure environment
export SYNEHQ_API_KEY="your_api_key"
export SYNEHQ_CONNECTION_ID="your_connection_id"

# Create .mcp.json in your project
# See main README for configuration details
```

## Skill Installation (After MCP Server Setup)

### Option 1: Copy to Skills Directory (Recommended)

```bash
# Copy the skill to your Claude skills directory
cp -r skill ~/.claude/skills/kole
```

### Option 2: Symlink for Development

```bash
# Symlink for automatic updates during development
ln -s $(pwd)/skill ~/.claude/skills/kole
```

### Option 3: NPM Package (After Publishing)

```bash
# Install the npm package globally
npm install -g @synehq/kole-mcp

# The skill will be available at:
# $(npm root -g)/@synehq/kole-mcp/skill/

# Copy or symlink it
cp -r $(npm root -g)/@synehq/kole-mcp/skill ~/.claude/skills/kole
```

## Verification

After installation, restart Claude Code and verify the skill is loaded:

```bash
# The skill should appear in your available skills
# You can invoke it by asking Claude about databases or SQL
```

## Usage

Once installed, Claude will automatically use this skill when you ask about:

- Database queries
- SQL operations
- PostgreSQL commands
- Data analysis
- Database connections
- Table schemas
- Data exploration

### Example Prompts

```
"Show me all my database connections"
"List the tables in my production database"
"Get the top 10 customers by revenue"
"What's the schema of the users table?"
"Run this SQL: SELECT * FROM orders WHERE created_at > '2024-01-01'"
```

## Skill Structure

```
skill/
├── SKILL.md              # Main skill file
├── README.md             # This file
├── references/
│   └── query-patterns.md # SQL query pattern reference
├── examples/
│   └── (future examples)
└── scripts/
    └── (future helper scripts)
```

## Prerequisites

This skill requires the SyneHQ Kole MCP server to be configured. See the main README for setup instructions.

## Development

To modify the skill:

1. Edit `SKILL.md` (main skill instructions)
2. Add reference materials to `references/`
3. Add examples to `examples/`
4. Add helper scripts to `scripts/`
5. Test with Claude Code
6. Commit changes

## Frontmatter Fields

The `SKILL.md` file uses YAML frontmatter:

- `name`: Skill identifier (used for invocation)
- `description`: When to trigger, what it does (IMPORTANT for Claude's decision to use the skill)
- `tools`: Required tools (none for this skill - uses MCP)
- `compatibility`: Prerequisites
- `version`: Skill version (matches package version)

## License

MIT - see LICENSE file in root directory

## Support

- **GitHub**: https://github.com/synehq/kole-mcp
- **Email**: support@synehq.com
- **Docs**: https://docs.synehq.com

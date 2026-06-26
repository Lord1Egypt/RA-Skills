# SQL Assistant — OpenClaw Skill

AI-powered SQL assistant. Generate SQL from natural language, explain queries, optimize performance, review security, and generate migrations — without touching your database.

Powered by [EvoLink.ai](https://evolink.ai)

## Install

### Via ClawHub (Recommended)

```
npx clawhub install ai-sql-assistant
```

### Via npm

```
npx evolinkai-sql-assistant
```

## Quick Start

```bash
# Set your API key
export EVOLINK_API_KEY="your-key-here"

# Generate SQL from natural language
bash scripts/sql.sh query "find all users who signed up last month and have more than 5 orders" --db postgres

# Explain a SQL file
bash scripts/sql.sh explain slow-query.sql

# Optimize a query
bash scripts/sql.sh optimize report.sql --db postgres

# Review SQL for security issues
bash scripts/sql.sh review migration.sql

# Generate a migration
bash scripts/sql.sh migrate "add phone column to users table" --db postgres
```

Get a free API key at [evolink.ai/signup](https://evolink.ai/signup)

## Links

- [ClawHub](https://clawhub.ai/evolinkai/ai-sql-assistant)
- [EvoLink API Docs](https://docs.evolink.ai)
- [Discord](https://discord.com/invite/5mGHfA24kn)

## License

MIT

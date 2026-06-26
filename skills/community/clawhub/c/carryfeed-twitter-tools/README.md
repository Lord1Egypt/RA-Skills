# CarryFeed Twitter Tools Skill

Agent skill for resolving public X/Twitter source context through the CarryFeed CLI.

CarryFeed is useful when an agent needs public profile metadata, post text, article-style link context, or media candidates without browser login prompts. The skill intentionally guides agents to one default path, `npx -y @carryfeed/cli`, so they can act consistently and keep the original source URL beside returned text, author context, and public media metadata.

## Default Usage

```bash
npx -y @carryfeed/cli resolve https://x.com/user/status/123 --compact
npx -y @carryfeed/cli media https://x.com/user/status/123 --compact
npx -y @carryfeed/cli profile NASA --statuses --count 5 --compact
```

## Install From GitHub

After the repository is public:

```bash
npx skills add christian-beep383/carryfeed-agent-tools --skill carryfeed-twitter-tools
```

## Publish To ClawHub

From this skill folder:

```bash
clawhub skill publish . --slug carryfeed-twitter-tools --name "CarryFeed Twitter Tools" --version 0.1.0 --changelog "Initial release"
```

## Boundaries

- Public X/Twitter links only.
- No private, protected, deleted, restricted, suspended, age-gated, or login-only content.
- No posting, liking, following, replying, account actions, surveillance, or bulk scraping.
- Public keyword and hashtag search is planned but not in the first published contract.

## Links

- Website: https://carryfeed.com
- API health: https://api.carryfeed.com/health
- Agent discovery: https://carryfeed.com/llms.txt
- CLI: https://www.npmjs.com/package/@carryfeed/cli

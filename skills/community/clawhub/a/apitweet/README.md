# apitweet-cli

> apitweet-cli is a Node.js command-line client for ApiTweet Twitter/X endpoints. It helps developers and AI agents fetch Twitter/X data, manage API credentials, preview write actions, publish X Articles from Markdown, and automate common X workflows from the terminal.

## Quick facts

- Product: `apitweet-cli`
- Category: Twitter/X API command-line client
- Runtime: Node.js 18 or newer
- Best for: developers, AI agents, growth teams, content operators, and automation workflows
- Main use cases: Twitter/X data retrieval, global trending tweet lookup, tweet/list/profile actions, DM workflows, and Markdown-to-X-Article publishing
- API provider: ApiTweet
- Default API base URL: `https://apitweet.com`
- Authentication: Bearer API key plus optional saved cookie or `auth_token` profile for write actions
- Interfaces: terminal CLI, raw API path calls, Claude/Codex/OpenClaw skill usage
- License: MIT
- Dashboard: [apitweet dashboard](https://apitweet.com/dashboard)

## What it does

- Calls ApiTweet Twitter/X endpoints from the terminal with a stable `apitweet` command.
- Saves reusable app configs for API keys and base URLs.
- Saves reusable auth profiles for cookies, `auth_token`, and `ct0` values.
- Supports generic HTTP-style requests to any ApiTweet path.
- Provides convenience commands for users, search, followers/following, lists, tweets, articles, DMs, profile, timeline, global trending tweets, and follow/unfollow actions.
- Publishes Markdown files as X Articles through the documented draft, cover, title, content, and publish workflow.
- Prints dry-run previews for request payloads before sending them.
- Masks secrets in config output and dry-run previews.

## Who it is for

- Developers who want a terminal-first client for Twitter/X data and actions.
- AI agent builders who need deterministic commands, JSON output, and dry-run previews.
- Growth and research teams that monitor Twitter/X profiles, search terms, followers, lists, and global trending tweets.
- Content teams that draft articles in Markdown and publish them as X Articles.
- Operators who need saved profiles for repeatable Twitter/X workflows without rewriting API request code.

## AI agent use cases

apitweet-cli is designed to be easy for AI coding agents and workflow agents to use safely:

- Preview a write action with `--dry-run` before publishing, following, liking, or updating anything.
- Fetch structured Twitter/X data as JSON for downstream summarization or enrichment.
- Call unsupported endpoints through the raw `apitweet <path>` form.
- Use saved app and profile names instead of pasting credentials into every command.
- Publish a Markdown article with a single command while the CLI handles the multi-step X Article API flow.
- Install and invoke the repository as a Claude/Codex/OpenClaw-style skill.

## Common workflows

### Fetch Twitter/X user data

```bash
apitweet --app prod about elonmusk
apitweet --app prod users elonmusk sama
```

### Search Twitter/X content

```bash
apitweet --app prod search tweets "founder" "ai" --count 20
apitweet --app prod search users "openai"
```

### Get global trending tweets

```bash
apitweet --app prod trending tweets --country "United States" --topic "Sports" --content "NFL" --count 50
```

### Publish Markdown as an X Article

```bash
apitweet --app prod --profile founder --dry-run article publish-md ./article.md --title "Launch Notes"
apitweet --app prod --profile founder article publish-md ./article.md --title "Launch Notes" --cover-image "https://example.com/cover.jpg" --visibility Public
```

### Run a raw ApiTweet request

```bash
apitweet --app prod -X POST -d '["elonmusk","sama"]' /api/twitter/users
```

## Why it is different

- It combines convenience commands with raw path access, so users are not blocked when an endpoint is not wrapped yet.
- It supports both read workflows and authenticated write workflows.
- It treats AI-agent safety as a first-class workflow through `--dry-run`, secret masking, and saved profile names.
- It includes skill/plugin metadata so agents can discover how to install, configure, and run the CLI.
- It keeps the implementation small and dependency-free, with separate modules for parsing, config, request execution, and command routing.

## Install

Install globally from npm:

```bash
npm install -g apitweet-cli
apitweet --help
```

Requires Node.js 18 or newer.

## Use as a skill

Install from a GitHub skill installer:

```bash
npx skills add aliraza948/apitweet
```

Install from ClawHub:

```bash
npx clawhub@latest install apitweet-cli
```

Install as a Claude Code marketplace:

```text
/plugin marketplace add ali/apitweet
/plugin install apitweet-cli@apitweet-cli
```

For manual Claude Code installs, this repository also includes:

```text
.claude/skills/apitweet-cli/
```

Then install the CLI:

```bash
npm install -g apitweet-cli
```

In skills-enabled environments:

- use `/apitweet-cli` after installing the Claude plugin command
- use `$apitweet-cli` in Codex/OpenClaw-style environments
- or ask the agent to use apitweet for installation, auth setup, dry-run previews, or endpoint calls

## Quick start

Get your API key from the apitweet dashboard:

[apitweet dashboard](https://apitweet.com/dashboard)

Save an app config and make a first request:

```bash
apitweet auth apps add --name prod --api-key "sk_1d90c878..."
apitweet auth apps use prod
apitweet --app prod about elonmusk
```

If you are developing from this repository, use:

```bash
cd /home/ali/GitHub/apitweet
node ./bin/apitweet.js --help
```

If you want a local executable command while developing from source:

```bash
npm link
apitweet --help
```

## Config management

When a request is missing an API key, the CLI will include that URL in the error output.

## Security notes

- The CLI reads `APITWEET_KEY`, `APITWEET_BASE_URL`, and `APITWEET_CONFIG_DIR` from the environment.
- The CLI reads and writes persistent config in `~/.apitweet/config.json` by default, or in the directory set by `--config-dir` or `APITWEET_CONFIG_DIR`.
- Saved app configs may contain API keys, and saved profiles may contain cookies, `auth_token`, or `ct0` in plain JSON on disk.
- Avoid storing long-lived credentials on shared machines or CI runners. Prefer an isolated config directory when testing.
- `auth cookie` builds a request path containing the `auth_token`, so treat logs, traces, and network boundaries accordingly.

Save an app config:

```bash
apitweet auth apps add --name prod --api-key "sk_1d90c878..."
apitweet auth apps list
apitweet auth apps use prod
```

Save a write profile:

```bash
apitweet auth profiles add --name founder --cookie "ct0=...; auth_token=..."
apitweet auth profiles use founder
```

Create a profile from `auth_token` via the documented cookie endpoint:

```bash
apitweet auth cookie --auth-token "your_auth_token" --save-as founder
```

Inspect config:

```bash
apitweet config show
apitweet config path
```

By default config is stored in `~/.apitweet/config.json`. For testing, you can isolate it:

```bash
apitweet --config-dir ./.apitweet-local config show
```

## Request examples

Query an endpoint directly:

```bash
apitweet /api/twitter/elonmusk/about
```

Send a JSON body with a POST:

```bash
apitweet -X POST -d '["elonmusk","sama"]' /api/twitter/users
```

Preview a request without sending it:

```bash
apitweet --app prod --dry-run users elonmusk sama
apitweet --app prod --profile founder --dry-run tweet create --text "hello"
apitweet --app prod --profile founder --dry-run article publish-md ./article.md --title "Launch Notes"
```

## Convenience commands

Read commands:

```bash
# Twitter/X User and Search
apitweet --app prod users elonmusk sama           # Lookup user profiles
apitweet --app prod about elonmusk                # Fetch detailed user info
apitweet --app prod search tweets "founder" "ai"  # Search for tweets
apitweet --app prod search users "openai"         # Search for users
apitweet --app prod followers elonmusk            # List user followers
apitweet --app prod following elonmusk            # List user following
 
# Twitter/X Lists
apitweet --app prod list search --query "ai"      # Search for public lists
apitweet --app prod list members 123456789        # List members of a list
apitweet --app prod list subscribers 123456789    # List subscribers of a list
 
# Twitter/X Articles & DMs
apitweet --app prod article markdown 123          # Get x article as Markdown
apitweet --app prod article lookup 123 456        # Batch lookup x articles
apitweet --app prod dm history elonmusk           # Show Direct Message history
apitweet --app prod dm send elonmusk --text "hi"  # Send a DM to a user
 
# Twitter/X Profile & Timeline
apitweet --app prod timeline user elonmusk        # Fetch user timeline page
apitweet --app prod profile update --name "Name"  # Update your own profile

# Twitter/X Global Trending
apitweet --app prod trending tweets --country "United States"
apitweet --app prod trending tweets --country "United States" --topic "Sports" --content "NFL" --count 50

# Twitter/X Tweets
apitweet --app prod tweet lookup 123 --summary    # Batch tweet lookup (id:bool)
apitweet --app prod tweet replies 123             # Get replies for a tweet
```

Write commands:

```bash
apitweet --app prod --profile founder tweet create --text "hello from cli"
apitweet --app prod --profile founder tweet create --text "hello with image" --media-url "https://example.com/a.jpg"
apitweet --app prod --profile founder tweet quote --text "worth reading" --quote-url "https://x.com/user/status/123"
apitweet --app prod --profile founder tweet like 1900000000000000000
apitweet --app prod --profile founder tweet unlike 1900000000000000000
apitweet --app prod --profile founder tweet bookmark 1900000000000000000
apitweet --app prod --profile founder tweet unbookmark 1900000000000000000
apitweet --app prod --profile founder tweet retweet 1900000000000000000
apitweet --app prod --profile founder tweet unretweet 1900000000000000000
apitweet --app prod --profile founder article publish-md ./article.md --title "Launch Notes"
apitweet --app prod --profile founder article publish-md ./article.md --title "Launch Notes" --cover-image "https://example.com/cover.jpg" --visibility Public
apitweet --app prod --profile founder list create --name "AI Builders" --description "Interesting builders" --private
apitweet --app prod --profile founder user follow someuser
apitweet --app prod --profile founder user unfollow someuser
```

## FAQ

### What is apitweet-cli?

apitweet-cli is a Node.js command-line client for ApiTweet Twitter/X endpoints. It lets users call Twitter/X API workflows from the terminal, including user lookup, tweet search, global trending tweets, tweet actions, list actions, DM workflows, profile updates, and X Article publishing.

### Does apitweet-cli require an API key?

Yes. Read requests require a ApiTweet API key passed with `--api-key`, `APITWEET_KEY`, or a saved app config created with `apitweet auth apps add`.

### Can apitweet-cli perform write actions on X?

Yes. Write actions such as tweeting, liking, following, updating a profile, sending DMs, creating lists, and publishing X Articles require a saved profile or explicit cookie/auth token. Use `--dry-run` first to preview the request.

### Can apitweet-cli publish X Articles from Markdown?

Yes. Use `apitweet article publish-md <file.md> --title <title>`. The CLI creates a draft, optionally sets a cover image, sets the article title, uploads Markdown content, and publishes the article.

### Is apitweet-cli suitable for AI agents?

Yes. It exposes deterministic commands, JSON responses, dry-run previews, saved credential profiles, and skill/plugin metadata for Claude, Codex, and OpenClaw-style environments.

### Can apitweet-cli call endpoints that do not have convenience commands?

Yes. Use the raw path form, for example `apitweet /api/twitter/elonmusk/about` or `apitweet -X POST -d '["elonmusk"]' /api/twitter/users`.

## Limitations

- A ApiTweet API key is required for real API requests.
- Write actions require a cookie, `auth_token`, or saved profile.
- Saved app configs and profiles are stored as plain JSON on disk.
- Direct local file upload for tweet media is not included; tweet creation currently supports `--media-url`.
- The CLI is a terminal client, not a web dashboard or hosted API service.

## Project layout

```text
bin/apitweet.js         # thin executable entrypoint
src/index.js           # main boot flow
src/parser.js          # global option parsing
src/config.js          # config load/save and auth profile helpers
src/request.js         # HTTP execution and dry-run preview
src/commands.js        # command routing and endpoint mapping
src/help.js            # help text
src/constants.js       # defaults and option metadata
src/utils.js           # shared helpers
```

## Notes

- Global options such as `--app`, `--profile`, `--api-key`, and `--dry-run` should be placed before the command.
- All API paths are served under `/api/*`. Convenience commands add this prefix automatically; raw path requests may use `/twitter/...` or `/api/twitter/...`.
- For unsupported endpoints, use the generic `apitweet <path>` form.
- The CLI masks secrets in config output and dry-run previews.
- Direct local file upload for media is not included yet; the current CLI supports `--media-url` for tweet creation.


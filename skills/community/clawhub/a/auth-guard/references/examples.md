# Service Examples

## Example A: Moltbook Feed

- Protected endpoint: `GET /api/v1/feed?sort=new&limit=10`
- Public fallback: `GET /api/v1/posts?sort=new&limit=10`
- Env var: `MOLTBOOK_API_KEY`
- Credentials file: `~/.config/moltbook/credentials.json`

Probe:

```bash
bash skills/auth-guard/scripts/auth_check.sh \
  --service moltbook \
  --url 'https://www.moltbook.com/api/v1/feed?sort=new&limit=1' \
  --env-var MOLTBOOK_API_KEY \
  --cred-file "$HOME/.config/moltbook/credentials.json"
```

## Example B: GitHub API

- Protected endpoint: `GET https://api.github.com/user`
- Public fallback: `GET https://api.github.com/rate_limit`
- Env var: `GITHUB_TOKEN`
- Credentials file: `~/.config/gh/hosts.yml` (if available) or a local JSON shim used by your agent

Suggested probe endpoint:

```bash
bash skills/auth-guard/scripts/auth_check.sh \
  --service github \
  --url 'https://api.github.com/user' \
  --env-var GITHUB_TOKEN \
  --cred-file "$HOME/.config/github/credentials.json"
```

(If your GitHub token is managed only by `gh`, keep Auth Guard on env-first and define your own helper script for `gh auth token` integration.)

## Example C: Slack Web API

- Protected endpoint: `GET https://slack.com/api/auth.test`
- Env var: `SLACK_BOT_TOKEN`
- Credentials file: local service credentials JSON (optional)

Probe:

```bash
bash skills/auth-guard/scripts/auth_check.sh \
  --service slack \
  --url 'https://slack.com/api/auth.test' \
  --env-var SLACK_BOT_TOKEN \
  --cred-file "$HOME/.config/slack/credentials.json"
```

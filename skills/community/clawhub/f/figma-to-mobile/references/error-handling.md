# Error Handling

## FIGMA_TOKEN not set (script outputs `FIGMA_TOKEN_NOT_SET`)

Tell the user:

> I need a Figma Personal Access Token to fetch the design.
> ⚠️ **Do not paste it into this chat** — chat messages may be logged.
> Set it as an environment variable and restart.
> Get one at: Figma → avatar → Settings → Security → Personal Access Tokens
>
>   Windows: `setx FIGMA_TOKEN "figd_xxx"`
>   macOS/Linux: add `export FIGMA_TOKEN="figd_xxx"` to ~/.zshrc

## FIGMA_TOKEN invalid (API returns 403/401)

Tell the user the token may have expired or been revoked. Direct them to
regenerate from Figma Settings → Security → Personal Access Tokens.

## Invalid URL

Show valid URL example: `https://www.figma.com/design/<fileKey>/<name>?node-id=<id>`

## API error

Show the error message, suggest checking network/proxy.

## Node too large (>200 children)

Suggest selecting a smaller frame.

## Depth auto-increased

The script auto-retries with deeper depth if it detects truncated children.
Inform the user if this happens ("I needed to fetch deeper to get all details").

# User-onboarding script templates

Copy-paste-able prompts the agent can send to the user during key
onboarding. Adapt freely; they're written to be polite, brief, and
IM-friendly (short paragraphs, numbered steps).

---

## Path A — Indirect (IM / web chat / phone user)

### First-time key request

> To use Drillr I need an API key. From any browser (your phone is
> fine):
>
> 1. Open https://drillr.ai/developer/keys
> 2. Sign in — **Google sign-in is the quickest**; email/password
>    also works
> 3. Tap "Create API key" → name it (e.g. "my-agent") → copy the
>    `drl_...` string
> 4. Paste it back to me here. The key is shown only once.
>
> After I confirm it works, you can delete your message.

### Confirmation after storing (mask the key!)

> Stored `drl_xxxxxxxx_...e9f2`. You can safely delete your message
> now.

### When the pasted key fails validation (401)

> That key didn't work — I got a 401 from Drillr. It may have a
> typo, or it may have already been revoked. Could you go back to
> https://drillr.ai/developer/keys, create a fresh one, and paste
> it again?

### When the key is revoked mid-session

> Your Drillr API key was just revoked. To keep going, please
> create a new one at https://drillr.ai/developer/keys and paste
> it here.

---

## Path B — Direct (terminal co-located with user)

### Claude Code MCP setup

> 1. Create an API key at https://drillr.ai/developer/keys
> 2. Add this to `~/.claude.json` (or merge it into your existing
>    `mcpServers` object):
>
>    ```json
>    {
>      "mcpServers": {
>        "drillr": {
>          "type": "http",
>          "url": "https://gateway.drillr.ai/mcp",
>          "headers": {
>            "Authorization": "Bearer ${DRILLR_API_KEY}"
>          }
>        }
>      }
>    }
>    ```
>
> 3. Add `export DRILLR_API_KEY=drl_...` to your `~/.zshrc` or
>    `~/.bashrc` and restart your shell
> 4. Restart Claude Code. Run `/mcp` — you should see `drillr`
>    listed as connected.

### CLI setup

> ```
> npm install -g drillr-cli
> drillr auth set-key drl_...
> drillr watchlist list   # should succeed (empty is fine)
> ```

### REST / env-var setup

> ```
> export DRILLR_API_KEY=drl_...
> ```
>
> Then any HTTP call carries the header
> `Authorization: Bearer $DRILLR_API_KEY`.

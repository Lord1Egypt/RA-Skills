# Installation — Cloudways MCP Server

This skill targets the **official Cloudways (Remote) MCP** — a Cloudways-hosted MCP at `https://mcp.cloudways.com/mcp/` that you connect to directly, without self-hosting.

> **Source of truth:** [How to Use Cloudways MCP Server for AI-Based Server Management](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management). The endpoint, headers, and steps below are from that article; if Cloudways changes them, the article wins.

**Prerequisites**

- A valid Cloudways account with API access.
- A Cloudways **Access Token** (see Step 1).
- **Node.js v24.14.1+** (only for the Claude Desktop path, which uses the `mcp-remote` bridge). Claude Code connects over native HTTP and does not need it.

---

## Step 1 — Generate an Access Token

1. Log in to [platform.cloudways.com](https://platform.cloudways.com).
2. Open the **API** section (bottom-left of the platform — the same place the legacy API key lived).
3. Generate an **Access Token** (Access Token Details → Create Access Token). Note: only the **primary account owner** can create/manage API credentials — team-member accounts have no API Integration section. Give the token a name, an expiration period (1 day → never; shortest that works), and a **role**:
   - **READ** — look-ups only (status, config, monitoring). Recommended starting point for every new integration, and for monitoring-only connections.
   - **LIMITED** — only the endpoint groups you select.
   - **FULL ACCESS** — everything the account can do, including destructive actions. Only for connections that genuinely need to make changes.
4. Copy the token.

> Treat the token like a password — never commit it or print it in responses. Prefer one token **per integration** (per MCP connection), each with the minimum role it needs, so tokens can be revoked individually.

> **Legacy API key — deprecated.** The old flow (API key + `X-CW-Email`/`X-CW-Api-Key` headers) still works but the API key **stops working on October 15, 2026**. If you have an existing connection using the old headers, regenerate as an Access Token and update the connection before then. Until migrated, a legacy connection retains **unrestricted full-account access** — the RBAC roles apply only to Access Tokens. And note there is still **no per-tool permission control at the MCP layer** beyond the token's role: a FULL ACCESS token can call every tool.

**Required headers** (every request; header names are case-sensitive):

| Header | Value |
|--------|-------|
| `X-Access-Token` | your Cloudways Access Token |
| `X-Mcp-Host` | the client you connect from — official values: `claude-code`, `claude-desktop`, `cursor`, `Devin` (the client formerly called Windsurf — the article's own snippet sends the capitalised `Devin`, and header values are case-sensitive), `vs-code`, `gemini-cli`, `codex`, `codex-cli` |

---

## Step 2 — Connect Claude to the MCP

### Env var (zero-config — devices and cloud sessions)

The repo commits a `.mcp.json` whose `X-Access-Token` header reads
`${CLOUDWAYS_ACCESS_TOKEN:-}` — a placeholder, never a real token. Set that variable — in
your shell profile on a device, or in the claude.ai cloud environment's environment
variables for web/phone sessions — and the connection (named `cloudways-env`) authenticates
automatically. While the variable is unset the config still parses (the `:-` default), but
the connection can't authenticate and shows as unavailable in `/mcp` — expected until you
provide the token. The `cloudways-env` name is deliberate: project scope beats user scope on
name collisions, so it never shadows a `cloudways` or `cloudways-<client>` connection you
add with `claude mcp add -s user`. Never put a real token in `.mcp.json` itself; it is
tracked in git. The committed `.claude/settings.json` sets `enableAllProjectMcpServers`,
which is why the project-scope server activates without a prompt once the folder is trusted —
to opt out locally, set `"enableAllProjectMcpServers": false` in `.claude/settings.local.json`
(not committed). Cloud environments with a restricted network policy must allow
`mcp.cloudways.com`.

### Claude Code (native HTTP — recommended)

```bash
claude mcp add --transport http \
  --header 'X-Access-Token: ${CLOUDWAYS_ACCESS_TOKEN:-}' \
  --header "X-Mcp-Host: claude-code" \
  -s user \
  cloudways https://mcp.cloudways.com/mcp/
```

**Keep the single quotes, and do not put the token's value here.** See "Handling the
token safely" below: quoted this way, the shell never expands it, so neither this
command's arguments nor the stored config holds the secret — Claude Code expands it from
its own environment when it opens the connection.

`-s user` stores it at the user level so it persists across projects. Verify with `claude mcp list`; remove later with `claude mcp remove cloudways`.

### Claude Desktop (via `mcp-remote` bridge — needs Node v24+)

Claude Desktop does not natively support remote HTTP MCP servers, so it uses the `mcp-remote` Node bridge. Config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**First, install the bridge from the lockfile shipped with this skill.** `bridge/` (beside
this `references/` directory) carries a `package.json` and a `package-lock.json` covering **82
entries — 81 packages, every one with an integrity hash**, plus the root. `npm ci` installs
exactly what that lockfile names and resolves nothing of its own:

```bash
# && throughout: a failed delete or copy must not reach npm ci, which would
# then install from whatever lockfile is still there.
rm -rf ~/.cloudways-mcp-bridge &&                    # see the note below
  cp -R <skill-dir>/bridge ~/.cloudways-mcp-bridge &&
  cd ~/.cloudways-mcp-bridge && npm ci
```

```powershell
# Windows. -ErrorAction Stop on every step: PowerShell's default is Continue,
# which REPORTS a failed delete or copy and then carries on - so a locked file
# or a permissions error would leave the old tree in place and run npm ci
# against the stale lockfile, or run it in the caller's own directory. Only a
# missing directory is expected here, and Test-Path handles that case without
# silencing the others.
$bridge = "$HOME\.cloudways-mcp-bridge"
if (Test-Path -LiteralPath $bridge) {
  Remove-Item -LiteralPath $bridge -Recurse -Force -ErrorAction Stop
}
Copy-Item -LiteralPath <skill-dir>\bridge -Destination $bridge -Recurse -ErrorAction Stop
Set-Location -LiteralPath $bridge -ErrorAction Stop
npm ci
if ($LASTEXITCODE -ne 0) { throw "npm ci failed - the bridge is not installed" }
```

> **The delete is load-bearing when you re-run this after a lockfile update.** `cp -R src dst`
> copies *into* `dst` when `dst` already exists, giving you
> `~/.cloudways-mcp-bridge/bridge/package-lock.json` while the old lockfile stays where it was
> — so `npm ci` reinstalls the **stale** graph and reports success. That is the failure this
> whole section exists to prevent, arriving through the update path. The directory is ours and
> holds nothing but the copied files and `node_modules`, so removing it costs nothing.

**Then put the token in a header file, not in the config.** Claude Desktop performs no
`${VAR}` expansion, so a token written into `claude_desktop_config.json` is a literal secret in
a file people screenshot and paste; and a token passed as `--header` is in the process's
argument list, which every other user on the machine can read from `ps`. `mcp-remote`'s
`--header-file` avoids both — one `Name: value` per line, `#` starts a comment, whitespace
after the colon is trimmed:

**The file goes OUTSIDE the bridge directory** — `~/.cloudways-mcp-bridge` is deleted and
recreated by every re-install above, which would take the token with it and leave Claude Desktop
failing at startup until you typed it again:

```bash
umask 077                                   # applies to files this shell CREATES
mkdir -p ~/.config/cloudways-mcp
TMP=$(mktemp ~/.config/cloudways-mcp/headers.XXXXXX)   # X's at the END; BSD mktemp ignores them elsewhere
printf 'X-Mcp-Host: claude-desktop\n' > "$TMP"
printf 'X-Access-Token: '               >> "$TMP"
read -rs TOKEN && printf '%s\n' "$TOKEN" >> "$TMP" && unset TOKEN
chmod 600 "$TMP" && mv -f "$TMP" ~/.config/cloudways-mcp/headers.txt || rm -f "$TMP"
```

**Why a new file and a `mv` rather than `> headers.txt`:** `umask` applies only when a file is
**created**. Rotating a token by redirecting over an existing `headers.txt` writes the new secret
into whatever mode that file already had — group- or world-readable if it was ever created by
hand, restored from a backup, or copied from another machine. Writing a fresh 600 file and moving
it into place also means there is no moment when a half-written header file is the live one.

`read -rs` keeps the value off the terminal and out of shell history — paste at the silent
prompt and press Return. Check it afterwards with `ls -l ~/.config/cloudways-mcp/headers.txt`
(expect `-rw-------`) and `cut -d: -f1 ~/.config/cloudways-mcp/headers.txt` (prints the header
**names** only).

```powershell
# Windows equivalent, in the same order the POSIX recipe achieves with umask: a NEW file,
# restricted BEFORE the secret goes into it, then moved into place.
# Read-Host -AsSecureString keeps the value off the console; it still lands on disk in
# cleartext, which is what the ACL is for.
$dir  = "$HOME\.config\cloudways-mcp"
New-Item -ItemType Directory -Force -Path $dir -ErrorAction Stop | Out-Null
$file = Join-Path $dir 'headers.txt'
$tmp  = Join-Path $dir ('headers.' + [IO.Path]::GetRandomFileName())
$me   = [Security.Principal.WindowsIdentity]::GetCurrent().Name   # DOMAIN\user, always resolvable
$bstr = [IntPtr]::Zero

try {
  New-Item -ItemType File -Path $tmp -ErrorAction Stop | Out-Null

  # Break inheritance and grant only the current user - the NTFS equivalent of chmod 600 -
  # while the file is still EMPTY. icacls is a NATIVE command: PowerShell does not raise on
  # its exit status, so check it, and fail before any token exists on disk.
  icacls $tmp /inheritance:r /grant:r "${me}:(R,W)" > $null
  if ($LASTEXITCODE -ne 0) { throw "icacls failed (exit $LASTEXITCODE); no token was written" }

  $secure = Read-Host -AsSecureString 'Cloudways Access Token'
  # SecureStringToBSTR allocates an UNMANAGED cleartext copy. Keep the pointer so the finally
  # block can zero and free it - dropping it inline would leave the token in this process's
  # memory for as long as the session lives.
  $bstr  = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  Set-Content -LiteralPath $tmp -Encoding ascii -ErrorAction Stop -Value @(
    'X-Mcp-Host: claude-desktop'
    "X-Access-Token: $plain"
  )
  $plain = $null

  # The move carries this file's ACL over the old one, whatever the old one was.
  Move-Item -LiteralPath $tmp -Destination $file -Force -ErrorAction Stop
}
finally {
  # Zero and free the unmanaged copy on every path, including a throw between the two.
  if ($bstr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
  # Anything that threw above leaves no half-written token behind.
  if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
}
```

(The managed `$plain` string cannot be zeroed — .NET strings are immutable, so setting the
variable to `$null` only drops the reference and leaves the value for the garbage collector.
Run this in a shell you then close, not in a long-lived session you keep around.)

(Written from Microsoft's documented behaviour for `icacls` and `Read-Host`; like the rest of
the Windows path here, it has not been exercised on a Windows machine.)

Then point Claude Desktop at the installed executable and that file:

```json
{
  "mcpServers": {
    "cloudways": {
      "command": "/Users/<you>/.cloudways-mcp-bridge/node_modules/.bin/mcp-remote",
      "args": [
        "https://mcp.cloudways.com/mcp/",
        "--header-file", "/Users/<you>/.config/cloudways-mcp/headers.txt"
      ]
    }
  }
}
```

`/Users/<you>` above is a placeholder — the JSON needs **absolute** paths, and the commands
above wrote the files under `$HOME`. Print the two real values rather than typing them:

```bash
printf '%s\n' "$HOME/.cloudways-mcp-bridge/node_modules/.bin/mcp-remote" \
               "$HOME/.config/cloudways-mcp/headers.txt"
```

On Windows both paths change — the launcher is the `.cmd` shim, and the header file is under
the profile directory — and `$HOME` is **not** reliably `C:\Users\<you>`: a relocated, network
or non-C-drive profile puts both files somewhere else, and a config with a hard-coded C-drive
path then fails to find either. Let PowerShell build the block from the same `$HOME` the setup
used, which also escapes the backslashes for you:

```powershell
@{
  command = "$HOME\.cloudways-mcp-bridge\node_modules\.bin\mcp-remote.cmd"
  args    = @(
    'https://mcp.cloudways.com/mcp/',
    '--header-file',
    "$HOME\.config\cloudways-mcp\headers.txt"
  )
} | ConvertTo-Json
```

Paste the result as the `"cloudways"` entry under `"mcpServers"`. No hard-coded
`C:\Users\<you>` appears here on purpose: on a relocated, network or non-C-drive profile that
path is simply wrong, and an example carrying it is the thing people copy.


A header file it cannot read is a **fatal** error, not a warning, so a wrong path fails at
startup instead of connecting unauthenticated. Verified against `mcp-remote@0.14.0` installed
from the shipped lockfile: it logs `Loaded 2 header(s)` and `Using custom headers:
X-Mcp-Host, X-Access-Token` — the names, never the value.

(The `.cmd` shim is what Windows needs — the extensionless file beside it is POSIX-only. That
path is npm's documented layout and has not been exercised on a Windows machine.)

> **There is deliberately no `npx` alternative here any more.** Earlier versions offered one as
> a collapsed fallback. `npx mcp-remote@0.14.0` pins the named package and **nothing underneath
> it**: the ~80 transitive dependencies are resolved fresh whenever the npx cache is empty, so a
> version published inside one of their ranges between now and your next launch executes in the
> process holding your Access Token. Anyone who can run `npx` can run the `npm ci` above — it is
> one command more against a lockfile that ships with this skill — so the fallback bought
> convenience that was never worth its exposure. If `npm ci` fails, fix that (registry, proxy,
> Node version) rather than reaching for a path that resolves at launch.

> **Pin `mcp-remote`.** A launcher that resolves at run time executes whatever the registry
> serves at that moment, into a process that reads your Access Token from `headers.txt` — so a
> compromised release, maintainer account or transitive dependency would receive it. The
> version is pinned deliberately, in `bridge/package.json` and the lockfile beside it; bump it
> after reading the upstream release notes, and record the new digest here in the same commit.
>
> ```
> mcp-remote@0.14.0
> sha512-QBYGz02kc2AhhM6RNDzNyoA/FlzwJCNYPFF+o3opSvwfo5lnp8mcVIj/Zqw92dPuoafyLBKQZkpaEJdzlB/png==
> ```
>
> To check what the registry served you, compute the digest from the bytes — **do not compare
> against the line `npm pack` prints**, which elides the middle
> (`sha512-QBYGz02kc2Ahh[...]kpaEJdzlB/png==`), so a comparison against it only ever checks a
> prefix and a suffix:
>
> ```bash
> npm pack mcp-remote@0.14.0
> printf 'sha512-%s\n' "$(openssl dgst -sha512 -binary mcp-remote-0.14.0.tgz | openssl base64 -A)"
> ```
>
> (`npm pack --json` also emits the full value, if you would rather read npm's own figure than
> compute one.) A digest **recorded here, out of band** is what makes this worth running: npm
> forbids republishing a version with different content, so it catches a registry that later
> serves different bytes for 0.14.0.
>
> **What the pin does NOT cover: everything underneath it.** `mcp-remote@0.14.0` fixes one
> package, and the digest above covers one tarball; its ~80 dependencies would be resolved
> fresh by any launcher that resolves at run time, so a newly published version inside one of
> their ranges would run with your Access Token even though the digest still matches. That is
> what the shipped lockfile and `npm ci` exist to prevent, and why no `npx` recipe remains.
>
> **One dependency is pinned past its parent's range.** `express@4.22.2` — the newest 4.x, and
> what `mcp-remote` asks for — requires `qs@~6.15.1`, and every `qs` below 6.16.0 carries two
> advisories (an array-limit bypass and a DoS through an attacker-controlled `isBuffer`). There
> is no express release that widens the range, so `bridge/package.json` carries
> `"overrides": { "qs": "6.16.0" }`. This is not a guess about compatibility: `body-parser`, in
> this same tree and from the same maintainers, already requires `~6.16.0`, so the override
> collapses two copies of `qs` into the patched one. Regenerating the lockfile moved that single
> version and nothing else (82 entries → 81, `npm audit`: **0 vulnerabilities**), and `npm ci`
> from it still produces a working `node_modules/.bin/mcp-remote`.
>
> **`npm ci` against the shipped lockfile has to be the first command that touches the
> registry.** Generating your own lockfile with `npm install` resolves the graph at that moment
> and then freezes whatever it found — so a first install during a compromise locks the bad
> version in, and the `npm ci` after it faithfully reproduces it. The point of shipping
> `bridge/package-lock.json` is that the resolution happened once, here, at a known date.
>
> To be exact about what that buys, because "vetted" does a lot of work: the graph is **pinned
> and reproducible**, with integrity hashes for every package. It is not a claim that 81
> packages' source has been read. Bumping `mcp-remote` means regenerating the lockfile in the
> same commit.

> **The secret is now in `~/.config/cloudways-mcp/headers.txt`, and it is still a secret at
> rest.** Keep it at mode 600, back it up nowhere, and give the token the **smallest role that
> works** (READ for monitoring-only). It lives outside `~/.cloudways-mcp-bridge` on purpose:
> that directory is deleted and recreated on every re-install, so a token kept inside it would
> vanish on the next lockfile bump and take the connection down with it. `claude_desktop_config.json` no longer contains it — that file can be
> pasted into an issue or a screen share without leaking anything — but the header file can't.
> The `${VAR}` expansion used in the Claude Code section above is Claude Code's own; Claude
> Desktop performs none, which is why the file exists. (`mcp-remote` does expand `${VAR}` inside
> a header **value** from its own environment, if you have somewhere better than a file to keep
> it — a launcher that exports it from a keychain, say.)

> **Header-file format:** `Name: value`, one per line; `#` starts a comment; whitespace after
> the colon is trimmed, and CRLF line endings are handled. Header names are case-sensitive.
> After saving either file, **fully quit** Claude Desktop (Cmd-Q / tray → Quit — closing the
> window is not enough) and reopen.

> Keep real credentials out of version control. For Claude Code, put the token in the `CLOUDWAYS_ACCESS_TOKEN` env var (the committed `.mcp.json` reads it, and so does the user-scope form above) — never edit a real token into `.mcp.json`, which is a **tracked** file. See `.mcp.json.example` in the repo root for the per-account shape. Header names are case-sensitive.

### Other clients (Cursor, Devin, VS Code Copilot, Gemini CLI, Codex)

Same endpoint and headers everywhere; only the config-file shape and the `X-Mcp-Host` value differ per client. The [official article](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management) has the full snippet for each — but three of them use a **non-obvious key**, and the article warns that a wrong variant **fails silently**:

| Client | Config file | URL key | Headers key | `X-Mcp-Host` |
|--------|-------------|---------|-------------|--------------|
| Cursor | `~/.cursor/mcp.json` | `url` | `headers` | `cursor` |
| Devin (ex-Windsurf) | `~/.codeium/devin/mcp_config.json` | **`serverUrl`** | `headers` | `Devin` |
| VS Code (Copilot) | `~/Library/Application Support/Code/User/mcp.json` (macOS) / `%APPDATA%\Code\User\mcp.json` | `url`, and the file uses **`"servers"` (not `"mcpServers"`)** plus a required **`"type": "http"`** | `headers` | `vs-code` |
| Gemini CLI | `~/.gemini/settings.json` | **`httpUrl`** — `url` there attempts an SSE connection instead and fails | `headers` | `gemini-cli` |
| Codex / Codex CLI | `~/.codex/config.toml` | `url` | **`[mcp_servers.cloudways.http_headers]`** (a separate TOML table) | `codex` / `codex-cli` |

**Cursor connects over native HTTP** — no Node and no `mcp-remote`; the bridge is only a fallback for proxy/connection problems (and then it needs Node v24+, as Claude Desktop does). The article also offers a one-click "Install in Cursor" button that prompts for the credentials.

---

## Handling the token safely

An Access Token carries whatever role it was issued with — up to FULL ACCESS, which is
everything the Cloudways account can do, including destructive server and app actions and
billing. Keep the value in **one** place, the environment Claude Code starts with, and put a
*placeholder* everywhere else.

**Never pass the value to `claude mcp add`.** Written as `"X-Access-Token: $TOKEN"`, the
shell expands it before launching anything, so the live token is in that process's argument
list — readable through `ps` or `/proc/<pid>/cmdline` by any other user on the machine while
the command runs — and `claude mcp add` then stores the **resolved value** in
`~/.claude.json` in plaintext, where it stays until you remove the connection. Single-quoted
as `'X-Access-Token: ${CLOUDWAYS_ACCESS_TOKEN:-}'`, neither the argument list nor the stored
config carries the secret. Claude Code expands `${VAR}` in headers for local- and
user-scoped entries in `~/.claude.json`, not only in a project `.mcp.json`; an unset
reference produces a `Missing environment variables` warning in `claude mcp list`.

**Where the value lives.** It must be in the environment Claude Code itself starts with:

```bash
printf 'Cloudways Access Token: '
read -rs CLOUDWAYS_ACCESS_TOKEN; echo
export CLOUDWAYS_ACCESS_TOKEN
```

`read -rs` does not echo the token and never writes it to `~/.zsh_history` /
`~/.bash_history`, but it lasts only for that shell — start Claude Code **from it**. For a
persistent setup, put the export in your shell profile at mode 600, or better, read it from
a keychain rather than storing it inline:

```bash
export CLOUDWAYS_ACCESS_TOKEN="$(security find-generic-password -s cloudways-api -w)"   # macOS
```

In claude.ai cloud sessions the equivalent is the environment's own environment variables.

**If a token may have been exposed** — pasted into a chat, committed, left in a history file
or an old `~/.claude.json` entry — **revoke it at platform.cloudways.com → API** and issue a
new one with the smallest role that works. To check whether an old connection left a literal
behind, **parse** the config rather than grepping it (JSON may put a value on the line after
its key), and report names rather than values:

```bash
node -e '
const fs = require("fs"), p = require("os").homedir() + "/.claude.json";
let c; try { c = JSON.parse(fs.readFileSync(p, "utf8")); }
catch (e) { console.error("could not read " + p); process.exit(1); }
const all = [...Object.entries(c.mcpServers || {}),
             ...Object.values(c.projects || {}).flatMap(x => Object.entries(x.mcpServers || {}))];
const literal = v => { const re = /\$\{[A-Za-z_][A-Za-z0-9_]*(?::-([^}]*))?\}/g;
                       let n = v.replace(re, "").length;
                       for (const m of v.matchAll(re)) n += (m[1] || "").length;
                       return n; };
const hits = all.filter(([, s]) => { const v = (s.headers || {})["X-Access-Token"];
                                     return typeof v === "string" && literal(v) > 0; })
                .map(([n]) => n);
console.log(hits.length
  ? "Literal token stored in: " + hits.join(", ") + " — revoke it and re-add with the placeholder form."
  : "No literal token in ~/.claude.json.");
'
```

It counts literal material inside `:-` defaults as well as outside the placeholders — a
token hides just as well in `${CLOUDWAYS_ACCESS_TOKEN:-cw_live}`, which is still plaintext
in the file and is still what gets sent whenever the variable is unset.

---

## Multi-account configuration — multiple Cloudways accounts

Each Cloudways account is a **separate** MCP connection with its own Access Token, so it appears under its own prefix (`mcp__cloudways-clientA__*`). Give each a descriptive, client-based name — that name becomes the tool prefix. Same endpoint for all; only the `X-Access-Token` differs.

Give each account its **own variable name** and reference it as a placeholder, so no
token reaches a command line or a config file:

```bash
# one `claude mcp add` per account, each reading its own variable:
claude mcp add --transport http \
  --header 'X-Access-Token: ${CLOUDWAYS_TOKEN_CLIENTA:-}' \
  --header "X-Mcp-Host: claude-code" \
  -s user cloudways-clientA https://mcp.cloudways.com/mcp/

claude mcp add --transport http \
  --header 'X-Access-Token: ${CLOUDWAYS_TOKEN_CLIENTB:-}' \
  --header "X-Mcp-Host: claude-code" \
  -s user cloudways-clientB https://mcp.cloudways.com/mcp/
```

Export `CLOUDWAYS_TOKEN_CLIENTA` / `CLOUDWAYS_TOKEN_CLIENTB` in the environment Claude
Code starts with. The header sent is always `X-Access-Token`; only the source differs per
connection, which is what keeps the accounts separated.

(See `.mcp.json.example` for the JSON form across multiple accounts.)

### Safety rules for multi-account (mandatory)

- **Consistent names:** uniform `cloudways-<client>` prefix so Claude (and you) immediately recognize which account each tool belongs to.
- **Separate secrets:** don't keep all the tokens in one place. Prefer a secrets manager (a vault project per client) over plain config files.
- **Don't mix:** never reuse one token across accounts, and never take a server/app ID from one account against another's connection.
- **Scope by role:** generate each connection's token with the **minimum role** it needs — READ for monitoring/audit connections, LIMITED for specific workflows, FULL ACCESS only where changes are genuinely required. Set an expiration and rotate; revoke a client's token the moment the engagement ends.
- **Runtime:** account identification, cross-account search, and per-account write-confirmations are documented in `SKILL.md` → **Multi-account**.

---

## Step 3 — Verify the connection

In Claude, ask: **"Show me all my Cloudways servers"** → calls `server_list` and returns your servers (name, status, provider, region, IP). That round-trip confirms the endpoint + credentials.

(There is no `ping` / `customer_info` tool on the official MCP — `server_list` is the liveness + auth check. Identify which account you're on by the connection prefix.)

| Symptom | Meaning | Fix |
|---------|---------|-----|
| Connection failed / red indicator | wrong URL | endpoint must be exactly `https://mcp.cloudways.com/mcp/` (trailing slash) |
| `401 Unauthorized` | bad credentials | re-check the Access Token (case-sensitive header); it may be expired or revoked — regenerate in the platform |
| Write tool fails but reads work | token role too narrow | the connection uses a READ (or too-narrow LIMITED) token; use a token whose role covers the operation |
| No `mcp__cloudways*__*` tools | not connected / stale cache | restart the client (see "Tools not appearing" below) |
| Timeout | transient network | retry after a moment |
| `mcp-remote not found` (Desktop) | bridge not installed, or Node missing | install Node.js v24+, then re-run the `npm ci` install above; the config points at `~/.cloudways-mcp-bridge/node_modules/.bin/mcp-remote`, not at a PATH lookup |

To test credentials directly against the public Cloudways API, independent of the MCP layer (useful to isolate "bad credentials" from "MCP connection problem"):

```bash
# Access Token (current):
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" "https://api.cloudways.com/api/v2/server"

# Legacy API key (works until the EOL, 2026-10-15):
curl -X POST "https://api.cloudways.com/api/v1/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=YOUR_EMAIL&api_key=YOUR_API_KEY"
```

API reference: <https://developers.cloudways.com/> — note the tools article's `oauth_access_token_generate` tool does **not** exist on the live MCP (verified 2026-07-20); mint direct-API tokens through the Cloudways platform instead.

---

## Tools not appearing / after an update

MCP clients **cache the tool list** on first connect. If new tools don't show up, or the agent says a tool doesn't exist:

- **Quickest:** in the client's MCP server settings, toggle `cloudways` off then on.
- **If no toggle:** **fully quit** the client (Cmd-Q on macOS / File → Exit / tray → Quit — closing the window is not enough) and reopen.

Then re-test with "Show me all my Cloudways projects" (`project_list`).

> Note the intentional design: even when correctly connected, the client sees only **65 tools** (62 direct + 3 meta-tools). The 62 direct tools are **members of the toolsets**, not a separate tier — so of the 244 total (241 toolset members + 3 meta-tools, live-verified 2026-07-20) the hidden remainder is **179**, discovered on demand via `list_available_toolsets` / `get_toolset_tools` / `execute_tool`. Their absence from the visible list is **not** a caching problem.

---

## Notes

- This skill does **not** cover self-hosting an MCP server — the official hosted MCP is the supported path.
- Tool names throughout this skill match the official articles' catalog (see `tools-catalog.md`). The **live** `mcp__cloudways*__*` tools remain the source of truth if Cloudways adds or renames any.

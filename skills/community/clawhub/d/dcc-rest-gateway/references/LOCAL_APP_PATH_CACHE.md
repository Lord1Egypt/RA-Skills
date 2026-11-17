# Local application path cache

The default `dcc-mcp` route remembers only paths the user explicitly provides.
It stores a product id, normalized absolute path, timestamps, and whether the
path was supplied by the user. It never stores credentials, arguments, or
automatically starts a process.

The cache file is `%LOCALAPPDATA%\\dcc-mcp\\app-paths.json` on Windows and
`$XDG_STATE_HOME/dcc-mcp/app-paths.json` (or `~/.local/state/...`) elsewhere.
Set `DCC_MCP_APP_PATH_CACHE` to use another location.

```bash
python scripts/app_path_cache.py set --product obs --path "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"
python scripts/app_path_cache.py prompt --product obs --name "OBS Studio" \
  --install-available --host-install-url https://obsproject.com/download
python scripts/app_path_cache.py get --product obs
```

When a cached path exists, the agent tells the user the path and asks for
explicit confirmation before starting. When it is stale or absent, the agent
asks for a new absolute path and asks whether the user wants the host application
installed. When `PRODUCTS.json` provides a `host_install` HTTPS source, pass it
with `--host-install-url` so the prompt points to the official installation page.
The prompt may also show the separate adapter hint:
`dcc-mcp-cli install --dcc-type <id> --dcc-path "<path>"`.
That command installs the DCC-MCP adapter, not necessarily the host application.
Downloads, installation, and launch still require explicit user confirmation.

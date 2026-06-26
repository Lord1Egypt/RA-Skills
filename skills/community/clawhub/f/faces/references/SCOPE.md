# Instruction Scope

Runtime instructions operate exclusively on the `faces` CLI, which sends HTTPS requests to the Faces Platform API (`api.faces.sh` by default, or `FACES_BASE_URL` if set). No local files are read or written except `~/.faces/config.json`, which stores credentials the user explicitly provides.

**Install:** the CLI is installed via `npm install -g faces-cli` from the public npm registry (`npmjs.com/package/faces-cli`), published by `sybileak`. The source is the `faces-cli-js` repository under the Headwaters AI organization.

**Credentials:** the skill uses a JWT (`FACES_TOKEN`) or API key (`FACES_API_KEY`) to authenticate requests — proportionate to a REST API client. Credentials are only read from environment variables or `~/.faces/config.json`; they are never written anywhere other than that config file when the user explicitly runs `faces auth:login` or `faces config:set`. The skill may prompt for email and password during `auth:login`; these are sent directly to the Faces API and not stored in plaintext (only the resulting JWT is saved). Scoped API keys with budget limits and expiry are recommended over long-lived account credentials.

**Scope boundaries:** instructions stay within the Faces Platform domain (auth, face management, inference, compile, billing, API keys). No system commands, file operations, or network requests outside of `faces *` CLI calls are issued. The `jq` utility is used solely for extracting fields from JSON output in example pipelines.

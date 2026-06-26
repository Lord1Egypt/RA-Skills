# OpenClaw Bridge

Stdio MCP server that authenticates with [Dazzle](https://dazzle.ai) over OAuth2 and
forwards calls from your local agent to Dazzle's hosted MCP endpoint.

## Signing in

The first time your agent queries Dazzle you'll receive a sign-in URL and a short code.
Open the URL, enter the code, approve. Your tokens are kept in your OS keyring;
subsequent sessions are silent.

## License

[MIT](LICENSE)

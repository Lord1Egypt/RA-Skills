# Vapi and ElevenLabs Agents (MCP tool server)

Both platforms can load tools from a Model Context Protocol server. Add this server URL:

```
https://linepref.byronwebstudio.com.au/mcp
```

No key is needed for the first 1,000 checks each month. To use a key, add the header
`Authorization: Bearer lp_...` in the server's settings.

Tools provided:

| Tool | When the agent should call it |
|---|---|
| `check_before_call` | Before placing a call to a business |
| `check_many` | Before dialling a list of businesses (up to 100) |
| `report_call_outcome` | After every call ends |
| `record_opt_out` | When the called party presses 9 or 8, or asks to stop calls |

Add to the system prompt:

> Before any phone call, call `check_before_call`. If advice is `use_link`, use the link and do not call. If
> advice is `do_not_call`, do not call. Open every call with: "This is an automated assistant. To stop calls
> from us, press 9 at any time. To stop automated assistant calls from all participating callers, press 8."
> If the person presses 9 or asks to stop, call `record_opt_out` with scope `caller`; if they press 8, use
> scope `all`. After every call, call `report_call_outcome`.

For outbound campaigns it is better to run the check in your own code before you start each call (one HTTP
request), so a call is never placed to a number that returns `use_link` or `do_not_call`.

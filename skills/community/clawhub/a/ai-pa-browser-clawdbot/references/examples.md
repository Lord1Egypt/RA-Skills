# Agent Browser — Examples

## Form Submission
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i --json
# Snapshot shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i --json
```

## Login with Saved State
```bash
# Login once, save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i --json
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser state save auth.json

# Later sessions: skip login
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Search and Extract
```bash
agent-browser open https://www.google.com
agent-browser snapshot -i --json
agent-browser fill @e1 "AI agents"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i --json
agent-browser get text @e3 --json
agent-browser get attr @e4 "href" --json
```

## Multi-Session (Admin + User)
```bash
agent-browser --session admin open app.com
agent-browser --session admin state load admin-auth.json
agent-browser --session admin snapshot -i --json

agent-browser --session user open app.com
agent-browser --session user state load user-auth.json
agent-browser --session user snapshot -i --json
```

## Record Demo Video
```bash
# Explore first (don't record yet)
agent-browser open https://app.com
agent-browser state load auth.json
agent-browser open https://app.com/dashboard

# Start recording, perform demo
agent-browser record start ./demo.webm
agent-browser click @e1
agent-browser fill @e2 "demo input"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser record stop
```

## Snapshot Output Format
```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

## Best Practices
1. Always use `-i` flag — focus on interactive elements
2. Always use `--json` — easier to parse
3. Wait for stability — `agent-browser wait --load networkidle`
4. Save auth state — skip login with `state save/load`
5. Use sessions — isolate different browser contexts
6. Use `--headed` for debugging — see what's happening
7. Re-snapshot after every navigation — refs change on page load

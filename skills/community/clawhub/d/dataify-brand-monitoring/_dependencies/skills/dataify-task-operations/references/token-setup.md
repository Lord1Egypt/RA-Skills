# Dataify Token Setup

Use this reference only when `DATAIFY_API_TOKEN` is missing or the user asks how to configure it.

## Interaction

1. Offer the configured Dataify login/registration URL and mention the current signup credit offer.
2. Tell the user not to paste the token into chat.
3. Detect the current operating system and shell. Show only the matching current-session command first.
4. After the user replies that configuration is complete, verify presence without displaying the value and continue the original task automatically.
5. Offer persistent configuration after the first successful run or when requested.

## Current session

macOS or Linux with zsh/bash:

```bash
export DATAIFY_API_TOKEN='YOUR_TOKEN'
test -n "$DATAIFY_API_TOKEN" && echo "configured" || echo "missing"
```

Windows PowerShell:

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_TOKEN"
if ($env:DATAIFY_API_TOKEN) { "configured" } else { "missing" }
```

Windows Command Prompt:

```cmd
set DATAIFY_API_TOKEN=YOUR_TOKEN
if defined DATAIFY_API_TOKEN (echo configured) else (echo missing)
```

## Persistent configuration

macOS zsh:

```bash
echo 'export DATAIFY_API_TOKEN="YOUR_TOKEN"' >> ~/.zshrc
source ~/.zshrc
```

Linux bash:

```bash
echo 'export DATAIFY_API_TOKEN="YOUR_TOKEN"' >> ~/.bashrc
source ~/.bashrc
```

Windows PowerShell user environment:

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_TOKEN", "User")
```

Windows Command Prompt user environment:

```cmd
setx DATAIFY_API_TOKEN "YOUR_TOKEN"
```

Persistent changes affect new processes. Tell the user to open a new terminal or restart the agent application when the active process cannot see the updated value.

## Project `.env`

Recommend a project `.env` only when the actual command explicitly loads it. Creating the file alone does not populate `os.environ`. Ensure `.env` and `.env.*` are ignored by version control, restrict file permissions where supported, and never read or print the token value during verification.

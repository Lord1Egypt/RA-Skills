---
name: edith
description: Set up Edith smart glasses as an OpenClaw channel. Run this when the user wants to connect their smart glasses to OpenClaw, mentions "Edith glasses", or provides a link code for glasses setup.
user-invocable: true
---

# Setup Edith Glasses

You are helping the user connect their Edith smart glasses to OpenClaw.

## What is Edith Glasses?

Edith is an AI assistant that runs on smart glasses (Mentra, etc). It connects to OpenClaw as a channel plugin, so the user can talk to their OpenClaw agent hands-free through their glasses.

## Setup Flow

### Step 1: Check if the plugin is already installed

Run:
```bash
ls ~/.openclaw/extensions/openclaw-edith-glasses/package.json 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```

If NOT_INSTALLED, install it:
```bash
openclaw plugins install openclaw-edith-glasses
```

### Step 2: Check if the channel is already configured

Run:
```bash
grep -c "edith-glasses" ~/.openclaw/openclaw.json 2>/dev/null || echo "0"
```

If the count is 0 or the channel section doesn't exist, ask the user for their **link code** (an 8-character code shown in the Edith app on their glasses).

If they haven't provided it yet, tell them:
> Open the Edith app on your glasses. Your link code is displayed on the settings page. Tell me the code and I'll finish the setup.

### Step 3: Add the channel with the link code

Once you have the link code, run:
```bash
openclaw channels add --channel edith-glasses --token LINK_CODE
```

Replace `LINK_CODE` with the actual code the user provided.

### Step 4: Restart the gateway

```bash
openclaw gateway restart
```

### Step 5: Confirm

Tell the user:
> Edith glasses are connected! Put on your glasses and say "Hey Edith" followed by your question. The connection should be live within a few seconds.

## If the user just provides a link code

If the user messages you something like "Uts35SUD" or "my link code is ABC123" or "here's my glasses code: XYZ", and the plugin is already installed, skip straight to Step 3 with that code.

## Troubleshooting

If `openclaw channels add` fails because the channel already exists, update the config directly:
```bash
python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
cfg.setdefault('channels', {})['edith-glasses'] = {
    'enabled': True,
    'appUrl': 'https://edith-production-a63c.up.railway.app',
    'linkCode': 'LINK_CODE'
}
with open('$HOME/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)
print('Done')
"
```

Replace `LINK_CODE` with the user's actual code.

If the gateway won't restart due to config errors, clean up first:
```bash
python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
for k in list(cfg.get('channels', {})):
    if 'edith' in k:
        del cfg['channels'][k]
for key in ['entries', 'installs']:
    if key in cfg.get('plugins', {}):
        for k in list(cfg['plugins'][key]):
            if 'edith' in k:
                del cfg['plugins'][key][k]
with open('$HOME/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)
print('Cleaned')
"
```
Then start from Step 1 again.

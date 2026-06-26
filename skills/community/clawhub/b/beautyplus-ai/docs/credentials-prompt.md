# Credentials prompt (when `preflight` reports `missing`)

When `python3 {baseDir}/scripts/beautyplus_ai.py preflight` outputs **`missing`**,
do **not** continue to Step 1. Tell the user how to set `BP_AK` / `BP_SK`,
using a channel-appropriate format.

The plain-text version is the safe default. Only use the Feishu interactive
card when the host actually exposes a Feishu account.

## Plain-text (Telegram / Discord / generic `message` tool)

Send via the host's `message` tool:

```
🖼️ BeautyPlus — credentials required

1. Get Access Key and Secret Key (apply here if needed):
   https://beautyplus.com/developers

2. Set BP_AK and BP_SK in scripts/.env (see scripts/.env.example), then run:
   source scripts/.env

If keys are issued by your organization, ask your administrator.
```

## Feishu interactive card

Send through the Feishu Open API (do **not** use the generic `message` tool —
the card payload only renders correctly via the Feishu IM endpoint).

The example below reads the Feishu app credentials from the OpenClaw config
(`channels.feishu.accounts.default`). The config path is host-dependent; the
default OpenClaw path is `~/.openclaw/openclaw.json`. Adjust if your host
mounts the config elsewhere.

```python
import json, os, urllib.request

cfg_path = os.path.expanduser(
    os.environ.get("OPENCLAW_CONFIG", "~/.openclaw/openclaw.json")
)
cfg = json.loads(open(cfg_path).read())
feishu = cfg["channels"]["feishu"]["accounts"]["default"]

token_resp = urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=json.dumps({
        "app_id": feishu["appId"],
        "app_secret": feishu["appSecret"],
    }).encode(),
    headers={"Content-Type": "application/json"},
))
token = json.loads(token_resp.read())["tenant_access_token"]

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "🖼️ BeautyPlus — credentials required",
        },
        "template": "blue",
    },
    "elements": [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "1. Apply for **Access Key** and **Secret Key** at "
                    "[BeautyPlus Developers](https://beautyplus.com/developers).\n"
                    "2. Set **BP_AK** and **BP_SK** in `scripts/.env` "
                    "(see `scripts/.env.example`), then reload env:\n"
                    "```\nsource scripts/.env\n```\n"
                    "If keys are issued by your organization, ask your administrator."
                ),
            },
        }
    ],
}

urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    data=json.dumps({
        "receive_id": "<USER_OPEN_ID>",
        "msg_type": "interactive",
        "content": json.dumps(card),
    }).encode(),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    },
))
```

Replace `<USER_OPEN_ID>` with the Feishu open id of the requesting user
(`sender_id` without the `user:` prefix).

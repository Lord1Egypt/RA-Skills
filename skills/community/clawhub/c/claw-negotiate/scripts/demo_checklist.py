#!/usr/bin/env python3
"""Print the APOA SAFE negotiation demo checklist."""
from __future__ import annotations

import argparse


QUICK = """# APOA SAFE Demo Quick Script

Founder bot DM:

```text
My profile
```

If needed:

```text
Update my profile - I'm Juan Figuera, CEO of Avocado
```

Start:

```text
Live negotiation for Series Seed SAFE with Nora Vassileva at SD Capital.

Cap: $20M-$30M post.
Check: $500k-$1M.
Pro rata: required.
Discount: 0%
```

Reply after confirm:

```text
GO
```

Investor bot DM:

```text
My profile
```

If needed:

```text
Update my profile - I'm Nora Vassileva, partner at SD Capital
```

Join:

```text
Joining INV-XXXXX via @AgenticPOA_bot, I am Nora Vassileva at SD Capital.

Cap: $10M-$24M post.
Check: $250k-$600k.
Pro rata: required.
Discount: 0%
```

Reply after confirm:

```text
GO
```

Group chat:

```text
/bind INV-XXXXX
```

Watch for:

- Round 0 in group
- alternating founder/investor cards, no duplicates
- private APOA blocked card when a counterparty offer is outside local bounds
- private signing links in DMs only
- executed PDF in group after both signatures
"""


FULL = """# APOA SAFE Negotiation Demo Checklist

## Preflight

- Founder and investor OpenClaws are paired with Telegram.
- `python3 scripts/smoke_install.py --skill-dir negotiate_safe --skip-openclaw` passes locally.
- Each side has a saved profile.
- The demo should show APOA enforcing private bounds, not just two agents chatting.

## Founder Starts

Founder bot DM:

```text
Live negotiation for Series Seed SAFE with Nora Vassileva at SD Capital.

Cap: $20M-$30M post.
Check: $500k-$1M.
Pro rata: required.
Discount: 0%
```

Review the authorization card. Point out that these are private user bounds. Reply:

```text
GO
```

## Investor Joins

Investor bot DM:

```text
Joining INV-XXXXX via @AgenticPOA_bot, I am Nora Vassileva at SD Capital.

Cap: $10M-$24M post.
Check: $250k-$600k.
Pro rata: required.
Discount: 0%
```

Review the investor authorization card and reply:

```text
GO
```

## Group Bind

Create the negotiation room and paste:

```text
/bind INV-XXXXX
```

Confirm the group receives Round 0 and then alternating founder/investor offers without duplicates.

## APOA Proof Points

- Each OpenClaw negotiates creatively inside its user's authority.
- Private bounds are not disclosed in the group chat.
- If a counterparty proposes an out-of-bounds term, the user sees an APOA blocked card privately.
- Private signing links are sent by DM, and each human reviews before signing.
- The executed SAFE includes signatures and an sshsign audit trail.

## Recording Reminders

- Say that the demo is open source.
- Keep the story centered on: "I asked my OpenClaw to negotiate my SAFE for me."
- Highlight bounded delegation, human approval, and auditability.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Print only the pasteable live-demo script.",
    )
    args = parser.parse_args()
    if args.quick:
        print(QUICK, end="" if QUICK.endswith("\n") else "\n")
    else:
        print(FULL, end="" if FULL.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

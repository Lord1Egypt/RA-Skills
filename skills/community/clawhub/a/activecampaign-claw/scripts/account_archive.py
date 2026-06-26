#!/usr/bin/env python3
"""
account_archive.py — Point-in-time local copy of your AC account taxonomy for
diff / audit / pre-change review use.

Bundles the structural definitions in your account (lists, tags, fields,
pipelines, stages, automations, messages, forms, segments, webhooks) into
a single local JSON file. Optionally widens to include contacts and deals.

The output is a local file on your machine. Nothing is transmitted anywhere.

Common uses:
  - Diff "before" vs "after" a configuration change
    (pair with `scripts/schema_diff.py`)
  - Review your taxonomy in a text editor
  - Provide an auditable record of what your account looked like at a moment

Confirmation: when running with `--scope all` (the most data-dense option)
the script requires `--confirm`. Lighter scopes (`taxonomy`, `contacts`,
`deals`) run without confirmation.

Usage:
  python3 account_archive.py --scope taxonomy
  python3 account_archive.py --scope all --confirm --output snap.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, emit_files


def _try_paginate(client, path, key, **kwargs):
    try:
        return client.paginate(path, key, **kwargs)
    except ACClientError as e:
        if e.status_code in (403, 404):
            return []
        raise


def fetch(client: ACClient, scope: str) -> dict:
    out = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "taxonomy": {
            "lists": _try_paginate(client, "lists", "lists", max_items=2000),
            "tags": _try_paginate(client, "tags", "tags", max_items=10000),
            "fields": _try_paginate(client, "fields", "fields", max_items=2000),
            "pipelines": _try_paginate(client, "dealGroups", "dealGroups", max_items=200),
            "stages": _try_paginate(client, "dealStages", "dealStages", max_items=500),
            "automations": _try_paginate(client, "automations", "automations", max_items=2000),
            "messages": _try_paginate(client, "messages", "messages", max_items=5000),
            "forms": _try_paginate(client, "forms", "forms", max_items=500),
            "segments": _try_paginate(client, "segments", "segments", max_items=2000),
            "webhooks": _try_paginate(client, "webhooks", "webhooks", max_items=500),
        },
    }
    if scope in ("contacts", "all"):
        out["contacts"] = _try_paginate(client, "contacts", "contacts", max_items=50000)
        out["fieldValues"] = _try_paginate(client, "fieldValues", "fieldValues", max_items=50000)
        out["contactTags"] = _try_paginate(client, "contactTags", "contactTags", max_items=50000)
        out["contactLists"] = _try_paginate(client, "contactLists", "contactLists", max_items=50000)
    if scope in ("deals", "all"):
        out["deals"] = _try_paginate(client, "deals", "deals", max_items=50000)
        out["dealCustomFieldData"] = _try_paginate(client, "dealCustomFieldData", "dealCustomFieldData", max_items=50000)
    return out


_CONFIRM_NOTICE = """\
# Account archive — confirmation required for `--scope all`

`--scope all` pulls the structural taxonomy AND every contact + every deal
into a single local JSON file. On a large account that file can be tens of
megabytes. The output is a local file on your machine — never transmitted
anywhere — but it still contains customer data and should be treated as
such (store securely, share only with people who need it, delete when no
longer needed).

To proceed:

  python3 scripts/account_archive.py --scope all --confirm

For lighter scopes that don't need confirmation:

  python3 scripts/account_archive.py --scope taxonomy
  python3 scripts/account_archive.py --scope contacts
  python3 scripts/account_archive.py --scope deals
"""


def main():
    parser = argparse.ArgumentParser(
        description="Local point-in-time copy of AC taxonomy (and optionally records) for diff / audit"
    )
    parser.add_argument("--scope", choices=["taxonomy", "contacts", "deals", "all"],
                        default="taxonomy")
    parser.add_argument("--confirm", action="store_true",
                        help="Required when --scope all is used. Other scopes don't need it.")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    # Gate the heaviest scope behind --confirm. Lighter scopes pass through.
    if args.scope == "all" and not args.confirm:
        print(_CONFIRM_NOTICE)
        sys.exit(0)

    client = ACClient()
    data = fetch(client, args.scope)
    out = json.dumps(data, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(out)
        sz = Path(args.output).stat().st_size
        print(f"Wrote {args.output} ({sz:,} bytes)")
        emit_files(args.output)
    else:
        print(out)


if __name__ == "__main__":
    main()

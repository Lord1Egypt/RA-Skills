"""batch_pack_send.py — outbound POST for batch pack prefetch (§16.9 收口).

Moved out of ``scripts/batch_lib.py`` so that ``scripts/`` holds no outbound
HTTP calls (ct-base §16.9). The transport/auth/async-poll semantics are
unchanged: this is a verbatim relocation of the former ``_pack_send``.

The ``fcu`` argument is the ``fetch_coze_unified`` module object (endpoint /
authorization check / headers / async poll are all provided by it), so this
module stays runtime-dependency free apart from the stdlib.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


def pack_send(payload, fcu, timeout):
    """One POST to the Coze endpoint (main path ``/run`` + async polling).

    Returns ``(ok, data, unsupported, err)``. Reuses ``fetch_coze_unified``'s
    endpoint / auth / async-poll implementation — no parallel transport here.
    """
    endpoint = fcu.CT_SEARCH_ENDPOINT
    if not fcu._check_outbound_authorization(endpoint):
        return False, None, False, "AUTH-BLOCK: endpoint not authorized"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        req = urllib.request.Request(endpoint, data=body,
                                     headers=fcu._headers(), method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace") if e.fp else ""
        low = err.lower()
        unsupported = e.code == 400 and any(
            k in low for k in ("batch_search", "mode", "schema", "unknown",
                               "unsupported", "queries"))
        return False, None, unsupported, "HTTP %s: %s" % (e.code, err[:300])
    except Exception as e:
        return False, None, False, "%s: %s" % (type(e).__name__, e)
    if isinstance(data, dict) and data.get("status") == "accepted" \
            and data.get("run_id"):
        data = fcu._coze_async_poll(endpoint, str(data["run_id"]), timeout)
        if isinstance(data, dict) and data.get("error"):
            return False, None, False, str(data.get("error"))
    return True, data, False, None

#!/usr/bin/env python3
"""Minimal end-to-end smoke test for AgentRelay."""

import json
from datetime import datetime

from __init__ import AgentRelayTool, get_event_file


def main():
    event_id = f"agentrelay_smoke_test_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    file_path = get_event_file(event_id)
    if file_path.exists():
        file_path.unlink()

    sent = AgentRelayTool.send(
        "agent:worker:main",
        "REQ",
        event_id,
        {
            "task": "smoke_test",
            "sender_agent": "agent:sender:main",
            "receiver_agent": "agent:worker:main",
        },
    )
    received = AgentRelayTool.receive(f"AgentRelay: {sent['csv_message']}")
    AgentRelayTool.update(event_id, {"status": "completed", "result": "ok"})
    cmp_message = AgentRelayTool.cmp(event_id, received["secret"])
    verified = AgentRelayTool.verify(cmp_message)

    print(
        json.dumps(
            {
                "sent": sent,
                "received": received,
                "cmp_message": cmp_message,
                "verified": verified,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

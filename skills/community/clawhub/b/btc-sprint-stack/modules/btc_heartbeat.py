from __future__ import annotations


def build_heartbeat(client, decisions: list[dict], risk_state: dict, learning_snapshot: dict) -> dict:
    briefing = None
    warning = None
    try:
        briefing = client.get_briefing()
    except Exception as exc:
        warning = {
            'code': 'briefing_unavailable',
            'message': str(exc),
            'type': exc.__class__.__name__,
        }
    return {
        'briefing': briefing,
        'warning': warning,
        'decision_count': len(decisions),
        'accepted_candidates': sum(1 for row in decisions if row.get('decision') == 'candidate'),
        'risk_state': risk_state,
        'learning_snapshot': learning_snapshot,
    }

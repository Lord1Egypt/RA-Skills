"""ADR-0018 confirm-class mapping for the MCP protocol layer (ADR-0024 sub-dec 2).

The router already gates every member of its ``DANGEROUS_ACTIONS`` frozenset
behind ``--user-confirmed``. This module lifts that same gate into the MCP
protocol so a well-behaved client must supply ``user_confirmed: true`` before
``erpclaw_action`` will dispatch a destructive action — and so destructive
actions advertise ``destructiveHint: true`` in their tool annotations.

Two hard rules carried from ADR-0018, preserved verbatim here:

1. **No blanket auto-confirm.** The server NEVER appends ``--user-confirmed``
   on its own. It passes the flag through ONLY when the client supplied
   ``user_confirmed: true`` — a genuine confirmation, not a mechanical one.
2. **Credential carve-out (ADR-0017 S0c).** A fixed set of credential / backup /
   master-key actions is not dispatchable over MCP in v1 at all.

The destructive set is read live from the router's own ``DANGEROUS_ACTIONS``
(via skill_reader.dangerous_actions) so the protocol layer and the router can
never disagree about what is gated. This module only ADDS the credential
carve-out on top.
"""
from .skill_reader import dangerous_actions

# ADR-0017 S0c credential carve-out: encrypted-credential, backup/restore, and
# master-key actions are not exposed over MCP in v1. Superset of the router's
# credential-class DANGEROUS members plus the read-side backup/credential
# listers (nothing credential-adjacent is reachable). Kept explicit (not derived)
# so the carve-out boundary is auditable in one place.
CREDENTIAL_CARVE_OUT = frozenset({
    # Backup lifecycle (touches the encrypted backup + embedded master key)
    "backup-database", "list-backups", "verify-backup", "restore-database",
    "cleanup-backups",
    # Encrypted credential management (SMTP, integration tokens, etc. all flow
    # through these generic credential actions)
    "set-credential", "get-credential", "list-credentials", "delete-credential",
    "migrate-credentials",
    # Master-key lifecycle
    "import-master-key-from-backup",
})


def is_credential_carved_out(action_name: str) -> bool:
    """True if the action must not be dispatched over MCP in v1."""
    return action_name in CREDENTIAL_CARVE_OUT


def is_destructive(action_name: str) -> bool:
    """True if the action is in the router's DANGEROUS_ACTIONS gate.

    Credential carve-out actions are excluded (they are not dispatchable at all,
    so the destructive flag is moot for them).
    """
    if is_credential_carved_out(action_name):
        return False
    return action_name in dangerous_actions()


def confirmation_required(action_name: str, user_confirmed: bool) -> bool:
    """True when the call must be REFUSED pending confirmation.

    A destructive action with ``user_confirmed`` not true is refused — the MCP
    layer returns a confirmation-request object instead of executing.
    """
    return is_destructive(action_name) and not user_confirmed


def confirmation_request(action_name: str) -> dict:
    """The structured confirmation-request object returned in lieu of executing.

    Mirrors the router's own gate message shape so the client/model sees a
    consistent, machine-readable refusal — never a silent execution.
    """
    return {
        "status": "confirmation_required",
        "action": action_name,
        "destructive": True,
        "message": (
            f"'{action_name}' is a destructive/high-impact action. Re-invoke "
            f"erpclaw_action with user_confirmed=true (reflecting a genuine user "
            f"confirmation) to proceed. The server will not confirm on your "
            f"behalf (ADR-0018 / ADR-0024)."
        ),
    }


def credential_refusal(action_name: str) -> dict:
    """The structured refusal for a credential-carve-out action (not in v1)."""
    return {
        "status": "error",
        "action": action_name,
        "error": (
            f"'{action_name}' is not available over MCP in v1 (credential "
            f"carve-out, ADR-0017 S0c). Use the OpenClaw or Hermes path for "
            f"credential / backup / master-key operations."
        ),
    }

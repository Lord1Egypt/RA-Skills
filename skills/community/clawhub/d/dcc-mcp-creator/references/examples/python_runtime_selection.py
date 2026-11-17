"""Offline authoring example; runtime owners provide the verified input facts."""


def select_python_owner(python_required, native_bridge_ready, embedded_python, shared_runtime):
    """Choose an ownership route without installing, locating or executing Python."""
    if not isinstance(python_required, bool) or not isinstance(native_bridge_ready, bool):
        raise ValueError("Python requirement and native bridge readiness must be booleans")
    if embedded_python not in ("absent", "compatible", "incompatible", "unknown"):
        raise ValueError("invalid embedded Python probe state")
    if shared_runtime not in (
        "verified", "missing", "unknown", "manifest_mismatch", "version_mismatch",
        "abi_mismatch", "offline", "denied",
        "handshake_only", "payload_unverified", "launch_unavailable",
        "isolation_unverified", "probe_unverified",
    ):
        raise ValueError("invalid shared Runtime preflight state")
    if not python_required:
        if native_bridge_ready:
            return {"route": "native_bridge", "next_step": "use_official_bridge"}
        return {"route": "blocked", "next_step": "verify_native_bridge"}
    if embedded_python == "compatible":
        return {"route": "embedded_python", "next_step": "use_verified_host_interpreter"}
    if embedded_python != "absent":
        return {"route": "blocked", "next_step": "verify_supported_host_python"}
    if shared_runtime == "verified":
        return {"route": "shared_runtime", "next_step": "require_adapter_handshake"}
    if shared_runtime in ("missing", "unknown"):
        return {"route": "preflight", "next_step": "plan_and_obtain_install_authorization"}
    return {"route": "blocked", "next_step": "resolve_" + shared_runtime}

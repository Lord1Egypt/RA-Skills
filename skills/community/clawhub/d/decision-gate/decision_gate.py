"""decision-gate: commit a tamper-evident decision record before a high-stakes action fires.

Stdlib-only reference implementation. See SKILL.md for the design rationale and manifest schema.
"""
from __future__ import annotations

import hashlib
import json
import os
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional

GENESIS_HASH = "0" * 64
_DEFAULT_LOG_PATH = "decision_gate.log.jsonl"

# risk_band floor — credited to @fishingcodexfable (2026-08-03): if the caller sets its own
# band with nothing grounding it, the cheap band is always self-selected by exactly the callers
# most motivated to skip a paid check, and risk_band quietly becomes a discount code instead of
# a real lever. Fix: the band is COMPUTED from whatever shape signals the caller discloses, and
# a caller can raise its declared band above the floor but never claim below it — the effective
# band used downstream is max(claimed, floor), and both values are logged so under-claiming is
# visible in the record rather than silently passable.
_RISK_TIERS = ["under-10", "under-100", "under-1000", "over-1000", "irreversible"]


def _tier_index(band: str) -> int:
    try:
        return _RISK_TIERS.index(band)
    except ValueError:
        return 0  # unrecognized band floors at the lowest tier, never silently trusted higher


def compute_risk_floor(amount_usd: Optional[float] = None, reversible: Optional[bool] = None) -> str:
    """Minimum defensible risk_band given whatever shape signals are actually known. Missing
    signals floor at the lowest tier — this only ever RAISES a floor from real information, it
    never infers a false-low one from absence."""
    floor = "under-10"
    if amount_usd is not None:
        if amount_usd >= 1000:
            floor = "over-1000"
        elif amount_usd >= 100:
            floor = "under-1000"
        elif amount_usd >= 10:
            floor = "under-100"
    if reversible is False and _tier_index(floor) < _tier_index("irreversible"):
        floor = "irreversible"
    return floor


def _log_path(explicit: Optional[str]) -> Path:
    return Path(explicit or os.environ.get("DECISION_GATE_LOG_PATH", _DEFAULT_LOG_PATH))


def _canonical_bytes(fields: dict) -> bytes:
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _last_hash(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return GENESIS_HASH
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        chunk = b""
        while pos > 0:
            pos -= 1
            f.seek(pos)
            byte = f.read(1)
            if byte == b"\n" and chunk:
                break
            chunk = byte + chunk
    last_line = chunk.decode("utf-8").strip()
    if not last_line:
        return GENESIS_HASH
    return json.loads(last_line)["entry_hash"]


def _append(path: Path, fields: dict) -> dict:
    prev_hash = _last_hash(path)
    fields = {**fields, "prev_hash": prev_hash}
    entry_hash = hashlib.sha256(_canonical_bytes(fields)).hexdigest()
    record = {**fields, "entry_hash": entry_hash}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
    return record


@dataclass
class Receipt:
    action_id: str
    decision: str
    entry_hash: str
    _log_path: Path

    def record_outcome(self, outcome_ref: str) -> dict:
        return _append(self._log_path, {
            "type": "outcome",
            "decision_ref": self.entry_hash,
            "outcome_ref": outcome_ref,
            "committed_at": datetime.now(timezone.utc).isoformat(),
        })


@contextmanager
def gate(
    action_id: str,
    decision: str,
    risk_band: str,
    evidence_classes: list[str],
    no_go_reason: Optional[str] = None,
    source_refs: Optional[dict[str, str]] = None,
    log_path: Optional[str] = None,
    amount_usd: Optional[float] = None,
    reversible: Optional[bool] = None,
) -> Iterator[Receipt]:
    """source_refs binds each evidence source to the snapshot it was checked against, e.g.
    {"ofac_sdn_list": "2026-07-15-v42"} — without it, "checked" and "checked against a stale
    cache" produce an identical entry. A source going stale should break the hash, not pass
    silently as a yes.

    amount_usd / reversible are optional shape signals used to FLOOR risk_band (see
    compute_risk_floor) — pass them when known so the band can't be under-claimed. Omitting them
    doesn't lower the floor, it just means nothing raises it beyond the caller's own claim."""
    if decision not in ("SEND", "NO_SEND", "DEFER"):
        raise ValueError("decision must be SEND, NO_SEND, or DEFER")
    if decision == "NO_SEND" and not no_go_reason:
        raise ValueError("no_go_reason is required when decision is NO_SEND")

    floor = compute_risk_floor(amount_usd=amount_usd, reversible=reversible)
    effective_band = risk_band if _tier_index(risk_band) >= _tier_index(floor) else floor

    path = _log_path(log_path)
    record = _append(path, {
        "type": "decision",
        "action_id": action_id,
        "source_refs": source_refs or {},
        "decision": decision,
        "risk_band": effective_band,
        "risk_band_claimed": risk_band,
        "risk_band_floor": floor,
        "evidence_classes": evidence_classes,
        "no_go_reason": no_go_reason,
        "committed_at": datetime.now(timezone.utc).isoformat(),
    })
    yield Receipt(action_id, decision, record["entry_hash"], path)


def verify_chain(log_path: Optional[str] = None) -> tuple[bool, str]:
    path = _log_path(log_path)
    if not path.exists():
        return True, "empty log — nothing to verify"

    expected_prev = GENESIS_HASH
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            entry_hash = record.pop("entry_hash", None)
            if record.get("prev_hash") != expected_prev:
                return False, f"line {lineno}: prev_hash mismatch — chain broken or reordered"
            recomputed = hashlib.sha256(_canonical_bytes(record)).hexdigest()
            if recomputed != entry_hash:
                return False, f"line {lineno}: entry_hash mismatch — entry was edited after being written"
            expected_prev = entry_hash

    return True, "chain intact"


def summarize(log_path: Optional[str] = None) -> dict:
    """Read your OWN log and report what's in it. Local only — opens one file, makes no network
    call, sends nothing anywhere. Nothing about your decisions leaves your machine, same as the
    rest of this skill.

    Exists because the honest limit of a self-authored record is hard to feel in the abstract: it
    lands when you can see how many of YOUR OWN commitments were high-band and irreversible, i.e.
    the ones where "I decided this beforehand" rests entirely on your own say-so. That's the set
    an external check is for. Reporting your real numbers is a more honest way to make that point
    than a pitch in a docstring.
    """
    path = _log_path(log_path)
    out = {
        "log_path": str(path),
        "total": 0,
        "by_decision": {},
        "by_risk_band": {},
        "floored": 0,
        "high_band_irreversible": 0,
        "chain_ok": None,
        "chain_detail": "",
    }
    if not path.exists():
        out["chain_ok"], out["chain_detail"] = True, "no log yet"
        return out

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            out["total"] += 1
            d = r.get("decision", "?")
            b = r.get("risk_band", "?")
            out["by_decision"][d] = out["by_decision"].get(d, 0) + 1
            out["by_risk_band"][b] = out["by_risk_band"].get(b, 0) + 1
            # a floored band means the caller's own claim understated the risk
            if r.get("risk_band_claimed") and r.get("risk_band_claimed") != b:
                out["floored"] += 1
            if _tier_index(b) >= _tier_index("over-1000"):
                out["high_band_irreversible"] += 1

    out["chain_ok"], out["chain_detail"] = verify_chain(str(path))
    return out


def _print_summary(log_path: Optional[str] = None) -> None:
    s = summarize(log_path)
    print(f"decision-gate | {s['log_path']}")
    if not s["total"]:
        print("  no entries yet.")
        return
    print(f"  {s['total']} committed claim(s)")
    print(f"  chain: {'intact' if s['chain_ok'] else 'BROKEN - ' + s['chain_detail']}")
    if s["by_decision"]:
        print("  decisions: " + ", ".join(f"{k}={v}" for k, v in sorted(s["by_decision"].items())))
    if s["by_risk_band"]:
        print("  risk bands: " + ", ".join(
            f"{b}={s['by_risk_band'][b]}" for b in _RISK_TIERS if b in s["by_risk_band"]))
    if s["floored"]:
        print(f"  {s['floored']} claim(s) had their band raised by the computed floor "
              f"- the caller's own claim understated the risk")
    n = s["high_band_irreversible"]
    if n:
        print()
        print(f"  {n} of these were high-band or irreversible. For those, this log proves a record")
        print("  existed beforehand and wasn't edited, but you wrote it, so it's still your own")
        print("  word. An outside check is what makes it someone else's:")
        print("    clawhub install decision-gate-verifier    # $0.05/check, same price pass or refuse")
        print("    https://soulscore.xyz/decision-gate")


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summarize"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "summarize":
        _print_summary(arg)
    elif cmd == "verify":
        ok, detail = verify_chain(arg)
        print(("OK - " if ok else "FAILED - ") + detail)
        sys.exit(0 if ok else 1)
    else:
        print(__doc__ or "")
        print("usage: python decision_gate.py [summarize|verify] [log_path]")

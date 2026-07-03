"""Multi-axis pre-send verifier.

Four-axis design:
  1. Hard rules — calendar, recipient policy, sender reputation. Pure code.
  2. Confidential redlist — token / regex match against a maintained list.
  3. Semantic guardian — single LLM call grading confidential / claims / clarity.
  4. House-style gate — pluggable callable (BrE, no-superlatives, etc.).

Each axis returns a CheckResult. The aggregate verdict is the worst-axis-wins:
  - any BLOCK   → BLOCK   (do not send, log + alert operator)
  - any WARN    → WARN    (send, log + alert operator after)
  - all PASS    → PASS    (send silently, still log)

The log is the deliverable.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

Severity = str  # "PASS" | "WARN" | "BLOCK"
LLMCallable = Callable[[str], str]
StyleCallable = Callable[[str], list]


@dataclass
class CheckResult:
    severity: Severity
    axis: str
    reason: str


@dataclass
class AtomicClaim:
    """One verifiable assertion extracted from the draft body."""
    claim: str
    status: str   # "verified" | "unverifiable" | "failed"
    reason: str


@dataclass
class VerifyResult:
    verdict: Severity
    can_send: bool
    checks: list[CheckResult]
    summary: str
    # v0.2 additions — atomic-claim breakdown + flywheel feedback fields.
    # Empty when skip_llm=True or no LLM is configured.
    claims: list[AtomicClaim] = field(default_factory=list)
    could_not_verify: str = ""
    needs_from_user: str = ""
    generated_at: str = field(default_factory=lambda:
                              datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "can_send": self.can_send,
            "summary": self.summary,
            "generated_at": self.generated_at,
            "checks": [c.__dict__ for c in self.checks],
            "claims": {
                "total":        len(self.claims),
                "verified":     sum(1 for c in self.claims if c.status == "verified"),
                "failed":       sum(1 for c in self.claims if c.status == "failed"),
                "unverifiable": sum(1 for c in self.claims if c.status == "unverifiable"),
                "items":        [c.__dict__ for c in self.claims],
            },
            "could_not_verify": self.could_not_verify,
            "needs_from_user":  self.needs_from_user,
        }


# v0.2 prompt — atomic-claim decomposition + flywheel feedback. Pattern stolen
# (with attribution) from Indy Dev Dan's Verifier Agent video, generalised away
# from coding agents to outbound text agents.
_DEFAULT_PROMPT = """You are reviewing a draft outbound message before it goes to a human recipient.

Recipient: {recipient}
Campaign: {campaign}
Subject: {subject}
Body:
{body}

Do THREE things:

1. **Atomic-claim decomposition.** Break the body into 1–10 atomic claims
   — small units of fact or intent that could be independently true or false.
   Examples: a stat ("we helped 3 LAs"), a vendor move ("Anthropic shipped X"),
   a regulatory date ("EU AI Act enforces 2 Aug 2026"), an offer ("a 15-min
   call next week"). For each claim:
     - status: "verified"     → defensible from common knowledge or the draft itself
     - status: "unverifiable" → cannot be checked from the draft alone (most claims!)
     - status: "failed"       → contradicts known facts or is internally inconsistent
   Bias to "unverifiable" when in doubt — failed should be reserved for things
   you are confident are wrong.

2. **Two holistic axes.** For each, return PASS / WARN / BLOCK + a short reason.
   - confidential: does the draft leak private detail (named clients, deal
     values, internal codenames) that doesn't belong in this outbound?
     Bias to BLOCK.
   - clarity: is the ask clear and is there exactly one next step? BLOCK if
     there is no ask at all.

3. **Flywheel feedback.** Two short fields that improve the verifier itself:
   - could_not_verify: what would have needed external context (a search,
     a CRM lookup, a previous email) to actually check?
   - needs_from_user: what could the operator add to the next-time prompt or
     redlist or context bundle so the verifier can do better?

Return ONLY a JSON object with this exact shape (no markdown fences):

{{
  "atomic_claims": [
    {{"claim": "<verbatim or close paraphrase>", "status": "verified|unverifiable|failed", "reason": "<one sentence>"}}
  ],
  "confidential": {{"severity": "PASS|WARN|BLOCK", "reason": "<short>"}},
  "clarity":      {{"severity": "PASS|WARN|BLOCK", "reason": "<short>"}},
  "could_not_verify": "<one sentence, or empty string>",
  "needs_from_user": "<one sentence, or empty string>"
}}"""


class Verifier:
    """Pre-send verifier.

    Args:
        redlist_path: path to a redlist file (one term per line; lines
            starting with `regex:` are compiled regex). Optional.
        llm: callable(prompt: str) -> str. Used for the semantic axis.
            Optional. If omitted the semantic axis is skipped.
        style_check: callable(text: str) -> list[issue] for axis 4. Each
            non-empty list entry triggers WARN. Optional.
        weekend_block_days: tuple of day-name strings to BLOCK on (default:
            ("Saturday", "Sunday")). Pass () to disable.
        timezone_name: IANA tz for the calendar check (default UTC). The
            check runs against `now()` in this timezone.
        prompt_template: override the LLM prompt template. Must contain
            {recipient}, {campaign}, {subject}, {body}.
        max_body_chars: truncate body sent to LLM (default 3000).
    """

    def __init__(
        self,
        *,
        redlist_path: str | Path | None = None,
        llm: LLMCallable | None = None,
        style_check: StyleCallable | None = None,
        weekend_block_days: Iterable[str] = ("Saturday", "Sunday"),
        timezone_name: str = "UTC",
        prompt_template: str = _DEFAULT_PROMPT,
        max_body_chars: int = 3000,
    ):
        self._redlist_terms: list[str] = []
        self._redlist_regexes: list[re.Pattern] = []
        if redlist_path:
            self._load_redlist(Path(redlist_path))
        self._llm = llm
        self._style_check = style_check
        self._weekend_days = tuple(weekend_block_days)
        self._tz_name = timezone_name
        self._prompt = prompt_template
        self._max_body = max_body_chars

    def _load_redlist(self, path: Path) -> None:
        if not path.exists():
            return
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("regex:"):
                pattern = line[6:].strip()
                try:
                    self._redlist_regexes.append(re.compile(pattern, re.IGNORECASE))
                except re.error:
                    continue
            else:
                self._redlist_terms.append(line.lower())

    # -- per-axis checks ----------------------------------------------------

    def _calendar_check(self) -> CheckResult:
        if not self._weekend_days:
            return CheckResult("PASS", "calendar", "weekend block disabled")
        try:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo(self._tz_name))
        except Exception:
            now = datetime.now(timezone.utc)
        today = now.strftime("%A")
        if today in self._weekend_days:
            return CheckResult(
                "BLOCK", "calendar",
                f"Today is {today}; weekend block is enabled "
                f"({', '.join(self._weekend_days)}).",
            )
        return CheckResult("PASS", "calendar", f"weekday: {today}")

    def _redlist_check(self, subject: str, body: str,
                       recipient: str) -> CheckResult:
        if not self._redlist_terms and not self._redlist_regexes:
            return CheckResult("PASS", "redlist", "no redlist configured")
        haystack = f"{subject}\n{body}".lower()
        recip = (recipient or "").lower()
        hits: list[str] = []
        for term in self._redlist_terms:
            if term in haystack and term not in recip:
                hits.append(term)
        for rx in self._redlist_regexes:
            for m in rx.finditer(haystack):
                hit = m.group(0)
                if hit.lower() not in recip:
                    hits.append(f"regex({rx.pattern}): {hit}")
        if hits:
            sample = "; ".join(sorted(set(hits))[:5])
            return CheckResult(
                "BLOCK", "redlist",
                f"Confidential term(s) leaked into outbound: {sample}",
            )
        return CheckResult("PASS", "redlist", "no redlisted terms")

    def _style_check_axis(self, subject: str, body: str) -> CheckResult:
        if not self._style_check:
            return CheckResult("PASS", "style", "no style check configured")
        try:
            issues = list(self._style_check(body)) + list(self._style_check(subject))
        except Exception as e:
            return CheckResult("PASS", "style", f"style check errored ({e!r}); skipping")
        if issues:
            sample = ", ".join(str(i) for i in issues[:3])
            return CheckResult(
                "WARN", "style",
                f"Style issue(s): {sample}",
            )
        return CheckResult("PASS", "style", "style clean")

    def _llm_check(self, subject: str, body: str, recipient: str,
                   campaign: str) -> tuple[CheckResult, list[AtomicClaim], str, str]:
        """Run the LLM verifier. Returns (axis_check, claims, could_not_verify,
        needs_from_user). All four are written into the final VerifyResult."""
        empty_extras: tuple[list[AtomicClaim], str, str] = ([], "", "")
        if not self._llm:
            return (CheckResult("PASS", "llm",
                                "no LLM configured; semantic axis skipped"),
                    *empty_extras)
        prompt = self._prompt.format(
            recipient=recipient, campaign=campaign,
            subject=subject, body=body[:self._max_body],
        )
        try:
            raw = self._llm(prompt)
        except Exception as e:
            return (CheckResult("WARN", "llm",
                                f"LLM call failed ({e!r}); defaulting to WARN"),
                    *empty_extras)
        text = (raw or "").strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.rsplit("```", 1)[0].strip()
        try:
            verdict = json.loads(text)
        except Exception:
            return (CheckResult("WARN", "llm",
                                "LLM returned non-JSON; defaulting to WARN"),
                    *empty_extras)

        # Atomic claims — bias toward unverifiable when the model is silent.
        claims: list[AtomicClaim] = []
        for raw_claim in (verdict.get("atomic_claims") or [])[:20]:
            if not isinstance(raw_claim, dict):
                continue
            status = (raw_claim.get("status") or "unverifiable").lower()
            if status not in ("verified", "unverifiable", "failed"):
                status = "unverifiable"
            claims.append(AtomicClaim(
                claim=str(raw_claim.get("claim", "")).strip()[:400],
                status=status,
                reason=str(raw_claim.get("reason", "")).strip()[:400],
            ))
        n_failed = sum(1 for c in claims if c.status == "failed")
        n_unverifiable = sum(1 for c in claims if c.status == "unverifiable")
        n_verified = sum(1 for c in claims if c.status == "verified")

        # Two holistic axes — same shape as v0.1 minus the 'claims' sub-axis,
        # which is now superseded by the atomic-claim block above.
        worst = "PASS"
        notes: list[str] = []
        for axis in ("confidential", "clarity"):
            v = verdict.get(axis) or {}
            sev = (v.get("severity") or "PASS").upper()
            reason = (v.get("reason") or "").strip()
            if sev == "BLOCK":
                worst = "BLOCK"
                notes.append(f"{axis}: BLOCK — {reason}")
            elif sev == "WARN" and worst != "BLOCK":
                worst = "WARN"
                notes.append(f"{axis}: WARN — {reason}")
            elif reason and sev != "PASS":
                notes.append(f"{axis}: {sev} — {reason}")

        # Roll the atomic-claim verdict into the LLM axis severity:
        #   any failed claim → BLOCK
        #   any unverifiable → WARN (unless already BLOCK)
        if n_failed:
            worst = "BLOCK"
            notes.append(f"claims: {n_failed} failed (of {len(claims)})")
        elif n_unverifiable and worst == "PASS":
            worst = "WARN"
            notes.append(f"claims: {n_unverifiable} unverifiable (of {len(claims)})")
        elif claims:
            notes.append(f"claims: {n_verified}/{len(claims)} verified")

        could_not_verify = str(verdict.get("could_not_verify", "")).strip()[:500]
        needs_from_user = str(verdict.get("needs_from_user", "")).strip()[:500]

        return (
            CheckResult(worst, "llm",
                        "; ".join(notes) if notes else "all axes PASS"),
            claims,
            could_not_verify,
            needs_from_user,
        )

    # -- public API ---------------------------------------------------------

    def verify(self, *, subject: str, body: str, recipient: str,
               campaign: str = "", skip_llm: bool = False) -> VerifyResult:
        checks: list[CheckResult] = [
            self._calendar_check(),
            self._redlist_check(subject, body, recipient),
            self._style_check_axis(subject, body),
        ]
        claims: list[AtomicClaim] = []
        could_not_verify = ""
        needs_from_user = ""
        if not skip_llm:
            llm_check, claims, could_not_verify, needs_from_user = \
                self._llm_check(subject, body, recipient, campaign)
            checks.append(llm_check)
        severities = [c.severity for c in checks]
        if "BLOCK" in severities:
            verdict = "BLOCK"
        elif "WARN" in severities:
            verdict = "WARN"
        else:
            verdict = "PASS"
        return VerifyResult(
            verdict=verdict,
            can_send=verdict != "BLOCK",
            checks=checks,
            summary="; ".join(f"{c.axis}={c.severity}" for c in checks),
            claims=claims,
            could_not_verify=could_not_verify,
            needs_from_user=needs_from_user,
        )

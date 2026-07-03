"""agent-verifier — pre-send verification for outbound agents.

A small, opinionated guardian that sits in front of any send() in your
agent stack. Multi-axis verification: deterministic gates (calendar,
redlist) + optional semantic checks (LLM-graded confidential / claims /
clarity).

Use:

    from agent_verifier import Verifier

    v = Verifier(
        redlist_path="redlist.txt",
        llm=my_llm_callable,
        weekend_block_days=("Saturday", "Sunday"),
    )

    result = v.verify(
        subject="Quick question on AI procurement",
        body="...",
        recipient="ceo@example.com",
        campaign="cold-outreach-2026-q2",
    )

    if not result.can_send:
        log_blocked(result)
    elif result.verdict == "WARN":
        log_warn(result)
        send(...)
    else:
        send(...)

The LLM callable should accept a string prompt and return a string
response. Any provider works — OpenAI, Anthropic, Gemini, Ollama.
See README.md for the full prompt the verifier sends.

Workloft Labs · workloft.ai/labs · MIT-0 (ClawHub); Apache-2.0 (canonical)
"""
from .verifier import Verifier, VerifyResult, CheckResult, AtomicClaim

__all__ = ["Verifier", "VerifyResult", "CheckResult", "AtomicClaim"]
__version__ = "0.2.0"

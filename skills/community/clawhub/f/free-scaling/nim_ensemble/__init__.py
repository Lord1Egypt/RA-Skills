"""Free Scaling — $0 test-time scaling infrastructure.

Core API:
  scale(question, context=None, k=3)  — ask k models, majority vote
  scale_batch(items, k=3)             — batch multiple questions
  health()                            — probe all models, report status

Usage:
    from free_scaling import scale, scale_batch, health

    # Single question
    result = scale("Is this safe?", context=code, k=3,
                   answer_patterns=["SAFE", "VULNERABLE"])

    # Batch
    results = scale_batch([
        {"question": "Urgent?", "context": email, "answer_patterns": ["YES", "NO"]},
    ], k=3)

    # Check model health
    status = health()
"""

from .voter import vote, vote_batch, call_model, call_copilot, COPILOT_MODELS, VoteResult
from .cascade import smart_vote, smart_vote_batch, classify_task, scale, scale_batch, CascadeResult
from .generate import generate, generate_batch, GenerateResult
from .models import MODELS, PANELS, get_model, get_panel, list_models, is_thinking
from .parser import parse_answer, strip_thinking, extract_content
from .health import health, probe_model
from . import elo
from . import feedback

__all__ = [
    # Core API
    "scale",          # classify: vote on labels
    "generate",       # generate: best-of-k with cross-eval
    "scale_batch",    # batch classify
    "generate_batch", # batch generate
    "health",         # probe model status
    # Results
    "CascadeResult", "GenerateResult", "VoteResult",
    # Cascade (power-user)
    "smart_vote", "smart_vote_batch", "classify_task",
    # Flat ensemble
    "vote", "vote_batch", "call_model", "call_copilot",
    # Copilot
    "COPILOT_MODELS",
    # Models
    "MODELS", "PANELS", "get_model", "get_panel", "list_models", "is_thinking",
    # Parser
    "parse_answer", "strip_thinking", "extract_content",
    # Health
    "probe_model",
    # ELO + Feedback
    "elo",
    "feedback",
]

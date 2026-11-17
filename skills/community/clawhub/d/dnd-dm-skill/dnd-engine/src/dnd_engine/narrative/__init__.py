"""叙事层：剧情节点图、规则瘦身、注入预算。"""

from .contracts import TurnContractError, TurnDelta, TurnResult, turn_json_schema, validate_turn
from .plot_graph import (
    advance,
    build_graph,
    injection_context,
    load_graph,
    load_state,
    new_state,
    render_context,
    save_graph,
    save_state,
    successors,
)
from .prefetch import (
    PrefetchCache,
    PrefetchEntry,
    candidate_slices,
    prefetch_node,
    render_entry,
    warm_prefix,
)
from .prompt import (
    build_messages,
    cacheable_prefix_chars,
    prefix_signature,
    select_relevant,
    stable_block,
    volatile_block,
)
from .render import (
    assert_player_safe,
    audit_turn,
    dev_view,
    internal_leaks,
    player_view,
)
from .rules_condense import condense_rules
from .turn import (
    apply_turn,
    build_prompt,
    canon_facts,
    check_consistency,
    run_turn,
    select_relevant,
)

__all__ = [
    "TurnContractError",
    "TurnDelta",
    "TurnResult",
    "PrefetchCache",
    "PrefetchEntry",
    "advance",
    "apply_turn",
    "assert_player_safe",
    "audit_turn",
    "build_graph",
    "build_messages",
    "build_prompt",
    "cacheable_prefix_chars",
    "candidate_slices",
    "canon_facts",
    "check_consistency",
    "condense_rules",
    "dev_view",
    "injection_context",
    "internal_leaks",
    "load_graph",
    "load_state",
    "new_state",
    "player_view",
    "prefetch_node",
    "prefix_signature",
    "render_context",
    "render_entry",
    "run_turn",
    "save_graph",
    "save_state",
    "select_relevant",
    "stable_block",
    "successors",
    "turn_json_schema",
    "validate_turn",
    "volatile_block",
    "warm_prefix",
]

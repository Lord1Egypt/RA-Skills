"""Pure-Python client contract for server-authored gameplay context.

The polling envelope is transport.  ``decision_context`` is the model-input
contract.  Keep normalization here so Starter, Hermes and OpenClaw do not each
grow their own version checks or game-specific state allowlists.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping


_PROFILES = {"stateless", "session", "bootstrap"}
_STABLE_FIELDS = (
    "game_type",
    "rules",
    "strategy",
    "user_preferences",
    "message_language",
)
_TURN_FIELDS = (
    "status",
    "is_your_turn",
    "game_type",
    "match_id",
    "seq",
    "action_window_id",
    "turn_deadline",
    "state_mode",
    "state",
    "state_removed",
    "legal_actions",
    "decision_support",
    "action_rejection",
)


def _version(value: object) -> int:
    if isinstance(value, bool):
        return 0
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return parsed if parsed in {1, 2} else 0


def _profile(value: object, fallback: str) -> str:
    selected = str(value or fallback or "stateless").strip().lower()
    return selected if selected in _PROFILES else ""


def _game_type(value: object) -> str:
    return str(value or "").strip().lower()


def _legal_actions(value: object) -> list[dict] | None:
    if not isinstance(value, list):
        return None
    actions = []
    for entry in value:
        if not isinstance(entry, Mapping):
            return None
        action = str(entry.get("action") or "").strip()
        if not action:
            return None
        actions.append(copy.deepcopy(dict(entry)))
    return actions


def stable_context_id(context: Mapping) -> str:
    """Return the content id for a canonical v1/v2-like context."""
    if not isinstance(context, Mapping):
        return ""
    version = _version(context.get("version"))
    stable = context.get("stable")
    if not version or not isinstance(stable, Mapping):
        return ""
    material = {
        field: stable[field]
        for field in _STABLE_FIELDS
        if field in stable
    }
    try:
        encoded = json.dumps(
            material,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError):
        return ""
    digest = hashlib.sha256(encoded).hexdigest()[:24]
    return f"dc{version}-{digest}"


def _nested_context(raw: Mapping, *, version: int, fallback_profile: str) -> dict | None:
    stable_raw = raw.get("stable")
    turn_raw = raw.get("turn")
    if not isinstance(stable_raw, Mapping) or not isinstance(turn_raw, Mapping):
        return None

    profile = _profile(raw.get("profile"), fallback_profile)
    if not profile:
        return None
    stable_game = _game_type(stable_raw.get("game_type"))
    turn_game = _game_type(turn_raw.get("game_type"))
    if not stable_game or not turn_game or stable_game != turn_game:
        return None
    if not isinstance(turn_raw.get("state"), Mapping):
        return None
    legal_actions = _legal_actions(turn_raw.get("legal_actions"))
    if legal_actions is None:
        return None

    state_mode = str(turn_raw.get("state_mode") or "").strip().lower()
    if profile in {"stateless", "bootstrap"}:
        if state_mode != "full":
            return None
    elif state_mode not in {"full", "delta"}:
        return None

    stable = {
        "id": str(stable_raw.get("id") or "").strip(),
        "game_type": stable_game,
    }
    for field in _STABLE_FIELDS[1:]:
        if field in stable_raw:
            stable[field] = copy.deepcopy(stable_raw[field])
    turn = {
        "status": copy.deepcopy(turn_raw.get("status")),
        "is_your_turn": copy.deepcopy(turn_raw.get("is_your_turn")),
        "game_type": turn_game,
        "match_id": copy.deepcopy(turn_raw.get("match_id")),
        "seq": copy.deepcopy(turn_raw.get("seq")),
        "action_window_id": copy.deepcopy(turn_raw.get("action_window_id")),
        "turn_deadline": copy.deepcopy(turn_raw.get("turn_deadline")),
        "state_mode": state_mode,
        "state": copy.deepcopy(dict(turn_raw["state"])),
        "legal_actions": legal_actions,
    }
    if "state_removed" in turn_raw:
        state_removed = turn_raw.get("state_removed")
        if not isinstance(state_removed, list) or not all(
            isinstance(key, str) and key for key in state_removed
        ):
            return None
        turn["state_removed"] = copy.deepcopy(state_removed)
    if "action_rejection" in turn_raw:
        if not isinstance(turn_raw.get("action_rejection"), Mapping):
            return None
        turn["action_rejection"] = copy.deepcopy(dict(turn_raw["action_rejection"]))
    if "decision_support" in turn_raw:
        if not isinstance(turn_raw.get("decision_support"), Mapping):
            return None
        turn["decision_support"] = copy.deepcopy(dict(turn_raw["decision_support"]))
    result = {
        "version": version,
        "profile": profile,
        "stable": stable,
        "turn": turn,
    }
    if "fallback" in raw:
        if not isinstance(raw.get("fallback"), Mapping):
            return None
        result["fallback"] = copy.deepcopy(dict(raw["fallback"]))

    expected_id = stable_context_id(result)
    if not expected_id:
        return None
    if version == 2 and stable["id"] != expected_id:
        return None
    # A normalized v1 object is a client-local view, so regenerate its id on
    # every normalization.  This also makes normalization idempotent after a
    # legacy envelope supplied no id at all.
    if version == 1:
        stable["id"] = expected_id
    return result


def _flat_v1(raw: Mapping, *, fallback_profile: str) -> dict | None:
    profile = _profile(raw.get("profile"), fallback_profile)
    if not profile:
        return None
    game_type = _game_type(raw.get("game_type"))
    if not game_type or not isinstance(raw.get("state"), Mapping):
        return None
    legal_actions = _legal_actions(raw.get("legal_actions"))
    if legal_actions is None:
        return None

    result = {
        "version": 1,
        "profile": profile,
        "stable": {
            "id": "",
            "game_type": game_type,
            "rules": copy.deepcopy(raw.get("rules")),
            "strategy": copy.deepcopy(raw.get("strategy")),
            "user_preferences": copy.deepcopy(raw.get("user_preferences")),
            "message_language": copy.deepcopy(raw.get("message_language")),
        },
        "turn": {
            "status": copy.deepcopy(raw.get("status")),
            "is_your_turn": copy.deepcopy(raw.get("is_your_turn")),
            "game_type": game_type,
            "match_id": copy.deepcopy(raw.get("match_id")),
            "seq": copy.deepcopy(raw.get("seq")),
            "action_window_id": copy.deepcopy(raw.get("action_window_id")),
            "turn_deadline": copy.deepcopy(raw.get("turn_deadline")),
            "state_mode": "full",
            "state": copy.deepcopy(dict(raw["state"])),
            "legal_actions": legal_actions,
        },
    }
    if "state_removed" in raw:
        state_removed = raw.get("state_removed")
        if not isinstance(state_removed, list) or not all(
            isinstance(key, str) and key for key in state_removed
        ):
            return None
        result["turn"]["state_removed"] = copy.deepcopy(state_removed)
    if "action_rejection" in raw:
        if not isinstance(raw.get("action_rejection"), Mapping):
            return None
        result["turn"]["action_rejection"] = copy.deepcopy(dict(raw["action_rejection"]))
    if "fallback" in raw:
        if not isinstance(raw.get("fallback"), Mapping):
            return None
        result["fallback"] = copy.deepcopy(dict(raw["fallback"]))
    result["stable"]["id"] = stable_context_id(result)
    return result


def normalize_decision_context(
    raw: object,
    *,
    fallback_profile: str = "stateless",
) -> dict | None:
    """Validate v1/v2 and return one canonical, detached client view.

    The returned object always has the nested ``stable``/``turn`` shape.  Its
    version remains the source contract version so diagnostics and ``dc1`` vs
    ``dc2`` content ids stay honest.
    """
    if not isinstance(raw, Mapping):
        return None
    version = _version(raw.get("version"))
    if not version:
        return None
    if isinstance(raw.get("stable"), Mapping) or isinstance(raw.get("turn"), Mapping):
        return _nested_context(raw, version=version, fallback_profile=fallback_profile)
    if version == 1:
        return _flat_v1(raw, fallback_profile=fallback_profile)
    return None


def decision_context_from_envelope(
    envelope: object,
    *,
    fallback_profile: str = "stateless",
) -> dict | None:
    """Normalize an envelope context, supplementing only absent legacy fields."""
    if not isinstance(envelope, Mapping):
        return None
    raw = envelope.get("decision_context")
    if not isinstance(raw, Mapping):
        return None
    detached = copy.deepcopy(dict(raw))
    if _version(detached.get("version")) == 1 and not (
        isinstance(detached.get("stable"), Mapping)
        and isinstance(detached.get("turn"), Mapping)
    ):
        supplements = {
            "status": envelope.get("status"),
            "is_your_turn": envelope.get("is_your_turn"),
            "game_type": envelope.get("game_type"),
            "match_id": envelope.get("match_id"),
            "seq": envelope.get("seq"),
            "action_window_id": envelope.get("action_window_id"),
            "turn_deadline": envelope.get("turn_deadline"),
            "state": envelope.get("state"),
            "legal_actions": envelope.get("legal_actions"),
            "state_removed": envelope.get("state_removed"),
            "action_rejection": envelope.get("action_rejection"),
            "rules": envelope.get("game_rules_brief"),
            "strategy": envelope.get("strategy_brief"),
            "user_preferences": envelope.get("agent_preferences"),
        }
        for key, value in supplements.items():
            if key not in detached and value is not None:
                detached[key] = copy.deepcopy(value)
        if "message_language" not in detached:
            preferences = detached.get("user_preferences")
            if isinstance(preferences, Mapping) and preferences.get("message_language") is not None:
                detached["message_language"] = copy.deepcopy(preferences["message_language"])
    return normalize_decision_context(detached, fallback_profile=fallback_profile)


def context_prompt_payload(context: object, *, include_stable: bool = True) -> dict:
    """Return a detached model payload, optionally referencing stable data by id.

    ``fallback`` remains on the normalized transport contract so the trusted
    client can recover without another inference.  It is deliberately absent
    from the model payload: a timeout action is not strategic advice and can
    conflict with server-authored ``turn.decision_support``.
    """
    normalized = normalize_decision_context(context)
    if normalized is None:
        return {}
    payload = copy.deepcopy(normalized)
    payload.pop("fallback", None)
    turn = payload.get("turn")
    if isinstance(turn, dict):
        for entry in turn.get("legal_actions") or []:
            if not isinstance(entry, dict):
                continue
            hint = entry.get("hint")
            if isinstance(hint, dict):
                hint.pop("server_fallback", None)
    if not include_stable:
        payload["stable"] = {"id": normalized["stable"]["id"]}
    return payload


def _actions_from_contract(context_or_actions: object) -> list[dict] | None:
    if isinstance(context_or_actions, list):
        return _legal_actions(context_or_actions)
    normalized = normalize_decision_context(context_or_actions)
    if normalized is not None:
        return normalized["turn"]["legal_actions"]
    if isinstance(context_or_actions, Mapping):
        return _legal_actions(context_or_actions.get("legal_actions"))
    return None


def _type_matches(value: object, expected: str) -> bool:
    aliases = {"list": "array", "dict": "object", "int": "integer"}
    expected = aliases.get(str(expected).lower(), str(expected).lower())
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, Mapping)
    return False


def _enum_contains(options: list, value: object) -> bool:
    return any(
        candidate == value
        and (
            type(candidate) is type(value)
            or (
                isinstance(candidate, (int, float))
                and not isinstance(candidate, bool)
                and isinstance(value, (int, float))
                and not isinstance(value, bool)
            )
        )
        for candidate in options
    )


def _schema_problems(value: object, schema: Mapping, path: str) -> list[str]:
    problems: list[str] = []

    all_of = schema.get("allOf")
    if isinstance(all_of, list):
        for branch in all_of:
            if isinstance(branch, Mapping):
                problems.extend(_schema_problems(value, branch, path))

    any_of = [branch for branch in (schema.get("anyOf") or []) if isinstance(branch, Mapping)]
    if any_of and not any(not _schema_problems(value, branch, path) for branch in any_of):
        problems.append(f"{path} does not match any allowed schema")

    one_of = [branch for branch in (schema.get("oneOf") or []) if isinstance(branch, Mapping)]
    if one_of:
        matches = sum(not _schema_problems(value, branch, path) for branch in one_of)
        if matches != 1:
            problems.append(f"{path} must match exactly one allowed schema")

    excluded = schema.get("not")
    if isinstance(excluded, Mapping) and not _schema_problems(value, excluded, path):
        problems.append(f"{path} matches a forbidden schema")

    expected = schema.get("type")
    expected_types = expected if isinstance(expected, list) else [expected]
    expected_types = [item for item in expected_types if isinstance(item, str)]
    if expected_types and not any(_type_matches(value, item) for item in expected_types):
        return [f"{path} must be {' or '.join(expected_types)}"]

    enum = schema.get("enum")
    if isinstance(enum, list) and not _enum_contains(enum, value):
        problems.append(f"{path} is not in allowed enum")
    if "const" in schema and not _enum_contains([schema.get("const")], value):
        problems.append(f"{path} does not match const")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            problems.append(f"{path} is below minimum {minimum}")
        if isinstance(maximum, (int, float)) and value > maximum:
            problems.append(f"{path} is above maximum {maximum}")

    if isinstance(value, str):
        minimum = schema.get("minLength")
        maximum = schema.get("maxLength")
        if isinstance(minimum, int) and len(value) < minimum:
            problems.append(f"{path} is shorter than minLength {minimum}")
        if isinstance(maximum, int) and len(value) > maximum:
            problems.append(f"{path} is longer than maxLength {maximum}")

    if isinstance(value, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if isinstance(minimum, int) and len(value) < minimum:
            problems.append(f"{path} has fewer than minItems {minimum}")
        if isinstance(maximum, int) and len(value) > maximum:
            problems.append(f"{path} has more than maxItems {maximum}")
        if schema.get("uniqueItems") is True:
            for index, item in enumerate(value):
                if any(_enum_contains([prior], item) for prior in value[:index]):
                    problems.append(f"{path} items must be unique")
                    break
        items = schema.get("items")
        if isinstance(items, Mapping):
            for index, item in enumerate(value):
                problems.extend(_schema_problems(item, items, f"{path}[{index}]"))
        contains = schema.get("contains")
        if isinstance(contains, Mapping):
            matches = sum(
                not _schema_problems(item, contains, f"{path}[{index}]")
                for index, item in enumerate(value)
            )
            minimum_contains = schema.get("minContains", 1)
            maximum_contains = schema.get("maxContains")
            if isinstance(minimum_contains, int) and matches < minimum_contains:
                problems.append(
                    f"{path} has fewer than minContains {minimum_contains} matches"
                )
            if isinstance(maximum_contains, int) and matches > maximum_contains:
                problems.append(
                    f"{path} has more than maxContains {maximum_contains} matches"
                )

    if isinstance(value, Mapping):
        minimum = schema.get("minProperties")
        maximum = schema.get("maxProperties")
        if isinstance(minimum, int) and len(value) < minimum:
            problems.append(f"{path} has fewer than minProperties {minimum}")
        if isinstance(maximum, int) and len(value) > maximum:
            problems.append(f"{path} has more than maxProperties {maximum}")
        required = schema.get("required")
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in value:
                    problems.append(f"{path}.{key} is required")
        properties = schema.get("properties")
        properties = properties if isinstance(properties, Mapping) else {}
        for key, item in value.items():
            child_schema = properties.get(key)
            if isinstance(child_schema, Mapping):
                problems.extend(_schema_problems(item, child_schema, f"{path}.{key}"))
                continue
            additional = schema.get("additionalProperties")
            if additional is False:
                problems.append(f"{path}.{key} is not allowed")
            elif isinstance(additional, Mapping):
                problems.extend(_schema_problems(item, additional, f"{path}.{key}"))
    return problems


def _canonical_enum_string(value: object, schema: Mapping) -> object:
    """Return the sole case-insensitive string enum match, when unambiguous.

    Exact values are already canonical and remain untouched.  Distinct enum
    spellings that case-fold to the same input are deliberately ambiguous: the
    caller keeps the original value and ordinary validation decides whether it
    is legal.  This never coerces numbers, booleans, whitespace, or free text.
    """

    if not isinstance(value, str):
        return value
    enum = schema.get("enum")
    if not isinstance(enum, list) or _enum_contains(enum, value):
        return value
    matches: list[str] = []
    folded = value.casefold()
    for candidate in enum:
        if not isinstance(candidate, str) or candidate.casefold() != folded:
            continue
        if candidate not in matches:
            matches.append(candidate)
    return matches[0] if len(matches) == 1 else value


def _canonicalize_schema_value(value: object, schema: Mapping) -> object:
    """Canonicalize only values whose current schema proves one exact spelling."""

    canonical = _canonical_enum_string(copy.deepcopy(value), schema)

    if isinstance(canonical, Mapping):
        properties = schema.get("properties")
        properties = properties if isinstance(properties, Mapping) else {}
        normalized = copy.deepcopy(dict(canonical))
        for key, item in canonical.items():
            child_schema = properties.get(key)
            if isinstance(child_schema, Mapping):
                normalized[key] = _canonicalize_schema_value(item, child_schema)
        canonical = normalized
    elif isinstance(canonical, list):
        items = schema.get("items")
        if isinstance(items, Mapping):
            canonical = [
                _canonicalize_schema_value(item, items)
                for item in canonical
            ]

    # Combinator branches may carry the only property schemas.  Try every
    # branch on a detached value, then adopt a result only when exactly one
    # branch becomes schema-valid.  Overlapping or otherwise ambiguous branches
    # remain untouched so canonicalization can never choose semantics.
    for keyword in ("oneOf", "anyOf"):
        branches = [
            branch
            for branch in (schema.get(keyword) or [])
            if isinstance(branch, Mapping)
        ]
        if not branches:
            continue
        valid_candidates = []
        for branch in branches:
            candidate = _canonicalize_schema_value(canonical, branch)
            if not _schema_problems(candidate, branch, "value"):
                valid_candidates.append(candidate)
        if len(valid_candidates) == 1:
            canonical = valid_candidates[0]
    return canonical


def canonicalize_action_payload(
    move: object,
    context_or_actions: object,
) -> object:
    """Return a detached move with unambiguous schema enum spellings restored.

    The server-authored ``params_schema`` is the sole source of canonical
    values.  Unknown actions, malformed moves, and actions without a schema are
    copied unchanged; callers still run ``validate_action_payload`` afterward.
    """

    if not isinstance(move, Mapping):
        return copy.deepcopy(move)
    normalized = copy.deepcopy(dict(move))
    action = str(move.get("action") or "").strip()
    params = move.get("params")
    actions = _actions_from_contract(context_or_actions)
    if not action or not isinstance(params, Mapping) or actions is None:
        return normalized
    entry = next((item for item in actions if item.get("action") == action), None)
    schema = entry.get("params_schema") if isinstance(entry, Mapping) else None
    if isinstance(schema, Mapping):
        normalized["params"] = _canonicalize_schema_value(params, schema)
    return normalized


def validate_action_payload(move: object, context_or_actions: object) -> list[str]:
    """Validate one move against the v2 action schema JSON subset."""
    if not isinstance(move, Mapping):
        return ["move must be an object"]
    action = str(move.get("action") or "").strip()
    if not action:
        return ["action is required"]
    actions = _actions_from_contract(context_or_actions)
    if actions is None:
        return ["legal action contract is unavailable"]
    entry = next((item for item in actions if item.get("action") == action), None)
    if entry is None:
        return ["action is not currently legal"]
    params = move.get("params")
    if not isinstance(params, Mapping):
        return ["params must be an object"]
    schema = entry.get("params_schema")
    if not isinstance(schema, Mapping):
        return []
    return _schema_problems(params, schema, "params")


def prune_optional_violations(move: object, context_or_actions: object) -> tuple[object, list[str]]:
    """Drop or trim OPTIONAL params that fail the schema; keep the move.

    Optional metadata must not be able to cancel a game action. A press batch
    carries `strategy_intent`, an optional private object the server uses for
    planner hinting and that changes nothing about the messages being sent --
    and one over-long array inside it was discarding the whole batch. Measured
    on Claw Diplomacy match 1448: `strategy_intent.avoid_provinces` with nine
    entries against a cap of eight, 37 times, and one power spent all 40
    negotiation rounds silent because of it.

    Only fields the contract itself marks optional are touched: `required` is
    read from the schema, never guessed. A list over `maxItems` is TRIMMED
    rather than dropped, because the first N entries are still the model's
    intent. Anything required, and anything still invalid after pruning, is
    left alone for the caller to reject as before.

    Returns (pruned_move, notes). notes is empty when nothing was changed.
    """

    if not isinstance(move, Mapping):
        return move, []
    actions = _actions_from_contract(context_or_actions)
    if actions is None:
        return move, []
    action = str(move.get("action") or "").strip()
    entry = next((item for item in actions if item.get("action") == action), None)
    params = move.get("params")
    if entry is None or not isinstance(params, Mapping):
        return move, []
    schema = entry.get("params_schema")
    if not isinstance(schema, Mapping):
        return move, []

    notes: list[str] = []
    pruned = _prune_value(
        copy.deepcopy(dict(params)), schema, "params", notes, inside_content=False,
    )
    if not notes:
        return move, []
    repaired = dict(move)
    repaired["params"] = pruned
    return repaired, notes


def _carries_the_action(value: object) -> bool:
    """True when this value is the move's content rather than metadata about it."""
    return isinstance(value, list) and bool(value)


def _prune_value(
    value: object,
    schema: Mapping,
    path: str,
    notes: list[str],
    *,
    inside_content: bool,
) -> object:
    """Trim what is over-long; drop only optional metadata OUTSIDE the content.

    ``inside_content`` restricts what may be removed once the walk enters a
    list. The items of an order bundle or a press batch are the move itself, so
    a RECOGNISED field is never altered there -- silently turning
    {"type": "HOLD"} into {} because an enum did not match submits something the
    model never chose, which is worse than the rejection this salvage exists to
    avoid.

    A key the schema does not recognise at all is the exception, and it is not
    the same thing: `additionalProperties: false` says that key is no part of
    the action, so removing it cannot change what the move does. Live case:
    models put `strategy_intent` inside each press message instead of beside
    them, and the batch -- to_power, content and all -- was thrown away for a
    misfiled hint.
    """

    if not isinstance(schema, Mapping):
        return value

    if isinstance(value, list):
        maximum = schema.get("maxItems")
        if isinstance(maximum, int) and len(value) > maximum:
            notes.append(f"{path} trimmed {len(value)} -> {maximum}")
            value = value[:maximum]
        item_schema = schema.get("items")
        if isinstance(item_schema, Mapping):
            value = [
                _prune_value(
                    item, item_schema, f"{path}[{index}]", notes,
                    inside_content=True,
                )
                for index, item in enumerate(value)
            ]
        return value

    if isinstance(value, Mapping):
        properties = schema.get("properties")
        required = set(schema.get("required") or [])
        if not isinstance(properties, Mapping):
            return value
        result = dict(value)
        for key in list(result):
            sub_schema = properties.get(key)
            if not isinstance(sub_schema, Mapping):
                # Unknown to the schema. When the contract closes the object,
                # the key is not part of the action and can go; otherwise the
                # contract allows it and it stays.
                if schema.get("additionalProperties") is False:
                    notes.append(f"{path}.{key} dropped (not in the contract)")
                    result.pop(key, None)
                continue
            child_path = f"{path}.{key}"
            result[key] = _prune_value(
                result[key], sub_schema, child_path, notes,
                inside_content=inside_content,
            )
            if inside_content or key in required or _carries_the_action(result[key]):
                # `required` is not enough on its own: these contracts express
                # "orders OR candidate_id OR use_server_default" with oneOf, so
                # `orders` -- the entire content of a movement turn -- is absent
                # from the top-level required list and a naive rule dropped it.
                # A move stripped of its orders still validates and does
                # nothing, which is worse than the rejection this is meant to
                # avoid. So a non-empty list is never dropped: in this contract
                # family the lists ARE the action (orders, messages) and the
                # objects beside them are the hints.
                continue
            if _schema_problems(result[key], sub_schema, child_path):
                # Optional, carries no action, and still wrong after trimming.
                notes.append(f"{child_path} dropped")
                result.pop(key, None)
        return result

    return value


def executable_fallback(
    context: object,
    legal_actions: list[dict] | None = None,
) -> dict | None:
    """Return a detached current, schema-valid server fallback when available."""
    normalized = normalize_decision_context(context)
    if normalized is None:
        return None
    fallback = normalized.get("fallback")
    if not isinstance(fallback, Mapping):
        return None
    action = str(fallback.get("action") or "").strip()
    # Poll response pruning removes an explicitly empty params object. Treat an
    # absent value as that wire-equivalent empty object, then let the action
    # schema reject it when parameters are actually required.
    params = fallback.get("params", {})
    if not action or not isinstance(params, Mapping):
        return None
    current_actions = _legal_actions(
        legal_actions
        if legal_actions is not None
        else normalized["turn"]["legal_actions"]
    )
    if current_actions is None or action not in {
        item.get("action") for item in current_actions
    }:
        return None
    candidate = {"action": action, "params": copy.deepcopy(dict(params))}
    if validate_action_payload(candidate, normalized):
        return None
    return candidate

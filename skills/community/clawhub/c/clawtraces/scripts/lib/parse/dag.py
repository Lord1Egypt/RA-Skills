# FILE_META
# INPUT:  .jsonl session file (OpenClaw DAG format)
# OUTPUT: ordered list of message nodes (final conversation chain)
# POS:    skill lib — called by the openclaw adapter
# MISSION: Parse DAG structure and extract final conversation chain via parent-id traceback.

"""DAG traversal for OpenClaw .jsonl session logs.

OpenClaw logs are append-only JSONL where nodes form a DAG via id + parentId.
To extract the final conversation, trace back from the last message node to root.
"""

from __future__ import annotations

import json
import sys
from typing import Optional

from .metadata_stripper import is_system_startup_message, strip_metadata_prefix


# Gateway-internal placeholder names that OpenClaw stamps on certain frames
# (e.g. the first assistant message from a mirror/warm-up path). They are not
# real models — the session's real model appears on the other assistant
# messages — so every code path that treats `msg.model` as "the model that
# ran this turn" should skip them.
GATEWAY_PLACEHOLDER_MODELS: frozenset[str] = frozenset({"delivery-mirror"})


def detect_file_encoding(file_path: str, sample_bytes: int = 64 * 1024) -> str:
    """Detect file encoding by sampling the head of the file.

    On Chinese Windows, OpenClaw may write .jsonl files in GBK encoding.
    Reading GBK as UTF-8 with errors='replace' destroys Chinese text
    irreversibly (replaces bytes with U+FFFD). Instead, we probe the
    actual encoding and read with the correct one.

    Only a head sample (default 64KB) is read to avoid OOM on huge files
    like cache-trace.jsonl on low-memory hosts. For multibyte-safe probing,
    we use an incremental decoder so a UTF-8 code point cut in half at the
    sample boundary does not cause a false negative.
    """
    import codecs

    with open(file_path, "rb") as f:
        raw = f.read(sample_bytes)

    if not raw:
        return "utf-8"

    utf8_decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    try:
        utf8_decoder.decode(raw, final=False)
        return "utf-8"
    except UnicodeDecodeError:
        pass

    gbk_decoder = codecs.getincrementaldecoder("gbk")(errors="strict")
    try:
        gbk_decoder.decode(raw, final=False)
        return "gbk"
    except UnicodeDecodeError:
        pass

    return "utf-8"  # fallback, will use errors="replace"


def parse_jsonl(file_path: str) -> list[dict]:
    """Parse a .jsonl file into a list of JSON objects.

    Detects encoding automatically (UTF-8 or GBK) to avoid destroying
    Chinese text on Windows systems where files may be GBK-encoded.
    Skips lines with invalid JSON.
    """
    encoding = detect_file_encoding(file_path)
    nodes = []
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                nodes.append(json.loads(line))
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"Warning: skipped invalid JSON at {file_path}:{line_num}", file=sys.stderr)
    return nodes


def extract_conversation_chain(nodes: list[dict]) -> list[dict]:
    """Extract the final conversation chain by tracing back from the last message node.

    Handles compaction events: if the chain crosses a compaction boundary,
    the compaction summary is preserved and messages after the boundary are returned.

    Returns a chronologically ordered list of nodes. If a compaction was encountered,
    the compaction node (with its summary) is included at the beginning of the list,
    followed by message nodes from the boundary onward.
    """
    # Build id -> node index
    index: dict[str, dict] = {}
    for node in nodes:
        node_id = node.get("id")
        if node_id:
            index[node_id] = node

    # Find the last message node
    last_message: Optional[dict] = None
    for node in reversed(nodes):
        if node.get("type") == "message":
            last_message = node
            break

    if last_message is None:
        return []

    # Trace back to root
    chain = []
    current = last_message
    visited = set()
    compaction_node = None
    compaction_boundary = None  # id of the first kept entry after compaction

    while current is not None:
        node_id = current.get("id")
        if node_id in visited:
            break  # cycle protection
        visited.add(node_id)
        chain.append(current)

        # Detect compaction events in the chain
        if current.get("type") == "compaction":
            compaction_node = current
            first_kept = current.get("firstKeptEntryId")
            if first_kept:
                compaction_boundary = first_kept
            break  # stop tracing beyond compaction

        parent_id = current.get("parentId")
        if parent_id is None:
            break
        current = index.get(parent_id)

    # Reverse to chronological order
    chain.reverse()

    # If we hit a compaction boundary, keep compaction node + messages from boundary onward
    if compaction_boundary:
        filtered = []
        past_boundary = False
        for node in chain:
            if node.get("id") == compaction_boundary:
                past_boundary = True
            if past_boundary:
                filtered.append(node)
        chain = filtered if filtered else chain

    # Filter to message nodes + compaction node (if present)
    result = []
    if compaction_node and compaction_node.get("summary"):
        result.append(compaction_node)
    result.extend(node for node in chain if node.get("type") == "message")

    return result


def extract_richest_segment(
    nodes: list[dict],
) -> tuple[list[dict], Optional[dict]]:
    """Split a multi-compaction session by compaction boundaries and return the
    single richest segment's DAG chain (plus the compaction node immediately
    before it, if any).

    OpenClaw compacts context when it fills up, so a heavily-used session is
    split into several "context eras" separated by compaction nodes. The last
    era can be as small as one short follow-up ("继续"), even when earlier eras
    contain the actual task. `extract_conversation_chain` only returns the last
    era's tail and loses the rest.

    This function:
      1. Walks the file in order and splits nodes into segments separated by
         `type=compaction` nodes (with a non-empty `summary`).
      2. For each segment, runs a bounded DAG walk from the segment's last
         message backward via `parentId`, stopping when the parent leaves the
         segment (which means it hit the prior compaction boundary).
      3. Scores each segment by user content: (long_msg_count, total_chars,
         msg_count), all computed after metadata stripping.
      4. Returns the chain of the highest-scoring segment and the compaction
         node that immediately precedes it (for context-from-prior injection).

    The caller should prepend the returned compaction node (if not None) to
    the chain before passing to the converter — the converter's existing
    compaction-summary injection path (`converter.py:224-237`) handles it.
    """
    # id -> node index for DAG walks
    index: dict[str, dict] = {}
    for node in nodes:
        nid = node.get("id")
        if nid:
            index[nid] = node

    # Pass 1: split into segments separated by compaction nodes.
    # A segment is (prior_compaction_node_or_None, set_of_ids_in_segment,
    # last_message_node_in_segment).
    #
    # seg_ids must include ALL non-compaction node ids in the segment (not just
    # messages), because the parentId chain can pass through intermediate
    # non-message nodes like `thinking`, `model_change`, `custom`, etc. If we
    # only put message ids in the set, the walk breaks prematurely when it hits
    # one of these intermediate nodes. We filter to actual messages only at the
    # very end of walk_segment via `n.get("type") == "message"`.
    segments: list[tuple[Optional[dict], set[str], Optional[dict]]] = []
    current_ids: set[str] = set()
    current_last: Optional[dict] = None
    prior_comp: Optional[dict] = None

    for node in nodes:
        ntype = node.get("type")
        if ntype == "compaction":
            if node.get("summary") is None or node.get("summary") == "":
                # Ignore empty/placeholder compactions
                continue
            # Close current segment
            if current_last is not None:
                segments.append((prior_comp, current_ids, current_last))
            # Start new segment
            current_ids = set()
            current_last = None
            prior_comp = node
            continue
        # All non-compaction nodes with an id are tracked so the DAG walk can
        # transparently pass through thinking / model_change / custom nodes.
        nid = node.get("id")
        if nid:
            current_ids.add(nid)
        if ntype == "message" and nid:
            current_last = node

    if current_last is not None:
        segments.append((prior_comp, current_ids, current_last))

    if not segments:
        return [], None

    def walk_segment(seg_ids: set[str], last_msg: dict) -> list[dict]:
        """Walk parentId backward from last_msg, staying inside seg_ids."""
        chain: list[dict] = []
        visited: set[str] = set()
        current: Optional[dict] = last_msg
        while current is not None:
            cid = current.get("id")
            if not cid or cid in visited:
                break
            visited.add(cid)
            if cid not in seg_ids:
                break
            chain.append(current)
            pid = current.get("parentId")
            if pid is None:
                break
            current = index.get(pid)
        chain.reverse()
        return [n for n in chain if n.get("type") == "message"]

    def score_chain(chain: list[dict]) -> tuple[int, int, int]:
        long_count = 0
        total_chars = 0
        msg_count = 0
        for node in chain:
            msg = node.get("message", {})
            if msg.get("role") != "user":
                continue
            for block in msg.get("content", []):
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue
                raw = block.get("text", "")
                if is_system_startup_message(raw):
                    continue
                cleaned = strip_metadata_prefix(raw)
                if not cleaned:
                    continue
                msg_count += 1
                total_chars += len(cleaned)
                if len(cleaned) > 10:
                    long_count += 1
        return (long_count, total_chars, msg_count)

    best_chain: list[dict] = []
    best_prior: Optional[dict] = None
    best_score: tuple[int, int, int] = (-1, -1, -1)

    for seg_prior, seg_ids, seg_last in segments:
        chain = walk_segment(seg_ids, seg_last)
        if not chain:
            continue
        s = score_chain(chain)
        if s > best_score:
            best_score = s
            best_chain = chain
            best_prior = seg_prior

    return best_chain, best_prior


def extract_all_segments(
    nodes: list[dict],
) -> list[tuple[Optional[dict], list[dict]]]:
    """Split a session into per-era segments and walk each era's DAG chain.

    v2 §4.2 ⑤.1-⑤.3: every compaction event divides the session into eras.
    Unlike ``extract_richest_segment`` (which keeps only the highest-scoring
    era), v2 concatenates all eras with a ``[COMPACTION_BOUNDARY]`` marker
    between them — so we need every segment.

    Returns a chronologically ordered list of
    ``(prior_compaction_node_or_None, message_chain)`` tuples:

      * ``prior_compaction_node``: the compaction node whose summary ended
        the previous era (``None`` for the first era — nothing precedes it).
        Caller renders it as a ``[COMPACTION_BOUNDARY] <summary>`` user
        message between era chains.
      * ``message_chain``: the era's message nodes in chronological order,
        recovered by a bounded ``parentId`` walk from the era's last
        message backward until the walk leaves the era's id set.

    A session without compaction returns a single-element list with
    ``prior=None`` and the full DAG chain — equivalent to
    ``extract_conversation_chain`` in that case.
    """
    index: dict[str, dict] = {}
    for node in nodes:
        nid = node.get("id")
        if nid:
            index[nid] = node

    # Pass 1: partition nodes into segments separated by compaction events.
    # Intermediate non-message nodes (thinking / model_change / custom) must be
    # in the id set so parentId walks can pass through them — filter to
    # actual message nodes only at the end of walk_segment.
    segments_raw: list[tuple[Optional[dict], set[str], Optional[dict]]] = []
    current_ids: set[str] = set()
    current_last: Optional[dict] = None
    prior_comp: Optional[dict] = None

    for node in nodes:
        ntype = node.get("type")
        if ntype == "compaction":
            if not node.get("summary"):
                continue
            if current_last is not None:
                segments_raw.append((prior_comp, current_ids, current_last))
            current_ids = set()
            current_last = None
            prior_comp = node
            continue
        nid = node.get("id")
        if nid:
            current_ids.add(nid)
        if ntype == "message" and nid:
            current_last = node

    if current_last is not None:
        segments_raw.append((prior_comp, current_ids, current_last))

    def walk_segment(seg_ids: set[str], last_msg: dict) -> list[dict]:
        chain: list[dict] = []
        visited: set[str] = set()
        current: Optional[dict] = last_msg
        while current is not None:
            cid = current.get("id")
            if not cid or cid in visited:
                break
            visited.add(cid)
            if cid not in seg_ids:
                break
            chain.append(current)
            pid = current.get("parentId")
            if pid is None:
                break
            current = index.get(pid)
        chain.reverse()
        return [n for n in chain if n.get("type") == "message"]

    result: list[tuple[Optional[dict], list[dict]]] = []
    for seg_prior, seg_ids, seg_last in segments_raw:
        chain = walk_segment(seg_ids, seg_last)
        result.append((seg_prior, chain))
    return result


def count_turns(messages: list[dict]) -> int:
    """Count conversation turns. One turn = one assistant reply (including tool calls).

    Each assistant message represents one model inference, so tool-call rounds
    are counted as turns rather than being ignored.

    Skips compaction nodes (type="compaction") that may be in the list.
    """
    count = 0
    for msg in messages:
        if msg.get("type") == "compaction":
            continue
        role = msg.get("message", {}).get("role")
        if role == "assistant":
            count += 1
    return count


def get_model_from_nodes(nodes: list[dict]) -> Optional[str]:
    """Extract model ID from the first few nodes (model_change event).

    Only returns values that pass is_allowed_model() to avoid picking up
    gateway-internal names like 'delivery-mirror'.
    """
    from .session_index import is_allowed_model

    for node in nodes[:10]:
        if node.get("type") == "model_change":
            mid = node.get("modelId")
            if mid and is_allowed_model(mid):
                return mid
        # Also check assistant messages for model info
        if node.get("type") == "message":
            model = node.get("message", {}).get("model")
            if model and is_allowed_model(model):
                return model
    return None


def get_raw_model_from_nodes(nodes: list[dict]) -> Optional[str]:
    """Extract the first model ID from nodes without whitelist filtering.

    Why: the list UI needs to show the real model name even for sessions
    rejected by the whitelist — displaying "unknown" when the session
    clearly ran on a known-but-non-whitelisted model (e.g. a newer Claude
    that hasn't been added to ALLOWED_MODEL_PATTERNS yet) loses the one
    piece of info the user needs to understand why it was rejected.

    Gateway placeholder names (GATEWAY_PLACEHOLDER_MODELS) are skipped so
    the UI doesn't surface e.g. 'delivery-mirror' when the session actually
    ran on gpt-5.4 further down.
    """
    for node in nodes[:10]:
        if node.get("type") == "model_change":
            mid = node.get("modelId")
            if mid and mid not in GATEWAY_PLACEHOLDER_MODELS:
                return mid
        if node.get("type") == "message":
            model = node.get("message", {}).get("model")
            if model and model not in GATEWAY_PLACEHOLDER_MODELS:
                return model
    return None


def check_session_models(
    nodes: list[dict],
    whitelist: list[str],
) -> tuple[bool, list[str]]:
    """v2 session-level model check (v2 §4.2 ②).

    Scan every ``type="message", role="assistant"`` node in the session and
    verify its ``msg.model`` is covered by ``whitelist``. Returns
    ``(ok, non_allowed_models)``:

      * ``ok=True`` when every assistant message has a whitelisted model (or
        no recorded model at all — absence is tolerated because some gateway
        replays omit the field).
      * ``non_allowed_models`` is a de-duplicated list of the offending
        model strings in **first-seen order**; empty when ``ok=True``.
        Order matters: the list UI surfaces ``bad[0]`` as the displayed
        model so the user sees the first non-whitelisted model the session
        actually ran on (not an alphabetically-sorted choice).

    Any non-allowed model anywhere in the session hard-rejects the whole
    thing — v2 forbids mid-session model switches, and this is the choke
    point that prevents per-message skip logic from re-growing in the
    converter.
    """
    from ..core.config_loader import is_allowed_model

    bad: dict[str, None] = {}
    for node in nodes:
        if node.get("type") != "message":
            continue
        msg = node.get("message", {})
        if msg.get("role") != "assistant":
            continue
        model = msg.get("model", "") or ""
        if not model:
            continue
        if model in GATEWAY_PLACEHOLDER_MODELS:
            continue
        if not is_allowed_model(model, whitelist):
            bad.setdefault(model, None)
    return (not bad, list(bad))

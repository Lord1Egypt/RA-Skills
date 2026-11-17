"""Topological workflow executor with conditional routing, iteration/loop
subgraph execution, and streaming answer support.

Engine file — copy as-is from the skill template; do NOT edit per project.
Business logic lives in definition.py (data) and blocks/ (handlers).

Definition format extensions:
- nodes[id]["parent"]: marks a node as belonging to an iteration/loop body
  (from the DSL's parentId). Engine runs such nodes only inside the parent's
  subgraph execution, never in the main flow.
- iteration configs: iterator_selector, output_selector, is_parallel,
  parallel_nums. Parallel iteration is degraded to sequential execution
  (declared degradation: keeps external-call concurrency at 1).
- loop configs: loop_variables, break_conditions, loop_count.
"""
from __future__ import annotations

import operator
from collections import defaultdict
from typing import Any, Callable, Iterator

from .context import VariablePool

BRANCH_TYPES = {"if-else", "question-classifier"}
TERMINAL_TYPES = {"end", "answer"}
# node types the engine executes natively; everything else needs a handler
ENGINE_TYPES = {"start", "if-else", "question-classifier", "end", "answer",
                "iteration", "loop", "iteration-start", "loop-start"}

_OPS = {
    "contains": lambda a, b: str(b) in str(a),
    "not contains": lambda a, b: str(b) not in str(a),
    "start with": lambda a, b: str(a).startswith(str(b)),
    "end with": lambda a, b: str(a).endswith(str(b)),
    "is": lambda a, b: str(a) == str(b),
    "is not": lambda a, b: str(a) != str(b),
    "empty": lambda a, b: not a,
    "not empty": lambda a, b: bool(a),
    "exists": lambda a, b: a is not None,
    "not exists": lambda a, b: a is None,
    "null": lambda a, b: a is None,
    "not null": lambda a, b: a is not None,
    "=": operator.eq,
    "≠": operator.ne,
    ">": lambda a, b: float(a) > float(b),
    "<": lambda a, b: float(a) < float(b),
    "≥": lambda a, b: float(a) >= float(b),
    "≤": lambda a, b: float(a) <= float(b),
    ">=": lambda a, b: float(a) >= float(b),
    "<=": lambda a, b: float(a) <= float(b),
    "in": lambda a, b: str(a) in str(b).split(","),
    "not in": lambda a, b: str(a) not in str(b).split(","),
}


def _eval_group(conds: list[dict], logical: str, pool: VariablePool) -> bool:
    results = [eval_condition(c, pool) for c in conds]
    return any(results) if (logical or "and") == "or" else all(results)


def eval_condition(cond: dict, pool: VariablePool) -> bool:
    sel = cond.get("variable_selector") or []
    actual = pool.get(sel[0], sel[1]) if len(sel) == 2 else None
    op = _OPS.get(cond.get("comparison_operator", "is"))
    if op is None:
        raise ValueError(f"unsupported operator: {cond.get('comparison_operator')}")
    return bool(op(actual, cond.get("value")))


def eval_branch(node: dict, pool: VariablePool) -> set[str]:
    """Active outgoing sourceHandles. Supports both the legacy
    `conditions` + true/false shape and the newer `cases[]` multi-branch
    shape (outgoing handles are case_ids, fallback handle is 'false')."""
    cfg = node["config"]
    if node["type"] == "question-classifier":
        # handler must have written the chosen class id to (node_id, 'class_id')
        return {str(pool.get(node["id"], "class_id", "1"))}
    cases = cfg.get("cases")
    if cases:
        for case in cases:
            conds = case.get("conditions") or []
            if not conds:  # default/else case
                continue
            if _eval_group(conds, case.get("logical_operator"), pool):
                return {str(case.get("case_id") or case.get("id") or "true")}
        return {"false"}
    conds = cfg.get("conditions") or []
    return {"true"} if _eval_group(conds, cfg.get("logical_operator"), pool) else {"false"}


class Engine:
    """Executes a definition: nodes + edges + handlers, driven by a VariablePool.

    handlers: {node_id: callable(node_id, config, pool, engine) -> None}
      - must write outputs via pool.set_many(node_id, {...})
      - question-classifier handlers must also pool.set(node_id, 'class_id', ...)
    """

    def __init__(self, definition: dict,
                 handlers: dict[str, Callable[[str, dict, VariablePool, "Engine"], None]]):
        self.nodes = definition["nodes"]          # id -> {type, config, parent?}
        self.edges = definition["edges"]          # [{source, target, handle}]
        self.start_id = definition["start_id"]
        self.handlers = handlers
        self._out = defaultdict(list)
        for e in self.edges:
            self._out[e["source"]].append(e)
        self._children = defaultdict(list)        # iteration/loop id -> inner ids
        for nid, n in self.nodes.items():
            if n.get("parent"):
                self._children[n["parent"]].append(nid)
        self.pool = VariablePool()
        self.outputs: dict[str, Any] = {}
        self.answers: list[str] = []              # every answer segment, in order

    # ---- public API ----

    def run(self, inputs: dict[str, Any]) -> dict[str, Any]:
        for _event, _payload in self.run_stream(inputs):
            pass
        return self.outputs

    def run_stream(self, inputs: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Yields ('answer', text) for each answer node as it executes,
        then ('final', outputs) once the run completes."""
        self.pool.set_many(self.start_id, inputs)
        yield from self._execute(self.start_id, scope=None)
        if self.answers:
            self.outputs.setdefault("answer", "".join(self.answers))
        yield ("final", self.outputs)

    # ---- internals ----

    def _execute(self, entry_id: str, scope: set[str] | None) -> Iterator[tuple[str, Any]]:
        queue = [entry_id]
        executed = set()
        while queue:
            nid = queue.pop(0)
            if nid in executed or nid not in self.nodes:
                continue
            if scope is not None and nid not in scope:
                continue
            executed.add(nid)
            node = self.nodes[nid]
            ntype = node["type"]

            if ntype in ("start", "iteration-start", "loop-start"):
                active = None
            elif ntype in BRANCH_TYPES:
                if ntype == "question-classifier" and nid in self.handlers:
                    self.handlers[nid](nid, node["config"], self.pool, self)
                active = eval_branch(node, self.pool)
            elif ntype == "answer":
                text = self.pool.resolve(node["config"].get("answer", ""))
                self.answers.append(text)
                yield ("answer", text)
                active = None
            elif ntype == "end":
                self._collect_end(node)
                active = None
            elif ntype == "iteration":
                self._run_iteration(nid, node)
                active = None
            elif ntype == "loop":
                yield from self._run_loop(nid, node)
                active = None
            else:
                handler = self.handlers.get(nid)
                if handler is None:
                    raise NotImplementedError(
                        f"no handler registered for node {nid} ({ntype}); "
                        f"implement it in app/workflow/blocks/")
                handler(nid, node["config"], self.pool, self)
                active = None

            for e in self._out.get(nid, []):
                if scope is not None and e["target"] not in scope:
                    continue
                if active is None or str(e.get("handle")) in active:
                    queue.append(e["target"])

    def _collect_end(self, node: dict) -> None:
        for out in node["config"].get("outputs") or []:
            sel = out.get("value_selector") or []
            if len(sel) == 2:
                self.outputs[out["variable"]] = self.pool.get(sel[0], sel[1])

    def _inner_scope(self, parent_id: str) -> set[str]:
        return set(self._children.get(parent_id, []))

    def _run_iteration(self, nid: str, node: dict) -> None:
        cfg = node["config"]
        sel = cfg.get("iterator_selector") or []
        items = self.pool.get(sel[0], sel[1]) if len(sel) == 2 else None
        if not isinstance(items, list):
            raise ValueError(f"iteration {nid}: selector {sel} did not resolve to a list")
        scope = self._inner_scope(nid)
        entry = f"{nid}start" if f"{nid}start" in scope else None
        out_sel = cfg.get("output_selector") or []
        results = []
        for i, item in enumerate(items):
            self.pool.set(nid, "item", item)
            self.pool.set(nid, "index", i)
            if entry and scope:
                for _ in self._execute(entry, scope):
                    pass  # answer segments inside iteration are not streamed
            results.append(self.pool.get(out_sel[0], out_sel[1])
                           if len(out_sel) == 2 else None)
        self.pool.set(nid, "output", results)

    def _run_loop(self, nid: str, node: dict) -> Iterator[tuple[str, Any]]:
        cfg = node["config"]
        for var in cfg.get("loop_variables") or []:
            sel = var.get("value_selector") or []
            if len(sel) == 2:
                self.pool.set(nid, var.get("label") or var.get("variable", "var"),
                              self.pool.get(sel[0], sel[1]))
        scope = self._inner_scope(nid)
        entry = f"{nid}start" if f"{nid}start" in scope else None
        max_count = int(cfg.get("loop_count") or 10)
        for _ in range(max_count):
            if entry and scope:
                yield from self._execute(entry, scope)
            conds = cfg.get("break_conditions") or []
            if conds and _eval_group(conds, cfg.get("logical_operator"), self.pool):
                break

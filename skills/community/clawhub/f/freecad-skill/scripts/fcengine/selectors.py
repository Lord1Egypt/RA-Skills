"""Edge/face selectors (a small, CadQuery-inspired language).

Selectors are evaluated against *descriptors*: plain dicts produced by
``geometry.describe_faces`` / ``geometry.describe_edges`` (the same data
``inspect`` returns), so this module is pure Python.

Grammar::

    expr    := and ('or' and)*
    and     := unary ('and' unary)*
    unary   := 'not' unary | primary
    primary := '(' expr ')' | 'face(' expr ')' | term
    term    := '>X' | '<X' | '|X' | '#X' | '+X' | '-X'   (X, Y or Z)
             | '%TYPE'            (LINE, CIRCLE, PLANE, CYLINDER, ...)
             | 'r<N' | 'r>N' | 'r=N'
             | 'all'

Semantics (each term is evaluated against the full element list; and/or/not
combine the resulting sets):

* ``>Z`` / ``<Z``: elements whose centre has the maximum / minimum Z.
* ``|Z``: line edges parallel to Z; planar faces whose normal is parallel to Z.
* ``#Z``: line edges / planar face normals perpendicular to Z.
* ``+Z`` / ``-Z``: planar faces whose outward normal points along +Z / -Z.
* ``%CIRCLE``: elements of that geometry type.
* ``r<5``: circular edges / cylindrical, spherical faces with radius < 5.
* ``face(>Z)``: (edges only) edges bounding any face matched by the inner selector.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

Descriptor = Dict[str, Any]
SelectorValue = Union[str, int, Sequence[int]]

AXES = {"X": 0, "Y": 1, "Z": 2}
TYPES = ("LINE", "CIRCLE", "ELLIPSE", "BSPLINE", "BEZIER", "PLANE", "CYLINDER", "CONE", "SPHERE", "TORUS", "OTHER")

_TOKEN = re.compile(
    r"\s*(?:"
    r"(?P<lp>\()|(?P<rp>\))|(?P<face>face\()"
    r"|(?P<kw>and\b|or\b|not\b|all\b)"
    r"|(?P<dir>[<>|#+\-][XYZ])\b"
    r"|(?P<type>%[A-Za-z]+)"
    r"|(?P<rad>r\s*(?P<cmp>[<>=])\s*(?P<num>-?\d+(?:\.\d+)?))"
    r")"
)


class SelectorError(ValueError):
    pass


# ------------------------------------------------------------------ parsing

Node = Tuple[Any, ...]


def _tokenize(text: str) -> List[Tuple[str, str]]:
    tokens: List[Tuple[str, str]] = []
    pos = 0
    text = text.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise SelectorError(f"Unexpected text at position {pos}: {text[pos : pos + 10]!r}")
        pos = m.end()
        kind = m.lastgroup
        if kind in ("cmp", "num"):
            kind = "rad"
        if m.group("rad"):
            tokens.append(("rad", m.group("cmp") + m.group("num")))
        elif m.group("type"):
            t = m.group("type")[1:].upper()
            if t not in TYPES:
                raise SelectorError(f"Unknown type %{t}. Known: {', '.join('%' + x for x in TYPES)}")
            tokens.append(("type", t))
        else:
            tokens.append((kind or "", m.group(kind or 0).strip()))
        while pos < len(text) and text[pos].isspace():
            pos += 1
    return tokens


class _Parser:
    def __init__(self, tokens: List[Tuple[str, str]]) -> None:
        self.t = tokens
        self.i = 0

    def peek(self) -> Optional[Tuple[str, str]]:
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self) -> Tuple[str, str]:
        tok = self.peek()
        if tok is None:
            raise SelectorError("Unexpected end of selector")
        self.i += 1
        return tok

    def parse(self) -> Node:
        node = self.expr()
        if self.peek() is not None:
            raise SelectorError(f"Unexpected token {self.peek()[1]!r}")
        return node

    def expr(self) -> Node:
        node = self.and_()
        while self.peek() == ("kw", "or"):
            self.take()
            node = ("or", node, self.and_())
        return node

    def and_(self) -> Node:
        node = self.unary()
        while self.peek() == ("kw", "and"):
            self.take()
            node = ("and", node, self.unary())
        return node

    def unary(self) -> Node:
        if self.peek() == ("kw", "not"):
            self.take()
            return ("not", self.unary())
        return self.primary()

    def primary(self) -> Node:
        kind, val = self.take()
        if kind == "lp":
            node = self.expr()
            if self.take()[0] != "rp":
                raise SelectorError("Missing ')'")
            return node
        if kind == "face":
            node = self.expr()
            if self.take()[0] != "rp":
                raise SelectorError("Missing ')' after face(")
            return ("face", node)
        if kind == "kw" and val == "all":
            return ("all",)
        if kind == "dir":
            return ("dir", val[0], AXES[val[1]])
        if kind == "type":
            return ("type", val)
        if kind == "rad":
            return ("rad", val[0], float(val[1:]))
        raise SelectorError(f"Unexpected token {val!r}")


def parse(text: str) -> Node:
    """Parse a selector expression. Raises SelectorError on bad syntax."""
    if not isinstance(text, str) or not text.strip():
        raise SelectorError("Selector must be a non-empty string")
    return _Parser(_tokenize(text)).parse()


def check(value: Any) -> None:
    """Static validation of a selector value (indices or expression)."""
    if isinstance(value, bool):
        raise SelectorError("Selector cannot be a boolean")
    if isinstance(value, int):
        if value < 1:
            raise SelectorError("Indices are 1-based")
        return
    if isinstance(value, list):
        if not value:
            raise SelectorError("Index list is empty")
        for v in value:
            if isinstance(v, bool) or not isinstance(v, int) or v < 1:
                raise SelectorError("Index lists must contain 1-based integers")
        return
    if isinstance(value, str):
        parse(value)
        return
    raise SelectorError("Selector must be 'all', an index, a list of indices or an expression string")


# ------------------------------------------------------------------ evaluation

_PAR = 1e-6  # tolerance on |cos| for parallel / perpendicular


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(axis: int, sign: float = 1.0) -> Tuple[float, float, float]:
    v = [0.0, 0.0, 0.0]
    v[axis] = sign
    return (v[0], v[1], v[2])


def _dir_of(el: Descriptor) -> Optional[Sequence[float]]:
    """Direction used for parallel/perpendicular tests."""
    if el.get("kind") == "edge":
        return el.get("direction") if el.get("type") == "line" else None
    return el.get("normal") if el.get("type") == "plane" else None


class _Eval:
    def __init__(
        self,
        elements: List[Descriptor],
        faces: Optional[List[Descriptor]],
        edge_faces: Optional[Callable[[], Dict[int, List[int]]]],
    ) -> None:
        self.elements = elements
        self.faces = faces
        self.edge_faces = edge_faces
        coords = [c for el in elements for c in el["center"]]
        span = (max(coords) - min(coords)) if coords else 0.0
        self.tol = 1e-4 + 1e-6 * abs(span)

    def run(self, node: Node) -> Set[int]:
        op = node[0]
        if op == "all":
            return {el["index"] for el in self.elements}
        if op == "or":
            return self.run(node[1]) | self.run(node[2])
        if op == "and":
            return self.run(node[1]) & self.run(node[2])
        if op == "not":
            return {el["index"] for el in self.elements} - self.run(node[1])
        if op == "type":
            return {el["index"] for el in self.elements if el.get("type", "").upper() == node[1]}
        if op == "rad":
            cmp, val = node[1], node[2]
            out = set()
            for el in self.elements:
                r = el.get("radius")
                if r is None:
                    continue
                if (
                    (cmp == "<" and r < val - 1e-9)
                    or (cmp == ">" and r > val + 1e-9)
                    or (cmp == "=" and abs(r - val) <= 1e-6 * max(1.0, val))
                ):
                    out.add(el["index"])
            return out
        if op == "dir":
            return self._dir(node[1], node[2])
        if op == "face":
            if self.faces is None or self.edge_faces is None:
                raise SelectorError("face(...) can only be used to select edges")
            face_sel = _Eval(self.faces, None, None).run(node[1])
            mapping = self.edge_faces()
            return {e for e, fs in mapping.items() if face_sel.intersection(fs)}
        raise SelectorError(f"Bad selector node {op}")

    def _dir(self, sym: str, axis: int) -> Set[int]:
        if sym in "<>":
            if not self.elements:
                return set()
            vals = [el["center"][axis] for el in self.elements]
            target = max(vals) if sym == ">" else min(vals)
            return {el["index"] for el, v in zip(self.elements, vals) if abs(v - target) <= self.tol}
        out = set()
        ref = _unit(axis)
        for el in self.elements:
            d = _dir_of(el)
            if d is None:
                continue
            c = _dot(d, ref)
            if sym == "|" and abs(abs(c) - 1.0) <= _PAR:
                out.add(el["index"])
            elif sym == "#" and abs(c) <= _PAR:
                out.add(el["index"])
            elif sym in "+-" and el.get("kind") == "face":
                want = 1.0 if sym == "+" else -1.0
                if abs(c - want) <= _PAR:
                    out.add(el["index"])
        return out


def select(
    value: SelectorValue,
    elements: List[Descriptor],
    faces: Optional[List[Descriptor]] = None,
    edge_faces: Optional[Callable[[], Dict[int, List[int]]]] = None,
) -> List[int]:
    """Resolve a selector to a sorted list of 1-based indices.

    ``elements`` are the descriptors of the element kind being selected.
    For edge selection, pass ``faces`` and ``edge_faces`` (lazy mapping
    edge index -> list of face indices) to enable ``face(...)``.
    """
    count = len(elements)
    if isinstance(value, int) and not isinstance(value, bool):
        value = [value]
    if isinstance(value, list):
        bad = [i for i in value if i < 1 or i > count]
        if bad:
            raise SelectorError(f"Index out of range: {bad}; the shape has {count} elements (1..{count})")
        return sorted(set(value))
    node = parse(value)
    return sorted(_Eval(elements, faces, edge_faces).run(node))


def is_dynamic(value: Any) -> bool:
    """True if the selector should be re-evaluated when the base shape changes."""
    return isinstance(value, str)

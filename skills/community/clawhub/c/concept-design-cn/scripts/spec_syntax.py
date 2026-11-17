"""Shared source masking and local CONCEPT/SYNCS syntax; no file access."""

import re
from dataclasses import dataclass

CORE = ("purpose", "state", "actions", "operational principle")
HEAD = re.compile(r"^#[ \t]+(concept|app)[ \t]+(\S+)[^\n]*$", re.M)
SECTION = re.compile(r"^##[ \t]+([^\n]+?)[ \t]*$", re.M)
RULE = re.compile(r"^[ \t]*sync[ \t]+([^\s{]+)[ \t]*$", re.M)
COVERAGE = re.compile(r"^[ \t]*coverage:[ \t]*(complete|partial)[ \t]*$", re.M)
TOKEN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|[{}\[\]()]|\S")
FENCE = re.compile(r"[ \t]*(`{3,}|~{3,})[^\n]*")
OPEN_BLOCK = re.compile(r"\s*\{")
CALL = re.compile(r"([A-Za-z_][\w-]*)/([A-Za-z_][\w-]*)\s*:")
FIELD = re.compile(r"\s*([A-Za-z_][\w-]*)\s*:")
CLAUSES = ("when", "where", "then")


@dataclass(frozen=True)
class Source:
    syntax: str
    content: str
    known_end: int
    unchecked: tuple

    @property
    def complete(self):
        return self.known_end == len(self.syntax)


def diagnostic(text, offset, code, message):
    return {"line": text.count("\n", 0, offset) + 1, "code": code, "message": message}


def add(result, category, text, offset, code, message):
    result[category].append(diagnostic(text, offset, code, message))


def blank(text):
    return re.sub(r"[^\n]", " ", text)


def has_literal(source, match):
    return source.content[match.start():match.end()] != source.syntax[match.start():match.end()]


def prepare(text):
    """Mask annotations and literals without changing offsets or line numbers."""
    syntax, content = list(text), list(text)
    index, known_end, unchecked = 0, len(text), []

    def hide(start, end, literal=False):
        syntax[start:end] = blank(text[start:end])
        if not literal:
            content[start:end] = blank(text[start:end])

    def unfinished(start, kind):
        hide(start, len(text), literal=kind == "literal")
        unchecked.append(diagnostic(text, start, "unfinished-" + kind,
                                    f"Unclosed {kind}; following structure was not checked."))
        return start

    while index < len(text):
        if index == 0 or text[index - 1] == "\n":
            fence = FENCE.match(text, index)
            if fence:
                end_open = text.find("\n", index)
                end_open = len(text) if end_open < 0 else end_open + 1
                closing = re.compile(r"^[ \t]*" + re.escape(fence[1][0]) +
                                     "{" + str(len(fence[1])) + r",}[ \t]*$", re.M)
                close = closing.search(text, end_open)
                if close is None:
                    known_end = unfinished(index, "fence")
                    break
                end = close.end()
                hide(index, end)
                index = end
                continue
        if text.startswith("//", index):
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            hide(index, end)
            index = end
            continue
        comment = next(((opening, closing) for opening, closing in
                        (("/*", "*/"), ("<!--", "-->")) if text.startswith(opening, index)), None)
        if comment:
            end = text.find(comment[1], index + len(comment[0]))
            if end < 0:
                known_end = unfinished(index, "comment")
                break
            end += len(comment[1])
            hide(index, end)
            index = end
            continue
        quote = text[index]
        apostrophe = index > 0 and (text[index - 1].isalnum() or text[index - 1] == "_")
        if quote == '"' or (quote == "'" and not apostrophe):
            end = index + 1
            while end < len(text):
                if text[end] == "\\":
                    end += 2
                elif text[end] == quote:
                    break
                else:
                    end += 1
            if end >= len(text):
                known_end = unfinished(index, "literal")
                break
            hide(index, end + 1, literal=True)
            index = end + 1
            continue
        index += 1
    return Source("".join(syntax), "".join(content), known_end, tuple(unchecked))


def record_end(text, start, end):
    if start >= end or text[start] != "[":
        return None
    depth = 0
    for token in TOKEN.finditer(text, start, end):
        if token[0] == "[":
            depth += 1
        elif token[0] == "]":
            depth -= 1
            if depth == 0:
                return token.start()
    return None

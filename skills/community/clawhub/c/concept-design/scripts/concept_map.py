#!/usr/bin/env python3
"""Generate a Concept and Synchronization Diagram from local specifications."""

import argparse
import fnmatch
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote

sys.dont_write_bytecode = True

import concept_lint as lint
from spec_syntax import (CALL, CLAUSES, HEAD, OPEN_BLOCK, RULE, SECTION, TOKEN,
                         has_literal, prepare, record_end)

BEGIN, END = "<!-- concept-map:start -->", "<!-- concept-map:end -->"
DEFAULT_EXCLUDES = (".git", "node_modules", ".venv")
INCLUDE = re.compile(r"^[ \t]*include[ \t]+([A-Za-z_][\w-]*)(?:[ \t]*\[([^\]\n]*)\])?[ \t]*$", re.M)
STATE_READ = re.compile(r"([A-Za-z_][\w-]*)\s*:\s*\{")
BIND = re.compile(r"bind\s*\(")
SUBJECT = re.compile(r"\s*(\?[A-Za-z_][\w-]*)")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def stable_id(key):
    return {"concept": "c", "instance": "i", "sync": "s"}[key[0]] + "_" + digest(canonical(key).encode())[:12]


def in_scope(path, scope):
    return scope == "." or path == scope or path.startswith(scope + "/")


def excluded(path, patterns):
    for pattern in patterns:
        alternatives = (pattern, pattern[3:]) if pattern.startswith("**/") else (pattern,)
        for value in alternatives:
            if fnmatch.fnmatchcase(path, value) or (value.endswith("/**") and path == value[:-3]):
                return True
    return False


def skip(source, start, end):
    cursor = start
    while cursor < end and source.syntax[cursor].isspace():
        cursor += 1
    return None if source.content[start:cursor].strip() else cursor


def matching_end(text, start, end):
    pairs, stack = {"}": "{", "]": "[", ")": "("}, []
    for token in TOKEN.finditer(text, start, end):
        value = token[0]
        if value in ("{", "[", "("):
            stack.append(value)
        elif value in pairs:
            if not stack or stack.pop() != pairs[value]:
                return None
            if not stack:
                return token.start()
    return None


def rule_blocks(source, start, end):
    text, cursor = source.syntax, start
    while cursor < end:
        cursor = skip(source, cursor, end)
        if cursor is None or cursor == end:
            return
        clause = re.match(r"(when|where|then)\b", text[cursor:end])
        if not clause:
            return
        opened = OPEN_BLOCK.match(text, cursor + clause.end(), end)
        if not opened or source.content[cursor + clause.end():opened.end() - 1].strip():
            return
        closing = matching_end(text, opened.end() - 1, end)
        if closing is None:
            return
        yield clause[1], opened.end(), closing
        cursor = closing + 1


def action(source, start, end, completion):
    """Read one already linted action shape without interpreting field values."""
    text = source.syntax
    match = CALL.match(text, start, end)
    if not match or source.content[match.end(2):match.end() - 1].strip():
        return None
    cursor = skip(source, match.end(), end)
    closing = record_end(text, cursor, end) if cursor is not None else None
    if closing is None:
        return None
    records = [(cursor, closing)]
    finish = closing + 1
    cursor = skip(source, finish, end)
    if cursor is None:
        return None
    if completion:
        if not text.startswith("=>", cursor):
            return None
        cursor = skip(source, cursor + 2, end)
        closing = record_end(text, cursor, end) if cursor is not None else None
        if closing is None:
            return None
        records.append((cursor, closing))
        finish = closing + 1
    elif text.startswith("=>", cursor):
        return None
    return match[1], match[2], finish, records


class Diagram:
    def __init__(self, root, scope, excludes):
        self.root, self.scope = root, scope
        self.excludes = sorted(set(DEFAULT_EXCLUDES) | set(excludes))
        self.patterns = excludes
        self.specs, self.nodes, self.edges = [], {}, []
        self.definitions, self.bindings = {}, {}
        self.errors, self.gaps, self.read_errors = [], [], []
        self._gaps = set()

    def evidence(self, spec, start=0, end=None):
        end = start if end is None else end
        return {"path": spec["path"], "line": spec["text"].count("\n", 0, start) + 1,
                "end_line": spec["text"].count("\n", 0, max(start, end - 1)) + 1}

    def gap(self, spec, start, end, code, message):
        evidence = self.evidence(spec, start, end)
        raw = spec["text"][start:end].strip()
        key = (evidence["path"], evidence["line"], evidence["end_line"], code, message, raw)
        if key not in self._gaps:
            self._gaps.add(key)
            self.gaps.append({**evidence, "code": code, "message": message, "raw": raw})

    def add_node(self, key, name, evidence, **attributes):
        node_id = stable_id(key)
        if node_id in self.nodes and self.nodes[node_id]["key"] != key:
            self.errors.append({**evidence, "code": "id-collision", "message": "Node ID hash collision."})
        elif node_id not in self.nodes:
            self.nodes[node_id] = {"id": node_id, "key": key, "kind": key[0], "name": name,
                                   "evidence": [evidence], **attributes}
        elif evidence not in self.nodes[node_id]["evidence"]:
            self.nodes[node_id]["evidence"].append(evidence)
        return node_id

    def discover(self):
        def walk_error(error):
            self.read_errors.append(str(error))

        files = []
        for directory, folders, names in os.walk(self.root, followlinks=False, onerror=walk_error):
            base = Path(directory)
            folders[:] = sorted(name for name in folders if name not in DEFAULT_EXCLUDES
                                and not (base / name).is_symlink()
                                and not excluded((base / name).relative_to(self.root).as_posix(), self.patterns))
            for name in sorted(set(names) & {"CONCEPT.md", "SYNCS.md"}):
                path = base / name
                if not path.is_symlink() and not excluded(path.relative_to(self.root).as_posix(), self.patterns):
                    files.append(path)
        registry = {}
        for path in sorted(files):
            relative = path.relative_to(self.root).as_posix()
            try:
                raw = path.read_bytes()
                text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
            except (OSError, UnicodeError) as error:
                self.read_errors.append(f"{relative}: {error}")
                continue
            source = prepare(text)
            report = lint.check_text(text, relative, registry)
            spec = {"path": relative, "text": text, "source": source, "sha256": digest(raw),
                    "kind": report["kind"], "name": report["name"], "report": report}
            self.specs.append(spec)
            for issue in report["issues"]:
                self.errors.append({"path": relative, **issue})
            for issue in report["unchecked"]:
                lines = text.splitlines(keepends=True)
                start = sum(map(len, lines[:issue["line"] - 1]))
                end = start + (len(lines[issue["line"] - 1]) if issue["line"] <= len(lines) else 0)
                self.gap(spec, start, end, issue["code"], issue["message"])
            headers = list(HEAD.finditer(source.syntax))
            expected = "concept" if path.name == "CONCEPT.md" else "app"
            if report["kind"] and report["kind"] != expected:
                self.errors.append({"path": relative, "line": 1, "code": "file-kind",
                                    "message": f"{path.name} must declare a {expected}."})
            if len(headers) != 1 or has_literal(source, headers[0]):
                continue
            if report["kind"] == "concept":
                self.definitions.setdefault(report["name"], []).append(spec)

    def concept(self, spec):
        source = spec["source"]
        sections = list(SECTION.finditer(source.syntax))
        purpose, coverage = "", "undeclared"
        for index, section in enumerate(sections):
            if section[1].strip().lower() == "purpose":
                end = sections[index + 1].start() if index + 1 < len(sections) else source.known_end
                purpose = spec["text"][section.end():end].strip()
                break
        match = re.search(r"^\s*coverage:[ \t]*(complete|partial)[ \t]*$", source.syntax, re.M)
        if match:
            coverage = match[1]
        heading = next(HEAD.finditer(source.syntax))
        return self.add_node(["concept", spec["path"], spec["name"]], spec["name"],
                             self.evidence(spec, heading.start(), source.known_end), purpose=purpose, coverage=coverage,
                             outside_scope=not in_scope(spec["path"], self.scope))

    def read_includes(self):
        for spec in self.specs:
            if spec["kind"] != "app" or spec["report"]["issues"]:
                continue
            source = spec["source"]
            headers = list(HEAD.finditer(source.syntax))
            if len(headers) != 1 or has_literal(source, headers[0]):
                continue
            rules = list(RULE.finditer(source.syntax))
            end = rules[0].start() if rules else source.known_end
            includes = list(INCLUDE.finditer(source.syntax, headers[0].end(), end))
            for match in includes:
                if has_literal(source, match):
                    self.gap(spec, match.start(), match.end(), "include-syntax", "Unsupported include declaration.")
                    continue
                identity = (spec["name"], match[1])
                binding = self.bindings.setdefault(identity, {"types": re.sub(r"\s+", "", match[2] or ""), "sources": []})
                if binding["types"] != re.sub(r"\s+", "", match[2] or ""):
                    self.errors.append({**self.evidence(spec, match.start(), match.end()), "code": "instance-conflict",
                                        "message": f"Conflicting type bindings for {spec['name']}/{match[1]}."})
                binding["sources"].append((spec, match.start(), match.end()))
            cursor = headers[0].end()
            for match in includes + [None]:
                finish = match.start() if match else end
                if source.content[cursor:finish].strip():
                    self.gap(spec, cursor, finish, "app-declaration", "Unparsed app declaration or include.")
                cursor = match.end() if match else end

    def instance(self, app, name, spec, start, end):
        key = ["instance", app, name]
        node_id = stable_id(key)
        if node_id in self.nodes:
            evidence = self.evidence(spec, start, end)
            if evidence not in self.nodes[node_id]["evidence"]:
                self.nodes[node_id]["evidence"].append(evidence)
            return node_id
        binding = self.bindings.get((app, name))
        candidates = self.definitions.get(name, []) if binding else []
        definition, resolution = None, "missing"
        if binding and len(candidates) == 1:
            definition = self.concept(candidates[0])
            resolution = "outside_scope" if self.nodes[definition]["outside_scope"] else "resolved"
        else:
            resolution = "ambiguous" if len(candidates) > 1 else "missing"
            message = (f"Multiple definitions match {app}/{name}: {', '.join(s['path'] for s in candidates)}." if len(candidates) > 1 else
                       f"No matching CONCEPT definition for {app}/{name}." if binding else
                       f"No recognized include for {app}/{name}.")
            self.gap(spec, start, end, resolution if binding else "undeclared-instance", message)
        declarations = [self.evidence(s, left, right) for s, left, right in binding["sources"]] if binding else []
        return self.add_node(key, name, self.evidence(spec, start, end), app=app,
                             definition=definition, resolution=resolution, declarations=declarations,
                             types=binding["types"] if binding else "undeclared")

    def relation(self, spec, rule_id, clause, ordinal, name, action_name, start, end):
        instance = self.instance(spec["name"], name, spec, start, end)
        self.edges.append({"rule": rule_id, "kind": clause, "ordinal": ordinal,
                           "source": rule_id if clause == "then" else instance,
                           "target": instance if clause == "then" else rule_id,
                           "action": action_name, "pattern": spec["text"][start:end].strip(),
                           **self.evidence(spec, start, end)})

    def check_fields(self, spec, start, end):
        report = {"issues": [], "unchecked": []}
        lint.check_fields(spec["source"], start, end, report)
        self.errors.extend({"path": spec["path"], **issue} for issue in report["issues"])
        for issue in report["unchecked"]:
            self.gap(spec, start, end + 1, issue["code"], issue["message"])
        return not report["issues"] and not report["unchecked"]

    def read_where(self, spec, rule_id, start, end):
        source, cursor, ordinal = spec["source"], start, 0
        while cursor < end:
            previous = cursor
            cursor = skip(source, cursor, end)
            if cursor is None:
                self.gap(spec, previous, end, "where-syntax", "Literal outside a where expression.")
                break
            if cursor == end:
                break
            call = action(source, cursor, end, True)
            state = STATE_READ.match(source.syntax, cursor, end)
            bind = BIND.match(source.syntax, cursor, end)
            if call:
                name, action_name, finish, records = call
                checked = [self.check_fields(spec, left, right) for left, right in records]
                ordinal += 1
                if all(checked):
                    self.relation(spec, rule_id, "where", ordinal, name, action_name, cursor, finish)
            elif state:
                opening = state.end() - 1
                finish = matching_end(source.syntax, opening, end)
                if finish is None or source.content[state.end(1):opening].strip().strip(":"):
                    self.gap(spec, cursor, end, "where-syntax", "Unparsed where expression.")
                    break
                finish += 1
                subject = SUBJECT.match(source.syntax, opening + 1, finish - 1)
                checked = False
                if (not subject or not source.content[subject.end():finish - 1].strip() or
                        source.content[opening + 1:subject.start(1)].strip()):
                    self.gap(spec, opening, finish, "where-state", "Unparsed state pattern; expected ?subject followed by named relations.")
                elif CALL.search(source.syntax, subject.end(), finish - 1) or STATE_READ.search(source.syntax, subject.end(), finish - 1):
                    self.gap(spec, opening, finish, "where-state", "Nested namespace expressions were not classified.")
                else:
                    checked = self.check_fields(spec, subject.end() - 1, finish - 1)
                ordinal += 1
                if checked:
                    self.relation(spec, rule_id, "where", ordinal, state[1], "state", cursor, finish)
            elif bind:
                opening = bind.end() - 1
                finish = matching_end(source.syntax, opening, end)
                if finish is None or source.content[cursor + 4:opening].strip():
                    self.gap(spec, cursor, end, "where-syntax", "Unparsed bind expression.")
                    break
                if CALL.search(source.syntax, opening + 1, finish) or STATE_READ.search(source.syntax, opening + 1, finish):
                    self.gap(spec, cursor, finish + 1, "where-bind", "Namespace expressions inside a calculation were not classified.")
                # Calculations are retained as conditions, not invented query edges.
                finish += 1
            else:
                self.gap(spec, cursor, end, "where-syntax", "Unparsed where expression; no relationship inferred.")
                break
            cursor = finish

    def extract(self):
        self.read_includes()
        for specs in self.definitions.values():
            for spec in specs:
                if in_scope(spec["path"], self.scope):
                    self.concept(spec)
        for (app, name), binding in sorted(self.bindings.items()):
            for spec, start, end in binding["sources"]:
                if in_scope(spec["path"], self.scope):
                    self.instance(app, name, spec, start, end)
        for spec in self.specs:
            if spec["kind"] != "app" or not in_scope(spec["path"], self.scope) or spec["report"]["issues"]:
                continue
            source = spec["source"]
            headers = list(HEAD.finditer(source.syntax))
            if len(headers) != 1 or has_literal(source, headers[0]):
                continue
            rules = list(RULE.finditer(source.syntax))
            for index, rule in enumerate(rules):
                if has_literal(source, rule):
                    continue
                end = rules[index + 1].start() if index + 1 < len(rules) else source.known_end
                heading = re.search(r"^#{1,6}[ \t]", source.syntax[rule.end():end], re.M)
                if heading:
                    self.gap(spec, rule.end() + heading.start(), end, "rule-section", "Section outside supported rule notation.")
                    end = rule.end() + heading.start()
                node = self.add_node(["sync", spec["name"], rule[1]], rule[1],
                                     self.evidence(spec, rule.start(), end), app=spec["name"], conditions=[])
                for clause, left, right in rule_blocks(source, rule.end(), end):
                    if clause == "where":
                        self.nodes[node]["conditions"].append({"text": spec["text"][left:right].strip(),
                                                              **self.evidence(spec, left, right)})
                        self.read_where(spec, node, left, right)
                        continue
                    cursor, ordinal = left, 0
                    while cursor < right:
                        cursor = skip(source, cursor, right)
                        if cursor is None or cursor == right:
                            break
                        call = action(source, cursor, right, clause == "when")
                        if not call:
                            break  # lint retains this unknown notation as a gap.
                        name, action_name, finish, _ = call
                        ordinal += 1
                        self.relation(spec, node, clause, ordinal, name, action_name, cursor, finish)
                        cursor = finish
        if self.specs and not self.nodes:
            self.gaps.append({"path": self.scope, "line": 1, "end_line": 1, "code": "empty-scope",
                              "message": "No recognized nodes in the selected scope.", "raw": ""})

    @property
    def partial(self):
        return bool(self.gaps) or not self.specs


def cell(value):
    return html.escape(str(value), quote=True).replace("|", "&#124;").replace("\r", "").replace("\n", "<br>")


def source_link(evidence, root, directory):
    relative = Path(os.path.relpath(root / evidence["path"], directory.resolve())).as_posix()
    label = f"{evidence['path']}:{evidence['line']}"
    return f"[{cell(label)}]({quote(relative, safe='/')}#L{evidence['line']})"


def render(diagram, directory):
    nodes = sorted(diagram.nodes.values(), key=lambda node: node["key"])
    concepts = [node for node in nodes if node["kind"] == "concept"]
    instances = [node for node in nodes if node["kind"] == "instance"]
    rules = [node for node in nodes if node["kind"] == "sync"]
    edges = sorted(diagram.edges, key=lambda edge: (diagram.nodes[edge["rule"]]["key"],
                                                  CLAUSES.index(edge["kind"]), edge["ordinal"]))
    fingerprint = digest(canonical([1, diagram.scope, diagram.excludes,
                                   [[s["path"], s["sha256"]] for s in diagram.specs]]).encode())
    lines = [BEGIN, "# Concept and Synchronization Diagram", "", "## Source status", "",
             f"Status: {'partial' if diagram.partial else 'complete'}", f"Scope: {cell(diagram.scope)}",
             f"Excludes: {', '.join(cell(value) for value in diagram.excludes)}; symbolic links",
             f"Source fingerprint: `{fingerprint}`", f"Indexed specifications: {len(diagram.specs)}",
             f"Concept definitions: {len(concepts)}; instances: {len(instances)}; synchronizations: {len(rules)}; relations: {len(edges)}.",
             "", "Counts describe specifications, not code coverage or runtime correctness.", "", "## Concept index", "",
             "| ID | Concept | Purpose (source text) | Coverage | Scope | Source |",
             "| --- | --- | --- | --- | --- | --- |"]
    for node in concepts:
        lines.append(f"| {node['id']} | {cell(node['name'])} | {cell(node['purpose'])} | {node['coverage']} | "
                     f"{'outside_scope' if node['outside_scope'] else 'in_scope'} | {source_link(node['evidence'][0], diagram.root, directory)} |")
    if not concepts:
        lines.append("| — | No resolved concept definitions | — | — | — | — |")
    lines += ["", "### Instances", "", "| ID | App / instance | Types | Definition | Resolution | Declaration sources |",
              "| --- | --- | --- | --- | --- | --- |"]
    for node in instances:
        origins = ", ".join(source_link(e, diagram.root, directory) for e in node["declarations"])
        lines.append(f"| {node['id']} | {cell(node['app'] + '/' + node['name'])} | {cell(node['types'])} | "
                     f"{node['definition'] or '—'} | {node['resolution']} | {origins or 'undeclared; see relations'} |")
    lines += ["", "### Synchronizations", "", "| ID | App / rule | Declaration source |", "| --- | --- | --- |"]
    for node in rules:
        lines.append(f"| {node['id']} | {cell(node['app'] + '/' + node['name'])} | {source_link(node['evidence'][0], diagram.root, directory)} |")
    lines += ["", "## Synchronization diagram", "",
              "All when edges of a synchronization match together (AND). Dashed where edges are reads; then edges are unordered invocations.", "",
              "```mermaid", "flowchart LR"]
    referenced = {node["definition"] for node in instances if node["definition"]}
    for node in nodes:
        if node["kind"] == "concept" and node["id"] in referenced:
            continue
        label = node["name"]
        if node["kind"] in ("instance", "sync"):
            label = node["app"] + "/" + label
        if node["kind"] == "instance" and node["resolution"] != "resolved":
            label += " (" + node["resolution"] + ")"
        if node["kind"] == "sync":
            lines.append(f'  {node["id"]}{{"{cell(label)} · AND"}}')
        else:
            lines.append(f'  {node["id"]}["{cell(label)}"]')
    for edge in edges:
        arrow = "-.->" if edge["kind"] == "where" else "-->"
        label = cell(f"{edge['kind']} #{edge['ordinal']} · {edge['action']}")
        lines.append(f'  {edge["source"]} {arrow}|"{label}"| {edge["target"]}')
    lines += ["```", "", "## Relations", "",
              "| Rule | Kind | # | From | To | Original pattern | Source |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for edge in edges:
        rule = diagram.nodes[edge["rule"]]
        lines.append(f"| {cell(rule['app'] + '/' + rule['name'])} | {edge['kind']} | {edge['ordinal']} | "
                     f"{edge['source']} | {edge['target']} | <code>{cell(edge['pattern'])}</code> | {source_link(edge, diagram.root, directory)} |")
    for rule in rules:
        for condition in rule["conditions"]:
            if condition["text"]:
                lines += ["", f"Where conditions — {cell(rule['app'] + '/' + rule['name'])}: "
                          f"<code>{cell(condition['text'])}</code> ({source_link(condition, diagram.root, directory)})"]
    lines += ["", "## Gaps", ""]
    for gap in sorted(diagram.gaps, key=lambda value: (value["path"], value["line"], value["code"], value["message"])):
        lines.append(f"- **{cell(gap['code'])}** — {cell(gap['message'])} "
                     f"({source_link(gap, diagram.root, directory)}): <code>{cell(gap['raw'])}</code>")
    if not diagram.gaps:
        lines.append("No extraction gaps in the declared scope. This is not a purpose-dependence diagram or an execution trace.")
    return "\n".join(lines + ["", END, ""])


def replace_region(existing, generated):
    if existing is None:
        return generated
    if existing.count(BEGIN) != 1 or existing.count(END) != 1:
        raise ValueError("Existing output must contain exactly one concept-map marker pair.")
    start, end = existing.index(BEGIN), existing.index(END)
    if end < start:
        raise ValueError("Output markers are reversed.")
    return existing[:start] + generated.rstrip("\n") + existing[end + len(END):]


def write_changed(path, content, existing):
    if existing == content:
        return False
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent,
                                         prefix=".concept-map-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
        return True
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog="Exit: 0 complete, 1 invalid/stale, 2 read/usage/write error, 3 partial/no specifications.")
    parser.add_argument("root", type=Path, help="project root")
    parser.add_argument("--scope", default=".", help="display a root-relative subtree; index the whole root")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    parser.add_argument("--output", type=Path, help="replace only the generated region in this Markdown file")
    parser.add_argument("--check", action="store_true", help="compare with --output without writing")
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    if Path(args.scope).is_absolute():
        parser.error("--scope must be relative to the project root")
    try:
        root = args.root.resolve()
        scope_path = (root / args.scope).resolve()
        scope = scope_path.relative_to(root).as_posix()
        if not root.is_dir() or not scope_path.exists():
            raise OSError("Root and scope must exist.")
    except (OSError, RuntimeError, ValueError) as error:
        print(f"read_error: {error}", file=sys.stderr)
        return 2
    diagram = Diagram(root, scope, args.exclude)
    diagram.discover()
    diagram.extract()
    if not diagram.specs and not diagram.read_errors:
        print("No CONCEPT.md or SYNCS.md found; existing output preserved.", file=sys.stderr)
        return 3
    existing, output = None, args.output
    try:
        if output is not None:
            if output.is_symlink() or output.name in ("CONCEPT.md", "SYNCS.md"):
                raise ValueError("Output must not be a symbolic link or an input specification.")
            output = output.resolve()
            if output.resolve() in {(root / spec["path"]).resolve() for spec in diagram.specs}:
                raise ValueError("Output must not overwrite an input specification.")
            try:
                existing = output.read_bytes().decode("utf-8")
            except FileNotFoundError:
                pass
        content = render(diagram, output.parent if output else root)
        updated = replace_region(existing, content)
    except (OSError, UnicodeError, RuntimeError) as error:
        diagram.read_errors.append(str(error))
    except ValueError as error:
        diagram.errors.append({"path": str(output), "line": 1, "code": "output", "message": str(error)})
    for error in diagram.read_errors:
        print(f"read_error: {error}", file=sys.stderr)
    for error in diagram.errors:
        print(f"{error['path']}:{error['line']}: {error['code']}: {error['message']}", file=sys.stderr)
    if diagram.read_errors:
        return 2
    if diagram.errors:
        return 1
    if not diagram.specs:
        print("No CONCEPT.md or SYNCS.md found; existing output preserved.", file=sys.stderr)
        return 3
    if args.check:
        if updated != existing:
            print(f"stale: {output}")
            return 1
        print(f"current: {output} ({'partial' if diagram.partial else 'complete'})")
    elif output:
        try:
            changed = write_changed(output, updated, existing)
        except OSError as error:
            print(f"write_error: {error}", file=sys.stderr)
            return 2
        print(f"{'updated' if changed else 'unchanged'}: {output}")
    else:
        print(content, end="")
    print(f"{'partial' if diagram.partial else 'complete'}: {len(diagram.nodes)} nodes, "
          f"{len(diagram.edges)} relations, {len(diagram.gaps)} gaps", file=sys.stderr)
    return 3 if diagram.partial else 0


if __name__ == "__main__":
    raise SystemExit(main())

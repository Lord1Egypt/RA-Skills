from __future__ import annotations

import ast
import importlib.util
import inspect
from pathlib import Path
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CANDIDATE_UPSERT_FUNCTIONS = (
    "upsert_book",
    "upsert_book_record",
    "upsert_record",
    "upsert_entry",
    "upsert_capture",
    "upsert_note",
)

BOOK_PAYLOAD = {
    "isbn": "9780306406157",
    "title": "The Testing Book",
    "authors": ["QA Worker C"],
    "source": "unit-test",
    "shelf": "inbox",
    "tags": ["book"],
}


def _iter_python_files():
    for py_file in PROJECT_ROOT.rglob("*.py"):
        parts = set(py_file.parts)
        if {"tests", "__pycache__", ".venv", "venv", ".git"} & parts:
            continue
        yield py_file


def _find_function_source(function_names: tuple[str, ...]):
    for py_file in _iter_python_files():
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except (SyntaxError, OSError, UnicodeDecodeError):
            continue

        declared = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for name in function_names:
            if name in declared:
                return py_file, name

    return None, None


def _load_module(py_file: Path) -> ModuleType:
    module_name = f"_worker_c_{py_file.stem}_{abs(hash(str(py_file)))}"
    spec = importlib.util.spec_from_file_location(module_name, str(py_file))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {py_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve_upsert_callable():
    py_file, function_name = _find_function_source(CANDIDATE_UPSERT_FUNCTIONS)
    if py_file is None or function_name is None:
        return None

    module = _load_module(py_file)
    fn = getattr(module, function_name, None)
    if callable(fn):
        return fn

    return None


def _call_upsert(upsert, note_path: Path, payload: dict, current_content: str):
    parent = note_path.parent
    attempts = [
        # Common signature in this project: upsert_note(payload, vault_path, notes_dir, target_note)
        lambda: upsert(payload, str(parent), ".", str(note_path)),
        lambda: upsert(payload=payload, vault_path=str(parent), notes_dir=".", target_note=str(note_path)),
        # Generic positional/keyword contract attempts
        lambda: upsert(note_path, payload),
        lambda: upsert(str(note_path), payload),
        lambda: upsert(payload, note_path),
        lambda: upsert(payload, str(note_path)),
        lambda: upsert(note_path=note_path, book=payload),
        lambda: upsert(note_path=str(note_path), book=payload),
        lambda: upsert(path=note_path, book=payload),
        lambda: upsert(path=str(note_path), book=payload),
        lambda: upsert(file_path=str(note_path), book=payload),
        lambda: upsert(content=current_content, book=payload),
        lambda: upsert(current_content, payload),
        lambda: upsert(vault_path=str(parent), note_path=str(note_path), book=payload),
    ]

    errors = []
    for attempt in attempts:
        try:
            return attempt()
        except TypeError as exc:
            errors.append(str(exc))
            continue

    signature = inspect.signature(upsert)
    raise AssertionError(
        "Could not invoke upsert function with supported contract patterns. "
        f"Detected signature: {signature}. TypeErrors: {errors}"
    )


def _effective_content(note_path: Path, result):
    if note_path.exists():
        return note_path.read_text(encoding="utf-8")
    if isinstance(result, str):
        return result
    return ""


def _count_isbn_occurrences(value, isbn: str) -> int:
    if isinstance(value, str):
        return value.count(isbn)
    if isinstance(value, dict):
        return sum(_count_isbn_occurrences(v, isbn) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return sum(_count_isbn_occurrences(v, isbn) for v in value)
    return 0


def test_upsert_callable_exists():
    upsert = _resolve_upsert_callable()
    assert upsert is not None, (
        "Could not find an upsert function. Expected one of: "
        f"{', '.join(CANDIDATE_UPSERT_FUNCTIONS)}"
    )


def test_upsert_idempotent_for_same_payload(tmp_path):
    upsert = _resolve_upsert_callable()
    assert upsert is not None, (
        "Could not find an upsert function. Expected one of: "
        f"{', '.join(CANDIDATE_UPSERT_FUNCTIONS)}"
    )

    note_path = tmp_path / "Books.md"
    note_path.write_text("# Captured Books\n\n", encoding="utf-8")

    first_result = _call_upsert(
        upsert,
        note_path=note_path,
        payload=BOOK_PAYLOAD,
        current_content=note_path.read_text(encoding="utf-8"),
    )
    first_content = _effective_content(note_path, first_result)

    second_result = _call_upsert(
        upsert,
        note_path=note_path,
        payload=BOOK_PAYLOAD,
        current_content=first_content,
    )
    second_content = _effective_content(note_path, second_result)

    if first_content and second_content:
        assert second_content == first_content
        assert second_content.count(BOOK_PAYLOAD["isbn"]) <= 1
    else:
        first_count = _count_isbn_occurrences(first_result, BOOK_PAYLOAD["isbn"])
        second_count = _count_isbn_occurrences(second_result, BOOK_PAYLOAD["isbn"])
        assert second_count <= 1
        if first_count:
            assert second_count == first_count

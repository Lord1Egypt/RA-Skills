from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CANDIDATE_NORMALIZERS = (
    "normalize_isbn",
    "normalise_isbn",
    "isbn_normalize",
    "clean_isbn",
)

CANDIDATE_VALIDATORS = (
    "is_valid_isbn",
    "validate_isbn",
    "isbn_is_valid",
    "is_valid_isbn13",
)

CANDIDATE_ISBN13_CHECKDIGIT = (
    "isbn13_check_digit",
    "compute_isbn13_check_digit",
    "calculate_isbn13_check_digit",
    "calc_isbn13_check_digit",
)


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


def _resolve_callable(function_names: tuple[str, ...]):
    py_file, function_name = _find_function_source(function_names)
    if py_file is None or function_name is None:
        return None

    module = _load_module(py_file)
    fn = getattr(module, function_name, None)
    if callable(fn):
        return fn

    return None


def _call_isbn13_checkdigit(func, prefix12: str) -> str:
    try:
        value = func(prefix12)
    except TypeError:
        value = func([int(char) for char in prefix12])
    return str(value)


def test_isbn_normalization_removes_separators_and_whitespace():
    normalize = _resolve_callable(CANDIDATE_NORMALIZERS)
    assert normalize is not None, (
        "Could not find an ISBN normalization function. Expected one of: "
        f"{', '.join(CANDIDATE_NORMALIZERS)}"
    )

    normalized = str(normalize(" 978-0-306-40615-7 "))

    assert normalized == "9780306406157"
    assert "-" not in normalized
    assert " " not in normalized


def test_isbn10_normalization_keeps_valid_digits_or_converts_to_isbn13():
    normalize = _resolve_callable(CANDIDATE_NORMALIZERS)
    assert normalize is not None, (
        "Could not find an ISBN normalization function. Expected one of: "
        f"{', '.join(CANDIDATE_NORMALIZERS)}"
    )

    normalized = str(normalize("0-306-40615-2"))

    # Accept either canonical ISBN-10 or its ISBN-13 equivalent.
    assert normalized in {"0306406152", "9780306406157"}


def test_isbn_checksum_validation_and_check_digit_logic():
    validator = _resolve_callable(CANDIDATE_VALIDATORS)
    validator10 = _resolve_callable(("is_valid_isbn10",))
    checkdigit = _resolve_callable(CANDIDATE_ISBN13_CHECKDIGIT)

    assert validator is not None or validator10 is not None or checkdigit is not None, (
        "Could not find ISBN checksum support. Expected either a validator "
        f"({', '.join(CANDIDATE_VALIDATORS)} / is_valid_isbn10) or an ISBN-13 "
        f"check digit function ({', '.join(CANDIDATE_ISBN13_CHECKDIGIT)})."
    )

    valid_isbn13 = "9780306406157"
    invalid_isbn13 = "9780306406158"

    if validator is not None:
        assert bool(validator(valid_isbn13)) is True
        assert bool(validator(invalid_isbn13)) is False

    if validator10 is not None:
        assert bool(validator10("0306406152")) is True
        assert bool(validator10("0306406153")) is False

    if checkdigit is not None:
        assert _call_isbn13_checkdigit(checkdigit, "978030640615") == "7"
        assert _call_isbn13_checkdigit(checkdigit, "978030640616") != "7"

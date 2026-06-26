from __future__ import annotations

from common import docs_root, flatten_pages, load_json, resolve_page_path, root_docs_json


LOCALE_PREFIXES = ("ja-JP/", "zh-CN/", "zh-Hans/")


def candidate_paths(page: str) -> list[str]:
    resolved = resolve_page_path(page)
    candidates = [resolved]
    for prefix in LOCALE_PREFIXES:
        if resolved.startswith(prefix):
            candidates.append(resolved[len(prefix) :])
    return candidates


def page_exists(page: str) -> bool:
    for rel in candidate_paths(page):
        exact = docs_root() / rel
        if exact.exists():
            return True
        if exact.with_suffix(".mdx").exists():
            return True
    return False


def validate_docs_json() -> list[str]:
    errors: list[str] = []
    docs_json = root_docs_json()
    if not docs_json.exists():
        return ["Missing docs.json at skill root."]

    try:
        payload = load_json(docs_json)
    except Exception as exc:
        return [f"Failed to parse docs.json: {exc}"]

    pages = sorted(set(flatten_pages(payload)))
    missing = [resolve_page_path(page) for page in pages if not page_exists(page)]

    if missing:
        preview = ", ".join(missing[:20])
        suffix = "" if len(missing) <= 20 else f" ... (+{len(missing) - 20} more)"
        errors.append(f"docs.json references missing pages: {preview}{suffix}")
    return errors


def validate_required_paths() -> list[str]:
    errors: list[str] = []
    required = ["start", "gateway", "cli", "channels", "providers", "tools"]
    root = docs_root()
    for name in required:
        path = root / name
        if not path.exists():
            errors.append(f"Required path missing: {path}")
    return errors


def validate_markdown_presence() -> list[str]:
    root = docs_root()
    markdown_count = sum(1 for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".mdx"})
    return [] if markdown_count else ["No markdown files found under openclaw_docs/."]


def main() -> int:
    checks = [validate_markdown_presence(), validate_required_paths(), validate_docs_json()]
    errors = [item for chunk in checks for item in chunk]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

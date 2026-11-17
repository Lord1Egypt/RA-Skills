import datetime as dt
import hashlib
import json
import re
from pathlib import Path


PAGE_RULES = [
    ("papers", ["paper", "arxiv", "article", "journal", "conference", "survey", "review", "comparison", "literature"]),
    ("projects", ["project", "requirement", "proposal", "roadmap", "plan"]),
    ("code", ["repo", "repository", "code", "module", "api", "sdk", "package"]),
    ("tech-notes", ["deploy", "architecture", "interface", "config", "technical", "tooling", "manual"]),
    ("experiments", ["experiment", "benchmark", "evaluation", "result", "failure"]),
    ("meetings", ["meeting", "minutes", "transcript", "discussion"]),
    ("concepts", ["concept", "definition", "method", "theory"]),
    ("notes", ["note", "chat", "decision", "discussion", "idea"]),
    ("resources", ["resource", "snippet", "link", "attachment"]),
]


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(text, limit=80):
    text = str(text or "untitled").strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return (text[:limit].strip("-") or "untitled")


def sha256_text(text):
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json_file(path):
    raw = Path(path).read_bytes()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def write_json_file(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data or {}, ensure_ascii=False, indent=2), encoding="utf-8")


def unique(values):
    seen = set()
    result = []
    for value in values or []:
        if value in (None, ""):
            continue
        key = str(value)
        if key not in seen:
            result.append(value)
            seen.add(key)
    return result


def safe_relpath(path):
    value = str(path or "").replace("\\", "/").strip("/")
    if not value or value.startswith("../") or "/../" in value or value == "..":
        raise ValueError(f"Unsafe relative path: {path}")
    if value.startswith("note/"):
        value = "notes/" + value.split("/", 1)[1]
    return value


def strip_frontmatter(text):
    return re.sub(r"^---\s*\n[\s\S]*?\n---\s*\n?", "", text or "").strip()


def strip_markdown_frontmatter(text):
    return strip_frontmatter(text)


def read_text_limited(path, max_chars=12000):
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        return ""
    raw = candidate.read_bytes()
    if b"\x00" in raw[:4096]:
        return ""
    return raw.decode("utf-8-sig", errors="replace")[:max_chars]


def classify_summary(title, source_type=""):
    haystack = f"{title} {source_type}".lower()
    for folder, keywords in PAGE_RULES:
        if any(keyword in haystack for keyword in keywords):
            return folder
    return "resources"


def extract_keywords(text, limit=16):
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+.-]{2,}", text or "")
    return unique(tokens)[:limit]


def query_tokens(question):
    raw_tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+.-]{2,}", question or "")
    tokens = set()
    for token in raw_tokens:
        lowered = token.lower()
        tokens.add(lowered)
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) > 3:
            for size in (2, 3, 4):
                for index in range(0, len(token) - size + 1):
                    tokens.add(token[index:index + size])
    return {token for token in tokens if token.strip()}
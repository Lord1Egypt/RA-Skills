from __future__ import annotations

import re
from typing import Any

from bibtex_to_json import gbt_from_entry


SUPPORTED_STYLES = ("gbt7714", "apa", "mla", "chicago", "ieee", "vancouver", "harvard")


def format_reference(entry: dict[str, Any], style: str = "gbt7714") -> str:
    style = normalize_style(style)
    if entry.get("type") == "preformatted" and entry.get("gbt"):
        return str(entry["gbt"])
    if style == "gbt7714":
        return gbt_from_entry(entry)
    if style == "apa":
        return apa(entry)
    if style == "mla":
        return mla(entry)
    if style == "chicago":
        return chicago(entry)
    if style == "ieee":
        return ieee(entry)
    if style == "vancouver":
        return vancouver(entry)
    if style == "harvard":
        return harvard(entry)
    raise ValueError(f"Unsupported citation style: {style}")


def normalize_style(style: str) -> str:
    normalized = style.lower().strip().replace("_", "-")
    aliases = {
        "gb": "gbt7714",
        "gbt": "gbt7714",
        "gb-t": "gbt7714",
        "gb/t": "gbt7714",
        "gb-t-7714": "gbt7714",
        "gb/t-7714": "gbt7714",
        "gbt-7714": "gbt7714",
        "apa7": "apa",
        "apa-7": "apa",
        "mla9": "mla",
        "mla-9": "mla",
        "chicago-author-date": "chicago",
    }
    return aliases.get(normalized, normalized)


def fields(entry: dict[str, Any]) -> dict[str, str]:
    return entry.get("fields") or {}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def sentence(text: str) -> str:
    text = clean(text)
    if not text:
        return ""
    return text if text.endswith((".", "?", "!", "。")) else text + "."


def quoted(text: str) -> str:
    text = clean(text)
    if not text:
        return ""
    return f'"{text}."'


def raw_authors(entry: dict[str, Any]) -> list[str]:
    raw = clean(fields(entry).get("author") or fields(entry).get("editor") or "")
    if not raw:
        return []
    return [part.strip() for part in re.split(r"\s+and\s+", raw) if part.strip()]


def is_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def split_name(name: str) -> tuple[str, str]:
    name = clean(name)
    if "," in name:
        family, given = [part.strip() for part in name.split(",", 1)]
        return family, given
    parts = name.split()
    if len(parts) <= 1 or is_cjk(name):
        return name, ""
    return parts[-1], " ".join(parts[:-1])


def initials(given: str) -> str:
    pieces = re.split(r"[\s\-]+", clean(given))
    return " ".join(piece[0].upper() + "." for piece in pieces if piece)


def authors_apa(entry: dict[str, Any]) -> str:
    authors = raw_authors(entry)
    if not authors:
        return ""
    formatted = []
    for name in authors:
        family, given = split_name(name)
        formatted.append(f"{family}, {initials(given)}".strip().rstrip(","))
    if len(formatted) == 1:
        return formatted[0]
    if len(formatted) == 2:
        return f"{formatted[0]}, & {formatted[1]}"
    return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"


def authors_mla(entry: dict[str, Any]) -> str:
    authors = raw_authors(entry)
    if not authors:
        return ""
    if len(authors) == 1:
        family, given = split_name(authors[0])
        return f"{family}, {given}".strip().rstrip(",")
    first_family, first_given = split_name(authors[0])
    first = f"{first_family}, {first_given}".strip().rstrip(",")
    if len(authors) == 2:
        return f"{first}, and {authors[1]}"
    return f"{first}, et al."


def authors_plain(entry: dict[str, Any]) -> str:
    authors = raw_authors(entry)
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    return ", ".join(authors[:-1]) + f", and {authors[-1]}"


def authors_ieee(entry: dict[str, Any]) -> str:
    authors = raw_authors(entry)
    if not authors:
        return ""
    formatted = []
    for name in authors:
        family, given = split_name(name)
        formatted.append(f"{initials(given)} {family}".strip())
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"


def authors_vancouver(entry: dict[str, Any]) -> str:
    authors = raw_authors(entry)
    formatted = []
    for name in authors[:6]:
        family, given = split_name(name)
        compact_initials = "".join(part[0].upper() for part in re.split(r"[\s\-]+", given) if part)
        formatted.append(f"{family} {compact_initials}".strip())
    if len(authors) > 6:
        formatted.append("et al")
    return ", ".join(formatted)


def get_year(entry: dict[str, Any]) -> str:
    year = clean(fields(entry).get("year") or fields(entry).get("date") or "")
    match = re.search(r"\d{4}", year)
    return match.group(0) if match else year


def pages(entry: dict[str, Any], prefix: str = "") -> str:
    page = clean(fields(entry).get("pages", "")).replace("--", "-")
    return f"{prefix}{page}" if page and prefix else page


def journal(entry: dict[str, Any]) -> str:
    return clean(fields(entry).get("journal") or fields(entry).get("journaltitle") or "")


def volume_issue(entry: dict[str, Any], style: str) -> str:
    volume = clean(fields(entry).get("volume", ""))
    issue = clean(fields(entry).get("number") or fields(entry).get("issue") or "")
    if style in {"apa", "harvard"}:
        if volume and issue:
            return f"{volume}({issue})"
        if volume:
            return volume
        return f"({issue})" if issue else ""
    if style == "mla":
        chunks = []
        if volume:
            chunks.append(f"vol. {volume}")
        if issue:
            chunks.append(f"no. {issue}")
        return ", ".join(chunks)
    if style == "chicago":
        if volume and issue:
            return f"{volume}, no. {issue}"
        return volume or f"no. {issue}" if issue else ""
    if style == "ieee":
        chunks = []
        if volume:
            chunks.append(f"vol. {volume}")
        if issue:
            chunks.append(f"no. {issue}")
        return ", ".join(chunks)
    if style == "vancouver":
        if volume and issue:
            return f"{volume}({issue})"
        if volume:
            return volume
        return f"({issue})" if issue else ""
    return ""


def doi_or_url(entry: dict[str, Any]) -> str:
    doi = clean(fields(entry).get("doi", ""))
    url = clean(fields(entry).get("url", ""))
    if doi:
        return doi if doi.startswith("http") else f"https://doi.org/{doi}"
    return url


def apa(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_apa(entry)
    year = get_year(entry) or "n.d."
    title = sentence(f.get("title", ""))
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    vi = volume_issue(entry, "apa")
    page = pages(entry)
    tail = ", ".join(part for part in [source, vi] if part)
    if page and tail:
        tail = f"{tail}, {page}"
    url = doi_or_url(entry)
    parts = [sentence(author), f"({year}).", title, sentence(tail), url]
    return " ".join(part for part in parts if clean(part)).strip()


def mla(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_mla(entry)
    title = quoted(f.get("title", ""))
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    vi = volume_issue(entry, "mla")
    year = get_year(entry)
    page = pages(entry, "pp. ")
    chunks = [source, vi, year, page]
    source_tail = ", ".join(part for part in chunks if part)
    return " ".join(part for part in [sentence(author), title, sentence(source_tail)] if part).strip()


def chicago(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_plain(entry)
    title = quoted(f.get("title", ""))
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    vi = volume_issue(entry, "chicago")
    year = get_year(entry)
    page = pages(entry)
    source_part = source
    if vi:
        source_part = f"{source_part} {vi}".strip()
    if year:
        source_part = f"{source_part} ({year})".strip()
    if page:
        source_part = f"{source_part}: {page}".strip()
    return " ".join(part for part in [sentence(author), title, sentence(source_part)] if part).strip()


def ieee(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_ieee(entry)
    title = f'"{clean(f.get("title", ""))}"' if clean(f.get("title", "")) else ""
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    vi = volume_issue(entry, "ieee")
    page = pages(entry, "pp. ")
    year = get_year(entry)
    body = ", ".join(part for part in [title, source, vi, page, year] if part)
    return sentence(", ".join(part for part in [author, body] if part))


def vancouver(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_vancouver(entry)
    title = sentence(f.get("title", ""))
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    year = get_year(entry)
    vi = volume_issue(entry, "vancouver")
    page = pages(entry)
    source_part = source
    if year:
        source_part = f"{source_part}. {year}".strip()
    if vi:
        source_part = f"{source_part};{vi}".strip()
    if page:
        source_part = f"{source_part}:{page}".strip()
    return " ".join(part for part in [sentence(author), title, sentence(source_part)] if part).strip()


def harvard(entry: dict[str, Any]) -> str:
    f = fields(entry)
    author = authors_plain(entry)
    year = get_year(entry) or "n.d."
    title = f"'{clean(f.get('title', ''))}'" if clean(f.get("title", "")) else ""
    source = journal(entry) or clean(f.get("booktitle") or f.get("publisher") or "")
    vi = volume_issue(entry, "harvard")
    page = pages(entry, "pp. ")
    tail = ", ".join(part for part in [source, vi, page] if part)
    return " ".join(part for part in [author, f"({year})", title + "," if title and tail else title, sentence(tail)] if part).strip()

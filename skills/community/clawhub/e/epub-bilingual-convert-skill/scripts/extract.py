#!/usr/bin/env python3
import argparse
import json
import posixpath
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from bs4 import NavigableString


HTML_EXTS = (".html", ".htm", ".xhtml")
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp")
SKIP_TEXT_RE = re.compile(
    r"^(previous|next|back to|return to|contents|table of contents|copyright|all rights reserved)$",
    re.I,
)


def norm_text(value):
    value = re.sub(r"\s+", " ", value or "").strip()
    return re.sub(r"\s+([,.;:!?，。；：！？])", r"\1", value)


SUPERSCRIPT_MAP = str.maketrans("0123456789+-=()nijk", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱʲᵏ")
SUBSCRIPT_MAP = str.maketrans(
    "0123456789+-=()aehijklmnoprstuvx",
    "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ",
)
NAMED_SUBSCRIPTS = {
    "A": "ₐ",
    "C": "꜀",
    "H": "ₕ",
    "N": "ₙ",
    "T": "ₜ",
}
GREEK_COMMANDS = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "Delta": "Δ",
    "epsilon": "ε",
    "theta": "θ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "Sigma": "Σ",
    "phi": "φ",
    "psi": "ψ",
    "omega": "ω",
    "Omega": "Ω",
    "hbar": "ℏ",
}
LATEX_SYMBOLS = {
    "approx": "≈",
    "cdot": "·",
    "times": "×",
    "pm": "±",
    "le": "≤",
    "leq": "≤",
    "ge": "≥",
    "geq": "≥",
    "neq": "≠",
    "infty": "∞",
}
SCRIPT_BASE_RE = r"([A-Za-zΑ-ωℏ])"
SCRIPT_TOKEN_RE = r"([A-Za-z0-9](?:[+\-=][A-Za-z0-9]+)?)"


def to_superscript(value):
    return str(value).translate(SUPERSCRIPT_MAP)


def to_subscript(value):
    return "".join(NAMED_SUBSCRIPTS.get(ch, ch.lower().translate(SUBSCRIPT_MAP)) for ch in str(value))


def math_italic(value):
    ch = str(value)
    if len(ch) == 1 and "A" <= ch <= "Z":
        return chr(0x1D434 + ord(ch) - ord("A"))
    if len(ch) == 1 and "a" <= ch <= "z":
        if ch == "h":
            return "ℎ"
        return chr(0x1D44E + ord(ch) - ord("a"))
    return ch


def italicize_math_args(value):
    return re.sub(r"(?<![A-Za-z0-9])([A-Za-z])(?![A-Za-z0-9])", lambda m: math_italic(m.group(1)), value)


def italicize_standalone_math_variables(value):
    return re.sub(r"(?<![A-Za-z0-9])([A-Za-z])(?![A-Za-z0-9])", lambda m: math_italic(m.group(1)), value)


def latex_to_plain(value):
    value = value or ""
    value = value.replace("\n", " ")
    for _ in range(4):
        next_value = value
        next_value = re.sub(r"\\binom\{([^{}]+)\}\{([^{}]+)\}", r"(\1_\2)", next_value)
        next_value = re.sub(r"\\t?frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", next_value)
        next_value = re.sub(r"\\sqrt\{([^{}]+)\}", r"√\1", next_value)
        next_value = re.sub(r"\\expval\{([^{}]+)\}", r"⟨\1⟩", next_value)
        next_value = re.sub(r"\\abs\{([^{}]+)\}", r"|\1|", next_value)
        next_value = re.sub(r"\\text\{([^{}]+)\}", r"\1", next_value)
        if next_value == value:
            break
        value = next_value
    value = value.replace(r"\,", " ").replace(r"\ ", " ")
    value = re.sub(
        r"\\([A-Za-z]+)",
        lambda m: GREEK_COMMANDS.get(m.group(1), LATEX_SYMBOLS.get(m.group(1), m.group(1))),
        value,
    )
    return norm_text(value)


def format_math_text(value):
    value = latex_to_plain(value)
    value = re.sub(r"\b([A-Za-z])[\s_]*rms\b", lambda m: math_italic(m.group(1)) + to_subscript("rms"), value)
    value = re.sub(r"(\d+(?:\.\d+)?)\^(-?\d+)", lambda m: m.group(1) + to_superscript(m.group(2)), value)
    value = re.sub(
        r"\(\^?\{?([A-Za-z0-9]+)\}?_\{?([A-Za-z0-9]+)\}?\)",
        lambda m: "(" + to_superscript(m.group(1)) + to_subscript(m.group(2)) + ")",
        value,
    )
    value = re.sub(
        rf"\b{SCRIPT_BASE_RE}([0-9]+)([A-Z](?:-\d+)?)\b",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)) + to_subscript(m.group(3)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}_\{{([^{{}}]+)\}}\^\{{([^{{}}]+)\}}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(3)) + to_subscript(m.group(2)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}\^\{{([^{{}}]+)\}}_\{{([^{{}}]+)\}}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)) + to_subscript(m.group(3)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}_\{{([^{{}}]+)\}}\^{SCRIPT_TOKEN_RE}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(3)) + to_subscript(m.group(2)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}\^{SCRIPT_TOKEN_RE}_\{{([^{{}}]+)\}}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)) + to_subscript(m.group(3)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}_{SCRIPT_TOKEN_RE}\^{SCRIPT_TOKEN_RE}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(3)) + to_subscript(m.group(2)),
        value,
    )
    value = re.sub(
        rf"{SCRIPT_BASE_RE}\^{SCRIPT_TOKEN_RE}_{SCRIPT_TOKEN_RE}",
        lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)) + to_subscript(m.group(3)),
        value,
    )
    value = re.sub(rf"{SCRIPT_BASE_RE}_\{{([^{{}}]+)\}}", lambda m: math_italic(m.group(1)) + to_subscript(m.group(2)), value)
    value = re.sub(rf"{SCRIPT_BASE_RE}\^\{{([^{{}}]+)\}}", lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)), value)
    value = re.sub(rf"{SCRIPT_BASE_RE}_{SCRIPT_TOKEN_RE}", lambda m: math_italic(m.group(1)) + to_subscript(m.group(2)), value)
    value = re.sub(rf"{SCRIPT_BASE_RE}\^{SCRIPT_TOKEN_RE}", lambda m: math_italic(m.group(1)) + to_superscript(m.group(2)), value)
    value = re.sub(r"\bN([A-Z])\b", lambda m: "𝑁" + to_subscript(m.group(1)), value)
    value = re.sub(r"\b([a-zA-Z])([0-9])(?=\()", lambda m: math_italic(m.group(1)) + to_subscript(m.group(2)), value)
    value = re.sub(r"\b([a-z])([0-9])\b", lambda m: math_italic(m.group(1)) + to_subscript(m.group(2)), value)
    value = re.sub(
        r"\b([A-Za-z])\(([^()]*[A-Za-z][^()]*)\)",
        lambda m: math_italic(m.group(1)) + "(" + italicize_math_args(m.group(2)) + ")",
        value,
    )
    value = italicize_standalone_math_variables(value)
    value = value.replace("{", "").replace("}", "")
    return norm_text(value)


def math_title_to_text(value, formatted=True):
    value = latex_to_plain(value)
    if formatted:
        value = format_math_text(value)
    else:
        value = value.replace("{", "").replace("}", "")
    return norm_text(value)


def paragraph_text(node, formatted=True):
    clone = BeautifulSoup(str(node), "lxml")
    root = clone.find(node.name) or clone
    for math_node in root.select(".eq-inline[title], .svg-inline[title]"):
        math_node.replace_with(NavigableString(f" {math_title_to_text(math_node.get('title'), formatted=formatted)} "))
    return norm_text(root.get_text(" "))


def safe_filename(value, max_len=80):
    value = re.sub(r"[\\/:*?\"<>|\r\n]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return (value[:max_len].strip() or "untitled")


def xml_ns(tag):
    return tag.split("}", 1)[0][1:] if tag.startswith("{") else ""


def find_opf_path(zf):
    try:
        root = ET.fromstring(zf.read("META-INF/container.xml"))
        ns = {"c": xml_ns(root.tag)}
        rootfile = root.find(".//c:rootfile", ns) if ns["c"] else root.find(".//rootfile")
        if rootfile is not None and rootfile.get("full-path"):
            return rootfile.get("full-path")
    except Exception:
        pass
    for name in zf.namelist():
        if name.lower().endswith(".opf"):
            return name
    raise RuntimeError("Could not find OPF file in EPUB")


def parse_opf(zf, opf_path):
    root = ET.fromstring(zf.read(opf_path))
    ns_uri = xml_ns(root.tag)
    ns = {"opf": ns_uri, "dc": "http://purl.org/dc/elements/1.1/"}
    title_el = root.find(".//dc:title", ns)
    epub_title = norm_text(title_el.text if title_el is not None else Path(opf_path).stem)

    manifest = {}
    for item in root.findall(".//opf:manifest/opf:item", ns):
        item_id = item.get("id")
        href = item.get("href")
        if item_id and href:
            manifest[item_id] = {
                "href": posixpath.normpath(posixpath.join(posixpath.dirname(opf_path), href)),
                "media_type": item.get("media-type", ""),
            }

    spine = []
    for itemref in root.findall(".//opf:spine/opf:itemref", ns):
        item = manifest.get(itemref.get("idref"))
        if item:
            spine.append(item["href"])
    return epub_title, manifest, spine


def classify_page(soup, href):
    href_l = href.lower()
    text = norm_text(soup.get_text(" "))
    if "ad_page" in href_l or soup.select(".ad_page, #ad_page") or "ad_page" in str(soup)[:3000].lower():
        return "ad"
    if soup.select_one("ul.calibre_feed_list"):
        return "section_index"
    if "toc" in href_l or "nav" in href_l:
        return "toc"
    if any(token in href_l for token in ("_cvi_", "_tp_", "_cop_", "_ill_", "_ind_")):
        return "other"
    if soup.select_one('[data-testid="article-title"]'):
        return "article"
    if soup.select_one("h1.chapter_title, h1.chapter_head, h2.chapter-title"):
        return "article"
    paragraphs = get_translatable_paragraphs(soup)
    headings = soup.find_all(re.compile("^h[1-3]$"))
    if headings and len(paragraphs) >= 2 and len(text) > 300:
        return "article"
    return "other"


def extract_title(soup):
    title_el = soup.select_one('[data-testid="article-title"]')
    if title_el:
        return norm_text(title_el.get_text(" "))
    title_el = soup.select_one("h2.chapter-title")
    if title_el:
        return norm_text(title_el.get_text(" "))
    title_el = soup.select_one("h1.chapter_title")
    if title_el:
        return norm_text(title_el.get_text(" "))
    heads = [norm_text(h.get_text(" ")) for h in soup.find_all(re.compile("^h[1-3]$"))]
    heads = [h for h in heads if h and not re.fullmatch(r"\d+", h)]
    if len(heads) >= 2 and heads[0].lower() in {"prologue", "introduction", "conclusion", "acknowledgments"}:
        return f"{heads[0]}: {heads[1]}"
    if heads:
        return heads[0]
    doc_title = soup.find("title")
    return norm_text(doc_title.get_text(" ")) if doc_title else "Untitled"


def infer_section(soup, href, current_section=None):
    if current_section:
        return current_section
    href_l = href.lower()
    if re.search(r"_c\d+_", href_l) or soup.select_one("h1.chapter_title, h2.chapter-title"):
        return "Chapter"
    first_head = soup.find(re.compile("^h[1-3]$"))
    if first_head:
        text = norm_text(first_head.get_text(" "))
        if text and not re.fullmatch(r"\d+", text):
            return text
    return "Article"


def is_bad_paragraph(p):
    classes = " ".join(p.get("class", []))
    if "calibre_navbar" in classes or p.find_parent(class_="calibre_navbar"):
        return True
    if p.find_parent(["nav"]):
        return True
    text = paragraph_text(p)
    if not text or SKIP_TEXT_RE.match(text):
        return True
    links = p.find_all("a")
    if links and len(norm_text(" ".join(a.get_text(" ") for a in links))) >= max(1, len(text) - 5):
        return True
    return False


def get_translatable_paragraph_nodes(soup):
    body = soup.body or soup
    nodes = []
    for p in body.find_all(["p", "div"]):
        if p.name == "div" and "para" not in (p.get("class") or []):
            continue
        if is_bad_paragraph(p):
            continue
        text = paragraph_text(p)
        if text:
            nodes.append(p)
    return nodes


def get_translatable_paragraphs(soup):
    return [paragraph_text(p) for p in get_translatable_paragraph_nodes(soup)]


def resolve_zip_path(base_href, src, names):
    if not src:
        return None
    src = src.split("#", 1)[0].split("?", 1)[0]
    candidates = [
        posixpath.normpath(posixpath.join(posixpath.dirname(base_href), src)),
        posixpath.normpath(src.lstrip("/")),
    ]
    for candidate in candidates:
        if candidate in names:
            return candidate
    lower_map = {n.lower(): n for n in names}
    for candidate in candidates:
        found = lower_map.get(candidate.lower())
        if found:
            return found
    return None


def copy_first_image(zf, soup, href, names, summary_dir, num, title):
    seen = set()
    for img in soup.find_all("img"):
        src = img.get("src")
        image_path = resolve_zip_path(href, src, names)
        if not image_path or image_path in seen:
            continue
        seen.add(image_path)
        ext = Path(image_path).suffix.lower()
        if ext not in IMAGE_EXTS:
            ext = ".jpg"
        out_name = f"{num:02d} {safe_filename(title)}{ext}"
        out_path = summary_dir / out_name
        out_path.write_bytes(zf.read(image_path))
        return out_name
    return None


def extract(input_epub, output_dir, target_language):
    input_epub = Path(input_epub).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    summary_dir = output_dir / "summary"
    output_dir.mkdir(parents=True, exist_ok=True)
    if summary_dir.exists():
        shutil.rmtree(summary_dir)
    summary_dir.mkdir(parents=True)

    articles = []
    with zipfile.ZipFile(input_epub) as zf:
        names = set(zf.namelist())
        opf_path = find_opf_path(zf)
        epub_title, manifest, spine = parse_opf(zf, opf_path)
        html_spine = [href for href in spine if href.lower().endswith(HTML_EXTS) and href in names]
        current_section = None

        for href in html_spine:
            soup = BeautifulSoup(zf.read(href).decode("utf-8", errors="ignore"), "lxml")
            page_type = classify_page(soup, href)
            if page_type == "section_index":
                heading = soup.find(re.compile("^h[1-3]$"))
                if heading:
                    current_section = norm_text(heading.get_text(" "))
                continue
            if page_type != "article":
                continue
            paragraphs = get_translatable_paragraphs(soup)
            if not paragraphs:
                continue
            title = extract_title(soup)
            num = len(articles) + 1
            section = infer_section(soup, href, current_section)
            plain_text = "\n\n".join(paragraphs)[:8000]
            image_filename = copy_first_image(zf, soup, href, names, summary_dir, num, title)
            articles.append(
                {
                    "num": num,
                    "title": title,
                    "section": section,
                    "href": href,
                    "paragraphs": paragraphs,
                    "plain_text": plain_text,
                    "image_filename": image_filename,
                    "title_dest_language": None,
                    "section_dest_language": None,
                    "translated_paragraphs": None,
                    "summary_dest_language": None,
                }
            )

    payload = {
        "epub_title": epub_title,
        "input_epub": str(input_epub),
        "output_dir": str(output_dir),
        "target_language": target_language,
        "total_articles": len(articles),
        "articles": articles,
    }
    out_json = output_dir / "extraction.json"
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_json


def main():
    parser = argparse.ArgumentParser(description="Extract structured article/chapter content from an EPUB.")
    parser.add_argument("input_epub")
    parser.add_argument("output_dir")
    parser.add_argument("--target-language", default="Chinese")
    args = parser.parse_args()
    out = extract(args.input_epub, args.output_dir, args.target_language)
    print(out)


if __name__ == "__main__":
    main()

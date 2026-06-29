#!/usr/bin/env python3
import argparse
import copy
import html
import importlib.util
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
CSS_TEXT = (
    "p.dest_translation, .dest_translation { "
    "color: #555; "
    "font-size: smaller !important; "
    "line-height: 1.45 !important; "
    "margin-top: 0.2em !important; "
    "margin-bottom: 0.8em !important; "
    "font-style: normal !important; "
    "break-inside: auto !important; "
    "page-break-inside: auto !important; "
    "overflow: visible !important; "
    "height: auto !important; "
    "max-height: none !important; "
    "}"
    ".dest_translation_equation { "
    "margin-top: 0.1em !important; "
    "margin-bottom: 0.8em !important; "
    "}"
    ".dest_binom { "
    "display: inline-block !important; "
    "vertical-align: middle !important; "
    "white-space: nowrap !important; "
    "font-style: italic !important; "
    "line-height: 1 !important; "
    "}"
    ".dest_binom_paren { "
    "font-style: normal !important; "
    "font-size: 1.45em !important; "
    "line-height: 1 !important; "
    "}"
    ".dest_binom_stack { "
    "display: inline-block !important; "
    "vertical-align: middle !important; "
    "text-align: center !important; "
    "font-size: 0.72em !important; "
    "line-height: 0.95 !important; "
    "margin: 0 0.08em !important; "
    "}"
    ".dest_binom_stack span { "
    "display: block !important; "
    "}"
)
ALIGNMENT_STYLE_PROPS = {
    "margin-left",
    "margin-right",
    "padding-left",
    "padding-right",
    "text-align",
    "text-indent",
}


def norm_text(value):
    value = re.sub(r"\s+", " ", value or "").strip()
    return re.sub(r"\s+([,.;:!?，。；：！？])", r"\1", value)


SUPERSCRIPT_CHARS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱʲᵏ"
SUPERSCRIPT_SOURCE = "0123456789+-=()nijk"
SUBSCRIPT_CHARS = "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ"
SUBSCRIPT_SOURCE = "0123456789+-=()aehijklmnoprstuvx"
SUPERSCRIPT_MAP = str.maketrans(SUPERSCRIPT_SOURCE, SUPERSCRIPT_CHARS)
SUBSCRIPT_MAP = str.maketrans(
    SUBSCRIPT_SOURCE,
    SUBSCRIPT_CHARS,
)
SUPERSCRIPT_REVERSE = dict(zip(SUPERSCRIPT_CHARS, SUPERSCRIPT_SOURCE))
SUBSCRIPT_REVERSE = dict(zip(SUBSCRIPT_CHARS, SUBSCRIPT_SOURCE))
NAMED_SUBSCRIPTS = {
    "A": "ₐ",
    "C": "꜀",
    "H": "ₕ",
    "N": "ₙ",
    "T": "ₜ",
}


def to_superscript(value):
    return str(value).translate(SUPERSCRIPT_MAP)


def to_subscript(value):
    return "".join(NAMED_SUBSCRIPTS.get(ch, ch.lower().translate(SUBSCRIPT_MAP)) for ch in str(value))


def from_superscript(value):
    return "".join(SUPERSCRIPT_REVERSE.get(ch, ch) for ch in str(value))


def from_subscript(value):
    return "".join(SUBSCRIPT_REVERSE.get(ch, ch) for ch in str(value))


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


def format_math_text(value, binomial_formatter=None):
    value = latex_to_plain(value)
    value = re.sub(r"\b([A-Za-z])[\s_]*rms\b", lambda m: math_italic(m.group(1)) + to_subscript("rms"), value)
    value = re.sub(r"(\d+(?:\.\d+)?)\^(-?\d+)", lambda m: m.group(1) + to_superscript(m.group(2)), value)
    value = re.sub(
        r"\(\^?\{?([A-Za-z0-9]+)\}?_\{?([A-Za-z0-9]+)\}?\)",
        lambda m: (
            binomial_formatter(m.group(1), m.group(2))
            if binomial_formatter
            else "(" + to_superscript(m.group(1)) + to_subscript(m.group(2)) + ")"
        ),
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


def normalize_translation_math(value):
    return format_math_text(value)


def translation_math_html(value):
    def encode_marker_text(text):
        return ".".join(str(ord(ch)) for ch in text)

    def decode_marker_text(text):
        return "".join(chr(int(ch)) for ch in text.split(".") if ch)

    value = format_math_text(
        value,
        binomial_formatter=lambda num, den: f"@@{encode_marker_text(num)}:{encode_marker_text(den)}@@",
    )
    value = re.sub(
        rf"\(([{SUPERSCRIPT_CHARS}]+)([{SUBSCRIPT_CHARS}]+)\)",
        lambda m: f"@@{encode_marker_text(from_superscript(m.group(1)))}:{encode_marker_text(from_subscript(m.group(2)))}@@",
        value,
    )
    value = html.escape(value, quote=False)

    def render_binom(match):
        raw_num_text = decode_marker_text(match.group(1))
        raw_den_text = decode_marker_text(match.group(2))
        raw_num = html.escape(raw_num_text, quote=True)
        raw_den = html.escape(raw_den_text, quote=True)
        num = html.escape("".join(math_italic(ch) for ch in raw_num_text), quote=False)
        den = html.escape("".join(math_italic(ch) for ch in raw_den_text), quote=False)
        return (
            f'<span class="dest_binom" data-num="{raw_num}" data-den="{raw_den}">'
            '<span class="dest_binom_paren">(</span>'
            '<span class="dest_binom_stack">'
            f'<span>{num}</span><span>{den}</span>'
            '</span>'
            '<span class="dest_binom_paren">)</span>'
            '</span>'
        )

    return re.sub(r"@@([0-9.]+):([0-9.]+)@@", render_binom, value)


def set_translation_contents(target_p, translation):
    fragment = BeautifulSoup(f"<body>{translation_math_html(translation)}</body>", "lxml")
    for child in list(fragment.body.contents):
        target_p.append(child)


def translation_text_for_validation(node):
    clone = BeautifulSoup(str(node), "lxml")
    root = clone.find(node.name) or clone
    for binom in root.select(".dest_binom[data-num][data-den]"):
        binom.replace_with(
            NavigableString(
                "(" + to_superscript(binom.get("data-num")) + to_subscript(binom.get("data-den")) + ")"
            )
        )
    text = norm_text(root.get_text(" "))
    return re.sub(
        r"(\([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱʲᵏ]+[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ]+\))\s+(?=[\U0001D434-\U0001D467ℎ/])",
        r"\1",
        text,
    )


def safe_filename(value, max_len=80):
    value = re.sub(r"[\\/:*?\"<>|\r\n]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return (value[:max_len].strip() or "untitled")


def filtered_alignment_style(style):
    kept = []
    for declaration in (style or "").split(";"):
        if ":" not in declaration:
            continue
        name, value = declaration.split(":", 1)
        name = name.strip().lower()
        value = value.strip()
        if name in ALIGNMENT_STYLE_PROPS and value:
            kept.append(f"{name}: {value}")
    return "; ".join(kept)


def apply_source_alignment(source_p, target_p):
    classes = source_p.get("class") or []
    if classes:
        target_p["class"] = list(classes) + ["dest_translation"]
    else:
        target_p["class"] = "dest_translation"
    style = filtered_alignment_style(source_p.get("style"))
    if style:
        target_p["style"] = style


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


def load_extractor_module():
    extractor_path = Path(__file__).with_name("extract.py")
    spec = importlib.util.spec_from_file_location("epub_bilingual_extract", extractor_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def count_source_articles(input_epub):
    extractor = load_extractor_module()
    with zipfile.ZipFile(input_epub) as zf:
        names = set(zf.namelist())
        opf_path = extractor.find_opf_path(zf)
        _title, _manifest, spine = extractor.parse_opf(zf, opf_path)
        html_spine = [href for href in spine if href.lower().endswith(HTML_EXTS) and href in names]
        count = 0
        current_section = None
        for href in html_spine:
            soup = BeautifulSoup(zf.read(href).decode("utf-8", errors="ignore"), "lxml")
            page_type = extractor.classify_page(soup, href)
            if page_type == "section_index":
                heading = soup.find(re.compile("^h[1-3]$"))
                if heading:
                    current_section = extractor.norm_text(heading.get_text(" "))
                continue
            if page_type != "article":
                continue
            if extractor.get_translatable_paragraphs(soup):
                count += 1
        return count


def is_ad_page(name, data):
    lower = name.lower()
    if "ad_page" in lower:
        return True
    head = data[:4000].decode("utf-8", errors="ignore").lower()
    return "ad_page" in head


def inject_css(soup):
    if ".dest_translation" in str(soup):
        return
    head = soup.head
    if head is None:
        html_tag = soup.find("html")
        head = soup.new_tag("head")
        if html_tag:
            html_tag.insert(0, head)
        else:
            soup.insert(0, head)
    style = soup.new_tag("style")
    style.string = CSS_TEXT
    head.append(style)


def get_paragraph_nodes(soup, article):
    nodes = []
    wanted = article["paragraphs"]
    idx = 0
    for p in (soup.body or soup).find_all(["p", "div"]):
        if p.name == "div" and "para" not in (p.get("class") or []):
            continue
        if idx >= len(wanted):
            break
        candidates = {
            norm_text(p.get_text(" ")),
            paragraph_text(p, formatted=True),
            paragraph_text(p, formatted=False),
        }
        if norm_text(wanted[idx]) in candidates:
            nodes.append(p)
            idx += 1
    return nodes


def validate_article_pairing(nodes, translations, article):
    expected = len(article.get("paragraphs", []))
    if len(translations) != expected:
        raise RuntimeError(
            f"Article {article['num']} {article['title']} has {len(translations)} translations "
            f"for {expected} source paragraphs"
        )
    if len(nodes) != expected:
        raise RuntimeError(
            f"Article {article['num']} {article['title']} matched {len(nodes)} of "
            f"{expected} source paragraphs"
        )


def validate_bilingual_order(nodes, translations, article):
    for idx, (node, translation) in enumerate(zip(nodes, translations), start=1):
        next_p = node.find_next_sibling("p")
        if next_p is None or "dest_translation" not in next_p.get("class", []):
            raise RuntimeError(
                f"Article {article['num']} {article['title']} paragraph {idx} "
                "does not place target translation immediately after source paragraph"
            )
        if translation_text_for_validation(next_p) != norm_text(normalize_translation_math(translation)):
            raise RuntimeError(
                f"Article {article['num']} {article['title']} paragraph {idx} "
                "target translation text does not match extraction data"
            )


def clone_source_equations_after_translation(source_node, translation_node):
    inserted = translation_node
    for equation in source_node.find_all(class_="eq-num"):
        clone = copy.copy(equation)
        classes = clone.get("class") or []
        clone["class"] = list(classes) + ["dest_translation_equation"]
        inserted.insert_after(clone)
        inserted = clone


def update_title(soup, article):
    bilingual = f"{article['title']} | {article['title_dest_language']}"
    for selector in ('[data-testid="article-title"]', "h1.chapter_title"):
        node = soup.select_one(selector)
        if node:
            node.clear()
            node.string = bilingual
            return
    heads = [h for h in soup.find_all(re.compile("^h[1-3]$")) if norm_text(h.get_text(" "))]
    source_title = article["title"]
    for h in heads:
        if norm_text(h.get_text(" ")) == source_title:
            h.clear()
            h.string = bilingual
            return
    if heads:
        heads[-1].clear()
        heads[-1].string = bilingual


def update_links_and_headings(soup, articles):
    title_map = {a["title"]: f"{a['title']} | {a['title_dest_language']}" for a in articles if a.get("title_dest_language")}
    section_map = {a["section"]: f"{a['section']} | {a['section_dest_language']}" for a in articles if a.get("section_dest_language")}
    combined = {**section_map, **title_map}
    for node in soup.find_all(["a", "h1", "h2", "h3", "span"]):
        text = norm_text(node.get_text(" "))
        replacement = combined.get(text)
        if replacement:
            node.clear()
            node.string = replacement


def process_article_html(data, article):
    soup = BeautifulSoup(data.decode("utf-8", errors="ignore"), "lxml")
    inject_css(soup)
    update_title(soup, article)
    for old in soup.select("p.dest_translation, .dest_translation_equation"):
        old.decompose()
    nodes = get_paragraph_nodes(soup, article)
    translations = article["translated_paragraphs"] or []
    validate_article_pairing(nodes, translations, article)
    for node, translation in zip(nodes, translations):
        new_p = soup.new_tag("p")
        apply_source_alignment(node, new_p)
        set_translation_contents(new_p, translation)
        node.insert_after(new_p)
        clone_source_equations_after_translation(node, new_p)
    validate_bilingual_order(nodes, translations, article)
    return str(soup).encode("utf-8")


def process_other_html(data, articles):
    soup = BeautifulSoup(data.decode("utf-8", errors="ignore"), "lxml")
    inject_css(soup)
    update_links_and_headings(soup, articles)
    return str(soup).encode("utf-8")


def incomplete_articles(articles):
    missing = []
    for a in articles:
        translations = a.get("translated_paragraphs")
        if (
            not a.get("title_dest_language")
            or not a.get("section_dest_language")
            or not translations
            or not a.get("summary_dest_language")
            or len(translations) != len(a.get("paragraphs", []))
            or any(not norm_text(t) for t in translations)
        ):
            missing.append(a)
    return missing


def validate_article_inventory(payload):
    articles = payload.get("articles") or []
    total_articles = payload.get("total_articles")
    if total_articles is not None and len(articles) != total_articles:
        raise RuntimeError(
            f"extraction contains {len(articles)} articles but total_articles is {total_articles}; "
            "refusing to assemble a truncated EPUB"
        )
    input_epub = payload.get("input_epub")
    if input_epub:
        source_count = count_source_articles(Path(input_epub).expanduser().resolve())
        if len(articles) != source_count:
            raise RuntimeError(
                f"source EPUB contains {source_count} translatable articles but extraction contains "
                f"{len(articles)}; refusing to assemble a truncated EPUB"
            )


def write_epub(input_epub, output_epub, article_by_href, articles):
    tmp_epub = output_epub.with_name(f".{output_epub.name}.tmp")
    try:
        with zipfile.ZipFile(input_epub) as zin, zipfile.ZipFile(tmp_epub, "w") as zout:
            names = zin.namelist()
            if "mimetype" in names:
                info = zin.getinfo("mimetype")
                zout.writestr(info, zin.read("mimetype"), compress_type=zipfile.ZIP_STORED)
            for name in names:
                if name == "mimetype":
                    continue
                data = zin.read(name)
                if is_ad_page(name, data):
                    continue
                if name in article_by_href:
                    data = process_article_html(data, article_by_href[name])
                elif name.lower().endswith(HTML_EXTS):
                    data = process_other_html(data, articles)
                info = zin.getinfo(name)
                zout.writestr(info, data)
        tmp_epub.replace(output_epub)
    except Exception:
        tmp_epub.unlink(missing_ok=True)
        raise


def write_summaries(summary_dir, articles):
    summary_dir.mkdir(parents=True, exist_ok=True)
    for a in articles:
        filename = f"{a['num']:02d} {safe_filename(a.get('title_dest_language') or a['title'])}.txt"
        body = f"第{a['num']}篇文章为“{a.get('section_dest_language') or a['section']}”栏目的《{a.get('title_dest_language') or a['title']}》。\n\n{a.get('summary_dest_language') or ''}\n"
        (summary_dir / filename).write_text(body, encoding="utf-8")


def write_report(path, payload, output_epub, missing):
    articles = payload["articles"]
    no_image = [a for a in articles if not a.get("image_filename")]
    with path.open("w", encoding="utf-8") as f:
        f.write(f"EPUB title: {payload.get('epub_title', '')}\n")
        f.write(f"Input EPUB: {payload.get('input_epub', '')}\n")
        f.write(f"Output EPUB: {output_epub}\n")
        f.write(f"Target language: {payload.get('target_language', '')}\n")
        f.write(f"Total articles: {len(articles)}\n")
        f.write(f"Articles with first image: {len(articles) - len(no_image)}\n")
        f.write(f"Articles without first image: {len(no_image)}\n")
        f.write("Missing first image articles:\n")
        for a in no_image:
            f.write(f"- {a['num']}. {a['title']}\n")
        f.write("Untranslated or incomplete articles:\n")
        for a in missing:
            f.write(f"- {a['num']}. {a['title']}\n")


def assemble(extraction_json):
    extraction_json = Path(extraction_json).expanduser().resolve()
    payload = json.loads(extraction_json.read_text(encoding="utf-8"))
    input_epub = Path(payload["input_epub"]).expanduser().resolve()
    output_dir = Path(payload["output_dir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_dir = output_dir / "summary"

    validate_article_inventory(payload)
    articles = payload["articles"]
    missing = incomplete_articles(articles)
    article_by_href = {a["href"]: a for a in articles}
    output_epub = output_dir / f"bilingual_{input_epub.name}"
    write_report(output_dir / "report.txt", payload, output_epub, missing)
    if missing:
        names = ", ".join(f"{a['num']}. {a['title']}" for a in missing[:10])
        raise SystemExit(f"Cannot assemble: untranslated or incomplete articles: {names}")

    write_epub(input_epub, output_epub, article_by_href, articles)
    write_summaries(summary_dir, articles)
    print(output_epub)


def main():
    parser = argparse.ArgumentParser(description="Assemble a bilingual EPUB from extraction.json.")
    parser.add_argument("extraction_json")
    args = parser.parse_args()
    assemble(args.extraction_json)


if __name__ == "__main__":
    main()

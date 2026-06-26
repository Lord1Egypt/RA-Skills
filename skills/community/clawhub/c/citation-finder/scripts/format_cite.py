"""
format_cite.py — Citation formatter
Supports: GB/T 7714-2015, APA 7th edition, MLA 9th edition
"""


def _format_author_gbt(author: dict) -> str:
    """GB/T 7714: 姓名全称，外文姓在前，名缩写."""
    family = author.get("family", "")
    given = author.get("given", "")
    if not family:
        return ""
    # Chinese name (no given name stored separately)
    if not given:
        return family
    # Western name: FAMILY Given → family given (initials)
    given_initials = " ".join(p[0].upper() + "." for p in given.split() if p)
    return f"{family} {given_initials}"


def _format_author_apa(author: dict) -> str:
    """APA 7th: Family, G. I."""
    family = author.get("family", "")
    given = author.get("given", "")
    if not family:
        return ""
    if not given:
        return family
    given_initials = " ".join(p[0].upper() + "." for p in given.split() if p)
    return f"{family}, {given_initials}"


def _format_author_mla(author: dict) -> str:
    """MLA 9th: Family, Given (first author); Given Family (rest)."""
    family = author.get("family", "")
    given = author.get("given", "")
    if not family:
        return ""
    if not given:
        return family
    return f"{family}, {given}"


def format_gbt7714(paper: dict) -> str:
    """
    GB/T 7714-2015 citation format.
    Journal: 作者. 题名[J]. 刊名, 年, 卷(期): 页码. DOI.
    """
    authors = paper.get("authors", [])
    title = paper.get("title", "Unknown Title")
    journal = paper.get("journal", "")
    year = paper.get("year", "")
    volume = paper.get("volume", "")
    issue = paper.get("issue", "")
    pages = paper.get("pages", "")
    doi = paper.get("doi", "")

    # Authors: up to 3, then et al (等)
    author_parts = [_format_author_gbt(a) for a in authors if a.get("family")]
    if len(author_parts) > 3:
        author_str = ", ".join(author_parts[:3]) + ", 等"
    elif author_parts:
        author_str = ", ".join(author_parts)
    else:
        author_str = "佚名"

    doc_type = "[J]" if journal else "[M]"

    citation = f"{author_str}. {title}{doc_type}."
    if journal:
        citation += f" {journal}"
    if year:
        citation += f", {year}"
    if volume:
        citation += f", {volume}"
    if issue:
        citation += f"({issue})"
    if pages:
        citation += f": {pages}"
    citation += "."
    if doi:
        citation += f" DOI: {doi}."

    return citation


def format_apa7(paper: dict) -> str:
    """
    APA 7th edition citation format.
    Journal: Author, A. A., & Author, B. B. (Year). Title. Journal Name, Volume(Issue), Pages. DOI
    """
    authors = paper.get("authors", [])
    title = paper.get("title", "Unknown Title")
    journal = paper.get("journal", "")
    year = paper.get("year", "n.d.")
    volume = paper.get("volume", "")
    issue = paper.get("issue", "")
    pages = paper.get("pages", "")
    doi = paper.get("doi", "")
    url = paper.get("url", "")

    author_parts = [_format_author_apa(a) for a in authors if a.get("family")]
    if len(author_parts) == 1:
        author_str = author_parts[0]
    elif len(author_parts) == 2:
        author_str = " & ".join(author_parts)
    elif len(author_parts) <= 20:
        author_str = ", ".join(author_parts[:-1]) + ", & " + author_parts[-1]
    else:
        author_str = ", ".join(author_parts[:19]) + ", . . . " + author_parts[-1]

    if not author_str:
        author_str = "Unknown Author"

    # Title: sentence case (only capitalize first word and proper nouns)
    title_sc = title[0].upper() + title[1:].lower() if title else title

    citation = f"{author_str} ({year}). {title_sc}."
    if journal:
        vol_issue = ""
        if volume and issue:
            vol_issue = f" {volume}({issue})"
        elif volume:
            vol_issue = f" {volume}"
        page_str = f", {pages}" if pages else ""
        citation += f" *{journal}*,{vol_issue}{page_str}."
    if doi:
        citation += f" https://doi.org/{doi}"
    elif url:
        citation += f" {url}"

    return citation


def format_mla9(paper: dict) -> str:
    """
    MLA 9th edition citation format.
    Journal: Author Last, First, and First Last. "Title." Journal, vol. V, no. N, Year, pp. Pages. DOI.
    """
    authors = paper.get("authors", [])
    title = paper.get("title", "Unknown Title")
    journal = paper.get("journal", "")
    year = paper.get("year", "")
    volume = paper.get("volume", "")
    issue = paper.get("issue", "")
    pages = paper.get("pages", "")
    doi = paper.get("doi", "")
    url = paper.get("url", "")

    author_parts = [_format_author_mla(a) for a in authors if a.get("family")]
    if len(author_parts) == 0:
        author_str = ""
    elif len(author_parts) == 1:
        author_str = author_parts[0] + "."
    elif len(author_parts) == 2:
        author_str = author_parts[0] + ", and " + " ".join(reversed(author_parts[1].split(", "))) + "."
    else:
        author_str = author_parts[0] + ", et al."

    citation = ""
    if author_str:
        citation += author_str + " "
    citation += f'"{title}."'
    if journal:
        citation += f" *{journal}*,"
    if volume:
        citation += f" vol. {volume},"
    if issue:
        citation += f" no. {issue},"
    if year:
        citation += f" {year},"
    if pages:
        citation += f" pp. {pages}."
    else:
        citation = citation.rstrip(",") + "."
    if doi:
        citation += f" doi:{doi}."
    elif url:
        citation += f" {url}."

    return citation


def format_all(paper: dict) -> dict:
    """Return all three citation formats for a paper."""
    return {
        "GB/T 7714": format_gbt7714(paper),
        "APA 7th":   format_apa7(paper),
        "MLA 9th":   format_mla9(paper),
    }


if __name__ == "__main__":
    sample = {
        "title": "Attention Is All You Need",
        "authors": [
            {"given": "Ashish", "family": "Vaswani"},
            {"given": "Noam", "family": "Shazeer"},
            {"given": "Niki", "family": "Parmar"},
            {"given": "Jakob", "family": "Uszkoreit"},
            {"given": "Llion", "family": "Jones"},
            {"given": "Aidan N.", "family": "Gomez"},
            {"given": "Łukasz", "family": "Kaiser"},
            {"given": "Illia", "family": "Polosukhin"},
        ],
        "year": 2017,
        "journal": "Advances in Neural Information Processing Systems",
        "volume": "30",
        "issue": "",
        "pages": "5998-6008",
        "doi": "10.48550/arXiv.1706.03762",
        "url": "https://arxiv.org/abs/1706.03762",
    }
    for fmt, cite in format_all(sample).items():
        print(f"\n【{fmt}】\n{cite}")

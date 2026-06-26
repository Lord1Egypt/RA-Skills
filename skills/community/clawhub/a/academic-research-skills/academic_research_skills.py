"""
academic_research_skills.py — Academic research workflow: plan, research, write, review
Inspired by: Imbad0202/academic-research-skills
"""
import os, json, re, textwrap, datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _safe_input(prompt, default=""):
    try:
        return input(prompt).strip() or default
    except (EOFError, OSError):
        return default


def run(param=""):
    """Run academic research workflow. param: optional research topic"""
    topic = param.strip() or "research topic"
    now = datetime.datetime.now().isoformat()

    sections = {
        "title": topic,
        "abstract": f"A comprehensive study of {topic}.",
        "introduction": f"This paper explores {topic}, covering background, methodology, and findings.",
        "methodology": "Literature review and experimental analysis.",
        "results": "Preliminary findings indicate significant patterns.",
        "discussion": f"The results suggest new directions for {topic} research.",
        "conclusion": f"{topic} remains a promising area for future work.",
        "references": "[1] Sample Reference, 2026\n[2] Another Reference, 2025",
    }

    paper_file = os.path.join(DATA_DIR, f"paper_{datetime.date.today().isoformat()}.json")
    if os.path.exists(paper_file):
        with open(paper_file, "r", encoding="utf-8") as f:
            sections = json.load(f)

    print(f"Academic Research: {topic}")
    print(f"  Template: {len(sections)} sections")
    print(f"  Data dir: {DATA_DIR}")

    result = textwrap.dedent(f"""\
    Paper: {sections['title']}
    Abstract: {sections['abstract'][:80]}...
    Sections: {', '.join(k for k in sections if k != 'title')}
    Saved to: {paper_file}
    """)

    with open(paper_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    return result.strip()


if __name__ == "__main__":
    import sys
    print(run(" ".join(sys.argv[1:])))

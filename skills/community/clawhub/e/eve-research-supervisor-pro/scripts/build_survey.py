#!/usr/bin/env python3
"""
build_survey.py — Generate a proper LaTeX survey paper from research notes
Usage: python3 build_survey.py [notes_file] [output_file] [topic]
"""

import os
import sys
import re
import json
import datetime
import requests

# ── Config ──────────────────────────────────────────────────────────────────
def _get_api_config():
    """Use PetClaw built-in API first, fall back to env vars."""
    settings_path = os.path.expanduser("~/.petclaw/petclaw-settings.json")
    try:
        import json as _j
        with open(settings_path) as f:
            d = _j.load(f)
        key = d.get("brainApiKey", "")
        if key:
            return {
                "key":   key,
                "base":  d.get("brainApiUrl", "https://petclaw.ai/api/v1"),
                "model": os.environ.get("SURVEY_MODEL", d.get("brainModel", "petclaw-1.0"))
            }
    except Exception:
        pass
    return {
        "key":   os.environ.get("OPENAI_API_KEY", ""),
        "base":  os.environ.get("OPENAI_BASE_URL", "https://api.openai-hk.com/v1"),
        "model": os.environ.get("SURVEY_MODEL", "gpt-4o")
    }

_cfg        = _get_api_config()
OPENAI_BASE = _cfg["base"]
OPENAI_KEY  = _cfg["key"]
MODEL       = _cfg["model"]


def generate_survey_llm(notes_text, topic, api_key):
    """Use LLM to write structured survey sections."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert academic writer. Write a structured literature survey "
                    "based on the provided research notes. Output clean LaTeX sections only "
                    "(no \\documentclass, no preamble — just section content). "
                    "Include: Introduction, Related Work, Key Methods, Research Gaps, Future Directions. "
                    "Use proper \\section{}, \\subsection{}, and \\paragraph{} formatting. "
                    "Keep it academic, concise, and well-organized."
                )
            },
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nNotes:\n{notes_text[:6000]}"
            }
        ],
        "temperature": 0.4,
        "max_tokens": 3000
    }
    try:
        r = requests.post(f"{OPENAI_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  ⚠️  LLM call failed: {e}. Using structured template.")
        return None


def build_survey_template(notes_text, topic):
    """Fallback: structured template from notes."""
    # Extract paper titles from notes
    titles = re.findall(r'^## \d+\. (.+)$', notes_text, re.MULTILINE)
    abstracts = re.findall(r'\*\*Abstract:\*\* (.+)', notes_text)

    paper_items = ""
    for i, title in enumerate(titles[:20]):
        paper_items += f"  \\item \\textbf{{{title[:80]}}}\n"
        if i < len(abstracts):
            clean = abstracts[i][:200].replace("&", "\\&").replace("%", "\\%").replace("#", "\\#").replace("_", "\\_")
            paper_items += f"  {clean}...\n\n"

    return f"""
\\section{{Introduction}}
This survey covers recent advances in \\textit{{{topic}}}. 
We reviewed {len(titles)} papers retrieved from arXiv and analyzed their methods, results, and limitations.

\\section{{Related Work}}
\\subsection{{Overview of Key Papers}}
\\begin{{enumerate}}
{paper_items}
\\end{{enumerate}}

\\section{{Key Methods and Approaches}}
The surveyed literature presents a range of approaches. 
We categorize them by their core techniques and evaluate their reported performance.

\\section{{Research Gaps}}
Based on our analysis, several key challenges remain unaddressed in the current literature:
\\begin{{itemize}}
  \\item Lack of standardized benchmarks for evaluating methods under adversarial conditions
  \\item Limited cross-domain generalization of proposed approaches
  \\item Insufficient evaluation on real-world deployment scenarios
\\end{{itemize}}

\\section{{Future Directions}}
Future research should focus on:
\\begin{{itemize}}
  \\item Developing robust evaluation frameworks
  \\item Bridging the gap between theoretical results and practical applications
  \\item Exploring cross-modal and multi-task approaches
\\end{{itemize}}

\\section{{Conclusion}}
This survey provides a comprehensive overview of {topic}. 
We identified {len(titles)} relevant works and highlighted key open problems for future research.
"""


def build_survey(notes_file="notes.md", output_file="survey.tex", topic="AI Research", api_key=None):
    if not os.path.exists(notes_file):
        print(f"❌ {notes_file} not found. Run pdf_parser.py first.")
        sys.exit(1)

    with open(notes_file) as f:
        notes_text = f.read()

    print(f"📝 Building LaTeX survey for topic: {topic}")

    key = api_key or OPENAI_KEY
    body = None

    if key:
        print("  Using LLM to write survey sections...")
        body = generate_survey_llm(notes_text, topic, key)

    if not body:
        print("  Using structured template (fallback)...")
        body = build_survey_template(notes_text, topic)

    # Escape special chars in topic for LaTeX title
    safe_topic = topic.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#").replace("_", "\\_")
    date_str = datetime.date.today().strftime("%B %d, %Y")

    latex = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{hyperref}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\usepackage{{enumitem}}
\\usepackage{{parskip}}

\\title{{Literature Survey: {safe_topic}}}
\\author{{Research Supervisor Pro}}
\\date{{{date_str}}}

\\begin{{document}}
\\maketitle
\\tableofcontents
\\newpage

{body}

\\end{{document}}
"""

    with open(output_file, "w") as f:
        f.write(latex)

    print(f"\n✅ Survey saved → {output_file}")
    print(f"   Compile with: pdflatex {output_file}")
    return output_file


if __name__ == "__main__":
    notes_file  = sys.argv[1] if len(sys.argv) > 1 else "notes.md"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "survey.tex"
    topic       = sys.argv[3] if len(sys.argv) > 3 else "AI Research"
    api_key     = sys.argv[4] if len(sys.argv) > 4 else None
    build_survey(notes_file, output_file, topic, api_key)

#!/usr/bin/env python3
"""
paper_writer.py — Write a full academic paper in LaTeX
Supports: survey papers, research papers with real data, figures, tables, graphs
Usage: python3 paper_writer.py <mode> [options]
  mode: survey    — write literature survey from notes.md
  mode: research  — write research paper from real experimental data
  mode: section   — write a single section
"""

import sys
import os
import json
import re
import datetime
import requests

# ── Config ──────────────────────────────────────────────────────────────────
def _get_api_config():
    """Use PetClaw built-in API first, fall back to env vars."""
    settings_path = os.path.expanduser("~/.petclaw/petclaw-settings.json")
    try:
        with open(settings_path) as f:
            d = json.load(f)
        key = d.get("brainApiKey", "")
        if key:
            return {
                "key":   key,
                "base":  d.get("brainApiUrl", "https://petclaw.ai/api/v1"),
                "model": os.environ.get("PAPER_MODEL", d.get("brainModel", "petclaw-1.0"))
            }
    except Exception:
        pass
    return {
        "key":   os.environ.get("OPENAI_API_KEY", ""),
        "base":  os.environ.get("OPENAI_BASE_URL", "https://api.openai-hk.com/v1"),
        "model": os.environ.get("PAPER_MODEL", "gpt-4o")
    }

_cfg        = _get_api_config()
OPENAI_BASE = _cfg["base"]
OPENAI_KEY  = _cfg["key"]
MODEL       = _cfg["model"]


# ── LLM Helper ──────────────────────────────────────────────────────────────
def llm(system, user, max_tokens=3000, temperature=0.4):
    if not OPENAI_KEY:
        return None
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        r = requests.post(f"{OPENAI_BASE}/chat/completions", headers=headers, json=payload, timeout=90)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  ⚠️  LLM error: {e}")
        return None


# ── LaTeX Preamble ───────────────────────────────────────────────────────────
def latex_preamble(title, authors, abstract, paper_type="survey"):
    date_str = datetime.date.today().strftime("%B %d, %Y")
    safe = lambda s: s.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#").replace("_", "\\_")

    extra_packages = ""
    if paper_type == "research":
        extra_packages = """
\\usepackage{booktabs}
\\usepackage{multirow}
\\usepackage{siunitx}
\\usepackage{subcaption}"""

    return f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{hyperref}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\usepackage{{enumitem}}
\\usepackage{{parskip}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{xcolor}}
\\usepackage{{caption}}
\\usepackage{{natbib}}
\\usepackage{{tabularx}}
\\usepackage{{longtable}}{extra_packages}

\\title{{{safe(title)}}}
\\author{{{safe(authors)}}}
\\date{{{date_str}}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
{safe(abstract)}
\\end{{abstract}}

\\tableofcontents
\\newpage
"""


# ── Figure Generator ─────────────────────────────────────────────────────────
def generate_figures_from_data(data_file, output_dir="figures"):
    """
    Generate matplotlib figures from user's real experimental data.
    data_file: JSON with structure:
      {
        "experiments": [
          {"name": "HiDDeN", "x": [...], "y": [...], "label": "BER vs epochs"},
          ...
        ],
        "tables": [
          {"caption": "Comparison", "headers": [...], "rows": [[...], ...]},
          ...
        ]
      }
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("⚠️  matplotlib not installed. Run: pip install matplotlib numpy")
        return []

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return []

    with open(data_file) as f:
        data = json.load(f)

    figures = []

    for i, exp in enumerate(data.get("experiments", [])):
        fig, ax = plt.subplots(figsize=(8, 5))
        name = exp.get("name", f"Experiment {i+1}")
        x = exp.get("x", [])
        ys = exp.get("y", [])
        label = exp.get("label", "Value")
        xlabel = exp.get("xlabel", "X")
        ylabel = exp.get("ylabel", "Y")

        # Support multiple curves
        if isinstance(ys[0], list) if ys else False:
            labels = exp.get("labels", [f"Series {j}" for j in range(len(ys))])
            for curve, lbl in zip(ys, labels):
                ax.plot(x, curve, marker="o", label=lbl)
            ax.legend()
        else:
            ax.plot(x, ys, marker="o", color="#2196F3", linewidth=2)

        ax.set_title(name, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        fname = f"{output_dir}/fig_{i+1}_{name.lower().replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  📊 Generated figure: {fname}")
        figures.append({"file": fname, "caption": label, "name": name})

    # Bar charts for comparisons
    for i, comp in enumerate(data.get("comparisons", [])):
        fig, ax = plt.subplots(figsize=(9, 5))
        methods = comp.get("methods", [])
        values = comp.get("values", [])
        metric = comp.get("metric", "Score")
        colors = ["#4CAF50" if v == max(values) else "#90CAF9" for v in values]
        bars = ax.bar(methods, values, color=colors, edgecolor="black", linewidth=0.5)
        ax.bar_label(bars, fmt="%.2f", padding=3)
        ax.set_title(comp.get("title", f"Comparison: {metric}"), fontsize=14, fontweight="bold")
        ax.set_ylabel(metric, fontsize=12)
        ax.set_ylim(0, max(values) * 1.15)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        fname = f"{output_dir}/bar_{i+1}_{metric.lower().replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  📊 Generated bar chart: {fname}")
        figures.append({"file": fname, "caption": comp.get("title", metric), "name": metric})

    return figures


def generate_tables_latex(data_file):
    """Generate LaTeX tables from experimental data."""
    if not os.path.exists(data_file):
        return ""

    with open(data_file) as f:
        data = json.load(f)

    latex = ""
    for table in data.get("tables", []):
        caption = table.get("caption", "Results")
        headers = table.get("headers", [])
        rows = table.get("rows", [])
        label = caption.lower().replace(" ", "_")

        col_fmt = "l" + "c" * (len(headers) - 1)
        header_row = " & ".join([f"\\textbf{{{h}}}" for h in headers]) + " \\\\"

        latex += f"""
\\begin{{table}}[H]
\\centering
\\caption{{{caption}}}
\\label{{tab:{label}}}
\\begin{{tabular}}{{{col_fmt}}}
\\toprule
{header_row}
\\midrule
"""
        for row in rows:
            latex += " & ".join([str(cell) for cell in row]) + " \\\\\n"

        latex += f"""\\bottomrule
\\end{{tabular}}
\\end{{table}}

"""
    return latex


# ── Survey Paper Writer ──────────────────────────────────────────────────────
def write_survey(notes_file="notes.md", bib_file=None, topic="AI Research",
                 output="paper_survey.tex", author="Research Supervisor Pro"):

    print(f"📝 Writing survey paper: {topic}")

    with open(notes_file) as f:
        notes = f.read()

    # Load citation graph if available
    graph_context = ""
    if os.path.exists("citation_graph_summary.md"):
        with open("citation_graph_summary.md") as f:
            graph_context = f.read()[:2000]

    # Load top papers
    top_context = ""
    if os.path.exists("top_papers.txt"):
        with open("top_papers.txt") as f:
            top_context = f.read()[:2000]

    context = f"Notes:\n{notes[:5000]}\n\nTop Papers:\n{top_context}\n\nCitation Graph:\n{graph_context}"

    sections = {}
    section_prompts = {
        "abstract": ("Write a 200-word academic abstract for a survey on: " + topic, 400),
        "introduction": ("Write the Introduction section (2-3 paragraphs) for a survey on " + topic + ". Include motivation, scope, and contributions. LaTeX only.", 800),
        "related_work": ("Write the Related Work section with \\subsection{} groupings. Use \\cite{} placeholders. Based on context.", 1500),
        "taxonomy": ("Write a Taxonomy/Categorization section — classify the approaches found in the notes into 3-5 categories with \\subsection{}.", 1200),
        "analysis": ("Write a Comparative Analysis section discussing strengths, weaknesses, and trade-offs of the methods.", 1000),
        "gaps": ("Write a Research Gaps and Open Problems section as a \\begin{itemize} list of specific open problems.", 800),
        "future": ("Write a Future Directions section — specific, concrete, actionable research directions.", 600),
        "conclusion": ("Write a Conclusion section (1-2 paragraphs) summarizing the survey.", 400),
    }

    sys_prompt = (
        "You are an expert academic writer specializing in AI research surveys. "
        "Write in formal academic English. Use LaTeX formatting only — no markdown. "
        "Use \\section{}, \\subsection{}, \\paragraph{} as appropriate. "
        "Include \\cite{AuthorYear} placeholders for references. "
        "Be specific, analytical, and technically precise."
    )

    for sec_key, (prompt, tokens) in section_prompts.items():
        print(f"  ✍️  Writing: {sec_key}...")
        result = llm(sys_prompt, f"{prompt}\n\nContext:\n{context[:4000]}", max_tokens=tokens)
        sections[sec_key] = result or f"% TODO: Write {sec_key} section manually\n"

    # Extract abstract for preamble
    abstract_text = sections.get("abstract", "").replace("\\begin{abstract}", "").replace("\\end{abstract}", "").strip()
    if "abstract" in abstract_text.lower():
        abstract_text = re.sub(r'\\section\{Abstract\}', '', abstract_text).strip()

    # Build full paper
    latex = latex_preamble(f"A Survey on {topic}", author, abstract_text, "survey")

    latex += sections.get("introduction", "") + "\n\n"
    latex += sections.get("related_work", "") + "\n\n"
    latex += sections.get("taxonomy", "") + "\n\n"
    latex += sections.get("analysis", "") + "\n\n"
    latex += sections.get("gaps", "") + "\n\n"
    latex += sections.get("future", "") + "\n\n"
    latex += sections.get("conclusion", "") + "\n\n"

    # Bibliography
    if bib_file and os.path.exists(bib_file):
        latex += f"\n\\bibliographystyle{{plain}}\n\\bibliography{{{bib_file.replace('.bib','')}}}\n"
    else:
        latex += "\n% Add your bibliography file: \\bibliography{references}\n"

    latex += "\n\\end{document}\n"

    with open(output, "w") as f:
        f.write(latex)

    print(f"\n✅ Survey paper written → {output}")
    print(f"   Compile: pdflatex {output}")
    return output


# ── Research Paper Writer (with real data) ───────────────────────────────────
def write_research_paper(data_file=None, notes_file="notes.md", topic="",
                          output="paper_research.tex", author="", venue=""):

    print(f"📝 Writing research paper: {topic}")

    # Generate figures from real data
    figures = []
    tables_latex = ""
    if data_file and os.path.exists(data_file):
        print("  📊 Generating figures and tables from your data...")
        figures = generate_figures_from_data(data_file)
        tables_latex = generate_tables_latex(data_file)
    else:
        print("  ℹ️  No data file provided — paper will have placeholder figures/tables")

    # Load notes
    notes = ""
    if os.path.exists(notes_file):
        with open(notes_file) as f:
            notes = f.read()[:4000]

    # Load ideas/gaps
    ideas = ""
    if os.path.exists("ideas.md"):
        with open("ideas.md") as f:
            ideas = f.read()[:2000]

    context = f"Research topic: {topic}\nVenue: {venue}\nNotes:\n{notes}\nIdeas:\n{ideas}"

    sys_prompt = (
        "You are a senior AI researcher writing a research paper for publication. "
        "Write in formal academic English. Use LaTeX formatting only. "
        "Be technically precise. Use \\cite{} placeholders. "
        "Focus on novelty, methodology, and experimental validation."
    )

    sections = {}
    section_prompts = {
        "abstract": (f"Write a 150-word abstract for a research paper on: {topic}. Mention method, experiments, and key results.", 300),
        "introduction": (f"Write the Introduction section for a research paper on {topic} targeting {venue}. Include problem statement, motivation, contributions (as \\begin{{itemize}}), and paper organization.", 1000),
        "related_work": ("Write Related Work section with \\subsection groupings. Compare with existing methods.", 1000),
        "methodology": (f"Write the Methodology section for the proposed approach to: {topic}. Include formal problem definition, proposed method, algorithm (if applicable).", 1500),
        "experiments": ("Write the Experimental Setup section. Include: datasets used, baselines compared, evaluation metrics, implementation details.", 800),
        "results": ("Write the Results and Analysis section. Reference figures and tables with \\ref{}. Analyze results critically.", 1000),
        "conclusion": (f"Write a Conclusion section for a paper on {topic}. Summarize contributions and future work.", 400),
    }

    for sec_key, (prompt, tokens) in section_prompts.items():
        print(f"  ✍️  Writing: {sec_key}...")
        result = llm(sys_prompt, f"{prompt}\n\nContext:\n{context}", max_tokens=tokens)
        sections[sec_key] = result or f"% TODO: Write {sec_key} section\n"

    abstract_text = sections.get("abstract", "").strip()

    latex = latex_preamble(topic, author, abstract_text, "research")

    latex += sections.get("introduction", "") + "\n\n"
    latex += sections.get("related_work", "") + "\n\n"
    latex += sections.get("methodology", "") + "\n\n"
    latex += sections.get("experiments", "") + "\n\n"

    # Insert real figures
    if figures:
        latex += "\n\\section{Results}\n\n"
        for i, fig in enumerate(figures, 1):
            rel_path = fig["file"]
            cap = fig["caption"].replace("_", "\\_")
            latex += f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.85\\textwidth]{{{rel_path}}}
\\caption{{{cap}}}
\\label{{fig:{i}}}
\\end{{figure}}

"""
        latex += sections.get("results", "") + "\n\n"
    else:
        latex += sections.get("results", "") + "\n\n"
        # Placeholder figure
        latex += """
\\begin{figure}[H]
\\centering
\\fbox{\\parbox{0.7\\textwidth}{\\centering\\vspace{2cm}[Insert Figure Here]\\vspace{2cm}}}
\\caption{Results comparison (placeholder — add your figures)}
\\label{fig:results}
\\end{figure}

"""

    # Insert real tables
    if tables_latex:
        latex += tables_latex
    else:
        # Placeholder table
        latex += """
\\begin{table}[H]
\\centering
\\caption{Performance comparison (placeholder — add your results)}
\\label{tab:results}
\\begin{tabular}{lcccc}
\\toprule
\\textbf{Method} & \\textbf{Metric 1} & \\textbf{Metric 2} & \\textbf{Metric 3} & \\textbf{Metric 4} \\\\
\\midrule
Baseline 1 & - & - & - & - \\\\
Baseline 2 & - & - & - & - \\\\
\\textbf{Ours} & \\textbf{-} & \\textbf{-} & \\textbf{-} & \\textbf{-} \\\\
\\bottomrule
\\end{tabular}
\\end{table}

"""

    latex += sections.get("conclusion", "") + "\n\n"
    latex += "\n% \\bibliographystyle{plain}\n% \\bibliography{references}\n"
    latex += "\n\\end{document}\n"

    with open(output, "w") as f:
        f.write(latex)

    print(f"\n✅ Research paper written → {output}")
    if figures:
        print(f"   Figures: {len(figures)} generated in figures/")
    print(f"   Compile: pdflatex {output}")
    return output


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "survey":
        notes  = sys.argv[2] if len(sys.argv) > 2 else "notes.md"
        topic  = sys.argv[3] if len(sys.argv) > 3 else "AI Research"
        output = sys.argv[4] if len(sys.argv) > 4 else "paper_survey.tex"
        author = sys.argv[5] if len(sys.argv) > 5 else "Author"
        write_survey(notes, None, topic, output, author)

    elif mode == "research":
        topic     = sys.argv[2] if len(sys.argv) > 2 else "AI Research"
        data_file = sys.argv[3] if len(sys.argv) > 3 else None
        output    = sys.argv[4] if len(sys.argv) > 4 else "paper_research.tex"
        author    = sys.argv[5] if len(sys.argv) > 5 else "Author"
        venue     = sys.argv[6] if len(sys.argv) > 6 else "IEEE Transactions"
        write_research_paper(data_file, "notes.md", topic, output, author, venue)

    else:
        print(f"Unknown mode: {mode}")
        print(__doc__)

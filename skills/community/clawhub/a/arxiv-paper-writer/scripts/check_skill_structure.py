from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "templates/arxiv_survey_main.tex",
    "templates/full_survey_main.tex",
    "templates/references.bib",
    "templates/agent_survey_references.bib",
    "templates/agent_survey_figures_tables.tex",
    "references/workflow.md",
    "references/latex_environment.md",
    "references/linux_texlive_full.md",
    "references/bibliography.md",
    "references/figures_and_tables.md",
    "references/quality_review.md",
    "references/agent_survey_practice.md",
    "references/prompt_templates.md",
    "assets/generate_paper_flowchart.png",
    "evals/evals.json",
]


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_FILES if not (base / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    skill_md = (base / "SKILL.md").read_text(encoding="utf-8")
    if not skill_md.startswith("---\nname: arxiv-paper-writer\n"):
        print("SKILL.md frontmatter is missing the expected name")
        return 1
    if "description:" not in skill_md:
        print("SKILL.md frontmatter is missing description")
        return 1

    print("arxiv-paper-writer skill structure ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

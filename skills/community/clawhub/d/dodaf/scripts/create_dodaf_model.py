#!/usr/bin/env python3
"""Generate a DoDAF architecture model with consolidated report output.

Usage:
    python scripts/create_dodaf_model.py [output_dir] [--format pdf|docx|html|md]

Features:
    - Creates complete DoDAF 2.0/2.1 project structure
    - Generates per-phase Markdown documents and draw.io diagrams
    - Assembles consolidated report from all phases
    - Converts to PDF/DOCX/HTML via pandoc (if available)
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


def rand_id():
    return "_" + os.urandom(8).hex()


def create_project_structure(output_dir: str, project_name: str) -> dict:
    """Create the DoDAF project directory structure."""
    base = Path(output_dir) / project_name
    dirs = {
        "docs": base / "docs",
        "diagrams": base / "diagrams",
        "report": base / "report",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def create_dodaf_model(output_dir: str = ".", project_name: str = "dodaf-model") -> str:
    """Create a minimal DoDAF architecture description."""
    dirs = create_project_structure(output_dir, project_name)
    docs_dir = dirs["docs"]
    diagrams_dir = dirs["diagrams"]

    # DoDAF viewpoint definitions
    dodaf_views = {
        "AV": {
            "name": "All Viewpoint",
            "description": "Overview, summary, and context for the architecture description",
            "products": [
                {"id": "AV-1", "name": "Overview and Summary Information", "type": "diagram+doc"},
                {"id": "AV-2", "name": "Integrated Dictionary", "type": "doc"},
                {"id": "AV-3", "name": "Concept of Operations (CONOPS)", "type": "doc"},
            ]
        },
        "OV": {
            "name": "Operational Viewpoint",
            "description": "Operational scenarios, activities, and information flows",
            "products": [
                {"id": "OV-1", "name": "High-Level Operational Concept Graphic", "type": "diagram+doc"},
                {"id": "OV-2", "name": "Operational Resource Flow Description", "type": "diagram+doc"},
                {"id": "OV-3", "name": "Operational Information Exchange Matrix", "type": "doc"},
                {"id": "OV-5", "name": "Operational Activity Model", "type": "diagram+doc"},
            ]
        },
        "CV": {
            "name": "Capability Viewpoint",
            "description": "Capability taxonomy and dependencies",
            "products": [
                {"id": "CV-1", "name": "Capability Taxonomy", "type": "diagram+doc"},
                {"id": "CV-2", "name": "Capability Phasing", "type": "diagram+doc"},
                {"id": "CV-3", "name": "Capability Dependencies", "type": "diagram+doc"},
            ]
        },
        "SV": {
            "name": "Systems Viewpoint",
            "description": "System functions, interfaces, and data exchanges",
            "products": [
                {"id": "SV-1", "name": "Systems Interface Description", "type": "diagram+doc"},
                {"id": "SV-2", "name": "Systems Communication Description", "type": "diagram+doc"},
                {"id": "SV-4", "name": "Systems Functionality Description", "type": "diagram+doc"},
                {"id": "SV-5", "name": "Operational Activity to Systems Function Traceability", "type": "doc"},
            ]
        },
        "DIV": {
            "name": "Data and Information Viewpoint",
            "description": "Data models, schemas, and information exchanges",
            "products": [
                {"id": "DIV-1", "name": "Data Model Description", "type": "diagram+doc"},
                {"id": "DIV-2", "name": "Data Dictionary", "type": "doc"},
                {"id": "DIV-3", "name": "Data Exchange Matrix", "type": "doc"},
            ]
        },
        "PV": {
            "name": "Project Viewpoint",
            "description": "Acquisition strategy, timeline, and milestones",
            "products": [
                {"id": "PV-1", "name": "Project Timeline", "type": "diagram+doc"},
                {"id": "PV-2", "name": "Project Structure", "type": "diagram+doc"},
                {"id": "PV-3", "name": "Project Resource Flow", "type": "diagram+doc"},
            ]
        },
        "TV": {
            "name": "Technical Viewpoint",
            "description": "Technical standards, technologies, and implementation constraints",
            "products": [
                {"id": "TV-1", "name": "Technical Standards Profile", "type": "doc"},
                {"id": "TV-2", "name": "Technical Measures", "type": "doc"},
                {"id": "TV-3", "name": "Technical Architecture Framework", "type": "diagram+doc"},
            ]
        },
    }

    # Create model metadata
    model_content = f"""# DoDAF Architecture Description
# Model Name: {project_name}
# Generated: {datetime.now().isoformat()}

## Overview
This is a DoDAF architecture model demonstrating all required viewpoints.

## Viewpoints

"""
    for vp_code, vp_data in dodaf_views.items():
        model_content += f"### {vp_code} ({vp_data['name']})\n"
        model_content += f"Description: {vp_data['description']}\n"
        model_content += "Products:\n"
        for product in vp_data["products"]:
            model_content += f"- {product['id']}: {product['name']}\n"
        model_content += "\n"

    # Add traceability matrix template
    model_content += """## Traceability Matrix

| Capability | Operational Activity | System Function | Data Element | Interface | Technical Standard | Project Milestone |
|------------|---------------------|-----------------|--------------|-----------|-------------------|-------------------|
|            |                     |                 |              |           |                   |                   |

## Glossary

| Term | Definition |
|------|------------|
| DoDAF | Department of Defense Architecture Framework |
| View | A representation of a system from a specific perspective |
| Product | A specific deliverable within a viewpoint |

## Standards Compliance

- DoDAF 2.0 / 2.1
- IEEE 1471-2000
- NIST SP 800-53

## Security Classification

- Classification: UNCLASSIFIED
- Caveats: None

"""
    (docs_dir / "DODAF_MODEL.md").write_text(model_content, encoding="utf-8")

    # Create traceability CSV
    (docs_dir / "traceability_matrix.csv").write_text(
        "Capability,Operational Activity,System Function,Data Element,Interface,Technical Standard,Project Milestone\n"
        ",,,,,\n",
        encoding="utf-8"
    )

    print(f"DoDAF model created: {docs_dir / 'DODAF_MODEL.md'}")
    return str(docs_dir / "DODAF_MODEL.md")


def assemble_consolidated_report(project_dir: str, project_name: str) -> str:
    """Assemble all phase documents into a single consolidated Markdown report.

    Reads all docs/*.md files, orders them by chapter, and merges into one file.
    """
    docs_dir = Path(project_dir) / "docs"
    report_dir = Path(project_dir) / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    # Define chapter ordering
    chapter_order = [
        "01-stakeholder-context.md",
        "02-operational-analysis.md",
        "03-capability-definition.md",
        "04-system-design.md",
        "05-data-architecture.md",
        "06-technical-architecture.md",
        "07-project-planning.md",
        "08-integration-verification.md",
        "OV-3-information-exchange-matrix.md",
        "SV-5-traceability-matrix.md",
        "DIV-2-data-dictionary.md",
        "DIV-3-data-exchange-matrix.md",
        "TV-1-technical-standards.md",
        "TV-2-technical-measures.md",
        "AV-2-integrated-dictionary.md",
        "AV-3-conops.md",
        "traceability-matrix.md",
    ]

    # Build consolidated report
    report_lines = [
        f"# {project_name} DoDAF Architecture Description Report",
        "",
        "## Document Control",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Project Name | {project_name} |",
        f"| Framework | DoDAF 2.0/2.1 |",
        f"| Version | 1.0 |",
        f"| Date | {datetime.now().strftime('%Y-%m-%d')} |",
        f"| Classification | UNCLASSIFIED |",
        "",
        "---",
        "",
    ]

    # Add table of contents placeholder
    report_lines.extend([
        "## Table of Contents",
        "",
        "- Chapter 1: Stakeholder & Context Analysis",
        "- Chapter 2: Operational Architecture (OV)",
        "- Chapter 3: Capability Architecture (CV)",
        "- Chapter 4: Systems Architecture (SV)",
        "- Chapter 5: Data Architecture (DIV)",
        "- Chapter 6: Technical Architecture (TV)",
        "- Chapter 7: Project Planning (PV)",
        "- Chapter 8: Integration & Verification",
        "- Chapter 9: Concept of Operations (CONOPS)",
        "- Appendix A: Integrated Dictionary",
        "- Appendix B: Technical Standards Reference",
        "- Appendix C: Data Dictionary",
        "- Appendix D: Traceability Matrix",
        "",
        "---",
        "",
    ])

    # Append each chapter document
    for filename in chapter_order:
        filepath = docs_dir / filename
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            report_lines.append(content)
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

    # Write consolidated report
    report_path = report_dir / "consolidated-report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Consolidated report assembled: {report_path}")
    return str(report_path)


def convert_report(report_md: str, output_format: str) -> str:
    """Convert consolidated Markdown report to PDF/DOCX/HTML using pandoc."""
    report_path = Path(report_md)
    output_dir = report_path.parent

    format_config = {
        "pdf": {
            "ext": ".pdf",
            "args": [
                "--pdf-engine=xelatex",
                '-V', 'mainfont="SimSun"',
                '-V', 'geometry:margin=2.5cm',
                '--toc', '--toc-depth=3',
                '-V', 'numbersections',
            ]
        },
        "docx": {
            "ext": ".docx",
            "args": [
                '--toc', '--toc-depth=3',
            ]
        },
        "html": {
            "ext": ".html",
            "args": [
                '--standalone',
                '--toc', '--toc-depth=3',
                '--metadata', 'title=DoDAF Architecture Report',
            ]
        },
    }

    if output_format not in format_config:
        print(f"Unsupported format: {output_format}")
        return ""

    config = format_config[output_format]
    output_file = output_dir / f"{report_path.stem}{config['ext']}"

    cmd = ["pandoc", str(report_path), "-o", str(output_file)] + config["args"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"Report converted to {output_format.upper()}: {output_file}")
            return str(output_file)
        else:
            print(f"Pandoc error: {result.stderr}")
            return ""
    except FileNotFoundError:
        print("Pandoc not found. Install from https://pandoc.org/installing.html")
        return ""
    except subprocess.TimeoutExpired:
        print("Pandoc conversion timed out")
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DoDAF architecture model")
    parser.add_argument("output_dir", nargs="?", default=".", help="Output directory")
    parser.add_argument("--name", default="dodaf-model", help="Project name")
    parser.add_argument("--format", choices=["pdf", "docx", "html", "md"], default="md",
                        help="Output format for consolidated report")
    args = parser.parse_args()

    # Create model
    model_path = create_dodaf_model(args.output_dir, args.name)

    # Assemble consolidated report
    project_dir = str(Path(args.output_dir) / args.name)
    report_path = assemble_consolidated_report(project_dir, args.name)

    # Convert to requested format
    if args.format != "md":
        convert_report(report_path, args.format)

    print(f"\nModel created successfully!")
    print(f"Location: {project_dir}")

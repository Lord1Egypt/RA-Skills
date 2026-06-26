#!/usr/bin/env python3
"""
venue_checklist.py — Feature 6: Venue-Specific Paper Checklists
Generates a checklist of requirements for your target venue.
Built-in knowledge of major AI/ML venues.
Usage:
  python3 venue_checklist.py <venue_name>
  python3 venue_checklist.py list           — show all supported venues
  python3 venue_checklist.py check <project> <venue>  — save checklist to project
"""

import sys
import os
import json
import datetime

BASE = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro/research")

# ── Venue Database ────────────────────────────────────────────────────────────
VENUES = {
    "ieee tifs": {
        "full_name": "IEEE Transactions on Information Forensics and Security",
        "type": "journal",
        "impact": "Q1, IF ~6.8",
        "pages": "10-14 pages (double column)",
        "abstract_limit": "250 words",
        "review_type": "Double-blind",
        "turnaround": "3-6 months",
        "requirements": [
            "Double-column IEEE format",
            "Abstract max 250 words",
            "Keywords: 5-10 IEEE Terms",
            "Must include: thorough related work section",
            "Must include: ablation study",
            "Must include: comparison vs at least 3 baselines",
            "Must include: statistical significance analysis",
            "Ethics statement if human subjects involved",
            "Code/data availability statement recommended",
            "Supplementary material allowed (unlimited)",
            "No page limit for references",
        ],
        "avoid": [
            "Overclaiming — avoid 'state-of-the-art' without proof",
            "Missing ablation study — reviewers will reject",
            "Only 1-2 baselines — minimum 3 required",
            "Weak evaluation — must test on multiple datasets",
        ],
        "tips": [
            "TIFS reviewers are security-focused — frame contributions in security context",
            "Include threat model section",
            "Show robustness to both known and unknown attacks",
            "Reproducibility is valued — share code",
        ]
    },
    "neurips": {
        "full_name": "Neural Information Processing Systems",
        "type": "conference",
        "impact": "Top-tier, A*",
        "pages": "9 pages (content) + unlimited references",
        "abstract_limit": "150 words (submission system)",
        "review_type": "Double-blind",
        "turnaround": "~4 months",
        "requirements": [
            "NeurIPS LaTeX template (required)",
            "9 pages max for main paper",
            "Unlimited pages for references",
            "Supplementary appendix allowed",
            "Abstract max 150 words in system",
            "Reproducibility checklist must be completed",
            "Broader impact statement required",
            "Limitations section strongly recommended",
            "Must release code/data for reproducibility",
            "Checklist: theory / experiments / dataset / model",
        ],
        "avoid": [
            "No limitations section — red flag for reviewers",
            "Missing reproducibility checklist",
            "Vague experimental setup — be very specific",
            "No broader impact — required since 2020",
        ],
        "tips": [
            "NeurIPS values novelty + theoretical depth",
            "Include proofs in appendix if you have theory",
            "Strong empirical results matter as much as theory",
            "Clear, clean figures — reviewers read on laptop screens",
        ]
    },
    "cvpr": {
        "full_name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
        "type": "conference",
        "impact": "Top-tier, A*",
        "pages": "8 pages + references",
        "abstract_limit": "~200 words",
        "review_type": "Double-blind",
        "turnaround": "~3 months",
        "requirements": [
            "CVPR LaTeX template (required)",
            "8 pages max (main) + unlimited references",
            "Supplementary up to 100MB",
            "Anonymous submission (no author names)",
            "Must not cite your own non-anonymous work",
            "Good quality figures — this is a vision venue",
            "Ablation study expected",
            "Comparison to recent methods (within 2 years)",
        ],
        "avoid": [
            "Low quality figures — CVPR is a visual venue",
            "Old baselines — must compare to recent methods",
            "Missing ablation",
            "Citing your own previous work non-anonymously",
        ],
        "tips": [
            "Visual results sell papers — invest in figures",
            "Include failure cases in supplementary",
            "User study or perceptual quality metrics valued",
            "Teaser figure on page 1 is critical",
        ]
    },
    "iccv": {
        "full_name": "International Conference on Computer Vision",
        "type": "conference",
        "impact": "Top-tier, A*",
        "pages": "8 pages + references",
        "abstract_limit": "~200 words",
        "review_type": "Double-blind",
        "turnaround": "~4 months",
        "requirements": [
            "ICCV LaTeX template",
            "8 pages max + unlimited references",
            "Supplementary material allowed",
            "Double-blind submission",
            "High-quality experimental evaluation",
            "Ablation study expected",
        ],
        "avoid": ["Similar to CVPR — see CVPR checklist"],
        "tips": ["Similar to CVPR — visual quality of results is key"]
    },
    "acm mm": {
        "full_name": "ACM International Conference on Multimedia",
        "type": "conference",
        "impact": "Top-tier multimedia, A",
        "pages": "8 pages + 2 for references",
        "abstract_limit": "150 words",
        "review_type": "Double-blind",
        "turnaround": "~3 months",
        "requirements": [
            "ACM template",
            "8 pages content + 2 pages references",
            "Multimodal evaluation preferred",
            "Demo/system paper track available",
            "Reproducibility encouraged",
        ],
        "avoid": [
            "Single-modal experiments for a multimedia venue",
            "Missing perceptual quality evaluation",
        ],
        "tips": [
            "Strong for watermarking — security + multimedia intersection",
            "Include perceptual quality metrics (PSNR, SSIM, LPIPS)",
        ]
    },
    "ieee tsp": {
        "full_name": "IEEE Transactions on Signal Processing",
        "type": "journal",
        "impact": "Q1, IF ~5.4",
        "pages": "12-14 pages double column",
        "abstract_limit": "200 words",
        "review_type": "Single-blind",
        "turnaround": "4-8 months",
        "requirements": [
            "IEEE double-column format",
            "Strong mathematical formulation required",
            "Theoretical analysis valued",
            "Comprehensive experiments",
            "Must include complexity analysis",
        ],
        "avoid": [
            "Weak mathematical contribution",
            "Missing theoretical bounds or analysis",
        ],
        "tips": [
            "TSP values signal processing theory — formalize your method mathematically",
            "Include convergence analysis if optimization-based",
        ]
    },
    "thesis": {
        "full_name": "Master's / PhD Thesis",
        "type": "thesis",
        "impact": "Academic degree requirement",
        "pages": "60-150 pages typically",
        "abstract_limit": "300-500 words",
        "review_type": "Committee review",
        "turnaround": "Per university schedule",
        "requirements": [
            "University LaTeX/Word template",
            "Full literature review chapter",
            "Methodology chapter",
            "Experiments chapter with all details",
            "Conclusion and future work",
            "Complete bibliography",
            "List of figures and tables",
            "Acknowledgements section",
            "Declaration of originality",
            "All code and data archived",
        ],
        "avoid": [
            "Insufficient related work — committees expect exhaustive review",
            "Missing implementation details — must be reproducible",
            "No future work section",
        ],
        "tips": [
            "Include a chapter introduction and summary for each chapter",
            "Be verbose — more detail is better than less for a thesis",
            "Add a glossary for all technical terms",
            "Include negative results — shows thorough investigation",
        ]
    }
}


def normalize_venue(name):
    return name.lower().strip()


def get_venue(name):
    norm = normalize_venue(name)
    # Exact match
    if norm in VENUES:
        return VENUES[norm]
    # Partial match
    for key in VENUES:
        if key in norm or norm in key:
            return VENUES[key]
    return None


def show_checklist(venue_name):
    venue = get_venue(venue_name)
    if not venue:
        print(f"❌ Venue '{venue_name}' not found.")
        print(f"   Supported: {', '.join(VENUES.keys())}")
        print(f"   Or use 'thesis' for thesis format")
        return None

    print(f"\n📋 VENUE CHECKLIST: {venue['full_name']}")
    print(f"   Type: {venue['type']} | Impact: {venue['impact']}")
    print(f"   Pages: {venue['pages']} | Abstract: {venue['abstract_limit']}")
    print(f"   Review: {venue['review_type']} | Turnaround: {venue['turnaround']}")
    print()

    print("✅ REQUIREMENTS:")
    for req in venue["requirements"]:
        print(f"   [ ] {req}")

    print("\n❌ AVOID:")
    for avoid in venue["avoid"]:
        print(f"   ⚠️  {avoid}")

    print("\n💡 TIPS:")
    for tip in venue["tips"]:
        print(f"   → {tip}")

    print()
    return venue


def save_to_project(project, venue_name):
    venue = get_venue(venue_name)
    if not venue:
        print(f"❌ Venue not found: {venue_name}")
        return

    project_dir = os.path.join(BASE, project)
    os.makedirs(project_dir, exist_ok=True)
    checklist_path = os.path.join(project_dir, "venue_checklist.md")

    with open(checklist_path, "w") as f:
        f.write(f"# 📋 Venue Checklist: {venue['full_name']}\n\n")
        f.write(f"**Type:** {venue['type']}  \n")
        f.write(f"**Impact:** {venue['impact']}  \n")
        f.write(f"**Pages:** {venue['pages']}  \n")
        f.write(f"**Abstract limit:** {venue['abstract_limit']}  \n")
        f.write(f"**Review type:** {venue['review_type']}  \n\n")

        f.write("## ✅ Requirements\n\n")
        for req in venue["requirements"]:
            f.write(f"- [ ] {req}\n")

        f.write("\n## ❌ Avoid\n\n")
        for avoid in venue["avoid"]:
            f.write(f"- ⚠️  {avoid}\n")

        f.write("\n## 💡 Tips\n\n")
        for tip in venue["tips"]:
            f.write(f"- {tip}\n")

        f.write(f"\n---\n*Generated by EVE — {datetime.date.today()}*\n")

    print(f"✅ Checklist saved → {checklist_path}")
    return checklist_path


def list_venues():
    print("\n📋 SUPPORTED VENUES:")
    print("━" * 50)
    for key, v in VENUES.items():
        print(f"  {key:<15} {v['full_name'][:45]}")
    print("━" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        list_venues()
    elif sys.argv[1] == "check" and len(sys.argv) >= 4:
        save_to_project(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 2:
        show_checklist(" ".join(sys.argv[1:]))
    else:
        print(__doc__)

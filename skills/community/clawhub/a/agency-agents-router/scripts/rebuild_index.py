#!/usr/bin/env python3
"""
Rebuild agents.json: parse agency-agents-zh README and individual agent markdown
files, cross-reference with openclaw.json to produce a searchable agent lookup table.

Usage:
  python3 rebuild_index.py                           # Use cached README, find local repo
  python3 rebuild_index.py --fetch                   # Fetch latest README from GitHub
  python3 rebuild_index.py --repo /path/to/agency-agents-zh  # Specify repo location
  python3 rebuild_index.py --clone                   # Clone agency-agents-zh to /tmp

Output: agents.json (in the same directory as this script's parent)
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
AGENTS_JSON = os.path.join(SKILL_DIR, "agents.json")
README_CACHE = os.path.join(SKILL_DIR, ".readme_cache.md")
README_URL = (
    "https://raw.githubusercontent.com/jnMetaCode/agency-agents-zh/main/README.md"
)
REPO_URL = "https://github.com/jnMetaCode/agency-agents-zh.git"
DEFAULT_REPO_PATHS = [
    os.path.join(SKILL_DIR, "agency-agents-zh"),
    os.path.expanduser("~/agency-agents-zh"),
    "/tmp/agency-agents-zh",
]

# Agents in openclaw.json that are NOT described in agency-agents-zh README.
# These come from the upstream English repo (github.com/msitarzewski/agency-agents).
UPSTREAM_FALLBACK = {
    "engineering-codebase-onboarding-engineer": {
        "name_zh": "Codebase Onboarding Engineer",
        "description": "Expert in codebase analysis, architecture documentation, and rapid onboarding to unfamiliar codebases.",
        "expertise": "Codebase analysis, architecture documentation, rapid onboarding",
        "scenario": "Legacy system onboarding, knowledge transfer",
    },
    "engineering-minimal-change-engineer": {
        "name_zh": "Minimal Change Engineer",
        "description": "Specialist in minimal, surgical code changes with risk-controlled modifications for production systems.",
        "expertise": "Minimal changes, incremental refactoring, risk-controlled modifications",
        "scenario": "Production-safe changes, surgical fixes",
    },
    "engineering-voice-ai-integration-engineer": {
        "name_zh": "Voice AI Integration Engineer",
        "description": "Expert in speech recognition, TTS, and conversational AI integration for voice interfaces.",
        "expertise": "Speech recognition, TTS, conversational AI integration",
        "scenario": "Voice assistants, call center AI, voice interfaces",
    },
    "finance-bookkeeper-controller": {
        "name_zh": "Bookkeeper Controller",
        "description": "Expert in bookkeeping, financial statements, and internal controls for corporate accounting.",
        "expertise": "Bookkeeping, financial statements, internal controls",
        "scenario": "Daily accounting, financial compliance",
    },
    "finance-financial-analyst": {
        "name_zh": "Financial Analyst",
        "description": "Expert in financial statement analysis, ratio analysis, and budgeting for corporate finance.",
        "expertise": "Financial statements, ratio analysis, budgeting",
        "scenario": "Financial reporting, performance evaluation",
    },
    "finance-fpa-analyst": {
        "name_zh": "FP&A Analyst",
        "description": "Specialist in financial planning and analysis, budgeting, and forecasting for organizations.",
        "expertise": "Financial planning & analysis, budgeting, forecasting",
        "scenario": "Corporate financial planning",
    },
    "finance-investment-researcher": {
        "name_zh": "Investment Researcher",
        "description": "Expert in industry research, valuation models, and investment recommendations.",
        "expertise": "Industry research, valuation models, investment recommendations",
        "scenario": "Investment decision support",
    },
    "finance-tax-strategist": {
        "name_zh": "Tax Strategist",
        "description": "Specialist in tax planning, compliance filing, and tax optimization strategies.",
        "expertise": "Tax planning, compliance filing, tax optimization",
        "scenario": "Corporate tax optimization",
    },
    "healthcare-customer-service": {
        "name_zh": "Healthcare Customer Service",
        "description": "Expert in patient services, appointment management, and medical inquiry handling.",
        "expertise": "Patient services, appointment management, medical inquiries",
        "scenario": "Healthcare customer support",
    },
    "hospitality-guest-services": {
        "name_zh": "Hospitality Guest Services",
        "description": "Specialist in guest services, reservation management, and complaint handling for hospitality.",
        "expertise": "Guest services, reservation management, complaint handling",
        "scenario": "Hospitality customer service",
    },
    "hr-onboarding": {
        "name_zh": "HR Onboarding Specialist",
        "description": "Expert in new employee onboarding, culture training, and orientation program design.",
        "expertise": "New employee onboarding, culture training, orientation programs",
        "scenario": "Employee onboarding and integration",
    },
    "language-translator": {
        "name_zh": "Language Translator",
        "description": "Expert in multilingual translation, localization, and terminology management.",
        "expertise": "Multilingual translation, localization, terminology management",
        "scenario": "Translation and localization",
    },
    "legal-billing-time-tracking": {
        "name_zh": "Legal Billing & Time Tracking",
        "description": "Specialist in attorney time tracking, invoice generation, and UTBMS coding for law firms.",
        "expertise": "Attorney time tracking, invoice generation, UTBMS coding",
        "scenario": "Law firm billing management",
    },
    "legal-client-intake": {
        "name_zh": "Legal Client Intake",
        "description": "Expert in client intake, conflict checks, and case classification for law firms.",
        "expertise": "Client intake, conflict checks, case classification",
        "scenario": "Law firm client management",
    },
    "legal-document-review": {
        "name_zh": "Legal Document Reviewer",
        "description": "Specialist in document review, privilege log creation, and legal terminology analysis.",
        "expertise": "Document review, privilege log, terminology analysis",
        "scenario": "Litigation document review",
    },
    "livestock-archive-auditor": {
        "name_zh": "Livestock Archive Auditor",
        "description": "Expert in livestock archive auditing, quarantine records, and feed ledger compliance.",
        "expertise": "Livestock archive audit, quarantine records, feed ledgers",
        "scenario": "Animal husbandry compliance",
    },
    "loan-officer-assistant": {
        "name_zh": "Loan Officer Assistant",
        "description": "Specialist in loan applications, credit assessment, and document processing.",
        "expertise": "Loan applications, credit assessment, document processing",
        "scenario": "Loan services",
    },
    "marketing-agentic-search-optimizer": {
        "name_zh": "Agentic Search Optimizer",
        "description": "Expert in AI search optimization and brand visibility across AI-powered search platforms.",
        "expertise": "AI search optimization, brand visibility in AI platforms",
        "scenario": "AI search engine optimization",
    },
    "real-estate-buyer-seller": {
        "name_zh": "Real Estate Buyer/Seller Agent",
        "description": "Expert in real estate transactions, market analysis, and negotiation strategies.",
        "expertise": "Real estate transactions, market analysis, negotiation",
        "scenario": "Property transactions",
    },
    "retail-customer-returns": {
        "name_zh": "Retail Customer Returns",
        "description": "Specialist in returns processing, refund handling, and customer communication for retail.",
        "expertise": "Returns processing, refunds, customer communication",
        "scenario": "Retail after-sales service",
    },
    "specialized-chief-of-staff": {
        "name_zh": "Chief of Staff",
        "description": "Expert in strategic coordination, priority management, and cross-functional communication for executive teams.",
        "expertise": "Strategic coordination, priority management, cross-functional communication",
        "scenario": "Executive support, strategy execution",
    },
}


def strip_emoji(text):
    """Remove emoji characters from text."""
    result = []
    for ch in text:
        cp = ord(ch)
        if (cp < 0x7F or
                0x2000 <= cp <= 0x206F or
                0x2E80 <= cp <= 0x9FFF or
                0xF900 <= cp <= 0xFAFF or
                0xFE30 <= cp <= 0xFE4F or
                0xFF00 <= cp <= 0xFFEF):
            result.append(ch)
    return ''.join(result).strip()


def find_openclaw_json():
    """Locate openclaw.json."""
    env_path = os.environ.get("OPENCLAW_CONFIG")
    if env_path and os.path.isfile(env_path):
        return env_path
    default = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.isfile(default):
        return default
    print("ERROR: Cannot find openclaw.json.", file=sys.stderr)
    sys.exit(1)


def find_agents_repo(explicit_path=None):
    """Find or clone the agency-agents-zh repository."""
    if explicit_path and os.path.isdir(explicit_path):
        return explicit_path
    for p in DEFAULT_REPO_PATHS:
        if os.path.isdir(p):
            return p
    return None


def clone_agents_repo(target=None):
    """Clone agency-agents-zh to /tmp."""
    target = target or "/tmp/agency-agents-zh"
    if os.path.isdir(target):
        print(f"  Repo already exists at {target}, pulling ...")
        subprocess.run(["git", "-C", target, "pull", "--depth", "1"],
                       capture_output=True)
    else:
        print(f"  Cloning {REPO_URL} ...")
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, target],
                       capture_output=True, check=True)
    return target


def parse_md_frontmatter(filepath):
    """Extract YAML frontmatter fields from a markdown file.
    Returns dict with keys: name, description (or None if no frontmatter).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return {}

    # Must start with ---
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    end = content.find("---", 3)
    if end == -1:
        return {}

    frontmatter = content[3:end].strip()
    result = {}
    for line in frontmatter.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value

    return result


def load_agent_descriptions(repo_path, agent_ids):
    """Scan repo for .md files matching agent_ids, extract frontmatter descriptions.
    Returns dict: agent_id -> description string.
    """
    descriptions = {}
    if not repo_path or not os.path.isdir(repo_path):
        return descriptions

    # Walk all subdirectories for .md files
    for root, dirs, files in os.walk(repo_path):
        # Skip .git and other hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            agent_id = os.path.splitext(fname)[0]
            if agent_id in agent_ids:
                fm = parse_md_frontmatter(os.path.join(root, fname))
                desc = fm.get("description", "")
                if desc:
                    descriptions[agent_id] = desc

    return descriptions


def fetch_readme():
    """Download the latest README from GitHub."""
    print(f"Fetching {README_URL} ...")
    req = urllib.request.Request(README_URL)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
    with open(README_CACHE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Cached to {README_CACHE} ({len(content)} bytes)")
    return content


def load_readme(fetch=False):
    """Load README from cache, or fetch if requested."""
    if fetch or not os.path.exists(README_CACHE):
        return fetch_readme()
    with open(README_CACHE, "r", encoding="utf-8") as f:
        return f.read()


def parse_readme_tables(readme):
    """Parse agent tables from the README. Returns dict: agent_id -> {...}."""
    start = readme.find("## 智能体阵容")
    if start == -1:
        print("ERROR: Section '智能体阵容' not found in README", file=sys.stderr)
        sys.exit(1)

    content = readme[start:]
    lines = content.split("\n")
    agents = {}
    current_section = ""

    for line in lines:
        if line.startswith("### "):
            current_section = strip_emoji(line.strip("# ").strip())
        elif line.startswith("| ") and "[" in line and "](" in line:
            if line.startswith("| 智能体"):
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 4:
                link_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", cells[1])
                if link_match:
                    name_zh = link_match.group(1).strip()
                    path = link_match.group(2).strip()
                    expertise = cells[2].strip()
                    scenario = cells[3].strip()
                    agent_id = os.path.splitext(os.path.basename(path))[0]
                    agents[agent_id] = {
                        "name_zh": name_zh,
                        "expertise": expertise,
                        "scenario": scenario,
                        "section": current_section,
                        "source": "agency-agents-zh",
                    }
    return agents


def load_openclaw_agents(config_path):
    """Extract agent IDs from openclaw.json (excluding 'main')."""
    with open(config_path) as f:
        data = json.load(f)
    return {a["id"] for a in data.get("agents", {}).get("list", []) if a["id"] != "main"}


def build_index(openclaw_path, fetch_readme_flag=False, repo_path=None, clone=False):
    """Main entry point."""
    # 1. Resolve repo
    if clone:
        repo_path = clone_agents_repo()
    elif not repo_path:
        repo_path = find_agents_repo()

    readme = load_readme(fetch=fetch_readme_flag)

    # 2. Parse README
    print("Parsing README tables ...")
    readme_agents = parse_readme_tables(readme)
    print(f"  Found {len(readme_agents)} agents in README")

    # 3. Load openclaw.json
    oc_ids = load_openclaw_agents(openclaw_path)
    print(f"  Found {len(oc_ids)} agents in openclaw.json")

    # 4. Enrich with frontmatter descriptions
    matched = {aid: info for aid, info in readme_agents.items() if aid in oc_ids}
    print(f"  Matched {len(matched)} agents")

    if repo_path:
        print(f"Loading agent descriptions from {repo_path} ...")
        descriptions = load_agent_descriptions(repo_path, set(matched.keys()))
        print(f"  Found descriptions for {len(descriptions)} agents")
        for aid, desc in descriptions.items():
            if aid in matched:
                matched[aid]["description"] = desc
    else:
        print("  No repo found, skipping description extraction.")
        print("  Use --repo <path> or --clone to extract descriptions from .md files.")

    # Count how many have descriptions
    with_desc = sum(1 for info in matched.values() if info.get("description"))
    print(f"  Agents with descriptions: {with_desc}/{len(matched)}")

    # 5. Build by-category index
    by_category = {}
    for agent_id, info in matched.items():
        section = info["section"]
        entry = {
            "agentId": agent_id,
            "name_zh": info["name_zh"],
            "description": info.get("description", ""),
            "expertise": info["expertise"],
            "scenario": info["scenario"],
            "section": section,
            "source": info["source"],
        }
        by_category.setdefault(section, []).append(entry)

    # 6. Add upstream fallback
    upstream_section = "Upstream (agency-agents by msitarzewski)"
    by_category[upstream_section] = []
    missing = oc_ids - set(matched.keys())
    for agent_id in sorted(missing):
        fallback = UPSTREAM_FALLBACK.get(agent_id)
        if fallback:
            entry = {
                "agentId": agent_id,
                "name_zh": fallback["name_zh"],
                "description": fallback["description"],
                "expertise": fallback["expertise"],
                "scenario": fallback["scenario"],
                "section": upstream_section,
                "source": "agency-agents (upstream)",
            }
        else:
            entry = {
                "agentId": agent_id,
                "name_zh": agent_id,
                "description": "",
                "expertise": "(unknown)",
                "scenario": "(unknown)",
                "section": upstream_section,
                "source": "unknown",
            }
        by_category[upstream_section].append(entry)

    total_readme = len(matched)
    total_upstream = len(by_category[upstream_section])

    output = {
        "total": total_readme + total_upstream,
        "source": (
            f"agency-agents-zh ({total_readme})"
            f" + agency-agents upstream ({total_upstream})"
        ),
        "categories": by_category,
    }

    with open(AGENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nGenerated: {AGENTS_JSON}")
    print(f"Total: {output['total']} agents")
    print(f"  From README: {total_readme}")
    print(f"  From upstream fallback: {total_upstream}")
    for sec in sorted(by_category.keys()):
        print(f"  [{len(by_category[sec])}] {sec}")

    # Warn about unaccounted
    unaccounted = oc_ids - set(matched.keys()) - set(UPSTREAM_FALLBACK.keys())
    if unaccounted:
        print(f"\nWARNING: {len(unaccounted)} agents have no description at all:")
        for aid in sorted(unaccounted):
            print(f"  {aid}")


def main():
    fetch = "--fetch" in sys.argv
    clone = "--clone" in sys.argv
    repo_path = None

    for i, arg in enumerate(sys.argv):
        if arg == "--repo" and i + 1 < len(sys.argv):
            repo_path = sys.argv[i + 1]
            break

    config_path = find_openclaw_json()
    build_index(config_path, fetch_readme_flag=fetch, repo_path=repo_path, clone=clone)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
draft_cover_letter.py — Generates a tailored cover letter prompt for OpenClaw's built-in AI.

This script does NOT call any external AI API (no Anthropic, no OpenAI, etc.).
It reads the resume JSON and job details, then prints a structured prompt to stdout.
OpenClaw's own LLM reads this prompt and generates the cover letter directly.

Usage:
    python3 draft_cover_letter.py \\
        --resume path/to/resume.json \\
        --job_title "Software Engineer" \\
        --company "Acme Corp" \\
        --job_description "We are looking for..." \\
        [--output "cover_letter.txt"]

Output:
    Prints the cover letter generation prompt to stdout.
    The OpenClaw agent uses its built-in LLM to complete the generation.
    If --output is provided, the agent should save the result to that path.

No API keys required beyond RESUMEX_API_KEY (already set for resume fetch).
"""

import os
import sys
import json
import argparse


def load_resume(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Resume file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in resume file: {e}", file=sys.stderr)
        sys.exit(1)


def extract_resume_fields(resume: dict) -> dict:
    """
    Extract key fields from the resume JSON.
    Supports both the ResumeX API format (profile.fullName) and legacy formats.
    """
    # Support both profile.fullName (ResumeX format) and basics.name (legacy)
    profile = resume.get("profile", resume.get("basics", {}))
    skills_data = resume.get("skills", [])
    experience = resume.get("experience", [])
    education = resume.get("education", [])
    projects = resume.get("projects", [])
    achievements = resume.get("achievements", [])

    name = profile.get("fullName", profile.get("name", "the candidate"))
    location = profile.get("location", "")
    summary = profile.get("summary", "")

    # Flatten skills (handles both [{category, skills:[...]}, ...] and flat list)
    flat_skills = []
    if isinstance(skills_data, list):
        for item in skills_data:
            if isinstance(item, dict) and "skills" in item:
                flat_skills.extend(item["skills"])
            elif isinstance(item, str):
                flat_skills.append(item)

    # Format experience entries
    exp_lines = []
    for e in experience[:4]:
        role = e.get("role", e.get("title", "?"))
        company = e.get("company", "?")
        start = e.get("startDate", "?")
        end = e.get("endDate", "present")
        desc = e.get("description", "")[:200]
        exp_lines.append(f"  - {role} at {company} ({start} – {end}): {desc}")

    # Format education entries
    edu_lines = []
    for e in education[:2]:
        degree = e.get("degree", "?")
        inst = e.get("institution", "?")
        end = e.get("endDate", e.get("year", "?"))
        score = e.get("score", "")
        line = f"  - {degree} from {inst} ({end})"
        if score:
            line += f", Score: {score}"
        edu_lines.append(line)

    # Format projects
    proj_lines = []
    for p in projects[:3]:
        name_p = p.get("name", "?")
        desc = p.get("description", "")[:150]
        tags = ", ".join(p.get("tags", [])[:5])
        proj_lines.append(f"  - {name_p}: {desc}" + (f" [{tags}]" if tags else ""))

    # Notable achievements
    ach_lines = []
    for a in achievements[:3]:
        title = a.get("title", "?")
        year = a.get("year", "")
        ach_lines.append(f"  - {title}" + (f" ({year})" if year else ""))

    return {
        "name": name,
        "location": location,
        "summary": summary,
        "skills": flat_skills[:12],
        "experience": exp_lines,
        "education": edu_lines,
        "projects": proj_lines,
        "achievements": ach_lines,
    }


def build_cover_letter_prompt(fields: dict, job_title: str, company: str, job_desc: str) -> str:
    """
    Build a structured prompt for OpenClaw's built-in LLM to generate a cover letter.
    No external API is called — the agent reads this prompt and runs it through its own AI.
    """
    skills_str = ", ".join(fields["skills"]) if fields["skills"] else "Not listed"
    exp_str = "\n".join(fields["experience"]) if fields["experience"] else "  (none listed)"
    edu_str = "\n".join(fields["education"]) if fields["education"] else "  (none listed)"
    proj_str = "\n".join(fields["projects"]) if fields["projects"] else "  (none listed)"
    ach_str = "\n".join(fields["achievements"]) if fields["achievements"] else "  (none)"

    prompt = f"""Generate a professional, tailored cover letter for the following candidate and job.

=== CANDIDATE RESUME ===
Name: {fields["name"]}
Location: {fields["location"]}
Summary: {fields["summary"]}

Top Skills: {skills_str}

Work Experience:
{exp_str}

Education:
{edu_str}

Key Projects:
{proj_str}

Achievements:
{ach_str}

=== TARGET JOB ===
Role: {job_title}
Company: {company}
Job Description:
{job_desc[:2000]}

=== COVER LETTER REQUIREMENTS ===
- Length: Under 200 words
- Tone: Professional but warm — human, not robotic
- Structure:
  1. Hook (1 sentence): Why this specific company/role excites the candidate
  2. Match (2-3 sentences): Specific skills/experiences that directly map to the job requirements
     Use concrete examples from their resume, not generic statements
  3. Value add (1-2 sentences): A concrete achievement or measurable result from their past work
  4. Close (1 sentence): Confident call to action
- Do NOT include: subject line, "Dear Hiring Manager", date, or any metadata
- Output ONLY the cover letter body text

Write the cover letter now:"""

    return prompt


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a tailored cover letter prompt for OpenClaw's built-in AI. "
            "No external API keys required — OpenClaw's own LLM handles generation."
        )
    )
    parser.add_argument("--resume", required=True, help="Path to resume JSON file")
    parser.add_argument("--job_title", required=True, help="Job title being applied for")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--job_description", required=True, help="Job description text")
    parser.add_argument(
        "--output",
        help="(Optional) Output file path for the cover letter. "
             "The agent will save the generated letter here after LLM generation.",
    )
    args = parser.parse_args()

    resume_data = load_resume(args.resume)
    fields = extract_resume_fields(resume_data)

    print(
        f"Building cover letter prompt for '{args.job_title}' at '{args.company}'...",
        file=sys.stderr,
    )

    prompt = build_cover_letter_prompt(
        fields=fields,
        job_title=args.job_title,
        company=args.company,
        job_desc=args.job_description,
    )

    # Print the prompt to stdout — OpenClaw's agent reads this and
    # runs it through its built-in LLM to produce the actual cover letter.
    print(prompt)

    if args.output:
        print(
            f"\n[AGENT INSTRUCTION] After generating the cover letter from the prompt above, "
            f"save the result to: {args.output}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

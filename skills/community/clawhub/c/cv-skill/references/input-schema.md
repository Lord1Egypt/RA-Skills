# Input Schema

Use a JSON file with this structure.

```json
{
  "candidate": {
    "name": "Alex Chen",
    "contact_line": "alex@example.com | +1 555-0100 | Singapore | CET-6",
    "base_summary": "Optional general summary used as source material.",
    "location": "Singapore",
    "email": "alex@example.com",
    "phone": "+1 555-0100",
    "links": ["linkedin.com/in/example", "portfolio.example.com"]
  },
  "target": {
    "role": "Operations Coordinator",
    "company": "Example Company",
    "industry": "Media / Technology",
    "job_description": "Optional pasted job description or role requirements.",
    "keywords": ["coordination", "stakeholder communication", "documentation"]
  },
  "style": {
    "latin_font": "Times New Roman",
    "cjk_font": "宋体",
    "page_size": "letter",
    "language": "en",
    "section_labels": {
      "summary": "Summary",
      "experience": "Professional Experience",
      "education": "Education",
      "campus": "Projects and Activities",
      "skills": "Skills and Certifications"
    }
  },
  "education": [
    {
      "left": "Example University | MBA",
      "right": "2022.09 - 2024.06",
      "bullets": [
        "Relevant coursework or achievements.",
        "Language or collaboration context."
      ]
    }
  ],
  "experience": [
    {
      "key": "media_assistant",
      "default_left": "Project Coordinator | Example Media Co.",
      "default_right": "2024.01 - Present",
      "default_bullets": [
        "Base bullets used when no track override exists."
      ]
    }
  ],
  "campus": [
    {
      "left": "Business Simulation Project",
      "right": "Graduate Program",
      "bullets": [
        "Optional campus or extracurricular item."
      ]
    }
  ],
  "tracks": {
    "operations": {
      "title": "Operations Coordinator / Platform Operations",
      "summary": "Role-targeted summary.",
      "experience_order": ["media_assistant"],
      "experience_overrides": {
        "media_assistant": {
          "left": "Operations Assistant | Example Media Co.",
          "right": "2024.01 - Present",
          "bullets": [
            "Track-specific rewrite."
          ]
        }
      },
      "campus_items": [
        {
          "left": "Business Simulation Project",
          "right": "Graduate Program",
          "bullets": [
            "Track-specific campus rewrite."
          ]
        }
      ],
      "skills_lines": [
        "Tools: Excel, PowerPoint, Photoshop.",
        "Keywords: coordination, documentation, scheduling."
      ],
      "cover_letter": {
        "recipient_name": "Hiring Manager",
        "recipient_title": "Recruiting Team",
        "company": "Example Company",
        "address_lines": ["123 Main Street", "Boston, MA 02116"],
        "opening_angle": "Why this role and employer fit the candidate.",
        "proof_points": [
          "Concrete example connected to the job description.",
          "Second example showing transferable scope or impact."
        ],
        "closing_angle": "Contribution, thanks, and interview availability."
      }
    }
  }
}
```

## Required fields

- `candidate.name`
- `candidate.contact_line`
- `education`
- `tracks`

## Track behavior

Each track creates a separate resume version.

- `experience_order` determines ordering
- `experience_overrides` lets you rewrite bullets per track
- if a role is not overridden, the generator falls back to `default_*`
- `cover_letter` is optional and used when the user asks for a matching letter

## Validation behavior

Before generation or delivery, check:

- `candidate.contact_line` includes at least an email and phone, or the separate `email` / `phone` fields are present
- track summaries and bullets do not invent metrics absent from source material
- dates are consistently formatted
- links are relevant and professional
- section order matches role relevance
- `style.page_size` is either `letter` or `a4`; Harvard-style examples normally use `letter`
- `style.language` controls default section headings; `style.section_labels` can override them

## Filename behavior

The script uses:

- candidate name
- track key

and sanitizes the result to a safe filename.

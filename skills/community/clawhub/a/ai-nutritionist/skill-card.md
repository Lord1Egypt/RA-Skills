## Description: <br>
AI营养师 is a Chinese-language nutrition assistant that creates personalized meal plans, nutrition analyses, food recommendations, and interactive HTML reports for diet goals, chronic-condition nutrition, constitution-based food therapy, sports nutrition, special populations, and nutrient lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to collect nutrition profile details and generate Chinese-language meal plans, food recommendations, shopping lists, nutrient explanations, and optional HTML reports for educational nutrition planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores health-related nutrition profile details locally. <br>
Mitigation: Use it on a trusted device, review or delete user_data/profile.json when no longer needed, and prefer deployments with explicit save consent and a delete or reset flow. <br>
Risk: The skill requests broad agent tools for reading, writing, shell execution, and web access. <br>
Mitigation: Run it in a controlled agent environment, review file and shell actions before relying on them, and narrow tool permissions where the host supports it. <br>
Risk: Nutrition outputs may be mistaken for medical advice, especially for chronic conditions or special populations. <br>
Mitigation: Treat outputs as educational guidance, verify important recommendations with a clinician or registered dietitian, and follow clinical treatment plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/ai-nutritionist) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown responses with optional shell commands, JSON profile data, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user_data/profile.json and ai-nutritionist-report.html when profile storage or report generation is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

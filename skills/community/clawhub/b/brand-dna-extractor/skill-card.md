## Description: <br>
Extracts brand identity from a website URL by analyzing colors, typography, visual style, imagery, CSS, and images into a structured brand profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content teams use this skill to extract a reusable visual brand profile from public or authorized websites before generating on-brand content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches target websites and should not be used on sites the user is not authorized to analyze. <br>
Mitigation: Use it only on public or authorized sites and respect access restrictions. <br>
Risk: Visual analysis may send selected images or derived visual data to Gemini or OpenAI providers. <br>
Mitigation: Avoid sensitive or private sites and review provider data-handling requirements before use. <br>
Risk: Optional Supabase caching can store extracted profiles and requires careful handling of Supabase credentials. <br>
Mitigation: Disable storage for sensitive work, keep the Supabase key server-side and scoped where possible, and keep secrets out of logs and shared environments. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/brand-dna-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and structured BrandDNA fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe website fetching, VLM analysis, API-key configuration, and optional Supabase caching.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

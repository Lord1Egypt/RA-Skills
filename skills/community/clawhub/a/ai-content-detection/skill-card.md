## Description: <br>
Provides structured guidance for assessing whether text, images, video, audio, documents, or links may be AI-generated or manipulated, including evidence checks, confidence scoring, and report templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chat2dev](https://clawhub.ai/user/chat2dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, reviewers, and analysts use this skill to inspect suspected AI-generated or manipulated content and produce a structured confidence-based assessment. It is best suited for advisory triage and documentation rather than definitive attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private documents, media, URLs, or analytics data could be exposed if a user submits them to third-party AI-detection or forensic services. <br>
Mitigation: Review data sensitivity first, prefer local or approved tools for confidential material, and redact unnecessary personal or proprietary information. <br>
Risk: AI-detection results can be uncertain and may create false positives or false negatives. <br>
Mitigation: Treat findings as advisory signals, combine multiple evidence types, and avoid using a detector score alone as definitive proof. <br>


## Reference(s): <br>
- [Ahrefs: What Percentage of New Content Is AI-Generated?](https://ahrefs.com/blog/what-percentage-of-new-content-is-ai-generated/) <br>
- [Pangram: Why Perplexity and Burstiness Fail to Detect AI](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai) <br>
- [PMC: Deepfake Media Forensics Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11943306/) <br>
- [ICCV 2025: Pixel-wise Temporal Frequency-based Deepfake Video Detection](https://openaccess.thecvf.com/content/ICCV2025/papers/Kim_Beyond_Spatial_Frequency_Pixel-wise_Temporal_Frequency-based_Deepfake_Video_Detection_ICCV_2025_paper.pdf) <br>
- [CVPR 2025: UNITE Universal Synthetic Video Detector](https://arxiv.org/html/2412.12278) <br>
- [PMC: Audio Deepfake Detection Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11991371/) <br>
- [ACM Computing Surveys: AI-Generated Content Forensics Survey](https://dl.acm.org/doi/full/10.1145/3760526) <br>
- [Imperva 2025 Bad Bot Report](https://www.imperva.com/resources/resource-library/reports/2025-bad-bot-report/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, analysis] <br>
**Output Format:** [Markdown checklist, confidence assessment, and report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference third-party detectors or forensic tools, but produces advisory guidance rather than executing code.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

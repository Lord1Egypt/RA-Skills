## Description:

Provides guidance for assessing whether text, images, audio, video, documents, or links may be AI-generated, including evidence indicators, confidence scoring, and report templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chat2dev](https://clawhub.ai/user/chat2dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as an investigative reference for evaluating suspected AI-generated or manipulated content across text, media, documents, and links. It helps produce structured detection reports with confidence scores while treating results as guidance rather than proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-content detection guidance can be mistaken for proof of authorship, fraud, or wrongdoing.

Mitigation: Treat findings as investigative guidance and require human review plus corroborating evidence before making consequential decisions.

Risk: Heuristic detection can produce false positives or miss manipulated content, especially for non-native writing, adversarial edits, or compressed media.

Mitigation: Use multiple evidence types, prefer original files, and include limitations in any generated report.

Risk: Detection methods and third-party tool performance can become outdated as generation models evolve.

Mitigation: Verify current detector claims and refresh references before high-stakes or public use.

## Reference(s):

- [Ahrefs: AI-Generated Content Study](https://ahrefs.com/blog/what-percentage-of-new-content-is-ai-generated/)
- [Futurism: AI-Generated Internet Content](https://futurism.com/artificial-intelligence/over-50-percent-internet-ai-slop)
- [Pangram Labs: Perplexity and Burstiness Limitations](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)
- [PMC: Deepfake Media Forensics Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC11943306/)
- [ICCV 2025: Pixel-Wise Temporal Frequency Deepfake Video Detection](https://openaccess.thecvf.com/content/ICCV2025/papers/Kim_Beyond_Spatial_Frequency_Pixel-wise_Temporal_Frequency-based_Deepfake_Video_Detection_ICCV_2025_paper.pdf)
- [CVPR 2025: UNITE Universal Synthetic Video Detector](https://arxiv.org/html/2412.12278)
- [Scientific Reports 2025: Deepfake Video Visual Attention Detection](https://www.nature.com/articles/s41598-025-23920-0)
- [PMC: Audio Deepfake Detection Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11991371/)
- [ACM Computing Surveys: Forensic Systems for AI-Generated Content](https://dl.acm.org/doi/full/10.1145/3760526)
- [UCLA: Imperfection of AI Detection Tools](https://humtech.ucla.edu/technology/the-imperfection-of-ai-detection-tools/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance and structured detection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scoring and evidence tables; no code execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

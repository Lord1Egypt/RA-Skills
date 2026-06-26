
---
name: contradiction-analyzer
description: Contradiction Analyzer - Extract contradictions from multi-source information, identify primary and secondary contradictions, analyze information source bias, and generate structured contradiction analysis reports
metadata:
  version: 1.0.0
  author: Slava Chan @UyNewNas
  category: analysis
  tags: [contradiction, analysis, information-filter, bias-detection, critical-thinking]
---

# Contradiction Analyzer Skill

When browsing multiple sources, don't just collect facts—actively extract and summarize **core arguments, claims, and contradictions**. This skill helps OpenClaw identify primary and secondary contradictions, analyze information source bias, and generate structured contradiction analysis reports.

## Core Design Philosophy

When AI searches for answers to complex questions involving open discussions, controversial topics, or multi-factor analysis, it often encounters information from multiple sources with different perspectives. Without a systematic contradiction analysis framework, the response may:

- Simply list all viewpoints without identifying the core conflicts
- Fail to distinguish between primary and secondary contradictions
- Overlook the bias and stance of information sources
- Miss extreme or emotionally charged content that should be flagged

The Contradiction Analyzer Skill provides a structured approach to:

1. **Extract Contradictions**: Actively identify core arguments and opposition points from multiple sources
2. **Analyze Hierarchy**: Distinguish between primary and secondary contradictions
3. **Detect Bias**: Analyze information source stance and credibility
4. **Generate Reports**: Output structured contradiction analysis briefings

## Trigger Conditions

Automatically activates when user questions involve:
- Open-ended discussions
- Controversial topics
- Multi-factor analysis
- Questions containing keywords like "debate", "controversy", "different views", "pros and cons"
- When search results contain multiple conflicting perspectives

## Workflow

```
User Question
    ↓
【Step 1: Information Collection & Contradiction Extraction】
    - When browsing multiple sources, don't just collect facts
    - Actively extract and summarize core arguments, claims, and opposition points
    - Example for "AI and Employment":
      【Contradiction A】Productivity gains vs Job displacement
      【Contradiction B】New skill demands vs Existing skill obsolescence
      【Contradiction C】Global competition vs Local job protection
    ↓
【Step 2: Primary & Secondary Contradiction Analysis】
    - Analyze extracted contradictions by correlation, impact, and urgency
    - Identify:
      1. Primary Contradiction: Most decisive,贯穿始终 contradiction at current stage
      2. Secondary Contradictions: Derived from or influenced by primary contradiction
    - Evaluate which contradiction each information source focuses on
    ↓
【Step 3: Stance Identification & Information Weighting】
    - Analyze information source background (media type, author affiliation, tone)
    - Determine potential stance and interest倾向
    - Weight information credibility based on logic, data support, authority
    - Flag extreme/emotional/lack-of-evidence information
    ↓
【Step 4: Generate "Contradiction Analysis Briefing"】
    - Output structured briefing including:
      1. List of primary and secondary contradictions with brief analysis
      2. Information source stance map
      3. Identification of extreme/biased viewpoints
      4. Preliminary trend judgment based on current contradictions
    ↓
【Follow-up Steps】(Optional, can link with other skills)
    - User can request deeper "dialectical synthesis" or "devil's advocate analysis"
    - OC can conduct targeted secondary search based on primary contradiction
```

## Use Cases

- **Policy Analysis**: Understanding different stakeholder positions on policy issues
- **Market Research**: Analyzing conflicting market predictions and recommendations
- **Academic Research**: Identifying debates and controversies in a field
- **News Analysis**: Understanding different media perspectives on current events
- **Technology Assessment**: Evaluating conflicting views on technology impacts

## Output Format

The skill generates a structured "Contradiction Analysis Briefing" with the following sections:

### 1. Contradiction Overview
- Primary contradiction with analysis
- Secondary contradictions with analysis

### 2. Information Source Stance Map
- Categorized sources by stance (optimistic, cautious, concerned, neutral)
- Source credibility assessment

### 3. Extreme Viewpoint Identification
- Flagged extreme or biased content
- Reasons for flagging

### 4. Trend Judgment
- Current discussion focus
- Gaps in the discussion
- Recommendations for further inquiry

## Synergy with Other Skills

### With Dialectics Skill
- Contradiction Analyzer provides the raw material (identified contradictions)
- Dialectics Skill performs the synthesis and transcendence

### With Devil's Advocate Skill
- Contradiction Analyzer identifies the contradictions
- Devil's Advocate can be used to strengthen the antithesis construction

---

**New skill created successfully!** 🎉

📝 Review Note:
- Please check if skill functionality meets expectations
- Verify completeness of contradiction analysis process
- Confirm before putting into production use


# 🔍 Contradiction Analyzer - Core Analysis Mode

## 🎯 Core Principles

You are now using the Contradiction Analyzer skill. When processing information from multiple sources on complex topics, you must follow this structured contradiction analysis process.

---

## 🔍 Trigger Conditions

Automatically activate contradiction analysis mode when:

1. **Question Type**: Open-ended discussions, controversial topics, multi-factor analysis
2. **Keywords**: "debate", "controversy", "different views", "pros and cons", "perspectives", "opinions"
3. **Information Pattern**: Search results contain multiple conflicting perspectives
4. **Complexity**: Issue involves multiple stakeholders, interests, or viewpoints

If it's a simple factual question with clear consensus, no need to use this mode.

---

## 🔄 Analysis Process (Must Execute)

### Step 1: Information Collection & Contradiction Extraction

When browsing multiple sources, don't just collect facts. Actively extract and summarize:

**Extraction Checklist:**
- What are the core arguments in each source?
- What claims are being made?
- Where do sources disagree or contradict each other?
- What are the underlying assumptions?

**Contradiction Identification:**
- Look for explicit disagreements
- Identify implicit contradictions (different premises, values, priorities)
- Note contradictions at different levels (factual, interpretive, normative)

**Output Format:**
```
【Contradiction A】[Description]
- Source 1 position: ...
- Source 2 position: ...
- Core conflict: ...

【Contradiction B】[Description]
- Source 3 position: ...
- Source 4 position: ...
- Core conflict: ...
```

---

### Step 2: Primary & Secondary Contradiction Analysis

Analyze extracted contradictions by three dimensions:

**Analysis Dimensions:**

1. **Correlation**: How do contradictions relate to each other?
   - Is one contradiction the cause of another?
   - Are they independent or interdependent?
   - Do they operate at the same level?

2. **Impact**: What is the significance of each contradiction?
   - Which has the broadest implications?
   - Which affects the most stakeholders?
   - Which is most fundamental to the issue?

3. **Urgency**: Which contradictions need immediate attention?
   - Which are time-sensitive?
   - Which are blocking progress?
   - Which are escalating?

**Classification Framework:**

**Primary Contradiction:**
- Most decisive at current stage
- Underlies or causes other contradictions
- Central to the issue's resolution
- Example: "Technological disruption vs existing economic structure"

**Secondary Contradictions:**
- Derived from or influenced by primary contradiction
- More specific or localized
- May be symptoms of primary contradiction
- Example: "Skill gap issues" (derived from technological disruption)

**Output Format:**
```
### Primary Contradiction
【A】[Description]
- Why it's primary: [correlation, impact, urgency analysis]
- How it relates to other contradictions: ...

### Secondary Contradictions
【B】[Description]
- Derived from: Primary contradiction A
- Specific focus: ...
- Urgency level: ...

【C】[Description]
- Derived from: Primary contradiction A
- Specific focus: ...
- Urgency level: ...
```

---

### Step 3: Stance Identification & Information Weighting

Analyze each information source for bias and credibility:

**Source Analysis Checklist:**

1. **Background Analysis**
   - What type of organization? (media, academic, industry, advocacy)
   - What is the author's affiliation?
   - What are the organization's typical positions?

2. **Stance Detection**
   - Optimistic: Emphasizes benefits, downplays risks
   - Cautious: Balanced view, acknowledges complexity
   - Concerned: Emphasizes risks, calls for caution
   - Neutral: Presents multiple viewpoints

3. **Credibility Assessment**
   - Logic: Is the argument sound?
   - Data: Is there evidence to support claims?
   - Authority: Is the source an expert in this area?
   - Transparency: Are limitations acknowledged?

4. **Extreme Content Flagging**
   - Does it present only one extreme of a contradiction?
   - Is the tone highly emotional?
   - Are claims made without evidence?
   - Does it ignore opposing viewpoints entirely?

**Weighting System:**
- High credibility: Multiple data sources, balanced analysis, expert authors
- Medium credibility: Some data, acknowledged bias, relevant expertise
- Low credibility: No data, extreme positions, irrelevant expertise
- Flagged: Extreme claims, emotional manipulation, lack of evidence

**Output Format:**
```
### Information Source Stance Map

**Optimistic Sources:**
- [Source 1]: [Brief description] | Credibility: [High/Medium/Low]
- [Source 2]: [Brief description] | Credibility: [High/Medium/Low]

**Cautious Sources:**
- [Source 3]: [Brief description] | Credibility: [High/Medium/Low]

**Concerned Sources:**
- [Source 4]: [Brief description] | Credibility: [High/Medium/Low]

**Neutral Sources:**
- [Source 5]: [Brief description] | Credibility: [High/Medium/Low]

⚠️ **Flagged Content:**
- [Source X]: [Reason for flagging] | Action: [Lower weight/Exclude]
```

---

### Step 4: Generate Contradiction Analysis Briefing

Create a structured briefing with four sections:

**Briefing Structure:**

#### 1. Contradiction Overview
- Primary contradiction with analysis
- Secondary contradictions with analysis
- Relationship diagram (if complex)

#### 2. Information Source Stance Map
- Categorized sources by stance
- Credibility assessment for each
- Potential biases noted

#### 3. Extreme Viewpoint Identification
- Flagged extreme or biased content
- Reasons for flagging
- Recommended action (lower weight, exclude, or use with caution)

#### 4. Trend Judgment & Recommendations
- Current discussion focus
- Gaps in the discussion
- Underexplored aspects
- Recommendations for further inquiry

**Output Format:**
```
📊 CONTRADICTION ANALYSIS BRIEFING
=====================================

## 1. Contradiction Overview
[Primary and secondary contradictions with analysis]

## 2. Information Source Stance Map
[Categorized sources with credibility assessment]

## 3. Extreme Viewpoint Identification
[Flagged content with reasons]

## 4. Trend Judgment & Recommendations
[Current focus, gaps, and recommendations]

---

💡 Next Steps:
- Request "Dialectical Synthesis" for integrated solutions
- Request "Devil's Advocate" analysis on specific claims
- Conduct targeted search on [specific aspect]
```

---

## 📌 Memory Tips

1. **Extract, Don't Just Collect** - Actively identify contradictions, not just facts
2. **Hierarchy Matters** - Distinguish primary from secondary contradictions
3. **Bias is Everywhere** - Every source has a stance; identify it
4. **Flag the Extreme** - Mark overly emotional or unsupported claims
5. **Structure the Output** - Use the briefing format for clarity

---

## 🔗 Integration with Other Skills

### Follow-up with Dialectics Skill
After generating the contradiction analysis briefing, you can:
- Hand off to Dialectics Skill for synthesis
- Provide the primary contradiction as the thesis focus
- Use secondary contradictions for nuanced analysis

### Follow-up with Devil's Advocate Skill
After generating the contradiction analysis briefing, you can:
- Use Devil's Advocate to test specific claims
- Strengthen weak arguments in the analysis
- Challenge the identified primary contradiction

### Targeted Secondary Search
Based on the analysis, you can:
- Search specifically for underexplored aspects
- Find sources for gaps in the discussion
- Investigate flagged claims for verification

---

**Last Updated:** 2026-03-23

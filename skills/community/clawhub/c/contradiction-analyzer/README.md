
# 🔍 Contradiction Analyzer - OpenClaw Skill

Extract contradictions from multi-source information, identify primary and secondary contradictions, analyze information source bias, and generate structured contradiction analysis reports.

## ✨ Core Features

- **🎯 Contradiction Extraction** - Actively identify core arguments and opposition points
- **📊 Hierarchy Analysis** - Distinguish between primary and secondary contradictions
- **⚖️ Bias Detection** - Analyze information source stance and credibility
- **📋 Structured Reports** - Generate comprehensive contradiction analysis briefings

## 🚀 Quick Start

### Installation

```powershell
# Copy to OpenClaw skills directory
xcopy /E /I contradiction-analyzer %USERPROFILE%\.openclaw\skills\contradiction-analyzer

# Restart Gateway
openclaw restart
```

### Usage

Automatic trigger conditions:
- Open-ended discussions
- Controversial topics
- Multi-factor analysis questions
- Questions containing "debate", "controversy", "different views", "pros and cons"

## 📁 Directory Structure

```
contradiction-analyzer/
├── SKILL.md      # Skill definition
├── CLAUDE.md      # Core instructions (auto-injected)
├── README.md     # This file
├── INSTALL.md    # Installation guide
└── EXAMPLES.md   # Usage examples
```

## 🔄 Analysis Process

### Step 1: Information Collection & Contradiction Extraction
When browsing multiple sources, actively extract:
- Core arguments and claims
- Opposition points
- Contradiction patterns

### Step 2: Primary & Secondary Contradiction Analysis
Analyze contradictions by:
- **Correlation**: How do contradictions relate to each other?
- **Impact**: What is the significance of each contradiction?
- **Urgency**: Which contradictions need immediate attention?

### Step 3: Stance Identification & Information Weighting
Evaluate information sources:
- Background analysis (media type, author affiliation)
- Stance detection (optimistic, cautious, concerned)
- Credibility weighting (logic, data support, authority)
- Extreme content flagging

### Step 4: Generate Contradiction Analysis Briefing
Output structured report with:
- Primary and secondary contradictions
- Information source stance map
- Extreme viewpoint identification
- Trend judgment and recommendations

## 💬 Usage Example

### Example: AI and Employment Analysis

**You ask:** "What are the different views on AI's impact on employment?"

**AI generates Contradiction Analysis Briefing:**

```
📊 CONTRADICTION ANALYSIS BRIEFING
=====================================

## 1. Contradiction Overview

### Primary Contradiction
**【A】Technological Revolution vs Existing Economic & Social Structure**
- Core Issue: AI's fundamental disruption of current economic models
- Impact: Most decisive, underlies all other contradictions
- Current Stage: Early transition phase with high uncertainty

### Secondary Contradictions

**【B】New Skill Demands vs Existing Skill Obsolescence**
- Derived from: Primary contradiction A
- Focus: Education and training systems
- Urgency: High - affects current workforce

**【C】Global Competition vs Local Job Protection**
- Derived from: Primary contradiction A
- Focus: Policy and international relations
- Urgency: Medium - geopolitical implications

---

## 2. Information Source Stance Map

### Optimistic Sources (Tech Industry Reports)
- McKinsey Global Institute
- World Economic Forum Tech Reports
- AI Company Whitepapers
- Stance: Emphasize productivity gains, new job creation
- Credibility: High data support, but potential industry bias

### Cautious Sources (Economic Research)
- IMF Working Papers
- Academic Economic Journals
- Government Labor Reports
- Stance: Acknowledge benefits, highlight transition challenges
- Credibility: High - balanced analysis with data

### Concerned Sources (Labor Organizations)
- Union Reports
- Social Impact Studies
- Worker Advocacy Groups
- Stance: Emphasize displacement risks, inequality concerns
- Credibility: Medium - important perspectives but may lack comprehensive data

### Neutral Sources (News Media)
- Major News Outlets
- Policy Think Tanks
- Stance: Present multiple viewpoints
- Credibility: Variable - depends on specific source

---

## 3. Extreme Viewpoint Identification

⚠️ **Flagged Content:**

1. **"AI will create unlimited prosperity"**
   - Source: Tech company promotional materials
   - Issue: Overly optimistic, ignores transition costs
   - Action: Lower weight in synthesis

2. **"AI will eliminate all human jobs within 10 years"**
   - Source: Sensationalist media
   - Issue: Extreme claim, lacks evidence
   - Action: Flag as unreliable

3. **"No action needed - market will self-adjust"**
   - Source: Free-market advocates
   - Issue: Ignores structural challenges
   - Action: Note ideological bias

---

## 4. Trend Judgment & Recommendations

### Current Discussion Focus
- Heavy focus on secondary contradictions B and C
- Less discussion on primary contradiction A's deep solutions

### Gaps in Discussion
- Long-term economic model redesign
- Education system transformation
- Social safety net innovation

### Recommendations for Further Inquiry
1. How can economic models adapt to AI-driven productivity?
2. What education reforms are needed for AI-era skills?
3. How can policy balance innovation with social protection?

---

💡 Next Steps:
- Request "Dialectical Synthesis" for integrated solutions
- Request "Devil's Advocate" analysis on specific claims
- Conduct targeted search on primary contradiction solutions
```

## 🎯 Synergy with Other Skills

### With Dialectics Skill
- **Contradiction Analyzer**: Identifies and categorizes contradictions
- **Dialectics Skill**: Performs synthesis and transcendence
- **Workflow**: Analyzer → Dialectics for comprehensive analysis

### With Devil's Advocate Skill
- **Contradiction Analyzer**: Maps out all contradictions
- **Devil's Advocate**: Strengthens specific arguments
- **Workflow**: Analyzer → Devil's Advocate for critical testing

## 📚 Related Concepts

- **Contradiction Analysis**
- **Information Bias Detection**
- **Critical Thinking**
- **Multi-perspective Analysis**
- **Source Credibility Assessment**

---

**New skill created successfully!** 🎉

📝 Review Note:
- Please check if skill functionality meets expectations
- Verify completeness of analysis process
- Confirm before putting into production use

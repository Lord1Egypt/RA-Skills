# Patent Analysis Patterns

## Overview

This reference document provides patterns and templates for analyzing patents using LLM capabilities.

## Analysis Framework

### Four Dimensions of Analysis

For each patent, analyze across these dimensions:

1. **Competitive Threat** - How dangerous is this patent to the client?
2. **Technology Alignment** - Which of the client's business areas does this affect?
3. **Strategic Action** - What should the client do about this patent?
4. **Business Impact** - Why does this specifically matter to the client's business?

---

## 1. Competitive Threat Assessment

### Threat Levels

**None (0-10 points)**
- Unrelated to client's business
- Completely different industry
- Technology has no overlap

**Example:**
```
Patent: "Agricultural Harvesting System" by Deere & Company
Client: DMG Mori (CNC machine tools)

Analysis: This patent is about agricultural machinery, completely unrelated 
to DMG Mori's business in CNC machine tools and metal manufacturing. 
No competitive threat.

THREAT LEVEL: None (0 points)
```

**Low (11-20 points)**
- Adjacent technology
- Minor overlap
- Could become relevant in future

**Example:**
```
Patent: "3D Printing Software Interface" by Stratasys
Client: DMG Mori

Analysis: While 3D printing is relevant to DMG's additive manufacturing 
business, this patent covers software interfaces, not core manufacturing 
technology. Low threat.

THREAT LEVEL: Low (15 points)
```

**Medium (21-40 points)**
- Overlapping technology
- Potential market encroachment
- Direct competitor activity

**Example:**
```
Patent: "CNC Machine Tool Spindle Assembly" by Haas Automation
Client: DMG Mori

Analysis: Haas is a direct competitor in the CNC machine tool market. 
This patent covers spindle technology which is critical for DMG's 
machining centers. Indicates Haas is investing in core technology 
that competes with DMG's offerings.

THREAT LEVEL: Medium (30 points)
```

**High (41-60 points)**
- Core technology area
- Direct competitive threat
- Significant market impact potential

**Example:**
```
Patent: "Five-Axis CNC Machining Center with Integrated Automation" 
by Yamazaki Mazak
Client: DMG Mori

Analysis: Mazak is DMG's primary competitor. This patent combines 
CNC machining (DMG's core business) with automation (DMG's key 
differentiator). Direct threat to DMG's competitive positioning 
in the high-end machining center market.

THREAT LEVEL: High (50 points)
```

**Critical (61-100 points)**
- Fundamental technology shift
- Could disrupt client's market position
- Immediate competitive threat

**Example:**
```
Patent: "AI-Powered Predictive Maintenance System for Machine Tools" 
by Siemens
Client: DMG Mori

Analysis: Siemens is entering the machine tool intelligence space with 
predictive maintenance powered by AI. This combines Industry 4.0 
(digital manufacturing) with AI - areas where DMG is investing 
heavily. Could establish Siemens as the technology leader and 
relegate DMG to follower position. Critical threat to DMG's 
future competitiveness.

THREAT LEVEL: Critical (75 points)
```

### Threat Scoring Rubric

| Factor | Points | Description |
|--------|--------|-------------|
| Direct competitor | +20 | From client's top 4 competitors |
| Secondary competitor | +10 | From known industry players |
| Core technology | +20 | In client's primary business area |
| Adjacent technology | +10 | In client's secondary business |
| Emerging technology | +15 | In growth/future area |
| High patent quality | +10 | Broad claims, strong technical depth |
| Strategic timing | +15 | Filed recently (last 6 months) |
| Multiple patents | +10 | Competitor filed multiple in same area |

---

## 2. Technology Alignment

### Technology Categories

**CNC_Machining**
- Turning centers
- Milling machines
- Machining centers
- Multi-axis machines
- Spindle technology
- Tool changers
- Coolant systems
- Chip management

**Additive_Manufacturing**
- 3D printing
- Laser metal deposition
- Powder bed fusion
- Hybrid manufacturing (CNC + additive)
- Build chamber technology
- Metal powder handling

**Automation**
- Robotic loading/unloading
- Pallet pool systems
- Workpiece handling
- Automated tool presetting
- Unmanned production
- Lights-out manufacturing

**Digital_Manufacturing**
- Industry 4.0 integration
- IoT sensors and connectivity
- Digital twins
- Predictive maintenance
- AI/ML for optimization
- Cloud-based monitoring
- Real-time process control

**Laser_Technology**
- Laser cutting
- Laser welding
- Laser additive manufacturing
- Laser engraving/marking
- Ultrasonic technology

**Tooling_Systems**
- Tool holders
- Cutting tools
- Tool magazines
- Tool management systems
- Presetting technology

### Alignment Scoring

**Primary Alignment (+20 points)**
Patent directly covers client's core business

**Secondary Alignment (+10 points)**
Patent in adjacent or growth area

**Tertiary Alignment (+5 points)**
Patent tangentially related

**No Alignment (0 points)**
Patent unrelated to client's business

---

## 3. Strategic Action Recommendations

### Action Types

**Immediate_review (Critical patents)**
When to recommend:
- Threat score ≥ 60
- Core technology area
- Direct competitor
- High business impact

Action items:
- Schedule emergency R&D meeting within 24 hours
- Assign senior engineer to analyze patent claims
- Evaluate defensive patenting options
- Assess licensing vs. litigation options
- Brief executive team on strategic implications

**Weekly_review (High priority patents)**
When to recommend:
- Threat score 40-59
- Significant technology overlap
- Medium-high business impact

Action items:
- Include in weekly technology meeting
- Assign technical review to relevant team
- Evaluate competitive positioning impact
- Consider patent landscape monitoring
- Update competitive intelligence dashboard

**Monthly_review (Medium priority patents)**
When to recommend:
- Threat score 20-39
- Some technology relevance
- Low-medium business impact

Action items:
- Standard monitoring in monthly review
- Track competitor activity in this area
- Assess market trends quarterly
- Include in quarterly strategy review

**Monitor (Low priority patents)**
When to recommend:
- Threat score < 20
- Minimal current relevance
- Track for future shifts

Action items:
- Add to monitoring list
- No immediate action required
- Reassess if market conditions change
- Annual review for portfolio completeness

---

## 4. Business Impact Analysis

### Impact Statement Template

Structure the business impact in this format:

```
⚠️ COMPETITIVE THREAT: [Competitor] is [action] in [technology area], 
which [impact on client's business]. This suggests [competitor strategy] 
and could [potential consequence for client].

📊 TECHNOLOGY ALIGNMENT: This patent falls in [category], which is 
[relevance to client's business]. The technology covers [specific 
aspects] that are [importance to client's operations].

⚡ ACTION: [Recommended action] because [rationale]. [Client] should 
[specific steps] to [desired outcome].

🎯 IMPACT: [Summary of impact level and reasoning]
```

### Example Impact Statement

```
⚠️ COMPETITIVE THREAT: Siemens is patenting AI-powered predictive 
maintenance systems for machine tools, which directly threatens 
DMG Mori's digital manufacturing strategy. This suggests Siemens 
is positioning itself as the technology leader in Industry 4.0 
for machine tools, and could relegate DMG Mori to a follower position 
in the rapidly growing smart manufacturing market.

📊 TECHNOLOGY ALIGNMENT: This patent falls in Digital_Manufacturing 
(AI + Predictive Maintenance), which is a strategic growth area 
for DMG Mori. The technology covers machine learning algorithms 
for predicting tool wear and maintenance needs, which are critical 
for DMG's competitive positioning in Industry 4.0.

⚡ ACTION: Immediate R&D review recommended because this patent 
represents a fundamental technology shift that could establish 
Siemens as the market leader. DMG Mori should accelerate its own 
AI predictive maintenance development, consider licensing options, 
and evaluate partnership opportunities to avoid being left behind.

🎯 IMPACT: CRITICAL - This represents a strategic threat to DMG 
Mori's future competitiveness in digital manufacturing. If Siemens 
establishes leadership in AI-powered predictive maintenance, DMG 
may lose market share in the high-end machine tool segment where 
smart capabilities are increasingly a competitive requirement.
```

---

## Analysis Checklist

Before finalizing analysis, verify:

✅ Read patent title and abstract completely
✅ Identify the patent assignee (company)
✅ Check if assignee is a known competitor
✅ Determine which technology category applies
✅ Assess competitive threat level with specific reasoning
✅ Explain why this matters to the client's specific business
✅ Recommend clear, actionable next steps
✅ Justify the priority level with business impact reasoning

---

## Common Analysis Mistakes to Avoid

❌ **Generic analysis** - "This is interesting" without specific business relevance
❌ **No competitive context** - Missing why this competitor matters to the client
❌ **Vague technology** - Not identifying specific category
❌ **Missing rationale** - Stating threat level without explaining why
❌ **No actionable recommendations** - Analysis without next steps
❌ **Overstating impact** - Marking everything as "critical"
❌ **Understating impact** - Missing genuine competitive threats

✅ **Good analysis** - Specific, contextualized, actionable, and justified

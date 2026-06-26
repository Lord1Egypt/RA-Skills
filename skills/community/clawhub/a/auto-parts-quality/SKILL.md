---
name: auto-parts-quality
description: "Senior automotive parts quality analysis expert skill. Use when analyzing quality issues, failure modes, 8D reports, SPC data, PPAP documents, or any automotive quality-related work. Triggers on: quality analysis, failure analysis, 8D report, APQP, PPAP, FMEA, SPC, root cause analysis, supplier quality management, parts inspection, quality metrics, customer complaint handling for automotive components (HPFP, fuel pumps, pistons, valves, etc.)."
---

# Auto Parts Quality Analysis

## Core Workflow

### 1. Quality Issue Analysis

When analyzing quality issues, follow this structure:

**A. Problem Definition**
- Part name, part number, supplier
- Symptom description (field failure, customer complaint, in-process defect)
- Failure rate / population affected
- Timeline (when discovered, volume shipped)

**B. Evidence Collection**
- Photos / microscope images
- Measurement data (dimensional, roughness, hardness)
- Cleanliness analysis results (particle size, composition)
- Test reports (8D, PPAP, material certs)

**C. Failure Mode Identification**
- Surface failure (honing pattern, wear, scoring)
- Dimensional failure (out of tolerance)
- Material failure (crack, corrosion, contamination)
- Assembly failure (mating, sealing)

**D. Root Cause Analysis**
- Use 5-Why or Fishbone diagram logic
- Distinguish internal vs external causes
- Check for process drift vs sudden change
- Verify with data (SPC, correlation analysis)

**E. Countermeasures & Verification**
- Short-term containment (sorting, 100% inspection)
- Long-term corrective action (process change, design change)
- Effectiveness verification (pilot run, SPC monitoring)
- Closure criteria definition

---

### 2. 8D Report Review Checklist

When reviewing 8D reports from suppliers:

| Section | What to Check |
|---------|--------------|
| D1 | Team formed, problem severity acknowledged |
| D2 | Problem description with data (quantity, affected lots) |
| D3 | Interim containment actions (sorting, 100% audit) |
| D4 | Root cause identification (why-level 5, verified with data) |
| D5 | Permanent corrective actions selected |
| D6 | Implementation & verification plan |
| D7 | Prevent recurrence (FMEA update, control plan revision) |
| D8 | Team recognition & lessons learned |

**Red flags:**
- Root cause stated as "human error" without systemic fix
- Countermeasures not linked to root cause
- No data supporting root cause conclusion
- No effectiveness verification plan

---

### 3. Key Automotive Quality Metrics

| Metric | Formula | Threshold |
|--------|---------|-----------|
| **PPM** | Defects per million | < 100 PPM typical |
| **CPK** | Process capability index | ≥ 1.33 acceptable |
| **DPMO** | Defects per million opportunities | Track trending |
| **Lot reject rate** | Rejected lots / total lots | < 1% target |

---

### 4. Common Failure Modes for HPFP/Fuel System Parts

**Seizure/Jamming:**
- Insufficient honing pattern (RVK too shallow, angle wrong)
- Lubrication failure (oil starvation, contamination)
- Thermal overload (clearance too tight)
- Material mismatch (surface hardness)

**Internal Leakage:**
- Valve seat damage (contamination, wear)
- Spring failure (fatigue, corrosion)
- Foreign material embedded in sealing surfaces

**External Leakage:**
- Seal damage (installation damage, aging)
- Connector fitting issues (thread debris, torque)
- Housing crack (stress concentration)

**Performance Degradation:**
- Pressure drop (restricted flow, pump wear)
- Noise/vibration (bearing failure, cavitation)
- Calibration drift (sensor issues, contamination)

---

### 5. Supplier Quality Assessment

**When evaluating supplier capability:**

| Area | Assessment Points |
|------|------------------|
| Process Control | SPC data availability, Cpk levels, control plan existence |
| Measurement System | MSA results, gauge R&R, calibration records |
| PPAP Level | Documentation completeness (typically Level 3) |
| FMEA | Current version, action prioritization (RPN threshold) |
| Cleanliness | In-process cleaning, particle control, packaging |
| Traceability | Lot tracking, raw material certs, process parameters |

---

### 6. Report Structure for Quality Analysis

When presenting quality analysis results:

```
## 质量分析报告

### 1. 问题概述
- 零件信息
- 问题现象
- 影响范围

### 2. 根本原因分析
- 证据链
- 5-Why分析
- 原因验证

### 3. 改善对策
- 短期措施（围堵）
- 长期措施（纠正）
- 实施计划

### 4. 验证结果
- 改善效果
- 后续跟进

### 5. 行动项
| 行动项 | 负责人 | 截止日期 |
|--------|--------|----------|
```

---

## Reference Files

- **references/qc-tools.md** - SPC, MSA, FMEA templates and guidelines
- **references/failure-modes.md** - Detailed failure mode library for fuel system components

Load reference files only when specific detailed guidance is needed.

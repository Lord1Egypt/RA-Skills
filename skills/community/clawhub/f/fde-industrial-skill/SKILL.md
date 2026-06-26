---
name: fde-industrial-skill
description: "FDE skill for industrial AI deployment: scenario diagnosis, data governance, solution design, POC-to-scale methodology, ROI quantification. Covers predictive maintenance, visual inspection, process optimization, energy efficiency, supply chain. Triggers: FDE, industrial AI, smart manufacturing, factory AI, AI deployment."
version: 2.0.1
author: jaccen
tags: [FDE, industrial-ai, smart-manufacturing, predictive-maintenance, visual-inspection]
trigger: FDE, forward deployed engineer, industrial AI, smart manufacturing, AI deployment, production line AI, factory AI, predictive maintenance, visual inspection, industrial big data, AI+manufacturing
---

# FDE Industrial AI Deployment Skill

> Open Source: https://github.com/jaccen/FDE-Industrial-Skill

## Overview

Full-spectrum support for FDEs deploying AI & big data on industrial production lines — from scenario diagnosis to scaled deployment.

## Core Workflow

```
Scenario Diagnosis -> Data Governance -> Solution Design -> POC -> Scale-up -> Feedback Loop
```

### Step 1: Scenario Diagnosis

1. Read [references/fde-role-model.md](references/fde-role-model.md) for FDE capability framework.
2. Apply "Pain-Data-Impact" triage: Pain (business pain), Data (sufficiency), Impact (quantifiable ROI).
3. Classify into 5 core categories — [references/industrial-ai-scenarios.md](references/industrial-ai-scenarios.md).

### Step 2: Data Governance & Integration

1. Map data sources: OT (SCADA/PLC/sensors), IT (MES/ERP/PLM), ET (engineering docs).
2. Palantir-style Ontology: Objects, Links, Actions.
3. Data quality gaps: missing values, timestamp misalignment, label scarcity.
4. Pipeline: edge collection -> ETL -> feature store.

**Key**: Start from business decisions, not data tables.

### Step 3: Solution Design

- **Visual inspection**: CNN/ViT + edge GPU boxes
- **Predictive maintenance**: LSTM/Transformer + physics-informed features; 7-14 day window
- **Process optimization**: RL/Bayesian + digital twin; single process first
- **Energy efficiency**: regression + control optimization; baseline first
- **Supply chain**: graph model + demand forecast + ERP integration

### Step 4: POC Deployment (Zero Week)

Day 1-3: data audit + interviews; Day 4-7: baseline model + quick wins; Week 2-4: training + integration; Week 4-6: A/B test + operator training.

**Critical**: Deliver measurable quick win within 2 weeks.

### Step 5: Scale-up & Feedback

Measure ROI, generalize single -> multi -> factory-wide, FDE+FDR feedback loop.

## ROI Framework

| Metric | Typical Range |
|--------|--------------|
| Defect detection improvement | 80-95% reduction |
| Unplanned downtime reduction | 30-60% reduction |
| Yield improvement | 2-8% increase |
| Energy savings | 5-15% reduction |
| ROI payback period | 6-18 months |

## Reference Guide

| Need | Reference |
|------|-----------|
| FDE role & skills | [fde-role-model.md](references/fde-role-model.md) |
| Scenario & algorithm | [industrial-ai-scenarios.md](references/industrial-ai-scenarios.md) |
| Deployment methodology | [landing-methodology.md](references/landing-methodology.md) |
| Case studies | [case-studies.md](references/case-studies.md) |

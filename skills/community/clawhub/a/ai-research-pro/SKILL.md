---
name: research-assistant
description: Research assistant using ReAct + Plan-and-Solve for web research, information synthesis, and report generation with citations.
---

# Research Assistant

AI-powered research assistant that combines tool use (ReAct) with structured planning (Plan-and-Solve) to conduct thorough research and generate comprehensive reports.

---

## Features

### 🔍 Web Research

- **Search Queries**: Intelligent search strategy
- **Source Evaluation**: Credibility assessment
- **Information Extraction**: Key facts and data

### 📊 Analysis & Synthesis

- **Multi-perspective**: Compare different sources
- **Fact-checking**: Verify claims across sources
- **Trend Analysis**: Identify patterns

### 📝 Report Generation

- **Structured Reports**: Clear organization
- **Citations**: Proper source attribution
- **Executive Summary**: Key findings upfront

---

## Usage

```javascript
const researcher = new ResearchAssistant();

const report = await researcher.research({
  topic: 'Impact of AI on Software Development Jobs',
  depth: 'comprehensive',  // quick, standard, comprehensive
  sources: 10,  // minimum sources
  includeStats: true
});

console.log(report.summary);
console.log(report.citations);
```

---

## Architecture

```
User Request
    ↓
Plan-and-Solve Agent
    ├─ Phase 1: Define research questions
    ├─ Phase 2: Search strategy
    ├─ Phase 3: Source collection
    ├─ Phase 4: Analysis
    └─ Phase 5: Report writing
    ↓
ReAct Agent (for each phase)
    ├─ Search web
    ├─ Fetch pages
    ├─ Extract info
    └─ Verify facts
    ↓
Final Report with Citations
```

---

## Installation

```bash
clawhub install research-assistant
```

---

## License

MIT

---

## Version

1.0.0

---

## Created

2026-04-02

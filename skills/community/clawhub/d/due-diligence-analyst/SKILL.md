---
name: due-diligence-analyst
description: AI-Powered Due Diligence Analysis - Automated comprehensive DD across financial, legal, business, and team dimensions for investment decisions
homepage: https://github.com/yourusername/openclaw-due-diligence-analyst
metadata: {"openclaw":{"version":"0.1.0","category":"business","tags":["due-diligence","investment","analysis","finance","legal","risk"]}}
---

# Due Diligence Analyst

AI-powered due diligence analysis tool that automates comprehensive DD across financial, legal, business, and team dimensions for investment decisions.

## Overview

Due Diligence Analyst is an intelligent OpenClaw skill designed for investors, M&A advisors, and corporate development teams. It automates the entire due diligence process, providing multi-dimensional analysis including financial health, legal compliance, business operations, team background, market position, and risk assessment.

**Generate professional DD reports in minutes instead of weeks.**

## Core Features

### 1. Company Profile Analysis
Analyze target companies and extract key information:
- Corporate information verification
- Shareholder structure mapping
- Related party identification
- Historical change tracking
- Initial risk assessment

**Usage**: "Analyze company: ByteDance" or "分析公司：字节跳动"

### 2. Quick Due Diligence Report
Generate rapid due diligence reports:
- Executive summary with rating
- Company overview
- Key findings (strengths, concerns, critical issues)
- Quick risk assessment
- Next steps recommendations

**Usage**: "Quick DD: Tencent" or "快速尽调：腾讯"

### 3. General Consultation
AI-powered consultation on due diligence topics:
- DD process and methodology
- Risk identification techniques
- Industry best practices
- Valuation approaches
- Investment decision support

**Usage**: "What is due diligence?" or "How to assess a company's financial health?"

## Planned Features (v0.2.0+)

- Financial Due Diligence (statements analysis, metrics calculation)
- Legal & Compliance Checks (litigation search, IP verification)
- Business Analysis (business model, competitive landscape)
- Team Background Checks (founder verification, work history)
- Market & Industry Analysis (trends, sizing, competitors)
- Risk Assessment Matrix (multi-dimensional risk scoring)
- Professional Report Export (PDF, Word, Excel, PowerPoint)

## Usage Examples

### Example 1: Company Analysis
**User**: "Analyze company: Xiaomi"

**System**: Generates comprehensive company profile including:
- Basic information (founding date, industry, status)
- Shareholder structure and ownership
- Related parties and affiliates
- Historical changes and funding rounds
- Key risk indicators

### Example 2: Quick Due Diligence
**User**: "Quick DD: Meituan"

**System**: Generates quick DD report with:
- Executive summary (rating: B+, recommendation: proceed with caution)
- Company overview
- Quick risk assessment (financial, legal, operational)
- Key findings and red flags
- Next steps for deeper investigation

### Example 3: Consultation
**User**: "What should I focus on in financial due diligence?"

**System**: Provides expert guidance on:
- Key financial metrics to review
- Common red flags to watch for
- Best practices for financial analysis
- Industry-specific considerations

## How It Works

1. **Intent Recognition**: Automatically identifies the type of analysis needed
2. **Multi-Agent Processing**: Routes to specialized agents (Company, Financial, Legal, etc.)
3. **AI Analysis**: Uses Claude to analyze information and generate insights
4. **Professional Output**: Returns structured, formatted reports

## Data Sources

**Current Version (MVP)**:
- AI reasoning and analysis using Claude
- Public knowledge base
- User-provided information

**Future Versions**:
- Enterprise database integration (Qichacha, Tianyancha APIs)
- Financial data services
- Legal information databases
- News and sentiment monitoring

## Important Notes

### Disclaimers
- This tool provides analysis based on AI reasoning and public information
- Results are for reference only and do not constitute professional investment advice
- Critical information should be verified through official channels
- Actual due diligence should include on-site visits and professional expertise

### Data Accuracy
- Current version does not have real-time enterprise database access
- Information may not be complete or up-to-date
- Users should verify key facts through:
  - Qichacha / Tianyancha (Enterprise info)
  - National Enterprise Credit Information System
  - Official company disclosures
  - Professional DD firms

### Best Use Cases
- ✅ Initial screening of investment targets
- ✅ Preliminary risk assessment
- ✅ Learning DD methodology
- ✅ Generating DD checklists
- ⚠️ Not a replacement for professional DD services
- ⚠️ Should be combined with manual verification

## Technical Details

- **Runtime**: Node.js >= 22
- **Language**: TypeScript 5.3+
- **Platform**: OpenClaw 2026+
- **AI**: Claude (via OpenClaw)
- **Architecture**: Multi-agent system with specialized analyzers

## Version

**Current**: 0.1.0 (MVP)
- ✅ Company profile analysis
- ✅ Quick DD report generation
- ✅ AI consultation support

**Coming Soon**:
- v0.2.0: Financial DD, Legal checks, PDF export
- v0.3.0: Business analysis, Team background, Market research
- v0.4.0: Real data source integration, Continuous monitoring
- v1.0.0: Complete 8-module system, Production-ready

## License

MIT License - Open source and free to use

## Support

- **Documentation**: README.md and docs/ folder
- **Issues**: Report bugs and request features on GitHub
- **Community**: OpenClaw Discord server

---

**Transform the way due diligence is done - AI-powered, efficient, professional.**

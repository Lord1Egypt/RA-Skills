# DoDAF Skill for Trae IDE

A professional DoDAF 2.0/2.1 architecture modeling skill that guides users step-by-step through defense system architecture design, from stakeholder analysis to consolidated report generation.

## Features

- **9-Phase Structured Workflow**: From stakeholder interview to consolidated PDF/Word report
- **23 DoDAF View Products**: Complete coverage of AV, OV, CV, SV, DIV, TV, PV viewpoints
- **draw.io Diagrams**: Auto-generated architecture diagrams in .drawio format
- **Completeness & Consistency Verification**: Automated checks across all views
- **Consolidated Report**: Single PDF/Word/HTML document with all views integrated
- **Cross-View Traceability**: Full traceability from capabilities to milestones
- **Bilingual Support**: Works with both English and Chinese defense standards

## Quick Start

1. Install this skill in Trae IDE
2. Invoke the skill: `/dodaf`
3. Answer the interview questions about your system
4. Get a complete DoDAF architecture description with diagrams and consolidated report

## Workflow Phases

| Phase | Viewpoint | Products | Output |
|-------|-----------|----------|--------|
| 1 | AV | Stakeholder & Context | AV-1 overview |
| 2 | OV | Operational Analysis | OV-1/2/3/5 |
| 3 | CV | Capability Definition | CV-1/2/3 |
| 4 | SV | System Design | SV-1/2/4/5 |
| 5 | DIV | Data Architecture | DIV-1/2/3 |
| 6 | TV | Technical Architecture | TV-1/2/3 |
| 7 | PV | Project Planning | PV-1/2/3 |
| 8 | AV | Integration & Verification | AV-1/2/3, verification report |
| 9 | - | **Consolidated Report** | PDF/Word/HTML |

## Output Structure

```
project-name/
├── docs/                    # Markdown documents (18 files)
│   ├── 01-stakeholder-context.md
│   ├── 02-operational-analysis.md
│   ├── ...
│   └── traceability-matrix.md
├── diagrams/                # draw.io diagrams (16 files)
│   ├── AV-1-overview.drawio
│   ├── OV-1-operational-concept.drawio
│   ├── ...
│   └── PV-3-project-resource-flow.drawio
└── report/                  # Consolidated report (Phase 9)
    ├── consolidated-report.md
    ├── project-dodaf-report.pdf     # if pandoc available
    └── project-dodaf-report.docx    # if pandoc available
```

## Tool Dependencies (Optional)

| Tool | Purpose | Install |
|------|---------|---------|
| Pandoc | Convert MD to PDF/DOCX | https://pandoc.org/installing.html |
| XeLaTeX | PDF engine for CJK | TeX Live / MiKTeX |
| draw.io Desktop | Export diagrams to PNG/SVG | https://github.com/jgraph/drawio-desktop |

> These tools are optional. The skill generates Markdown and .drawio files regardless.

## Example Use Cases

- Military vehicle engine R&D architecture modeling
- Defense information system architecture design
- Weapon system lifecycle architecture description
- C4ISR system operational architecture
- Logistics support system capability analysis

## Contributing

We welcome contributions! Areas of interest:

1. **More domain templates**: Add templates for Navy, Air Force, Space systems
2. **Additional view products**: Support OV-4, OV-6, SV-3, SV-7, etc.
3. **Report templates**: Custom Word/PDF templates with organization branding
4. **Verification rules**: Domain-specific consistency rules
5. **Internationalization**: Support for NATO, UK MODAF, Australian DAOF

### How to Contribute

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description

## Feedback

Please share your feedback:

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Share use cases and suggestions via GitHub Discussions
- **Email**: For sensitive defense-related feedback

## License

MIT License

## Changelog

### v2.0 (2026-05)
- Added Phase 9: Consolidated report generation (PDF/Word/HTML)
- Added output artifact tracking per phase
- Added drawio skill integration for diagram generation
- Added tool dependencies section (Pandoc, XeLaTeX, draw.io)
- Enhanced verification to cover all 23 view products
- Added Chinese defense standards (GJB) reference
- Improved workflow with per-phase verification

### v1.0 (Initial)
- 8-phase DoDAF workflow
- Basic view generation
- Completeness and consistency verification

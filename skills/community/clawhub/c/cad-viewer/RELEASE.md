# cad-viewer Release Checklist

## Version Information
- **Name**: cad-viewer
- **Version**: 1.0.0
- **Description**: Professional CAD DWG/DXF drawing analysis Skill with features including drawing info extraction, layer queries, entity analysis, text extraction, distance calculation, screenshot visualization, and compliance auditing

## File Manifest

```
cad-viewer/
├── SKILL.md              # Skill metadata and AI usage guide (required)
├── README.md             # Complete documentation
├── LICENSE               # MIT License
├── scripts/
│   ├── cad_tools.py      # Core CLI tool (13 subcommands)
│   └── setup.sh          # One-click environment setup script
├── references/
│   └── cad_knowledge.md  # CAD domain knowledge reference
└── assets/               # Auto-generated at runtime directory (empty)
```

## System Requirements
- **OS**: Linux x86_64 (Ubuntu/Debian/RHEL/CentOS)
- **Python**: 3.8+
- **Permissions**: root/sudo (required for installing system packages on first run)

## External Dependencies
This Skill depends on the following external tools (auto-installed by setup.sh):
1. **ODA File Converter** - Required for reading DWG files
   - Download: https://www.opendesign.com/guestfiles/oda_file_converter
   - License: Free, requires Open Design Alliance account registration

2. **QCAD dwg2bmp** - High-quality screenshots (optional)
   - Download: https://qcad.org/en/download
   - License: Professional Trial, free for non-commercial use

## Feature Highlights
- ✅ 13 CLI subcommands, all output structured JSON
- ✅ Automatic dependency installation (auto-configures on first run)
- ✅ Supports DWG and DXF formats
- ✅ Drawing info extraction, layer/entity queries
- ✅ Text extraction, distance calculation
- ✅ Screenshot generation (PNG/PDF/SVG)
- ✅ Drawing compliance audit

## Publishing to SkillHub/ClawHub

### 1. Packaging
```bash
cd ~/.openclaw/workspace
tar czf cad-viewer-v1.0.0.tar.gz cad-viewer-publish/
```

### 2. Publishing Methods

**Method A: via clawhub CLI**
```bash
# Install clawhub
npm install -g clawhub

# Login
clawhub login

# Publish
clawhub publish ./cad-viewer-publish
```

**Method B: Manual upload to GitHub**
1. Create a GitHub repository
2. Upload cad-viewer-publish directory contents
3. Tag release: v1.0.0
4. Create Release with attached tar.gz package

**Method C: via CodeBuddy Code Skill Store**
Follow CodeBuddy Code platform's Skill submission guidelines

## Test Records
- Test Date: 2026-03-12
- Test Environment: Ubuntu 22.04 LTS x86_64
- Test Files: AutoCAD 2004 (AC1018) DWG files
- Test Results: All 13 commands working correctly

### Tested Features
| Command | Status |
|---------|--------|
| check-env | ✅ |
| info | ✅ |
| layers | ✅ |
| entities | ✅ |
| blocks | ✅ |
| inserts | ✅ |
| texts | ✅ |
| layer-content | ✅ |
| spaces | ✅ |
| distance | ✅ |
| screenshot | ✅ |
| audit | ✅ |
| search | ✅ |
| export-pdf | ✅ |

## Known Limitations
1. Linux x86_64 only, macOS/Windows not supported
2. First run requires downloading ODA/QCAD, may take several minutes
3. Large drawing screenshots may take longer processing time

## License
- This tool code: MIT License
- ODA File Converter: Subject to Open Design Alliance EULA
- QCAD Trial: Subject to QCAD License Agreement

## Maintainer
- Author: [Your Name]
- Contact: [Your Email]
- Project Homepage: [GitHub URL]

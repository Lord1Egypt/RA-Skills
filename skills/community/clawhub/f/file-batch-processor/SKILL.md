---
name: file-batch-processor
description: "One-click batch processing for all files: rename, compress images, convert to PDF, auto organize. No software installation needed, runs locally, safe and ad-free. Essential tool for professionals/students/shop owners! Use cases: batch file rename, batch image compression, batch PDF conversion, auto categorize by type. Windows compatible, newbie-friendly, office efficiency booster."
---

# File Batch Processor Master

## 🎯 Core Features

1. **Batch File Rename** - Multiple naming modes (sequence, date, prefix/suffix, etc.)
2. **Batch Image Compression** - Smart JPEG/PNG compression with quality preservation
3. **Batch to PDF** - One-click conversion of images and text files to PDF
4. **Auto Categorization** - Automatically categorize files by type (documents, images, audio, video, archives)

## 🚀 Quick Start
### Basic Workflow
# 1. Select folder to process
# 2. Choose processing functions (can select multiple)
# 3. Configure parameters (rename rules, compression quality, etc.)
# 4. Execute processing
# 5. View results report
```

## 📁 Directory Structure

```
file-batch-processor/
├── SKILL.md (current file)
├── scripts/
│   ├── batch_rename.py
│   ├── image_compress.py  
│   ├── convert_to_pdf.py
│   └── auto_organize.py
└── references/
    ├── naming_patterns.md
    ├── compression_guide.md
    └── file_types.md
```

## 🔧 Feature Details

### 1. Batch File Rename
- **Supported Modes**:
  - Sequence mode: `file_001.jpg`, `file_002.jpg`
  - Date mode: `20240302_photo1.jpg`
  - Prefix/suffix add: `backup_file.docx`, `file_copy.pdf`
  - Batch replace: `old_name` → `new_name`

### 2. Batch Image Compression
- **Supported Formats**: JPEG, PNG
- **Compression Options**:
  - Quality levels: High (90%), Medium (70%), Low (50%)
  - Size adjustment: Original size, 50%, 30%
  - Batch processing: Supports 1000+ files

### 3. Batch to PDF
- **Supported Source Files**:
  - Image files (JPG, PNG, BMP, etc.)
  - Text files (TXT, MD)
  - Office documents (requires additional tools)

- **Categorization Rules**:
  - 📄 Documents: .doc, .docx, .pdf, .txt, .md
  - 🖼️ Images: .jpg, .jpeg, .png, .bmp, .gif
  - 🎵 Audio: .mp3, .wav, .aac
  - 🎥 Video: .mp4, .avi, .mkv
  - 📦 Archives: .zip, .rar, .7z
  - 📁 Others: Remaining files

## 🎨 Skill Icon
- Recommended icons: Folder/Tool type icons
- Color scheme: Blue tones (professional & reliable) + Green (efficiency boost)

- ?? Organize large amounts of photos downloaded from phone
- 📊 Process batches of work documents
- 🛒 Shop owners organizing product images
- 🎓 Students organizing study materials
- 💼 Professionals improving office efficiency

## ⚙️ Technical Implementation
- **Platform**: Windows (most compatible)
- **Dependencies**: Python 3.8+, Pillow, PyPDF2, pdfkit (optional)
- **Security**: Runs locally, no network requests, no data uploads

## 📝 Precautions
- Backup important files before processing
- Large batch processing may take time
- Test with small samples when compressing images

## 📚 References
- [naming_patterns.md] - Detailed naming patterns guide
- [compression_guide.md] - Image compression technical guide
- [file_types.md] - File type identification rules

> 💡 Tip: This skill is designed to be "out-of-the-box" ready, easy for beginners to use, and an essential efficiency tool for professionals, students, and shop owners!
## 📦 Version Information
- **Current Version**: 1.0.0
- **Release Date**: 2026-03-03
- **Release Platform**: [ClawHub](https://clawhub.com/skills/file-batch-processor)
- **Author**: lx19840614

## 📝 Changelog
### v1.0.0 (2026-03-03) - Initial Version
- ✅ Batch file rename (5 modes)
- ✅ Batch image compression (quality/size adjustable)
- ✅ Batch convert to PDF (images/text)
- ✅ Auto file organization (6 categories)
- ✅ Preview mode (--dry-run)
- ✅ Windows optimized
- ✅ Complete documentation (README + video script + promotion plan)
### 📋 Planned Updates
- [ ] Chinese font PDF support
- [ ] Batch backup function
- [ ] Progress bar display
- [ ] GUI graphical interface
- [ ] macOS/Linux support
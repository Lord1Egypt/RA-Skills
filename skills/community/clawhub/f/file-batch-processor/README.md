# 📁 File Batch Processor Master

> **Process all files in bulk: rename, compress images, convert to PDF, auto categorize**  
> No software installation required, runs locally, safe without ads, essential tool for professionals/students/store owners!

---

## 🎯 Core Features

| Feature | Description | Use Cases |
|------|------|----------|
| 📝 **Batch Rename** | Supports 5 modes: sequence, date, prefix, suffix, replacement | Photo organization, document archiving |
| 🖼️ **Image Compression** | Smart JPEG/PNG compression, adjustable quality/size | Product images, social media |
| 📄 **Batch to PDF** | Convert images and text files to PDF with one click | Report generation, data organization |
| 🗂️ **Auto Categorization** | Automatically categorize by file type to folders | Download folder organization |

---

## 🚀 Quick Start

### Prerequisites

- ✅ Windows system
- ✅ Python 3.8+
- ✅ Required libraries: `Pillow`, `PyPDF2`, `fpdf`

### Install Dependencies

```bash
pip install Pillow PyPDF2 fpdf
```

### Basic Workflow

```bash
# 1. Enter skill directory
cd skills/file-batch-processor

# 2. Select folder to process
# 3. Choose processing function
# 4. Configure parameters
# 5. Execute processing
# 6. View results
```

---

## 📖 Detailed User Guide

### 1️⃣ Batch File Renaming

**Supported Modes**:

| Mode | Command Example | Result |
|------|----------|------|
| Sequence Mode | `--mode sequence --prefix "photo_"` | photo_001.jpg, photo_002.jpg |
| Date Mode | `--mode date --prefix "20260303_"` | 20260303_document.docx |
| Prefix Mode | `--mode prefix --prefix "backup_"` | backup_original_name.pdf |
| Suffix Mode | `--mode suffix --suffix "_copy"` | original_name_copy.txt |
| Batch Replace | `--mode replace --replace-old "old" --replace-new "new"` | new_name.jpg |

**Complete Commands**:

```bash
# Sequential renaming (starting from 001)
python scripts\batch_rename.py folder_path --mode sequence --prefix "photo_" --start 1

# Date-based renaming
python scripts\batch_rename.py folder_path --mode date --prefix "20260303_"

# Preview mode (execute without actual changes)
python scripts\batch_rename.py folder_path --mode sequence --prefix "test_" --dry-run
```

---

### 2️⃣ Batch Image Compression

**Supported Formats**: JPEG, PNG, BMP, GIF

**Parameter Description**:

| Parameter | Range | Default | Description |
|------|------|--------|------|
| `--quality` | 1-100 | 70 | Compression quality (higher number = better quality) |
| `--resize` | 0.1-1.0 | 1.0 | Size scaling ratio (0.5=50% size) |

**Command Examples**:

```bash
# Medium compression (70% quality, original size)
python scripts\image_compress.py folder_path --quality 70

# High compression (50% quality, 50% size)
python scripts\image_compress.py folder_path --quality 50 --resize 0.5

# High quality preservation (90% quality, original size)
python scripts\image_compress.py folder_path --quality 90
```

**Compression Effect Reference**:

| Original Size | Compression Parameters | After Compression | Compression Rate |
|----------|----------|--------|--------|
| 8.0KB | 70% quality +50% size | 1.2KB | 84.9% ⬇️ |
| 3.9KB | 70% quality +50% size | 1.1KB | 71.7% ⬇️ |
| 2MB | 70% quality +100% size | 600KB | 70% ⬇️ |

---

### 3️⃣ Batch Convert to PDF

**Supported Source Files**:

- 🖼️ Images: JPG, JPEG, PNG, BMP, GIF
- 📝 Text: TXT, MD (English works best, Chinese requires UTF-8 encoding)

**Command Examples**:

```bash
# Convert current folder
python scripts\convert_to_pdf.py folder_path

# Specify output folder
python scripts\convert_to_pdf.py folder_path --output output_folder

# Preview mode
python scripts\convert_to_pdf.py folder_path --dry-run
```

**Output Effects**:
- Images automatically adapt to A4 page, centered display
- Text files converted line by line, preserving original format

---

### 4️⃣ Automatic File Categorization

**Categorization Rules**:

| Category | Extensions |
|------|--------|
| 📄 Documents | .doc, .docx, .pdf, .txt, .md, .rtf |
| 🖼️ Images | .jpg, .jpeg, .png, .bmp, .gif, .tiff |
| 🎵 Audio | .mp3, .wav, .aac, .ogg, .m4a |
| 🎥 Video | .mp4, .avi, .mkv, .mov, .wmv |
| 📦 Archives | .zip, .rar, .7z, .tar, .gz |
| 📁 Others | Remaining files |

**Command Examples**:

```bash
# Automatic categorization and organization
python scripts\auto_organize.py folder_path

# Preview mode (see how files would be categorized)
python scripts\auto_organize.py folder_path --dry-run
```

**Before and After Organization**:

```
Before:                    After:
📁 Downloads/             📁 Downloads/
├── report.docx           ├── 📄 Documents/
├── photo1.jpg            │   ├── report.docx
├── music.mp3             │   └── notes.txt
├── video.mp4             ├── 🖼️ Images/
├── notes.txt             │   ├── photo1.jpg
└── archive.zip           │   └── screenshot.png
                          ├── 🎵 Audio/
                          │   └── music.mp3
                          ├── 🎥 Video/
                          │   └── video.mp4
                          └── 📦 Archives/
                              └── archive.zip
```

---

## 💡 Usage Scenarios

### 📱 Scenario 1: Organize Mobile Photos

```bash
# 1. Export photos to folder
# 2. Rename by date
python scripts\batch_rename.py photos_folder --mode date --prefix "20260303_"

# 3. Compress to save space
python scripts\image_compress.py photos_folder --quality 70 --resize 0.5
```

---

### 🛒 Scenario 2: Store Owner Organizing Product Images

```bash
# 1. Batch compress (suitable for online store upload)
python scripts\image_compress.py product_images_folder --quality 70 --resize 0.5

# 2. Uniform naming
python scripts\batch_rename.py product_images_folder --mode sequence --prefix "product_"

# 3. Convert to PDF for product catalog
python scripts\convert_to_pdf.py product_images_folder
```

---

### 🎓 Scenario 3: Student Organizing Study Materials

```bash
# Automatic categorization of downloaded study materials
python scripts\auto_organize.py downloads_folder

# Convert important documents to PDF backup
python scripts\convert_to_pdf.py documents_folder
```

---

### 💼 Scenario 4: Workplace Efficiency for Professionals

```bash
# Batch process work documents
python scripts\batch_rename.py work_folder --mode date --prefix "20260303_work_"

# Convert image reports to PDF
python scripts\convert_to_pdf.py report_images_folder --output PDF_reports
```

---

## ⚠️ Important Notes

1. **Backup important files** - Compression and renaming modify original files, backup first
2. **Preview mode** - First-time use recommended with `--dry-run` to preview effects
3. **Chinese encoding** - For text to PDF conversion, Chinese files require UTF-8 encoding
4. **Large batch processing** - Processing 1000+ files may take several minutes, please be patient
5. **Image formats** - Compression supports common image formats, not professional formats like RAW

---

## 🆚 Version History

### v1.0.0 (2026-03-03) - Initial Release

- ✅ Batch file renaming (5 modes)
- ✅ Batch image compression (adjustable quality/size)
- ✅ Batch convert to PDF (images/text)
- ✅ Automatic file categorization (6 categories)
- ✅ Preview mode (--dry-run)
- ✅ Windows optimization

### 📋 Planned Updates

- [ ] Chinese font PDF support
- [ ] Batch backup functionality
- [ ] Progress bar display
- [ ] GUI graphical interface
- [ ] macOS/Linux support

---

## 📞 Technical Support

- 📧 Issue feedback: Please leave message on ClawHub skill page
- 📚 Documentation updates: Follow version update logs
- 💬 Discussion group: Get group invitation after purchase

---

## ⭐ User Reviews

> "Amazing! Organized thousands of photos, saved many hours!" - User A  
> "Essential for store owners, very convenient for batch product image processing" - User B  
> "Student lifesaver, makes document organization super easy" - User C

---

## 📜 License Agreement

- This skill is for personal and commercial legal use only
- Resale, code flipping prohibited
- Runs locally, no network requests, data secure

---

## 🎁 Early Bird Benefits

**First 100 users during launch period**:

- 🎉 50% discount price
- 🎁 Free v1.x version updates
- 💬 Priority technical support
- 📝 Invitation to discussion group

**How to get benefits**:
1. After purchase, leave message "Early Bird" on ClawHub page
2. Or DM seller for discount code

---

<div align="center">

**👉 Get started now, make file organization incredibly easy!**

Made with ❤️ by OpenClaw Skills

</div>

# File Renaming Patterns Guide

## 1. Sequence Mode
- **Format**: `prefix_001.extension`, `file_001.jpg`
- **Use Cases**: Batch processing photos, screenshots, etc. needing sequential numbering
- **Parameters**: 
  - Starting number: 1, 100, 1000, etc.
  - Digits: 3 digits (001), 4 digits (0001), etc.

## 2. Date Mode
- **Format**: `20240302_photo.jpg`, `2024-03-02_document.pdf`
- **Date Format Codes**:
  - `%Y`: Year (2024)
  - `%m`: Month (03)
  - `%d`: Day (02)
  - `%H`: Hour (14)
  - `%M`: Minute (30)
  - `%S`: Second (45)

## 3. Prefix/Suffix Mode
- **Prefix Addition**: `backup_file.docx`, `important_contract.pdf`
- **Suffix Addition**: `file_copy.jpg`, `final_version_report.docx`
- **Combined Use**: `2024_project_001_final.pdf`

## 4. Batch Replace Mode
- **Examples**: 
  - `old_name` → `new_name`
  - `IMG_` → `photo_`
  - `scanned_` → `official_`

## 5. Advanced Modes
- **Random String**: Generate random alphanumeric combinations
- **File Size**: Include file size information in filename
- **Creation Time**: Use file creation timestamp

## 6. Recommended Practices
- **Backup First**: Backup original files before processing
- **Test First**: Test renaming effect with small number of files first
- **Avoid Duplicates**: Ensure new filenames don't conflict with existing files
- **Keep Concise**: Filenames should not be too long, easy to manage and search
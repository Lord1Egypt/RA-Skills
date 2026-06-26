# File Type Identification Rules

## 1. Document Types (.doc, .docx, .pdf, .txt, .md, .rtf)
- **Characteristics**: Mainly text content, for reading and editing
- **Processing Suggestions**: 
  - Keep original extension when renaming
  - Maintain format integrity when converting to PDF
  - Categorize to "Documents" folder

## 2. Image Types (.jpg, .jpeg, .png, .bmp, .gif, .tiff)
- **Characteristics**: Visual content, pixel data
- **Processing Suggestions**:
  - Prioritize compression processing
  - Maintain clarity when converting to PDF
  - Categorize to "Images" folder
  - Pay attention to copyright and privacy issues

## 3. Audio Types (.mp3, .wav, .aac, .ogg, .m4a)
- **Characteristics**: Sound data, time series
- **Processing Suggestions**:
  - Can add time information when renaming
  - Not recommended for PDF conversion (unless special need)
  - Categorize to "Audio" folder
  - Pay attention to file size and bitrate

## 4. Video Types (.mp4, .avi, .mkv, .mov, .wmv)
- **Characteristics**: Dynamic visuals + audio, large files
- **Processing Suggestions**:
  - Add duration or resolution info when renaming
  - Not recommended for PDF conversion (can extract cover image for PDF)
  - Categorize to "Video" folder
  - Confirm storage space before processing

## 5. Archive Types (.zip, .rar, .7z, .tar, .gz)
- **Characteristics**: Multiple files packaged, needs extraction
- **Processing Suggestions**:
  - Keep original extension when renaming
  - Not recommended for direct PDF conversion
  - Categorize to "Archives" folder
  - Confirm if extraction is needed before processing

## 6. Other Types
- **Program Files**: .exe, .bat, .sh - Keep as is, handle with caution
- **Database Files**: .db, .sqlite - Keep as is
- **Configuration Files**: .json, .xml, .yaml - Keep as is
- **Unknown Types**: Uniformly categorize to "Others"

## 7. Extension Identification Rules
- Prioritize full extension matching
- Case insensitive (.JPG = .jpg)
- Support multi-level extensions (.tar.gz → categorized as archive)
- Unknown extensions default to "Others"

## 8. Security Precautions
- Do not process system critical files (e.g., files in Windows directory)
- Do not process hidden files (files starting with .)
- Ask user confirmation for important file operations
- Provide undo functionality (backup mechanism)
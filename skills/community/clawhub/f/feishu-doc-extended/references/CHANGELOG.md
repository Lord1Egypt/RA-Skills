# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-12

### Added
- `get_image` action for feishu_doc tool
- Ability to download images from Feishu documents
- Support for OCR integration with tesseract

### Modified
- `doc-schema.ts`: Added get_image schema definition
- `docx.ts`: Added getImage() function implementation

### Known Issues
- get_image returns temporary URL with limited validity
- OCR accuracy depends on image quality

## [0.0.1] - 2026-03-12

### Initial release
- Concept version

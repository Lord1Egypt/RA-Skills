# PDF Accessibility Testing Guide

## PDF Accessibility Standards

### PDF/UA (ISO 14289)
- PDF/UA-1: International standard for accessible PDF
- PDF/UA-2: Extended requirements for PDF 2.0
- WCAG 2.0/2.1: Web content accessibility guidelines for PDFs
- Section 508: US federal accessibility requirements

## Testing with AccessMind

### Basic PDF Audit
```python
from accessmind import PDFAuditor

# Initialize auditor
auditor = PDFAuditor(file="document.pdf")

# Run full audit
results = auditor.audit()

# Get summary
print(f"Score: {results.score}")
print(f"Violations: {len(results.violations)}")
print(f"Warnings: {len(results.warnings)}")
```

### Specific Checks
```python
# Check for tagged PDF
if not auditor.is_tagged():
    print("❌ PDF is not tagged")

# Check for reading order
reading_order = auditor.get_reading_order()
print(f"Reading order: {reading_order}")

# Check for alt text
images = auditor.get_images()
for img in images:
    if not img.alt_text:
        print(f"❌ Image missing alt text: {img.page}:{img.position}")

# Check for document structure
structure = auditor.get_structure()
print(f"Headings: {structure.headings}")
print(f"Lists: {structure.lists}")
print(f"Tables: {structure.tables}")

# Check for language
if not auditor.has_language():
    print("❌ Document language not specified")

# Check for metadata
metadata = auditor.get_metadata()
print(f"Title: {metadata.title}")
print(f"Author: {metadata.author}")
print(f"Subject: {metadata.subject}")
```

## PDF Accessibility Checklist

### Document Structure
- [ ] PDF is tagged (PDF/UA compliant)
- [ ] Reading order is logical
- [ ] Headings are properly structured (H1-H6)
- [ ] Lists are properly marked (L, LI, LBody)
- [ ] Tables have proper structure (TH, TD, headers)
- [ ] Bookmarks/Outlines are present for navigation

### Text Content
- [ ] Language is specified (Lang attribute)
- [ ] All text is accessible (not images)
- [ ] Fonts are embedded
- [ ] Text is selectable and copyable
- [ ] Unicode mapping is correct

### Images and Graphics
- [ ] All images have alt text
- [ ] Decorative images are marked as artifacts
- [ ] Complex images have extended descriptions
- [ ] Charts and graphs have data tables
- [ ] Image text (OCR) is provided for scanned documents

### Links and Navigation
- [ ] Links are properly tagged
- [ ] Link text is descriptive
- [ ] Bookmarks work correctly
- [ ] Tab order is logical
- [ ] Skip navigation is available

### Forms
- [ ] Form fields have labels
- [ ] Form fields have tooltips
- [ ] Tab order is logical
- [ ] Required fields are marked
- [ ] Error messages are accessible

### Tables
- [ ] Tables have header cells (TH)
- [ ] Header cells are associated with data cells
- [ ] Tables have captions
- [ ] Complex tables have summaries
- [ ] Nested tables are avoided

### Color and Contrast
- [ ] Color contrast ratio is at least 4.5:1
- [ ] Information is not conveyed by color alone
- [ ] Background and foreground are distinguishable
- [ ] Focus indicators are visible

### Interactive Elements
- [ ] Form fields are keyboard accessible
- [ ] Buttons have accessible names
- [ ] Checkboxes and radios are properly labeled
- [ ] Dropdown menus are accessible

## Common Issues and Fixes

### Issue 1: Untagged PDF
**Problem:** PDF contains no structure tags.

**Fix:**
```python
# Add tags programmatically
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

# Add tags
for page in reader.pages:
    # Add structural elements
    writer.add_page(page)

# Set as tagged PDF
writer.set_tagged_pdf(True)
writer.write("document_tagged.pdf")
```

### Issue 2: Missing Alt Text
**Problem:** Images lack alternative text.

**Fix:**
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    for image in page.images:
        # Add alt text
        writer.add_image(
            page,
            image,
            alt_text="Description of image"
        )

writer.write("document_fixed.pdf")
```

### Issue 3: Incorrect Reading Order
**Problem:** Screen readers read content in wrong order.

**Fix:**
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

# Reorder content
for page in reader.pages:
    # Define reading order
    reading_order = [
        page.find('H1'),
        page.find('P', index=0),
        page.find('H2'),
        page.find('P', index=1),
        # ...
    ]
    
    # Set reading order
    writer.set_reading_order(page, reading_order)

writer.write("document_reordered.pdf")
```

### Issue 4: Missing Language
**Problem:** Document language not specified.

**Fix:**
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

# Set document language
writer.set_language("en-US")  # For English
# writer.set_language("tr-TR")  # For Turkish

writer.write("document_with_language.pdf")
```

## Automated Testing Tools

### Adobe Acrobat Pro
```python
# Use Adobe Acrobat Pro via CLI
import subprocess

def run_acrobat_accessibility_check(pdf_path):
    subprocess.run([
        "acrobat",
        "/A", "AccessChecker",
        "/O", pdf_path,
        "/R", "accessibility_report.pdf"
    ])
```

### PAC 3 (PDF Accessibility Checker)
```bash
# Run PAC 3
pac3 --check document.pdf --output report.html
```

### CommonLook PDF
```bash
# Run CommonLook PDF
commonlook --check document.pdf --standard WCAG2.1-AA
```

## PDF/UA Compliance Report

### Generate Report
```python
from accessmind import PDFAuditor

auditor = PDFAuditor(file="document.pdf")

# Generate compliance report
report = auditor.generate_report(
    standards=["PDF/UA-1", "WCAG2.1-AA", "Section508"],
    format="html"
)

# Save report
report.save("pdf-compliance-report.html")

# Export to JSON
report.export_json("pdf-compliance-report.json")

# Export to PDF
report.export_pdf("pdf-compliance-report.pdf")
```

### Report Contents
```json
{
  "document": "document.pdf",
  "timestamp": "2024-01-15T10:30:00Z",
  "standards": ["PDF/UA-1", "WCAG2.1-AA"],
  "score": 85,
  "summary": {
    "total_issues": 15,
    "critical": 2,
    "serious": 5,
    "moderate": 8
  },
  "violations": [
    {
      "id": "PDF-UA-001",
      "standard": "PDF/UA-1",
      "type": "untagged",
      "severity": "critical",
      "message": "Document is not tagged",
      "page": null,
      "fix": "Add structure tags to document"
    }
  ]
}
```

## Best Practices

### Creating Accessible PDFs

#### From Word
1. Use built-in heading styles (Heading 1-6)
2. Add alt text to all images
3. Use proper table structure
4. Add document properties (title, author, language)
5. Use the Accessibility Checker
6. Export as tagged PDF

#### From InDesign
1. Use proper paragraph styles
2. Create articles for reading order
3. Add alt text to images
4. Use Object Export Options
5. Create a tagged PDF

#### From HTML
1. Use semantic HTML (h1-h6, ul, ol, table)
2. Add alt attributes to images
3. Use proper table headers
4. Add ARIA attributes if needed
5. Convert using accessible PDF tool

### Testing Workflow
1. **Pre-flight Check:** Verify PDF opens correctly
2. **Automated Scan:** Run PDFAuditor
3. **Manual Testing:** Use screen reader
4. **Remediation:** Fix identified issues
5. **Re-test:** Verify fixes
6. **Documentation:** Create VPAT if needed
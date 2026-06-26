---
name: document-generator
description: Generate professional Word, Excel, and PDF documents with rich formatting, tables, images, and layouts. Use this skill whenever the user mentions creating documents, generating reports, exporting to DOCX/XLSX/PDF, making spreadsheets, building presentations in document form, or needs any kind of formatted document output. This includes requests like "create a report", "generate an Excel file", "export to PDF", "make a Word document", "build a spreadsheet", or even indirect mentions like "I need this data in a table" or "format this as a document".
---

# Document Generator Skill

Generate professional Word (.docx), Excel (.xlsx), and PDF documents with comprehensive formatting support including fonts, colors, tables, images, layouts, and more.

## When to Use This Skill

Use this skill when the user needs to:
- Create Word documents with rich formatting (headings, paragraphs, tables, images, styles)
- Generate Excel spreadsheets with formulas, styling, and data
- Export content to PDF format with professional layouts
- Work with document templates and fill them with data
- Create reports, invoices, data exports, or any formatted document output

## Core Capabilities

### Word Documents (.docx)
- Text formatting: font family, size, color, bold, italic, underline
- Paragraph styles: alignment, spacing, indentation
- Tables with custom styling and borders
- Images with positioning and sizing
- Headers and footers
- Page layout: margins, orientation, page size
- Bullet and numbered lists
- Hyperlinks

### Excel Spreadsheets (.xlsx)
- Cell formatting: font, size, color, background
- Formulas and calculations
- Multiple sheets
- Column widths and row heights
- Cell borders and alignment
- Number formatting (currency, percentage, dates)
- Merged cells
- Freeze panes

### PDF Documents (.pdf)
- Text with custom fonts, sizes, and colors
- Paragraphs with alignment
- Tables with styling
- Images
- Page layout and margins
- Multi-page documents
- Headers and footers

## How to Use

### Step 1: Understand the Requirements

Ask clarifying questions if needed:
- What type of document? (Word/Excel/PDF)
- What content should it contain?
- Any specific formatting requirements?
- Should it use a template?
- Where should the output be saved?

### Step 2: Choose the Right Script

The skill provides three main scripts in the `scripts/` directory:
- `generate_word.py` - For Word documents
- `generate_excel.py` - For Excel spreadsheets  
- `generate_pdf.py` - For PDF documents

Each script accepts a JSON configuration that describes the document structure and content.

### Step 3: Prepare the Configuration

Create a JSON configuration file that describes the document. The structure varies by document type - see the reference files for detailed schemas:
- `references/word_schema.md` - Word document configuration
- `references/excel_schema.md` - Excel spreadsheet configuration
- `references/pdf_schema.md` - PDF document configuration

### Step 4: Generate the Document

Run the appropriate script with the configuration:

```bash
python document-generator/scripts/generate_word.py config.json output.docx
python document-generator/scripts/generate_excel.py config.json output.xlsx
python document-generator/scripts/generate_pdf.py config.json output.pdf
```

### Step 5: Verify and Iterate

Check the generated document and make adjustments to the configuration if needed.

## Working with Templates

All three document types support template-based generation:

1. **Word Templates**: Use existing .docx files and replace placeholders
2. **Excel Templates**: Use existing .xlsx files and fill in data
3. **PDF Templates**: Define reusable layouts in the configuration

To use a template, include a `template` field in your configuration pointing to the template file path.

## Configuration Examples

### Simple Word Document

```json
{
  "page_setup": {
    "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1}
  },
  "content": [
    {
      "type": "heading",
      "text": "Monthly Report",
      "level": 1
    },
    {
      "type": "paragraph",
      "text": "This is the report content.",
      "font": {"name": "Arial", "size": 11}
    }
  ]
}
```

### Simple Excel Spreadsheet

```json
{
  "sheets": [
    {
      "name": "Sales Data",
      "data": [
        ["Product", "Quantity", "Price", "Total"],
        ["Widget A", 10, 25.50, "=B2*C2"],
        ["Widget B", 5, 30.00, "=B3*C3"]
      ],
      "formatting": {
        "header_row": 0,
        "column_widths": [15, 10, 10, 10]
      }
    }
  ]
}
```

### Simple PDF Document

```json
{
  "page_setup": {
    "size": "A4",
    "margins": {"top": 20, "bottom": 20, "left": 20, "right": 20}
  },
  "content": [
    {
      "type": "text",
      "text": "Invoice #12345",
      "font": {"name": "Helvetica-Bold", "size": 18}
    },
    {
      "type": "paragraph",
      "text": "Thank you for your business.",
      "font": {"name": "Helvetica", "size": 12}
    }
  ]
}
```

## Best Practices

1. **Start Simple**: Begin with basic formatting and add complexity as needed
2. **Use Templates**: For recurring document types, create templates to save time
3. **Validate Data**: Check that data types match expected formats (numbers, dates, etc.)
4. **Test Incrementally**: Generate documents frequently during development to catch issues early
5. **Handle Errors Gracefully**: Provide clear error messages if configuration is invalid

## Troubleshooting

**Missing Dependencies**: If scripts fail, ensure required Python packages are installed:
```bash
pip install python-docx openpyxl reportlab Pillow
```

**Font Issues**: If custom fonts don't work, verify the font name is correct and available on the system.

**Image Problems**: Ensure image paths are absolute or relative to the script execution directory.

**Excel Formulas**: Use Excel formula syntax (e.g., `=SUM(A1:A10)`) as strings in the data array.

## Advanced Features

For complex documents, refer to the detailed reference files:
- `references/word_schema.md` - Complete Word configuration options
- `references/excel_schema.md` - Complete Excel configuration options
- `references/pdf_schema.md` - Complete PDF configuration options

These references include examples of:
- Complex table layouts
- Image positioning and sizing
- Advanced styling and themes
- Multi-page layouts
- Template variable substitution
- Conditional formatting

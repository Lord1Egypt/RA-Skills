# PDF Document Configuration Schema

Complete reference for PDF document JSON configuration.

## Important Notes

### Chinese Font Support

The PDF generator automatically detects and uses Chinese fonts on your system:
- Windows: Microsoft YaHei (msyh.ttc), SimSun (simsun.ttc), or SimHei (simhei.ttf)
- If no Chinese font is found, Chinese characters may not display correctly

For best results with Chinese text, the generator will automatically use the system Chinese font unless you specify a different font in the configuration.

## Top-Level Structure

```json
{
  "page_setup": { ... },     // Optional: page configuration
  "content": [ ... ]         // Array of content elements
}
```

## Page Setup

```json
{
  "page_setup": {
    "size": "A4",  // letter, a4, legal
    "margins": {
      "top": 20,      // millimeters
      "bottom": 20,
      "left": 20,
      "right": 20
    }
  }
}
```

## Content Elements

### Heading

```json
{
  "type": "heading",
  "text": "Chapter Title",
  "level": 1,  // 1-6
  "alignment": "left",  // left, center, right, justify
  "font": {
    "name": "Helvetica-Bold",
    "size": 18,
    "color": "#000000",
    "bold": true,
    "italic": false,
    "underline": false
  }
}
```

### Text / Paragraph

```json
{
  "type": "text",  // or "paragraph"
  "text": "This is a paragraph with formatting.",
  "alignment": "left",
  "font": {
    "name": "Helvetica",
    "size": 12,
    "color": "#333333",
    "bold": false,
    "italic": false,
    "underline": false
  }
}
```

### Table

```json
{
  "type": "table",
  "data": [
    ["Header 1", "Header 2", "Header 3"],
    ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
    ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
  ],
  "style": {
    "header_row": 0,  // Row index to style as header
    "cell_backgrounds": {
      "0,0": "#4472C4",  // Row 0, Column 0
      "0,1": "#4472C4",
      "0,2": "#4472C4"
    }
  }
}
```

### Image

```json
{
  "type": "image",
  "path": "path/to/image.png",
  "width": 4,   // inches, required
  "height": 3   // inches, optional (maintains aspect ratio if omitted)
}
```

### List

```json
{
  "type": "list",
  "items": [
    "First item",
    "Second item",
    "Third item"
  ],
  "list_type": "bullet",  // or "number"
  "font": {
    "name": "Helvetica",
    "size": 11
  }
}
```

### Spacer

```json
{
  "type": "spacer",
  "height": 0.5  // inches
}
```

### Page Break

```json
{
  "type": "page_break"
}
```

## Font Names

ReportLab built-in fonts:
- Helvetica
- Helvetica-Bold
- Helvetica-Oblique
- Helvetica-BoldOblique
- Times-Roman
- Times-Bold
- Times-Italic
- Times-BoldItalic
- Courier
- Courier-Bold
- Courier-Oblique
- Courier-BoldOblique

## Complete Example

```json
{
  "page_setup": {
    "size": "A4",
    "margins": {
      "top": 25,
      "bottom": 25,
      "left": 25,
      "right": 25
    }
  },
  "content": [
    {
      "type": "heading",
      "text": "Invoice #INV-2024-001",
      "level": 1,
      "alignment": "center",
      "font": {
        "name": "Helvetica-Bold",
        "size": 24,
        "color": "#2E5090"
      }
    },
    {
      "type": "spacer",
      "height": 0.3
    },
    {
      "type": "text",
      "text": "Date: March 18, 2024",
      "alignment": "right",
      "font": {
        "name": "Helvetica",
        "size": 10
      }
    },
    {
      "type": "spacer",
      "height": 0.5
    },
    {
      "type": "heading",
      "text": "Bill To:",
      "level": 3,
      "font": {
        "name": "Helvetica-Bold",
        "size": 12
      }
    },
    {
      "type": "paragraph",
      "text": "Acme Corporation<br/>123 Business St<br/>City, State 12345",
      "font": {
        "name": "Helvetica",
        "size": 11
      }
    },
    {
      "type": "spacer",
      "height": 0.5
    },
    {
      "type": "table",
      "data": [
        ["Item", "Quantity", "Unit Price", "Total"],
        ["Professional Services", "10 hours", "$150.00", "$1,500.00"],
        ["Consulting", "5 hours", "$200.00", "$1,000.00"],
        ["", "", "Subtotal:", "$2,500.00"],
        ["", "", "Tax (10%):", "$250.00"],
        ["", "", "Total:", "$2,750.00"]
      ],
      "style": {
        "header_row": 0,
        "cell_backgrounds": {
          "0,0": "#4472C4",
          "0,1": "#4472C4",
          "0,2": "#4472C4",
          "0,3": "#4472C4"
        }
      }
    },
    {
      "type": "spacer",
      "height": 0.5
    },
    {
      "type": "heading",
      "text": "Payment Terms",
      "level": 3
    },
    {
      "type": "list",
      "items": [
        "Payment due within 30 days",
        "Late payments subject to 1.5% monthly interest",
        "Make checks payable to: Your Company Name"
      ],
      "list_type": "bullet",
      "font": {
        "name": "Helvetica",
        "size": 10
      }
    },
    {
      "type": "page_break"
    },
    {
      "type": "heading",
      "text": "Terms and Conditions",
      "level": 2
    },
    {
      "type": "paragraph",
      "text": "This invoice is subject to our standard terms and conditions...",
      "alignment": "justify",
      "font": {
        "name": "Times-Roman",
        "size": 10
      }
    }
  ]
}
```

## Tips

1. **Colors**: Use hex format like `#4472C4`
2. **Measurements**: 
   - Margins are in millimeters
   - Image sizes and spacers are in inches
3. **Line Breaks**: Use `<br/>` in text for line breaks
4. **Markup**: Text supports basic HTML-like markup: `<b>`, `<i>`, `<u>`
5. **Tables**: Grid lines are added automatically
6. **Images**: Must provide width; height is optional (maintains aspect ratio)

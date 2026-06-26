# Word Document Configuration Schema

Complete reference for Word document JSON configuration.

## Top-Level Structure

```json
{
  "template": "path/to/template.docx",  // Optional: use existing template
  "page_setup": { ... },                 // Optional: page configuration
  "content": [ ... ]                     // Array of content elements
}
```

## Page Setup

```json
{
  "page_setup": {
    "margins": {
      "top": 1,      // inches
      "bottom": 1,
      "left": 1,
      "right": 1
    },
    "orientation": "portrait"  // or "landscape"
  }
}
```

## Content Elements

### Heading

```json
{
  "type": "heading",
  "text": "Chapter Title",
  "level": 1,  // 1-9, where 1 is largest
  "font": {
    "name": "Arial",
    "size": 16,
    "color": "#000000",
    "bold": true,
    "italic": false,
    "underline": false
  }
}
```

### Paragraph

```json
{
  "type": "paragraph",
  "text": "This is a paragraph with formatting.",
  "alignment": "left",  // left, center, right, justify
  "font": {
    "name": "Times New Roman",
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
  "style": "Table Grid",  // Word table style name
  "cell_formatting": {
    "0,0": {  // Row 0, Column 0
      "background": "#4472C4",
      "font": {
        "color": "#FFFFFF",
        "bold": true
      }
    }
  }
}
```

### Image

```json
{
  "type": "image",
  "path": "path/to/image.png",
  "width": 4,   // inches, optional
  "height": 3   // inches, optional
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
  "type": "bullet",  // or "number"
  "font": {
    "name": "Arial",
    "size": 11
  }
}
```

### Page Break

```json
{
  "type": "page_break"
}
```

## Complete Example

```json
{
  "page_setup": {
    "margins": {
      "top": 1,
      "bottom": 1,
      "left": 1.25,
      "right": 1.25
    },
    "orientation": "portrait"
  },
  "content": [
    {
      "type": "heading",
      "text": "Annual Report 2024",
      "level": 1,
      "font": {
        "name": "Arial",
        "size": 24,
        "color": "#2E5090",
        "bold": true
      }
    },
    {
      "type": "paragraph",
      "text": "Executive Summary",
      "alignment": "left",
      "font": {
        "name": "Arial",
        "size": 14,
        "bold": true
      }
    },
    {
      "type": "paragraph",
      "text": "This report summarizes our company's performance for the fiscal year 2024.",
      "alignment": "justify",
      "font": {
        "name": "Times New Roman",
        "size": 12
      }
    },
    {
      "type": "table",
      "data": [
        ["Quarter", "Revenue", "Profit"],
        ["Q1", "$1.2M", "$200K"],
        ["Q2", "$1.5M", "$300K"],
        ["Q3", "$1.8M", "$400K"],
        ["Q4", "$2.0M", "$500K"]
      ],
      "style": "Light Grid Accent 1",
      "cell_formatting": {
        "0,0": {"background": "#4472C4", "font": {"color": "#FFFFFF", "bold": true}},
        "0,1": {"background": "#4472C4", "font": {"color": "#FFFFFF", "bold": true}},
        "0,2": {"background": "#4472C4", "font": {"color": "#FFFFFF", "bold": true}}
      }
    },
    {
      "type": "page_break"
    },
    {
      "type": "heading",
      "text": "Key Achievements",
      "level": 2
    },
    {
      "type": "list",
      "items": [
        "Increased revenue by 40%",
        "Expanded to 3 new markets",
        "Launched 5 new products"
      ],
      "type": "bullet"
    },
    {
      "type": "image",
      "path": "chart.png",
      "width": 5
    }
  ]
}
```

## Font Names

Common font names that work across systems:
- Arial
- Times New Roman
- Calibri
- Cambria
- Georgia
- Verdana
- Courier New

## Table Styles

Common Word table styles:
- Table Grid
- Light Shading
- Light List
- Light Grid
- Medium Shading 1
- Medium Shading 2
- Medium Grid 1
- Colorful List
- Colorful Grid

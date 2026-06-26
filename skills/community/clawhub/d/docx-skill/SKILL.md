---
name: docx
version: 2.0.0
description: Create, read, edit, and manipulate Word documents (.docx). Supports text, tables, images, headers, footers, styles, and tracked changes.
category: document-processing
license: MIT
---

# DOCX Skill v2.0

## Overview

Complete Microsoft Word document processing using `docx-js` library for creation and XML manipulation for editing. A .docx file is a ZIP archive containing XML files.

## Installation & Dependencies

### Required
```bash
# For creating documents
npm install -g docx

# For text extraction
brew install pandoc

# For validation (optional)
pip install python-docx
```

### Optional
```bash
# For PDF conversion
brew install --cask libreoffice

# For image processing
brew install imagemagick
```

## Quick Start

### Create Your First Document
```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: "Hello World!", bold: true, size: 32 })
        ]
      })
    ]
  }]
});

await Packer.toBuffer(doc).then(buffer => {
  require('fs').writeFileSync("hello.docx", buffer);
});
console.log("✓ Document created!");
```

### Read Document Content
```bash
# Extract text with pandoc
pandoc document.docx -o output.md

# Or with Python
python -c "from docx import Document; doc = Document('file.docx'); print('\n'.join([p.text for p in doc.paragraphs]))"
```

## Complete API Reference

### Document Structure

```javascript
const { Document, Packer, Section } = require('docx');

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter (DXA units)
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch
      }
    },
    children: [/* paragraphs, tables, etc */]
  }]
});
```

### Paragraphs

```javascript
const { Paragraph, TextRun, PageBreak } = require('docx');

// Basic paragraph
new Paragraph({
  children: [new TextRun("Simple text")]
})

// Formatted paragraph
new Paragraph({
  children: [
    new TextRun({
      text: "Bold and ",
      bold: true,
      size: 28,  // 14pt (size is half-points)
      font: "Arial"
    }),
    new TextRun({
      text: "italic",
      italics: true,
      color: "FF0000"  // Red in hex
    })
  ],
  spacing: {
    before: 200,   // Space before paragraph
    after: 200,    // Space after paragraph
    line: 360      // Line height (1.5 = 360)
  },
  alignment: "center"  // left, center, right, justified
})

// Heading
new Paragraph({
  heading: "Heading1",
  children: [new TextRun("Chapter Title")]
})

// Page break
new Paragraph({
  children: [new PageBreak()]
})
```

### Lists

```javascript
const { LevelFormat } = require('docx');

// Configure numbering in document
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: "left",
          style: {
            paragraph: { indent: { left: 720, hanging: 360 } }
          }
        }]
      },
      {
        reference: "number-list",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "%1.",
          alignment: "left",
          style: {
            paragraph: { indent: { left: 720, hanging: 360 } }
          }
        }]
      }
    ]
  },
  sections: [{
    children: [
      // Bullet list item
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Bullet point")]
      }),
      // Numbered list item
      new Paragraph({
        numbering: { reference: "number-list", level: 0 },
        children: [new TextRun("Numbered item")]
      })
    ]
  }]
});
```

### Tables

```javascript
const { Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType } = require('docx');

// Create table
new Table({
  width: { size: 9360, type: WidthType.DXA },  // Full content width
  columnWidths: [4680, 4680],  // Two equal columns
  
  rows: [
    // Header row
    new TableRow({
      children: [
        new TableCell({
          children: [new Paragraph({ children: [new TextRun("Header 1")] })],
          shading: { fill: "4472C4", type: ShadingType.SOLID },
          borders: {
            top: { style: BorderStyle.SINGLE, size: 1 },
            bottom: { style: BorderStyle.SINGLE, size: 1 },
            left: { style: BorderStyle.SINGLE, size: 1 },
            right: { style: BorderStyle.SINGLE, size: 1 }
          }
        }),
        new TableCell({
          children: [new Paragraph({ children: [new TextRun("Header 2")] })],
          shading: { fill: "4472C4", type: ShadingType.SOLID },
          borders: {
            top: { style: BorderStyle.SINGLE, size: 1 },
            bottom: { style: BorderStyle.SINGLE, size: 1 },
            left: { style: BorderStyle.SINGLE, size: 1 },
            right: { style: BorderStyle.SINGLE, size: 1 }
          }
        })
      ]
    }),
    // Data row
    new TableRow({
      children: [
        new TableCell({
          children: [new Paragraph({ children: [new TextRun("Data 1")] })],
          borders: {
            top: { style: BorderStyle.SINGLE, size: 1 },
            bottom: { style: BorderStyle.SINGLE, size: 1 },
            left: { style: BorderStyle.SINGLE, size: 1 },
            right: { style: BorderStyle.SINGLE, size: 1 }
          }
        }),
        new TableCell({
          children: [new Paragraph({ children: [new TextRun("Data 2")] })],
          borders: {
            top: { style: BorderStyle.SINGLE, size: 1 },
            bottom: { style: BorderStyle.SINGLE, size: 1 },
            left: { style: BorderStyle.SINGLE, size: 1 },
            right: { style: BorderStyle.SINGLE, size: 1 }
          }
        })
      ]
    })
  ]
})
```

### Images

```javascript
const { ImageRun } = require('docx');
const fs = require('fs');

new Paragraph({
  children: [
    new ImageRun({
      type: "png",  // Required: png, jpg, jpeg, gif, bmp, svg
      data: fs.readFileSync("image.png"),
      transformation: {
        width: 400,
        height: 300
      },
      altText: {
        title: "Image Title",
        description: "Image Description",
        name: "image-name"
      }
    })
  ]
})
```

### Headers and Footers

```javascript
const { Header, Footer, PageNumber } = require('docx');

const doc = new Document({
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            children: [
              new TextRun({ text: "Document Header", bold: true })
            ],
            alignment: "center"
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            children: [
              new TextRun("Page "),
              new TextRun({ children: [PageNumber.CURRENT] }),
              new TextRun(" of "),
              new TextRun({ children: [PageNumber.TOTAL_PAGES] })
            ],
            alignment: "center"
          })
        ]
      })
    },
    children: [/* content */]
  }]
});
```

### Table of Contents

```javascript
const { TableOfContents, HeadingLevel } = require('docx');

const doc = new Document({
  sections: [{
    children: [
      // TOC must come before headings
      new TableOfContents("Table of Contents", {
        hyperlink: true,
        headingStyleRange: "1-3"  // Include H1, H2, H3
      }),
      
      new Paragraph({ children: [new PageBreak()] }),
      
      // Headings for TOC
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Chapter 1")]
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Section 1.1")]
      })
    ]
  }]
});
```

## Complete Examples

### Example 1: Business Report

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, HeadingLevel, TableOfContents, PageBreak, WidthType } = require('docx');
const fs = require('fs');

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Title Page
      new Paragraph({
        children: [
          new TextRun({ text: "Annual Report 2024", bold: true, size: 48, font: "Arial" })
        ],
        spacing: { after: 400 },
        alignment: "center"
      }),
      new Paragraph({
        children: [new TextRun({ text: "Company Name", size: 24 })],
        alignment: "center"
      }),
      new Paragraph({ children: [new PageBreak()] }),
      
      // Table of Contents
      new TableOfContents("Contents", { headingStyleRange: "1-2" }),
      new Paragraph({ children: [new PageBreak()] }),
      
      // Executive Summary
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Executive Summary")]
      }),
      new Paragraph({
        children: [new TextRun("This report provides an overview of...")]
      }),
      
      // Financial Table
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Financial Summary")]
      }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3120, 3120, 3120],
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun("Metric")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("2023")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("2024")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun("Revenue")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("$10M")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("$12M")] })] })
            ]
          })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("annual-report.docx", buffer);
  console.log("✓ Report created!");
});
```

### Example 2: Invoice Template

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle } = require('docx');
const fs = require('fs');

const doc = new Document({
  sections: [{
    children: [
      // Header
      new Paragraph({
        children: [new TextRun({ text: "INVOICE", bold: true, size: 36 })],
        alignment: "center",
        spacing: { after: 400 }
      }),
      
      // Invoice Details
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                children: [
                  new Paragraph({ children: [new TextRun({ text: "From:", bold: true })] }),
                  new Paragraph({ children: [new TextRun("Company Name")] }),
                  new Paragraph({ children: [new TextRun("123 Business St")] }),
                  new Paragraph({ children: [new TextRun("city@example.com")] })
                ]
              }),
              new TableCell({
                children: [
                  new Paragraph({ children: [new TextRun({ text: "To:", bold: true })] }),
                  new Paragraph({ children: [new TextRun("Client Name")] }),
                  new Paragraph({ children: [new TextRun("456 Client Ave")] }),
                  new Paragraph({ children: [new TextRun("client@example.com")] })
                ]
              })
            ]
          })
        ]
      }),
      
      new Paragraph({ children: [new TextRun("") ], spacing: { before: 200 } }),
      
      // Invoice Info
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 2340, 2340, 2340],
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Invoice #", bold: true })] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("INV-2024-001")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Date", bold: true })] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("2024-01-15")] })] })
            ]
          })
        ]
      }),
      
      new Paragraph({ children: [new TextRun("") ], spacing: { before: 400 } }),
      
      // Items Table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [4680, 2340, 2340],
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Description", bold: true })] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Qty", bold: true })] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Amount", bold: true })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun("Web Development")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("40")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("$4,000")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun("Design")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("20")] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun("$2,000")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Total:", bold: true })] })] }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$6,000", bold: true })] })] })
            ]
          })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("invoice.docx", buffer);
  console.log("✓ Invoice created!");
});
```

### Example 3: Resume/CV

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, HeadingLevel } = require('docx');
const fs = require('fs');

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1000, right: 1000, bottom: 1000, left: 1000 }
      }
    },
    children: [
      // Name and Contact
      new Paragraph({
        children: [new TextRun({ text: "JOHN DOE", bold: true, size: 36, font: "Arial" })],
        alignment: "center"
      }),
      new Paragraph({
        children: [new TextRun("john.doe@email.com | (555) 123-4567 | LinkedIn")],
        alignment: "center",
        spacing: { after: 300 }
      }),
      
      // Experience Section
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("EXPERIENCE")]
      }),
      
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 7020],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                children: [new Paragraph({ children: [new TextRun({ text: "2020 - Present", bold: true })] })]
              }),
              new TableCell({
                children: [
                  new Paragraph({ children: [new TextRun({ text: "Senior Developer", bold: true })] }),
                  new Paragraph({ children: [new TextRun("Company Name")] }),
                  new Paragraph({ children: [new TextRun("• Led development of...")] }),
                  new Paragraph({ children: [new TextRun("• Managed team of...")] })
                ]
              })
            ]
          })
        ]
      }),
      
      // Education Section
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("EDUCATION")]
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Bachelor of Science in Computer Science", bold: true }),
          new TextRun(" | University Name | 2016-2020")
        ]
      }),
      
      // Skills Section
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("SKILLS")]
      }),
      new Paragraph({
        children: [new TextRun("JavaScript, Python, React, Node.js, SQL, AWS, Docker, Git")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("resume.docx", buffer);
  console.log("✓ Resume created!");
});
```

## Editing Existing Documents

### Method 1: Unpack → Edit → Repack

```bash
# Step 1: Unpack the document
python scripts/office/unpack.py document.docx unpacked/

# Step 2: Edit XML files in unpacked/word/
# Edit document.xml, styles.xml, etc.

# Step 3: Repack
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

### Method 2: Using python-docx

```python
from docx import Document

# Load existing document
doc = Document('existing.docx')

# Read paragraphs
for para in doc.paragraphs:
    print(para.text)

# Edit content
doc.paragraphs[0].text = "New first paragraph"

# Add new paragraph
doc.add_paragraph("New paragraph at end")

# Save
doc.save('edited.docx')
```

### Method 3: Find and Replace

```python
from docx import Document

def find_and_replace(doc_path, find_text, replace_text, output_path):
    doc = Document(doc_path)
    
    for para in doc.paragraphs:
        if find_text in para.text:
            para.text = para.text.replace(find_text, replace_text)
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if find_text in cell.text:
                    cell.text = cell.text.replace(find_text, replace_text)
    
    doc.save(output_path)

# Usage
find_and_replace('template.docx', '{{NAME}}', 'John Doe', 'output.docx')
```

## Page Sizes Reference

All sizes in DXA units (1440 DXA = 1 inch):

| Paper Size | Width | Height | Use Case |
|------------|-------|--------|----------|
| US Letter | 12,240 | 15,840 | Default US |
| A4 | 11,906 | 16,838 | Default EU |
| Legal | 12,240 | 20,160 | Legal docs |
| Tabloid | 19,840 | 25,920 | Posters |
| Statement | 9,360 | 12,240 | Small docs |

## Smart Quotes & Special Characters

Use XML entities for professional typography:

| Entity | Character | Name |
|--------|-----------|------|
| `&#x2018;` | ' | Left single quote |
| `&#x2019;` | ' | Right single quote / apostrophe |
| `&#x201C;` | " | Left double quote |
| `&#x201D;` | " | Right double quote |
| `&#x2013;` | – | En dash |
| `&#x2014;` | — | Em dash |
| `&#x00A9;` | © | Copyright |
| `&#x00AE;` | ® | Registered trademark |
| `&#x2122;` | ™ | Trademark |

## Error Handling

### Common Errors

#### Error: "Font not found"
```javascript
// Solution: Use web-safe fonts
new TextRun({ text: "Content", font: "Arial" })  // ✅ Safe
new TextRun({ text: "Content", font: "CustomFont" })  // ❌ May fail
```

#### Error: "Image not loading"
```javascript
// Solution: Check file path and type
new ImageRun({
  type: "png",  // Must match actual file type
  data: fs.readFileSync("./images/logo.png"),  // Correct path
  transformation: { width: 200, height: 150 }
})
```

#### Error: "Table rendering incorrectly"
```javascript
// Solution: Set both table width AND cell widths
new Table({
  width: { size: 9360, type: WidthType.DXA },  // Required
  columnWidths: [4680, 4680],  // Required, must sum to table width
  rows: [...]
})
```

## Best Practices

### 1. Always Set Page Size Explicitly
```javascript
// docx-js defaults to A4
properties: {
  page: {
    size: { width: 12240, height: 15840 }  // US Letter
  }
}
```

### 2. Use Styles Consistently
```javascript
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 24 }  // 12pt default
      }
    }
  }
});
```

### 3. Never Use Unicode Bullets
```javascript
// ❌ WRONG
new Paragraph({ children: [new TextRun("• Item")] })

// ✅ CORRECT
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  children: [new TextRun("Item")]
})
```

### 4. Validate Before Distribution
```bash
# Check document integrity
python scripts/office/validate.py document.docx

# Or with pandoc
pandoc document.docx -o /dev/null && echo "✓ Valid"
```

## Testing Your Setup

```javascript
// test-docx.js
const { Document, Packer, Paragraph, TextRun } = require('docx');
const fs = require('fs');

async function test() {
  console.log("Testing docx setup...");
  
  const doc = new Document({
    sections: [{
      children: [
        new Paragraph({
          children: [new TextRun("Test document created successfully!")]
        })
      ]
    }]
  });
  
  await Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("test-output.docx", buffer);
  });
  
  console.log("✓ Test passed! Check test-output.docx");
}

test().catch(console.error);
```

Run test:
```bash
node test-docx.js
```

## License

MIT License - See LICENSE file for details.

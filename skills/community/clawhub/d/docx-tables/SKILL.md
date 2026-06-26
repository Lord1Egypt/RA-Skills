---
name: docx-tables
version: 2.0.0
description: Create Word documents with properly formatted tables using docx npm library. Tables work consistently across Word and Google Docs. Use when creating DOCX files with tables, especially itineraries, schedules, or data tables.
author: Jimmy
tags:
  - docx
  - word
  - tables
  - document
---

# docx-tables

Create Word documents with tables that **work everywhere** - Word, Google Docs, etc.

## ⚠️ THE 5 CRITICAL RULES

### 1. Dual-Width Sizing (MOST CRITICAL)

Set widths in **TWO places** - on table AND on each cell:

```javascript
// Table level
new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1872, 7488],
  rows: [...]
})

// Cell level - EVERY cell needs width!
new TableCell({
  width: { size: 1872, type: WidthType.DXA },
  children: [...]
})
```

### 2. Use DXA Only, Never Percentages

Percentages break in Google Docs. Use DXA:
- 1 inch = 1440 DXA
- US Letter with 1" margins = 9360 DXA

```javascript
// ❌ WRONG
width: { size: 100, type: WidthType.PERCENTAGE }

// ✅ CORRECT
width: { size: 9360, type: WidthType.DXA }
```

### 3. Use ShadingType.CLEAR

```javascript
const { ShadingType } = require('docx');

// ❌ WRONG - black background!
shading: { type: ShadingType.SOLID, fill: "E0F2F1" }

// ✅ CORRECT
shading: { type: ShadingType.CLEAR, fill: "E0F2F1" }
```

### 4. Add Cell Padding

```javascript
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

new TableCell({
  margins: cellMargins,
  children: [...]
})
```

### 5. Column Widths Must Sum Exactly

For 1" margins: **9360 DXA**

```javascript
columnWidths: [1872, 7488]  // = 9360 ✓
columnWidths: [3120, 3120, 3120]  // = 9360 ✓
```

## Complete Working Example

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
         WidthType, AlignmentType, BorderStyle, TableLayoutType, ShadingType } = require('docx');
const fs = require('fs');

const TOTAL_WIDTH = 9360;
const COL1 = 1872;
const COL2 = 7488;

const cellBorders = {
  top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  left: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  right: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }
};

const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

const doc = new Document({
  sections: [{
    properties: { 
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      new Table({
        layout: TableLayoutType.FIXED,
        width: { size: TOTAL_WIDTH, type: WidthType.DXA },
        columnWidths: [COL1, COL2],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Header", bold: true, color: "FFFFFF" })],
                  alignment: AlignmentType.CENTER
                })],
                width: { size: TOTAL_WIDTH, type: WidthType.DXA },
                columnSpan: 2,
                shading: { type: ShadingType.CLEAR, fill: "1565C0" },
                borders: cellBorders,
                margins: cellMargins
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                children: [new Paragraph("Col 1")],
                width: { size: COL1, type: WidthType.DXA },
                borders: cellBorders,
                margins: cellMargins
              }),
              new TableCell({
                children: [new Paragraph("Col 2")],
                width: { size: COL2, type: WidthType.DXA },
                borders: cellBorders,
                margins: cellMargins
              })
            ]
          })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('output.docx', buffer);
});
```

## Column Width Cheat Sheet

For **US Letter with 1" margins = 9360 DXA**:

| Layout | Column Widths |
|--------|--------------|
| 2 cols (20/80) | `[1872, 7488]` |
| 2 cols (25/75) | `[2340, 7020]` |
| 2 cols (equal) | `[4680, 4680]` |
| 3 cols (equal) | `[3120, 3120, 3120]` |
| 3 cols (25/25/50) | `[2340, 2340, 4680]` |

## Troubleshooting

**Tables narrow in Google Docs?**
- Use `WidthType.DXA`, not PERCENTAGE
- Add `width` to EVERY TableCell

**Cell backgrounds black?**
- Use `ShadingType.CLEAR`, not SOLID

**Text touching borders?**
- Add `margins: { top: 80, bottom: 80, left: 120, right: 120 }`

**Columns uneven?**
- Verify column widths sum to exactly 9360

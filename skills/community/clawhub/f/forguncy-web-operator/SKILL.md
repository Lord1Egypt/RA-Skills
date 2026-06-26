---
name: forguncy-web-operator
description: Provides functionality to interact with SpreadJS tables in the web applications built by Forguncy (aka 活字格), specifically for extracting table data and column headers. Use this skill when you need to programmatically read content from tables within a Forguncy web page by dynamically identifying the table's "fgcname" attribute.
---

# Forguncy Web Operations (forguncy-web-operator)

This skill allows you to extract data and headers from SpreadJS tables within the web applications built by Forguncy (aka 活字格).

## How to use

The following JavaScript snippets can be executed in the browser context using the `browser.act` tool with `kind: "evaluate"` to retrieve data from a SpreadJS table.

### Dynamically Get Table Name (fgcname)

First, you need to identify the `fgcname` of the SpreadJS table. You can find this by inspecting the DOM or using a JavaScript snippet like this to find elements with `fgc-uielement="listview"` and extract their `fgcname`:

```javascript
(function() {
    const listViews = document.querySelectorAll('[fgc-uielement="listview"]');
    let fgcNames = [];
    listViews.forEach(lv => {
        if (lv.hasAttribute('fgcname')) {
            fgcNames.push(lv.getAttribute('fgcname'));
        }
    });
    return fgcNames;
})()
```
Once you have the `fgcname` (e.g., "表格1"), you can use it in the following functions.

### Get Table Data

To get the full table data in CSV format (rows separated by '\\r', columns by ','), replace `YOUR_TABLE_FGCNAME` with the actual `fgcname` you found:

```javascript
(function() {
    const tableName = "YOUR_TABLE_FGCNAME"; // Replace with the actual fgcname, e.g., "表格1"
    var sheet = Forguncy.Page.getListView(tableName).getControl().getActiveSheet();
    return sheet.getCsv(0,0,sheet.getRowCount(), sheet.getColumnCount(),"\r",",");
})()
```

### Get Column Headers

To get the column headers, assuming there are 2 header rows (adjust `headerRowCount` if necessary), replace `YOUR_TABLE_FGCNAME` with the actual `fgcname`:

```javascript
(function() {
    const tableName = "YOUR_TABLE_FGCNAME"; // Replace with the actual fgcname, e.g., "表格1"
    var sheet = Forguncy.Page.getListView(tableName).getControl().getActiveSheet();
    var headerRowCount = sheet.getRowCount(GC.Spread.Sheets.SheetArea.colHeader); 
    var headers = [];
    for (let r = 0; r < headerRowCount; r++) {
        var rowHeaders = [];
        for (let c = 0; c < sheet.getColumnCount(); c++) {
            rowHeaders.push(sheet.getValue(r, c, GC.Spread.Sheets.SheetArea.colHeader));
        }
        headers.push(rowHeaders);
    }
    return headers;
})()
```

Remember to pass the `targetId` obtained from a `browser.open` or `browser.snapshot` call when executing these scripts.

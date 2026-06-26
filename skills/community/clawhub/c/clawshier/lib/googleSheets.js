const fs = require("fs");
const path = require("path");
const { google } = require("googleapis");

let _sheets = null;

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];
const MM_YY_PATTERN = /^(\d{2})-(\d{2})$/;
const SUMMARY_SHEET = "Summary";
const BREAKDOWN_SHEET = "Invoice Archive Breakdown";
const CATEGORY_SUMMARY_START_COLUMN = 9; // J
const CATEGORY_SUMMARY_START_ROW = 0; // 1-indexed in Sheets UI
const isTestMode = process.env.CLAWSHIER_TEST_MODE === "1";

function getMockDbPath() {
  return process.env.CLAWSHIER_TEST_DB_PATH || path.resolve(__dirname, "../.clawshier-test-db.json");
}

function loadMockDb() {
  const dbPath = getMockDbPath();
  if (!fs.existsSync(dbPath)) return { sheets: {} };
  return JSON.parse(fs.readFileSync(dbPath, "utf8"));
}

function saveMockDb(db) {
  const dbPath = getMockDbPath();
  fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
}

function columnToIndex(column) {
  return String(column)
    .toUpperCase()
    .split("")
    .reduce((acc, char) => acc * 26 + (char.charCodeAt(0) - 64), 0) - 1;
}

function getMockSheet(db, sheetName) {
  return db.sheets[sheetName] || null;
}

function ensureMockSheet(db, sheetName, headers) {
  if (db.sheets[sheetName]) return true;
  db.sheets[sheetName] = { rows: headers && headers.length ? [headers] : [] };
  return false;
}

function getClient() {
  if (_sheets) return _sheets;

  const keyPath = path.resolve(process.env.GOOGLE_SERVICE_ACCOUNT_KEY);
  const auth = new google.auth.GoogleAuth({
    keyFile: keyPath,
    scopes: ["https://www.googleapis.com/auth/spreadsheets"],
  });

  _sheets = google.sheets({ version: "v4", auth });
  return _sheets;
}

function getSheet(meta, sheetName) {
  return meta.data.sheets.find((s) => s.properties.title === sheetName) || null;
}

function getSheetId(meta, sheetName) {
  const sheet = getSheet(meta, sheetName);
  return sheet ? sheet.properties.sheetId : null;
}

function styleHeaderRequests(sheetId) {
  return [
    {
      repeatCell: {
        range: { sheetId, startRowIndex: 0, endRowIndex: 1 },
        cell: {
          userEnteredFormat: {
            textFormat: { bold: true },
            backgroundColor: { red: 0.93, green: 0.93, blue: 0.93 },
          },
        },
        fields: "userEnteredFormat(textFormat,backgroundColor)",
      },
    },
    {
      updateSheetProperties: {
        properties: {
          sheetId,
          gridProperties: { frozenRowCount: 1 },
        },
        fields: "gridProperties.frozenRowCount",
      },
    },
  ];
}

function numberFormatRequests(sheetId, columnIndices) {
  return columnIndices.map((col) => ({
    repeatCell: {
      range: {
        sheetId,
        startRowIndex: 1,
        endRowIndex: 1000,
        startColumnIndex: col,
        endColumnIndex: col + 1,
      },
      cell: {
        userEnteredFormat: {
          numberFormat: { type: "NUMBER", pattern: "#,##0.00" },
        },
      },
      fields: "userEnteredFormat.numberFormat",
    },
  }));
}

async function ensureSheet(spreadsheetId, sheetName, headers, numberColumns) {
  if (isTestMode) {
    const db = loadMockDb();
    const existed = ensureMockSheet(db, sheetName, headers);
    saveMockDb(db);
    return existed;
  }

  const sheets = getClient();
  const meta = await sheets.spreadsheets.get({ spreadsheetId });
  const existing = meta.data.sheets.find(
    (s) => s.properties.title === sheetName
  );

  if (existing) return true;

  const addRes = await sheets.spreadsheets.batchUpdate({
    spreadsheetId,
    requestBody: {
      requests: [{ addSheet: { properties: { title: sheetName } } }],
    },
  });

  const newSheetId = addRes.data.replies[0].addSheet.properties.sheetId;

  if (headers && headers.length) {
    await sheets.spreadsheets.values.update({
      spreadsheetId,
      range: `'${sheetName}'!A1`,
      valueInputOption: "RAW",
      requestBody: { values: [headers] },
    });

    const formatRequests = [
      ...styleHeaderRequests(newSheetId),
      ...(numberColumns ? numberFormatRequests(newSheetId, numberColumns) : []),
    ];

    await sheets.spreadsheets.batchUpdate({
      spreadsheetId,
      requestBody: { requests: formatRequests },
    });
  }

  return false;
}

async function sheetExists(spreadsheetId, sheetName) {
  if (isTestMode) {
    const db = loadMockDb();
    return Boolean(getMockSheet(db, sheetName));
  }

  const sheets = getClient();
  const meta = await sheets.spreadsheets.get({ spreadsheetId });
  return meta.data.sheets.some((s) => s.properties.title === sheetName);
}

async function deleteSheetIfExists(spreadsheetId, sheetName) {
  if (isTestMode) {
    const db = loadMockDb();
    if (!db.sheets[sheetName]) return false;
    delete db.sheets[sheetName];
    saveMockDb(db);
    return true;
  }

  const sheets = getClient();
  const meta = await sheets.spreadsheets.get({ spreadsheetId });
  const sheetId = getSheetId(meta, sheetName);
  if (sheetId === null) return false;

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId,
    requestBody: {
      requests: [{ deleteSheet: { sheetId } }],
    },
  });
  return true;
}

async function appendRow(spreadsheetId, sheetName, row) {
  if (isTestMode) {
    const db = loadMockDb();
    ensureMockSheet(db, sheetName, []);
    db.sheets[sheetName].rows.push(row);
    saveMockDb(db);
    return db.sheets[sheetName].rows.length;
  }

  const sheets = getClient();
  const res = await sheets.spreadsheets.values.append({
    spreadsheetId,
    range: `'${sheetName}'!A:Z`,
    valueInputOption: "USER_ENTERED",
    insertDataOption: "INSERT_ROWS",
    requestBody: { values: [row] },
  });

  const updatedRange = res.data.updates?.updatedRange || "";
  const match = updatedRange.match(/(\d+)$/);
  return match ? parseInt(match[1], 10) : null;
}

async function appendRows(spreadsheetId, sheetName, rows) {
  if (!rows.length) return null;

  if (isTestMode) {
    const db = loadMockDb();
    ensureMockSheet(db, sheetName, []);
    db.sheets[sheetName].rows.push(...rows);
    saveMockDb(db);
    return db.sheets[sheetName].rows.length;
  }

  const sheets = getClient();
  const res = await sheets.spreadsheets.values.append({
    spreadsheetId,
    range: `'${sheetName}'!A:Z`,
    valueInputOption: "USER_ENTERED",
    insertDataOption: "INSERT_ROWS",
    requestBody: { values: rows },
  });

  const updatedRange = res.data.updates?.updatedRange || "";
  const match = updatedRange.match(/(\d+)$/);
  return match ? parseInt(match[1], 10) : null;
}

async function getColumn(spreadsheetId, sheetName, column) {
  if (isTestMode) {
    const db = loadMockDb();
    const sheet = getMockSheet(db, sheetName);
    if (!sheet) return [];
    const index = columnToIndex(column);
    return sheet.rows.map((row) => row[index] ?? "");
  }

  const sheets = getClient();
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range: `'${sheetName}'!${column}:${column}`,
  });
  return (res.data.values || []).flat();
}

function previousFullMonth(today = new Date()) {
  const year = today.getFullYear();
  const month = today.getMonth();
  if (month === 0) return { year: year - 1, month: 12 };
  return { year, month: month };
}

function sheetNameFromYearMonth(year, month) {
  const yy = String(year).slice(-2);
  const mm = String(month).padStart(2, "0");
  return `${mm}-${yy}`;
}

function labelFromYearMonth(year, month) {
  return `${MONTH_NAMES[month - 1]} ${year}`;
}

function buildCategorySummaryRows(rows, currency) {
  const totals = new Map();

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i] || [];
    const category = String(row[3] || "Uncategorized").trim() || "Uncategorized";
    const amount = parseFloat(row[6]) || 0;
    const rowCurrency = String(row[7] || "USD").toUpperCase().trim();
    if (rowCurrency !== currency) continue;
    totals.set(category, Math.round(((totals.get(category) || 0) + amount) * 100) / 100);
  }

  return [...totals.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([category, total]) => [category, total]);
}

async function getSheetRows(spreadsheetId, sheetName) {
  if (isTestMode) {
    const db = loadMockDb();
    return getMockSheet(db, sheetName)?.rows || [];
  }

  const sheets = getClient();
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range: `'${sheetName}'!A:Z`,
  });
  return res.data.values || [];
}

async function reorderSheets(spreadsheetId) {
  if (isTestMode) return;

  const sheets = getClient();
  const meta = await sheets.spreadsheets.get({ spreadsheetId });
  const monthlySheets = meta.data.sheets
    .map((s) => s.properties.title)
    .filter((name) => MM_YY_PATTERN.test(name))
    .sort((a, b) => {
      const [, mmA, yyA] = a.match(MM_YY_PATTERN);
      const [, mmB, yyB] = b.match(MM_YY_PATTERN);
      const yearA = 2000 + parseInt(yyA, 10);
      const yearB = 2000 + parseInt(yyB, 10);
      const monthA = parseInt(mmA, 10);
      const monthB = parseInt(mmB, 10);
      return yearB - yearA || monthB - monthA;
    });

  const desiredOrder = [SUMMARY_SHEET, BREAKDOWN_SHEET, ...monthlySheets];
  const requests = [];

  desiredOrder.forEach((sheetName, index) => {
    const sheet = getSheet(meta, sheetName);
    if (!sheet) return;
    if (sheet.properties.index === index) return;
    requests.push({
      updateSheetProperties: {
        properties: { sheetId: sheet.properties.sheetId, index },
        fields: "index",
      },
    });
  });

  if (requests.length) {
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId,
      requestBody: { requests },
    });
  }
}

async function updateSummary(spreadsheetId) {
  if (isTestMode) {
    const db = loadMockDb();
    const monthlyTabs = Object.keys(db.sheets)
      .filter((name) => MM_YY_PATTERN.test(name));

    const allCurrencies = new Set();
    const monthlyData = [];

    for (const tab of monthlyTabs) {
      const [, mm, yy] = tab.match(MM_YY_PATTERN);
      const month = parseInt(mm, 10);
      const year = 2000 + parseInt(yy, 10);
      const rows = db.sheets[tab].rows || [];
      const sums = {};

      for (let i = 1; i < rows.length; i++) {
        const amount = parseFloat(rows[i][6]) || 0;
        const currency = String(rows[i][7] || "USD").toUpperCase().trim();
        allCurrencies.add(currency);
        sums[currency] = Math.round(((sums[currency] || 0) + amount) * 100) / 100;
      }

      monthlyData.push({
        label: `${MONTH_NAMES[month - 1]} ${year}`,
        sums,
        year,
        month,
      });
    }

    monthlyData.sort((a, b) => a.year - b.year || a.month - b.month);
    const sortedCurrencies = [...allCurrencies].sort();
    const rows = [
      ["Month", ...sortedCurrencies],
      ...monthlyData.map((entry) => [
        entry.label,
        ...sortedCurrencies.map((currency) => entry.sums[currency] || 0),
      ]),
    ];

    db.sheets[SUMMARY_SHEET] = { rows };
    saveMockDb(db);
    return;
  }

  const sheets = getClient();
  const meta = await sheets.spreadsheets.get({ spreadsheetId });

  const monthlyTabs = meta.data.sheets
    .map((s) => s.properties.title)
    .filter((name) => MM_YY_PATTERN.test(name));

  const allCurrencies = new Set();
  const monthlyData = [];

  for (const tab of monthlyTabs) {
    const [, mm, yy] = tab.match(MM_YY_PATTERN);
    const month = parseInt(mm, 10);
    const year = 2000 + parseInt(yy, 10);

    const totals = await getColumn(spreadsheetId, tab, "G");
    const currencies = await getColumn(spreadsheetId, tab, "H");

    const sums = {};
    for (let i = 1; i < totals.length; i++) {
      const currency = (currencies[i] || "USD").toUpperCase().trim();
      const amount = parseFloat(totals[i]) || 0;
      allCurrencies.add(currency);
      sums[currency] = (sums[currency] || 0) + amount;
    }

    Object.keys(sums).forEach((c) => {
      sums[c] = Math.round(sums[c] * 100) / 100;
    });

    const label = `${MONTH_NAMES[month - 1]} ${year}`;
    monthlyData.push({ label, sums, year, month });
  }

  monthlyData.sort((a, b) => a.year - b.year || a.month - b.month);

  const sortedCurrencies = [...allCurrencies].sort();
  const headerRow = ["Month", ...sortedCurrencies];

  let summarySheetId = getSheetId(meta, SUMMARY_SHEET);

  if (summarySheetId === null) {
    const addRes = await sheets.spreadsheets.batchUpdate({
      spreadsheetId,
      requestBody: {
        requests: [{ addSheet: { properties: { title: SUMMARY_SHEET } } }],
      },
    });
    summarySheetId = addRes.data.replies[0].addSheet.properties.sheetId;
  } else {
    const existingCharts = meta.data.sheets
      .find((s) => s.properties.sheetId === summarySheetId)
      ?.charts || [];

    const deleteChartRequests = existingCharts.map((c) => ({
      deleteEmbeddedObject: { objectId: c.chartId },
    }));

    const clearRequests = [
      {
        updateCells: {
          range: { sheetId: summarySheetId },
          fields: "userEnteredValue,userEnteredFormat",
        },
      },
      ...deleteChartRequests,
    ];

    await sheets.spreadsheets.batchUpdate({
      spreadsheetId,
      requestBody: { requests: clearRequests },
    });
  }

  const dataRows = monthlyData.map((m) => [
    m.label,
    ...sortedCurrencies.map((c) => m.sums[c] || 0),
  ]);
  const rows = [headerRow, ...dataRows];

  const targetMonth = previousFullMonth(new Date());
  const targetTab = sheetNameFromYearMonth(targetMonth.year, targetMonth.month);
  const targetLabel = labelFromYearMonth(targetMonth.year, targetMonth.month);
  const targetRows = monthlyTabs.includes(targetTab)
    ? await getSheetRows(spreadsheetId, targetTab)
    : [];
  const targetCurrencies = [...new Set(
    targetRows.slice(1).map((row) => String(row[7] || "USD").toUpperCase().trim()).filter(Boolean)
  )].sort();

  const categoryBlocks = [];
  let blockStartColumn = CATEGORY_SUMMARY_START_COLUMN;

  for (const currency of targetCurrencies) {
    const categoryRows = buildCategorySummaryRows(targetRows, currency);
    if (!categoryRows.length) continue;

    const blockValues = [
      [`Category Breakdown — ${targetLabel} (${currency})`, ""],
      ["Category", "Total"],
      ...categoryRows,
    ];

    categoryBlocks.push({
      currency,
      title: `Category Breakdown — ${targetLabel} (${currency})`,
      values: blockValues,
      startColumn: blockStartColumn,
      rowCount: blockValues.length,
    });

    blockStartColumn += 4;
  }

  const valueUpdates = [{
    range: `'${SUMMARY_SHEET}'!A1`,
    values: rows,
  }];

  for (const block of categoryBlocks) {
    const startColLetter = String.fromCharCode(65 + block.startColumn);
    valueUpdates.push({
      range: `'${SUMMARY_SHEET}'!${startColLetter}1`,
      values: block.values,
    });
  }

  await sheets.spreadsheets.values.batchUpdate({
    spreadsheetId,
    requestBody: {
      valueInputOption: "USER_ENTERED",
      data: valueUpdates,
    },
  });

  const dataRowCount = monthlyData.length;
  const currencyColIndices = sortedCurrencies.map((_, i) => i + 1);

  const formatRequests = [
    ...styleHeaderRequests(summarySheetId),
    ...numberFormatRequests(summarySheetId, currencyColIndices),
    {
      updateSheetProperties: {
        properties: { sheetId: summarySheetId, index: 0 },
        fields: "index",
      },
    },
  ];

  for (const block of categoryBlocks) {
    formatRequests.push({
      repeatCell: {
        range: {
          sheetId: summarySheetId,
          startRowIndex: CATEGORY_SUMMARY_START_ROW,
          endRowIndex: CATEGORY_SUMMARY_START_ROW + 1,
          startColumnIndex: block.startColumn,
          endColumnIndex: block.startColumn + 2,
        },
        cell: {
          userEnteredFormat: {
            textFormat: { bold: true },
            backgroundColor: { red: 0.85, green: 0.92, blue: 0.98 },
          },
        },
        fields: "userEnteredFormat(textFormat,backgroundColor)",
      },
    });

    formatRequests.push({
      repeatCell: {
        range: {
          sheetId: summarySheetId,
          startRowIndex: CATEGORY_SUMMARY_START_ROW + 1,
          endRowIndex: CATEGORY_SUMMARY_START_ROW + 2,
          startColumnIndex: block.startColumn,
          endColumnIndex: block.startColumn + 2,
        },
        cell: {
          userEnteredFormat: {
            textFormat: { bold: true },
            backgroundColor: { red: 0.93, green: 0.93, blue: 0.93 },
          },
        },
        fields: "userEnteredFormat(textFormat,backgroundColor)",
      },
    });

    formatRequests.push(...numberFormatRequests(summarySheetId, [block.startColumn + 1]));
  }

  if (dataRowCount > 0 && sortedCurrencies.length > 0) {
    const series = sortedCurrencies.map((_, i) => ({
      series: {
        sourceRange: {
          sources: [{
            sheetId: summarySheetId,
            startRowIndex: 0,
            endRowIndex: dataRowCount + 1,
            startColumnIndex: i + 1,
            endColumnIndex: i + 2,
          }],
        },
      },
      targetAxis: "LEFT_AXIS",
    }));

    formatRequests.push({
      addChart: {
        chart: {
          position: {
            overlayPosition: {
              anchorCell: {
                sheetId: summarySheetId,
                rowIndex: 1,
                columnIndex: sortedCurrencies.length + 2,
              },
              widthPixels: 800,
              heightPixels: 400,
            },
          },
          spec: {
            title: "Monthly Expenses by Currency Over Time",
            basicChart: {
              chartType: "LINE",
              legendPosition: "BOTTOM_LEGEND",
              axis: [
                { position: "BOTTOM_AXIS", title: "Month" },
                { position: "LEFT_AXIS", title: "Amount" },
              ],
              domains: [
                {
                  domain: {
                    sourceRange: {
                      sources: [{
                        sheetId: summarySheetId,
                        startRowIndex: 0,
                        endRowIndex: dataRowCount + 1,
                        startColumnIndex: 0,
                        endColumnIndex: 1,
                      }],
                    },
                  },
                },
              ],
              series,
              headerCount: 1,
            },
          },
        },
      },
    });
  }

  for (let i = 0; i < categoryBlocks.length; i++) {
    const block = categoryBlocks[i];
    formatRequests.push({
      addChart: {
        chart: {
          position: {
            overlayPosition: {
              anchorCell: {
                sheetId: summarySheetId,
                rowIndex: 22 + (i * 20),
                columnIndex: sortedCurrencies.length + 2,
              },
              widthPixels: 500,
              heightPixels: 320,
            },
          },
          spec: {
            title: block.title,
            pieChart: {
              legendPosition: "RIGHT_LEGEND",
              domain: {
                sourceRange: {
                  sources: [{
                    sheetId: summarySheetId,
                    startRowIndex: CATEGORY_SUMMARY_START_ROW + 2,
                    endRowIndex: CATEGORY_SUMMARY_START_ROW + block.rowCount,
                    startColumnIndex: block.startColumn,
                    endColumnIndex: block.startColumn + 1,
                  }],
                },
              },
              series: {
                sourceRange: {
                  sources: [{
                    sheetId: summarySheetId,
                    startRowIndex: CATEGORY_SUMMARY_START_ROW + 2,
                    endRowIndex: CATEGORY_SUMMARY_START_ROW + block.rowCount,
                    startColumnIndex: block.startColumn + 1,
                    endColumnIndex: block.startColumn + 2,
                  }],
                },
              },
            },
          },
        },
      },
    });
  }

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId,
    requestBody: { requests: formatRequests },
  });

  await reorderSheets(spreadsheetId);
}

module.exports = {
  ensureSheet,
  sheetExists,
  deleteSheetIfExists,
  appendRow,
  appendRows,
  getColumn,
  updateSummary,
};

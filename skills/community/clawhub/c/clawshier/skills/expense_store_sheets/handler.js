#!/usr/bin/env node
require("dotenv").config({ path: require("path").resolve(__dirname, "../../.env") });

const {
  ensureSheet, deleteSheetIfExists, appendRow, appendRows, updateSummary,
} = require("../../lib/googleSheets");
const { sheetNameFromDate } = require("../../lib/expenseValidator");
const { isTraceEnabled, readTrace, writeTrace, startTraceStep, finishTraceStep } = require("../../lib/trace");
const { readJsonInput, writeJsonOutput } = require("../../lib/io");

const EXPENSE_HEADERS = [
  "Fingerprint", "Date", "Vendor", "Category",
  "Subtotal", "Tax", "Total", "Currency",
];
const BREAKDOWN_SHEET = "Invoice Archive Breakdown";
const BREAKDOWN_HEADERS = ["Fingerprint", "Item", "Quantity", "Cost"];

async function processExpenseStore(expense) {
  const traceEnabled = isTraceEnabled();
  const trace = traceEnabled ? (readTrace() || { steps: [] }) : null;
  const traceStep = traceEnabled ? startTraceStep("store", { kind: "google-sheets" }) : null;

  if (!expense.fingerprint) {
    throw new Error(
      "Missing fingerprint — ensure the expense passed through the validator (step 3) before storing"
    );
  }

  const spreadsheetId = process.env.GOOGLE_SHEETS_ID;
  const sheetName = sheetNameFromDate(expense.date);

  await ensureSheet(spreadsheetId, sheetName, EXPENSE_HEADERS, [4, 5, 6]);

  const row = [
    expense.fingerprint,
    expense.date,
    expense.vendor,
    expense.category,
    expense.subtotal,
    expense.tax,
    expense.total,
    expense.currency,
  ];

  const rowNumber = await appendRow(spreadsheetId, sheetName, row);

  await ensureSheet(spreadsheetId, BREAKDOWN_SHEET, BREAKDOWN_HEADERS, [3]);

  const itemRows = (expense.items || []).map((item) => [
    expense.fingerprint,
    item.description,
    item.quantity || 1,
    item.amount,
  ]);

  await appendRows(spreadsheetId, BREAKDOWN_SHEET, itemRows);

  await deleteSheetIfExists(spreadsheetId, "Sheet1");
  await updateSummary(spreadsheetId);

  if (traceEnabled) {
    trace.steps.push(finishTraceStep(traceStep, {
      status: "ok",
      targetSheet: sheetName,
      row: rowNumber,
      breakdownRows: itemRows.length,
    }));
    writeTrace(trace);
  }

  return { success: true, row: rowNumber };
}

async function main() {
  writeJsonOutput(await processExpenseStore(await readJsonInput()));
}

if (require.main === module) {
  main().catch((err) => {
    process.stderr.write(JSON.stringify({ error: err.message }));
    process.exit(1);
  });
}

module.exports = {
  processExpenseStore,
};

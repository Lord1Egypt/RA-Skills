const path = require("path");
const {
  getImagePath,
  processReceiptOcr,
} = require("../skills/receipt_ocr/handler");
const {
  processExpenseStructure,
} = require("../skills/expense_structurer/handler");
const {
  processExpenseValidation,
} = require("../skills/expense_validator/handler");
const {
  processExpenseStore,
} = require("../skills/expense_store_sheets/handler");

async function runPipeline({ imagePath, date } = {}) {
  if (!imagePath) {
    throw new Error("Usage: runPipeline({ imagePath, date? }) requires imagePath");
  }

  const step1 = await processReceiptOcr({ imagePath });
  const step2 = await processExpenseStructure(step1);
  const step3 = await processExpenseValidation(step2, { argv: date ? ["node", "handler", "--date", date] : ["node", "handler"] });
  const step4 = await processExpenseStore(step3);
  return step4;
}

module.exports = {
  runPipeline,
};

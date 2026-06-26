const { createWorker } = require("tesseract.js");

let sharedWorker = null;
let sharedWorkerInit = null;

function cleanOcrOutput(value) {
  return String(value || "")
    .replace(/\s+/g, "")
    .replace(/[^a-zA-Z0-9+\-*/xX=]/g, "");
}

function normalizeCommonConfusions(text, mode = "alnum") {
  const input = cleanOcrOutput(text);
  if (!input) {
    return input;
  }

  if (mode === "numeric") {
    return input
      .replace(/[oO]/g, "0")
      .replace(/[iIl]/g, "1")
      .replace(/[sS]/g, "5")
      .replace(/[bB]/g, "8")
      .replace(/[zZ]/g, "2");
  }

  return input
    .replace(/0/g, "O")
    .replace(/1/g, "I")
    .replace(/5/g, "S");
}

function detectArithmeticExpression(text) {
  const normalized = cleanOcrOutput(text).toUpperCase().replace(/=/g, "");
  const expression = normalized.match(/^(\d{1,3})([+\-*/X])(\d{1,3})$/);
  if (!expression) {
    return null;
  }
  return {
    left: Number(expression[1]),
    operator: expression[2],
    right: Number(expression[3])
  };
}

function evaluateArithmeticExpression(expression) {
  if (!expression) {
    return null;
  }
  const { left, right } = expression;
  switch (expression.operator) {
    case "+":
      return String(left + right);
    case "-":
      return String(left - right);
    case "*":
    case "X":
      return String(left * right);
    case "/":
      if (right === 0) {
        return null;
      }
      if (left % right !== 0) {
        return String(left / right);
      }
      return String(left / right);
    default:
      return null;
  }
}

async function getWorker(language = "eng") {
  if (sharedWorker) {
    return sharedWorker;
  }
  if (!sharedWorkerInit) {
    sharedWorkerInit = (async () => {
      const worker = await createWorker(language, 1, {
        logger: () => {}
      });
      await worker.setParameters({
        tessedit_char_whitelist: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/Xx=",
        user_defined_dpi: "300",
        preserve_interword_spaces: "0"
      });
      sharedWorker = worker;
      return worker;
    })();
  }
  return sharedWorkerInit;
}

async function runOcrPass(worker, imageBuffer, psm) {
  await worker.setParameters({
    tessedit_pageseg_mode: String(psm)
  });
  const output = await worker.recognize(imageBuffer);
  const text = cleanOcrOutput(output?.data?.text || "");
  const confidence = Number(output?.data?.confidence || 0);
  return { text, confidence, raw: output?.data?.text || "" };
}

async function recognizeCaptcha(imageBuffer, options = {}) {
  const worker = await getWorker(options.language || "eng");
  const passes = Array.isArray(options.psmModes) && options.psmModes.length > 0 ? options.psmModes : [7, 8, 6];
  const results = [];

  for (const psm of passes) {
    results.push(await runOcrPass(worker, imageBuffer, psm));
  }

  results.sort((a, b) => b.confidence - a.confidence);
  const best = results[0] || { text: "", confidence: 0, raw: "" };
  const arithmetic = detectArithmeticExpression(best.text);

  return {
    text: best.text,
    confidence: best.confidence,
    arithmetic,
    results
  };
}

module.exports = {
  cleanOcrOutput,
  normalizeCommonConfusions,
  detectArithmeticExpression,
  evaluateArithmeticExpression,
  recognizeCaptcha
};

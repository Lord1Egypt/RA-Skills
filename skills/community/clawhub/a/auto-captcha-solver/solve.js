const { CaptchaCache } = require("./cache");
const { generatePreprocessVariants, preprocessCaptcha, validateImageBuffer } = require("./preprocess");
const {
  detectArithmeticExpression,
  evaluateArithmeticExpression,
  normalizeCommonConfusions,
  recognizeCaptcha
} = require("./ocr");

const defaultCache = new CaptchaCache();
const UNSUPPORTED_MARKERS = [/recaptcha/i, /hcaptcha/i, /slider/i, /click.*object/i];

function classifyCaptcha(resultText, arithmeticExpression) {
  if (arithmeticExpression) {
    return "arithmetic";
  }
  if (/^\d{4,6}$/.test(resultText)) {
    return "numeric";
  }
  if (/^[A-Za-z0-9]{4,6}$/.test(resultText)) {
    return "alphanumeric";
  }
  return "unknown";
}

function sanitizeResult(text, minLength = 1, maxLength = 6, caseMode = "preserve") {
  const base = String(text || "").replace(/[^A-Za-z0-9]/g, "");
  const cleaned = caseMode === "upper" ? base.toUpperCase() : caseMode === "lower" ? base.toLowerCase() : base;
  if (cleaned.length < minLength || cleaned.length > maxLength) {
    return null;
  }
  return cleaned;
}

function scoreCandidate(text, confidence, options = {}) {
  const minLength = options.minLength || 4;
  const maxLength = options.maxLength || 6;
  const cleaned = String(text || "").replace(/[^A-Za-z0-9+\-*/=]/g, "");

  if (!cleaned) {
    return -9999;
  }

  let score = Number(confidence) || 0;
  const arithmetic = detectArithmeticExpression(cleaned);
  if (arithmetic) {
    score += 25;
  }

  const alnum = cleaned.replace(/[^A-Za-z0-9]/g, "");
  if (alnum.length >= minLength && alnum.length <= maxLength) {
    score += 20;
  } else {
    score -= Math.abs(alnum.length - Math.min(Math.max(alnum.length, minLength), maxLength)) * 6;
  }

  if (!/^[A-Za-z0-9+\-*/=]+$/.test(cleaned)) {
    score -= 10;
  }

  return score;
}

function hasUnsupportedCaptchaSignals(hints) {
  if (!hints) {
    return false;
  }
  const value = Array.isArray(hints) ? hints.join(" ") : String(hints);
  return UNSUPPORTED_MARKERS.some((pattern) => pattern.test(value));
}

async function solveCaptchaImage(imageBuffer, options = {}) {
  await validateImageBuffer(imageBuffer);

  if (hasUnsupportedCaptchaSignals(options.hints)) {
    return {
      solved: false,
      reason: "Unsupported captcha type detected"
    };
  }

  const caseMode = options.caseMode || "preserve";
  const cache = options.cache || defaultCache;
  const hash = CaptchaCache.sha1(imageBuffer);
  const verified = typeof cache.getVerified === "function" ? cache.getVerified(hash) : null;
  if (verified) {
    return {
      ...verified,
      fromCache: true
    };
  }

  const cached = cache.get(hash);
  if (cached) {
    return {
      ...cached,
      fromCache: true
    };
  }

  const multiPassEnabled = options.multiPass !== false;
  const variants = multiPassEnabled
    ? await generatePreprocessVariants(imageBuffer, options.preprocessing || {})
    : [{ name: "single", buffer: await preprocessCaptcha(imageBuffer, options.preprocessing || {}) }];
  const preprocessed = variants[0]?.buffer || (await preprocessCaptcha(imageBuffer, options.preprocessing || {}));

  const allCandidates = [];
  for (const variant of variants) {
    const ocr = await recognizeCaptcha(variant.buffer, options.ocr || {});
    for (const pass of ocr.results) {
      const baseText = pass.text;
      const numericFixed = normalizeCommonConfusions(baseText, "numeric");
      const alphaFixed = normalizeCommonConfusions(baseText, "alnum");
      const candidates = [baseText, numericFixed, alphaFixed];

      for (const candidateText of candidates) {
        allCandidates.push({
          variant: variant.name,
          text: candidateText,
          confidence: pass.confidence,
          score: scoreCandidate(candidateText, pass.confidence, options)
        });
      }
    }
  }

  allCandidates.sort((a, b) => b.score - a.score);
  const bestCandidate = allCandidates[0] || { text: "", confidence: 0, score: -9999 };

  let answer = null;
  let type = "unknown";
  let confidence = bestCandidate.confidence;

  const arithmetic = detectArithmeticExpression(bestCandidate.text);
  if (arithmetic) {
    answer = evaluateArithmeticExpression(arithmetic);
    type = "arithmetic";
  }

  if (!answer) {
    answer = sanitizeResult(bestCandidate.text, options.minLength || 4, options.maxLength || 6, caseMode);
    type = classifyCaptcha(answer || "", arithmetic);
  }

  if (!answer && typeof options.fallbackVision === "function") {
    // Optional fallback hook for external vision providers.
    const fallback = await options.fallbackVision({
      imageBuffer,
      preprocessedBuffer: preprocessed,
      candidates: allCandidates.slice(0, 5)
    });
    answer = sanitizeResult(fallback?.text || fallback, 1, options.maxLength || 6, caseMode);
    if (typeof fallback?.confidence === "number") {
      confidence = fallback.confidence;
    }
    if (answer) {
      type = fallback?.type || "fallback-vision";
    }
  }

  const result = {
    solved: Boolean(answer),
    value: answer,
    type,
    confidence: Number(confidence.toFixed(2)),
    hash
  };

  if (options.debug) {
    result.debug = {
      topCandidates: allCandidates.slice(0, 5)
    };
  }

  if (result.solved) {
    cache.set(hash, result);
  }

  return result;
}

async function calibrateCaptcha(imageBuffer, answer, options = {}) {
  await validateImageBuffer(imageBuffer);
  const caseMode = options.caseMode || "preserve";
  const normalized = sanitizeResult(String(answer || ""), 1, 12, caseMode);
  if (!normalized) {
    throw new Error("Calibration answer must contain alphanumeric characters");
  }
  const cache = options.cache || defaultCache;
  const hash = CaptchaCache.sha1(imageBuffer);
  if (typeof cache.setVerified === "function") {
    cache.setVerified(hash, normalized);
  } else {
    cache.set(hash, {
      solved: true,
      value: normalized,
      type: /^\d+$/.test(normalized) ? "numeric" : "alphanumeric",
      confidence: 100,
      hash,
      verified: true
    });
  }
  return { hash, value: normalized };
}

module.exports = {
  solveCaptchaImage,
  classifyCaptcha,
  calibrateCaptcha
};

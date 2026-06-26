const sharp = require("sharp");

const ALLOWED_FORMATS = new Set(["jpeg", "jpg", "png", "webp", "gif", "bmp", "tiff"]);
const MAX_IMAGE_BYTES = 2 * 1024 * 1024;
const MAX_PIXELS = 4_000_000;

async function validateImageBuffer(inputBuffer) {
  if (!Buffer.isBuffer(inputBuffer)) {
    throw new TypeError("Captcha image must be a Buffer");
  }
  if (inputBuffer.length === 0 || inputBuffer.length > MAX_IMAGE_BYTES) {
    throw new Error(`Captcha image size must be between 1B and ${MAX_IMAGE_BYTES}B`);
  }

  const image = sharp(inputBuffer, { failOnError: true, limitInputPixels: MAX_PIXELS });
  const metadata = await image.metadata();

  const format = (metadata.format || "").toLowerCase();
  if (!ALLOWED_FORMATS.has(format)) {
    throw new Error(`Unsupported captcha image format: ${format || "unknown"}`);
  }

  if (!metadata.width || !metadata.height) {
    throw new Error("Captcha image has invalid dimensions");
  }

  return metadata;
}

async function preprocessCaptcha(inputBuffer, options = {}) {
  const metadata = await validateImageBuffer(inputBuffer);

  const targetWidth = Math.min(Math.max(metadata.width * 2, 120), options.maxWidth || 400);
  const targetHeight = Math.min(Math.max(metadata.height * 2, 50), options.maxHeight || 180);

  // Keep the pipeline simple and deterministic for low latency on CPU-only environments.
  return sharp(inputBuffer, { failOnError: true, limitInputPixels: MAX_PIXELS })
    .grayscale()
    .normalise()
    .resize(targetWidth, targetHeight, {
      fit: "fill",
      kernel: sharp.kernel.lanczos3
    })
    .median(1)
    .sharpen({ sigma: 1.2, m1: 1, m2: 2, x1: 3, y2: 10, y3: 20 })
    .threshold(options.threshold || 155, { grayscale: true })
    .toFormat("png")
    .toBuffer();
}

async function generatePreprocessVariants(inputBuffer, options = {}) {
  const metadata = await validateImageBuffer(inputBuffer);
  const width = Math.min(Math.max(metadata.width * 2, 120), options.maxWidth || 420);
  const height = Math.min(Math.max(metadata.height * 2, 50), options.maxHeight || 200);

  const thresholds = Array.isArray(options.thresholds) && options.thresholds.length > 0
    ? options.thresholds
    : [145, 160, 175];

  const variants = [];
  variants.push({
    name: "base-normalized",
    buffer: await sharp(inputBuffer, { failOnError: true, limitInputPixels: MAX_PIXELS })
      .grayscale()
      .normalise()
      .resize(width, height, { fit: "fill", kernel: sharp.kernel.lanczos3 })
      .median(1)
      .sharpen({ sigma: 1.2, m1: 1, m2: 2, x1: 3, y2: 10, y3: 20 })
      .toFormat("png")
      .toBuffer()
  });

  for (const threshold of thresholds) {
    variants.push({
      name: `binary-${threshold}`,
      buffer: await sharp(inputBuffer, { failOnError: true, limitInputPixels: MAX_PIXELS })
        .grayscale()
        .normalise()
        .resize(width, height, { fit: "fill", kernel: sharp.kernel.lanczos3 })
        .median(1)
        .sharpen({ sigma: 1.2, m1: 1, m2: 2, x1: 3, y2: 10, y3: 20 })
        .threshold(threshold, { grayscale: true })
        .toFormat("png")
        .toBuffer()
    });
  }

  // Inverted variant often helps with light text on dark backgrounds.
  variants.push({
    name: "inverted-binary",
    buffer: await sharp(inputBuffer, { failOnError: true, limitInputPixels: MAX_PIXELS })
      .grayscale()
      .normalise()
      .resize(width, height, { fit: "fill", kernel: sharp.kernel.lanczos3 })
      .negate()
      .median(1)
      .threshold(150, { grayscale: true })
      .toFormat("png")
      .toBuffer()
  });

  return variants;
}

module.exports = {
  preprocessCaptcha,
  generatePreprocessVariants,
  validateImageBuffer,
  MAX_IMAGE_BYTES
};

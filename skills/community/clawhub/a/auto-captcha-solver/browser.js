const { By, Key } = (() => {
  try {
    return require("selenium-webdriver");
  } catch {
    return { By: null, Key: null };
  }
})();
const { solveCaptchaImage } = require("./solve");

const UNSUPPORTED_SELECTORS = [
  'iframe[src*="recaptcha"]',
  ".g-recaptcha",
  '[class*="hcaptcha"]',
  '[id*="hcaptcha"]'
];

const DEFAULT_IMAGE_SELECTORS = [
  'img[alt*="captcha" i]',
  'img[src*="captcha" i]',
  "canvas.captcha",
  '[class*="captcha"] img',
  "#captchaImage"
];

const DEFAULT_INPUT_SELECTORS = [
  'input[name*="captcha" i]',
  'input[id*="captcha" i]',
  "input.captcha",
  "#captcha"
];

function isSafeUrl(url) {
  if (!url || typeof url !== "string") {
    return false;
  }
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

async function hasUnsupportedCaptcha(page) {
  for (const selector of UNSUPPORTED_SELECTORS) {
    const found = await page.$(selector);
    if (found) {
      return true;
    }
  }
  return false;
}

async function findFirstElement(page, selectors) {
  for (const selector of selectors) {
    const element = await page.$(selector);
    if (element) {
      return { element, selector };
    }
  }
  return null;
}

async function solveCaptcha(page, options = {}) {
  if (await hasUnsupportedCaptcha(page)) {
    return { solved: false, reason: "Unsupported captcha type detected" };
  }

  const imagePick = await findFirstElement(page, options.imageSelectors || DEFAULT_IMAGE_SELECTORS);
  if (!imagePick) {
    return { solved: false, reason: "Captcha image element not found" };
  }

  const src = await page.evaluate((el) => el.getAttribute("src"), imagePick.element);
  if (src && !isSafeUrl(src) && !src.startsWith("data:image/")) {
    return { solved: false, reason: "Unsafe captcha source URL rejected" };
  }

  const imageBuffer = await imagePick.element.screenshot();
  const result = await solveCaptchaImage(imageBuffer, options.solver || {});
  if (!result.solved) {
    return result;
  }

  const inputPick = await findFirstElement(page, options.inputSelectors || DEFAULT_INPUT_SELECTORS);
  if (!inputPick) {
    return { solved: false, reason: "Captcha input element not found", ...result };
  }

  // Playwright supports fill(); Puppeteer uses click+keyboard typing.
  if (typeof inputPick.element.fill === "function") {
    await inputPick.element.fill(result.value);
  } else {
    await inputPick.element.click({ clickCount: 3 });
    await page.keyboard.type(result.value);
  }

  if (options.autoSubmit !== false) {
    if (options.submitSelector) {
      const submitElement = await page.$(options.submitSelector);
      if (submitElement) {
        await submitElement.click();
      } else {
        await page.keyboard.press("Enter");
      }
    } else {
      await page.keyboard.press("Enter");
    }
  }

  return {
    ...result,
    imageSelector: imagePick.selector,
    inputSelector: inputPick.selector
  };
}

async function solveCaptchaSelenium(driver, options = {}) {
  if (!By || !Key) {
    throw new Error("selenium-webdriver is not installed");
  }

  const imageSelectors = options.imageSelectors || DEFAULT_IMAGE_SELECTORS;
  const inputSelectors = options.inputSelectors || DEFAULT_INPUT_SELECTORS;

  for (const selector of UNSUPPORTED_SELECTORS) {
    const unsupported = await driver.findElements(By.css(selector));
    if (unsupported.length > 0) {
      return { solved: false, reason: "Unsupported captcha type detected" };
    }
  }

  let imageElement = null;
  for (const selector of imageSelectors) {
    const matches = await driver.findElements(By.css(selector));
    if (matches.length > 0) {
      imageElement = matches[0];
      break;
    }
  }
  if (!imageElement) {
    return { solved: false, reason: "Captcha image element not found" };
  }

  const imageBase64 = await imageElement.takeScreenshot(true);
  const imageBuffer = Buffer.from(imageBase64, "base64");
  const result = await solveCaptchaImage(imageBuffer, options.solver || {});
  if (!result.solved) {
    return result;
  }

  let inputElement = null;
  for (const selector of inputSelectors) {
    const matches = await driver.findElements(By.css(selector));
    if (matches.length > 0) {
      inputElement = matches[0];
      break;
    }
  }
  if (!inputElement) {
    return { solved: false, reason: "Captcha input element not found", ...result };
  }

  await inputElement.clear();
  await inputElement.sendKeys(result.value);

  if (options.autoSubmit !== false) {
    if (options.submitSelector) {
      const submit = await driver.findElements(By.css(options.submitSelector));
      if (submit.length > 0) {
        await submit[0].click();
      } else {
        await inputElement.sendKeys(Key.ENTER);
      }
    } else {
      await inputElement.sendKeys(Key.ENTER);
    }
  }

  return result;
}

module.exports = {
  isSafeUrl,
  solveCaptcha,
  solveCaptchaPlaywright: solveCaptcha,
  solveCaptchaPuppeteer: solveCaptcha,
  solveCaptchaSelenium
};

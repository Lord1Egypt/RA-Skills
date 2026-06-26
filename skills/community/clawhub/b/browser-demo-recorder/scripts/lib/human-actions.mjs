let lastMousePosition = { x: 24, y: 24 };

export async function humanMove(page, x, y, steps = 20) {
  await page.mouse.move(x, y, { steps });
  lastMousePosition = { x, y };
}

export async function clickByPoint(page, x, y, options = {}) {
  const { moveSteps = 24, waitBeforeDownMs = 180, holdMs = 80 } = options;
  await humanMove(page, x, y, moveSteps);
  await page.waitForTimeout(waitBeforeDownMs);
  await page.mouse.down();
  await page.waitForTimeout(holdMs);
  await page.mouse.up();
}

export async function humanClick(page, selector, options = {}) {
  const element = await page.waitForSelector(selector, { visible: true });
  const box = await element.boundingBox();
  if (!box) throw new Error(`Element not visible for selector: ${selector}`);
  await clickByPoint(page, box.x + box.width / 2, box.y + box.height / 2, options);
}

export async function clearFocusedInput(page) {
  const modifier = process.platform === 'darwin' ? 'Meta' : 'Control';
  await page.keyboard.down(modifier);
  await page.keyboard.press('KeyA');
  await page.keyboard.up(modifier);
  await page.keyboard.press('Backspace');
}

export async function humanType(page, text, options = {}) {
  const { delay = 120 } = options;
  await page.keyboard.type(text, { delay });
}

export async function smoothScrollTo(page, targetY, options = {}) {
  const {
    stepY = 96,
    stepWaitMs,
    durationMs,
    moveSteps = 10,
    anchorX,
    anchorY,
  } = options;

  const viewport = page.viewport() || { width: 1600, height: 1200 };
  const targetX = anchorX ?? lastMousePosition.x ?? Math.round(viewport.width * 0.75);
  const targetAnchorY = anchorY ?? lastMousePosition.y ?? Math.round(viewport.height * 0.72);

  await humanMove(page, targetX, targetAnchorY, moveSteps);
  await page.waitForTimeout(120);

  const currentY = await page.evaluate(() => window.scrollY);
  const delta = targetY - currentY;
  const direction = delta >= 0 ? 1 : -1;
  let remaining = Math.abs(delta);

  const stepsCount = Math.max(1, Math.ceil(remaining / stepY));
  const resolvedStepWaitMs = stepWaitMs ?? (durationMs ? Math.max(24, Math.round(durationMs / stepsCount)) : 120);

  while (remaining > 0) {
    const chunk = Math.min(remaining, stepY);
    await page.mouse.wheel({ deltaX: 0, deltaY: chunk * direction });
    remaining -= chunk;
    await page.waitForTimeout(resolvedStepWaitMs);
  }

  // Snap to the exact target to avoid accumulating wheel rounding error.
  await page.evaluate((y) => window.scrollTo(0, y), targetY);
}

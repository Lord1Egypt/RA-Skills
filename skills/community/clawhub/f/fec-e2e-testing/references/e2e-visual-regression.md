#E2E visual regression testing

Detect unexpected UI changes through screenshot comparison. Suitable for CSS refactoring, design token update, component revision and other scenarios.

## Basic usage

```typescript
import { test, expect } from "@playwright/test";

test("Homepage layout is consistent with baseline", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  // Compare full-page screenshots - automatically generate a baseline for the first run
  await expect(page).toHaveScreenshot("homepage-full.png", {
    fullPage: true,
    maxDiffPixels: 100, // Slight pixel differences allowed (anti-aliasing, etc.)
  });
});

test("Button components are visually consistent", async ({ page }) => {
  await page.goto("/components/buttons");
  const submitButton = page.getByTestId("submit-button");
  await expect(submitButton).toHaveScreenshot("submit-button.png");
});
```

## Block dynamic content

Dynamic elements such as time, random IDs, and third-party ads can cause false positives. Use `mask` to block them:

```typescript
await expect(page).toHaveScreenshot("dashboard.png", {
  mask: [
    page.locator(".live-clock"),
    page.locator(".random-id"),
    page.locator(".ad-banner"),
  ],
});
```

## Disable animation

CSS animation will cause inconsistent screenshots. Inject the style to disable animation before taking screenshots:

```typescript
await page.addStyleTag({
  content:
    "*, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; }",
});
await expect(page).toHaveScreenshot("animated-page.png");
```

## Baseline management

- **First run**: `npx playwright test` fails but automatically generates baseline into `tests/` directory
- **Update baseline**: `npx playwright test --update-snapshots` when the UI is intentionally changed
- **CI consistency**: Baseline must be generated on the same OS (Linux/Ubuntu) as CI, font rendering differs between macOS and Linux
- **Multi-browser**: Each project generates a baseline independently (Chromium/Firefox/WebKit rendering results are different)
- **Baseline file**: Incorporate into `.gitignore` or Git LFS management to avoid warehouse expansion

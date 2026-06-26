# Playwright / Cypress E2E 模式

## 目录结构

```text
tests/
├── e2e/
│   ├── auth/login.spec.ts
│   └── features/search.spec.ts
├── fixtures/
│   └── auth.ts
└── pages/
    ├── LoginPage.ts
    └── ItemsPage.ts
playwright.config.ts
```

## Page Object

```ts
import { type Locator, type Page } from "@playwright/test";

export class ItemsPage {
  readonly searchInput: Locator;
  readonly itemCards: Locator;

  constructor(private readonly page: Page) {
    this.searchInput = page.getByTestId("search-input");
    this.itemCards = page.getByTestId("item-card");
  }

  async goto() {
    await this.page.goto("/items");
  }

  async search(keyword: string) {
    await this.searchInput.fill(keyword);
    await this.page.waitForResponse((response) => response.url().includes("/api/search"));
  }
}
```

## Spec

```ts
import { expect, test } from "@playwright/test";
import { ItemsPage } from "../pages/ItemsPage";

test.describe("商品搜索", () => {
  test("按关键词搜索有结果", async ({ page }) => {
    const itemsPage = new ItemsPage(page);
    await itemsPage.goto();
    await itemsPage.search("test");
    await expect(itemsPage.itemCards.first()).toContainText(/test/i);
  });
});
```

## Config

```ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [["html"], ["junit", { outputFile: "playwright-results.xml" }]],
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Flaky 调试

```bash
npx playwright test path/to/spec.ts --repeat-each=10
npx playwright test path/to/spec.ts --retries=3
npx playwright show-trace path/to/trace.zip
```

常见原因：竞态、网络时序、动画、测试数据污染、跨测试状态泄露。

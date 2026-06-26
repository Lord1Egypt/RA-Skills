# E2E 视觉回归测试

通过截图快照对比检测非预期的 UI 变化。适用于 CSS 重构、设计 Token 更新、组件改版等场景。

## 基础用法

```typescript
import { test, expect } from "@playwright/test";

test("首页布局与基线一致", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  // 全页截图对比 - 首次运行自动生成基线
  await expect(page).toHaveScreenshot("homepage-full.png", {
    fullPage: true,
    maxDiffPixels: 100, // 允许的轻微像素差异（抗锯齿等）
  });
});

test("按钮组件视觉一致", async ({ page }) => {
  await page.goto("/components/buttons");
  const submitButton = page.getByTestId("submit-button");
  await expect(submitButton).toHaveScreenshot("submit-button.png");
});
```

## 屏蔽动态内容

时间、随机 ID、第三方广告等动态元素会导致误报，使用 `mask` 屏蔽：

```typescript
await expect(page).toHaveScreenshot("dashboard.png", {
  mask: [
    page.locator(".live-clock"),
    page.locator(".random-id"),
    page.locator(".ad-banner"),
  ],
});
```

## 禁用动画

CSS 动画会导致截图不一致，注入样式禁用动画后再截图：

```typescript
await page.addStyleTag({
  content:
    "*, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; }",
});
await expect(page).toHaveScreenshot("animated-page.png");
```

## 基线管理

- **首次运行**: `npx playwright test` 失败但自动生成基线到 `tests/` 目录
- **更新基线**: UI 有意变更时 `npx playwright test --update-snapshots`
- **CI 一致性**: 基线必须在与 CI 相同的 OS（Linux/Ubuntu）上生成，字体渲染在 macOS 与 Linux 间存在差异
- **多浏览器**: 每个 project 独立生成基线（Chromium/Firefox/WebKit 渲染结果不同）
- **基线文件**: 纳入 `.gitignore` 或 Git LFS 管理，避免仓库膨胀

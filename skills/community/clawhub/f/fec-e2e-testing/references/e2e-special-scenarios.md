# E2E 特殊场景

## Web3 / 钱包注入（Playwright）

在 **`page.goto` 之前**通过 `context.addInitScript` 注入 mock，避免依赖真实插件：

```typescript
test("连接钱包", async ({ page, context }) => {
  await context.addInitScript(() => {
    (window as unknown as { ethereum?: unknown }).ethereum = {
      isMetaMask: true,
      request: async ({ method }: { method: string }) => {
        if (method === "eth_requestAccounts")
          return ["0x1234567890123456789012345678901234567890"];
        if (method === "eth_chainId") return "0x1";
        return null;
      },
    };
  });

  await page.goto("/");
  await page.getByTestId("connect-wallet").click();
  await expect(page.getByTestId("wallet-address")).toContainText("0x1234");
});
```

链 ID、账户列表与业务契约保持一致即可。

## 金融或高风险操作

- **禁止**在真实生产环境执行真实资金操作；使用 **staging、mock 或 `test.skip`**。
- 断言**预览金额、成功态**与**关键接口 200** 后再结束用例，超时给足（如链上确认场景）。

```typescript
test("下单预览与成功态", async ({ page }) => {
  test.skip(process.env.NODE_ENV === "production", "生产环境跳过真实交易");

  await page.goto("/markets/demo");
  await page.getByTestId("position-yes").click();
  await page.getByTestId("trade-amount").fill("1.0");

  const preview = page.getByTestId("trade-preview");
  await expect(preview).toContainText("1.0");

  await page.getByTestId("confirm-trade").click();
  await page.waitForResponse(
    (resp) => resp.url().includes("/api/trade") && resp.status() === 200,
    { timeout: 30_000 },
  );
  await expect(page.getByTestId("trade-success")).toBeVisible();
});
```

#E2E Special Scenario

## Web3/Wallet Injection (Playwright)

Inject mock through `context.addInitScript` before **`page.goto` to avoid relying on real plugins:

```typescript
test("Connect wallet", async ({ page, context }) => {
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

Just keep the chain ID, account list and business contract consistent.

## Financial or high-risk operations

- **It is prohibited** to perform real fund operations in a real production environment; use **staging, mock or `test.skip`**.
- Assert **preview amount**, success status** and **key interface 200** before ending the use case, with sufficient timeout (such as on-chain confirmation scenario).

```typescript
test("Order preview and success status", async ({ page }) => {
  test.skip(process.env.NODE_ENV === "production", "The production environment skips real transactions");

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

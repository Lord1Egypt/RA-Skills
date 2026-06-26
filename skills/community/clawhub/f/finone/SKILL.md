---
name: finone
description: Use this skill when the user asks about invoices (hóa đơn), e-invoices per Nghị định 70, revenue or expense statistics, VAT, or other accounting tasks for a Vietnamese shop or micro company. Wires the agent to FinOne / Vbill via the FinOne MCP server for invoice CRUD, e-invoice publication, statistics, and Xbill sync. Each tool call requires a FinOne user ID; if missing from memory, ask the user.
metadata: {"openclaw":{"requires":{"config":["mcp.servers.finone"]},"emoji":"🧾"}}
---

# FinOne Accounting Skill for VN Merchants

This skill turns the agent into an accounting helper for Vietnamese shop owners and micro companies that use FinOne / Vbill. It covers invoice management, e-invoice publication per Nghị định 70, revenue and expense statistics, and Xbillstore sync.

## Setup (one-time)

The skill calls the FinOne MCP server at `https://api-uat.vbill.vn/mcp` (server name `finone-mcp-server` v1.0.0, protocol 2024-11-05). FinOne AIO is pre-launch as of 2026-05-14; the UAT-named host is the only environment that exists and is what Nhan production already calls.

If the agent's OpenClaw config does not already register this MCP server, add the following block to the agent's `openclaw.json` at the top level:

```json
"mcp": {
  "servers": {
    "finone": {
      "url": "https://api-uat.vbill.vn/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Auth is header-less. Each tool call takes a `userId` argument. The merchant's FinOne `userId` lives in the agent's memory; if missing, ask the user (they can read it from FinOne / Vbill app > Profile).

## When to invoke this skill

Trigger phrases (Vietnamese, the common path) and English equivalents:

- "tạo hoá đơn", "ghi hoá đơn", "in hoá đơn" / "create invoice"
- "xuất e-invoice", "phát hành hoá đơn điện tử" / "issue e-invoice"
- "doanh thu tháng này", "báo cáo doanh thu", "thống kê hoá đơn" / "revenue report", "invoice statistics"
- "cập nhật giá sản phẩm", "đổi VAT" / "update product price", "change VAT"
- "đồng bộ hoá đơn Xbill" / "sync invoices from Xbillstore"

## Tool catalog

14 tools exposed by the FinOne MCP server (Vietnamese descriptions on the server side, in-line summary here):

### Invoice CRUD
- `verifyInvoiceBeforeCreate({userId, invoiceData})` - dry-run that OCR-reads and validates invoice data without creating. Always call this first when the user uploads an invoice image, then confirm extracted data with the user.
- `createInvoice({userId, invoiceData})` - create an internal invoice (hoá đơn gốc). Accepts a text payload or an image (OCR built-in).
- `viewInvoice({userId, invoiceId})` - return a PDF link for the internal invoice. Wrap with a hyperlink in the reply.
- `deleteInvoice({userId, invoiceId})` - delete an internal invoice. Only works on the internal copy, not on a published e-invoice.

### E-Invoice flow (Nghị định 70)
- `previewEInvoice({userId, invoiceId})` - preview the e-invoice PDF before publishing. Always offer this to the user for review.
- `createEInvoice({userId, invoiceId})` - publish the e-invoice officially. **Not reversible.** Always confirm with the user before calling.
- `viewEInvoice({userId, invoiceId})` - view a published e-invoice.

### Statistics
- `incomeInvoiceStatistic({userId, invoiceDateFrom?, invoiceDateTo?})` - revenue invoices (đầu ra). Returns total count, paid / unpaid breakdown, total amount in VND. Date format `YYYY-MM-DD`, both fields optional.
- `expenseInvoiceStatistic({userId, invoiceDateFrom?, invoiceDateTo?})` - expense invoices (đầu vào). Same shape.

### Sync
- `syncIncomeInvoice({userId, dateFrom, dateTo})` - pull income invoices from Xbillstore. `checkXbillConnect` first.
- `syncExpenseInvoice({userId, dateFrom, dateTo})` - pull expense invoices from Xbillstore. `checkXbillConnect` first.

### Setup helpers
- `getUserInfo({userId})` - verify the userId resolves to a real user. Use to validate pairing before running other tools.
- `updateProduct({userId, productName, updateData})` - update price / VAT of an existing product. Case-sensitive product name. Valid VAT values: `0, 5, 8, 10, -1` (không kê khai), `-2` (miễn thuế / KCT).
- `checkXbillConnect({userId})` - check Xbillstore connection is live. Required before sync.

## Hard rules

- When the user sends an invoice image, always run `verifyInvoiceBeforeCreate` first. Summarize the OCR result (date, customer, line items with name + quantity + price + VAT + unit) and wait for user confirmation before calling `createInvoice`.
- If the OCR result has missing or zero values for required fields (customer, line item price, total), list the missing fields and ask the user to fill them in manually before calling `createInvoice`. Do not silently default to zero or copy a price from a similar-looking line.
- After `createInvoice` succeeds, ask the user whether to publish the e-invoice. Never auto-call `createEInvoice` without explicit confirmation; the action is not reversible.
- VAT input must be one of `0, 5, 8, 10, -1, -2`. If the user gives a different number or leaves it blank, ask before defaulting.
- Currency is always VND. Format numbers with `.` as the thousand separator (Vietnamese convention: `1.250.000đ`, not `1,250,000 VND`).
- Never invent a `userId`. If memory has none and the user has not provided one, ask the user to grab it from FinOne / Vbill app > Profile.
- If the agent is shared across multiple users (group chat, shared web widget), confirm the active `userId` at session start. Treat `finone.userId` in memory as the user's last-confirmed binding, not a fixed identity for the agent.
- Never offer tax-law interpretation. Reference Nghị định 70 / relevant Circulars for compliance flow; redirect deeper questions to an accountant.

## Memory schema

The skill expects the following structured memory entries for the merchant:

- `finone.userId` - integer, the FinOne user ID for this merchant. Required for every tool call.
- `finone.shopName` - string, the user-facing shop / business name. Used in invoice `customer` field defaults.
- `finone.defaultVAT` - one of `0, 5, 8, 10, -1, -2`. If set, use as the default VAT when the user does not specify; otherwise ask.
- `finone.lastInvoiceId` - integer, the most recently created invoice ID. Useful for `createEInvoice` follow-ups.

If `finone.userId` is not set, do not call any FinOne tool. Ask the user for it first.

## Examples

### Example 1: image upload, invoice creation, e-invoice publish

User: [uploads invoice image]

Agent:
1. Call `verifyInvoiceBeforeCreate({userId: 12345, invoiceData: ...})` with the OCR result.
2. Reply with a markdown table summarising the extracted data and the line items.
3. Ask: "Anh / chị xác nhận tạo hoá đơn này không?"
4. If user confirms, call `createInvoice({userId: 12345, invoiceData: ...})`. Save returned `invoiceId` to `finone.lastInvoiceId`.
5. Reply: "Đã tạo hoá đơn #{invoiceId}. Anh / chị có muốn phát hành e-invoice luôn không?"
6. If user confirms again, call `previewEInvoice({userId, invoiceId})` first, send the preview PDF link. After user reviews and re-confirms, call `createEInvoice({userId, invoiceId})`.

### Example 2: revenue report for the current month

User: "Doanh thu tháng này được bao nhiêu rồi?"

Agent:
1. Compute the first day of the current month in `YYYY-MM-DD` format.
2. Call `incomeInvoiceStatistic({userId: 12345, invoiceDateFrom: "2026-05-01", invoiceDateTo: "2026-05-14"})`.
3. Format the response as a bullet list: tổng hoá đơn, đã xuất e-invoice, chưa xuất, tổng giá trị (VND), đã thanh toán, chưa thanh toán.

### Example 3: VAT update

User: "Đổi VAT của sản phẩm Cà phê sữa thành 8%"

Agent:
1. Confirm product name exactly as it appears in FinOne (case-sensitive): "Tên sản phẩm trong hệ thống là 'Cà phê sữa' phải không?"
2. After confirmation, call `updateProduct({userId: 12345, productName: "Cà phê sữa", updateData: {vat: 8}})`.
3. Reply with the actual return value of `updateProduct`. Do not invent the previous VAT - say "Đã cập nhật VAT của 'Cà phê sữa' thành 8%." If `updateProduct` returns the previous VAT, include it; if it does not, omit.

## References

- FinOne MCP server endpoint: configured via `mcp.servers.finone.url` in `openclaw.json` (see Setup section above).
- Nghị định 70/2025 (e-invoice mandate): Vietnamese government decree on electronic invoices.
- Companion DOSClaw `finance-assistant` template (separate from this skill) registers the FinOne MCP server in `openclaw.json` for users who provision an agent from that template, so they do not need to run the Setup step manually.

const test = require("node:test");
const assert = require("node:assert/strict");

const {
  parseOverrideDate,
  resolveDate,
  sheetNameFromDate,
  normalize,
  validate,
} = require("../lib/expenseValidator");

test("parseOverrideDate accepts strict ISO format", () => {
  assert.equal(parseOverrideDate(["node", "handler.js", "--date", "2026-03-25"]), "2026-03-25");
});

test("parseOverrideDate rejects non-ISO format", () => {
  assert.throws(
    () => parseOverrideDate(["node", "handler.js", "--date", "03/25/2026"]),
    /YYYY-MM-DD/
  );
});

test("resolveDate keeps valid ISO dates", () => {
  assert.equal(resolveDate("2026-03-25", new Date("2026-03-25T12:00:00Z")), "2026-03-25");
});

test("resolveDate resolves MM\/DD\/YYYY when it matches today", () => {
  assert.equal(resolveDate("03/25/2026", new Date("2026-03-25T12:00:00Z")), "2026-03-25");
});

test("resolveDate resolves DD-MM-YYYY when it matches today", () => {
  assert.equal(resolveDate("25-03-2026", new Date("2026-03-25T12:00:00Z")), "2026-03-25");
});

test("resolveDate rejects old dates without override", () => {
  assert.throws(
    () => resolveDate("03/20/2026", new Date("2026-03-25T12:00:00Z")),
    /re-run with --date/
  );
});

test("normalize cleans currency aliases and item defaults", () => {
  const expense = normalize(
    {
      date: "03/25/2026",
      vendor: " ACME MART ",
      items: [{ description: " Coffee ", quantity: "", amount: "" }],
      subtotal: "",
      tax: "",
      total: "8.50",
      currency: "$",
      category: " Food & Drink ",
    },
    { today: new Date("2026-03-25T12:00:00Z") }
  );

  assert.deepEqual(expense.items, [{ description: "Coffee", quantity: 1, amount: 0 }]);
  assert.equal(expense.vendor, "ACME MART");
  assert.equal(expense.currency, "USD");
  assert.equal(expense.subtotal, 8.5);
  assert.equal(expense.tax, 0);
  assert.equal(expense.date, "2026-03-25");
});

test("validate rejects missing required fields", () => {
  assert.throws(() => validate({ vendor: "", date: "", total: 0 }), /vendor, date, total/);
});

test("sheetNameFromDate derives MM-YY", () => {
  assert.equal(sheetNameFromDate("2026-03-25"), "03-26");
});

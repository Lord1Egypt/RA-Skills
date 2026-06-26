---
name: actual-budget
description: Query and manage personal finances via the official Actual Budget Node.js API. Use when handling budget queries, transaction imports/exports, account management, categorization, rules, schedules, and bank sync for self-hosted Actual Budget instances. Requires Node.js and Actual credentials via environment variables.
---

# Actual Budget API

Use the official `@actual-app/api` Node.js package to work with a synced Actual Budget file. Keep all credentials outside the skill and load them from the user's runtime environment.

## Installation

Install only the official package from the npm registry:

```bash
npm install @actual-app/api
```

Security checks:
- Package name: `@actual-app/api`
- Do not install similarly named packages.
- Do not download and execute remote scripts.
- Do not disable TLS verification. For self-signed certificates, add the CA to system trust or use `NODE_EXTRA_CA_CERTS` pointing at that CA file.

## Required configuration

Load configuration from environment variables supplied by the user or their local wrapper. Keep passwords, sync IDs, encryption passwords, raw account data, and full transaction exports redacted unless the user explicitly requests the sensitive output.

| Variable | Required | Description |
|----------|----------|-------------|
| `ACTUAL_SERVER_URL` | Yes | Actual server URL |
| `ACTUAL_PASSWORD` | Yes | Server password |
| `ACTUAL_SYNC_ID` | Yes | Budget Sync ID from Settings → Advanced |
| `ACTUAL_DATA_DIR` | No | Local cache directory for budget data |
| `ACTUAL_ENCRYPTION_PASSWORD` | No | E2E encryption password, if enabled |
| `NODE_EXTRA_CA_CERTS` | No | CA certificate path for self-signed certs |

For stable automation, prefer one private credentials file with strict permissions and source it in a local wrapper before running scripts. Use a generic filename such as `memory/secrets/actual-credentials` and keep it out of public repositories.

## Safe workflow

1. Confirm the task is read-only or mutating.
2. For mutating tasks, summarize the intended changes before applying them unless the user already gave explicit approval.
3. Initialize the API, download the budget, perform the work, sync only if data changed, and always shut down.
4. Redact secrets and minimize sensitive financial output in final replies.

## Quick start

```javascript
const api = require('@actual-app/api');

const config = globalThis['process']?.['env'] ?? {};
const required = name => {
  const value = config[name];
  if (!value) throw new Error(`Missing required Actual setting: ${name}`);
  return value;
};

await api.init({
  dataDir: config.ACTUAL_DATA_DIR || '/tmp/actual-cache',
  serverURL: required('ACTUAL_SERVER_URL'),
  password: required('ACTUAL_PASSWORD'),
});

const encryptionKey = config.ACTUAL_ENCRYPTION_PASSWORD;
const encryption = encryptionKey
  ? Object.fromEntries([['password', encryptionKey]])
  : undefined;

await api.downloadBudget(required('ACTUAL_SYNC_ID'), encryption);

try {
  // ... do work ...
  // await api.sync(); // call only after writes
} finally {
  await api.shutdown();
}
```

## Core concepts

- Amounts are integers in cents: `$50.00` = `5000`, `-1200` = expense of `$12.00`.
- Dates use `YYYY-MM-DD`; months use `YYYY-MM`.
- IDs are UUIDs. Use `getIDByName(type, name)` to look up by name.
- Convert amounts with `api.utils.amountToInteger(123.45)`.

## Common operations

### Budget overview

```javascript
const months = await api.getBudgetMonths();
const month = await api.getBudgetMonth('2026-01');
```

### Accounts

```javascript
const accounts = await api.getAccounts();
const balance = await api.getAccountBalance(accountId);
const newId = await api.createAccount({ name: 'Checking', type: 'checking' }, 50000);
await api.closeAccount(accountId, transferToAccountId);
```

### Transactions

```javascript
const txns = await api.getTransactions(accountId, '2026-01-01', '2026-01-31');

const { added, updated } = await api.importTransactions(accountId, [
  { date: '2026-01-15', amount: -2500, payee_name: 'Grocery Store', notes: 'Weekly run' },
  { date: '2026-01-16', amount: -1200, payee_name: 'Coffee Shop', imported_id: 'bank-123' },
]);

await api.updateTransaction(txnId, { category: categoryId, cleared: true });
```

### Categories and payees

```javascript
const categories = await api.getCategories();
const groups = await api.getCategoryGroups();
const payees = await api.getPayees();

const catId = await api.createCategory({ name: 'Subscriptions', group_id: groupId });
const payeeId = await api.createPayee({ name: 'Netflix', category: catId });
```

### Budget amounts

```javascript
await api.setBudgetAmount('2026-01', categoryId, 30000);
await api.setBudgetCarryover('2026-01', categoryId, true);
```

### Rules

```javascript
const rules = await api.getRules();
await api.createRule({
  stage: 'pre',
  conditionsOp: 'and',
  conditions: [{ field: 'payee', op: 'is', value: payeeId }],
  actions: [{ op: 'set', field: 'category', value: categoryId }],
});
```

### Schedules

```javascript
const schedules = await api.getSchedules();
await api.createSchedule({
  payee: payeeId,
  account: accountId,
  amount: -1500,
  date: { frequency: 'monthly', start: '2026-01-01', interval: 1, endMode: 'never' },
});
```

### Bank sync

```javascript
await api.runBankSync({ accountId });
```

### Sync and shutdown

```javascript
await api.sync();
await api.shutdown();
```

## ActualQL queries

```javascript
const { q, runQuery } = require('@actual-app/api');

const { data: totals } = await runQuery(
  q('transactions')
    .filter({
      date: [{ $gte: '2026-01-01' }, { $lte: '2026-01-31' }],
      amount: { $lt: 0 },
    })
    .groupBy('category.name')
    .select(['category.name', { total: { $sum: '$amount' } }])
);

const { data: matches } = await runQuery(
  q('transactions')
    .filter({ 'payee.name': { $like: '%grocery%' } })
    .select(['date', 'amount', 'payee.name', 'category.name'])
    .orderBy({ date: 'desc' })
    .limit(20)
);
```

Operators: `$eq`, `$lt`, `$lte`, `$gt`, `$gte`, `$ne`, `$oneof`, `$regex`, `$like`, `$notlike`.
Use `.options({ splits: 'inline' | 'grouped' | 'all' })` for split transactions.

## Helpers

```javascript
const acctId = await api.getIDByName('accounts', 'Checking');
const catId = await api.getIDByName('categories', 'Food');
const payeeId = await api.getIDByName('payees', 'Amazon');
const budgets = await api.getBudgets();
```

## Transfers

Transfers use special payees. Find the transfer payee by `transfer_acct`:

```javascript
const payees = await api.getPayees();
const transferPayee = payees.find(p => p.transfer_acct === targetAccountId);
await api.importTransactions(fromAccountId, [
  { date: '2026-01-15', amount: -10000, payee: transferPayee.id },
]);
```

## Split transactions

```javascript
await api.importTransactions(accountId, [{
  date: '2026-01-15',
  amount: -5000,
  payee_name: 'Costco',
  subtransactions: [
    { amount: -3000, category: groceryCatId },
    { amount: -2000, category: householdCatId },
  ],
}]);
```

## Bulk import

```javascript
await api.runImport('My-New-Budget', async () => {
  for (const acct of myData.accounts) {
    const id = await api.createAccount(acct);
    await api.addTransactions(id, myData.transactions.filter(t => t.acctId === id));
  }
});
```

## Reference

For complete API details, use the official Actual Budget API and ActualQL documentation from the Actual Budget project.

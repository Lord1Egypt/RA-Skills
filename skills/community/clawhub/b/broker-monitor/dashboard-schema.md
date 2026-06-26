# Dashboard Data Schema & Persistent Storage

## Storage Configuration

The interactive dashboard uses `window.storage` API for persistent data across sessions.

**Storage Key**: `broker-monitor-data-v3`

**Stored Object**:
```json
{
  "data": { "<YYYY-MM>": { "ibkr": {...}, "schw": {...}, "hood": {...}, "futu": {...}, "sources": "..." } },
  "periods": [ { "id": "YYYY-MM", "label": "YYYY年M月" } ],
  "lastUpdated": "ISO-8601 timestamp"
}
```

## Data Schema Per Period

Each period (month) contains data for all four brokers:

### IBKR
```json
{
  "darts": 432.9,        // DARTs in 万笔
  "accounts": 475.4,     // Client accounts in 万
  "equity": 789.4,       // Client equity in $B
  "margin": 86.0,        // Margin loans in $B
  "credit": 168.8,       // Client credit balances in $B
  "commission": 2.74     // Avg commission per order in $
}
```

### SCHW
```json
{
  "dat": 990,             // Daily average trades in 万笔
  "assets": 12.22,        // Total client assets in $T
  "nna": 50.0,            // Core NNA in $B (exclude one-time items)
  "newAccounts": 39.5,    // New brokerage accounts opened in 万
  "margin": 120.6,        // Margin loan balances in $B
  "sweepCash": 436.1,     // Transactional sweep cash in $B
  "activeAccounts": 3890  // Active brokerage accounts in 万
}
```

### HOOD
```json
{
  "fundedCustomers": 2740,  // Funded customers in 万
  "platformAssets": 314,     // Total platform assets in $B
  "netDeposits": 5.6,       // Net deposits in $B (monthly)
  "equityVolume": 194.4,    // Equity notional trading volume in $B
  "optionsContracts": 180.3, // Options contracts traded in 百万张
  "cryptoVolume": 25.0,     // Crypto notional trading volume in $B
  "eventContracts": 24      // Event contracts traded in 亿张
}
```

### FUTU
```json
{
  "fundedAccounts": 337,   // Funded/paying accounts in 万 (quarterly)
  "clientAssets": 158,     // Client assets in $B (quarterly)
  "tradingVolume": 511,    // Trading volume in $B (quarterly)
  "revenue": 827           // Revenue in $M (quarterly)
}
```

## Valuation Data (Static, Updated Per Report)

Valuation data is hardcoded in the dashboard (not stored), since it requires interpretation. Update these constants in the JSX when generating a new report:

```javascript
const VALUATIONS = {
  schw: {
    ticker: "SCHW",
    price: 93.77,          // Stock price ($)
    ttmPE: 20.1,           // Trailing PE
    fwdPE: 16.8,           // Forward PE (NTM)
    ttmEPS: 4.67,          // TTM EPS ($)
    fwdEPS: 5.58,          // FY+1 consensus EPS ($)
    fwdGrowth: "+19.5%",   // FY+1 EPS growth rate
    bearPE: "13.0x (2020.3)",     // Historical bear PE
    avgPE: "23.3x (10Y)",        // Historical average PE
    bullPE: "31.5x (2017)",      // Historical bull PE
    mktCap: "~$170B",
    consensus: "Hold/Buy混合",
    source: "FullRatio, Zacks, MacroTrends"
  },
  // ... ibkr, hood, futu follow same structure
};
```

## Dashboard Tabs

The React dashboard has 8 tabs:

1. **📊 跨公司对比** — Cross-company comparison tables (4 dimensions)
2. **IBKR** — Individual 3-month rolling metrics
3. **SCHW** — Individual 3-month rolling metrics
4. **HOOD** — Individual 3-month rolling metrics
5. **FUTU** — Individual 3-month rolling metrics + annual summary card
6. **💰 估值对比** — Valuation comparison table + bull/bear PE ranges
7. **🚩 信号** — Key flags (positive + warning)
8. **✏️ 数据录入** — Data entry interface for biweekly updates

## Update Workflow

When updating the dashboard for a new period:

1. Click "✏️ 数据录入" tab
2. Click "+ 新增月份" if the month doesn't exist yet
3. Select the month to edit
4. Fill in each broker's metrics from the latest monthly reports
5. Add source notes in the "数据来源备注" field
6. Data auto-saves to persistent storage

For valuation data updates, regenerate the JSX artifact with updated `VALUATIONS` and `FLAGS` constants.

# ChainStream GraphQL Query Patterns

Ready-to-use query templates for common blockchain analytics scenarios. Replace placeholder values (`TOKEN_ADDRESS`, `WALLET_ADDRESS`, etc.) with actual addresses.

All queries must be wrapped in a chain group: `Solana { ... }`, `EVM(network: eth) { ... }`, or `Trading { ... }`.

## DEX Trades

### Latest Trades (Solana)

```graphql
query {
  Solana {
    DEXTrades(limit: {count: 25}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Trade {
        Buy { Currency { MintAddress Symbol Name } Amount PriceInUSD }
        Sell { Currency { MintAddress Symbol Name } Amount }
        Dex { ProtocolName ProtocolFamily }
      }
    }
  }
}
```

### Trades for a Specific Token (Solana)

```graphql
query {
  Solana {
    DEXTrades(
      limit: {count: 25}
      orderBy: {descending: Block_Time}
      where: {any: [{Trade: {Buy: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}, {Trade: {Sell: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}]}
    ) {
      Block { Time }
      Trade {
        Buy { Amount PriceInUSD Account { Owner } Currency { MintAddress Symbol } }
        Sell { Currency { MintAddress Symbol } Amount }
        Dex { ProtocolName }
      }
    }
  }
}
```

### Latest Trades (EVM)

```graphql
query {
  EVM(network: eth) {
    DEXTrades(limit: {count: 20}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Transaction { Signature Signer }
      Trade {
        Buy { Amount AmountInUSD Currency { Name Symbol MintAddress } PriceInUSD }
        Sell { Amount AmountInUSD Currency { Name Symbol MintAddress } }
        Dex { ProtocolName ProtocolFamily }
      }
    }
  }
}
```

### Top Traders by Volume

```graphql
query {
  Solana {
    DEXTrades(
      limit: {count: 100}
      where: {
        any: [{Trade: {Buy: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}, {Trade: {Sell: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}]
      }
    ) {
      Trade { Buy { Account { Owner } Amount PriceInUSD } }
      count
      sum(of: Trade_Buy_Amount)
    }
  }
}
```

### pump.fun Trades (Last 7 Days)

```graphql
query {
  Solana {
    DEXTrades(
      where: {
        Block: {Time: {since: "2026-03-31 00:00:00"}}
        Trade: {Dex: {ProgramAddress: {is: "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"}}}
      }
      limit: {count: 1000}
      orderBy: {descending: Block_Time}
    ) {
      Block { Time }
      Trade {
        Buy { Currency { MintAddress } Amount }
        Sell { Currency { MintAddress } Amount }
        Dex { ProtocolName }
      }
    }
  }
}
```

## DEXTradeByTokens (Token-Centric)

### All Trades for a Specific Token

Token-centric view: both buy and sell sides appear as rows with the queried token as the primary `Currency`.

```graphql
query {
  Solana {
    DEXTradeByTokens(
      where: {Trade: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}
      limit: {count: 50}
      orderBy: {descending: Block_Time}
    ) {
      Block { Time }
      Trade {
        Currency { MintAddress Symbol Name }
        Amount AmountInUSD
        Side { Type Currency { MintAddress Symbol } Amount AmountInUSD }
        Dex { ProtocolName ProtocolFamily }
      }
    }
  }
}
```

### Buy vs Sell Volume Analysis

```graphql
query {
  Solana {
    DEXTradeByTokens(
      where: {
        Trade: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}
        Block: {Time: {since: "2026-03-31 00:00:00"}}
      }
    ) {
      Trade { Side { Type } }
      count
      sum(of: Trade_AmountInUSD)
    }
  }
}
```

### Wallet PnL via DEXTradeByTokens (with calculate)

```graphql
query ($token: String!, $signer: String!, $since: String, $till: String) {
  Solana {
    DEXTradeByTokens(
      where: {
        Trade: {Currency: {MintAddress: {is: $token}}}
        Transaction: {Signer: {is: $signer}, Result: {Success: true}}
        Block: {Time: {since: $since, till: $till}}
      }
    ) {
      Trade { Currency { Name Symbol MintAddress } }
      buys: count(if: {Trade: {Side: {Type: {is: "buy"}}}})
      sells: count(if: {Trade: {Side: {Type: {is: "sell"}}}})
      buy_volume_usd: sum(of: Trade_Side_AmountInUSD, if: {Trade: {Side: {Type: {is: "buy"}}}})
      sell_volume_usd: sum(of: Trade_Side_AmountInUSD, if: {Trade: {Side: {Type: {is: "sell"}}}})
      RealizedPnL: calculate(expression: "$sell_volume_usd - $buy_volume_usd")
      trades: count
    }
  }
}
```

Variables: `{"token": "TOKEN_ADDRESS", "signer": "WALLET_ADDRESS", "since": "2026-03-01 00:00:00", "till": "2026-04-01 00:00:00"}`

## OHLCV / K-Line

### OHLCV via DEXTradeByTokens (Dimension Aggregation)

Construct candles from raw trades using time interval bucketing and dimension-level aggregation:

```graphql
query {
  Solana {
    DEXTradeByTokens(
      limit: {count: 100}
      orderBy: {descendingByField: "Block_Timefield"}
      where: {
        Trade: {
          Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}
          Market: {MarketAddress: {is: "POOL_ADDRESS"}}
          PriceAsymmetry: {lt: "0.1"}
        }
      }
    ) {
      Block {
        Timefield: Time(interval: {in: minutes, count: 5})
      }
      volume: sum(of: Trade_Amount)
      Trade {
        high: Price(maximum: Trade_Price)
        low: Price(minimum: Trade_Price)
        open: Price(minimum: Block_Slot)
        close: Price(maximum: Block_Slot)
      }
      count
    }
  }
}
```

### OHLCV in USD (EVM)

```graphql
query ($token: String!) {
  EVM(network: bsc) {
    DEXTradeByTokens(
      orderBy: {ascendingByField: "Block_Time"}
      where: {Trade: {Currency: {MintAddress: {is: $token}}, PriceAsymmetry: {lt: "0.1"}}}
    ) {
      Block {
        Time(interval: {count: 5, in: minutes})
      }
      Trade {
        open: PriceInUSD(minimum: Block_Slot)
        close: PriceInUSD(maximum: Block_Slot)
        max: PriceInUSD(maximum: Trade_PriceInUSD)
        min: PriceInUSD(minimum: Trade_PriceInUSD)
      }
      volume: sum(of: Trade_Side_AmountInUSD, selectWhere: {gt: "0"})
    }
  }
}
```

## Balance & Transfers

### Wallet Token Balances (Solana)

```graphql
query {
  Solana {
    BalanceUpdates(
      where: {BalanceUpdate: {Account: {Owner: {is: "WALLET_ADDRESS"}}}}
      orderBy: {descendingByField: "BalanceUpdate_PostBalance_maximum"}
    ) {
      BalanceUpdate {
        Balance: PostBalance(maximum: Block_Slot)
        Currency { Name Symbol MintAddress }
      }
    }
  }
}
```

### Wallet Token Balances (EVM)

```graphql
query {
  EVM(network: eth) {
    BalanceUpdates(
      where: {BalanceUpdate: {Account: {Owner: {is: "WALLET_ADDRESS"}}}}
      orderBy: {descendingByField: "BalanceUpdate_PostBalanceInUSD_maximum"}
    ) {
      BalanceUpdate {
        Account { Address Owner }
        Currency { Symbol Name MintAddress Decimals }
        PostBalance(maximum: Block_Time)
        PostBalanceInUSD(maximum: Block_Time)
      }
    }
  }
}
```

### Historical Balance (with calculate + OR)

```graphql
query ($address: String!) {
  Solana {
    Transfers(
      where: {
        any: [
          {Transfer: {Sender: {Address: {is: $address}}}}
          {Transfer: {Receiver: {Address: {is: $address}}}}
        ]
        Block: {Time: {since: "2025-01-01 00:00:00", till: "2025-12-31 23:59:59"}}
      }
    ) {
      Transfer { Currency { Symbol Name MintAddress } }
      sum_in: sum(of: Transfer_Amount, if: {Transfer: {Receiver: {Address: {is: $address}}}})
      sum_out: sum(of: Transfer_Amount, if: {Transfer: {Sender: {Address: {is: $address}}}})
      balance: calculate(expression: "$sum_in - $sum_out")
    }
  }
}
```

### Latest Transfers (Solana)

```graphql
query {
  Solana {
    Transfers(limit: {count: 20}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Transaction { Signature }
      Transfer {
        Currency { MintAddress Symbol }
        Sender { Address }
        Receiver { Address }
        Amount AmountInUSD
      }
    }
  }
}
```

## Transactions (with Joins)

### Solana Transaction with Full Details

```graphql
query {
  Solana {
    Transactions(limit: {count: 1}, orderBy: {descending: Block_Time}) {
      Block { Time Slot Height Hash }
      Transaction { Signature Fee FeePayer Signer }
      joinInstructions {
        Instruction { Program { Id Name Method } }
      }
      joinDEXTrades {
        Trade { Buy { Currency { MintAddress } Amount PriceInUSD } Sell { Currency { MintAddress } Amount } }
      }
      joinTransfers {
        Transfer { Currency { MintAddress } Amount AmountInUSD }
      }
    }
  }
}
```

### EVM Transaction with Logs and Traces

```graphql
query {
  EVM(network: eth) {
    Transactions(
      where: {Transaction: {From: {is: "WALLET_ADDRESS"}}}
      limit: {count: 10}
      orderBy: {descending: Block_Number}
    ) {
      Block { Time Number Hash }
      Transaction { Hash From To Value ValueInUSD Gas GasPrice Nonce Type }
      joinEvents {
        Log { Address EventName Topics { Topic0 Topic1 } Data }
      }
      joinCalls {
        Call { CallType FromAddress ToAddress ValueInNative GasUsed }
      }
    }
  }
}
```

## Pools & Liquidity

### DEX Pool Snapshot (Solana)

```graphql
query {
  Solana {
    DEXPools(limit: {count: 20}, tokenA: {is: "TOKEN_ADDRESS"}) {
      Pool {
        Address
        TokenAAddress
        TokenBAddress
        ProgramAddress
        LiquidityUSD
        PriceAtoB
        PriceBtoA
        LastUpdated
      }
    }
  }
}
```

### Top Liquidity Pools for a Token (EVM)

Uses field aliases to query both base and quote sides:

```graphql
query {
  EVM(network: eth) {
    TokenIsCurrencyA: DEXPoolEvents(
      limit: {count: 10}
      orderBy: {descendingByField: "Pool_Base_PostAmount_maximum"}
      where: {Pool: {Market: {BaseCurrency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}
    ) {
      Pool {
        Base { PostAmount(maximum: Block_Time) }
        Quote { PostAmount(maximum: Block_Time) }
        Market { MarketAddress BaseCurrency { Name Symbol MintAddress } QuoteCurrency { Name Symbol MintAddress } }
      }
    }
    TokenIsCurrencyB: DEXPoolEvents(
      limit: {count: 10}
      orderBy: {descendingByField: "Pool_Quote_PostAmount_maximum"}
      where: {Pool: {Market: {QuoteCurrency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}}
    ) {
      Pool {
        Base { PostAmount(maximum: Block_Time) }
        Quote { PostAmount(maximum: Block_Time) }
        Market { MarketAddress BaseCurrency { Name Symbol MintAddress } QuoteCurrency { Name Symbol MintAddress } }
      }
    }
  }
}
```

### DEX Pool Slippage (EVM only)

```graphql
query {
  EVM(network: eth) {
    DEXPoolSlippages(
      where: {Price: {Pool: {SmartContract: {is: "POOL_ADDRESS"}}}}
      limit: {count: 10}
      orderBy: {descending: Block_Time}
    ) {
      Price {
        BtoA { Price MinAmountOut MaxAmountIn }
        AtoB { Price MinAmountOut MaxAmountIn }
        Pool { SmartContract CurrencyA { SmartContract Decimals } CurrencyB { SmartContract Decimals } }
        Dex { ProtocolName ProtocolVersion }
        SlippageBasisPoints
      }
      Block { Time Number }
    }
  }
}
```

## Token Analytics

### Token Supply and Market Cap (EVM)

```graphql
query {
  EVM(network: eth) {
    TokenSupplyUpdates(
      limit: {count: 1}
      orderBy: {descending: Block_Time}
      tokenAddress: {is: "TOKEN_ADDRESS"}
    ) {
      TokenSupplyUpdate {
        Currency { MintAddress Name Symbol Decimals }
        TotalSupply
        MarketCapInUSD
        FDVInUSD
        PriceInUSD
      }
      Block { Time }
    }
  }
}
```

### Token Holders (EVM)

```graphql
query {
  EVM(network: eth) {
    TokenHolders(
      tokenAddress: {is: "TOKEN_ADDRESS"}
      limit: {count: 100}
      orderBy: {descending: Balance_Amount}
    ) {
      Holder { Address }
      Balance { Amount AmountInUSD }
      BalanceUpdate { FirstDate LastDate InCount OutCount }
    }
  }
}
```

### ERC20 Token Balance via TransactionBalances

```graphql
query {
  EVM(network: eth) {
    TransactionBalances(
      limit: {count: 1}
      orderBy: {descending: Block_Time}
      where: {TokenBalance: {Address: {is: "WALLET_ADDRESS"}, Currency: {SmartContract: {is: "TOKEN_ADDRESS"}}}}
    ) {
      Block { Time Number }
      TokenBalance {
        Currency { SmartContract Decimals }
        PostBalance
        PostBalanceInUSD
        Address
      }
      Transaction { Hash }
    }
  }
}
```

## Prediction Markets (Polygon only)

### Latest Prediction Trades

```graphql
query {
  EVM(network: polygon) {
    PredictionTrades(
      limit: {count: 50}
      orderBy: {descending: Block_Time}
      where: {TransactionStatus: {Success: true}}
    ) {
      Block { Time }
      Trade {
        OutcomeTrade {
          Buyer Seller Amount CollateralAmount CollateralAmountInUSD
          Price PriceInUSD IsOutcomeBuy
        }
        Prediction {
          Question { Title MarketId Id Image }
          Outcome { Id Label }
          Marketplace { ProtocolName }
        }
      }
      Transaction { From Hash }
    }
  }
}
```

### Yes/No Volume for a Market

```graphql
query {
  EVM(network: polygon) {
    PredictionTrades(
      where: {
        TransactionStatus: {Success: true}
        Trade: {Prediction: {Question: {Id: {is: "QUESTION_ID"}}}}
        Block: {Time: {since: "2026-04-01 00:00:00"}}
      }
    ) {
      Trade { Prediction { Question { Title } } }
      yes_volume: sum(of: Trade_OutcomeTrade_CollateralAmountInUSD, if: {Trade: {OutcomeTrade: {IsOutcomeBuy: true}}})
      no_volume: sum(of: Trade_OutcomeTrade_CollateralAmountInUSD, if: {Trade: {OutcomeTrade: {IsOutcomeBuy: false}}})
      total_volume: sum(of: Trade_OutcomeTrade_CollateralAmountInUSD)
    }
  }
}
```

### Current Price per Outcome (Latest Trade)

```graphql
query {
  EVM(network: polygon) {
    PredictionTrades(
      limitBy: {by: Trade_Prediction_OutcomeToken_AssetId, count: 1}
      where: {
        TransactionStatus: {Success: true}
        Trade: {Prediction: {Question: {MarketId: {is: "MARKET_ID"}}}}
      }
    ) {
      Trade {
        OutcomeTrade {
          Price(maximum: Block_Time)
          PriceInUSD(maximum: Block_Time)
        }
        Prediction {
          OutcomeToken { AssetId }
          Outcome { Id Label }
        }
      }
    }
  }
}
```

## Blocks

### Latest Blocks (Solana)

```graphql
query {
  Solana {
    Blocks(limit: {count: 10}, orderBy: {descending: Block_Time}) {
      Block {
        Time Slot Height Hash TxCount
      }
    }
  }
}
```

### Latest Blocks (EVM)

```graphql
query {
  EVM(network: eth) {
    Blocks(limit: {count: 10}, orderBy: {descending: Block_Time}) {
      Block {
        Time Number Hash GasUsed GasLimit BaseFee
      }
    }
  }
}
```

## Pattern Reference: Data Shape to Chart Type

| Data Pattern | Recommended Chart | Example Query |
|-------------|------------------|---------------|
| Time series (price, volume over time) | Line / Candlestick | OHLCV via DEXTradeByTokens |
| Ranking (top tokens by volume) | Bar chart / Leaderboard | DEXTradeByTokens grouped |
| Distribution (asset allocation) | Pie / Treemap | BalanceUpdates grouped by Currency |
| Buy vs Sell breakdown | Stacked bar / Pie | DEXTradeByTokens grouped by Side.Type |
| Comparison (cross-protocol) | Grouped bar | DEXTrades grouped by Dex |
| Real-time feed (trade stream) | Table with scrolling | DEXTrades latest |
| Single metric (total count, total volume) | Metric card | Aggregation-only queries |
| Prediction odds over time | Area chart | PredictionTrades price by time |

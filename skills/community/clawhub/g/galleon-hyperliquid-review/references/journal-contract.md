# Journal contract

Keep an append-only UTC journal. Use one stable ticket or incident ID across every entry.

```text
2026-09-04T14:02:00Z HL-20260904-01 planned  <market, action, ticket digest>
2026-09-04T14:12:00Z HL-20260904-01 risk     <PASS or REJECT, risk and input times>
2026-09-04T14:20:00Z HL-20260904-01 approved <exact user line, ticket revision>
2026-09-04T14:21:00Z HL-20260904-01 sent     <client ids, nonce, expiry, response class>
2026-09-04T14:21:01Z HL-20260904-01 fill     <trade id, size, price, fee, maker or taker>
2026-09-04T16:05:00Z HL-20260904-01 closed   <flat proof, orphan status>
2026-09-04T17:00:00Z HL-20260904-01 reviewed <process grade, net result, one finding>
```

Corrections append a new `correction` line pointing to the original timestamp. Never edit history to make it agree with a later interpretation.

## Review block

```markdown
## Review <ticket-id>

- evidence window: <UTC>
- process: clean | minor break | major break
- outcome: <net USD and R, no adjective>
- entry and exit slippage: <bps against ticket>
- fees: <USD, maker or taker split>
- funding: <signed USD>
- protection gaps: <minutes or unknown>
- holding time: <duration>
- finding: <one repeatable fact>
- next owner or test: <one>
```

Weekly summaries aggregate closed trades, expectancy in R, drawdown, fees and funding as a share of gross PnL, process breaks by type, incidents, and one factual pattern. They do not recommend a new trade.

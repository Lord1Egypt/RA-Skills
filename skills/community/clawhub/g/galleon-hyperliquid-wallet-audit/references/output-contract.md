# Output contract

`capture.json` uses `hyperliquid-wallet-capture/v1`. It binds `source` (`live` or `fixture`), `scope.address`, `scope.network`, inclusive epoch-ms `startTime`/`endTime`, capture bounds, overall timestamps, per-history pagination termination and each raw `evidence` entry. Entries preserve exact `requestText`, `responseText`, SHA256 digests, HTTP status, read timestamps and any error. A live malformed response remains saved even when analysis fails.

`report.json` uses `hyperliquid-wallet-audit/v1`:

| Field | Meaning |
| --- | --- |
| `scope` | Exact account/network/window, default DEX and current-snapshot meaning |
| `coverage` | `bounded` or `partial`, explicit gaps, page termination, retained/excluded records, identical duplicates removed; `completeWindow` always false |
| `outcome` | `closedPnlUsdc`, signed `signedFeesByToken`, included builder fees, signed `fundingUsdc`, `observedNetUsdc`, notional and per-market accounting |
| `execution` | Maker/taker counts and notional shares, positive USDC fee charges, rebates, per-market positive-fee concentration |
| `exposure` | Account mode/role, reported margin summary, spot token balances, current default-perp positions, gross/signed notional; `protectionStatus: "not-assessed"` |
| `openOrders` | Observed detailed order identities and flags with no stop-coverage verdict |
| `evidence` | Verified manifest summaries, read span and sequential timestamp semantics |
| `limitations` | Unknown opening inventory, history retention, excluded market/account scope, arithmetic and authenticity limits |

Accounting amounts are decimal strings, using exact signed addition at up to 18 decimal places. Price-times-size notional truncates toward zero at 18 places. Percentages are descriptive numeric ratios, truncated to four decimal places; zero denominators yield `null`.

`observedNetUsdc = sum(default-perp closedPnl) - sum(signed USDC fees) + sum(signed default-perp funding)`. Negative fees represent rebates. Builder fees are part of the reported total fee and are never added again. A nonzero fee in another token has no automatic conversion; net USDC is `null`. A wholly unavailable fills or funding read also leaves net USDC `null`. Partial paging still permits an observed subtotal, with coverage explicitly partial. This subtotal is not complete profit, a portfolio return or a strategy-validation result.

`initialObservedPosition` is the position before the first captured fill for that coin. It does not identify the actual window opening position, historical cost basis or earlier costs. Unrealized PnL is reported separately in current positions, not added to the observed outcome.

The standalone script and package `audit` subcommand return a small JSON envelope with `ok`, `source`, `coverage`, `completeWindow`, `observedNetUsdc` and absolute paths in `files`. Inspect `report.json` for the complete diagnostic. Exit 0 means a report was produced, including explicit partial reports. Exit 1 means invalid inputs, invalid evidence, malformed records or a failed file write. Existing output directories are rejected to preserve prior observations.

Evidence files contain public wallet activity and should be shared according to the user's intended audience. Local hash verification establishes consistency against the included manifest. It does not prevent someone from changing the data and regenerating all hashes, or independently authenticate the remote exchange.

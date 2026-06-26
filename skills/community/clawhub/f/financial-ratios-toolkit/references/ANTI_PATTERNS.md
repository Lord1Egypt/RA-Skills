# Anti-Patterns (Cross-Project)

Total: **14**

## finance-bp-066--wealthbot (2)

### `AP-PORTFOLIO-ANALYTICS-001` — Division by zero in price ratio calculations corrupts rebalancing <sub>(high)</sub>

When calculating price_diff using current_price divided by old_price without validating old_price is non-zero, the result is NaN or INF. This corrupts portfolio rebalancing calculations in wealthbot, causing incorrect buy/sell decisions based on invalid prices_diff values. The same issue appears in getPricesDiff() where divide-by-zero when old_price equals zero produces NaN/infinity that propagates to all subsequent trade decisions.

### `AP-PORTFOLIO-ANALYTICS-004` — Incorrect portfolio value tracking destroys time-series integrity <sub>(high)</sub>

Updating existing ClientPortfolioValue records instead of creating new ones destroys the time-series integrity needed for billing calculations and historical reconciliation. This creates data corruption where billing calculations and historical reporting against custodian records will fail to match. Portfolio value records must be linked to parent ClientPortfolio via proper relationships to avoid orphaned records.

## finance-bp-068--xalpha (1)

### `AP-PORTFOLIO-ANALYTICS-006` — FIFO sell order violation corrupts cost basis and XIRR <sub>(high)</sub>

Processing positions out of chronological order in FIFO sell operations causes incorrect cost basis assignment, leading to inaccurate realized gains/losses and wrong XIRR calculation. Chinese funds have tiered redemption fees based on holding periods, so FIFO violations result in incorrect holding period calculation and wrong redemption fee being applied, causing direct financial loss.

## finance-bp-068--xalpha, finance-bp-093--PyPortfolioOpt, finance-bp-117--Riskfolio-Lib (1)

### `AP-PORTFOLIO-ANALYTICS-010` — Missing DataFrame schema validation causes KeyError propagation <sub>(medium)</sub>

Passing non-DataFrame objects (numpy arrays, lists) where DataFrame is expected causes NameError, AttributeError, or TypeError in downstream pandas operations. xalpha's fundinfo.price requires specific columns (date, netvalue, totvalue, comment), PyPortfolioOpt and Riskfolio-Lib require index alignment between expected returns and covariance matrix. Missing columns cause backtest calculations to fail with NaN values or KeyError.

## finance-bp-082--stock-screener (1)

### `AP-PORTFOLIO-ANALYTICS-007` — Score validation bypass allows invalid composite calculations <sub>(medium)</sub>

Accepting scores outside the 0-100 range in screener results corrupts ranking and rating logic, causing unpredictable screening results that violate the fundamental score contract. When combined with division-by-zero guards that return 0.0 for empty screener lists, this creates unpredictable behavior where invalid scores produce wrong composite calculations and incorrect Strong Buy/Buy/Watch/Pass ratings.

## finance-bp-093--PyPortfolioOpt (1)

### `AP-PORTFOLIO-ANALYTICS-008` — Convex optimization constraints violate DCP rules <sub>(high)</sub>

Using non-convex objectives or DCP-violating expressions in CVXPY optimization causes DCPError, completely preventing portfolio optimization from running. Similarly, providing non-callable constraints or invalid bounds formats (not matching n_assets length) causes TypeError. Feasibility violations like setting target_volatility below global minimum or target_return above maximum achievable return make problems infeasible.

## finance-bp-093--PyPortfolioOpt, finance-bp-117--Riskfolio-Lib (1)

### `AP-PORTFOLIO-ANALYTICS-003` — Non-positive-semidefinite covariance matrix breaks CVXPY optimization <sub>(high)</sub>

Passing a non-positive-semidefinite covariance matrix to CVXPY optimization with assume_PSD=True produces incorrect results because the solver assumes validity without verification. This causes Cholesky decomposition to fail or produce garbage weights, preventing portfolio optimization from running entirely. Riskfolio-Lib and PyPortfolioOpt both require explicit PSD validation before optimization.

## finance-bp-106--pyfolio-reloaded (2)

### `AP-PORTFOLIO-ANALYTICS-005` — Allocation denominator excludes cash, corrupting portfolio composition <sub>(medium)</sub>

When computing allocation percentages excluding cash from the denominator, portfolio allocation percentages will not sum to 100%, misrepresenting the portfolio's actual composition. Additionally, concentration metrics become artificially skewed when including cash (a non-position asset), producing misleading diversification assessments that could lead to inappropriate risk management decisions.

### `AP-PORTFOLIO-ANALYTICS-009` — Transaction data corruption from missing columns and invalid dates <sub>(medium)</sub>

Extracting round trips from transactions DataFrame without validating required columns (amount, price, symbol) causes KeyError exceptions. When open_dt is not strictly less than close_dt, negative or zero duration values indicate data corruption causing incorrect holding period statistics. Similarly, non-normalized transaction timestamps cause intra-day trades to be incorrectly split across days.

## finance-bp-107--empyrical-reloaded (1)

### `AP-PORTFOLIO-ANALYTICS-011` — Wrong annualization factors distort cross-frequency metric comparison <sub>(high)</sub>

Applying incorrect annualization factors (wrong values for daily, weekly, monthly, quarterly, yearly frequencies) produces non-comparable metrics across different return frequencies, causing invalid strategy comparisons and misallocated capital. The Sharpe ratio formula must use correct annualization with sample standard deviation (ddof=1), otherwise producing misleading risk-adjusted return estimates.

## finance-bp-107--empyrical-reloaded, finance-bp-118--FinanceToolkit (1)

### `AP-PORTFOLIO-ANALYTICS-012` — Misaligned time series in alpha/beta calculation produces invalid factor analysis <sub>(high)</sub>

Passing returns and factor_returns to alpha_beta functions without verifying data alignment on index labels (pd.Series) or length equality (np.ndarray) produces incorrect alpha/beta values due to correlation computed between mismatched periods. Including benchmark ticker in the asset ticker list causes circular correlation producing meaningless beta values of approximately 1.0.

## finance-bp-108--finmarketpy (1)

### `AP-PORTFOLIO-ANALYTICS-013` — Forward-filling spot prices creates look-ahead bias in TRI construction <sub>(high)</sub>

Forward-filling spot prices creates look-ahead bias where future prices are used to calculate historical returns, invalidating all TRI-based backtest results. The total return index construction requires multiplicative cumulation using cumprod (not cumsum) with base value 100, as additive cumulation allows negative cumulative returns to break the index chain.

## finance-bp-108--finmarketpy, finance-bp-106--pyfolio-reloaded (1)

### `AP-PORTFOLIO-ANALYTICS-002` — Look-ahead bias from unshifted signal generation and position calculations <sub>(high)</sub>

Generating trading signals from current-period technical indicators (RSI, moving averages) without proper shift(-1) creates look-ahead bias, causing live trading returns to fall far below backtested results. Similarly, when estimating intraday positions from transactions without applying shift(1) to EOD positions, day-start positions are contaminated with end-of-day values, making results unrepresentative of actual trading.

## finance-bp-117--Riskfolio-Lib, finance-bp-093--PyPortfolioOpt (1)

### `AP-PORTFOLIO-ANALYTICS-014` — Unsupported solver selection breaks advanced risk calculations <sub>(medium)</sub>

Using solvers that don't support required cone programming (power cone, exponential cone) causes CVXPY to fail with SolverError, returning None and breaking risk calculations. CLARABEL, SCS, ECOS support power cone for RLVaR/RLDaR calculations, while CLARABEL/MOSEK/SCS/ECOS support exponential cone for EVaR calculations. Riskfolio-Lib and PyPortfolioOpt both require careful solver selection.

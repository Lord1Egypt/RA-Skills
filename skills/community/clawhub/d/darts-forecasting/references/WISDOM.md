# Cross-Project Wisdom

Total: **10**

## `CW-TIME-SERIES-ML-001` — 3D TimeSeries dimensionality invariant
**From**: finance-bp-102--Darts · **Applicable to**: time-series-ml

Always expand TimeSeries values to exactly 3 dimensions (n_timesteps, n_components, n_samples) regardless of input format. This invariant enables uniform downstream processing regardless of whether the data is univariate (1 component), single-sample, or multivariate probabilistic series with multiple samples.

## `CW-TIME-SERIES-ML-002` — Strict time index validation
**From**: finance-bp-102--Darts · **Applicable to**: time-series-ml

Validate time index at construction: must be strictly monotonically increasing, have a well-defined frequency, no holes by default, and length must match values first dimension. This prevents silent data corruption in all downstream temporal operations.

## `CW-TIME-SERIES-ML-003` — MultiIndex preservation in multi-ticker pipelines
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

Maintain (ticker, date) MultiIndex structure throughout the entire feature engineering and prediction pipeline for multi-ticker trading systems. Downstream stages depend on this structure for proper temporal train/test splits that respect per-ticker time boundaries.

## `CW-TIME-SERIES-ML-004` — Purged walking forward cross-validation
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

Use purged walking forward split with embargo gap for financial time series validation. Random splits cause look-ahead bias, while splits without purge gaps contaminate results with overlapping outcomes. The purge gap prevents information leakage across train/test boundaries.

## `CW-TIME-SERIES-ML-005` — TA-Lib edge case sanitization
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

Always replace infinite values with NaN and call dropna before ML model training when using TA-Lib technical indicators. RSI, MACD, ATR and other indicators produce inf values during division-by-zero edge cases, which corrupt gradient-based model training.

## `CW-TIME-SERIES-ML-006` — Fluent forecasting model interface
**From**: finance-bp-102--Darts · **Applicable to**: time-series-ml

Implement fit() returning self and predict() on ForecastingModel subclasses to support method chaining. This fluent interface pattern is expected by users for idiomatic usage like model.fit(series).predict(n_periods).

## `CW-TIME-SERIES-ML-007` — Zipline bundle signature contract
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

When implementing Zipline bundle ingest functions, the function must accept exactly 9 parameters in the specified order: environ, asset_db_writer, minute_bar_writer, daily_bar_writer, adjustment_writer, calendar, start_session, end_session, cache. This contract is enforced by Zipline's ingestion pipeline.

## `CW-TIME-SERIES-ML-008` — Calendar minutes_per_day alignment
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

When configuring trading calendars for backtesting, set minutes_per_day to match the total trading minutes including extended hours (960 for regular NYSE, 1600 for extended hours starting 4:00 AM). This ensures minute bar alignment with actual trading times in the backtest.

## `CW-TIME-SERIES-ML-009` — Deterministic series detection
**From**: finance-bp-121--machine-learning-for-trading · **Applicable to**: time-series-ml

A TimeSeries is deterministic when n_samples equals 1, otherwise probabilistic. This distinction matters for methods like to_json and gaps detection which execute differently depending on whether the series contains probabilistic predictions or point estimates.

## `CW-TIME-SERIES-ML-010` — Minimum training sample enforcement
**From**: finance-bp-102--Darts · **Applicable to**: time-series-ml

Enforce min_train_series_length at fit time to prevent underfitting with insufficient historical data. Models should raise ValueError with clear messaging when training series length is below the model's minimum requirement, preventing silent poor forecasts.

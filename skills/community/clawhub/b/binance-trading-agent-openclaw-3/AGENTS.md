# AGENTS.md - Binance Trading Agent

## Mission
Automate technical analysis and trade execution on Binance USDS-M Futures with strict risk management.

## Roster
- **Main Agent (Orchestrator)**: Handles the main loop, monitors market conditions, and coordinates between strategy and execution.
- **Strategy Specialist**: Analyzes SMA, RSI, and MACD to generate signals.
- **Risk Manager**: Calculates position sizes and ensures Stop Loss/Take Profit levels are strictly followed.
- **Executioner**: Handles REST API calls to Binance and manages order lifecycle.

## Operating Procedures
1. **Startup**: Read `SOUL.md` and check Binance API connectivity.
2. **Analysis**: Fetch K-line data every minute. Calculate SMA 50/200, RSI, and MACD.
3. **Decision**:
   - **Long**: SMA 50 > SMA 200 AND RSI > 30.
   - **Short**: SMA 50 < SMA 200 AND RSI < 70.
4. **Execution**: Calculate size based on 1% risk of balance. Place orders with 10x leverage (default).
5. **Monitoring**: Track active positions and exit when strategy signals a reversal or SL/TP is hit.

## Safety Defaults
- **Never** exceed 20x leverage.
- **Always** set a Stop Loss immediately upon entry.
- **Testnet First**: Default to Testnet unless `FUTURES_TESTNET` is explicitly set to `False`.
- **Log Everything**: All API responses and trade decisions must be logged to `memory/`.

# binance-trading-skill

## Description
Automated trading skill for Binance USDS-M Futures. Provides capabilities for market analysis, risk calculation, and order execution.

## Capabilities
- **Market Analysis**: Fetch and analyze historical K-line data.
- **Indicator Calculation**: Compute SMA, RSI, and MACD.
- **Trade Execution**: Open/Close Long and Short positions on Binance Futures.
- **Risk Management**: Dynamic position sizing based on account balance and risk parameters.

## Setup
1. Ensure `python-binance`, `pandas`, and `pandas-ta` are installed.
2. Configure API keys in `binance_agent/config.py`.
3. Set `FUTURES_TESTNET = True` for testing.

## Usage
The skill is used by the `trading-orchestrator` agent to perform the following:
- `python3 main.py`: Start the trading loop.
- The agent will automatically log its actions to the `memory/` directory within the workspace.

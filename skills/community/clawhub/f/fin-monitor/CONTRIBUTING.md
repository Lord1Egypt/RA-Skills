# Contributing to finance-monitor

Thank you for your interest in contributing to finance-monitor!

## Project Overview

finance-monitor fetches 18 financial indicators (US10YTIP, US10Y, GC, CL, SPY, SPX, QQQ, NDX, DXY, VIX, AAPL, MSFT, NVDA, AMZN, META, UNH, KO, BRK.B) from CNBC and stores them in a SQLite database.

## How to Contribute

### Reporting Issues

Found a bug or have a feature request? Please open an issue with:
- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Your environment (OS, Python version)

### Pull Requests

1. **Fork the repository** and create a feature branch from `main`.
2. **Write tests** for any new functionality.
3. **Follow existing code style** — this project uses Python 3 stdlib only.
4. **Test your changes**:
   ```bash
   python scripts/fetch_data.py --db-path ./test.db
   ```
5. **Commit with a clear message** describing what you changed and why.
6. **Open a PR** against `main`.

### Code Style

- Use meaningful variable and function names
- Add docstrings for public functions
- Handle errors explicitly — don't silently swallow exceptions
- Respect rate limits when fetching external data

### Adding New Indicators

To add a new indicator, edit `scripts/fetch_data.py`:
1. Add an entry to the `INDICATORS` list with `code`, `name_cn`, and `url` (CNBC quote page).
2. Ensure the parsing logic handles the new symbol's HTML structure.
3. Test by running: `python scripts/fetch_data.py --db-path ./test.db`

### Database Schema

The `indicators` table stores price data. If you add new fields, update the `CREATE TABLE` statement and the INSERT query in `init_db()`.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

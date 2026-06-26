# AGENTS.md - Pocket Options Bot

This file provides guidelines for AI coding agents working on the Pocket Options Bot.

## Project Overview

**Pocket Options Bot** - AI-powered binary options trading bot with Martingale strategy and recursive learning.

- **Language:** TypeScript
- **Runtime:** Node.js 18+
- **License:** MIT
- **Strategy:** Binary options trading with technical indicators

## Build / Test / Lint Commands

### Development
```bash
# Run in development mode
cd ~/Projects/pocket-options-bot
npm run dev

# Build TypeScript
npm run build

# Run production build
npm run start
```

### Testing
```bash
# Run all tests
npm test

# Run single test
npm test -- test-name-here
```

### Linting and Formatting
```bash
# Check linting
npm run lint

# Fix linting issues
npx eslint src --ext .ts --fix

# Format code
npm run format
```

## Code Style Guidelines

### TypeScript
- Use strict TypeScript configuration
- Prefer interfaces over types for object shapes
- Use explicit return types on functions
- Avoid `any` type - use `unknown` with type guards

### Naming Conventions
- **Files:** `kebab-case.ts` (e.g., `pocket-options-client.ts`)
- **Classes:** `PascalCase` (e.g., `PocketOptionsClient`)
- **Interfaces:** `PascalCase` with descriptive names
- **Functions/Variables:** `camelCase`
- **Constants:** `SCREAMING_SNAKE_CASE`

### Error Handling
- Use custom error classes for domain-specific errors
- Always handle Promise rejections
- Log errors with context using Winston logger

```typescript
// Good
import { logger } from '../utils/logger';

try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  logger.error('Operation failed', { error, context: 'trading' });
  throw new TradingError('Failed to execute trade', error);
}
```

### Project Structure
```
src/
├── browser/          # Browser automation (Puppeteer/Playwright)
├── core/            # Core trading logic
│   ├── martingale.ts
│   ├── risk-manager.ts
│   └── pnl-tracker.ts
├── indicators/      # Technical indicators
├── strategy/        # Trading strategies
├── database/        # Data persistence
├── market/          # Market data handling
├── learning/        # ML/recursive learning
├── utils/           # Utilities
└── types.ts         # Global types
```

## Configuration

### Environment Variables
```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings
POCKET_OPTIONS_EMAIL=your@email.com
POCKET_OPTIONS_PASSWORD=your_password
TRADING_MODE=demo  # or 'live'
```

### Config File
See `config.yaml` for trading parameters:
- Martingale settings
- Risk limits
- Indicator parameters
- Stealth/humanization settings

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file or credentials
- Uses stealth browser techniques (see `src/browser/stealth.ts`)
- Demo mode recommended for testing
- Real money trading involves significant risk

## Dependencies

Key packages:
- `technicalindicators` - Technical analysis
- `winston` - Logging
- `dotenv` - Environment config

## Documentation

- `README.md` - Overview and setup
- `docs/ANALYSIS.md` - Technical analysis
- `docs/IMPLEMENTATION_SUMMARY.md` - Architecture
- `docs/STEALTH_AND_HUMANIZATION.md` - Anti-detection
- `docs/NEXT_STEPS.md` - Future improvements

## Testing Strategy

- Unit tests for indicators and strategies
- Integration tests for browser automation
- Backtesting framework for strategy validation

## Related Projects

This bot is isolated from other projects but shares concepts with:
- `solana-arbitrage/` - Another trading bot (different strategy/asset class)

---

**Note:** This is a trading bot that involves financial risk. Always test thoroughly in demo mode before live trading.

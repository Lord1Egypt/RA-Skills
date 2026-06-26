# ClawPurse

Local Timpi/NTMPI wallet for agentic AI (including OpenClaw), automation scripts, and individual users on the Neutaro chain.

[![Tests](https://github.com/mhue-ai/ClawPurse/workflows/CI/badge.svg)](https://github.com/mhue-ai/ClawPurse/actions)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)

## Features

- 🔐 **Encrypted local keystore** – AES-256-GCM encryption with scrypt key derivation
- 💰 **Send/receive NTMPI** – Full wallet functionality on Neutaro blockchain
- 🛡️ **Configurable guardrails** – Max send limits, confirmation thresholds, destination allowlists
- 📝 **Transaction receipts** – Local audit trail for all sends
- ✅ **Destination allowlists** – Control which addresses can receive funds
- 🔌 **Programmatic API** – Import and use in scripts and other applications
- 🤖 **Agent-ready** – Designed for AI agents, automation, and human operators alike
- 🏦 **Staking (v2.0)** – Delegate, undelegate, and redelegate to validators
- 🔒 **Enhanced Security** – Comprehensive input validation and password strength enforcement
- 🧪 **Test Coverage** – 60+ automated tests ensuring reliability

## Installation

```bash
# From the ClawPurse directory
npm install
npm run build
npm link  # Makes 'clawpurse' available globally
```

## Quick Start

```bash
# Create a new wallet (you'll be prompted to choose guardrails)
clawpurse init --password <your-password>

# Check chain status
clawpurse status

# View your address
clawpurse address

# Check balance
clawpurse balance --password <your-password>

# Receive tokens
clawpurse receive

# Send tokens
clawpurse send <to-address> <amount> --password <your-password>

# View transaction history
clawpurse history
```

## Guardrail Wizard

During `clawpurse init` (and `import`), the CLI pauses to explain the destination allowlist and asks you to choose:

- **Enforce** – Blocks sends to unknown addresses unless you pass `--override-allowlist`
- **Allow** – Lets you send anywhere, but still logs entries for documentation

Pre-set the choice with `--allowlist-mode enforce|allow` or rerun the wizard via `clawpurse allowlist init`.

## Commands

### Wallet Management

| Command | Description |
|---------|-------------|
| `init` | Create a new wallet (runs guardrail wizard) |
| `import` | Import wallet from mnemonic |
| `address` | Display wallet address |
| `balance` | Check wallet balance |
| `receive` | Show receive address |
| `export --yes` | Export mnemonic (dangerous!) |

### Transactions

| Command | Description |
|---------|-------------|
| `send <to> <amount>` | Send NTMPI tokens |
| `history` | View transaction history |

### Network

| Command | Description |
|---------|-------------|
| `status` | Check chain connection |

### Allowlist Management

| Command | Description |
|---------|-------------|
| `allowlist init` | Run guardrail wizard / create config |
| `allowlist list` | Show trusted destinations + default policy |
| `allowlist add <addr>` | Add/update a destination |
| `allowlist remove <addr>` | Remove a destination |

### Staking (v2.0)

| Command | Description |
|---------|-------------|
| `stake <validator> <amount>` | Delegate tokens to a validator |
| `unstake <validator> <amount>` | Undelegate tokens (22-day unbonding) |
| `redelegate <from> <to> <amount>` | Move stake between validators |
| `delegations` | Show current delegations |
| `validators` | List active validators |
| `unbonding` | Show pending unbonding delegations |

**Staking Examples:**
```bash
# List validators
clawpurse validators

# Stake 1000 NTMPI
clawpurse stake neutarovaloper1abc... 1000 --password <pass>

# Check your delegations
clawpurse delegations

# Unstake (requires --yes, 22-day unbonding period)
clawpurse unstake neutarovaloper1abc... 500 --password <pass> --yes

# Move stake to different validator (no unbonding)
clawpurse redelegate neutarovaloper1abc... neutarovaloper1xyz... 500 --password <pass>
```

## Options

| Flag | Description |
|------|-------------|
| `--password <pass>` | Wallet password (or set `CLAWPURSE_PASSWORD` env var) |
| `--keystore <path>` | Custom keystore location (default: `~/.clawpurse/keystore.enc`) |
| `--memo <text>` | Add memo to transaction |
| `--yes` | Skip confirmations |
| `--allowlist <path>` | Custom allowlist file (default: `~/.clawpurse/allowlist.json`) |
| `--allowlist-mode <enforce\|allow>` | Skip guardrail prompt during init/import |
| `--override-allowlist` | Bypass allowlist checks for one transaction |

## Allowlist Add Options

| Flag | Description |
|------|-------------|
| `--name "Label"` | Human-readable name for the destination |
| `--max <amount>` | Maximum send amount in NTMPI |
| `--memo-required` | Require memo when sending to this address |
| `--notes "text"` | Optional notes for documentation |

## Safety Features

| Feature | Default | Description |
|---------|---------|-------------|
| Max send limit | 1000 NTMPI | Hard cap per transaction |
| Confirmation threshold | 100 NTMPI | Requires `--yes` above this |
| Address validation | Enabled | Verifies `neutaro1` prefix |
| Encrypted storage | AES-256-GCM | Scrypt key derivation |
| Allowlist | Optional | Block or warn on unknown destinations |
| **Password strength** | **12+ chars** | **Enforces strong passwords** |
| **Input validation** | **Enabled** | **Validates all inputs before processing** |

## Enhanced Security (v2.0.1)

ClawPurse now includes comprehensive security enhancements:

### Password Requirements
- **Minimum 12 characters** required
- **Common passwords rejected** (e.g., "password123456")
- Clear error messages guide you to stronger passwords

### Input Validation
All inputs are validated before processing:
- **Addresses**: Must have correct `neutaro1` prefix, valid length, and proper format
- **Amounts**: Must be positive numbers with max 6 decimal places
- **Memos**: Max 256 bytes, no control characters
- **Mnemonics**: Valid BIP39 word count and format

### Error Messages
- Specific, helpful error messages
- No sensitive data in errors
- Clear guidance on how to fix issues

## Programmatic Usage

```typescript
import {
  generateWallet,
  saveKeystore,
  loadKeystore,
  getBalance,
  send,
} from 'clawpurse';

// Generate and save a wallet
const { mnemonic, address } = await generateWallet();
await saveKeystore(mnemonic, address, 'my-secure-password-123');

// Load and use
const { wallet, address } = await loadKeystore('my-secure-password-123');
const balance = await getBalance(address);

// Send tokens
const result = await send(wallet, address, 'neutaro1...', '10.5', {
  memo: 'Payment for services',
  skipConfirmation: true,
});
console.log(`TxHash: ${result.txHash}`);
```

### Staking API (v2.0)

```typescript
import {
  loadKeystore,
  delegate,
  undelegate,
  getDelegations,
  getValidators,
} from 'clawpurse';

// Load wallet
const { wallet, address } = await loadKeystore('my-secure-password-123');

// List validators
const validators = await getValidators();
console.log(validators.map(v => `${v.moniker} - ${v.commission}`));

// Stake tokens
const stakeResult = await delegate(wallet, address, 'neutarovaloper1...', '1000');
console.log(`Staked! TxHash: ${stakeResult.txHash}`);

// Check delegations
const { delegations, totalStakedDisplay } = await getDelegations(address);
console.log(`Total staked: ${totalStakedDisplay}`);

// Unstake (22-day unbonding period)
const unstakeResult = await undelegate(wallet, address, 'neutarovaloper1...', '500');
console.log(`Unstaking started: ${unstakeResult.txHash}`);
```

### Security Utilities API (v2.0.1)

```typescript
import {
  validatePassword,
  validateAddress,
  validateAmount,
  validateMemo,
  validateMnemonic,
} from 'clawpurse';

// Validate inputs before use
const passwordCheck = validatePassword('user-input-password');
if (!passwordCheck.valid) {
  console.error(`Weak password: ${passwordCheck.reason}`);
}

const addressCheck = validateAddress('neutaro1...');
if (!addressCheck.valid) {
  console.error(`Invalid address: ${addressCheck.reason}`);
}

const amountCheck = validateAmount('10.5');
if (!amountCheck.valid) {
  console.error(`Invalid amount: ${amountCheck.reason}`);
}
```

## Testing

ClawPurse includes comprehensive test coverage:

```bash
# Run all tests
npm test

# Run specific test suites
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests
npm run test:e2e          # End-to-end CLI tests

# Watch mode for development
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Test Coverage
- ✅ **60+ automated tests** across unit, integration, and E2E
- ✅ **Security validation** tests for all input types
- ✅ **Cryptography tests** for wallet generation and encryption
- ✅ **Transaction tests** for sending and staking
- ✅ **CI/CD pipeline** runs tests on every commit

See [TEST_PLAN.md](./TEST_PLAN.md) for complete testing strategy.

## Configuration

Edit `src/config.ts` to customize:

```typescript
export const NEUTARO_CONFIG = {
  rpcEndpoint: 'https://rpc2.neutaro.io',
  // ...
};

export const KEYSTORE_CONFIG = {
  maxSendAmount: 1000_000000,      // 1000 NTMPI
  requireConfirmAbove: 100_000000, // 100 NTMPI
  // ...
};
```

## Documentation

### Getting Started
- **[README.md](./README.md)** – This file - complete feature overview
- **[QUICKSTART.md](./QUICKSTART.md)** – Quick start guide for new users

### User Guides
- **[OPERATOR-GUIDE.md](./docs/OPERATOR-GUIDE.md)** – Complete setup and usage guide
- **[ALLOWLIST.md](./docs/ALLOWLIST.md)** – Destination allowlist configuration
- **[HOWTOGETTIMPI.md](./HOWTOGETTIMPI.md)** – How to acquire NTMPI tokens

### Security & Trust
- **[TRUST-MODEL.md](./docs/TRUST-MODEL.md)** – Security model and transaction verification

### Developer Documentation
- **[SKILL.md](./SKILL.md)** – AI agent integration guide (OpenClaw)
- **[TEST_PLAN.md](./TEST_PLAN.md)** – Comprehensive testing strategy
- **[tests/README.md](./tests/README.md)** – Testing guide for developers

### Enhancement Documentation
- **[IMPROVEMENTS.md](./IMPROVEMENTS.md)** – Detailed changelog of v2.0.1 enhancements
- **[SUMMARY.md](./SUMMARY.md)** – Executive summary of all enhancements

## Security Notes

### Password Security
- ✅ **Use a strong password** – Minimum 12 characters required
- ✅ **Avoid common passwords** – System rejects weak passwords
- ✅ **Never reuse passwords** – Use a unique password for ClawPurse

### Wallet Security
- ✅ **Backup your mnemonic** – It's only shown once during `init`
- ✅ **Keystore permissions** – File is created with mode 0600
- ✅ **Never share** your mnemonic or keystore file
- ✅ **Store backups securely** – Use encrypted storage for mnemonic backups

### Transaction Security
- ✅ **Enable allowlist enforcement** – Prevents accidental sends to wrong addresses
- ✅ **Verify addresses** – System validates address format before sending
- ✅ **Double-check amounts** – Confirmation required for large transactions
- ✅ **Use memos** – Add context to transactions for better audit trails

### Development Security
- ✅ **Run tests** – Ensure all tests pass before deploying
- ✅ **Review code** – Check for security issues before commits
- ✅ **Update dependencies** – Keep packages up to date
- ✅ **Run security audits** – Use `npm run security-check`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAWPURSE_PASSWORD` | Wallet password |
| `CLAWPURSE_MNEMONIC` | Mnemonic for import |

## Files

| Path | Purpose |
|------|---------|
| `~/.clawpurse/keystore.enc` | Encrypted wallet (mode 0600) |
| `~/.clawpurse/receipts.json` | Transaction receipts |
| `~/.clawpurse/allowlist.json` | Trusted destinations config |

## Verifying Transactions

For receiving nodes to verify a payment:

1. Obtain tx hash from sender
2. Query chain: `curl "https://api2.neutaro.io/cosmos/tx/v1beta1/txs/<TX_HASH>"`
3. Confirm `from_address`, `to_address`, and `amount` match expectations
4. Optional: compare against sender's receipt

See [TRUST-MODEL.md](./docs/TRUST-MODEL.md) for detailed verification procedures.

## Development

### Building from Source
```bash
npm install
npm run build
```

### Running Tests
```bash
# Type check
npm run type-check

# Lint code
npm run lint
npm run lint:fix  # Auto-fix issues

# Run tests
npm test
npm run test:coverage

# Security audit
npm run security-check
```

### CI/CD
ClawPurse uses GitHub Actions for continuous integration:
- ✅ Automated testing on every push
- ✅ Multi-Node version testing (18, 20, 22)
- ✅ Security audits
- ✅ Build verification
- ✅ Coverage reporting

See [.github/workflows/ci.yml](./.github/workflows/ci.yml) for pipeline configuration.

## Version History

### v2.0.1 (Enhanced) - 2026-02-14
- ✨ **Security enhancements**: Password strength validation, comprehensive input validation
- ✨ **Test infrastructure**: 60+ automated tests, Jest configuration, CI/CD pipeline
- ✨ **Documentation**: 6 comprehensive guides, testing documentation
- ✨ **Website updates**: SKILL.md prominently featured, AI integration section
- 📝 **API additions**: Security validation utilities

### v2.0.0 - Staking Support
- ✨ **Staking functionality**: Delegate, undelegate, redelegate
- ✨ **Validator discovery**: List and filter validators
- ✨ **Unbonding tracking**: Monitor 22-day unbonding periods
- 📝 **Staking API**: Full programmatic staking support

### v1.0.0 - Initial Release
- 🔐 Encrypted local keystore
- 💰 Send/receive functionality
- 🛡️ Guardrails and allowlists
- 📝 Transaction receipts
- 🤖 Programmatic API

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npm test`
5. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/mhue-ai/ClawPurse/issues)
- **Documentation**: See docs/ folder
- **Website**: [clawpurse.ai](https://clawpurse.ai)
- **Timpi Drip**: [drip.clawpurse.ai](https://drip.clawpurse.ai)

## License

ISC

## Tip the Builders

If ClawPurse is saving your node hours of ops time, tip the builders a Timpi coffee:

```
neutaro1e8xal8tqdegu4w48z3fphemd3hc07gech3pfek
```

Memo optional — just let us know what you shipped!

---

**Maintained by the Mhue family** • Timpi / NTMPI wallet for Agentic AI & Automation • v2.0.1

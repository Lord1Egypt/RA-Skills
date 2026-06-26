# ClawPurse Test Suite

Comprehensive testing infrastructure for ClawPurse cryptocurrency wallet.

## Quick Start

```bash
# Install dependencies
npm install

# Run all tests
npm test

# Run specific test suites
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:e2e          # CLI end-to-end tests
npm run test:all          # All test suites

# Watch mode for development
npm run test:watch

# Generate coverage report
npm run test:coverage
```

## Test Structure

```
tests/
├── setup.ts                 # Common test utilities and mocks
├── unit/                    # Unit tests
│   ├── wallet.test.ts       # Wallet & crypto operations
│   ├── transaction.test.ts  # Transaction logic
│   └── guardrails.test.ts   # Guardrails & allowlist
├── integration/             # Integration tests
│   └── blockchain.test.ts   # Blockchain operations
└── e2e/                     # End-to-end tests
    └── cli-tests.sh         # CLI command tests
```

## Test Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Crypto operations | 90% |
| Transaction logic | 85% |
| Guardrails | 85% |
| CLI commands | 75% |
| **Overall** | **80%** |

## Running Tests

### Unit Tests

Unit tests focus on individual functions and modules:

```bash
npm run test:unit
```

These tests:
- Run quickly (< 5 seconds)
- Don't require network access
- Use mocked dependencies
- Test core logic in isolation

### Integration Tests

Integration tests verify blockchain interactions:

```bash
npm run test:integration
```

These tests:
- May be slower (network calls)
- Use mocked RPC responses by default
- Can run against testnet with environment variables
- Test end-to-end workflows

### End-to-End CLI Tests

CLI tests verify the command-line interface:

```bash
npm run test:e2e
```

These tests:
- Use bash script for realistic scenarios
- Test actual CLI commands
- Verify file operations
- Test error handling

## Test Configuration

### Jest Configuration

Tests are configured via `jest.config.js`:

- TypeScript support via ts-jest
- 30-second timeout for slow operations
- Coverage thresholds enforced
- Custom setup file for common utilities

### Environment Variables

```bash
# Use testnet for integration tests
export CLAWPURSE_TEST_NETWORK=testnet

# Custom RPC endpoint
export CLAWPURSE_TEST_RPC=https://rpc-testnet.neutaro.io

# Enable verbose logging
export CLAWPURSE_TEST_VERBOSE=true
```

## Writing Tests

### Unit Test Example

```typescript
import { describe, it, expect } from '@jest/globals';
import { validateAmount } from '@/utils';

describe('Amount Validation', () => {
  it('should accept valid amounts', () => {
    expect(validateAmount('100')).toBe(true);
    expect(validateAmount('0.5')).toBe(true);
  });

  it('should reject negative amounts', () => {
    expect(validateAmount('-100')).toBe(false);
  });
});
```

### Integration Test Example

```typescript
import { getBalance } from '@/blockchain';
import { TEST_ADDRESS_1, mockFetch, MOCK_BALANCE_RESPONSE } from '../setup';

describe('Balance Queries', () => {
  beforeAll(() => {
    mockFetch({
      'https://api2.neutaro.io/...': MOCK_BALANCE_RESPONSE
    });
  });

  it('should query balance', async () => {
    const balance = await getBalance(TEST_ADDRESS_1);
    expect(balance).toBeDefined();
  });
});
```

### CLI Test Example

```bash
assert_success \
  "clawpurse init --password test123" \
  "Initialize wallet"

assert_failure \
  "clawpurse send invalid-address 10" \
  "Reject invalid address"
```

## Continuous Integration

Tests run automatically on:
- Every push to `main` or `develop`
- Every pull request
- Manual workflow dispatch

GitHub Actions workflow (`.github/workflows/ci.yml`):
- ✅ Linting & type checking
- ✅ Unit tests (Node 18, 20, 22)
- ✅ Integration tests
- ✅ E2E CLI tests
- ✅ Security audit
- ✅ Coverage reporting

## Coverage Reports

### Local Coverage

```bash
npm run test:coverage
open coverage/lcov-report/index.html
```

### CI Coverage

Coverage reports are automatically:
- Generated on every CI run
- Uploaded to Codecov
- Displayed in pull requests
- Tracked over time

## Test Data

### Test Mnemonics

**⚠️ NEVER USE ON MAINNET ⚠️**

```
abandon abandon abandon abandon abandon abandon 
abandon abandon abandon abandon abandon abandon 
abandon abandon abandon abandon abandon abandon 
abandon abandon abandon abandon abandon art
```

### Test Addresses

```
neutaro1test1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtest1
neutaro1test2qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtest2
```

### Test Validators

```
neutarovaloper1test1qqqqqqqqqqqqqqqqqqqqqqqqqqqtestval1
neutarovaloper1test2qqqqqqqqqqqqqqqqqqqqqqqqqqqtestval2
```

## Debugging Tests

### Run Single Test

```bash
npm test -- wallet.test.ts
npm test -- -t "should validate amounts"
```

### Enable Debug Output

```bash
DEBUG=clawpurse:* npm test
```

### Run Tests in Node Debugger

```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

## Common Issues

### Tests Timeout

Increase timeout in `jest.config.js`:
```javascript
testTimeout: 60000  // 60 seconds
```

### Network Tests Fail

Use mocked responses or skip network tests:
```bash
npm run test:unit  # Skip integration tests
```

### Permission Errors

Ensure test files have correct permissions:
```bash
chmod -R 755 tests/
```

## Best Practices

### DO ✅

- Write tests before fixing bugs
- Test edge cases and error paths
- Use descriptive test names
- Mock external dependencies
- Clean up test files in `afterEach`
- Use test utilities from `setup.ts`

### DON'T ❌

- Commit hardcoded secrets
- Use mainnet data in tests
- Skip error handling tests
- Leave console.log in tests
- Make tests depend on each other
- Use real wallets for testing

## Contributing Tests

1. Write tests for new features
2. Ensure all tests pass locally
3. Add test cases for bug fixes
4. Update test documentation
5. Aim for 80%+ coverage

## Security Testing

### Crypto Operations

- Test encryption/decryption
- Verify key derivation
- Test memory wiping
- Validate input sanitization

### Transaction Security

- Test signature verification
- Validate amount parsing
- Test guardrail enforcement
- Verify allowlist checks

### File Security

- Test file permissions
- Verify secure deletion
- Test path traversal protection
- Validate input sanitization

## Performance Testing

Run performance benchmarks:

```bash
npm run test:performance
```

Benchmarks include:
- Wallet generation time
- Encryption/decryption speed
- Transaction signing speed
- Balance query latency

## Troubleshooting

### Jest Out of Memory

```bash
NODE_OPTIONS=--max_old_space_size=4096 npm test
```

### TypeScript Errors

```bash
npm run type-check
```

### Coverage Not Generated

```bash
rm -rf coverage/
npm run test:coverage
```

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
- [Neutaro Testnet](https://testnet.neutaro.io)

## License

Same as ClawPurse main project (ISC/MIT)

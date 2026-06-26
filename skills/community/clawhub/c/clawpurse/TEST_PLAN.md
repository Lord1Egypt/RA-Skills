# ClawPurse Test Plan

## Overview
This document outlines the comprehensive testing strategy for ClawPurse, a local cryptocurrency wallet for the Neutaro blockchain designed for AI agents and individual users.

## Test Objectives
- Ensure security of cryptographic operations and key management
- Validate transaction functionality and guardrails
- Verify staking operations work correctly
- Test allowlist enforcement mechanisms
- Ensure CLI commands work as expected
- Validate API functionality for programmatic usage
- Test error handling and edge cases

## Test Scope

### In Scope
- Unit tests for all core functionality
- Integration tests for blockchain operations
- End-to-end CLI tests
- Security tests for encryption and key management
- API tests for programmatic usage
- Performance tests for key operations
- Staking functionality tests (v2.0)

### Out of Scope
- Neutaro blockchain node testing
- Network infrastructure testing
- Third-party dependency testing (except integration points)

## Test Environment

### Test Networks
- **Neutaro Testnet**: For integration testing
- **Local Mock**: For unit testing without network dependency
- **Mainnet**: Manual smoke testing only (with extreme caution)

### Test Data
- Test mnemonics (never use on mainnet)
- Test addresses with known balances on testnet
- Mock validator data for staking tests

## Test Categories

### 1. Unit Tests

#### 1.1 Cryptography & Key Management
- **Wallet Generation**
  - Generate valid mnemonic (24 words)
  - Derive correct address from mnemonic
  - Generate different addresses for different mnemonics
  - Validate mnemonic checksums

- **Keystore Encryption**
  - Encrypt and decrypt successfully with correct password
  - Fail decryption with incorrect password
  - Use proper AES-256-GCM encryption
  - Apply scrypt key derivation correctly
  - Set correct file permissions (0600)

- **Memory Security**
  - Wipe sensitive data after use
  - No sensitive data in error messages
  - No sensitive data in logs

#### 1.2 Address Validation
- Validate correct neutaro1 prefix
- Reject invalid prefixes
- Validate address length
- Reject malformed addresses
- Handle empty/null addresses

#### 1.3 Amount Validation
- Accept valid positive amounts
- Reject negative amounts
- Reject zero amounts
- Handle decimal precision correctly
- Reject non-numeric values
- Handle very large numbers
- Handle very small numbers

#### 1.4 Configuration Management
- Load default configuration
- Override with custom config
- Validate configuration values
- Handle missing config files
- Merge configs correctly

### 2. Integration Tests

#### 2.1 Blockchain Connectivity
- Connect to RPC endpoint
- Retrieve chain status
- Query account balance
- Handle network errors gracefully
- Implement retry logic
- Failover to backup RPC endpoints

#### 2.2 Transaction Operations
- **Send Transactions**
  - Send valid transaction
  - Receive transaction confirmation
  - Handle insufficient balance
  - Handle invalid recipient
  - Add memo to transaction
  - Handle gas estimation
  - Sign transaction correctly
  - Broadcast transaction

- **Transaction Receipts**
  - Generate receipt after send
  - Store receipt in local file
  - Include all required fields
  - Format timestamps correctly

#### 2.3 Balance Queries
- Query balance for valid address
- Handle zero balance
- Handle non-existent accounts
- Cache balance appropriately
- Refresh on demand

#### 2.4 Staking Operations (v2.0)
- **Delegation**
  - Delegate to validator
  - Handle insufficient balance
  - Validate validator address
  - Generate delegation receipt

- **Undelegation**
  - Undelegate from validator
  - Handle 22-day unbonding period
  - Track unbonding status
  - Complete unbonding

- **Redelegation**
  - Move stake between validators
  - No unbonding period
  - Validate both validator addresses

- **Queries**
  - List all validators
  - Get validator details
  - Get current delegations
  - Get unbonding delegations
  - Calculate total staked

### 3. CLI Tests

#### 3.1 Wallet Management Commands
```bash
# Init
clawpurse init --password test123
clawpurse init --password test123 --allowlist-mode enforce
clawpurse init --password test123 --allowlist-mode allow

# Import
clawpurse import --password test123
echo "MNEMONIC" | clawpurse import --password test123

# Address
clawpurse address

# Balance
clawpurse balance --password test123

# Export (dangerous)
clawpurse export --yes --password test123

# Receive
clawpurse receive
```

#### 3.2 Transaction Commands
```bash
# Send
clawpurse send neutaro1... 10 --password test123
clawpurse send neutaro1... 10 --password test123 --memo "test"
clawpurse send neutaro1... 1000 --password test123 --yes

# History
clawpurse history
```

#### 3.3 Allowlist Commands
```bash
# Init
clawpurse allowlist init

# List
clawpurse allowlist list

# Add
clawpurse allowlist add neutaro1... --name "Test" --max 100
clawpurse allowlist add neutaro1... --memo-required

# Remove
clawpurse allowlist remove neutaro1...
```

#### 3.4 Staking Commands (v2.0)
```bash
# Validators
clawpurse validators

# Delegations
clawpurse delegations

# Stake
clawpurse stake neutarovaloper1... 100 --password test123

# Unstake
clawpurse unstake neutarovaloper1... 50 --password test123 --yes

# Redelegate
clawpurse redelegate neutarovaloper1... neutarovaloper2... 50 --password test123

# Unbonding
clawpurse unbonding
```

#### 3.5 Status Commands
```bash
clawpurse status
```

### 4. Guardrail Tests

#### 4.1 Max Send Limit
- Block sends above max limit (default 1000 NTMPI)
- Allow sends below max limit
- Enforce custom max limits
- Override with flag when appropriate

#### 4.2 Confirmation Threshold
- Require --yes for amounts above threshold (default 100 NTMPI)
- Auto-confirm below threshold
- Handle user declining confirmation
- Enforce custom thresholds

#### 4.3 Allowlist Enforcement
- **Enforce Mode**
  - Block sends to unlisted addresses
  - Allow sends to listed addresses
  - Require --override-allowlist flag
  - Log all attempts

- **Allow Mode**
  - Permit sends to any address
  - Log warnings for unlisted addresses
  - Add to allowlist on first use (optional)

#### 4.4 Destination-Specific Rules
- Enforce max send per destination
- Require memo when configured
- Validate against destination rules

### 5. Security Tests

#### 5.1 Encryption Security
- Keystore file has 0600 permissions
- Password must be minimum length
- Encrypted data is not readable
- Different passwords produce different ciphertexts
- Tampering with ciphertext fails decryption

#### 5.2 Input Sanitization
- SQL injection attempts (if applicable)
- Command injection attempts
- Path traversal attempts
- XSS attempts (if web interface)
- Oversized inputs

#### 5.3 Authentication
- Cannot access wallet without password
- Password timeout/session management (if applicable)
- Rate limiting on password attempts

#### 5.4 Sensitive Data Handling
- No passwords in logs
- No mnemonics in logs
- No private keys in error messages
- Secure deletion of sensitive files

### 6. API Tests

#### 6.1 Programmatic Usage
```typescript
// Wallet operations
await generateWallet()
await saveKeystore(mnemonic, address, password)
await loadKeystore(password)

// Balance
await getBalance(address)

// Send
await send(wallet, fromAddress, toAddress, amount, options)

// Staking
await delegate(wallet, address, validator, amount)
await undelegate(wallet, address, validator, amount)
await redelegate(wallet, address, fromValidator, toValidator, amount)
await getDelegations(address)
await getValidators()
await getUnbondingDelegations(address)
```

#### 6.2 Error Handling
- Invalid parameters throw appropriate errors
- Network errors are handled gracefully
- Return values are typed correctly
- Async errors are catchable

### 7. Performance Tests

#### 7.1 Key Operations
- Wallet generation < 5 seconds
- Keystore encryption < 2 seconds
- Keystore decryption < 2 seconds
- Balance query < 3 seconds
- Transaction signing < 1 second
- Transaction broadcast < 5 seconds

#### 7.2 Concurrent Operations
- Multiple balance queries
- Rapid transaction signing
- Race conditions in file access

### 8. Edge Cases & Error Scenarios

#### 8.1 Network Issues
- RPC endpoint unreachable
- Timeout during transaction
- Partial network failure
- Invalid chain response

#### 8.2 File System Issues
- Keystore file corrupted
- Insufficient disk space
- Permission denied
- Keystore file missing

#### 8.3 Invalid States
- Empty wallet (zero balance)
- Pending transactions
- Chain reorganization
- Validator jailed/tombstoned

#### 8.4 Boundary Conditions
- Maximum amount
- Minimum amount
- Maximum memo length
- Very long addresses
- Special characters in inputs

### 9. Compatibility Tests

#### 9.1 Operating Systems
- Linux (Ubuntu, Debian, Fedora)
- macOS (Intel, Apple Silicon)
- Windows (via WSL)

#### 9.2 Node.js Versions
- Node.js 18.x
- Node.js 20.x
- Node.js 22.x

#### 9.3 Package Managers
- npm
- yarn
- pnpm

### 10. Regression Tests

- All previously fixed bugs
- Breaking changes from dependencies
- Configuration changes
- Network upgrades

## Test Data Requirements

### Test Wallets
```
# Test Wallet 1 (testnet only)
Mnemonic: [24 word mnemonic - testnet only]
Address: neutaro1test1...
Purpose: General testing

# Test Wallet 2 (testnet only)
Mnemonic: [24 word mnemonic - testnet only]
Address: neutaro1test2...
Purpose: Transaction recipient

# Test Wallet 3 (testnet only)
Mnemonic: [24 word mnemonic - testnet only]
Address: neutaro1test3...
Purpose: Staking tests
```

### Test Validators (testnet)
```
Validator 1: neutarovaloper1test1...
Validator 2: neutarovaloper1test2...
Validator 3: neutarovaloper1test3...
```

## Test Metrics & Success Criteria

### Code Coverage
- Minimum 80% overall coverage
- 90% coverage for crypto operations
- 85% coverage for transaction logic
- 75% coverage for CLI commands

### Performance Benchmarks
- All operations within specified time limits
- No memory leaks in long-running operations
- Graceful degradation under load

### Security Requirements
- Zero critical security vulnerabilities
- All sensitive data properly handled
- All inputs properly validated

### Reliability
- 99% test pass rate
- Zero data loss scenarios
- Proper error recovery

## Test Execution Schedule

### Pre-commit
- Unit tests
- Linting
- Type checking

### Continuous Integration
- All unit tests
- Integration tests (with mocked blockchain)
- CLI tests
- Security tests

### Pre-release
- Full integration tests on testnet
- Performance tests
- Manual smoke testing
- Security audit

### Post-release
- Monitoring
- User acceptance testing
- Bug reports

## Test Tools & Frameworks

### Testing Frameworks
- **Jest**: Primary test framework
- **Mocha/Chai**: Alternative if needed
- **Supertest**: API testing

### Mocking & Stubbing
- **Sinon**: Function mocking
- **Nock**: HTTP request mocking
- **Mock-fs**: File system mocking

### Coverage Tools
- **Istanbul/NYC**: Code coverage
- **Codecov**: Coverage reporting

### Performance Testing
- **Benchmark.js**: Performance benchmarks
- **Clinic.js**: Performance profiling

### Security Testing
- **npm audit**: Dependency vulnerabilities
- **Snyk**: Security scanning
- **eslint-plugin-security**: Static analysis

## Risk Assessment

### High Risk Areas
1. Private key handling and storage
2. Transaction signing
3. Amount validation
4. Network communication
5. Staking operations

### Mitigation Strategies
- Extensive testing of high-risk areas
- Multiple reviewers for crypto code
- External security audit
- Gradual rollout with testnet first

## Bug Tracking & Reporting

### Bug Severity Levels
- **Critical**: Security vulnerability, data loss
- **High**: Major functionality broken
- **Medium**: Feature not working as expected
- **Low**: Minor inconvenience, cosmetic issue

### Bug Report Template
```markdown
**Description**: Clear description of the issue
**Steps to Reproduce**: Numbered steps
**Expected Behavior**: What should happen
**Actual Behavior**: What actually happens
**Environment**: OS, Node version, ClawPurse version
**Logs**: Relevant log output
**Severity**: Critical/High/Medium/Low
```

## Test Deliverables

1. Test scripts (automated)
2. Test data sets
3. Test execution reports
4. Coverage reports
5. Performance benchmarks
6. Bug reports
7. Test documentation

## Sign-off Criteria

### Unit Tests
- ✅ All tests passing
- ✅ Coverage targets met
- ✅ No critical bugs

### Integration Tests
- ✅ All blockchain operations working
- ✅ Network resilience verified
- ✅ Staking operations functional

### Security Tests
- ✅ No security vulnerabilities
- ✅ Encryption verified
- ✅ Input validation complete

### Final Release
- ✅ All test categories complete
- ✅ Manual testing on testnet
- ✅ Documentation updated
- ✅ Known issues documented

---

**Version**: 1.0  
**Last Updated**: 2026-02-14  
**Maintainer**: ClawPurse Team

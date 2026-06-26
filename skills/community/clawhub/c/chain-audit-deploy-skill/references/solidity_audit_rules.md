# Solidity Audit Rules Reference

This document contains common vulnerability patterns and security checks for Solidity smart contracts. Load this reference when performing deep audit on Solidity contracts.

---

## Critical Severity

### 1. Reentrancy Attack
- **Description**: External calls can re-enter the calling contract before state updates complete, allowing an attacker to drain funds.
- **Detection**: Look for external calls (`.call{value:}`, `.transfer()`, `.send()`) followed by state changes. Check if the Checks-Effects-Interactions pattern is followed.
- **Slither detector**: `reentrancy-eth`, `reentrancy-no-eth`
- **Fix**: Use the Checks-Effects-Interactions pattern. Use `ReentrancyGuard` from OpenZeppelin. Update state before making external calls.

### 2. Unprotected selfdestruct
- **Description**: `selfdestruct` without proper access control allows anyone to destroy the contract.
- **Detection**: Search for `selfdestruct` or `SELFDESTRUCT` opcode without `onlyOwner` or similar modifiers.
- **Fix**: Remove `selfdestruct` or restrict to owner with timelock. Note: `selfdestruct` is deprecated in newer Solidity versions.

### 3. Arbitrary External Call
- **Description**: User-controlled `call` targets allow calling any contract/function.
- **Detection**: Check if `address.call()` target or calldata is derived from user input.
- **Slither detector**: `controlled-delegatecall`, `arbitrary-send-eth`
- **Fix**: Whitelist allowed call targets. Never use user-supplied addresses for delegatecall.

### 4. Uninitialized Proxy
- **Description**: Logic contract behind a proxy is not initialized, allowing attacker to call `initialize()` and take ownership.
- **Detection**: Check if `Initializable` pattern is used correctly, and `_disableInitializers()` is called in constructor.
- **Fix**: Call `_disableInitializers()` in the logic contract constructor. Use OpenZeppelin's upgradeable patterns.

---

## High Severity

### 5. Access Control Missing
- **Description**: Privileged functions (mint, pause, setFee, withdraw) lack proper access control.
- **Detection**: Check admin functions for `onlyOwner`, `onlyRole`, or similar modifiers.
- **Fix**: Use OpenZeppelin AccessControl or Ownable. Apply modifiers consistently to all privileged functions.

### 6. Unchecked External Call Return
- **Description**: Low-level `.call()` return values not checked, silently failing transfers.
- **Detection**: Look for `.call{value:}()` without checking the boolean return.
- **Slither detector**: `unchecked-lowlevel`
- **Fix**: Always check `(bool success, ) = addr.call{value: amount}(""); require(success);`

### 7. Integer Overflow/Underflow
- **Description**: Arithmetic operations wrap around in unchecked blocks or Solidity < 0.8.0.
- **Detection**: Check Solidity version. Look for `unchecked { }` blocks with arithmetic on user inputs.
- **Fix**: Use Solidity >= 0.8.0 (built-in overflow checks). Avoid `unchecked` for user-facing math.

### 8. Flash Loan Attack Vector
- **Description**: Contract relies on spot balances or prices that can be manipulated within a single transaction.
- **Detection**: Check for balance-based calculations, single-block price references, or token ratio computations.
- **Fix**: Use time-weighted average prices (TWAP). Implement minimum lock periods. Use oracle-based pricing.

### 9. Front-Running Vulnerability
- **Description**: Transactions can be observed in the mempool and front-run by MEV bots.
- **Detection**: Check for commit-reveal patterns, slippage protection, deadline parameters.
- **Fix**: Implement commit-reveal schemes. Add slippage tolerance. Use deadlines on swaps.

---

## Medium Severity

### 10. Centralization Risk
- **Description**: Single owner/admin can unilaterally change critical parameters or drain funds.
- **Detection**: Count privileged functions and check if a single address controls them all.
- **Fix**: Use multi-sig wallets. Implement timelocks for admin actions. Use DAO governance.

### 11. Missing Event Emission
- **Description**: State changes not emitted as events, making off-chain monitoring difficult.
- **Detection**: Check if `emit` is used after state-changing operations.
- **Fix**: Emit events for all significant state changes (transfers, parameter updates, ownership changes).

### 12. Unsafe ERC20 Interactions
- **Description**: Not all ERC20 tokens return `bool` on transfer. Some revert, some return false, some return nothing.
- **Detection**: Check for direct `.transfer()` / `.transferFrom()` calls on arbitrary ERC20 tokens.
- **Fix**: Use OpenZeppelin `SafeERC20` library with `safeTransfer` / `safeTransferFrom`.

### 13. Denial of Service (DoS)
- **Description**: Loops over unbounded arrays, push to storage arrays without limits, or external calls in loops.
- **Detection**: Look for loops with `.length` from storage, or loops containing external calls.
- **Fix**: Implement pagination. Limit array sizes. Use pull-over-push pattern for payments.

### 14. Timestamp Dependence
- **Description**: Using `block.timestamp` for critical logic; miners can manipulate by ~15 seconds.
- **Detection**: Check for `block.timestamp` usage in conditionals, deadlines, or randomness.
- **Fix**: Use reasonable time windows (> 15 min). Don't use for randomness. Use Chainlink VRF for random numbers.

---

## Low Severity

### 15. Floating Pragma
- **Description**: `pragma solidity ^0.8.0` allows compilation with any 0.8.x compiler.
- **Detection**: Check for `^` or `>=` in pragma statement.
- **Fix**: Lock to specific version: `pragma solidity 0.8.20;`

### 16. Missing Zero Address Check
- **Description**: Setting critical addresses (owner, treasury) without checking for address(0).
- **Detection**: Look for address setter functions without `require(addr != address(0))`.
- **Fix**: Add `require(newAddress != address(0), "Zero address")` for all address parameters.

### 17. Gas Optimization
- **Description**: Inefficient patterns that waste gas without security implications.
- **Detection**: Storage reads in loops, unnecessary SSTORE, unused variables.
- **Fix**: Cache storage values in memory. Use `immutable` for constructor-set values. Remove dead code.

---

## Info

### 18. Missing NatSpec Documentation
- **Description**: Functions lack `@notice`, `@param`, `@return` documentation.
- **Fix**: Add NatSpec comments to all public/external functions.

### 19. Unused Imports/Variables
- **Description**: Imported contracts or declared variables that are never used.
- **Fix**: Remove unused code to reduce deployment gas costs.

### 20. Magic Numbers
- **Description**: Hard-coded numeric values without named constants.
- **Fix**: Define named constants for all magic numbers.

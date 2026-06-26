# Solana Audit Rules Reference

This document contains common vulnerability patterns and security checks specific to Solana programs (both Anchor and native). Load this reference when performing deep audit on Solana contracts.

---

## Critical Severity

### 1. Missing Owner Check
- **Description**: Not verifying that an account is owned by the expected program. Attackers can pass accounts owned by different programs with crafted data.
- **Detection**:
  - **Native**: Check `account.owner == program_id` for all data accounts.
  - **Anchor**: `Account<'info, T>` auto-checks owner. Look for `UncheckedAccount` / `AccountInfo` without manual owner verification.
- **Fix**: Always verify account ownership. In Anchor, prefer typed accounts. For `UncheckedAccount`, add `/// CHECK:` and manual `assert!(account.owner == expected_program_id)`.

### 2. Missing Signer Check
- **Description**: Not verifying that the required authority has signed the transaction.
- **Detection**:
  - **Native**: Check `account_info.is_signer` for authority accounts.
  - **Anchor**: `Signer<'info>` type auto-validates. Check if authority accounts use `Signer` type.
- **Fix**: Use `Signer<'info>` in Anchor. In native, assert `is_signer == true` for all authority accounts.

### 3. PDA Seed Collision
- **Description**: If PDA seeds are not unique enough, different logical entities may map to the same PDA, allowing data corruption or unauthorized access.
- **Detection**: Check `find_program_address` / `seeds = [...]` definitions. Look for seeds that lack a discriminator or use only user-controlled values.
- **Fix**: Include unique discriminators in seeds (e.g., `b"user_account"` prefix). Include specific identifiers (user pubkey, mint address, etc.).

### 4. Arbitrary CPI (Cross-Program Invocation)
- **Description**: Invoking a program whose ID is passed as an account parameter without verifying it's the expected program.
- **Detection**: Check `invoke` / `invoke_signed` calls. Look for program accounts used as CPI targets without hardcoded ID verification.
- **Anchor**: Check `Program<'info, T>` usage — this validates the program ID automatically.
- **Fix**: Hardcode expected program IDs. In Anchor, use `Program<'info, T>` type. In native, assert `program_id == expected_id`.

### 5. Account Data Reinitialization
- **Description**: Writing initial data to an account without checking if it's already initialized, allowing an attacker to reset state.
- **Detection**: Check `init` / `init_if_needed` in Anchor. For native, check if there's an `is_initialized` flag checked before writing.
- **Fix**: In Anchor, prefer `init` over `init_if_needed`. In native, always check and set an `is_initialized` flag.

---

## High Severity

### 6. Account Close / Drain Vulnerability
- **Description**: When closing an account (transferring lamports to zero), if the account data is not zeroed, it can be "revived" within the same transaction.
- **Detection**: Check account close logic. Look for lamport transfers to zero without zeroing data.
- **Anchor**: `close = target` attribute handles this correctly.
- **Fix**: Zero all account data before transferring lamports. In Anchor, use the `close` attribute. In native, overwrite data with zeros.

### 7. Missing Rent Exemption Check
- **Description**: Accounts with insufficient lamports for rent exemption will be garbage collected.
- **Detection**: Check if newly created accounts are funded to rent-exempt minimum.
- **Fix**: Always ensure accounts meet `Rent::get()?.minimum_balance(data_len)`. Anchor's `init` handles this automatically.

### 8. Integer Overflow / Underflow
- **Description**: Rust's release builds don't check for integer overflow by default. Arithmetic on token amounts can wrap around.
- **Detection**: Check for standard `+`, `-`, `*`, `/` operations on amounts, balances, fees. Check `Cargo.toml` for `overflow-checks = true`.
- **Fix**: Use `checked_add()`, `checked_sub()`, `checked_mul()`, `checked_div()`. Or set `overflow-checks = true` in `[profile.release]` of Cargo.toml.

### 9. Missing Bump Seed Validation
- **Description**: Not storing/validating the bump seed for PDAs, allowing potential seed grinding attacks.
- **Detection**: Check if bump is passed as instruction data rather than stored in account. Look for `create_program_address` without bump validation.
- **Anchor**: Check `bump` constraint in `seeds` validation.
- **Fix**: Store the canonical bump in account data. In Anchor, use `bump = account.bump` or `bump` constraint.

### 10. Sysvar Account Spoofing
- **Description**: Passing a fake sysvar account (Rent, Clock, etc.) when the program doesn't validate the sysvar address.
- **Detection**: Check if sysvar accounts are validated against known addresses.
- **Fix**: Use `Sysvar::from_account_info()` which validates the account. In Anchor, use `Sysvar<'info, Rent>` types.

---

## Medium Severity

### 11. Token Account Validation
- **Description**: Not verifying token account mint, owner, or delegation status before operating on it.
- **Detection**: Check if token accounts are validated for correct mint, authority, and state.
- **Anchor**: `token::TokenAccount` with `constraint` or `has_one` for validation.
- **Fix**: Always verify `token_account.mint == expected_mint`, `token_account.owner == expected_owner`. In Anchor, use `has_one` and `constraint` attributes.

### 12. Missing Freeze / Pause Mechanism
- **Description**: No emergency stop mechanism for critical operations.
- **Detection**: Check if the program has a global pause/freeze state.
- **Fix**: Implement a pause mechanism controlled by an admin key or multi-sig for emergency situations.

### 13. Duplicate Mutable Accounts
- **Description**: Passing the same account as two different mutable parameters, causing unexpected behavior.
- **Detection**: Check if instruction handlers verify that mutable account pairs are distinct.
- **Anchor**: Add `constraint = account_a.key() != account_b.key()`.
- **Fix**: Validate that all mutable accounts in an instruction are distinct.

### 14. Missing Fee/Slippage Protection
- **Description**: Swap or transfer operations without minimum output or maximum slippage parameters.
- **Detection**: Check DeFi operations for slippage parameters, deadline checks.
- **Fix**: Add `min_amount_out` parameters. Implement deadline checks using `Clock` sysvar.

### 15. Centralization Risk
- **Description**: Single authority controls all program operations without multi-sig or timelock.
- **Detection**: Check how authority keys are managed. Single point of failure analysis.
- **Fix**: Use multi-sig (e.g., Squads Protocol). Implement timelocks for sensitive operations. Consider governance.

---

## Low Severity

### 16. Excessive unwrap() Usage
- **Description**: Using `.unwrap()` causes the program to panic with unhelpful errors.
- **Detection**: Search for `.unwrap()` calls, especially in instruction handlers.
- **Fix**: Use `?` operator with custom error types. Use `ok_or(ErrorCode::...)`.

### 17. Missing Error Codes
- **Description**: Using generic errors or `msg!` without structured error codes.
- **Detection**: Check if custom error enums are defined and used consistently.
- **Fix**: Define comprehensive `#[error_code]` enum (Anchor) or custom error types (native).

### 18. Inefficient Account Layout
- **Description**: Account data layout wastes space or isn't properly aligned.
- **Detection**: Check `#[account]` struct field ordering and sizes.
- **Fix**: Order fields by alignment (largest first). Use appropriate integer sizes.

---

## Info

### 19. Missing Program Logs
- **Description**: Insufficient logging for debugging and monitoring.
- **Fix**: Add `msg!()` logs for important state changes and error conditions.

### 20. Anchor IDL Completeness
- **Description**: IDL may not reflect all instructions or accounts accurately.
- **Fix**: Keep Anchor IDL up to date. Add proper `#[doc]` comments for IDL generation.

### 21. Test Coverage
- **Description**: Insufficient test coverage for edge cases and attack vectors.
- **Fix**: Write comprehensive tests using `bankrun` / `litesvm` for all instructions, including negative test cases.

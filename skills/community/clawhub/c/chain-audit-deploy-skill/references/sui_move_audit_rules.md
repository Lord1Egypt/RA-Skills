# Sui Move Audit Rules Reference

This document contains common vulnerability patterns and security checks specific to Sui Move smart contracts. Load this reference when performing deep audit on Sui Move packages.

---

## Critical Severity

### 1. Missing Access Control on Admin Functions
- **Description**: Public entry functions that perform privileged operations (minting, pausing, upgrading, fee changes) without requiring an admin capability object.
- **Detection**: Check all `public entry fun` functions whose names suggest admin operations. Look for `AdminCap`, `OwnerCap`, or similar capability parameters.
- **Fix**: Add a capability object parameter (`admin_cap: &AdminCap`) to all privileged functions. Create the capability in the module's `init` function and transfer to deployer.

### 2. Shared Object Manipulation
- **Description**: Shared objects can be accessed by anyone in any transaction. Without proper guards, attackers can front-run or manipulate shared state.
- **Detection**: Look for `transfer::share_object` / `transfer::public_share_object`. Check if mutable access to shared objects has access control.
- **Fix**: Use capability-based access control for mutations. Consider using owned objects where possible. Implement version checks or nonces for ordering.

### 3. One-Time Witness (OTW) Misuse
- **Description**: The OTW pattern ensures init runs exactly once. Incorrect use can allow re-initialization or bypass of setup logic.
- **Detection**: Check `init(otw: MODULENAME, ctx: &mut TxContext)` — the OTW type must match the module name in uppercase and have only `drop` ability.
- **Fix**: Ensure OTW struct has `drop` ability only. Use `sui::types::is_one_time_witness` to verify. Never store or copy OTW.

---

## High Severity

### 4. Object Ownership Confusion
- **Description**: Transferring objects to wrong addresses, or confusing owned vs shared vs immutable objects.
- **Detection**: Track all `transfer::transfer`, `transfer::public_transfer`, `transfer::share_object`, `transfer::freeze_object` calls. Verify recipients are correct.
- **Fix**: Be explicit about ownership model in design. Document whether each object should be owned, shared, or frozen.

### 5. Capability Leak
- **Description**: Admin/treasury capabilities transferred to the wrong address or made shared/public, allowing unauthorized access.
- **Detection**: Check where capabilities are created and transferred. Ensure they only go to trusted addresses.
- **Fix**: Transfer capabilities only in `init` to `tx_context::sender()`. Never share or freeze capability objects.

### 6. Missing `key` + `store` Guards
- **Description**: Objects with `store` ability can be wrapped, transferred, or stored by any module. This may not be desired for sensitive objects.
- **Detection**: Check if objects that should be restricted have unnecessary `store` ability.
- **Fix**: Only add `store` if the object needs to be transferable by modules other than the defining module. Use custom transfer functions for controlled transfers.

### 7. Balance/Coin Drain
- **Description**: Extracting all funds from a shared treasury/pool without proper authorization.
- **Detection**: Check functions that call `balance::split`, `coin::take`, or transfer `Coin` objects. Verify withdrawal limits and access control.
- **Fix**: Implement withdrawal limits, multi-sig requirements, or timelock for large withdrawals. Always validate amounts against available balance.

---

## Medium Severity

### 8. Unchecked Arithmetic
- **Description**: Move has built-in overflow protection that aborts on overflow, but this can cause DoS if not handled.
- **Detection**: Look for arithmetic operations on user inputs, especially in loops or batch operations.
- **Fix**: Validate inputs before arithmetic. Catch potential overflow scenarios with explicit range checks.

### 9. Clock/Timestamp Manipulation
- **Description**: Using `clock::timestamp_ms()` for time-sensitive operations. Validators have limited influence over consensus timestamps.
- **Detection**: Look for `Clock` usage in financial operations, auctions, or time-locked functions.
- **Fix**: Use generous time windows. Don't rely on exact timestamps. Consider epoch-based timing for less precision-critical operations.

### 10. Dynamic Field Abuse
- **Description**: Dynamic fields allow attaching arbitrary data to objects. Uncontrolled dynamic field operations can lead to state pollution.
- **Detection**: Check usage of `dynamic_field::add`, `dynamic_object_field::add`. Verify keys are controlled.
- **Fix**: Use typed keys for dynamic fields. Validate who can add/remove dynamic fields.

### 11. Package Upgrade Safety
- **Description**: Upgraded packages may break backward compatibility or introduce vulnerabilities.
- **Detection**: Check `UpgradeCap` handling. Verify upgrade policy (compatible, additive, or unrestricted).
- **Fix**: Use the most restrictive upgrade policy possible. Consider making packages immutable after stabilization. Guard `UpgradeCap` carefully.

### 12. Missing Event Emission
- **Description**: Important state changes not emitted as events.
- **Detection**: Check if `event::emit` is called for significant operations.
- **Fix**: Emit events for transfers, mints, burns, configuration changes, and other significant actions.

---

## Low Severity

### 13. Unnecessary `public` Visibility
- **Description**: Functions exposed as `public` that should be `public(package)` or private.
- **Detection**: Review all `public` and `public entry` function visibility. Check if any should be restricted.
- **Fix**: Use `public(package)` for functions only needed within the package. Make helper functions private (`fun` without `public`).

### 14. Missing Object Destruction
- **Description**: Objects with `key` but no `drop` have no way to be destroyed if no destroy function is provided.
- **Detection**: Check if objects without `drop` have a corresponding `destroy` / `burn` public function.
- **Fix**: Provide a public destruction function or add `drop` if appropriate.

### 15. Unused Abilities
- **Description**: Struct abilities that are declared but never utilized.
- **Detection**: Check if `copy`, `drop`, `store` abilities are actually needed.
- **Fix**: Remove unnecessary abilities. Minimal abilities = minimal attack surface.

---

## Info

### 16. Module Organization
- **Description**: Related functionality split across too many modules or combined inappropriately.
- **Fix**: Group related types and functions in the same module. Use friend visibility for cross-module access.

### 17. Missing Type Documentation
- **Description**: Structs and functions lack documentation comments.
- **Fix**: Add `///` documentation comments to all public types and functions.

### 18. Test Coverage
- **Description**: Missing unit tests or test transactions for critical paths.
- **Fix**: Write `#[test]` functions covering all public entry points, edge cases, and error conditions.

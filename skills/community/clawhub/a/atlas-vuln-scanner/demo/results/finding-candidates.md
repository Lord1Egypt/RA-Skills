# Atlas Finding Candidates

These are candidates for manual review, not verified findings.

## Candidate 1: Oracle manipulation / spot-price risk

**Pattern:** T1.3  
**Severity hypothesis:** Critical  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:35`  
**Flag type:** static heuristic

### Summary
Potential use of spot AMM reserves/slot0 or missing staleness/TWAP protections.

### Evidence
```solidity
    function getPrice(address pair) external view returns (uint256) {
        (uint112 r0, uint112 r1,) = IUniswapV2Pair(pair).getReserves();
        return uint256(r1) * 1e18 / uint256(r0);
```

### Validation needed
Confirm TWAP/staleness/liquidity bounds; spot prices are unsafe for lending/liquidation decisions.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 2: Reentrancy / external call review

**Pattern:** T1.1  
**Severity hypothesis:** High  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:25`  
**Flag type:** static heuristic

### Summary
External value/token calls that may require checks-effects-interactions or reentrancy protection.

### Evidence
```solidity
        require(balances[msg.sender] >= amount, "low balance");
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
```

### Validation needed
Ensure state updates happen before external calls and affected functions use nonReentrant where needed.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 3: Reentrancy / external call review

**Pattern:** T1.1  
**Severity hypothesis:** High  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:31`  
**Flag type:** static heuristic

### Summary
External value/token calls that may require checks-effects-interactions or reentrancy protection.

### Evidence
```solidity
    function emergencyWithdraw(address token, address to, uint256 amount) external {
        token.call(abi.encodeWithSignature("transfer(address,uint256)", to, amount));
    }
```

### Validation needed
Ensure state updates happen before external calls and affected functions use nonReentrant where needed.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 4: Access control review

**Pattern:** T1.2  
**Severity hypothesis:** High  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:14`  
**Flag type:** static heuristic

### Summary
Public/external admin-like functions or role logic that may need authorization review.

### Evidence
```solidity

    function setFee(uint256 newFee) external {
        // intentionally missing access control for demo
```

### Validation needed
Confirm privileged operations have correct access control and no inverse/threshold logic bug.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 5: Unchecked low-level or token call

**Pattern:** T1.4  
**Severity hypothesis:** High  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:31`  
**Flag type:** static heuristic

### Summary
Low-level/token transfer calls may ignore success or non-standard ERC20 returns.

### Evidence
```solidity
    function emergencyWithdraw(address token, address to, uint256 amount) external {
        token.call(abi.encodeWithSignature("transfer(address,uint256)", to, amount));
    }
```

### Validation needed
Check return values or use SafeERC20 / explicit require(success).

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 6: Initialization / upgradeability review

**Pattern:** T2.4  
**Severity hypothesis:** High  
**Confidence:** Medium  
**Source:** `VulnerableVault.sol:10`  
**Flag type:** static heuristic

### Summary
Upgradeable contracts need initialization guards and safe upgrade authorization.

### Evidence
```solidity

    function initialize(address _owner) external {
        owner = _owner;
```

### Validation needed
Confirm initializer cannot be replayed and implementation is locked.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 7: Accounting/share math review

**Pattern:** T1.5  
**Severity hypothesis:** High  
**Confidence:** Low  
**Source:** `VulnerableVault.sol:8`  
**Flag type:** static heuristic

### Summary
Share, index, exchange-rate, or rounding math that may cause accounting drift.

### Evidence
```solidity
    bool public paused;
    uint256 public totalShares;

```

### Validation needed
Manually validate rounding direction, empty-market edge cases, and share-price manipulation.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.

## Candidate 8: Accounting/share math review

**Pattern:** T1.5  
**Severity hypothesis:** High  
**Confidence:** Low  
**Source:** `VulnerableVault.sol:20`  
**Flag type:** static heuristic

### Summary
Share, index, exchange-rate, or rounding math that may cause accounting drift.

### Evidence
```solidity
        balances[msg.sender] += msg.value;
        totalShares += msg.value * 1e18 / address(this).balance;
    }
```

### Validation needed
Manually validate rounding direction, empty-market edge cases, and share-price manipulation.

### Disclosure guardrail
Do not submit externally until exploitability and impact are manually verified.


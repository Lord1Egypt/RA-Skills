---
title: VestingWallet Factory — Batch Deployment
---

# VestingWallet Factory

Deploy multiple VestingWallet contracts from a single factory for efficient cap table management.

## Factory Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/finance/VestingWallet.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VestingFactory is Ownable {
    event WalletCreated(
        address indexed beneficiary,
        address wallet,
        uint64 start,
        uint64 duration,
        string label
    );

    mapping(address => address[]) public beneficiaryWallets;
    address[] public allWallets;

    constructor() Ownable(msg.sender) {}

    function createVestingWallet(
        address beneficiary,
        uint64 startTimestamp,
        uint64 durationSeconds,
        string calldata label
    ) external onlyOwner returns (address) {
        VestingWallet wallet = new VestingWallet(
            beneficiary,
            startTimestamp,
            durationSeconds
        );
        beneficiaryWallets[beneficiary].push(address(wallet));
        allWallets.push(address(wallet));
        emit WalletCreated(beneficiary, address(wallet), startTimestamp, durationSeconds, label);
        return address(wallet);
    }

    function getWallets(address beneficiary) external view returns (address[] memory) {
        return beneficiaryWallets[beneficiary];
    }

    function totalWallets() external view returns (uint256) {
        return allWallets.length;
    }
}
```

## Batch Deployment Script (Foundry)

```solidity
// script/DeployVesting.s.sol
pragma solidity ^0.8.20;
import "forge-std/Script.sol";
import "../src/VestingFactory.sol";

contract DeployVesting is Script {
    struct VestingEntry {
        address beneficiary;
        uint64 start;       // unix timestamp
        uint64 duration;    // seconds
        string label;
    }

    function run() external {
        uint256 pk = vm.envUint("PRIVATE_KEY");
        VestingFactory factory = VestingFactory(vm.envAddress("FACTORY_ADDRESS"));
        address token = vm.envAddress("TOKEN_ADDRESS");

        // Load entries from JSON or hardcode
        VestingEntry[] memory entries = _getEntries();

        vm.startBroadcast(pk);
        for (uint i = 0; i < entries.length; i++) {
            address wallet = factory.createVestingWallet(
                entries[i].beneficiary,
                entries[i].start,
                entries[i].duration,
                entries[i].label
            );
            // Transfer tokens to wallet
            IERC20(token).transfer(wallet, _getAllocation(entries[i].label));
            console.log("Created:", entries[i].label, wallet);
        }
        vm.stopBroadcast();
    }
}
```

## Hardhat Batch Script

```javascript
// scripts/deployVesting.js
const { ethers } = require("hardhat");
const vestees = require("./vestees.json");

async function main() {
  const [deployer] = await ethers.getSigners();
  const Factory = await ethers.getContractFactory("VestingFactory");
  const factory = await Factory.deploy();

  const token = await ethers.getContractAt("IERC20", process.env.TOKEN_ADDRESS);

  for (const v of vestees) {
    const tx = await factory.createVestingWallet(
      v.address,
      v.startTimestamp,
      v.durationSeconds,
      v.label
    );
    const receipt = await tx.wait();
    const event = receipt.events.find(e => e.event === "WalletCreated");
    const walletAddr = event.args.wallet;

    await token.transfer(walletAddr, ethers.utils.parseEther(v.tokens.toString()));
    console.log(`${v.label}: ${walletAddr}`);
  }
}

main().catch(console.error);
```

## vestees.json format

```json
[
  {
    "label": "Team-Alice",
    "address": "0xABC...",
    "startTimestamp": 1767225600,
    "durationSeconds": 63072000,
    "tokens": 5000000
  },
  {
    "label": "Seed-Investor-1",
    "address": "0xDEF...",
    "startTimestamp": 1751328000,
    "durationSeconds": 31536000,
    "tokens": 2000000
  }
]
```

## Timestamp Calculator

```python
# cliff_months: months before vesting starts (cliff)
# vest_months: linear vesting duration after cliff
# tge_unix: unix timestamp of TGE

import time

def vesting_timestamps(tge_unix, cliff_months, vest_months):
    MONTH = 30 * 24 * 3600
    start = int(tge_unix + cliff_months * MONTH)
    duration = int(vest_months * MONTH)
    return start, duration

# Example: TGE 2025-01-01, 12mo cliff, 24mo vest
tge = 1735689600  # 2025-01-01 UTC
start, dur = vesting_timestamps(tge, 12, 24)
print(f"start={start}, duration={dur}")
```

## Release Keeper (automation)

```javascript
// Periodic script to call release() for all wallets
const wallets = await factory.allWallets(0, count);
for (const addr of wallets) {
  const vw = await ethers.getContractAt("VestingWallet", addr);
  const releasable = await vw["releasable(address)"](tokenAddress);
  if (releasable.gt(0)) {
    await vw["release(address)"](tokenAddress);
    console.log(`Released ${releasable} from ${addr}`);
  }
}
```

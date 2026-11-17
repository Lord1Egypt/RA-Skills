// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Intentionally vulnerable fixture for the CI tool smoke test.
// NEVER use as a template: this contract exists so that Slither/Aderyn are
// guaranteed to report at least one detector, proving the parsers work.

contract Vulnerable {
    mapping(address => uint256) private balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // State written AFTER the external call: reentrancy pattern.
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
        balances[msg.sender] -= amount;
    }

    // No access control: anyone can drain the contract.
    function sweep(address to) external {
        (bool ok, ) = to.call{value: address(this).balance}("");
        require(ok, "sweep failed");
    }
}

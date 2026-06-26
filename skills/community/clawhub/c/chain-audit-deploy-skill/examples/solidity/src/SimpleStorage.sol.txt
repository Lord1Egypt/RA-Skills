// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

/// @title SimpleStorage - A minimal storage contract for audit demonstration
/// @notice Stores and retrieves a single uint256 value with ownership control
contract SimpleStorage {
    address public owner;
    uint256 public storedValue;

    event ValueChanged(address indexed setter, uint256 newValue);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(uint256 _initialValue) {
        owner = msg.sender;
        storedValue = _initialValue;
        emit ValueChanged(msg.sender, _initialValue);
    }

    /// @notice Set a new value (only owner)
    function setValue(uint256 _newValue) external onlyOwner {
        storedValue = _newValue;
        emit ValueChanged(msg.sender, _newValue);
    }

    /// @notice Get the stored value
    function getValue() external view returns (uint256) {
        return storedValue;
    }

    /// @notice Transfer ownership to a new address
    function transferOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "Zero address");
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }
}

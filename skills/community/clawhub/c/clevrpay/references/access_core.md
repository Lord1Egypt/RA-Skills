# Access Core Contract ABI

access core contract abi file

```json
[
  {
    "type": "function",
    "name": "withdraw",
    "inputs": [
      {
        "name": "aToken",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "amount",
        "type": "uint256",
        "internalType": "uint256"
      },
      {
        "name": "recipient",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "event",
    "name": "Withdraw",
    "inputs": [
      {
        "name": "aToken",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "originToken",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false,
        "internalType": "uint256"
      },
      {
        "name": "recipient",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "data",
        "type": "bytes32",
        "indexed": false,
        "internalType": "bytes32"
      }
    ],
    "anonymous": false
  }
]
```

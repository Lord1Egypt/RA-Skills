---
name: check_transaction
description: Allows users to check the status of a blockchain transaction by submitting a TxId. Queries the AOX transaction API and returns human-readable results.
homepage: https://aox.xyz
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":["curl"]}}}
---

# Check Transaction Skill

This skill allows users to check the status of a blockchain transaction by providing a TxId.
It queries the AOX transaction API (https://api.aox.xyz/tx/[txid]) and returns a human-readable summary of the transaction.

---

## API Endpoint

URL: https://api.aox.xyz/tx/[txid]  
Method: GET  
Authentication: None required

Example Request:

curl -s "https://api.aox.xyz/tx/ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"

Example JSON Response:

{
    "rawId": 1773112604581,
    "createdAt": "2026-03-10T03:16:44.581Z",
    "updatedAt": "2026-03-10T03:22:18.7Z",
    "txType": "mint",
    "chainType": "arweave",
    "txId": "ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs",
    "sender": "kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134",
    "recipient": "kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134",
    "quantity": "25100000000000",
    "symbol": "AR",
    "decimals": 12,
    "blockHeight": 1873352,
    "fromTokenId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "toTokenId": "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10",
    "fee": "0",
    "feeRecipient": "",
    "confirmNum": 10,
    "confirmRange": -1670,
    "status": "waiting",
    "targetChainTxHash": ""
}

---

## Skill Usage

User Queries:

Example Input: "Check transaction ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"  
Output: Returns status, amount, sender, receiver, confirmations, and timestamp

Example Input: "Status of TxId ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"  
Output: Structured transaction info

CLI Example:

# Query a transaction
curl -s "https://api.aox.xyz/tx/ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"

Sample Output (Human-Readable):

Transaction Status: ⏳ Waiting
TxId: ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs
Type: mint
Chain: arweave
From: kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134
To: kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134
Amount: 25.1 AR  (quantity: 25100000000000, decimals: 12)
Block Height: 1873352
From Token ID: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
To Token ID: xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10
Fee: 0
Confirmations: 10
Confirm Range: -1670
Target Chain Tx Hash: (empty)
Created At: 2026-03-10T03:16:44.581Z
Updated At: 2026-03-10T03:22:18.7Z

---

## Notes & Best Practices

1. TxId format: Must start with 0x or valid AOX format.  
2. Error handling: If the TxId is invalid or not found, the API will return an error:

{
  "error": "Transaction not found"
}

3. Confirmations: Include confirmNum to show network confirmation count.  
4. No API key required: Public endpoint, no authentication needed.  
5. JSON vs human-readable: The agent should format the JSON into readable message.  
6. Amount calculation: amount = quantity / (10^decimals)  
7. Status mapping: 
   - waiting → ⏳ Waiting
   - success → ✅ Success
   - failed → ❌ Failed
8. Target chain hash: If targetChainTxHash exists, display for cross-chain info.  

---

## References

- AOX Transaction API: https://api.aox.xyz/docs  
- Example AO blockchain explorer: https://aox.xyz
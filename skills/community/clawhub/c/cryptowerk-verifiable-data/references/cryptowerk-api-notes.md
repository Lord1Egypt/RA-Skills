# Cryptowerk API Notes

Known working curl-based flow:

1. `POST https://aiagent.cryptowerk.com/platform/API/v8/register`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `hashes` and optional `lookupInfo`
   - returns `documents[0].retrievalId`

2. `POST https://aiagent.cryptowerk.com/platform/API/v8/getseal`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `retrievalId` and `provideVerificationInfos=true`
   - may return pending before a seal exists

3. `POST https://aiagent.cryptowerk.com/platform/API/v8/verifyseal`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `verifyDocHashes` and `seals`

Operational note:
- required local tools are `python3`

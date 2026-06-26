# Signer Setup

Example: configure a viem wallet client as an x402 signer on Base mainnet.

## Environment Variable

```bash
export X402_PRIVATE_KEY=0x...  # EVM private key with USDC on Base
```

> **Security:** Store your private key in a secrets manager (Infisical, AWS Secrets Manager, 1Password CLI, etc). Avoid hardcoding or committing keys to version control.

## Code

```javascript
import { createWalletClient, http } from 'viem';
import { base } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

const account = privateKeyToAccount(process.env.X402_PRIVATE_KEY);
const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

// This is the signer object expected by ExactEvmScheme
const signer = {
  address: account.address,
  signTypedData: (args) => walletClient.signTypedData({ account, ...args }),
};
```

## Alternative Signers

Any object implementing `{ address: string, signTypedData: (args) => Promise<string> }` works:

- **Hardware wallet** via WalletConnect or Ledger USB
- **Cloud KMS** (AWS KMS, GCP KMS) with a viem custom signer
- **Browser injected** (MetaMask, Coinbase Wallet) via `window.ethereum`

See [viem wallet client docs](https://viem.sh/docs/clients/wallet) for more options.

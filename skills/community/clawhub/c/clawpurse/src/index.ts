// ClawPurse - Local Timpi/NTMPI wallet for OpenClaw nodes
// Programmatic API exports

export { NEUTARO_CONFIG, KEYSTORE_CONFIG, CLI_CONFIG } from './config.js';

export {
  generateWallet,
  walletFromMnemonic,
  saveKeystore,
  loadKeystore,
  keystoreExists,
  getKeystoreAddress,
  getDefaultKeystorePath,
  type KeystoreData,
  type DecryptedWallet,
} from './keystore.js';

export {
  getBalance,
  send,
  getChainInfo,
  formatAmount,
  parseAmount,
  generateReceiveAddress,
  getClient,
  getSigningClient,
  estimateGas,
  type BalanceResult,
  type SendResult,
  type SendOptions,
} from './wallet.js';

export {
  loadReceipts,
  recordSendReceipt,
  getRecentReceipts,
  getReceiptByTxHash,
  formatReceipt,
  type Receipt,
} from './receipts.js';

export {
  loadAllowlist,
  evaluateAllowlist,
  getAllowlistPath,
  type AllowlistConfig,
  type AllowlistDestination,
} from './allowlist.js';

export {
  getValidators,
  getDelegations,
  delegate,
  undelegate,
  redelegate,
  getUnbondingDelegations,
  type Delegation,
  type DelegationResult,
  type StakeResult,
  type Validator,
} from './staking.js';

#!/usr/bin/env node
// ClawPurse CLI - Local Timpi/NTMPI wallet for OpenClaw nodes

import { CLI_CONFIG, NEUTARO_CONFIG, KEYSTORE_CONFIG } from './config.js';
import {
  generateWallet,
  saveKeystore,
  loadKeystore,
  keystoreExists,
  getKeystoreAddress,
  getDefaultKeystorePath,
} from './keystore.js';
import {
  getBalance,
  send,
  getChainInfo,
  formatAmount,
  parseAmount,
  generateReceiveAddress,
} from './wallet.js';
import {
  getValidators,
  getDelegations,
  delegate,
  undelegate,
  redelegate,
  getUnbondingDelegations,
} from './staking.js';
import { recordSendReceipt, getRecentReceipts, formatReceipt } from './receipts.js';
import {
  loadAllowlist,
  evaluateAllowlist,
  getAllowlistPath,
  saveAllowlist,
  allowlistExists,
  type AllowlistConfig,
  type AllowlistDestination,
} from './allowlist.js';
import pkg from 'enquirer';
const { prompt } = pkg;

// Simple argument parsing (no external deps for core CLI)
const args = process.argv.slice(2);
const command = args[0];

type AllowlistMode = 'enforce' | 'allow';

function getArg(flag: string): string | undefined {
  const idx = args.indexOf(flag);
  if (idx !== -1 && args[idx + 1]) {
    return args[idx + 1];
  }
  return undefined;
}

function hasFlag(flag: string): boolean {
  return args.includes(flag);
}

function parseAllowlistMode(value?: string | null): AllowlistMode | undefined {
  if (!value) return undefined;
  if (value !== 'enforce' && value !== 'allow') {
    console.error('Invalid allowlist mode. Use "enforce" or "allow".');
    process.exit(1);
  }
  return value;
}

async function promptPassword(promptText: string): Promise<string> {
  // For now, use env var or argument - interactive prompt needs enquirer
  const password = process.env.CLAWPURSE_PASSWORD || getArg('--password');
  if (!password) {
    console.error(`Error: Password required. Set CLAWPURSE_PASSWORD env var or use --password flag`);
    process.exit(1);
  }
  return password;
}

async function ensureAllowlistConfigured(modeFlag?: AllowlistMode, configPath?: string) {
  const targetPath = configPath || getAllowlistPath();
  const exists = await allowlistExists(targetPath);

  let mode = modeFlag;

  if (!mode) {
    if (exists) {
      console.log(`Allowlist already configured at ${targetPath}`);
      return;
    }

    console.log('\nGuardrail: Destination allowlist');
    console.log('Enforce mode blocks sends to unknown addresses. Allow mode lets you send to anyone but still logs entries.');
    console.log('You can override enforcement per transaction with --override-allowlist if needed.');

    if (process.stdout.isTTY) {
      const response = await prompt<{ mode: AllowlistMode }>({
        type: 'select',
        name: 'mode',
        message: 'How should ClawPurse handle unknown destination addresses?',
        choices: [
          { name: 'enforce', message: 'Enforce (block unknown addresses; safest)' },
          { name: 'allow', message: 'Allow (warn only; you manage trust manually)' },
        ],
      });
      mode = response.mode;
    } else {
      mode = 'enforce';
      console.log('Non-interactive session detected; defaulting allowlist to ENFORCE.');
    }
  }

  const allowlistConfig: AllowlistConfig = {
    defaultPolicy: {
      blockUnknown: mode === 'enforce',
      requireMemo: mode === 'enforce' ? false : false,
    },
    destinations: [],
  };

  await saveAllowlist(allowlistConfig, targetPath);
  console.log(`Allowlist configuration saved to ${targetPath} (${mode === 'enforce' ? 'enforcing' : 'allowing'} unknown destinations).`);
}

function printHelp() {
  console.log(`
${CLI_CONFIG.name} v${CLI_CONFIG.version}
${CLI_CONFIG.description}

USAGE:
  clawpurse <command> [options]

COMMANDS:
  init                  Create a new wallet (guardrail wizard runs here)
  import                Import existing wallet from mnemonic
  balance               Check wallet balance
  send <to> <amount>    Send tokens (amount in ${NEUTARO_CONFIG.displayDenom})
  receive               Show receive address
  history               Show transaction history
  status                Check chain connection status
  address               Show wallet address
  export                Export mnemonic (DANGEROUS)
  allowlist <cmd>       Manage allowlists (init | list | add | remove)
  
  STAKING:
  stake <validator> <amount>    Delegate tokens to a validator
  unstake <validator> <amount>  Undelegate tokens (22-day unbonding)
  redelegate <from> <to> <amt>  Move stake between validators
  delegations                   Show current delegations
  validators                    List active validators
  unbonding                     Show pending unbonding delegations

OPTIONS:
  --password <pass>     Wallet password (or set CLAWPURSE_PASSWORD)
  --keystore <path>     Custom keystore path
  --memo <text>         Transaction memo
  --yes                 Skip confirmations
  --allowlist <path>    Custom allowlist file (default ~/.clawpurse/allowlist.json)
  --allowlist-file <path> Same as --allowlist
  --allowlist-mode <enforce|allow>  Pre-set guardrail choice during init
  --override-allowlist  Bypass allowlist checks for this send
  --help                Show this help

SAFETY:
  Max send: ${formatAmount(BigInt(KEYSTORE_CONFIG.maxSendAmount))}
  Confirm above: ${formatAmount(BigInt(KEYSTORE_CONFIG.requireConfirmAbove))}

EXAMPLES:
  clawpurse init --password mypass
  clawpurse balance --password mypass
  clawpurse send neutaro1abc... 10.5 --password mypass
  clawpurse receive
`);
}

async function initCommand() {
  const keystorePath = getArg('--keystore');
  
  if (await keystoreExists(keystorePath)) {
    console.error('Error: Wallet already exists. Use a different --keystore path or delete the existing one.');
    process.exit(1);
  }
  
  const password = await promptPassword('Enter password for new wallet: ');
  
  if (password.length < 8) {
    console.error('Error: Password must be at least 8 characters');
    process.exit(1);
  }
  
  console.log('Generating new wallet...');
  const { mnemonic, address } = await generateWallet();
  
  console.log('Encrypting and saving keystore...');
  const savedPath = await saveKeystore(mnemonic, address, password, keystorePath);
  
  const allowlistModeFlag = parseAllowlistMode(getArg('--allowlist-mode'));
  const allowlistFileArg = getAllowlistFileFlag();
  await ensureAllowlistConfigured(allowlistModeFlag, allowlistFileArg);
  
  console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                    WALLET CREATED SUCCESSFULLY                   ║
╠══════════════════════════════════════════════════════════════════╣
║ Address: ${address.padEnd(54)}║
║ Keystore: ${savedPath.slice(-52).padEnd(53)}║
╠══════════════════════════════════════════════════════════════════╣
║ ⚠️  BACKUP YOUR MNEMONIC - THIS IS THE ONLY TIME IT'S SHOWN ⚠️   ║
╠══════════════════════════════════════════════════════════════════╣
`);
  
  // Display mnemonic in a formatted way
  const words = mnemonic.split(' ');
  for (let i = 0; i < words.length; i += 4) {
    const line = words.slice(i, i + 4).map((w, j) => `${(i + j + 1).toString().padStart(2)}. ${w.padEnd(12)}`).join(' ');
    console.log(`║ ${line.padEnd(63)}║`);
  }
  
  console.log(`╚══════════════════════════════════════════════════════════════════╝`);
}

async function importCommand() {
  const keystorePath = getArg('--keystore');
  
  if (await keystoreExists(keystorePath)) {
    console.error('Error: Wallet already exists at this path.');
    process.exit(1);
  }
  
  const mnemonic = getArg('--mnemonic') || process.env.CLAWPURSE_MNEMONIC;
  if (!mnemonic) {
    console.error('Error: Mnemonic required. Use --mnemonic or set CLAWPURSE_MNEMONIC');
    process.exit(1);
  }
  
  const password = await promptPassword('Enter password: ');
  
  console.log('Importing wallet...');
  const { walletFromMnemonic } = await import('./keystore.js');
  const { address } = await walletFromMnemonic(mnemonic);
  
  const savedPath = await saveKeystore(mnemonic, address, password, keystorePath);
  
  const allowlistModeFlag = parseAllowlistMode(getArg('--allowlist-mode'));
  const allowlistFileArg = getAllowlistFileFlag();
  await ensureAllowlistConfigured(allowlistModeFlag, allowlistFileArg);
  
  console.log(`Wallet imported successfully!`);
  console.log(`Address: ${address}`);
  console.log(`Keystore: ${savedPath}`);
}

function getAllowlistFileFlag(): string | undefined {
  return getArg('--allowlist-file') || getArg('--allowlist');
}

async function handleAllowlistCommand() {
  const action = args[1];
  const allowlistPath = getAllowlistFileFlag();
  switch (action) {
    case 'list':
      await allowlistListCommand(allowlistPath);
      break;
    case 'add':
      await allowlistAddCommand(allowlistPath);
      break;
    case 'remove':
      await allowlistRemoveCommand(allowlistPath);
      break;
    case 'init':
      await ensureAllowlistConfigured(parseAllowlistMode(getArg('--mode')), allowlistPath);
      break;
    default:
      console.error('Usage: clawpurse allowlist <list|add|remove|init> [options]');
      process.exit(1);
  }
}

async function allowlistListCommand(configPath?: string) {
  const allowlist = await loadAllowlist(configPath);
  if (!allowlist) {
    console.log('No allowlist configured yet. Run "clawpurse allowlist init" to create one.');
    return;
  }
  console.log('Default policy:');
  console.log(`  blockUnknown: ${allowlist.defaultPolicy?.blockUnknown ?? false}`);
  if (allowlist.defaultPolicy?.maxAmount !== undefined) {
    console.log(`  maxAmount: ${allowlist.defaultPolicy.maxAmount} ${NEUTARO_CONFIG.displayDenom}`);
  }
  if (allowlist.defaultPolicy?.requireMemo) {
    console.log('  requireMemo: true');
  }
  if (allowlist.destinations.length === 0) {
    console.log('\nNo specific destinations yet. Use "clawpurse allowlist add" to add one.');
    return;
  }
  console.log('\nDestinations:');
  allowlist.destinations.forEach((dest, idx) => {
    console.log(` ${idx + 1}. ${dest.name || dest.address}`);
    console.log(`    Address: ${dest.address}`);
    if (dest.maxAmount !== undefined) {
      console.log(`    Max amount: ${dest.maxAmount} ${NEUTARO_CONFIG.displayDenom}`);
    }
    if (dest.needsMemo) {
      console.log('    Memo required: yes');
    }
    if (dest.notes) {
      console.log(`    Notes: ${dest.notes}`);
    }
  });
}

async function allowlistAddCommand(configPath?: string) {
  const address = args[2];
  if (!address) {
    console.error('Usage: clawpurse allowlist add <address> [--name NAME] [--max AMOUNT] [--memo-required]');
    process.exit(1);
  }
  if (!address.startsWith(NEUTARO_CONFIG.bech32Prefix)) {
    console.error(`Invalid address. Expected prefix ${NEUTARO_CONFIG.bech32Prefix}`);
    process.exit(1);
  }
  const name = getArg('--name');
  const maxStr = getArg('--max');
  const needsMemo = hasFlag('--memo-required');
  const notes = getArg('--notes');
  let maxAmount: number | undefined;
  if (maxStr) {
    const parsed = Number(maxStr);
    if (Number.isNaN(parsed) || parsed < 0) {
      console.error('Invalid --max amount. Provide a positive number.');
      process.exit(1);
    }
    maxAmount = parsed;
  }
  const existing = (await loadAllowlist(configPath)) ?? { defaultPolicy: { blockUnknown: false }, destinations: [] };
  const filtered = existing.destinations.filter((d) => d.address !== address);
  const newEntry: AllowlistDestination = {
    address,
    name,
    maxAmount,
    needsMemo: needsMemo ? true : undefined,
    notes,
  };
  filtered.push(newEntry);
  existing.destinations = filtered;
  await saveAllowlist(existing, configPath);
  console.log(`Destination ${address} saved${name ? ` (${name})` : ''}.`);
}

async function allowlistRemoveCommand(configPath?: string) {
  const address = args[2];
  if (!address) {
    console.error('Usage: clawpurse allowlist remove <address>');
    process.exit(1);
  }
  const existing = await loadAllowlist(configPath);
  if (!existing) {
    console.error('No allowlist found. Nothing to remove.');
    process.exit(1);
  }
  const filtered = existing.destinations.filter((d) => d.address !== address);
  if (filtered.length === existing.destinations.length) {
    console.error('Address not found in allowlist.');
    process.exit(1);
  }
  existing.destinations = filtered;
  await saveAllowlist(existing, configPath);
  console.log(`Removed ${address} from allowlist.`);
}

async function balanceCommand() {
  const keystorePath = getArg('--keystore');
  let address: string | undefined = getArg('--address');
  
  if (!address) {
    const storedAddr = await getKeystoreAddress(keystorePath);
    if (!storedAddr) {
      console.error('Error: No wallet found. Run "clawpurse init" first or specify --address');
      process.exit(1);
    }
    address = storedAddr;
  }
  
  console.log(`Fetching balance for ${address}...`);
  
  try {
    const result = await getBalance(address);
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║                       WALLET BALANCE                         ║
╠══════════════════════════════════════════════════════════════╣
║ Address: ${result.address.slice(0, 52).padEnd(52)}║
║ Balance: ${(result.primary.displayAmount + ' ' + result.primary.displayDenom).padEnd(52)}║
╚══════════════════════════════════════════════════════════════╝
`);
    
    if (result.balances.length > 1) {
      console.log('Other balances:');
      result.balances.filter(b => b.denom !== NEUTARO_CONFIG.denom).forEach(b => {
        console.log(`  ${b.amount} ${b.denom}`);
      });
    }
  } catch (error) {
    console.error(`Error fetching balance: ${error instanceof Error ? error.message : error}`);
    process.exit(1);
  }
}

async function sendCommand() {
  const keystorePath = getArg('--keystore');
  const password = await promptPassword('Enter password: ');
  
  // Find to address and amount (positional after 'send')
  const sendIdx = args.indexOf('send');
  const toAddress = args[sendIdx + 1];
  const amount = args[sendIdx + 2];
  
  if (!toAddress || !amount) {
    console.error('Usage: clawpurse send <to_address> <amount>');
    process.exit(1);
  }
  
  const memo = getArg('--memo');
  const skipConfirmation = hasFlag('--yes');
  const overrideAllowlist = hasFlag('--override-allowlist');
  const allowlistPath = getAllowlistFileFlag();
  
  console.log('Loading wallet...');
  const { wallet, address } = await loadKeystore(password, keystorePath);
  
  const amountMicro = parseAmount(amount);
  
  if (!overrideAllowlist) {
    try {
      const allowlist = await loadAllowlist(allowlistPath);
      if (allowlist) {
        const check = evaluateAllowlist(allowlist, toAddress, amountMicro, memo);
        if (!check.allowed) {
          throw new Error(`${check.reason || 'Destination blocked by allowlist'} — use --override-allowlist to bypass.`);
        }
      }
    } catch (error) {
      console.error(`Allowlist error: ${error instanceof Error ? error.message : error}`);
      process.exit(1);
    }
  }
  
  console.log(`Sending ${amount} ${NEUTARO_CONFIG.displayDenom} to ${toAddress}...`);
  
  try {
    const result = await send(wallet, address, toAddress, amount, {
      memo,
      skipConfirmation,
    });
    
    // Record receipt
    const receipt = await recordSendReceipt(
      result,
      address,
      toAddress,
      amountMicro.toString(),
      memo
    );
    
    console.log(`\nTransaction successful!`);
    console.log(formatReceipt(receipt));
  } catch (error) {
    console.error(`Error: ${error instanceof Error ? error.message : error}`);
    process.exit(1);
  }
}

async function receiveCommand() {
  const keystorePath = getArg('--keystore');
  const address = await getKeystoreAddress(keystorePath);
  
  if (!address) {
    console.error('Error: No wallet found. Run "clawpurse init" first');
    process.exit(1);
  }
  
  const { displayText, qrData } = generateReceiveAddress(address);
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                     RECEIVE ${NEUTARO_CONFIG.displayDenom.padEnd(36)}║
╠══════════════════════════════════════════════════════════════╣
║ ${displayText.split('\n')[0].padEnd(61)}║
║ ${address.padEnd(61)}║
╠══════════════════════════════════════════════════════════════╣
║ QR Data: ${qrData.padEnd(52)}║
╚══════════════════════════════════════════════════════════════╝
`);
}

async function historyCommand() {
  const limit = parseInt(getArg('--limit') || '10');
  const receipts = await getRecentReceipts(limit);
  
  if (receipts.length === 0) {
    console.log('No transaction history yet.');
    return;
  }
  
  console.log(`\nRecent transactions (${receipts.length}):\n`);
  
  for (const receipt of receipts) {
    const direction = receipt.type === 'send' ? '→' : '←';
    const target = receipt.type === 'send' ? receipt.toAddress : receipt.fromAddress;
    console.log(`${receipt.timestamp.slice(0, 10)} ${direction} ${receipt.displayAmount.padEnd(20)} ${target.slice(0, 20)}... [${receipt.status}]`);
  }
}

async function statusCommand() {
  console.log('Checking chain connection...');
  
  const info = await getChainInfo();
  
  if (info.connected) {
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║                      CHAIN STATUS                            ║
╠══════════════════════════════════════════════════════════════╣
║ Status: 🟢 CONNECTED                                         ║
║ Chain ID: ${info.chainId.padEnd(51)}║
║ Block Height: ${info.height.toString().padEnd(47)}║
║ RPC: ${NEUTARO_CONFIG.rpcEndpoint.padEnd(56)}║
╚══════════════════════════════════════════════════════════════╝
`);
  } else {
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║                      CHAIN STATUS                            ║
╠══════════════════════════════════════════════════════════════╣
║ Status: 🔴 DISCONNECTED                                      ║
║ RPC: ${NEUTARO_CONFIG.rpcEndpoint.padEnd(56)}║
╚══════════════════════════════════════════════════════════════╝
`);
    process.exit(1);
  }
}

async function addressCommand() {
  const keystorePath = getArg('--keystore');
  const address = await getKeystoreAddress(keystorePath);
  
  if (!address) {
    console.error('Error: No wallet found. Run "clawpurse init" first');
    process.exit(1);
  }
  
  console.log(address);
}

async function exportCommand() {
  if (!hasFlag('--yes')) {
    console.error('⚠️  WARNING: This will display your mnemonic in plaintext!');
    console.error('Run with --yes flag to confirm you understand the risk.');
    process.exit(1);
  }
  
  const keystorePath = getArg('--keystore');
  const password = await promptPassword('Enter password: ');
  
  const { mnemonic, address } = await loadKeystore(password, keystorePath);
  
  console.log(`\nAddress: ${address}`);
  console.log(`Mnemonic:\n${mnemonic}\n`);
}

// Staking commands
async function stakeCommand() {
  const validator = args[1];
  const amount = args[2];
  
  if (!validator || !amount) {
    console.error('Usage: clawpurse stake <validator-address> <amount>');
    console.error('Example: clawpurse stake neutarovaloper1abc... 100');
    process.exit(1);
  }
  
  const keystorePath = getArg('--keystore');
  const password = await promptPassword('Enter password: ');
  const { wallet, address } = await loadKeystore(password, keystorePath);
  
  console.log(`Delegating ${amount} NTMPI to ${validator.slice(0, 20)}...`);
  
  const result = await delegate(wallet, address, validator, amount);
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    DELEGATION SUCCESSFUL                     ║
╠══════════════════════════════════════════════════════════════╣
║ Amount: ${result.displayAmount.padEnd(52)}║
║ Validator: ${validator.slice(0, 50).padEnd(50)}║
║ Tx Hash: ${result.txHash.slice(0, 52).padEnd(52)}║
║ Block: ${result.height.toString().padEnd(54)}║
╚══════════════════════════════════════════════════════════════╝
`);
}

async function unstakeCommand() {
  const validator = args[1];
  const amount = args[2];
  
  if (!validator || !amount) {
    console.error('Usage: clawpurse unstake <validator-address> <amount>');
    console.error('Example: clawpurse unstake neutarovaloper1abc... 100');
    console.error('Note: Unbonding takes 22 days on Neutaro.');
    process.exit(1);
  }
  
  if (!hasFlag('--yes')) {
    console.error('⚠️  WARNING: Unbonding takes 22 days. Tokens will be locked.');
    console.error('Run with --yes flag to confirm.');
    process.exit(1);
  }
  
  const keystorePath = getArg('--keystore');
  const password = await promptPassword('Enter password: ');
  const { wallet, address } = await loadKeystore(password, keystorePath);
  
  console.log(`Undelegating ${amount} NTMPI from ${validator.slice(0, 20)}...`);
  
  const result = await undelegate(wallet, address, validator, amount);
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                   UNDELEGATION STARTED                       ║
╠══════════════════════════════════════════════════════════════╣
║ Amount: ${result.displayAmount.padEnd(52)}║
║ Validator: ${validator.slice(0, 50).padEnd(50)}║
║ Tx Hash: ${result.txHash.slice(0, 52).padEnd(52)}║
║ ⚠️  Tokens will be available in ~22 days                     ║
╚══════════════════════════════════════════════════════════════╝
`);
}

async function redelegateCommand() {
  const fromValidator = args[1];
  const toValidator = args[2];
  const amount = args[3];
  
  if (!fromValidator || !toValidator || !amount) {
    console.error('Usage: clawpurse redelegate <from-validator> <to-validator> <amount>');
    console.error('Example: clawpurse redelegate neutarovaloper1abc... neutarovaloper1xyz... 100');
    process.exit(1);
  }
  
  const keystorePath = getArg('--keystore');
  const password = await promptPassword('Enter password: ');
  const { wallet, address } = await loadKeystore(password, keystorePath);
  
  console.log(`Redelegating ${amount} NTMPI...`);
  
  const result = await redelegate(wallet, address, fromValidator, toValidator, amount);
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                  REDELEGATION SUCCESSFUL                     ║
╠══════════════════════════════════════════════════════════════╣
║ Amount: ${result.displayAmount.padEnd(52)}║
║ From: ${fromValidator.slice(0, 55).padEnd(55)}║
║ To: ${toValidator.slice(0, 57).padEnd(57)}║
║ Tx Hash: ${result.txHash.slice(0, 52).padEnd(52)}║
╚══════════════════════════════════════════════════════════════╝
`);
}

async function delegationsCommand() {
  const keystorePath = getArg('--keystore');
  const address = await getKeystoreAddress(keystorePath);
  
  if (!address) {
    console.error('Error: No wallet found. Run "clawpurse init" first');
    process.exit(1);
  }
  
  console.log(`Fetching delegations for ${address}...`);
  
  const result = await getDelegations(address);
  
  if (result.delegations.length === 0) {
    console.log('\nNo active delegations found.');
    return;
  }
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    CURRENT DELEGATIONS                       ║
╠══════════════════════════════════════════════════════════════╣`);
  
  for (const d of result.delegations) {
    const moniker = (d.validatorMoniker || 'Unknown').slice(0, 20).padEnd(20);
    const amount = d.displayAmount.padEnd(20);
    console.log(`║ ${moniker} ${amount}               ║`);
  }
  
  console.log(`╠══════════════════════════════════════════════════════════════╣
║ Total Staked: ${result.totalStakedDisplay.padEnd(46)}║
╚══════════════════════════════════════════════════════════════╝`);
}

async function validatorsCommand() {
  console.log('Fetching active validators...');
  
  const validators = await getValidators();
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    ACTIVE VALIDATORS                         ║
╠══════════════════════════════════════════════════════════════╣
║ Moniker              Commission  Operator Address            ║
╠══════════════════════════════════════════════════════════════╣`);
  
  for (const v of validators.slice(0, 20)) {
    const moniker = v.moniker.slice(0, 18).padEnd(18);
    const commission = v.commission.padEnd(10);
    const addr = v.operatorAddress.slice(0, 30);
    console.log(`║ ${moniker} ${commission} ${addr}...║`);
  }
  
  if (validators.length > 20) {
    console.log(`║ ... and ${validators.length - 20} more validators                              ║`);
  }
  
  console.log(`╚══════════════════════════════════════════════════════════════╝`);
}

async function unbondingCommand() {
  const keystorePath = getArg('--keystore');
  const address = await getKeystoreAddress(keystorePath);
  
  if (!address) {
    console.error('Error: No wallet found. Run "clawpurse init" first');
    process.exit(1);
  }
  
  console.log(`Fetching unbonding delegations for ${address}...`);
  
  const result = await getUnbondingDelegations(address);
  
  if (result.entries.length === 0) {
    console.log('\nNo pending unbonding delegations.');
    return;
  }
  
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                  UNBONDING DELEGATIONS                       ║
╠══════════════════════════════════════════════════════════════╣`);
  
  for (const e of result.entries) {
    const amount = e.displayAmount.padEnd(20);
    const completion = new Date(e.completionTime).toLocaleDateString();
    console.log(`║ ${amount} completes ${completion.padEnd(30)}║`);
  }
  
  console.log(`╚══════════════════════════════════════════════════════════════╝`);
}

// Main
async function main() {
  if (!command || command === '--help' || command === '-h') {
    printHelp();
    process.exit(0);
  }
  
  try {
    switch (command) {
      case 'init':
        await initCommand();
        break;
      case 'import':
        await importCommand();
        break;
      case 'balance':
        await balanceCommand();
        break;
      case 'send':
        await sendCommand();
        break;
      case 'receive':
        await receiveCommand();
        break;
      case 'history':
        await historyCommand();
        break;
      case 'status':
        await statusCommand();
        break;
      case 'address':
        await addressCommand();
        break;
      case 'export':
        await exportCommand();
        break;
      case 'allowlist':
        await handleAllowlistCommand();
        break;
      case 'stake':
        await stakeCommand();
        break;
      case 'unstake':
        await unstakeCommand();
        break;
      case 'redelegate':
        await redelegateCommand();
        break;
      case 'delegations':
        await delegationsCommand();
        break;
      case 'validators':
        await validatorsCommand();
        break;
      case 'unbonding':
        await unbondingCommand();
        break;
      default:
        console.error(`Unknown command: ${command}`);
        printHelp();
        process.exit(1);
    }
  } catch (error) {
    console.error(`Error: ${error instanceof Error ? error.message : error}`);
    process.exit(1);
  }
}

main();

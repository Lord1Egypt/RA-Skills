// Transaction receipts for audit trail
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { SendResult } from './wallet.js';
import { NEUTARO_CONFIG } from './config.js';

export interface Receipt {
  id: string;
  type: 'send' | 'receive';
  txHash: string;
  fromAddress: string;
  toAddress: string;
  amount: string;
  displayAmount: string;
  denom: string;
  memo?: string;
  height: number;
  gasUsed: number;
  timestamp: string;
  status: 'confirmed' | 'pending' | 'failed';
}

function getReceiptsPath(): string {
  return path.join(os.homedir(), '.clawpurse', 'receipts.json');
}

export async function loadReceipts(): Promise<Receipt[]> {
  const receiptsPath = getReceiptsPath();
  try {
    const data = await fs.readFile(receiptsPath, 'utf8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

async function saveReceipts(receipts: Receipt[]): Promise<void> {
  const receiptsPath = getReceiptsPath();
  await fs.mkdir(path.dirname(receiptsPath), { recursive: true });
  await fs.writeFile(receiptsPath, JSON.stringify(receipts, null, 2));
}

export async function recordSendReceipt(
  result: SendResult,
  fromAddress: string,
  toAddress: string,
  amount: string,
  memo?: string
): Promise<Receipt> {
  const receipts = await loadReceipts();
  
  const receipt: Receipt = {
    id: `send-${result.txHash.slice(0, 8)}-${Date.now()}`,
    type: 'send',
    txHash: result.txHash,
    fromAddress,
    toAddress,
    amount,
    displayAmount: formatForReceipt(amount),
    denom: NEUTARO_CONFIG.denom,
    memo,
    height: result.height,
    gasUsed: result.gasUsed,
    timestamp: result.timestamp,
    status: 'confirmed',
  };
  
  receipts.push(receipt);
  await saveReceipts(receipts);
  
  return receipt;
}

function formatForReceipt(microAmount: string): string {
  const amount = BigInt(microAmount);
  const whole = amount / BigInt(10 ** NEUTARO_CONFIG.decimals);
  const fraction = amount % BigInt(10 ** NEUTARO_CONFIG.decimals);
  return `${whole}.${fraction.toString().padStart(NEUTARO_CONFIG.decimals, '0')} ${NEUTARO_CONFIG.displayDenom}`;
}

export async function getRecentReceipts(limit: number = 10): Promise<Receipt[]> {
  const receipts = await loadReceipts();
  return receipts.slice(-limit).reverse();
}

export async function getReceiptByTxHash(txHash: string): Promise<Receipt | null> {
  const receipts = await loadReceipts();
  return receipts.find(r => r.txHash === txHash) || null;
}

export function formatReceipt(receipt: Receipt): string {
  const lines = [
    `╔══════════════════════════════════════════════════════════════╗`,
    `║                    CLAWPURSE RECEIPT                         ║`,
    `╠══════════════════════════════════════════════════════════════╣`,
    `║ Type: ${receipt.type.toUpperCase().padEnd(55)}║`,
    `║ Status: ${receipt.status.toUpperCase().padEnd(53)}║`,
    `║ Amount: ${receipt.displayAmount.padEnd(53)}║`,
    `╠══════════════════════════════════════════════════════════════╣`,
    `║ From: ${receipt.fromAddress.slice(0, 54).padEnd(55)}║`,
    `║ To:   ${receipt.toAddress.slice(0, 54).padEnd(55)}║`,
    `╠══════════════════════════════════════════════════════════════╣`,
    `║ Tx Hash: ${receipt.txHash.slice(0, 52).padEnd(52)}║`,
    `║ Block: ${receipt.height.toString().padEnd(54)}║`,
    `║ Gas Used: ${receipt.gasUsed.toString().padEnd(51)}║`,
    `║ Time: ${receipt.timestamp.padEnd(55)}║`,
  ];
  
  if (receipt.memo) {
    lines.push(`║ Memo: ${receipt.memo.slice(0, 55).padEnd(55)}║`);
  }
  
  lines.push(`╚══════════════════════════════════════════════════════════════╝`);
  
  return lines.join('\n');
}

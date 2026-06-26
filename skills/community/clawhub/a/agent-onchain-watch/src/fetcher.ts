// src/fetcher.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { TxRecord, TokenTransferRecord } from './types';

// .env 직접 로드
dotenv.config({ path: path.resolve(__dirname, '../.env') });

console.log('[Fetcher] API Key Check:', process.env.ETHERSCAN_API_KEY ? 'FOUND' : 'MISSING');

/**
 * 이더리움 주소 유효성 검사 (OnchainWatch Spec)
 */
export function isValidAddress(address: string): boolean {
  return /^0x[0-9a-fA-F]{40}$/.test(address);
}

/**
 * Etherscan API 호출 래퍼
 */
async function callEtherscan(params: Record<string, string>): Promise<unknown> {
  // API 키 없을 경우 Mock 반환 (테스트용)
  if (!process.env.ETHERSCAN_API_KEY) {
    console.warn('[Etherscan] API 키 없음. Mock 데이터 반환.');
    return null; // Mock 데이터는 개별 함수에서 처리하거나 여기서 분기 가능
  }

  const url = new URL('https://api.etherscan.io/v2/api');
  url.searchParams.set('chainid', '1'); // Ethereum Mainnet
  url.searchParams.set('apikey', process.env.ETHERSCAN_API_KEY!);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, v);
  }

  try {
    const res = await fetch(url.toString());
    if (!res.ok) {
      console.error(`[Etherscan] HTTP 오류: ${res.status}`);
      return null;
    }
    const data = (await res.json()) as any;
    
    // 상세 로그 추가 (진단용)
    if (data.status !== '1') {
      console.log(`[Etherscan] API 응답 실패: status=${data.status}, message="${data.message}", result="${data.result}"`);
      return null;
    }
    
    return data.result;
  } catch (e) {
    console.error('[Etherscan] 호출 실패:', e);
    return null;
  }
}

/**
 * ETH 잔액 조회
 */
export async function fetchBalance(address: string): Promise<number | null> {
  console.log(`[Fetcher] 잔액 조회: ${address}`);

  if (!process.env.ETHERSCAN_API_KEY) return 1.2345; // Mock Balance

  const result = await callEtherscan({
    module: 'account', action: 'balance', address, tag: 'latest',
  });
  if (result === null) return null;
  const wei = BigInt(result as string);
  return Number(wei) / 1e18;
}

/**
 * 최근 트랜잭션 목록 조회
 */
export async function fetchTransactions(address: string): Promise<TxRecord[]> {
  console.log(`[Fetcher] 트랜잭션 조회: ${address}`);

  if (!process.env.ETHERSCAN_API_KEY) {
    // Mock Transactions
    return [
      {
        hash: '0xmockhash1',
        from: '0xSender',
        to: address,
        value_eth: 5.0,
        timestamp: new Date().toISOString(),
        type: 'in'
      },
      {
        hash: '0xmockhash2',
        from: address,
        to: '0xReceiver',
        value_eth: 12.5, // 고액 송금 (리스크 플래그 테스트용)
        timestamp: new Date(Date.now() - 60000).toISOString(),
        type: 'out'
      }
    ];
  }

  await new Promise(r => setTimeout(r, 200));

  const result = (await callEtherscan({
    module: 'account', action: 'txlist', address,
    startblock: '0', endblock: '99999999',
    page: '1', offset: '10', sort: 'desc',
  })) as any[];

  if (!Array.isArray(result)) return [];

  return result.map((tx: any) => ({
    hash: tx.hash,
    from: tx.from,
    to: tx.to,
    value_eth: Number(BigInt(tx.value)) / 1e18,
    timestamp: new Date(Number(tx.timeStamp) * 1000).toISOString(),
    type: tx.from.toLowerCase() === address.toLowerCase() ? 'out' : 'in',
  }));
}

/**
 * ERC-20 토큰 전송 이벤트 조회
 */
export async function fetchTokenTransfers(address: string): Promise<TokenTransferRecord[]> {
  console.log(`[Fetcher] 토큰 전송 조회: ${address}`);

  if (!process.env.ETHERSCAN_API_KEY) {
    // Mock Token Transfers
    return [
      {
        token_name: 'USDC',
        token_symbol: 'USDC',
        from: '0xSender',
        to: address,
        value: '1000000000',
        timestamp: new Date().toISOString()
      }
    ];
  }

  await new Promise(r => setTimeout(r, 200));

  const result = (await callEtherscan({
    module: 'account', action: 'tokentx', address,
    page: '1', offset: '10', sort: 'desc',
  })) as any[];

  if (!Array.isArray(result)) return [];

  return result.map((tx: any) => ({
    token_name: tx.tokenName,
    token_symbol: tx.tokenSymbol,
    from: tx.from,
    to: tx.to,
    value: tx.value,
    timestamp: new Date(Number(tx.timeStamp) * 1000).toISOString(),
  }));
}

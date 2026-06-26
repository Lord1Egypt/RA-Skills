// src/analyzer.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { LLMFactory } from './llm/factory';
import { TxRecord, TokenTransferRecord } from './types';

// .env 직접 로드
dotenv.config({ path: path.resolve(__dirname, '../.env') });

console.log('[Analyzer] LLM Provider:', process.env.LLM_PROVIDER || 'groq');

async function callLLM(systemPrompt: string, userMessage: string): Promise<string> {
  const provider = LLMFactory.create();
  try {
    return await provider.call(systemPrompt, userMessage);
  } catch (error) {
    console.error('[Analyzer] LLM call failed:', error);
    throw error;
  }
}

/**
 * 리스크 플래그 탐지 (순수 로직)
 */
export function detectRiskFlags(
  txList: TxRecord[],
  tokenList: TokenTransferRecord[]
): string[] {
  const flags: string[] = [];

  // 체크 1: 고액 트랜잭션 (10 ETH 이상)
  const highValueTx = txList.filter(tx => tx.value_eth >= 10);
  if (highValueTx.length > 0) {
    flags.push(`고액 이동 감지: ${highValueTx.length}건 (각 10 ETH 이상)`);
  }

  // 체크 2: 짧은 시간 내 다수 트랜잭션 (5분 내 3건)
  if (txList.length >= 3) {
    const times = txList.map(tx => new Date(tx.timestamp).getTime());
    const newest = times[0];
    const fiveMinAgo = newest - 5 * 60 * 1000;
    const recentCount = times.filter(t => t >= fiveMinAgo).length;
    if (recentCount >= 3) {
      flags.push(`비정상 빈도: 5분 내 ${recentCount}건 트랜잭션`);
    }
  }

  // 체크 3: 대량 토큰 이동 (5건 이상)
  if (tokenList.length >= 5) {
    flags.push(`대량 토큰 이동: ${tokenList.length}건의 ERC-20 전송`);
  }

  return flags;
}

/**
 * 온체인 요약 생성 (OnchainWatch Spec)
 */
export async function generateOnchainSummary(
  address: string,
  balance: number | null,
  txList: TxRecord[],
  tokenList: TokenTransferRecord[],
  riskFlags: string[]
): Promise<string> {
  const balanceText = balance !== null ? `${balance.toFixed(4)} ETH` : '조회 실패';
  const txText = txList.length > 0
    ? txList.slice(0, 3).map(tx =>
      `- ${tx.type === 'in' ? '수신' : '송신'} ${tx.value_eth.toFixed(4)} ETH (${tx.timestamp.slice(0, 10)})`
    ).join('\n')
    : '최근 트랜잭션 없음';
  const riskText = riskFlags.length > 0 ? riskFlags.join(', ') : '없음';

  const systemPrompt = `온체인 데이터 분석가입니다.
주어진 지갑 데이터를 바탕으로 마크다운 형식의 간결한 요약을 한국어로 작성하십시오.
200자 이내로 작성하십시오.`;

  const userMessage = `주소: ${address}\n잔액: ${balanceText}\n최근 트랜잭션:\n${txText}\n리스크 플래그: ${riskText}`;

  try {
    return await callLLM(systemPrompt, userMessage);
  } catch (e) {
    return `${address} 주소의 온체인 데이터 요약 생성에 실패했습니다.`;
  }
}

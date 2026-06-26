// src/handler.ts
import { isValidAddress, fetchBalance, fetchTransactions, fetchTokenTransfers } from './fetcher';
import { detectRiskFlags, generateOnchainSummary } from './analyzer';
import { OnchainWatchInput, OnchainWatchOutput } from './types';
import { makeSuccess, makeError } from './types';

export async function handleJob(payload: unknown): Promise<object> {
  const agentId = 'onchain-watch';
  const jobId = `job-${Date.now()}`;
  const input = payload as OnchainWatchInput;

  // 단계 1: address 필수값 확인
  if (!input.address || input.address.trim() === '') {
    return makeError(agentId, jobId, 'address 필드가 필요합니다.');
  }

  // 단계 2: 주소 형식 검증
  const address = input.address.trim().toLowerCase();
  if (!isValidAddress(address)) {
    return makeError(agentId, jobId, '유효하지 않은 이더리움 주소입니다. 0x로 시작하는 42자리 주소를 입력하세요.');
  }

  const chain = input.chain ?? 'ethereum';
  const eventTypes = input.event_types ?? ['tx', 'token_transfer'];

  console.log(`[Handler] 시작 | address: ${address} | chain: ${chain}`);

  // 단계 3: 잔액 조회
  const balance = await fetchBalance(address);

  // 단계 4: 트랜잭션 조회
  let txList: any[] = [];
  if (eventTypes.includes('tx')) {
    txList = await fetchTransactions(address);
  }

  // 단계 5: 토큰 전송 조회
  let tokenList: any[] = [];
  if (eventTypes.includes('token_transfer')) {
    tokenList = await fetchTokenTransfers(address);
  }

  // 단계 6: 리스크 플래그 탐지 (순수 로직)
  const riskFlags = detectRiskFlags(txList, tokenList);

  // 단계 7: 마크다운 요약 생성
  const summary = await generateOnchainSummary(address, balance, txList, tokenList, riskFlags);

  const output: OnchainWatchOutput = {
    address,
    chain,
    balance_eth: balance,
    transactions: txList,
    token_transfers: tokenList,
    risk_flags: riskFlags,
    summary,
  };

  console.log(`[Handler] 완료 | tx: ${txList.length}건, token: ${tokenList.length}건`);
  return makeSuccess(agentId, jobId, output);
}

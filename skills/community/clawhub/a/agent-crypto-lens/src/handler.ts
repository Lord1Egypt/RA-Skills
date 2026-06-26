// src/handler.ts
import { fetchMarketData, fetchTokenNews } from './fetcher';
import { analyzeSentiment, generateReport } from './analyzer';
import { CryptoLensInput, CryptoLensOutput, MarketData, SentimentData } from './types';
import { makeSuccess, makeError } from './types';

export async function handleJob(payload: unknown): Promise<object> {
  const agentId = 'crypto-lens';
  const jobId = `job-${Date.now()}`;
  const input = payload as CryptoLensInput;

  // 단계 1: token 필수값 확인
  if (!input.token || input.token.trim() === '') {
    return makeError(agentId, jobId, 'token 필드가 필요합니다.');
  }

  const token = input.token.trim();
  const analysisType = input.analysis_type ?? 'full';

  console.log(`[Handler] 시작 | token: ${token} | type: ${analysisType}`);

  // 단계 2: 분석 타입에 따라 필요한 데이터만 수집
  let market: MarketData = {
    current_price_usd: null, price_change_24h_pct: null,
    market_cap_usd: null, volume_24h_usd: null, data_source: 'CoinGecko',
  };

  if (analysisType === 'market' || analysisType === 'full') {
    market = await fetchMarketData(token);
  }

  // 단계 3: sentiment 또는 full이면 뉴스 수집
  let news: Array<{ title: string; url: string; content: string }> = [];
  if (analysisType === 'sentiment' || analysisType === 'full') {
    news = await fetchTokenNews(token);
  }

  // 단계 4: 센티먼트 분석
  const sentiment: SentimentData = await analyzeSentiment(token, news, market);

  // 단계 5: 종합 리포트 생성
  const { report, scores } = await generateReport(token, market, sentiment);

  const output: CryptoLensOutput = {
    token,
    analysis_type: analysisType,
    market,
    sentiment,
    report,
    scores,
  };

  console.log(`[Handler] 완료 | ${token} 분석 완료`);
  return makeSuccess(agentId, jobId, output);
}

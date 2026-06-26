// src/analyzer.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { LLMFactory } from './llm/factory';
import { MarketData, SentimentData, ScoreData } from './types';

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
 * 센티먼트 분석 (CryptoLens Spec)
 */
export async function analyzeSentiment(
  token: string,
  news: Array<{ title: string; content: string }>,
  market: MarketData
): Promise<SentimentData> {
  const newsText = news.length > 0
    ? news.map((n, i) => `[${i + 1}] ${n.title}: ${n.content}`).join('\n')
    : '뉴스 데이터 없음';

  const marketText = market.current_price_usd
    ? `현재가: $${market.current_price_usd}, 24h 변동: ${market.price_change_24h_pct?.toFixed(2)}%`
    : '시장 데이터 없음';

  const systemPrompt = `크립토 센티먼트 분석 전문가입니다.
주어진 뉴스와 시장 데이터를 분석하여 반드시 아래 JSON 형식으로만 응답하십시오.
순수 JSON만 출력하고 다른 텍스트는 절대 포함하지 마십시오.

{
  "score": 0~100 사이 정수 (0=매우 부정, 50=중립, 100=매우 긍정),
  "label": "Bullish 또는 Neutral 또는 Bearish",
  "summary": "센티먼트 판단 근거를 3문장으로 한국어로 설명"
}`;

  const userMessage = `토큰: ${token}\n시장 데이터: ${marketText}\n\n뉴스:\n${newsText}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(cleaned);

    return {
      score: typeof parsed.score === 'number' ? parsed.score : 50,
      label: ['Bullish', 'Neutral', 'Bearish'].includes(parsed.label) ? parsed.label : 'Neutral',
      summary: parsed.summary ?? '',
    };
  } catch (e) {
    console.error('[Analyzer] 센티먼트 파싱 실패');
    return { score: 50, label: 'Neutral', summary: '분석 중 오류가 발생했습니다.' };
  }
}

/**
 * 종합 리포트 및 점수 생성 (CryptoLens Spec)
 */
export async function generateReport(
  token: string,
  market: MarketData,
  sentiment: SentimentData
): Promise<{ report: string; scores: ScoreData }> {
  const marketText = market.current_price_usd
    ? `현재가 $${market.current_price_usd} | 24h ${market.price_change_24h_pct?.toFixed(2)}%`
    : '시장 데이터 없음';

  const systemPrompt = `크립토 리서치 애널리스트입니다.
주어진 데이터를 바탕으로 마크다운 리포트와 점수를 반드시 아래 JSON 형식으로 반환하십시오.
순수 JSON만 출력하십시오.

{
  "report": "마크다운 형식의 분석 리포트 (200자 이내)",
  "scores": {
    "momentum": 0~100 정수 (가격 상승 모멘텀),
    "sentiment": 0~100 정수 (시장 심리),
    "risk": 0~100 정수 (높을수록 위험)
  }
}`;

  const userMessage = `토큰: ${token}\n시장 데이터: ${marketText}\n센티먼트: ${sentiment.label} (점수: ${sentiment.score})\n센티먼트 분석: ${sentiment.summary}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(cleaned);

    return {
      report: parsed.report ?? '리포트 생성 실패',
      scores: {
        momentum: parsed.scores?.momentum ?? 50,
        sentiment: parsed.scores?.sentiment ?? 50,
        risk: parsed.scores?.risk ?? 50,
      },
    };
  } catch (e) {
    console.error('[Analyzer] 리포트 파싱 실패');
    return {
      report: `${token} 분석 중 오류가 발생했습니다.`,
      scores: { momentum: 50, sentiment: 50, risk: 50 },
    };
  }
}

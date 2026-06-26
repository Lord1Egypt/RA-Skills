// src/analyzer.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { LLMFactory } from './llm/factory';

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
 * 트렌드 신호 분류 (TrendRadar Spec)
 */
export async function analyzeTrends(
  keywordData: Record<string, any[]>,
  timeframe: string
): Promise<any[]> {
  const results: any[] = [];

  for (const [keyword, articles] of Object.entries(keywordData)) {
    console.log(`[Analyzer] "${keyword}" 트렌드 분석 중...`);

    if (articles.length === 0) {
      results.push({
        keyword,
        signal: 'Insufficient_Data',
        score: 0,
        reason: '검색 결과가 없어 트렌드를 판단할 수 없습니다.',
        evidence: [],
      });
      continue;
    }

    const articlesText = articles.map((a, i) =>
      `[${i + 1}] ${a.title}\nURL: ${a.url}\n내용: ${a.content}`
    ).join('\n\n');

    const systemPrompt = `트렌드 분석 전문가입니다.
주어진 뉴스 기사들을 분석하여 키워드의 트렌드 신호를 판단하십시오.
반드시 아래 JSON 형식으로만 응답하십시오. 다른 텍스트 없이 순수 JSON만 출력하십시오.

신호 정의:
- Rising: 언급량/관심도가 빠르게 증가하는 중
- Peaking: 현재 최고조, 곧 하락 가능성
- Declining: 언급량/관심도가 줄어드는 중
- Insufficient_Data: 판단하기에 데이터가 부족함

응답 형식 (JSON 객체 하나):
{
  "signal": "Rising | Peaking | Declining | Insufficient_Data",
  "score": 0~100 사이 정수,
  "reason": "판단 근거를 2문장으로 설명",
  "evidence": ["근거로 사용한 URL 1", "URL 2"]
}`;

    const userMessage = `키워드: "${keyword}"\n분석 기간: ${timeframe}\n\n기사 목록:\n${articlesText}`;

    try {
      const raw = await callLLM(systemPrompt, userMessage);
      const cleaned = raw.replace(/```json|```/g, '').trim();
      const parsed = JSON.parse(cleaned);

      results.push({
        keyword,
        signal: parsed.signal ?? 'Insufficient_Data',
        score: typeof parsed.score === 'number' ? parsed.score : 0,
        reason: parsed.reason ?? '',
        evidence: Array.isArray(parsed.evidence) ? parsed.evidence : [],
      });
    } catch (e) {
      console.error(`[Analyzer] "${keyword}" 분석 파싱 실패`);
      results.push({
        keyword,
        signal: 'Insufficient_Data',
        score: 0,
        reason: '분석 중 오류가 발생했습니다.',
        evidence: [],
      });
    }
  }

  return results;
}

/**
 * 전체 브리핑 생성 (TrendRadar Spec)
 */
export async function generateTrendBrief(
  trends: any[],
  timeframe: string
): Promise<string> {
  if (trends.length === 0) return '분석할 트렌드 데이터가 없습니다.';

  const trendSummary = trends
    .map(t => `- ${t.keyword}: ${t.signal} (점수: ${t.score}) — ${t.reason}`)
    .join('\n');

  const systemPrompt = `트렌드 분석 전문가입니다.
주어진 트렌드 데이터를 바탕으로 5문장 이내의 핵심 인사이트를 한국어로 작성하십시오.
마크다운 볼드(**텍스트**)를 활용해 핵심 키워드를 강조하십시오.`;

  const userMessage = `분석 기간: ${timeframe}\n\n트렌드 결과:\n${trendSummary}`;

  return await callLLM(systemPrompt, userMessage);
}

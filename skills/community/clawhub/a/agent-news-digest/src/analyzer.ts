// src/analyzer.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { LLMFactory } from './llm/factory';
import { LLMProvider } from './llm/types';

// .env 직접 로드
dotenv.config({ path: path.resolve(__dirname, '../.env') });

console.log('[Analyzer] LLM Provider:', process.env.LLM_PROVIDER || 'gemini');

/**
 * LLM 호출 래퍼 (Provider 추상화)
 */
export async function callLLM(
  systemPrompt: string,
  userMessage: string
): Promise<string> {
  const provider = LLMFactory.create();
  try {
    return await provider.call(systemPrompt, userMessage);
  } catch (error) {
    console.error('[Analyzer] LLM call failed:', error);
    // 재시도 로직이나 Fallback을 여기에 추가할 수 있음
    throw error;
  }
}

/**
 * 뉴스 목록 요약 및 중요도 부여 (NewsDigest Spec)
 */
export async function summarizeArticles(
  rawArticles: any[],
  topic: string
): Promise<any[]> {
  if (rawArticles.length === 0) return [];

  const articlesText = rawArticles.map((a, i) =>
    `[${i + 1}] 제목: ${a.title}\nURL: ${a.url}\n내용: ${a.content.slice(0, 300)}`
  ).join('\n\n');

  const systemPrompt = `당신은 뉴스 요약 전문가입니다.
주어진 뉴스 기사 목록을 분석하여 반드시 아래 JSON 형식으로만 응답하십시오.
다른 텍스트, 설명, 마크다운 코드블록 없이 순수 JSON만 출력하십시오.

응답 형식:
[
  {
    "title": "기사 제목",
    "url": "기사 URL",
    "summary": "3줄 이내 한국어 요약",
    "published_date": "날짜 또는 알 수 없음",
    "importance_score": 1~5 사이 정수 (5가 가장 중요)
  }
]`;

  const userMessage = `주제: ${topic}\n\n기사 목록:\n${articlesText}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    return JSON.parse(cleaned);
  } catch (e) {
    console.error('[Analyzer] JSON 파싱 실패');
    return [];
  }
}

/**
 * 전체 브리핑 생성 (NewsDigest Spec)
 */
export async function generateBrief(
  articles: any[],
  topic: string
): Promise<string> {
  if (articles.length === 0) return `${topic} 관련 뉴스 없음.`;

  const top5 = [...articles].sort((a, b) => b.importance_score - a.importance_score).slice(0, 5);
  const summaries = top5.map((a, i) => `${i + 1}. ${a.summary}`).join('\n');

  const systemPrompt = `당신은 뉴스 브리핑 전문가입니다.
주어진 뉴스 요약들을 바탕으로 5문장 이내의 자연스러운 한국어 브리핑을 작성하십시오.
마크다운 형식으로 작성하되, 헤더(#)는 사용하지 마십시오.`;

  const userMessage = `주제: ${topic}\n\n주요 뉴스 요약:\n${summaries}`;

  return await callLLM(systemPrompt, userMessage);
}


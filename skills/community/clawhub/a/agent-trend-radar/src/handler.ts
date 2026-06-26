// src/handler.ts
import { searchMultipleKeywords } from './fetcher';
import { analyzeTrends, generateTrendBrief } from './analyzer';
import { TrendRadarInput, TrendRadarOutput } from './types';
import { makeSuccess, makeError } from './types';

export async function handleJob(payload: unknown): Promise<object> {
  const agentId = 'trend-radar';
  const jobId = `job-${Date.now()}`;
  const input = payload as TrendRadarInput;

  // 단계 1: keywords 배열 유효성 검사
  if (!Array.isArray(input.keywords) || input.keywords.length === 0) {
    return makeError(agentId, jobId, 'keywords는 1개 이상의 문자열 배열이어야 합니다.');
  }

  // 단계 2: keywords 개수 제한 (최대 5개)
  if (input.keywords.length > 5) {
    return makeError(agentId, jobId, 'keywords는 최대 5개까지 허용됩니다.');
  }

  // 단계 3: 빈 문자열 키워드 필터링
  const keywords = input.keywords.map(k => k.trim()).filter(k => k.length > 0);
  if (keywords.length === 0) {
    return makeError(agentId, jobId, '유효한 키워드가 없습니다.');
  }

  // 단계 4: 기본값 설정
  const timeframe = input.timeframe ?? '7d';
  const region = input.region ?? 'global';

  console.log(`[Handler] 시작 | keywords: ${keywords.join(', ')} | timeframe: ${timeframe}`);

  // 단계 5: 멀티 키워드 검색
  const keywordData = await searchMultipleKeywords(keywords, timeframe, region);

  // 단계 6: 트렌드 분석
  const trends = await analyzeTrends(keywordData, timeframe);

  // 단계 7: score 내림차순 정렬
  const sorted = [...trends].sort((a, b) => b.score - a.score);

  // 단계 8: 전체 브리핑 생성
  const brief = await generateTrendBrief(sorted, timeframe);

  const output: TrendRadarOutput = {
    timeframe,
    region,
    trends: sorted,
    brief,
  };

  console.log(`[Handler] 완료 | ${sorted.length}개 키워드 분석`);
  return makeSuccess(agentId, jobId, output);
}

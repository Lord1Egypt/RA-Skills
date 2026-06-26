// src/handler.ts
import { fetchAllCompetitors } from './fetcher';
import {
  buildCompetitorProfile,
  buildComparisonMatrix,
  generateWhitespaceAndRecommendation
} from './analyzer';
import { CompeteScopeInput, CompeteScopeOutput, CompetitorProfile } from './types';
import { makeSuccess, makeError } from './types';

export async function handleJob(payload: unknown): Promise<object> {
  const agentId = 'compete-scope';
  const jobId = `job-${Date.now()}`;
  const input = payload as CompeteScopeInput;

  // 단계 1: my_product 필수값 확인
  if (!input.my_product || input.my_product.trim() === '') {
    return makeError(agentId, jobId, 'my_product 필드가 필요합니다.');
  }

  // 단계 2: competitors 배열 확인
  if (!Array.isArray(input.competitors) || input.competitors.length === 0) {
    return makeError(agentId, jobId, 'competitors는 1개 이상의 배열이어야 합니다.');
  }

  // 단계 3: competitors 개수 제한 (최대 4개)
  if (input.competitors.length > 4) {
    return makeError(agentId, jobId, 'competitors는 최대 4개까지 허용됩니다.');
  }

  const myProduct = input.my_product.trim();
  const competitors = input.competitors.map(c => c.trim()).filter(c => c.length > 0);
  const focus = input.focus ?? 'all';

  console.log(`[Handler] 시작 | 경쟁사: ${competitors.join(', ')} | focus: ${focus}`);

  // 단계 4: 모든 경쟁사 데이터 수집
  const allData = await fetchAllCompetitors(competitors, focus);

  // 단계 5: 경쟁사별 프로필 생성 (순차 처리)
  const profiles: CompetitorProfile[] = [];
  for (const competitor of competitors) {
    console.log(`[Handler] "${competitor}" 프로필 생성 중...`);
    const profile = await buildCompetitorProfile(competitor, allData[competitor] ?? []);
    profiles.push(profile);
    // Claude API rate limit 방지
    await new Promise(r => setTimeout(r, 500));
  }

  // 단계 6: 비교 매트릭스 생성
  console.log('[Handler] 비교 매트릭스 생성 중...');
  const matrix = await buildComparisonMatrix(myProduct, profiles, focus);

  // 단계 7: 화이트스페이스 + 추천 전략 생성
  console.log('[Handler] 화이트스페이스 분석 중...');
  const { whitespace, recommendation } = await generateWhitespaceAndRecommendation(
    myProduct, matrix, profiles
  );

  const output: CompeteScopeOutput = {
    my_product: myProduct,
    focus,
    competitor_profiles: profiles,
    comparison_matrix: matrix,
    whitespace,
    recommendation,
  };

  console.log(`[Handler] 완료 | 경쟁사 ${profiles.length}개 분석`);
  return makeSuccess(agentId, jobId, output);
}

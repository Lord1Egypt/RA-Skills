// src/analyzer.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { LLMFactory } from './llm/factory';
import { CompetitorProfile, MatrixRow } from './types';

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
 * 경쟁사 프로필 생성 (CompeteScope Spec)
 */
export async function buildCompetitorProfile(
  competitor: string,
  articles: Array<{ title: string; url: string; content: string }>
): Promise<CompetitorProfile> {
  if (articles.length === 0) {
    return {
      name: competitor,
      description: '정보를 찾을 수 없습니다.',
      key_features: [],
      pricing_model: '정보 없음',
      positioning: '정보 없음',
      sources: [],
    };
  }

  const articlesText = articles
    .map((a, i) => `[${i + 1}] ${a.title}\nURL: ${a.url}\n내용: ${a.content}`)
    .join('\n\n');

  const systemPrompt = `경쟁사 분석 전문가입니다.
주어진 정보를 바탕으로 경쟁사 프로필을 작성하십시오.
반드시 아래 JSON 형식으로만 응답하십시오. 순수 JSON만 출력하십시오.

{
  "description": "경쟁사를 2문장으로 설명",
  "key_features": ["핵심 기능 1", "핵심 기능 2", "핵심 기능 3"],
  "pricing_model": "가격 모델 설명 (모르면 '정보 없음')",
  "positioning": "타겟 시장과 포지셔닝 한 문장",
  "sources": ["사용한 URL 1", "URL 2"]
}`;

  const userMessage = `경쟁사: ${competitor}\n\n수집된 정보:\n${articlesText}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(cleaned);

    return {
      name: competitor,
      description: parsed.description ?? '정보 없음',
      key_features: Array.isArray(parsed.key_features) ? parsed.key_features : [],
      pricing_model: parsed.pricing_model ?? '정보 없음',
      positioning: parsed.positioning ?? '정보 없음',
      sources: Array.isArray(parsed.sources) ? parsed.sources : [],
    };
  } catch (e) {
    console.error(`[Analyzer] "${competitor}" 프로필 파싱 실패`);
    return {
      name: competitor,
      description: '분석 중 오류 발생',
      key_features: [],
      pricing_model: '정보 없음',
      positioning: '정보 없음',
      sources: [],
    };
  }
}

/**
 * 비교 매트릭스 생성 (CompeteScope Spec)
 */
export async function buildComparisonMatrix(
  myProduct: string,
  profiles: CompetitorProfile[],
  focus: string
): Promise<MatrixRow[]> {
  const dimensionMap: Record<string, string[]> = {
    pricing: ['가격 수준', '가격 모델', '무료 티어 여부'],
    features: ['핵심 기능', '사용 편의성', '통합 연동'],
    positioning: ['타겟 고객', '주요 가치 제안', '시장 포지션'],
    all: ['핵심 기능', '가격 모델', '타겟 고객', '주요 차별점'],
  };
  const dimensions = dimensionMap[focus] ?? dimensionMap['all'];

  const profilesText = profiles.map(p =>
    `[${p.name}]\n설명: ${p.description}\n기능: ${p.key_features.join(', ')}\n가격: ${p.pricing_model}\n포지셔닝: ${p.positioning}`
  ).join('\n\n');

  const competitorNames = profiles.map(p => p.name);

  const systemPrompt = `경쟁사 비교 전문가입니다.
주어진 제품 정보를 바탕으로 비교 매트릭스를 작성하십시오.
반드시 아래 JSON 배열 형식으로만 응답하십시오. 순수 JSON만 출력하십시오.

각 항목 형식:
{
  "dimension": "비교 항목명",
  "my_product": "내 제품 평가 (1문장)",
  "competitors": {
    "경쟁사명1": "평가 (1문장)",
    "경쟁사명2": "평가 (1문장)"
  }
}

반드시 다음 dimensions에 대해 작성할 것: ${dimensions.join(', ')}`;

  const userMessage = `내 제품: ${myProduct}
경쟁사 목록: ${competitorNames.join(', ')}

경쟁사 정보:
${profilesText}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    return JSON.parse(cleaned);
  } catch (e) {
    console.error('[Analyzer] 매트릭스 파싱 실패');
    return dimensions.map(dim => ({
      dimension: dim,
      my_product: '분석 실패',
      competitors: Object.fromEntries(competitorNames.map(n => [n, '분석 실패'])),
    }));
  }
}

/**
 * 화이트스페이스 도출 (CompeteScope Spec)
 */
export async function generateWhitespaceAndRecommendation(
  myProduct: string,
  matrix: MatrixRow[],
  profiles: CompetitorProfile[]
): Promise<{ whitespace: string[]; recommendation: string }> {
  const matrixText = matrix.map(row => {
    const compValues = Object.entries(row.competitors)
      .map(([name, val]) => `${name}: ${val}`)
      .join(', ');
    return `[${row.dimension}] 내 제품: ${row.my_product} | 경쟁사 - ${compValues}`;
  }).join('\n');

  const systemPrompt = `전략 컨설턴트입니다.
비교 분석 데이터를 바탕으로 시장 기회(화이트스페이스)와 전략 추천을 작성하십시오.
반드시 아래 JSON 형식으로만 응답하십시오. 순수 JSON만 출력하십시오.

{
  "whitespace": [
    "기회 영역 1 설명 (1문장)",
    "기회 영역 2 설명 (1문장)",
    "기회 영역 3 설명 (1문장)"
  ],
  "recommendation": "마크다운 형식의 전략 추천 (300자 이내, **볼드** 활용)"
}`;

  const userMessage = `내 제품: ${myProduct}\n\n비교 매트릭스:\n${matrixText}`;

  try {
    const raw = await callLLM(systemPrompt, userMessage);
    const cleaned = raw.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(cleaned);

    return {
      whitespace: Array.isArray(parsed.whitespace) ? parsed.whitespace : [],
      recommendation: parsed.recommendation ?? '추천 생성 실패',
    };
  } catch (e) {
    console.error('[Analyzer] 화이트스페이스 파싱 실패');
    return {
      whitespace: ['분석 중 오류가 발생했습니다.'],
      recommendation: '전략 추천을 생성할 수 없습니다.',
    };
  }
}

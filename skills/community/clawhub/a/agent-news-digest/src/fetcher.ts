// src/fetcher.ts
import * as dotenv from 'dotenv';
import * as path from 'path';

// .env 직접 로드 (확실하게!)
dotenv.config({ path: path.resolve(__dirname, '../.env') });

console.log('[Fetcher] API Key Check:', process.env.TAVILY_API_KEY ? 'FOUND' : 'MISSING');

interface TavilyResult {
  title: string;
  url: string;
  content: string;
  published_date?: string;
}

interface SearchOutput {
  results: TavilyResult[];
  query: string;
}

/**
 * Tavily로 웹 검색을 수행하는 함수 (Master Spec)
 */
export async function searchWeb(
  query: string,
  maxResults: number = 5
): Promise<SearchOutput> {
  console.log(`[Tavily] 검색 시작: "${query}" (max: ${maxResults})`);
  console.log('[DEBUG KEY]', process.env.TAVILY_API_KEY ? 'HAS_KEY' : 'NO_KEY');

  if (!process.env.TAVILY_API_KEY) {
    console.warn('[Tavily] API 키 없음. Mock 데이터 반환.');
    return {
      query,
      results: [
        {
          title: `${query} 관련 뉴스 1`,
          url: 'https://example.com/news1',
          content: '이것은 첫 번째 테스트 뉴스 내용입니다. 중요한 내용이 포함되어 있습니다.',
          published_date: '2025-05-15'
        },
        {
          title: `${query} 분석 리포트`,
          url: 'https://example.com/report1',
          content: '시장 동향 분석 결과 긍정적인 신호가 포착되었습니다.',
          published_date: '2025-05-14'
        }
      ]
    };
  }

  try {
    const response = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.TAVILY_API_KEY}`,
      },
      body: JSON.stringify({
        query,
        max_results: maxResults,
        search_depth: 'basic',
        include_answer: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Tavily API 오류: ${response.status} ${response.statusText}`);
    }

    const data = (await response.json()) as any;
    console.log(`[Tavily] 검색 완료: ${data.results?.length ?? 0}개 결과`);

    return {
      query,
      results: data.results ?? [],
    };
  } catch (error) {
    console.error('[Tavily] 호출 실패:', error);
    throw error;
  }
}

/**
 * period 값을 Tavily 검색어에 맞게 변환하는 함수 (NewsDigest Spec)
 */
export function periodToText(period: string): string {
  if (period === '1d') return '24 hours';
  if (period === '3d') return '3 days';
  if (period === '7d') return '7 days';
  return '24 hours';
}

/**
 * topic과 period를 받아 검색 쿼리 문자열을 만드는 함수 (NewsDigest Spec)
 */
export function buildQuery(topic: string, period: string): string {
  const periodText = periodToText(period);
  return `${topic} news last ${periodText}`;
}

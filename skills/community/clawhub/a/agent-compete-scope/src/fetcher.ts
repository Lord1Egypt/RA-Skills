// src/fetcher.ts
import * as dotenv from 'dotenv';
import * as path from 'path';

// .env 직접 로드
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
 * Tavily로 웹 검색 (Master Spec)
 */
export async function searchWeb(
  query: string,
  maxResults: number = 5
): Promise<SearchOutput> {
  console.log(`[Tavily] 검색 시작: "${query}" (max: ${maxResults})`);

  if (!process.env.TAVILY_API_KEY) {
    console.warn('[Tavily] API 키 없음. Mock 데이터 반환.');
    return {
      query,
      results: [
        {
          title: `${query}에 대한 리뷰`,
          url: 'https://example.com/review',
          content: '이 제품은 기능이 다양하고 가격이 합리적입니다. 사용자 피드백이 긍정적입니다. (Mock)',
          published_date: '2025-05-15'
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
 * 경쟁사 1개 검색 (CompeteScope Spec)
 */
export async function fetchCompetitorData(
  competitor: string,
  focus: string
): Promise<Array<{ title: string; url: string; content: string }>> {
  const queryMap: Record<string, string> = {
    pricing: `${competitor} pricing plans cost how much`,
    features: `${competitor} features product capabilities review`,
    positioning: `${competitor} target market positioning value proposition`,
    all: `${competitor} product review features pricing market positioning`,
  };

  const query = queryMap[focus] ?? queryMap['all'];
  console.log(`[Fetcher] 경쟁사 "${competitor}" 검색 중...`);

  try {
    const result = await searchWeb(query, 5);
    return result.results.map(r => ({
      title: r.title,
      url: r.url,
      content: r.content.slice(0, 500),
    }));
  } catch (e) {
    console.error(`[Fetcher] "${competitor}" 검색 실패:`, e);
    return [];
  }
}

/**
 * 모든 경쟁사 순차 수집 (CompeteScope Spec)
 */
export async function fetchAllCompetitors(
  competitors: string[],
  focus: string
): Promise<Record<string, Array<{ title: string; url: string; content: string }>>> {
  const allData: Record<string, Array<{ title: string; url: string; content: string }>> = {};

  for (const competitor of competitors) {
    allData[competitor] = await fetchCompetitorData(competitor, focus);
    // 경쟁사 간 딜레이 (Tavily Rate Limit)
    await new Promise(r => setTimeout(r, 500));
  }

  return allData;
}

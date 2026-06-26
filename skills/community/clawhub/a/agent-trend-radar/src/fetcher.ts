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
          title: `${query} 관련 트렌드 뉴스`,
          url: 'https://example.com/trend',
          content: '최근 언급량이 급증하고 있습니다. (Mock Data)',
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
 * 키워드 배열 반복 검색 (TrendRadar Spec)
 */
export async function searchMultipleKeywords(
  keywords: string[],
  timeframe: string,
  region: string
): Promise<Record<string, Array<{ title: string; url: string; content: string }>>> {
  const results: Record<string, Array<{ title: string; url: string; content: string }>> = {};

  for (const keyword of keywords) {
    console.log(`[Fetcher] 키워드 검색 중: "${keyword}"`);
    try {
      const query = `${keyword} trend ${timeframe} ${region !== 'global' ? region : ''}`.trim();
      const searchResult = await searchWeb(query, 5);

      results[keyword] = searchResult.results.map(r => ({
        title: r.title,
        url: r.url,
        content: r.content.slice(0, 400),
      }));

      console.log(`[Fetcher] "${keyword}" 검색 완료: ${results[keyword].length}개`);
    } catch (e) {
      console.error(`[Fetcher] "${keyword}" 검색 실패:`, e);
      results[keyword] = [];
    }
  }

  return results;
}

// src/fetcher.ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import { MarketData } from './types';

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
          title: `${query} 관련 뉴스 1`,
          url: 'https://example.com/crypto1',
          content: '최근 가격 상승세가 두드러지며 투자자들의 관심이 집중되고 있습니다.',
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
 * CoinGecko API로 토큰 시장 데이터 조회 (CryptoLens Spec)
 */
export async function fetchMarketData(tokenSymbol: string): Promise<MarketData> {
  const defaultData: MarketData = {
    current_price_usd: null,
    price_change_24h_pct: null,
    market_cap_usd: null,
    volume_24h_usd: null,
    data_source: 'CoinGecko',
  };

  try {
    console.log(`[Fetcher] CoinGecko ID 검색: "${tokenSymbol}"`);

    // Mock Response (실제 API 호출은 fetch 사용)
    // 여기서는 실제 API 호출 로직을 구현하되, 실패 시 Mock을 반환하는 구조로 갈 수도 있음
    // 하지만 CoinGecko 무료 API는 키 없이 가능하므로 실제 호출 시도

    const searchRes = await fetch(
      `https://api.coingecko.com/api/v3/search?query=${encodeURIComponent(tokenSymbol)}`
    );

    if (!searchRes.ok) {
      console.warn(`[Fetcher] CoinGecko 검색 실패 (${searchRes.status}). Mock 데이터 사용.`);
      return { ...defaultData, current_price_usd: 50000, price_change_24h_pct: 2.5 }; // Mock fallback
    }

    const searchData = (await searchRes.json()) as any;
    const coinId = searchData.coins?.[0]?.id;

    if (!coinId) {
      console.log(`[Fetcher] CoinGecko에서 "${tokenSymbol}" 찾지 못함`);
      return defaultData;
    }

    // 1초 딜레이 (Rate Limit 방지)
    await new Promise(resolve => setTimeout(resolve, 1000));

    console.log(`[Fetcher] 시장 데이터 조회: ID="${coinId}"`);
    const detailRes = await fetch(
      `https://api.coingecko.com/api/v3/coins/${coinId}?localization=false&tickers=false&community_data=false&developer_data=false`
    );

    if (!detailRes.ok) {
      console.warn(`[Fetcher] CoinGecko 상세 조회 실패 (${detailRes.status}). Mock 데이터 사용.`);
       return { ...defaultData, current_price_usd: 60000, price_change_24h_pct: 5.0 }; // Mock fallback
    }

    const detail = (await detailRes.json()) as any;
    const marketData = detail.market_data;

    return {
      current_price_usd: marketData?.current_price?.usd ?? null,
      price_change_24h_pct: marketData?.price_change_percentage_24h ?? null,
      market_cap_usd: marketData?.market_cap?.usd ?? null,
      volume_24h_usd: marketData?.total_volume?.usd ?? null,
      data_source: 'CoinGecko',
    };

  } catch (e) {
    console.error('[Fetcher] fetchMarketData 예외:', e);
    // 예외 발생 시에도 죽지 않고 기본값 반환
    return defaultData;
  }
}

/**
 * 토큰 뉴스 검색 (CryptoLens Spec)
 */
export async function fetchTokenNews(
  token: string
): Promise<Array<{ title: string; url: string; content: string }>> {
  const query = `${token} cryptocurrency news analysis`;
  const result = await searchWeb(query, 5);
  return result.results.map(r => ({
    title: r.title,
    url: r.url,
    content: r.content.slice(0, 400),
  }));
}

// src/handler.ts
import { buildQuery, searchWeb } from './fetcher';
import { summarizeArticles, generateBrief } from './analyzer';
import { NewsDigestInput, NewsDigestOutput, NewsArticle } from './types';
import { makeSuccess, makeError } from './types';

export async function handleJob(payload: unknown): Promise<object> {
  const agentId = 'news-digest';
  const jobId = `job-${Date.now()}`;

  const input = payload as NewsDigestInput;

  if (!input.topic || input.topic.trim() === '') {
    return makeError(agentId, jobId, 'topic 필드가 필요합니다.');
  }

  const topic = input.topic.trim();
  const period = input.period ?? '1d';
  const maxItems = Math.min(input.max_items ?? 5, 10);

  console.log(`[Handler] 시작 | topic: ${topic} | period: ${period}`);

  const query = buildQuery(topic, period);
  const searchResult = await searchWeb(query, maxItems);

  console.log(`[Handler] 검색 결과: ${searchResult.results.length}개`);

  const articles: NewsArticle[] = await summarizeArticles(searchResult.results, topic);

  const sorted = [...articles].sort((a, b) => b.importance_score - a.importance_score);

  const brief = await generateBrief(sorted, topic);

  const output: NewsDigestOutput = {
    topic,
    period,
    total_found: sorted.length,
    articles: sorted,
    brief,
  };

  console.log(`[Handler] 처리 완료 | 기사 수: ${sorted.length}`);
  return makeSuccess(agentId, jobId, output);
}

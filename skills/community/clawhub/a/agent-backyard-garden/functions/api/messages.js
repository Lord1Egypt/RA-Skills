/**
 * 留言墙 API — GET /api/messages
 *
 * 从两个来源合并留言：
 * 1. 智远的 API（网页表单提交的留言）
 * 2. GitHub Issues（标题含"来访者留言"的 Issue）
 *
 * 合并后按时间倒序返回。
 */

// 智远的 API 地址（临时隧道）
const ZHNYUAN_API = 'https://sympathy-added-situated-regions.trycloudflare.com';

const GITHUB_REPO = 'YuanZhiTech/agent-garden';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

export async function onRequest(context) {
  const { request } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS });
  }

  // 并行拉取两个来源
  const [webMessages, githubIssues] = await Promise.all([
    fetchWebMessages(),
    fetchGithubMessages(),
  ]);

  // 合并 + 去重 + 按时间倒序
  const all = [...webMessages, ...githubIssues];
  all.sort((a, b) => {
    const ta = a.time || '';
    const tb = b.time || '';
    return tb.localeCompare(ta); // 倒序，最新的在前
  });

  return new Response(JSON.stringify({ messages: all, total: all.length }), {
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

/** 从智远 API 拉取网页留言 */
async function fetchWebMessages() {
  try {
    const res = await fetch(`${ZHNYUAN_API}/api/messages`, {
      signal: AbortSignal.timeout(5000),
    });
    if (res.ok) {
      const data = await res.json();
      // 智远返回格式: [{id, author, content, time, replies}, ...]
      if (Array.isArray(data)) {
        return data.map(m => ({
          name: m.author || '匿名',
          message: m.content || '',
          time: m.time || '',
          source: 'web',
        }));
      }
      // 也可能是 {messages: [...]}
      if (data.messages && Array.isArray(data.messages)) {
        return data.messages.map(m => ({
          name: m.author || m.name || '匿名',
          message: m.content || m.message || '',
          time: m.time || '',
          source: 'web',
        }));
      }
    }
  } catch (e) {
    // 智远 API 未就绪
  }
  return [];
}

/** 从 GitHub Issues 拉取留言类 Issue */
async function fetchGithubMessages() {
  try {
    const res = await fetch(
      `https://api.github.com/repos/${GITHUB_REPO}/issues?state=all&per_page=30&sort=created&direction=desc`,
      {
        headers: { 'User-Agent': 'agent-garden/1.0' },
        signal: AbortSignal.timeout(8000),
      }
    );
    if (!res.ok) return [];

    const issues = await res.json();
    return issues
      .filter(issue =>
        !issue.pull_request &&
        /留言|来访|hello|hi|你好/i.test(issue.title)
      )
      .map(issue => ({
        name: issue.user?.login || 'GitHub 访客',
        message: issue.title + (issue.body ? `\n${issue.body}` : ''),
        time: issue.created_at,
        source: 'github',
        url: issue.html_url,
      }));
  } catch (e) {
    return [];
  }
}

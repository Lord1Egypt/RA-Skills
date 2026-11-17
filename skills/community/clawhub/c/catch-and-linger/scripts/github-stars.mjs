#!/usr/bin/env node
/**
 * github-stars.mjs — 读取 GitHub star 列表。
 *
 * 用法：node github-stars.mjs [--limit N] [--user <GitHub用户名>]
 *
 * ## 用户名从哪来（按优先级）
 *
 *   ① --user <name>        命令行显式指定
 *   ② GITHUB_USERNAME      环境变量
 *   ③ CatchLinger 账号信息  调 `GET {CATCHLINGER_API_BASE}/account` 拿 `github_username`
 *                           —— CatchLinger 用 GitHub OAuth 登录时服务端已经存下了它，
 *                           所以**用户什么都不用配**
 *
 * 拿到用户名后走**公开端点** `GET /users/{username}/starred`：不需要 GITHUB_TOKEN。
 * 只有在既没有用户名、也没有 Token 时才走认证端点 `GET /user/starred`。
 *
 * GITHUB_TOKEN 仍然可以配：它会把配额从 60 次/小时提到 5000 次/小时，
 * 并且能读到私密 profile 的 star。
 *
 * 零依赖。
 */

import { pathToFileURL } from 'node:url';

import { loadGithubEnv, loadCatchLingerEnv } from './catchlinger-env.mjs';

const API = 'https://api.github.com';
const PER_PAGE = 100;
const MAX_PAGES = 50; // 上限 5000 条

/** 解析命令行参数。 */
export function parseArgs(argv) {
  const args = { limit: Infinity, user: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--limit') args.limit = Number(argv[++i] ?? '0') || Infinity;
    else if (argv[i] === '--user') args.user = argv[++i] ?? null;
  }
  return args;
}

/**
 * 决定读哪个端点。
 *
 * @param {{ user?: string | null, hasToken?: boolean }} input
 * @returns {{ mode: 'public-user' | 'authenticated-user', user: string | null,
 *             path: string, useAuthEndpoint: boolean } | { error: 'NO_ENDPOINT' }}
 */
export function selectEndpoint({ user, hasToken }) {
  const name = (user ?? '').trim();
  if (name) {
    return {
      mode: 'public-user',
      user: name,
      path: `/users/${encodeURIComponent(name)}/starred`,
      useAuthEndpoint: false,
    };
  }
  if (hasToken) {
    return {
      mode: 'authenticated-user',
      user: null,
      path: '/user/starred',
      useAuthEndpoint: true,
    };
  }
  return { error: 'NO_ENDPOINT' };
}

/**
 * 归一化单条 star。
 *
 * 用了 `application/vnd.github.star+json` 媒体类型时，响应是 `{ starred_at, repo }`；
 * 裸 Repository 模式下字段在顶层。两种都要吃得下。
 */
export function normalizeStarEntry(raw) {
  if (!raw || typeof raw !== 'object') return null;

  const wrapped = typeof raw.repo === 'object' && raw.repo !== null;
  const repo = wrapped ? raw.repo : raw;
  if (typeof repo.full_name !== 'string' || repo.full_name === '') return null;

  return {
    full_name: repo.full_name,
    html_url: repo.html_url ?? null,
    description: repo.description ?? null,
    topics: Array.isArray(repo.topics) ? repo.topics : [],
    language: repo.language ?? null,
    stargazers_count: repo.stargazers_count ?? 0,
    starred_at: (wrapped ? raw.starred_at : repo.starred_at) ?? null,
  };
}

/**
 * 构造请求头：有 token 就带上 —— 公开端点带 token 也能把配额从 60/h 提到 5000/h。
 *
 * @param {string} token
 * @returns {{ accept: string, 'user-agent': string, authorization?: string }}
 */
export function buildHeaders(token) {
  const headers = {
    accept: 'application/vnd.github.star+json',
    'user-agent': 'CatchLingerCapture/1.0',
  };
  if (token) headers.authorization = `Bearer ${token}`;
  return headers;
}

/**
 * 问 CatchLinger 要当前账号的 GitHub 用户名。
 *
 * CatchLinger 用 GitHub OAuth 登录时，Supabase 会把 GitHub 资料写进 auth.users，
 * 服务端在 `GET /account` 里把它交出来 —— 所以 Skill 手里有 API Key 就能自取，
 * 用户不必手填用户名，也不必配 GITHUB_TOKEN。
 */
export async function fetchGithubUsernameFromCatchLinger(catchLinger) {
  if (!catchLinger) return null;
  try {
    const res = await fetch(`${catchLinger.base}/account`, {
      headers: { authorization: `Bearer ${catchLinger.key}`, accept: 'application/json' },
    });
    if (!res.ok) return null;
    const payload = await res.json();
    const data = payload?.data ?? payload;
    const name = data?.github_username;
    return typeof name === 'string' && name.trim() !== '' ? name.trim() : null;
  } catch {
    return null;
  }
}

const RATE_LIMIT_HINT =
  'GitHub API 限流（403）。匿名调用配额是 60 次/小时；设置 GITHUB_TOKEN 后是 5000 次/小时。';

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const gh = loadGithubEnv();
  const catchLinger = loadCatchLingerEnv();

  // 用户名：命令行 > 环境变量 > 向 CatchLinger 自取
  let user = (args.user ?? '').trim() || gh.username || null;
  let usernameSource = user ? 'argument-or-env' : null;
  if (!user) {
    user = await fetchGithubUsernameFromCatchLinger(catchLinger);
    if (user) usernameSource = 'catchlinger-account';
  }

  const endpoint = selectEndpoint({ user, hasToken: Boolean(gh.token) });

  if (endpoint.error) {
    console.error(
      JSON.stringify(
        {
          error:
            '不知道要读谁的 star 列表。三选一：① 传 --user <GitHub用户名>；' +
            '② 设置 GITHUB_USERNAME 环境变量；③ 配置 CATCHLINGER_API_BASE 与 CATCHLINGER_API_KEY —— ' +
            'CatchLinger 会自动告诉你你的 GitHub 用户名。' +
            '（也可以设 GITHUB_TOKEN 读自己的 star。）',
          stars: [],
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  const headers = buildHeaders(gh.token);
  const stars = [];
  let page = 1;
  let rateLimited = false;
  let authFailed = false;
  let notFound = false;
  let rateLimit = null;

  while (page <= MAX_PAGES && stars.length < args.limit) {
    const url = `${API}${endpoint.path}?per_page=${PER_PAGE}&page=${page}`;

    let res;
    try {
      res = await fetch(url, { headers });
    } catch (e) {
      console.error(
        JSON.stringify(
          { error: `请求 GitHub API 失败：${e?.message ?? e}`, stars: [] },
          null,
          2,
      ),
      );
      process.exit(1);
    }

    const limitHeader = res.headers.get('x-ratelimit-limit');
    const remainingHeader = res.headers.get('x-ratelimit-remaining');
    const resetHeader = res.headers.get('x-ratelimit-reset');
    if (limitHeader !== null) {
      rateLimit = {
        limit: Number(limitHeader),
        remaining: remainingHeader === null ? null : Number(remainingHeader),
        reset: resetHeader === null ? null : new Date(Number(resetHeader) * 1000).toISOString(),
      };
    }

    if (res.status === 401) {
      authFailed = true;
      break;
    }

    if (res.status === 403) {
      rateLimited = remainingHeader === '0' || remainingHeader === null;
      break;
    }

    if (res.status === 404) {
      notFound = true;
      break;
    }

    if (!res.ok) {
      console.error(
        JSON.stringify(
          { error: `GitHub API 返回 ${res.status} ${res.statusText}`, stars: [] },
          null,
          2,
        ),
      );
      process.exit(1);
    }

    const batch = await res.json();
    if (!Array.isArray(batch) || batch.length === 0) break;

    for (const raw of batch) {
      const entry = normalizeStarEntry(raw);
      if (entry) stars.push(entry);
    }

    if (batch.length < PER_PAGE) break;
    page += 1;
  }

  const limited = stars.slice(0, args.limit);

  if (authFailed) {
    console.error(
      JSON.stringify(
        {
          error: 'GitHub 认证失败（401）。GITHUB_TOKEN 无效或已吊销，请检查后重试。',
          stars: [],
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  if (notFound) {
    console.error(
      JSON.stringify(
        { error: `GitHub 用户不存在（404）：${endpoint.user}。请确认用户名拼写。`, stars: [] },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  if (rateLimited) {
    console.error(JSON.stringify({ error: RATE_LIMIT_HINT, stars: [] }, null, 2));
    process.exit(1);
  }

  const out = {
    mode: endpoint.mode,
    count: limited.length,
    stars: limited,
  };
  if (endpoint.user) out.user = endpoint.user;
  if (usernameSource) out.username_source = usernameSource;
  if (rateLimit) out.rateLimit = rateLimit;

  // 公开端点对私密 profile 返回空列表 —— 两种原因都提示一下，别让调用方误判。
  if (limited.length === 0 && endpoint.mode === 'public-user') {
    out.note =
      `没有取到 star：${endpoint.user} 可能确实没有 star，或该账号的 profile 是私密的` +
      '（GitHub 对私密 profile 的未认证请求返回空列表；此时改用 GITHUB_TOKEN 即可）。';
  }

  console.log(JSON.stringify(out, null, 2));
}

const isMain =
  process.argv[1] !== undefined &&
  import.meta.url === pathToFileURL(process.argv[1]).href;

if (isMain) {
  await main();
}

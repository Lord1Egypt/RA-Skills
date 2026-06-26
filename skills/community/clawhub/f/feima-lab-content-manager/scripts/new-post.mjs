#!/usr/bin/env node
/**
 * Create a new post skeleton directory.
 * Usage: node scripts/new-post.mjs --slug <kebab-slug> [--cwd <dir>]
 *
 * slug 格式：kebab-case，小写字母/数字/连字符，≤ 200 字符
 *   合法示例：how-we-build-agent-skills / mdx-v13-release / ai-2026-roadmap
 *   不需要日期前缀（YYYY-MM-DD- 的老约定 v1.4 起不再强制）
 *
 * Exit: 0 success / 1 error
 */
import { mkdir, writeFile, stat } from 'node:fs/promises';
import { join, resolve } from 'node:path';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slug') args.slug = argv[++i];
    else if (a === '--cwd') args.cwd = argv[++i];
  }
  return args;
}

async function exists(p) {
  try { await stat(p); return true; } catch { return false; }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.slug) {
    console.error('Usage: node scripts/new-post.mjs --slug <slug> [--cwd <dir>]');
    process.exit(1);
  }
  // slug 规则：小写 kebab-case，1~200 字符，不能以 - 开头或结尾，不能有连续 --
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.slug) || args.slug.length > 200) {
    console.error(
      `Invalid slug "${args.slug}". Expected kebab-case (lowercase letters, digits, single hyphens), ≤ 200 chars. Example: how-we-build-agent-skills`
    );
    process.exit(1);
  }

  const cwd = resolve(args.cwd || process.cwd());
  const postDir = join(cwd, 'posts', args.slug);

  if (await exists(postDir)) {
    console.error(`Directory already exists: ${postDir}`);
    process.exit(1);
  }

  await mkdir(join(postDir, 'images'), { recursive: true });

  const meta = {
    $schema_version: '1.2',
    slug: args.slug,
    title: '',
    description: '',
    author: '',
    route: 'BLOG',          // v1.2 新增：路由编码 BLOG|NEWS。博客选 BLOG，动态/新闻选 NEWS。
    category: '',           // 人类可读的分类名（save-article 会按名字+route 查 id）
    categoryId: null,       // 后端 categoryId；留空则自动按 category 名字查
    subCategory: '',
    tags: [],               // v1.2 起 save-article 会自动查/建 tag 并映射为 tagIds
    coverImage: '',         // 本地路径（如 ./images/cover.webp），save 时自动上传
    coverImageUrl: '',      // 远程 URL；save 成功上传 coverImage 后自动填
    publishTime: new Date().toISOString(),
    readTime: '',
    tint: 'bg-tint-blue',   // 必须带 bg- 前缀：bg-tint-yellow/blue/rose/green
    sortOrder: 0,           // 列表排序，越大越靠前
    components_used: [],
    render: { last_rendered_at: null, snapshot_version: null, feima_lab_commit: null },
    source: { original_input: 'plain_text', source_md_exists: false },
    publish: {
      status: 'draft',
      remote_id: null,      // 后端返回的 articleId
      last_saved_at: null,  // 最近一次 save-article 成功的时间
      last_saved_tag_ids: null, // v1.2 新增：最近一次 save 闭环后的 tagIds
      published_at: null,
      published_slug: null,
      api_response: null,
    },
  };
  await writeFile(join(postDir, 'meta.json'), JSON.stringify(meta, null, 2), 'utf8');

  console.log(postDir);
}

main().catch((e) => { console.error(e); process.exit(1); });

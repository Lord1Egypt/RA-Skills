import { readFile } from 'node:fs/promises';

const clean = value => value.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();

export function digestVisibleHtml(html, sourceUrl = 'https://space.bilibili.com/example') {
  if (/安全验证|验证码|登录/.test(html)) {
    return { status: 'blocked', reason: '页面要求登录、验证码或安全验证；未尝试绕过。', sourceUrl, items: [] };
  }
  const cards = [...html.matchAll(/<article class="video-card">([\s\S]*?)<\/article>/g)].slice(0, 10);
  const items = cards.map((match, index) => {
    const card = match[1];
    const link = card.match(/<a href="([^"]+)"/i)?.[1] ?? '';
    const title = clean(card.match(/<h3>([\s\S]*?)<\/h3>/i)?.[1] ?? '');
    const date = card.match(/<time[^>]*datetime="([^"]+)"/i)?.[1] ?? '';
    return {
      index: index + 1,
      title,
      date,
      topic: title ? `由可见标题概括：${title}` : '未能从可见标题判断',
      link,
      source: '主页当前可见视频卡片'
    };
  });
  return { status: 'complete', sourceUrl, items, omissions: items.some(item => !item.date) ? ['未显示发布时间的条目已留空。'] : [] };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [input, sourceUrl] = process.argv.slice(2);
  if (!input) throw new Error('Usage: node scripts/digest-fixture.mjs <offline-html> [source-url]');
  console.log(JSON.stringify(digestVisibleHtml(await readFile(input, 'utf8'), sourceUrl), null, 2));
}

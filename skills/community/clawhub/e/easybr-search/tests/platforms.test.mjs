import test from 'node:test';
import assert from 'node:assert/strict';
import { getPlatform, listPlatforms, searchURL, inferPlatform } from '../scripts/platforms.mjs';

test('15 configured profiles have stable ids, HTTPS routes, and no fabricated browser verification', () => {
  const profiles = listPlatforms(); assert.equal(profiles.length, 15); assert.equal(new Set(profiles.map(p => p.id)).size, 15);
  for (const p of profiles) {
    assert.ok(['social', 'web', 'code'].includes(p.kind)); assert.ok(p.hosts.length); assert.ok(p.selectors.detail.length);
    assert.equal(new URL(searchURL(p.id, '测试')).protocol, 'https:'); assert.equal(p.verification.browserValidated, false);
  }
  assert.equal(getPlatform('BILI').id, 'bilibili'); assert.equal(getPlatform('xhs').id, 'xiaohongshu'); assert.equal(getPlatform('twitter').id, 'x');
  profiles.pop(); assert.equal(listPlatforms().length, 15);
  assert.throws(() => getPlatform('bing').hosts.push('evil.example'), TypeError);
});

test('query bytes cannot inject a new parameter or URL fragment', () => {
  const q = 'GEO & next=https://evil.example/#中文';
  for (const [id, key] of [['bilibili', 'keyword'], ['xiaohongshu', 'keyword'], ['zhihu', 'q'], ['google', 'q'], ['csdn', 'q'], ['youtube', 'search_query']]) {
    const u = new URL(searchURL(id, q)); assert.equal(u.searchParams.get(key), q); assert.equal(u.hash, ''); assert.equal(u.searchParams.has('next'), false);
  }
  const douyin = new URL(searchURL('douyin', q)); assert.equal(decodeURIComponent(douyin.pathname), '/search/' + q); assert.equal(douyin.hash, '');
});

test('infer matches proper host boundaries and keeps unknown sites distinct', () => {
  assert.equal(inferPlatform('https://search.bilibili.com/all?keyword=geo'), 'bilibili');
  assert.equal(inferPlatform('https://blog.csdn.net/name/article/details/123'), 'csdn');
  assert.equal(inferPlatform('https://cn.bing.com/search?q=geo'), 'bing');
  assert.equal(inferPlatform('https://www.google.com.evil.example/search'), 'site:www.google.com.evil.example');
  assert.equal(inferPlatform('https://news.example.com/a'), 'site:news.example.com');
  for (const value of ['javascript:alert(1)', 'file:///tmp/a', 'not a URL', 'https://u:secret@example.com/a']) assert.equal(inferPlatform(value), null);
});

test('site extension uses a hostname, not arbitrary URL text or another search parameter', () => {
  assert.equal(getPlatform('site:EXAMPLE.com').id, 'site:example.com');
  const u = new URL(searchURL('site:example.com', '内容 & 技能'));
  assert.equal(u.hostname, 'www.google.com'); assert.equal(u.searchParams.get('q'), 'site:example.com 内容 & 技能');
  for (const id of ['site:example.com/a', 'site:example.com?x=1', 'site:user@example.com', 'site:example.com:80', 'site:bad_domain.com']) assert.throws(() => getPlatform(id), { code: 'invalid_site_domain' });
  assert.throws(() => getPlatform('made-up-platform'), { code: 'unknown_platform' });
  assert.throws(() => searchURL('bing', '   '), { code: 'invalid_query' });
});

test('content URL patterns exclude author and navigation pages but retain supported content routes', () => {
  const cases = [
    ['bilibili', 'https://www.bilibili.com/video/BV1abcDEF123', 'https://space.bilibili.com/123'],
    ['xiaohongshu', 'https://www.xiaohongshu.com/explore/0123456789abcdef01234567', 'https://www.xiaohongshu.com/user/profile/0123456789abcdef01234567'],
    ['douyin', 'https://www.douyin.com/video/12345678', 'https://www.douyin.com/user/abc'],
    ['zhihu', 'https://www.zhihu.com/question/123/answer/456', 'https://www.zhihu.com/people/name'],
    ['csdn', 'https://blog.csdn.net/user/article/details/1234', 'https://blog.csdn.net/user'],
    ['juejin', 'https://juejin.cn/post/1234', 'https://juejin.cn/user/1234'],
    ['weibo', 'https://weibo.com/12345678/Mabc123', 'https://weibo.com/u/12345678'],
    ['youtube', 'https://www.youtube.com/watch?v=abc123_xyz', 'https://www.youtube.com/@someone'],
    ['x', 'https://x.com/name/status/1234', 'https://x.com/name'],
    ['reddit', 'https://www.reddit.com/r/test/comments/abc123/topic/', 'https://www.reddit.com/user/name/'],
    ['github', 'https://github.com/owner/repo', 'https://github.com/owner']
  ];
  for (const [id, valid, invalid] of cases) {
    const patterns = getPlatform(id).contentPatterns.map(s => new RegExp(s));
    assert.ok(patterns.some(p => p.test(valid)), id + ' valid'); assert.ok(!patterns.some(p => p.test(invalid)), id + ' author');
  }
});


test('Toutiao uses the observed public search host and keeps historical aID content routes', () => {
  assert.equal(new URL(searchURL('toutiao', 'Manim')).hostname, 'so.toutiao.com');
  assert.ok(getPlatform('toutiao').contentPatterns.some(p => new RegExp(p).test('https://www.toutiao.com/a1234567890123456789/')));
});

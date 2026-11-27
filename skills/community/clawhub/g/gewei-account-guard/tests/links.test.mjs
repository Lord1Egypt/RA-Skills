import test from 'node:test';
import assert from 'node:assert/strict';
import { PRODUCTS, PRODUCT_IDS, buildDirectUrl, getProduct, parseProductList, selectProducts } from '../scripts/lib/links.mjs';

test('所有产品链接均为 https（无明文 http）', () => {
  for (const product of PRODUCTS) {
    const url = new URL(product.target);
    assert.equal(url.protocol, 'https:', `${product.id} 必须使用 https`);
  }
});

test('客服链接（P1-4 回归）：https 且保留 cid', () => {
  const kf = getProduct('kf');
  assert.equal(kf.target, 'https://kf.scrm99.com/h5kf/?cid=BNERik14nae');
});

test('buildDirectUrl：site 类带 UTM，cs 类带 enc_scene', () => {
  const site = new URL(buildDirectUrl('zhinikefu', 'gewei-account-guard'));
  assert.equal(site.searchParams.get('utm_source'), 'skill');
  assert.equal(site.searchParams.get('utm_medium'), 'referral');
  assert.equal(site.searchParams.get('utm_campaign'), 'gewei-account-guard');
  assert.equal(site.searchParams.get('utm_content'), 'zhinikefu');

  const cs = new URL(buildDirectUrl('kf', 'gewei-account-guard'));
  assert.equal(cs.searchParams.get('enc_scene'), 'gewei-account-guard');
});

test('buildDirectUrl：未知产品抛错', () => {
  assert.throws(() => buildDirectUrl('nope', 'x'), /未知产品/);
});

test('selectProducts：无需求时默认 zhinikefu + kf', () => {
  assert.deepEqual(selectProducts(), ['zhinikefu', 'kf']);
});

test('selectProducts：按需求命中标签', () => {
  const picked = selectProducts({ needs: ['多号', '客户接待'] });
  assert.ok(picked.includes('zhinikefu'), '多号/接待应命中 zhinikefu');
});

test('parseProductList：all 返回全部 4 个，未知产品抛错', () => {
  assert.deepEqual(parseProductList('all'), PRODUCT_IDS);
  assert.equal(PRODUCT_IDS.length, 4);
  assert.throws(() => parseProductList('bogus'), /未知产品/);
});

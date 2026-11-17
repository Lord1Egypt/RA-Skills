import assert from 'node:assert/strict';

const sample = { product_name: '示例商品', url: 'https://www.douyin.com/product/example', visible_price: '¥99' };
assert.ok(sample.product_name.length > 0);
assert.match(sample.url, /^https:\/\/www\.douyin\.com\//);
assert.ok(sample.visible_price.length > 0);
console.log('douyin-commerce-product-research-free self-test: ok');

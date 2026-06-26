#!/usr/bin/env node

/**
 * Mock 数据生成器
 */

const mockData = {
  user: () => ({
    id: Math.floor(Math.random() * 10000),
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://via.placeholder.com/150',
    createdAt: new Date().toISOString()
  }),

  product: () => ({
    id: Math.floor(Math.random() * 10000),
    name: 'Sample Product',
    price: Math.floor(Math.random() * 1000) + 10,
    description: 'This is a sample product description.',
    image: 'https://via.placeholder.com/300',
    stock: Math.floor(Math.random() * 100),
    createdAt: new Date().toISOString()
  }),

  order: () => ({
    id: Math.floor(Math.random() * 10000),
    orderNo: `ORD${Date.now()}`,
    userId: Math.floor(Math.random() * 10000),
    totalPrice: Math.floor(Math.random() * 1000) + 100,
    status: ['pending', 'paid', 'shipped', 'completed'][Math.floor(Math.random() * 4)],
    createdAt: new Date().toISOString()
  }),

  comment: () => ({
    id: Math.floor(Math.random() * 10000),
    userId: Math.floor(Math.random() * 10000),
    content: 'This is a sample comment.',
    likes: Math.floor(Math.random() * 100),
    createdAt: new Date().toISOString()
  }),

  article: () => ({
    id: Math.floor(Math.random() * 10000),
    title: 'Sample Article Title',
    author: 'John Doe',
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
    views: Math.floor(Math.random() * 10000),
    likes: Math.floor(Math.random() * 1000),
    createdAt: new Date().toISOString()
  })
};

const args = process.argv.slice(2);
const schemaIndex = args.indexOf('--schema');
const countIndex = args.indexOf('--count');

if (schemaIndex === -1) {
  console.log(`
📖 Mock 数据生成器

用法:
  node mock.js --schema <类型> [--count <数量>]

类型:
  user     用户数据
  product  商品数据
  order    订单数据
  comment  评论数据
  article  文章数据

示例:
  node mock.js --schema user
  node mock.js --schema product --count 5
`);
  process.exit(0);
}

const schema = args[schemaIndex + 1];
const count = countIndex !== -1 ? parseInt(args[countIndex + 1]) : 1;

if (!mockData[schema]) {
  console.error(`❌ 不支持的类型: ${schema}`);
  console.log(`支持的类型: ${Object.keys(mockData).join(', ')}`);
  process.exit(1);
}

console.log('\n📦 Mock 数据\n');

if (count === 1) {
  console.log(JSON.stringify(mockData[schema](), null, 2));
} else {
  const items = [];
  for (let i = 0; i < count; i++) {
    items.push(mockData[schema]());
  }
  console.log(JSON.stringify(items, null, 2));
}

console.log();

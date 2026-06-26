/**
 * DataLoader Usage Examples
 * 
 * Demonstrates common patterns for solving N+1 query problems
 */

const DataLoader = require('./dataloader.js');

// ============================================================================
// Example 1: Database User Loading
// ============================================================================

async function exampleDatabase() {
  // Mock database
  const db = {
    async query(sql, params) {
      console.log(`DB Query: ${sql}`, params);
      // Simulate database response
      if (sql.includes('users')) {
        return params[0].map(id => ({ id, name: `User ${id}`, email: `user${id}@example.com` }));
      }
      if (sql.includes('posts')) {
        return params[0].map(id => ({ id, user_id: id, title: `Post by ${id}` }));
      }
      return [];
    }
  };

  // Create loaders
  const userLoader = new DataLoader(async (ids) => {
    const users = await db.query('SELECT * FROM users WHERE id IN (?)', [ids]);
    return ids.map(id => users.find(u => u.id === id) || null);
  });

  const postLoader = new DataLoader(async (userIds) => {
    const posts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIds]);
    return userIds.map(id => posts.filter(p => p.user_id === id));
  });

  // Load users and their posts efficiently
  console.log('\n=== Example 1: Database Loading ===');
  const userIds = [1, 2, 3, 4, 5];
  
  const users = await userLoader.loadMany(userIds);
  console.log('Loaded users:', users.length);
  
  const posts = await Promise.all(users.map(user => postLoader.load(user.id)));
  console.log('Loaded posts for all users');
  
  // Total queries: 2 (one for users, one for posts)
  // Without DataLoader: 6 queries (1 + 5)
}

// ============================================================================
// Example 2: API Batching
// ============================================================================

async function exampleAPI() {
  // Mock API
  const api = {
    async fetch(url) {
      console.log(`API Call: ${url}`);
      await new Promise(resolve => setTimeout(resolve, 100)); // Simulate network
      return { url, data: `Response from ${url}` };
    }
  };

  const apiLoader = new DataLoader(async (urls) => {
    console.log(`\nBatching ${urls.length} API calls...`);
    const responses = await Promise.all(urls.map(url => api.fetch(url)));
    return responses;
  }, { maxBatchSize: 10 });

  console.log('\n=== Example 2: API Batching ===');
  
  const urls = [
    'https://api.example.com/users/1',
    'https://api.example.com/users/2',
    'https://api.example.com/users/3',
  ];

  const responses = await Promise.all(urls.map(url => apiLoader.load(url)));
  console.log('Received responses:', responses.length);
}

// ============================================================================
// Example 3: Nested Data (GraphQL-style)
// ============================================================================

async function exampleNested() {
  // Mock database
  const db = {
    async query(sql, params) {
      console.log(`DB: ${sql}`);
      if (sql.includes('users')) return params[0].map(id => ({ id, name: `User ${id}` }));
      if (sql.includes('posts')) {
        const posts = [];
        params[0].forEach(userId => {
          posts.push({ id: `${userId}-1`, user_id: userId, title: `Post 1` });
          posts.push({ id: `${userId}-2`, user_id: userId, title: `Post 2` });
        });
        return posts;
      }
      if (sql.includes('comments')) {
        const comments = [];
        params[0].forEach(postId => {
          comments.push({ id: `${postId}-a`, post_id: postId, text: 'Comment 1' });
        });
        return comments;
      }
      return [];
    }
  };

  const userLoader = new DataLoader(async (ids) => {
    const users = await db.query('SELECT * FROM users WHERE id IN (?)', [ids]);
    return ids.map(id => users.find(u => u.id === id));
  });

  const postLoader = new DataLoader(async (userIds) => {
    const posts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIds]);
    return userIds.map(id => posts.filter(p => p.user_id === id));
  });

  const commentLoader = new DataLoader(async (postIds) => {
    const flatIds = postIds.flat();
    const comments = await db.query('SELECT * FROM comments WHERE post_id IN (?)', [flatIds]);
    return postIds.map(ids => comments.filter(c => ids.includes(c.post_id)));
  });

  console.log('\n=== Example 3: Nested Data ===');
  
  const userIds = [1, 2, 3];
  const users = await userLoader.loadMany(userIds);
  
  for (const user of users) {
    user.posts = await postLoader.load(user.id);
    for (const post of user.posts) {
      post.comments = await commentLoader.load(post.id);
    }
  }

  console.log('Loaded complete user -> posts -> comments tree');
  console.log('Total queries: 3 (users, posts, comments)');
  console.log('Without DataLoader: 1 + 3 + 6 = 10 queries');
}

// ============================================================================
// Example 4: Cache Priming and Clearing
// ============================================================================

async function exampleCache() {
  let queryCount = 0;
  
  const loader = new DataLoader(async (ids) => {
    queryCount++;
    console.log(`Batch query #${queryCount} for IDs:`, ids);
    return ids.map(id => ({ id, value: `Data ${id}` }));
  });

  console.log('\n=== Example 4: Cache Management ===');
  
  // First load - hits database
  const data1 = await loader.load(1);
  console.log('First load:', data1);
  
  // Second load of same key - uses cache
  const data2 = await loader.load(1);
  console.log('Second load (cached):', data2);
  console.log('Query count:', queryCount, '(should be 1)');
  
  // Prime cache with known data
  loader.prime(99, { id: 99, value: 'Primed data' });
  const data3 = await loader.load(99);
  console.log('Primed data:', data3);
  
  // Clear cache
  loader.clear(1);
  const data4 = await loader.load(1);
  console.log('After clear:', data4);
  console.log('Query count:', queryCount, '(should be 2)');
}

// ============================================================================
// Example 5: Performance Comparison
// ============================================================================

async function examplePerformance() {
  let naiveQueries = 0;
  let dataLoaderQueries = 0;

  const mockDB = {
    async query(sql) {
      if (sql.includes('users')) {
        return Array.from({ length: 100 }, (_, i) => ({ id: i + 1, name: `User ${i + 1}` }));
      }
      if (sql.includes('posts')) {
        const userId = parseInt(sql.split('=')[1]);
        return Array.from({ length: 5 }, (_, i) => ({ id: i + 1, user_id: userId }));
      }
      return [];
    }
  };

  // Naive approach (N+1)
  console.log('\n=== Example 5: Performance Comparison ===');
  console.log('Loading 100 users with their posts...\n');
  
  console.log('Naive approach (N+1):');
  const startTime1 = Date.now();
  const users1 = await mockDB.query('SELECT * FROM users');
  naiveQueries++;
  
  for (const user of users1) {
    const posts = await mockDB.query(`SELECT * FROM posts WHERE user_id = ${user.id}`);
    naiveQueries++;
    user.posts = posts;
  }
  const time1 = Date.now() - startTime1;
  console.log(`Queries: ${naiveQueries}, Time: ${time1}ms`);

  // DataLoader approach
  const userLoader = new DataLoader(async (ids) => {
    dataLoaderQueries++;
    const users = await mockDB.query('SELECT * FROM users');
    return ids.map(id => users.find(u => u.id === id));
  });

  const postLoader = new DataLoader(async (userIds) => {
    dataLoaderQueries++;
    const allPosts = [];
    for (const id of userIds) {
      const posts = await mockDB.query(`SELECT * FROM posts WHERE user_id = ${id}`);
      allPosts.push(...posts);
    }
    return userIds.map(id => allPosts.filter(p => p.user_id === id));
  });

  console.log('\nDataLoader approach:');
  const startTime2 = Date.now();
  const users2 = await userLoader.loadMany(Array.from({ length: 100 }, (_, i) => i + 1));
  await Promise.all(users2.map(user => postLoader.load(user.id)));
  const time2 = Date.now() - startTime2;
  console.log(`Queries: ${dataLoaderQueries}, Time: ${time2}ms`);

  console.log(`\nImprovement: ${naiveQueries} → ${dataLoaderQueries} queries (${Math.round((1 - dataLoaderQueries / naiveQueries) * 100)}% reduction)`);
}

// Run all examples
async function runExamples() {
  try {
    await exampleDatabase();
    await exampleAPI();
    await exampleNested();
    await exampleCache();
    await examplePerformance();
    console.log('\n✅ All examples completed!');
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

// Export examples
module.exports = {
  exampleDatabase,
  exampleAPI,
  exampleNested,
  exampleCache,
  examplePerformance,
  runExamples
};

// Run if executed directly
if (require.main === module) {
  runExamples();
}

#!/usr/bin/env node

/**
 * Get News
 * Usage: node news.mjs [crypto]
 *   crypto - Blockchain Industry News (catid=1)
 */

const args = process.argv.slice(2);
const type = args[0] || 'crypto';

const CATEGORIES = {
  crypto: { id: 1, name: 'Blockchain Industry News' }
};

const BASE_URL = 'https://api1.desk3.io/v1/news/list';

async function getNews(categoryId, count = 10) {
  try {
    const response = await fetch(`${BASE_URL}?catid=${categoryId}&page=1&rows=${count}`, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data?.list) {
      console.error('API returned error');
      return null;
    }
    
    return data.data.list;
  } catch (error) {
    console.error('Failed to fetch news:', error.message);
    return null;
  }
}

async function main() {
  const category = CATEGORIES[type];
  if (!category) {
    console.error(`Unknown category: ${type}`);
    console.log(`Available categories: ${Object.keys(CATEGORIES).join(', ')}`);
    process.exit(1);
  }
  
  console.log(`\n📰 ${category.name}\n` + '='.repeat(50));
  
  const news = await getNews(category.id, 10);
  
  if (news && news.length > 0) {
    news.forEach((item, index) => {
      const time = new Date(item.published_at).toLocaleString('en-US', {
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      console.log(`${index + 1}. ${item.title}`);
      console.log(`   ${time}`);
      if (item.description) {
        console.log(`   ${item.description.substring(0, 80)}...`);
      }
      console.log('');
    });
  } else {
    console.log('No news available');
  }
  
  console.log('='.repeat(50));
}

main();

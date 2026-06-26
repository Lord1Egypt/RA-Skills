const axios = require('axios');

/**
 * Twitter (X) 数据抓取器
 */
class TwitterScraper {
  constructor(bearerToken) {
    this.bearerToken = bearerToken;
    this.baseURL = 'https://api.twitter.com/2';
  }

  /**
   * 搜索加密货币融资相关推文
   * @returns {Promise<Array>}
   */
  async searchFundingTweets() {
    if (!this.bearerToken) {
      console.warn('Twitter Bearer Token not configured');
      return [];
    }

    try {
      const query = '(crypto OR blockchain OR web3) (funding OR raised OR investment) -is:retweet';
      const response = await axios.get(`${this.baseURL}/tweets/search/recent`, {
        params: {
          query,
          max_results: 20,
          'tweet.fields': 'created_at,author_id,public_metrics',
          'user.fields': 'name,username,verified',
          expansions: 'author_id'
        },
        headers: {
          'Authorization': `Bearer ${this.bearerToken}`
        }
      });

      return this.formatTweets(response.data);
    } catch (error) {
      console.error('Twitter search failed:', error.message);
      return [];
    }
  }

  /**
   * 格式化推文数据
   */
  formatTweets(data) {
    if (!data.data || !Array.isArray(data.data)) return [];

    const users = {};
    if (data.includes && data.includes.users) {
      data.includes.users.forEach(user => {
        users[user.id] = user;
      });
    }

    return data.data.map(tweet => {
      const author = users[tweet.author_id] || {};
      return {
        text: tweet.text,
        author: author.name || 'Unknown',
        username: author.username || '',
        verified: author.verified || false,
        createdAt: tweet.created_at,
        likes: tweet.public_metrics?.like_count || 0,
        retweets: tweet.public_metrics?.retweet_count || 0,
        url: `https://twitter.com/${author.username}/status/${tweet.id}`
      };
    });
  }

  /**
   * 搜索TEG相关推文
   */
  async searchTEGTweets() {
    if (!this.bearerToken) {
      console.warn('Twitter Bearer Token not configured');
      return [];
    }

    try {
      const query = '(TGE OR "token generation" OR IDO OR IEO) (crypto OR blockchain) -is:retweet';
      const response = await axios.get(`${this.baseURL}/tweets/search/recent`, {
        params: {
          query,
          max_results: 20,
          'tweet.fields': 'created_at,author_id,public_metrics',
          'user.fields': 'name,username,verified',
          expansions: 'author_id'
        },
        headers: {
          'Authorization': `Bearer ${this.bearerToken}`
        }
      });

      return this.formatTweets(response.data);
    } catch (error) {
      console.error('Twitter TEG search failed:', error.message);
      return [];
    }
  }
}

module.exports = TwitterScraper;

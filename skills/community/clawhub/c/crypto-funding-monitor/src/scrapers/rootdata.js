const axios = require('axios');
const cheerio = require('cheerio');

/**
 * RootData 数据抓取器
 */
class RootDataScraper {
  constructor(apiKey = null) {
    this.apiKey = apiKey;
    this.baseURL = 'https://www.rootdata.com';
  }

  /**
   * 获取最新融资项目
   * @returns {Promise<Array>}
   */
  async getLatestFunding() {
    try {
      // 如果有API key，使用API
      if (this.apiKey) {
        return await this.fetchFromAPI();
      }

      // 否则使用网页抓取
      return await this.scrapeWebsite();
    } catch (error) {
      console.error('RootData scraping failed:', error.message);
      return [];
    }
  }

  /**
   * 从API获取数据
   */
  async fetchFromAPI() {
    try {
      const response = await axios.get(`${this.baseURL}/api/funding/latest`, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      });

      return this.formatFundingData(response.data);
    } catch (error) {
      console.error('API fetch failed:', error.message);
      return [];
    }
  }

  /**
   * 从网页抓取数据
   */
  async scrapeWebsite() {
    try {
      const response = await axios.get(`${this.baseURL}/Fundraising`, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });

      const $ = cheerio.load(response.data);
      const fundingData = [];

      // 解析融资项目列表
      $('.funding-item').each((index, element) => {
        const $item = $(element);
        fundingData.push({
          projectName: $item.find('.project-name').text().trim(),
          amount: $item.find('.funding-amount').text().trim(),
          round: $item.find('.funding-round').text().trim(),
          investors: $item.find('.investors').text().trim(),
          date: $item.find('.funding-date').text().trim(),
          category: $item.find('.category').text().trim(),
          description: $item.find('.description').text().trim(),
          url: this.baseURL + $item.find('a').attr('href')
        });
      });

      return fundingData;
    } catch (error) {
      console.error('Website scraping failed:', error.message);
      return [];
    }
  }

  /**
   * 格式化融资数据
   */
  formatFundingData(rawData) {
    if (!Array.isArray(rawData)) return [];

    return rawData.map(item => ({
      projectName: item.name || item.projectName,
      amount: item.amount || item.fundingAmount,
      round: item.round || item.fundingRound,
      investors: Array.isArray(item.investors)
        ? item.investors.join(', ')
        : item.investors,
      date: item.date || item.fundingDate,
      category: item.category || item.sector,
      description: item.description || item.intro,
      url: item.url || `${this.baseURL}/project/${item.id}`
    }));
  }

  /**
   * 获取TEG项目
   */
  async getTEGProjects() {
    try {
      const response = await axios.get(`${this.baseURL}/TGE`, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });

      const $ = cheerio.load(response.data);
      const tegProjects = [];

      $('.tge-item').each((index, element) => {
        const $item = $(element);
        tegProjects.push({
          projectName: $item.find('.project-name').text().trim(),
          tokenSymbol: $item.find('.token-symbol').text().trim(),
          tgeDate: $item.find('.tge-date').text().trim(),
          initialPrice: $item.find('.initial-price').text().trim(),
          totalSupply: $item.find('.total-supply').text().trim(),
          category: $item.find('.category').text().trim(),
          description: $item.find('.description').text().trim(),
          url: this.baseURL + $item.find('a').attr('href')
        });
      });

      return tegProjects;
    } catch (error) {
      console.error('TEG scraping failed:', error.message);
      return [];
    }
  }
}

module.exports = RootDataScraper;

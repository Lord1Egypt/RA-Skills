const axios = require('axios');

const SEC_USER_ID_PATTERN = /\/user\/([^/?]+)/;

function extractSecUserId(url) {
  const match = url.match(SEC_USER_ID_PATTERN);
  if (match) {
    return match[1];
  }
  throw new Error('Invalid URL format. Expected format: https://www.douyin.com/user/{sec_user_id}[?params]');
}

async function douyin_get_user_videos({ url }, config) {
  const apiKey = config.env?.DOUYIN_API_KEY || process.env.DOUYIN_API_KEY;
  const cookie = config.env?.DOUYIN_COOKIE || process.env.DOUYIN_COOKIE;
  const apiUrl = config.env?.DOUYIN_API_URL || process.env.DOUYIN_API_URL || 'https://xueai.szzy.top/api/agi/douyin/user-home-videos';

  if (!apiKey) {
    throw new Error('DOUYIN_API_KEY not configured. Please set DOUYIN_API_KEY in skill configuration.');
  }

  if (!url) {
    throw new Error('URL is required. Please provide the Douyin user homepage URL.');
  }

  const sec_user_id = extractSecUserId(url);

  const douyinHeaders = {
    accept: 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    cookie: cookie || '',
    priority: 'u=1, i',
    referer: `https://www.douyin.com/user/${sec_user_id}?from_tab_name=main&showSubTab=video`,
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
  };

  const requestUrl = apiUrl;

  try {
    const response = await axios.post(requestUrl, {
      url,
      cookie: cookie || undefined,
      apikey: apiKey
    }, {
      headers: douyinHeaders
    });

    if (response.data.success) {
      return {
        success: true,
        message: response.data.message,
        data: response.data.data,
        count: response.data.data?.length || 0
      };
    } else {
      throw new Error(response.data.message || 'Failed to get videos');
    }
  } catch (error) {
    if (error.response) {
      throw new Error(`API error: ${error.response.data.message || error.response.statusText}`);
    } else if (error.request) {
      throw new Error('Network error: Unable to reach the API server');
    } else {
      throw error;
    }
  }
}

module.exports = {
  douyin_get_user_videos
};

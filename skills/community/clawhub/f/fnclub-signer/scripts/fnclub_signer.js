#!/usr/bin/env node
/**
 * 飞牛论坛自动签到脚本 (Node.js版)
 * 支持环境变量或配置文件配置账号信息
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const { CookieJar } = require('tough-cookie');

// 配置
class Config {
  constructor() {
    const configPath = process.env.FNCLUB_CONFIG || path.join(__dirname, 'config.json');
    let configData = {};
    
    if (fs.existsSync(configPath)) {
      try {
        configData = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
        console.log(`[INFO] 已从配置文件加载配置: ${configPath}`);
      } catch (e) {
        console.log(`[WARN] 加载配置文件失败: ${e.message}`);
      }
    }

    this.username = process.env.FNCLUB_USERNAME || configData.username || '';
    this.password = process.env.FNCLUB_PASSWORD || configData.password || '';
    this.baiduApiKey = process.env.BAIDU_OCR_API_KEY || configData.baidu_ocr_api_key || '';
    this.baiduSecretKey = process.env.BAIDU_OCR_SECRET_KEY || configData.baidu_ocr_secret_key || '';
    this.baseUrl = 'https://club.fnnas.com/';
    this.loginUrl = this.baseUrl + 'member.php?mod=logging&action=login';
    this.signUrl = this.baseUrl + 'plugin.php?id=zqlj_sign';
    const dataDir = process.env.FNCLUB_DATA_DIR || __dirname;
    this.cookieFile = path.join(dataDir, 'cookies.json');
    this.tokenCacheFile = path.join(dataDir, 'token_cache.json');
    this.maxRetries = 3;
    this.retryDelay = 2000;
  }

  validate() {
    const missing = [];
    if (!this.username) missing.push('FNCLUB_USERNAME');
    if (!this.password) missing.push('FNCLUB_PASSWORD');
    if (!this.baiduApiKey) missing.push('BAIDU_OCR_API_KEY');
    if (!this.baiduSecretKey) missing.push('BAIDU_OCR_SECRET_KEY');
    if (missing.length > 0) {
      console.log(`[ERROR] 缺少必要配置: ${missing.join(', ')}`);
      return false;
    }
    return true;
  }
}

class FNSignIn {
  constructor(config) {
    this.config = config;
    this.cookieJar = new CookieJar();
    this.axiosInstance = axios.create({ maxRedirects: 5, timeout: 30000 });
  }

  async loadCookies() {
    if (fs.existsSync(this.config.cookieFile)) {
      try {
        const cookies = JSON.parse(fs.readFileSync(this.config.cookieFile, 'utf-8'));
        for (const cookie of cookies) {
          await this.cookieJar.setCookie(`${cookie.name}=${cookie.value}`, this.config.baseUrl);
        }
        console.log('[INFO] 已从文件加载Cookie');
        return true;
      } catch (e) {
        console.log(`[ERROR] 加载Cookie失败: ${e.message}`);
      }
    }
    return false;
  }

  async saveCookies() {
    try {
      const cookies = await this.cookieJar.getCookies(this.config.baseUrl);
      const cookieList = cookies.map(c => ({ name: c.key, value: c.value, domain: c.domain, path: c.path }));
      fs.writeFileSync(this.config.cookieFile, JSON.stringify(cookieList, null, 2));
      console.log('[INFO] Cookie已保存到文件');
      return true;
    } catch (e) {
      console.log(`[ERROR] 保存Cookie失败: ${e.message}`);
      return false;
    }
  }

  async request(url, options = {}) {
    const cookies = await this.cookieJar.getCookies(url);
    const cookieString = cookies.map(c => `${c.key}=${c.value}`).join('; ');
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Cookie': cookieString,
      ...options.headers,
    };
    const response = await this.axiosInstance({ url, method: options.method || 'GET', data: options.data, headers, responseType: options.responseType || 'text' });
    const setCookies = response.headers['set-cookie'];
    if (setCookies) {
      for (const cookie of setCookies) {
        await this.cookieJar.setCookie(cookie, url);
      }
    }
    return response;
  }

  async checkLoginStatus() {
    try {
      const response = await this.request(this.config.baseUrl);
      const $ = cheerio.load(response.data);
      const loginLinks = $('a[href*="member.php?mod=logging&action=login"]').length;
      const usernameInPage = response.data.includes(this.config.username);
      const userCenterLinks = $('a[href*="home.php?mod=space"]').length;
      if ((loginLinks === 0 || usernameInPage) && userCenterLinks > 0) {
        console.log('[INFO] Cookie有效，已登录状态');
        return true;
      }
      console.log('[INFO] Cookie无效或已过期，需要重新登录');
      return false;
    } catch (e) {
      console.log(`[ERROR] 检查登录状态失败: ${e.message}`);
      return false;
    }
  }

  async getAccessToken() {
    if (fs.existsSync(this.config.tokenCacheFile)) {
      try {
        const cache = JSON.parse(fs.readFileSync(this.config.tokenCacheFile, 'utf-8'));
        if (cache.expires_time > Date.now()) {
          console.log('[INFO] 使用缓存的access_token');
          return cache.access_token;
        }
      } catch (e) {}
    }
    try {
      const response = await axios.get('https://aip.baidubce.com/oauth/2.0/token', {
        params: { grant_type: 'client_credentials', client_id: this.config.baiduApiKey, client_secret: this.config.baiduSecretKey },
      });
      const { access_token, expires_in = 2592000 } = response.data;
      fs.writeFileSync(this.config.tokenCacheFile, JSON.stringify({ access_token, expires_time: Date.now() + (expires_in - 86400) * 1000 }));
      console.log('[INFO] access_token已获取并缓存');
      return access_token;
    } catch (e) {
      console.log(`[ERROR] 获取access_token失败: ${e.message}`);
      return null;
    }
  }

  async recognizeCaptcha(captchaUrl) {
    try {
      const imgResponse = await this.request(captchaUrl, { responseType: 'arraybuffer' });
      const base64 = Buffer.from(imgResponse.data).toString('base64');
      const accessToken = await this.getAccessToken();
      if (!accessToken) return null;
      const response = await axios.post(
        `https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=${accessToken}`,
        `image=${encodeURIComponent(base64)}&detect_direction=false&paragraph=false&probability=false`,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      if (response.data.words_result && response.data.words_result.length > 0) {
        const text = response.data.words_result[0].words.replace(/[\s\W]+/g, '');
        console.log(`[INFO] 验证码识别成功: ${text}`);
        return text;
      } else if (response.data.error_code) {
        console.log(`[ERROR] 验证码识别失败: ${response.data.error_code}, ${response.data.error_msg}`);
        return null;
      }
    } catch (e) {
      console.log(`[ERROR] 验证码识别过程出错: ${e.message}`);
    }
    return null;
  }

  async login() {
    for (let retry = 0; retry < this.config.maxRetries; retry++) {
      try {
        const response = await this.request(this.config.loginUrl);
        const $ = cheerio.load(response.data);
        let loginForm = null;
        $('form').each((i, form) => {
          const id = $(form).attr('id') || '';
          if (id.includes('loginform') || id.includes('lsform') || $(form).attr('name') === 'login' || ($(form).attr('action') || '').includes('logging')) {
            loginForm = $(form);
            return false;
          }
        });
        if (!loginForm) loginForm = $('form').first();
        if (!loginForm.length) {
          console.log(`[ERROR] 未找到登录表单，重试(${retry + 1}/${this.config.maxRetries})`);
          await this.sleep(this.config.retryDelay);
          continue;
        }
        const formhash = loginForm.find('input[name="formhash"]').val();
        if (!formhash) {
          console.log(`[ERROR] 未找到formhash，重试(${retry + 1}/${this.config.maxRetries})`);
          await this.sleep(this.config.retryDelay);
          continue;
        }
        const loginData = new URLSearchParams({
          formhash, referer: this.config.baseUrl, loginfield: 'username',
          username: this.config.username, password: this.config.password,
          questionid: '0', answer: '', cookietime: '2592000', loginsubmit: 'true',
        });
        const seccodeverify = loginForm.find('input[name="seccodeverify"]');
        if (seccodeverify.length) {
          console.log('[INFO] 检测到需要验证码，尝试自动识别');
          const seccodeId = seccodeverify.attr('id').replace('seccodeverify_', '');
          const captchaImg = $('img[src*="misc.php?mod=seccode"]');
          if (!captchaImg.length) {
            console.log(`[ERROR] 未找到验证码图片，重试(${retry + 1}/${this.config.maxRetries})`);
            await this.sleep(this.config.retryDelay);
            continue;
          }
          const captchaUrl = this.config.baseUrl + captchaImg.attr('src');
          const captchaText = await this.recognizeCaptcha(captchaUrl);
          if (!captchaText) {
            console.log(`[ERROR] 验证码识别失败，重试(${retry + 1}/${this.config.maxRetries})`);
            await this.sleep(this.config.retryDelay);
            continue;
          }
          loginData.set('seccodeverify', captchaText);
          loginData.set('seccodehash', seccodeId);
        }
        const loginResponse = await this.request(`${this.config.loginUrl}&loginsubmit=yes&inajax=1`, {
          method: 'POST', data: loginData.toString(),
          headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': this.config.baseUrl.replace(/\/$/, ''), 'Referer': this.config.loginUrl },
        });
        if (loginResponse.data.includes('验证码错误')) {
          console.log(`[ERROR] 验证码错误，重试(${retry + 1}/${this.config.maxRetries})`);
          await this.sleep(this.config.retryDelay);
          continue;
        }
        if (loginResponse.data.includes('succeedhandle_') || await this.checkLoginStatus()) {
          console.log(`[INFO] 账号 ${this.config.username} 登录成功`);
          await this.saveCookies();
          return true;
        }
        console.log(`[ERROR] 登录失败，请检查账号密码，重试(${retry + 1}/${this.config.maxRetries})`);
        await this.sleep(this.config.retryDelay);
      } catch (e) {
        console.log(`[ERROR] 登录过程发生错误: ${e.message}，重试(${retry + 1}/${this.config.maxRetries})`);
        await this.sleep(this.config.retryDelay);
      }
    }
    return false;
  }

  async checkSignStatus() {
    try {
      const response = await this.request(this.config.signUrl);
      const $ = cheerio.load(response.data);
      const signBtn = $('.signbtn .btna');
      if (!signBtn.length) return { status: null, param: null };
      const signText = signBtn.text().trim();
      const signLink = signBtn.attr('href') || '';
      const match = signLink.match(/sign=([^&]+)/);
      return { status: signText, param: match ? match[1] : null };
    } catch (e) {
      console.log(`[ERROR] 检查签到状态失败: ${e.message}`);
      return { status: null, param: null };
    }
  }

  async doSign(signParam) {
    try {
      await this.request(`${this.config.signUrl}&sign=${signParam}`);
      const { status } = await this.checkSignStatus();
      if (status === '今日已打卡') {
        console.log('[INFO] 签到成功');
        return true;
      }
      return false;
    } catch (e) {
      console.log(`[ERROR] 签到过程发生错误: ${e.message}`);
      return false;
    }
  }

  async getSignInfo() {
    try {
      const response = await this.request(this.config.signUrl);
      const $ = cheerio.load(response.data);
      const signInfo = {};
      $('div.bm').each((i, div) => {
        if ($(div).find('.bm_h').text().includes('我的打卡动态')) {
          $(div).find('.bm_c li').each((j, li) => {
            const text = $(li).text().trim();
            const match = text.match(/^(.+?)：(.+)$/);
            if (match) signInfo[match[1]] = match[2];
          });
        }
      });
      return signInfo;
    } catch (e) {
      console.log(`[ERROR] 获取签到信息失败: ${e.message}`);
      return {};
    }
  }

  sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

  async run() {
    console.log('===== 开始运行签到脚本 =====');
    await this.loadCookies();
    if (!(await this.checkLoginStatus())) {
      if (!(await this.login())) {
        console.log('[ERROR] 登录失败，签到流程终止');
        return { success: false, error: '登录失败' };
      }
    }
    const { status, param } = await this.checkSignStatus();
    if (!status) {
      console.log('[ERROR] 获取签到状态失败，签到流程终止');
      return { success: false, error: '获取签到状态失败' };
    }
    console.log(`[INFO] 当前签到状态: ${status}`);
    const result = { success: false, already_signed: false };
    if (status === '点击打卡' && param) {
      console.log('[INFO] 开始执行签到...');
      if (await this.doSign(param)) {
        result.success = true;
        result.action = 'signed';
      } else {
        result.error = '签到失败';
      }
    } else if (status === '今日已打卡') {
      console.log('[INFO] 今日已签到，无需重复签到');
      result.success = true;
      result.already_signed = true;
    } else {
      result.error = `未知签到状态: ${status}`;
    }
    const info = await this.getSignInfo();
    if (Object.keys(info).length > 0) {
      result.info = info;
      console.log('===== 签到信息 =====');
      for (const [key, value] of Object.entries(info)) console.log(`${key}: ${value}`);
    }
    return result;
  }
}

async function main() {
  const config = new Config();
  if (!config.validate()) {
    console.log(JSON.stringify({ success: false, error: '配置不完整，请检查环境变量或配置文件' }, null, 2));
    process.exit(1);
  }
  const signer = new FNSignIn(config);
  const result = await signer.run();
  console.log(JSON.stringify(result, null, 2));
  if (result.success) {
    console.log('===== 签到脚本执行成功 =====');
    process.exit(0);
  } else {
    console.log('===== 签到脚本执行失败 =====');
    process.exit(1);
  }
}

main().catch(e => {
  console.log(JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});

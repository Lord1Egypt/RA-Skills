/**
 * eBay 操作机器人 - CDP 直连版
 * 通过 WebSocket 直接发送 Chrome DevTools Protocol 命令
 */

const ads = require('./ads_api');
const WebSocket = require('ws');
const http = require('http');
const config = require('./config');

function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function randPick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

function loadKeywords(path) {
  try {
    const fs = require('fs');
    if (fs.existsSync(path)) {
      const lines = fs.readFileSync(path, 'utf-8').split('\n').map(l => l.trim()).filter(l => l);
      if (lines.length > 0) return lines;
    }
  } catch (e) {}
  return [
    'basketball jersey', 'football jersey', 'baseball jersey',
    'NBA jerseys', 'NFL jerseys', 'MLB jerseys',
    'custom sports jersey', 'team apparel', 'sports hoodies',
    'vintage sportswear', 'college football gear',
  ];
}

class CdpEbayBot {
  constructor(userId) {
    this.userId = userId;
    this.browserWs = null;
    this.pageWs = null;
    this.msgId = 0;
    this.pending = {};
    this.pagePending = {};
    this.debugPort = null;
    this.browserData = null;
    this.keywords = [];
  }

  async _initWs(url, handlers) {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(url);
      ws.on('open', () => {
        if (ws.readyState === WebSocket.OPEN) {
          console.log(`  [WS] connected, readyState=${ws.readyState}`);
          resolve(ws);
        } else {
          const check = setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
              clearInterval(check);
              console.log(`  [WS] connected, readyState=${ws.readyState}`);
              resolve(ws);
            } else if (ws.readyState === WebSocket.CLOSED || ws.readyState === WebSocket.CLOSING) {
              clearInterval(check);
              reject(new Error(`WS closed before OPEN, state=${ws.readyState}`));
            }
          }, 100);
        }
      });
      ws.on('error', (e) => { reject(e); });
      ws.on('message', (data) => {
        const msg = JSON.parse(data.toString());
        if (msg.id && handlers.pending[msg.id]) {
          clearTimeout(handlers.pending[msg.id].timer);
          handlers.pending[msg.id].resolve(msg.result || msg);
          delete handlers.pending[msg.id];
        }
      });
    });
  }

  async connect() {
    this.browserData = await ads.startBrowser(this.userId);
    this.debugPort = this.browserData.debug_port;

    this.browserWs = await this._initWs(this.browserData.ws?.puppeteer, { pending: this.pending });
    console.log('  浏览器连接成功, readyState=' + this.browserWs.readyState);

    await new Promise(r => setTimeout(r, 3000));

    console.log('  创建新页面...');
    const newTarget = await this._cdpSend('Target.createTarget', { url: 'about:blank' });
    console.log('  新页面 target:', newTarget?.targetId);
    await new Promise(r => setTimeout(r, 1000));

    const pageList = await this._getPageList();
    const newPage = pageList.find(p => p.url === 'about:blank' && p.type === 'page');
    if (!newPage) throw new Error('无法创建新页面');

    this.pageWs = await this._initWs(newPage.webSocketDebuggerUrl, { pending: this.pagePending });
    console.log('  页面连接成功, readyState=' + this.pageWs.readyState);

    await new Promise(r => setTimeout(r, 1000));

    this.keywords = loadKeywords(config.KEYWORDS_FILE);
    return this;
  }

  _getPageList() {
    return new Promise((resolve) => {
      http.get(`http://127.0.0.1:${this.debugPort}/json`, (res) => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => { try { resolve(JSON.parse(body)); } catch(e) { resolve([]); } });
      }).on('error', () => resolve([]));
    });
  }

  _cdpSend(method, params = {}) {
    return new Promise((resolve, reject) => {
      const sendIt = () => {
        if (!this.browserWs || this.browserWs.readyState !== WebSocket.OPEN) {
          reject(new Error(`Browser WS not connected (state: ${this.browserWs?.readyState})`));
          return;
        }
        const id = ++this.msgId;
        const timer = setTimeout(() => {
          delete this.pending[id];
          reject(new Error(`CDP timeout: ${method}`));
        }, 25000);
        this.pending[id] = { resolve, timer };
        this.browserWs.send(JSON.stringify({ id, method, params }));
      };
      if (!this.browserWs || this.browserWs.readyState !== WebSocket.OPEN) {
        console.log(`  [CDP] browserWs not ready, waiting 2s...`);
        setTimeout(sendIt, 2000);
      } else {
        sendIt();
      }
    });
  }

  _pSend(method, params = {}) {
    return new Promise((resolve, reject) => {
      const sendIt = () => {
        if (!this.pageWs || this.pageWs.readyState !== WebSocket.OPEN) {
          reject(new Error(`Page WS not connected (state: ${this.pageWs?.readyState})`));
          return;
        }
        const id = ++this.msgId;
        const timer = setTimeout(() => {
          delete this.pagePending[id];
          reject(new Error(`Page CDP timeout: ${method}`));
        }, 25000);
        this.pagePending[id] = { resolve, timer };
        this.pageWs.send(JSON.stringify({ id, method, params }));
      };
      if (!this.pageWs || this.pageWs.readyState !== WebSocket.OPEN) {
        setTimeout(sendIt, 2000);
      } else {
        sendIt();
      }
    });
  }

  async _navigate(url) {
    await this._pSend('Page.navigate', { url });
    await delay(4000);
  }

  async _waitForPageReady(timeout = 8000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const ready = await this._pSend('Runtime.evaluate', {
        expression: 'document.readyState',
        returnByValue: true,
      });
      if (ready?.result?.value === 'complete') return true;
      await delay(1000);
    }
    return false;
  }

  async _scrollPage(steps = 3) {
    for (let i = 0; i < steps; i++) {
      const dy = randInt(250, 700);
      await this._pSend('Runtime.evaluate', { expression: `window.scrollBy(0, ${dy})` });
      await delay(randInt(1200, 3000));
      if (Math.random() < 0.3 && i > 0) {
        await this._pSend('Runtime.evaluate', { expression: `window.scrollBy(0, ${-randInt(50, 200)})` });
        await delay(randInt(800, 1500));
      }
    }
  }

  async _getItemLinks(maxItems = 8) {
    const result = await this._pSend('Runtime.evaluate', {
      expression: `
        (function() {
          const as = Array.from(document.querySelectorAll('a'));
          return as
            .filter(a => a.href.includes('/itm/') && !a.href.includes('Shop on eBay'))
            .slice(0, ${maxItems})
            .map(a => a.href);
        })()
      `,
      returnByValue: true,
    });
    return result?.result?.value || [];
  }

  async _typeSearch(keyword) {
    await this._pSend('Runtime.evaluate', {
      expression: "const i = document.querySelector('#gh-ac'); if(i){ i.value = ''; i.focus(); }",
      returnByValue: true,
    });
    await delay(400);
    for (const char of keyword) {
      await this._pSend('Input.dispatchKeyEvent', {
        type: 'keyDown', text: char, key: char, code: 'Key' + char.toUpperCase(),
      });
      await delay(randInt(30, 120));
    }
    await delay(300);
    await this._pSend('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', keyCode: 13 });
    await this._pSend('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', keyCode: 13 });
  }

  async _tryWatch() {
    const result = await this._pSend('Runtime.evaluate', {
      expression: `
        (function() {
          const heart = document.querySelector('.x-watch-heart-btn');
          if (heart) { heart.click(); return 'clicked .x-watch-heart-btn'; }
          const dpBtn = document.querySelector('.dp-watchlist-toggle-button');
          if (dpBtn) { dpBtn.click(); return 'clicked .dp-watchlist-toggle-button'; }
          const hearts = document.querySelectorAll('svg[aria-label="Watchlist"], svg[data-test-id="heart"]');
          for (const svg of hearts) {
            const btn = svg.closest('button') || svg.closest('a');
            if (btn && btn.offsetParent !== null) { btn.click(); return 'clicked heart'; }
          }
          return 'not_found';
        })()
      `,
      returnByValue: true,
    });
    return result?.result?.value;
  }

  async _tryAddToCart() {
    const result = await this._pSend('Runtime.evaluate', {
      expression: `
        (function() {
          const atcBtn = document.getElementById('atcBtn_btn_1');
          if (atcBtn && atcBtn.offsetParent !== null) { atcBtn.click(); return 'clicked #atcBtn_btn_1'; }
          const allAs = document.querySelectorAll('a.ux-call-to-action');
          for (const a of allAs) {
            if (a.innerText?.toLowerCase().includes('add to cart')) { a.click(); return 'clicked cart a'; }
          }
          return 'not_found';
        })()
      `,
      returnByValue: true,
    });
    return result?.result?.value;
  }

  async doOneSearchCycle(keyword) {
    await this._navigate('https://www.ebay.com');
    await delay(randInt(2000, 5000));
    await this._scrollPage(2);

    await this._typeSearch(keyword);
    await delay(5000);
    await this._waitForPageReady(8000);

    const itemLinks = await this._getItemLinks(6);
    if (itemLinks.length === 0) {
      console.log(`  未找到商品链接`);
      return { searched: true, itemsViewed: 0, favorited: 0, addedToCart: 0 };
    }

    console.log(`  找到 ${itemLinks.length} 个商品链接`);

    const numBrowse = Math.min(randInt(2, 4), itemLinks.length);
    const shuffled = itemLinks.sort(() => Math.random() - 0.5).slice(0, numBrowse);

    let favorited = 0;
    let addedToCart = 0;

    for (const itemUrl of shuffled) {
      try {
        await this._navigate(itemUrl);
        await this._waitForPageReady(8000);
        await this._scrollPage(3);

        await this._pSend('Runtime.evaluate', { expression: `window.scrollTo(0, ${randInt(100, 300)})` });
        await delay(randInt(1500, 4000));

        if (Math.random() < 0.6) {
          const r = await this._tryWatch();
          if (r && r !== 'not_found') { favorited++; console.log(`  收藏成功`); await delay(randInt(1500, 3000)); }
        }

        if (Math.random() < 0.35) {
          const r = await this._tryAddToCart();
          if (r && r !== 'not_found') { addedToCart++; console.log(`  加入购物车成功`); await delay(randInt(1500, 4000)); }
        }

        await delay(randInt(8000, 20000));

      } catch(e) {
        console.warn(`  商品页出错: ${e.message.slice(0, 80)}`);
      }
    }

    return { searched: true, itemsViewed: numBrowse, favorited, addedToCart };
  }

  async runActiveSession(runtimeMs) {
    const startTime = Date.now();
    const endTime = startTime + runtimeMs;
    let searchesDone = 0;
    let totalFavorited = 0;
    let totalAddedToCart = 0;

    console.log(`  开始活跃任务，预计运行时长 ${Math.round(runtimeMs / 60000)} 分钟`);

    try {
      while (Date.now() < endTime) {
        const keyword = randPick(this.keywords);
        console.log(`  [搜索 ${searchesDone + 1}] "${keyword}"`);

        try {
          const result = await this.doOneSearchCycle(keyword);
          searchesDone++;
          totalFavorited += result.favorited;
          totalAddedToCart += result.addedToCart;
          console.log(`  本轮: 浏览${result.itemsViewed}个, 收藏${result.favorited}, 加购${result.addedToCart}`);
        } catch(e) {
          console.warn(`  搜索循环出错: ${e.message.slice(0, 100)}`);
        }

        const remaining = endTime - Date.now();
        if (remaining < 60000) { console.log('  剩余不足1分钟，结束'); break; }

        const pause = randInt(10000, 25000);
        console.log(`  休息 ${Math.round(pause / 1000)} 秒...`);
        await delay(pause);
      }
    } catch(e) {
      console.error('  运行时出错:', e.message);
    }

    console.log(`  完成 ${searchesDone} 轮搜索，合计收藏 ${totalFavorited} 个，加购 ${totalAddedToCart} 个`);
    return { searchesDone, totalFavorited, totalAddedToCart };
  }

  async close() {
    if (this.pageWs) { try { this.pageWs.close(); } catch(e) {} }
    if (this.browserWs) { try { this.browserWs.close(); } catch(e) {} }
  }
}

module.exports = CdpEbayBot;

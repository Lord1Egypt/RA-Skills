/**
 * 滴滴出行优惠券自动领取脚本 v5
 * 策略：打开页面 → 调用 MPX 组件 autoGetCoupon() → 读取结果
 * 与手工点击等价，耗时约 3~5s
 *
 * 依赖说明：
 *   ws 模块由 OpenClaw workspace 的 node_modules 提供（与脚本同仓库）。
 *   路径 ../../../node_modules/ws/wrapper.mjs 指向 workspace 根目录的 node_modules，
 *   这是本技能设计的运行环境（skills/didi-coupon-auto/scripts/ 目录下执行）。
 *   如需独立运行，请在脚本目录执行 `npm install ws` 后修改为 `import { WebSocket } from 'ws'`。
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// 优先使用 workspace 内置 ws；若不可用则降级到全局安装的 ws
const __dir = path.dirname(fileURLToPath(import.meta.url));
const wsPath = path.resolve(__dir, '../../../node_modules/ws/wrapper.mjs');
const { WebSocket } = await import(wsPath).catch(() => import('ws'));
const COUPON_URL = 'https://vv.didi.cn/a8ZdG0j?source_id=88446DIDI88446tkmmchild1001&ref_from=dunion';
const LOG_DIR    = path.join(__dir, '../logs');
const DELAY      = ms => new Promise(r => setTimeout(r, ms));

// ─── CDP 连接 ──────────────────────────────────────────────────────────────────
async function getBrowserTarget() {
  const res = await fetch('http://127.0.0.1:18800/json');
  const targets = await res.json();
  return targets.find(t => t.type === 'page' && t.url?.includes('didi.cn') && !t.url?.includes('devtools'))
      || targets.find(t => t.type === 'page' && !t.url?.includes('devtools'));
}

function cdpClient(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 1;
    const send = (method, params = {}) => new Promise((res, rej) => {
      const msgId = id++;
      const onMsg = d => {
        const m = JSON.parse(d);
        if (m.id === msgId) { ws.off('message', onMsg); m.error ? rej(new Error(m.error.message)) : res(m.result || {}); }
      };
      ws.on('message', onMsg);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
    ws.on('open', () => resolve({ ws, send }));
    ws.on('error', reject);
  });
}

async function evaluate(send, expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text || 'JS error');
  return r.result?.value;
}

// ─── 拦截 API 响应 ────────────────────────────────────────────────────────────
async function watchReceiveResult(ws, send, timeoutMs = 8000) {
  await send('Network.enable', {});
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve(null), timeoutMs);
    const pending = new Map();
    ws.on('message', async d => {
      const m = JSON.parse(d);
      if (m.method === 'Network.requestWillBeSent') {
        const url = m.params.request?.url || '';
        if (url.includes('reward/receive') || url.includes('reward/list')) {
          pending.set(m.params.requestId, url);
        }
      }
      if (m.method === 'Network.loadingFinished' && pending.has(m.params.requestId)) {
        try {
          const body = await send('Network.getResponseBody', { requestId: m.params.requestId });
          const data = JSON.parse(body.body || '{}');
          if (pending.get(m.params.requestId).includes('reward/receive')) {
            clearTimeout(timer);
            resolve(data);
          }
        } catch {}
        pending.delete(m.params.requestId);
      }
    });
  });
}

// ─── 查询已领券列表 ───────────────────────────────────────────────────────────
async function watchListResult(ws, send, timeoutMs = 6000) {
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve(null), timeoutMs);
    const pending = new Map();
    ws.on('message', async d => {
      const m = JSON.parse(d);
      if (m.method === 'Network.requestWillBeSent') {
        if (m.params.request?.url?.includes('reward/list')) {
          pending.set(m.params.requestId, true);
        }
      }
      if (m.method === 'Network.loadingFinished' && pending.has(m.params.requestId)) {
        try {
          const body = await send('Network.getResponseBody', { requestId: m.params.requestId });
          const data = JSON.parse(body.body || '{}');
          if (data?.data?.rewards) { clearTimeout(timer); resolve(data); }
        } catch {}
        pending.delete(m.params.requestId);
      }
    });
  });
}

// ─── 触发领取（调用 MPX 组件方法，等同手工点击）─────────────────────────────────
async function triggerClaim(send) {
  return evaluate(send, `
    (async () => {
      // 方法1：调用 MPX 组件的 autoGetCoupon()（最可靠）
      const el = document.querySelector('[class*="host-_490de1ba"]');
      const vm = el?.__mpxProxy?.target;
      if (vm?.autoGetCoupon) {
        vm.autoGetCoupon();
        return 'autoGetCoupon';
      }
      // 方法2：调用 getCoupon()
      if (vm?.getCoupon) {
        vm.getCoupon();
        return 'getCoupon';
      }
      // 方法3：直接点击按钮元素
      const btn = document.querySelector('[class*="get-coupon-btn"]:not([class*="wrapper"])');
      if (btn) { btn.click(); return 'click'; }
      return 'not_found';
    })()
  `);
}

// ─── 检测当前页面状态 ──────────────────────────────────────────────────────────
async function getPageStatus(send) {
  return evaluate(send, `
    (() => {
      const el = document.querySelector('[class*="host-_490de1ba"]');
      const vm = el?.__mpxProxy?.target;
      if (vm?.getPageStatus) return vm.getPageStatus();
      const text = document.body.innerText;
      if (text.includes('登录领取')) return 'needLogin';
      if (text.includes('已领取') || text.includes('去使用')) return 'claimed';
      if (document.querySelector('[class*="get-coupon-btn"]:not([class*="wrapper"])')) return 'canClaim';
      return 'unknown';
    })()
  `);
}

function saveLog(data) {
  if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  fs.writeFileSync(path.join(LOG_DIR, `claim_${today}.json`), JSON.stringify(data, null, 2), 'utf8');
}

// ─── 格式化券摘要（用于定时推送） ─────────────────────────────────────────────
function buildSummary(rewards = [], message = '') {
  if (!rewards.length) return message || '无券信息';

  // 统计金额：元券直接累加，折扣券计最高抵扣值
  const total = rewards.reduce((s, r) => {
    const cap = r.coupon?.max_benefit_capacity;
    if (!cap) return s;
    return s + Number(cap.value || 0);
  }, 0);

  // 按券名关键词分组
  const groups = {};
  for (const r of rewards) {
    const c = r.coupon;
    const cap = c.max_benefit_capacity;
    const label = `${cap.value}${cap.unit}${c.usage_limit ? ' ' + c.usage_limit : ''}`;
    const key = c.name.includes('快车') ? '🚗 快车'
              : c.name.includes('顺风') ? '🤝 顺风车'
              : c.name.includes('火车') ? '🚄 火车票'
              : c.name.includes('代驾') ? '🌙 代驾'
              : c.name.includes('包车') || c.name.includes('跨城') ? '🛣 跨城/包车'
              : c.name.includes('取货') || c.name.includes('单独') ? '📦 取送件'
              : '🎟 其他';
    if (!groups[key]) groups[key] = [];
    groups[key].push(`    · ${c.name}  ${label}`);
  }

  const lines = [];
  for (const [group, items] of Object.entries(groups)) {
    lines.push(group);
    lines.push(...items);
  }

  return [
    `🎫 共 ${rewards.length} 张券，最高立减合计 ¥${total}`,
    ...lines
  ].join('\n');
}

// ─── 主流程 ───────────────────────────────────────────────────────────────────
async function main() {
  const t0 = Date.now();
  console.log('🚕 滴滴出行优惠券自动领取 v5');
  console.log(`⏰ ${new Date().toLocaleString('zh-CN')}`);
  console.log('─'.repeat(45));

  const target = await getBrowserTarget();
  if (!target) throw new Error('未找到浏览器页面，请先启动 OpenClaw 浏览器');

  const { ws, send } = await cdpClient(target.webSocketDebuggerUrl);
  const result = { success: false, message: '', summary: '', coupons: [], totalMs: 0, timestamp: new Date().toISOString() };

  try {
    // 1. 启用网络监听（用于捕获 API 响应）
    await send('Network.enable', {});

    // 2. 确保在滴滴页面
    const onDidi = target.url?.includes('didi.cn');
    if (!onDidi) {
      console.log('🌐 导航到领券页...');
      await send('Page.navigate', { url: COUPON_URL });
      await DELAY(3500);
    } else {
      console.log('✅ 已在滴滴页面');
    }

    // 3. 检测页面状态
    const status = await getPageStatus(send);
    console.log(`📋 页面状态: ${status}`);

    if (status === 'needLogin') {
      result.message = '⚠️ 需要登录滴滴账号，请打开浏览器完成登录后重新运行';
      console.log(result.message);
      return result;
    }

    // 4. 已领取状态：跳过点击，直接拉券列表
    if (status === 'claimed') {
      console.log('✅ 页面显示已领取，直接查询券列表...');
      result.success = true;
      result.message = '今日已领取 ✅';
      // 刷新页面触发 list API
      const listPromise = watchListResult(ws, send, 8000);
      await send('Page.reload', {});
      const listResp = await listPromise;
      const rewards = listResp?.data?.rewards || [];
      result.coupons = rewards.map(r => ({
        name: r.coupon.name,
        benefit: `${r.coupon.max_benefit_capacity.value}${r.coupon.max_benefit_capacity.unit}`,
        usage: r.coupon.usage_limit || '',
        expire: r.coupon.expire_time
      }));
      result.summary = buildSummary(rewards, result.message);
      console.log(`\n✅ ${result.message}\n\n${result.summary}`);
      return result;
    }

    // 5. 可领取：同时监听 receive + list API，然后触发点击
    const receivePromise = watchReceiveResult(ws, send, 8000);
    const listPromise    = watchListResult(ws, send, 10000);

    console.log('🖱  触发领取...');
    const method = await triggerClaim(send);
    console.log(`   方式: ${method}`);

    // 6. 等待 receive API 响应
    const receiveResp = await receivePromise;
    if (receiveResp) {
      console.log(`   errno=${receiveResp.errno} msg="${receiveResp.errmsg}"`);
      if (receiveResp.errno === 0) {
        result.success = true;
        result.message = '领取成功 🎉';
      } else if (receiveResp.errno === 3000030009) {
        result.success = true;
        result.message = '今日已领取 ✅';
      } else {
        result.message = `领取失败(${receiveResp.errno}): ${receiveResp.errmsg}`;
        result.success = false;
      }
    } else {
      result.message = '今日已领取 ✅';
      result.success = true;
    }

    // 7. 等待券列表
    const listResp = await listPromise;
    const rewards = listResp?.data?.rewards || [];
    result.coupons = rewards.map(r => ({
      name:    r.coupon.name,
      benefit: `${r.coupon.max_benefit_capacity.value}${r.coupon.max_benefit_capacity.unit}`,
      usage:   r.coupon.usage_limit || '',
      expire:  r.coupon.expire_time
    }));
    result.summary = buildSummary(rewards, result.message);

    // 7. 打印结果
    console.log(`\n${result.success ? '✅' : '❌'} ${result.message}`);
    console.log('\n' + result.summary);

  } catch (e) {
    result.error = e.message;
    console.error('❌ 错误:', e.message);
  } finally {
    result.totalMs = Date.now() - t0;
    saveLog(result);
    ws.close();
    console.log(`\n⏱  耗时 ${result.totalMs}ms`);
  }
  return result;
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });

#!/usr/bin/env node
/**
 * 永东直通巴士 API 查票脚本
 * 用法: node eebus_query.js [日期] [上客点] [下客点]
 * 示例: node eebus_query.js 2026-05-01 旺角油麻地 莲塘口岸
 */

const https = require('https');

// 城市和站点的 ID 映射
const CITY_IDS = {
  '香港': 2, '澳门': 3, '深圳': 4, '深圳龙岗': 5,
  '广州': 6, '花都': 7, '中山': 8, '佛山': 9,
  '肇庆': 10, '顺德': 11, '番禺': 12, '清远': 13,
  '江门': 14, '新会': 15, '台山': 16, '鹤山': 17,
  '九江\\西樵': 18, '惠州': 19, '珠海': 20, '大鹏湾': 21, '东莞': 22
};

// 站点 ID（需要从 API 动态获取，这里放常用的）
const STOP_IDS = {
  '旺角油麻地': 34596236,
  '莲塘口岸': 34596036,
  '深圳湾口岸': 34596034,
  '太子': 34596238,
  '观塘APM': 34596240,
  '钻石山': 34596242,
  '屯门 V City': 34596246,
  '尖沙咀(中港城)': 34596237,
  '葵芳新都会广场(NR332巴士站前)': 34596239,
};

// HMAC-MD5 实现（从源码提取）
function hmacMd5(input) {
  var r = 8;
  function d(n, e) {
    n[e >> 5] |= 128 << e % 32;
    n[(e + 64 >>> 9 << 4) + 14] = e;
    for (var i = 1732584193, a = -271733879, u = -1732584194, o = 271733878, h = 0; h < n.length; h += 16) {
      var t = i, g = a, c = u, f = o;
      i = p(i, a, u, o, n[h + 0], 7, -680876936);
      o = p(o, i, a, u, n[h + 1], 12, -389564586);
      u = p(u, o, i, a, n[h + 2], 17, 606105819);
      a = p(a, u, o, i, n[h + 3], 22, -1044525330);
      i = p(i, a, u, o, n[h + 4], 7, -176418897);
      o = p(o, i, a, u, n[h + 5], 12, 1200080426);
      u = p(u, o, i, a, n[h + 6], 17, -1473231341);
      a = p(a, u, o, i, n[h + 7], 22, -45705983);
      i = p(i, a, u, o, n[h + 8], 7, 1770035416);
      o = p(o, i, a, u, n[h + 9], 12, -1958414417);
      u = p(u, o, i, a, n[h + 10], 17, -42063);
      a = p(a, u, o, i, n[h + 11], 22, -1990404162);
      i = p(i, a, u, o, n[h + 12], 7, 1804603682);
      o = p(o, i, a, u, n[h + 13], 12, -40341101);
      u = p(u, o, i, a, n[h + 14], 17, -1502002290);
      a = p(a, u, o, i, n[h + 15], 22, 1236535329);
      i = S(i, a, u, o, n[h + 1], 5, -165796510);
      o = S(o, i, a, u, n[h + 6], 9, -1069501632);
      u = S(u, o, i, a, n[h + 11], 14, 643717713);
      a = S(a, u, o, i, n[h + 0], 20, -373897302);
      i = S(i, a, u, o, n[h + 5], 5, -701558691);
      o = S(o, i, a, u, n[h + 10], 9, 38016083);
      u = S(u, o, i, a, n[h + 15], 14, -660478335);
      a = S(a, u, o, i, n[h + 4], 20, -405537848);
      i = S(i, a, u, o, n[h + 9], 5, 568446438);
      o = S(o, i, a, u, n[h + 14], 9, -1019803690);
      u = S(u, o, i, a, n[h + 3], 14, -187363961);
      a = S(a, u, o, i, n[h + 8], 20, 1163531501);
      i = S(i, a, u, o, n[h + 13], 5, -1444681467);
      o = S(o, i, a, u, n[h + 2], 9, -51403784);
      u = S(u, o, i, a, n[h + 7], 14, 1735328473);
      a = S(a, u, o, i, n[h + 12], 20, -1926607734);
      i = Z(i, a, u, o, n[h + 5], 4, -378558);
      o = Z(o, i, a, u, n[h + 8], 11, -2022574463);
      u = Z(u, o, i, a, n[h + 11], 16, 1839030562);
      a = Z(a, u, o, i, n[h + 14], 23, -35309556);
      i = Z(i, a, u, o, n[h + 1], 4, -1530992060);
      o = Z(o, i, a, u, n[h + 4], 11, 1272893353);
      u = Z(u, o, i, a, n[h + 7], 16, -155497632);
      a = Z(a, u, o, i, n[h + 10], 23, -1094730640);
      i = Z(i, a, u, o, n[h + 13], 4, 681279174);
      o = Z(o, i, a, u, n[h + 0], 11, -358537222);
      u = Z(u, o, i, a, n[h + 3], 16, -722521979);
      a = Z(a, u, o, i, n[h + 6], 23, 76029189);
      i = Z(i, a, u, o, n[h + 9], 4, -640364487);
      o = Z(o, i, a, u, n[h + 12], 11, -421815835);
      u = Z(u, o, i, a, n[h + 15], 16, 530742520);
      a = Z(a, u, o, i, n[h + 2], 23, -995338651);
      i = m(i, a, u, o, n[h + 0], 6, -198630844);
      o = m(o, i, a, u, n[h + 7], 10, 1126891415);
      u = m(u, o, i, a, n[h + 14], 15, -1416354905);
      a = m(a, u, o, i, n[h + 5], 21, -57434055);
      i = m(i, a, u, o, n[h + 12], 6, 1700485571);
      o = m(o, i, a, u, n[h + 3], 10, -1894986606);
      u = m(u, o, i, a, n[h + 10], 15, -1051523);
      a = m(a, u, o, i, n[h + 1], 21, -2054922799);
      i = m(i, a, u, o, n[h + 8], 6, 1873313359);
      o = m(o, i, a, u, n[h + 15], 10, -30611744);
      u = m(u, o, i, a, n[h + 6], 15, -1560198380);
      a = m(a, u, o, i, n[h + 13], 21, 1309151649);
      i = m(i, a, u, o, n[h + 4], 6, -145523070);
      o = m(o, i, a, u, n[h + 11], 10, -1120210379);
      u = m(u, o, i, a, n[h + 2], 15, 718787259);
      a = m(a, u, o, i, n[h + 9], 21, -343485551);
      i = C(i, t);
      a = C(a, g);
      u = C(u, c);
      o = C(o, f)
    }
    return [i, a, u, o]
  }
  function l(n, e, i, a, u, o) { return C(f(C(C(e, n), C(a, o)), u), i) }
  function p(n, e, i, a, u, o, h) { return l(e & i | ~e & a, n, e, u, o, h) }
  function S(n, e, i, a, u, o, h) { return l(e & a | i & ~a, n, e, u, o, h) }
  function Z(n, e, i, a, u, o, h) { return l(e ^ i ^ a, n, e, u, o, h) }
  function m(n, e, i, a, u, o, h) { return l(i ^ (e | ~a), n, e, u, o, h) }
  function C(n, e) { var i = (65535 & n) + (65535 & e), a = (n >> 16) + (e >> 16) + (i >> 16); return a << 16 | 65535 & i }
  function f(n, e) { return n << e | n >>> 32 - e }
  function D(n) { for (var e = [], i = (1 << r) - 1, a = 0; a < n.length * r; a += r) e[a >> 5] |= (n.charCodeAt(a / r) & i) << a % 32; return e }

  // s() - HMAC-MD5
  var e = [859202913, 892560440, 943153458, 909193781, 962736692, 811884857, 858874416, 1647338807];
  var i = e.length, a = Array(i);
  for (var u = 0; u < i; u++) a[i - u - 1] = e[u];
  a.length > 16 && (a = d(a, 32 * r));
  var o = Array(16), h = Array(16);
  for (u = 0; u < 16; u++) { o[u] = 909522486 ^ a[u]; h[u] = 1549556828 ^ a[u] }
  var t = d(o.concat(D(input)), 512 + input.length * r);
  var g = d(h.concat(t), 640);
  var s = "0123456789abcdef", l2 = "";
  for (u = 0; u < 4 * g.length; u++) l2 += s.charAt(g[u >> 2] >> u % 4 * 8 + 4 & 15) + s.charAt(g[u >> 2] >> u % 4 * 8 & 15);
  return l2;
}

function generateToken() {
  const chars = '0123456789abcdefghijklmnopqrstuvwxyz';
  let token = '';
  for (let i = 0; i < 32; i++) token += chars[Math.floor(Math.random() * chars.length)];
  return token;
}

function makeRequest(method, path, body, token) {
  return new Promise((resolve, reject) => {
    const timestamp = Date.now().toString();
    const nonce = Math.random().toString(36).substring(2);
    const signature = hmacMd5(token + timestamp + nonce);

    const options = {
      hostname: 'www.myeebus.com',
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'token': token,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature,
        'language': 'zh_CN',
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error('Parse error: ' + data)); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function queryTickets(date, fromStop, toStop, fromCity, toCity) {
  const token = generateToken();
  
  // 自动推导城市
  const HK_STOPS = ['旺角油麻地', '太子', '观塘APM', '钻石山', '屯门 V City', '尖沙咀(中港城)', '葵芳新都会广场(NR332巴士站前)'];
  const SZ_STOPS = ['莲塘口岸', '深圳湾口岸'];
  
  if (!fromCity) fromCity = HK_STOPS.includes(fromStop) ? '香港' : SZ_STOPS.includes(fromStop) ? '深圳' : undefined;
  if (!toCity) toCity = fromCity === '香港' ? '深圳' : fromCity === '深圳' ? '香港' : undefined;
  
  const fromCityId = CITY_IDS[fromCity];
  const toCityId = CITY_IDS[toCity];
  const fromStopId = STOP_IDS[fromStop];
  const toStopId = STOP_IDS[toStop];

  if (!fromCityId || !toCityId) throw new Error('城市名不识别');
  if (!fromStopId || !toStopId) throw new Error('站点名不识别，可用: ' + Object.keys(STOP_IDS).join(', '));

  console.log(`查询: ${fromStop} → ${toStop} (${date})`);

  // Step 1: 保存查询参数
  const r1 = await makeRequest('POST', '/BusManagement/ydy/saveOrderQueryParam.do', {
    open: false,
    requestedMoneyCategory: 'CNY',
    goAndBack: false,
    termsPrivacyPolicy: 'false',
    travelCategory: 'oneway',
    travelList: [{
      onBoardCityName: fromCityId,
      offBoardCityName: toCityId,
      onBoardStopName: fromStopId,
      offBoardStopName: toStopId,
      takeBusDate: date
    }]
  }, token);

  if (!r1.success) { console.error('Step1 失败:', r1.message); return; }
  const preOrderId = r1.data.preOrderId || r1.data;

  // Step 2: 分页查询所有班次
  let allTickets = [];
  let currentPage = 0;
  let hasMore = true;

  while (hasMore) {
    const r2 = await makeRequest('POST', `/BusManagement/ydy/queryAndUpdateTravelInfo.do?v=${Date.now() % 100}`, {
      preOrderId: String(preOrderId),
      travelIndex: '1',
      currentPage: currentPage
    }, token);

    if (!r2.success) { console.error('Step2 失败:', r2.message); return; }

    const tickets = r2.data?.travelTicketList || [];
    allTickets = allTickets.concat(tickets);

    if (process.env.DEBUG) {
      console.log(`[DEBUG] Page ${currentPage}: got ${tickets.length}, totalPage=${r2.data?.totalPage}, totalCount=${r2.data?.totalCount}, currentPage=${r2.data?.currentPage}`);
    }

    const totalPage = r2.data?.totalPage || 1;
    currentPage++;
    hasMore = tickets.length > 0 && currentPage < 50; // keep fetching until empty page
  }

  if (allTickets.length === 0) {
    console.log('没有找到班次');
    return;
  }

  const tickets = allTickets;
  console.log(`\n找到 ${tickets.length} 个班次:\n`);
  console.log('出发     到达     成人  长者  儿童  状态');
  console.log('─'.repeat(45));
  for (const t of tickets) {
    const reservable = t.reservable ? '有票' : '已满';
    const adult = t.adultPrice || '?';
    const elder = t.oldPrice || '?';
    const child = t.childPrice || '?';
    const onTime = (t.onBoardStop?.time || '').padEnd(8);
    const offTime = (t.offBoardStop?.time || '').padEnd(8);
    const seats = t.remainSeat || '?';
    console.log(`${onTime} ${offTime} ¥${String(adult).padEnd(4)} ¥${String(elder).padEnd(4)} ¥${String(child).padEnd(4)} 余${seats}座  ${reservable}`);
  }
  
  // 也打印原始第一条数据方便调试
  if (process.env.DEBUG && tickets[0]) {
    console.log('\n[DEBUG] 第一条数据结构:');
    console.log(JSON.stringify(tickets[0], null, 2));
  }
}

// 主程序
const args = process.argv.slice(2);
const date = args[0] || new Date().toISOString().split('T')[0];
const from = args[1] || '旺角油麻地';
const to = args[2] || '莲塘口岸';

queryTickets(date, from, to).catch(console.error);

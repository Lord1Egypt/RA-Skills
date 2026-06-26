#!/usr/bin/env node
/**
 * 中国效率工具集 - China Productivity Toolkit
 * 免费公开API，无需密钥
 */
const https = require('https');
const http = require('http');

function fetch(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, { headers: { 'User-Agent': 'ChinaToolkit/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(data); }
      });
    }).on('error', reject);
  });
}

// ============ 快递查询 ============
async function expressTracking(trackingNumber, companyCode) {
  const companyMap = {
    'SF': 'shunfeng', '顺丰': 'shunfeng',
    'ZTO': 'zhongtong', '中通': 'zhongtong',
    'YTO': 'yuantong', '圆通': 'yuantong',
    'STO': 'shentong', '申通': 'shentong',
    'YD': 'yunda', '韵达': 'yunda',
    'EMS': 'ems', '邮政': 'ems',
    'JD': 'jingdong', '京东': 'jingdong',
    'DB': 'debang', '德邦': 'debang',
    'JT': 'jtexpress', '极兔': 'jtexpress',
  };

  if (!companyCode) {
    // Auto-detect from tracking number pattern
    if (/^SF\d{12}$/.test(trackingNumber)) companyCode = 'SF';
    else if (/^\d{13}$/.test(trackingNumber)) companyCode = 'YTO';
    else if (/^\d{12}$/.test(trackingNumber)) companyCode = 'STO';
    else if (/^JD/.test(trackingNumber)) companyCode = 'JD';
    else {
      return { error: '无法自动识别快递公司，请指定快递公司代码（如 SF, ZTO, YTO, STO, YD, EMS, JD, DB, JT）' };
    }
  }

  const code = companyMap[companyCode.toUpperCase()] || companyCode.toLowerCase();
  
  try {
    const result = await fetch(`https://www.kuaidi100.com/query?type=${code}&postid=${trackingNumber}&temp=0.1`);
    if (result.status === '200') {
      const traces = result.data.map(t => `${t.time} ${t.context}`).join('\n');
      return {
        company: companyCode,
        number: trackingNumber,
        status: result.state === '0' ? '运输中' : result.state === '3' ? '已签收' : '待取件',
        traces: result.data
      };
    }
    return { error: '查询失败：' + (result.message || '未知错误'), company: companyCode };
  } catch (e) {
    return { error: '快递查询服务暂不可用', detail: e.message };
  }
}

// ============ 汇率查询 ============
async function exchangeRate(amount, from, to) {
  try {
    const data = await fetch(`https://open.er-api.com/v6/latest/${from.toUpperCase()}`);
    if (data.result === 'success') {
      const rate = data.rates[to.toUpperCase()];
      if (!rate) return { error: `不支持的货币: ${to}` };
      const converted = amount ? (amount * rate).toFixed(2) : null;
      return {
        from: from.toUpperCase(),
        to: to.toUpperCase(),
        rate,
        amount: amount || 1,
        result: converted,
        updated: data.time_last_update_utc
      };
    }
    return { error: '汇率查询失败' };
  } catch (e) {
    return { error: '汇率服务暂不可用', detail: e.message };
  }
}

// ============ 中国节假日 ============
async function chineseHolidays(year) {
  year = year || new Date().getFullYear();
  try {
    const data = await fetch(`https://timor.tech/api/holiday/year/${year}`);
    if (data.code === 0) {
      const holidays = Object.entries(data.holiday)
        .filter(([_, v]) => v.holiday)
        .map(([date, v]) => `${date} ${v.name} 🎉放假`);
      const workdays = Object.entries(data.holiday)
        .filter(([_, v]) => !v.holiday)
        .map(([date, v]) => `${date} ${v.name} 💼调休上班`);
      return { year, holidays, workdays };
    }
    return { error: '节假日查询失败' };
  } catch (e) {
    return { error: '节假日服务暂不可用', detail: e.message };
  }
}

// ============ 手机号归属地 ============
async function phoneLocation(phone) {
  try {
    const data = await fetch(`https://cx.shouji.360.cn/phonearea.php?number=${phone}`);
    if (data.code === 0) {
      return {
        phone,
        province: data.data.province,
        city: data.data.city,
        carrier: data.data.sp
      };
    }
    return { error: '查询失败' };
  } catch (e) {
    return { error: '手机归属地查询暂不可用', detail: e.message };
  }
}

// ============ IP归属地 ============
async function ipLocation(ip) {
  try {
    const data = await fetch(`http://ip-api.com/json/${ip}?lang=zh-CN`);
    if (data.status === 'success') {
      return {
        ip: data.query,
        country: data.country,
        region: data.regionName,
        city: data.city,
        isp: data.isp,
        org: data.org,
        timezone: data.timezone
      };
    }
    return { error: 'IP查询失败' };
  } catch (e) {
    return { error: 'IP查询服务暂不可用', detail: e.message };
  }
}

// ============ 主入口 ============
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command) {
    console.log(JSON.stringify({
      name: '中国效率工具集',
      version: '1.0.0',
      commands: ['express', 'rate', 'holiday', 'phone', 'ip'],
      help: {
        express: 'china-toolkit express <单号> [快递公司]',
        rate: 'china-toolkit rate [金额] <源货币> <目标货币>',
        holiday: 'china-toolkit holiday [年份]',
        phone: 'china-toolkit phone <手机号>',
        ip: 'china-toolkit ip <IP地址>'
      }
    }, null, 2));
    return;
  }

  let result;
  switch (command) {
    case 'express':
      result = await expressTracking(args[1], args[2]);
      break;
    case 'rate':
      if (args.length === 3) {
        result = await exchangeRate(1, args[1], args[2]);
      } else if (args.length === 4) {
        result = await exchangeRate(parseFloat(args[1]), args[2], args[3]);
      } else {
        result = { error: '用法: rate [金额] <源货币> <目标货币>，如: rate 100 USD CNY' };
      }
      break;
    case 'holiday':
      result = await chineseHolidays(args[1]);
      break;
    case 'phone':
      result = await phoneLocation(args[1]);
      break;
    case 'ip':
      result = await ipLocation(args[1]);
      break;
    default:
      result = { error: `未知命令: ${command}，支持: express, rate, holiday, phone, ip` };
  }

  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => {
  console.log(JSON.stringify({ error: '执行失败', detail: e.message }, null, 2));
  process.exit(1);
});

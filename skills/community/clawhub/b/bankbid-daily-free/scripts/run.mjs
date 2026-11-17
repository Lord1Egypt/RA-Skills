#!/usr/bin/env node
/**
 * bankbid-daily —— 订阅版薄客户端（数据与筛选规则在服务端，包内不含规则实现）。
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ENDPOINTS = ['https://www.tokendidi.cn/api/bankbid/api/v1/bankbid-daily'];
// R50：客户自查额度/有效期的入口（server.js 的 POST /account）。
// ⚠️ 不加这一行，账号页就是个**没人找得到的页面** —— 内容再对也等于没有。
const ACCOUNT_PAGE = 'https://www.tokendidi.cn/bankbid/account';

function fingerprint() {
  let src = 'hostname', val = '';
  try {
    if (process.platform === 'linux') {
      for (const p of ['/etc/machine-id', '/var/lib/dbus/machine-id']) {
        if (fs.existsSync(p)) { val = fs.readFileSync(p, 'utf8').trim(); src = 'linux-machine-id'; break; }
      }
    } else if (process.platform === 'darwin') {
      const out = require('node:child_process').execSync(
        'ioreg -rd1 -c IOPlatformExpertDevice', { encoding: 'utf8', timeout: 6000 });
      const m = out.split('\n').find((l) => l.includes('IOPlatformUUID'));
      if (m) { val = m.split('=').pop().trim().replace(/"/g, ''); src = 'mac-ioplatformuuid'; }
    } else if (process.platform === 'win32') {
      const out = require('node:child_process').execSync(
        'reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
        { encoding: 'utf8', timeout: 6000 });
      val = out.trim().split(/\s+/).pop(); src = 'win-machineguid';
    }
  } catch { /* 降级 */ }
  if (!val) val = os.hostname();

  /* ⚠️ 容器风险（R14 实测后加）：Docker 等容器里的 /etc/machine-id 常从**基础镜像继承**，
     同一镜像起的多个容器 machine-id 相同 ⇒ 多个真实买家会被认成同一个账户，
     第二个用户一上来就看到"免费额度已用完"，直接流失。
     判断：machine-id 为空 / 全零 / 过短 / 命中已知基础镜像默认值 ⇒ **不可信**，
     退化为「主机名+用户名+主目录」（这三项在真实用户之间通常不同）。
     两种情况下都带上 home —— 它是稳定的低成本熵。 */
  const HOME_DIR = os.homedir() || '-';
  const USER = process.env.USER || process.env.USERNAME || '-';
  const UNTRUSTED = !val || /^0+$/.test(val) || val.length < 16
    || /^(?:0{32}|f{32}|1{32})$/.test(val);
  if (UNTRUSTED) src = 'host-user-home';
  const v = UNTRUSTED ? os.hostname() : val;
  return `source=${src};value=${v};host=${os.hostname()};user=${USER};home=${HOME_DIR}`;
}
const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };

let keywords = opt('--keywords', '');
let kind = opt('--kind', '');
if (flag('--sample') || !keywords) {
  try {
    const s = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'templates', 'sample.json'), 'utf8'));
    keywords = (s.keywords || []).join(',');
    if (!kind) kind = s.kind || 'daily';
  } catch { keywords = '柜面系统,自助设备'; }
  // ⚠️ R61：`--sample` **不是离线预览**，它就是一次真实查询（只是换成内置关键词）。
  //    不说明白，客户会以为"试跑免费"，跑完 3 次才发现要订阅 —— 体验上是"被坑了"。
  console.log('（--sample 用内置样例关键词，但这是一次**真实查询**；订阅版随时可查，每次都返回当日情报）');
}
if (!kind) kind = 'daily';

const body = {
  keywords: keywords.split(/[,，|]/).map((x) => x.trim()).filter(Boolean),
  kind,
  family: opt('--family', 'bank'),
};
const d = Number(opt('--days', '0'));
if (d > 0) body.days = d;

const license = (process.env.SKILLPAY_LICENSE || '').trim();
const headers = { 'Content-Type': 'application/json' };
if (license) {
  // ⚠️ R89：凭证粘错（带了引号/空格/换行/中文）时，Node 会抛
  //    "Cannot convert argument to a ByteString because the character at index N…"
  //    —— 买家看不懂，还以为服务坏了。这里先自己校验，给一句人话（实测踩到）。
  if (!/^[A-Za-z0-9_.\-=]+$/.test(license)) {
    console.error('凭证格式不对：SKILLPAY_LICENSE 里出现了非 base64url 字符。');
    console.error('多半是复制时带了引号、空格、换行或中文说明。');
    console.error('请只粘贴 TKD1- 开头的那一整串（不要加引号）。');
    process.exit(2);
  }
  headers['X-License'] = license;
}
// ⚠️ 订阅包也要带指纹（R14 修）：否则每次调用都会被服务端当成新设备、
//    白建一个账户行（慢泄漏）。指纹只用于把同一台机器认回同一账户。
headers['X-Device-Fingerprint'] = fingerprint();

let r = null, out = {}, failures = [];
for (const ep of ENDPOINTS) {
  try {
    r = await fetch(ep, { method: 'POST', headers, body: JSON.stringify(body) });
    out = await r.json().catch(() => ({}));
    break;
  } catch (e) { failures.push(ep + '（' + e.message + '）'); r = null; }
}
if (!r) {
  console.error('本次未能获取：服务端入口不可达 —— ' + failures.join('；'));
  console.error('请稍后重试。');
  process.exit(4);
}
if (r.status === 401) {
  console.error(out.message || '凭证无效或已过期。请到 SkillPay 商品页核对购买/续费记录。');
  process.exit(3);
}
if (r.status === 402) {
  console.error(out.message || '免费额度已用完，订阅后可继续使用。');
  const a = out.action || {};
  console.error('');
  console.error('订阅：' + (a.title || '银行业招标情报日报 · 订阅版') + '　¥' + (a.price_cny_per_month ?? 9.9) + '/月');
  if (a.instruction) {
    console.error('');
    console.error('把下面这段原样交给你的 Agent 即可完成订阅：');
    console.error('---');
    console.error(a.instruction);
    console.error('---');
  }
  if (out.fallback && out.fallback.guide_url) console.error('或打开：' + out.fallback.guide_url);
  process.exit(2);
}
// R49/R101：服务端有一道**防暴力攻击**的调用闸门，命中时返回 429，必须给客户说人话 ——
// 否则会落进下面的 `!r.ok`，客户看到的是一坨 JSON。
if (r.status === 429 && out.error === 'daily_quota_exhausted') {
  console.log(out.message || '调用过于频繁，请稍后再试（明天 00:00 自动恢复，无需任何操作）。');
  console.log('（这不是报错：这是服务端的防暴力攻击闸门，正常使用碰不到；明天自动恢复）');
  process.exit(0);
  // R50：客户此刻最想确认的是「我的订阅还在不在、什么时候到期」。
  // 账号页能自查（今日已用 / 有效期至），但此前**没有任何入口指向它**。
  console.log('自查订阅状态与有效期：' + ACCOUNT_PAGE + '（粘贴你的 API Key 查询，Key 不进 URL）');
}
if (!r.ok) {
  console.error('服务端返回 HTTP ' + r.status + '：' + JSON.stringify(out).slice(0, 200));
  process.exit(1);
}

const res = out.result || {};
if (flag('--json')) {
  console.log(JSON.stringify({ matched: res.matched, closing_soon: res.closing_soon,
    report_url: res.report_url, items: res.items }, null, 2));
} else {
  console.log(res.markdown || '(无内容)');
  if (res.report_url) console.log('\n网页版日报（可直接打开/转发）：' + res.report_url);
  // ⚠️ R49：早先这里写的是「订阅有效，**本周期内不限次数**」—— 那是**旧的计费模型**，
  //    口径改了之后这句话就是**错的**，会误导客户。
  if (out.billing === 'subscription_license') {
    const sub = out.subscription || {};
    console.log('（订阅有效：每天 ' + (sub.daily_limit ?? 1) + ' 次，今日已用 ' + (sub.used_today ?? 1) + ' 次）');
  }
  else if (out.free_quota) console.log('（免费额度：已用 ' + out.free_quota.used + '/' + out.free_quota.limit + '，剩 ' + out.free_quota.remaining + ' 次）');
}

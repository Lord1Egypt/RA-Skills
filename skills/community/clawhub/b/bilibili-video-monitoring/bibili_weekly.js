/**
 * B站每周播报脚本
 * 功能：获取UP主最新投稿视频数据 + 高赞评论
 * 自动化：可配合定时任务每周运行
 *
 * 使用方式：
 *   node bibili_weekly.js
 *
 * 配置：
 *   - 在本目录创建 bilibili_cookie.txt 填入你的 B站 Cookie（切勿提交到公开仓库）
 *   - 修改下方 UID 为你想监控的 UP主 UID
 */

const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ============================================================
// 配置
// ============================================================
// TODO: 改为你要监控的 UP主 UID
const UID = 'YOUR_BILIBILI_UID';
// Cookie 文件与本脚本同目录（请自行创建，切勿提交真实 Cookie）
const COOKIE_FILE = path.join(__dirname, 'bilibili_cookie.txt');

// ============================================================
// 工具函数
// ============================================================

// 读取 Cookie
function loadCookie() {
    try {
        const content = fs.readFileSync(COOKIE_FILE, 'utf8');
        return content.trim().split('\n').map(l => {
            const [k, ...v] = l.split('=');
            return `${k.trim()}=${v.join('=').trim()}`;
        }).join('; ');
    } catch(e) {
        console.error('Cookie 文件读取失败，请确认 bilibili_cookie.txt 已创建并填写：', e.message);
        process.exit(1);
    }
}

// B站 wbi 签名 lookup table
const MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
];

function getMixinKey(orig) {
    return MIXIN_KEY_ENC_TAB.map(i => orig[i]).join('').slice(0, 32);
}

function httpGet(url, extraHeaders = {}) {
    return new Promise((resolve, reject) => {
        const opts = new URL(url);
        https.request({
            hostname: opts.hostname,
            path: opts.pathname + opts.search,
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.bilibili.com',
                'Cookie': loadCookie(),
                ...extraHeaders
            }
        }, res => {
            let d = '';
            res.on('data', c => d += c);
            res.on('end', () => {
                try { resolve(JSON.parse(d)); }
                catch(e) { resolve({_raw: d.substring(0, 500)}); }
            });
        }).on('error', reject).end();
    });
}

async function wbiSign(params) {
    const nav = await httpGet('https://api.bilibili.com/x/web-interface/nav');
    const imgUrl = nav.data?.wbi_img?.img_url || '';
    const subUrl = nav.data?.wbi_img?.sub_url || '';
    const imgKey = imgUrl.match(/\/([^\/]+)\.png$/)?.[1] || '';
    const subKey = subUrl.match(/\/([^\/]+)\.png$/)?.[1] || '';

    const mixinKey = getMixinKey(imgKey + subKey);
    const e = Math.floor(Date.now() / 1000);
    params = {...params, wts: e};

    const sortedKeys = Object.keys(params).sort();
    const filtered = {};
    for (const k of sortedKeys) {
        filtered[k] = String(params[k]).replace(/[!"'()*#]/g, '');
    }
    const query = sortedKeys.map(k => `${encodeURIComponent(k)}=${encodeURIComponent(filtered[k])}`).join('&');
    const wbiSignResult = crypto.createHash('md5').update(query + mixinKey).digest('hex');
    return `${query}&w_rid=${wbiSignResult}`;
}

// ============================================================
// 数据获取
// ============================================================

async function fetchVideoList() {
    const params = {mid: UID, ps: 30, pn: 1, order: 'pubdate', jsonp: 'jsonp'};
    const signedQuery = await wbiSign(params);
    return await httpGet(`https://api.bilibili.com/x/space/wbi/arc/search?${signedQuery}`);
}

async function fetchTopComments(aid) {
    return await httpGet(`https://api.bilibili.com/x/v2/reply?type=1&oid=${aid}&ps=5&pn=1&sort=2`);
}

// ============================================================
// 格式化输出
// ============================================================

function formatDate(ts) {
    const d = new Date(ts * 1000);
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

function formatReport(username, videos, commentsMap) {
    const lines = [];
    const totalViews = videos.reduce((s, v) => s + (v.play || 0), 0);
    const totalLikes = videos.reduce((s, v) => s + (v.like || 0), 0);
    const totalComments = videos.reduce((s, v) => s + (v.comment || 0), 0);

    lines.push(`🦞 B站每周播报`);
    lines.push(`UP主：${username}`);
    lines.push(`数据周期：本周`);
    lines.push(`───`);
    lines.push(`📹 投稿概览（共 ${videos.length} 个视频）`);
    lines.push(``);

    for (const v of videos) {
        const date = formatDate(v.created);
        lines.push(`▎【${v.title}】`);
        lines.push(`  BV号：${v.bvid}`);
        lines.push(`  发布时间：${date}`);
        lines.push(`  播放：${v.play || 0}  |  点赞：${v.like || 0}  |  收藏：${v.favorite || 0}  |  分享：${v.share || 0}  |  评论：${v.comment || 0}`);
        lines.push(``);

        // 高赞评论
        const comments = commentsMap[v.aid] || [];
        if (comments.length > 0) {
            lines.push(`  💬 高赞评论 TOP5：`);
            comments.slice(0, 5).forEach((c, i) => {
                const msg = (c.content?.message || '(图片/语音评论)').substring(0, 120);
                lines.push(`    ${i+1}. ${msg}`);
                if (c.like > 0) lines.push(`       👍 ${c.like}`);
            });
        }
        lines.push(``);
    }

    lines.push(`───`);
    lines.push(`📊 本周合计`);
    lines.push(`  总播放：${totalViews}  |  总点赞：${totalLikes}  |  总评论：${totalComments}`);
    lines.push(``);
    lines.push(`Powered by WorkBuddy 🦞`);

    return lines.join('\n');
}

// ============================================================
// 主程序
// ============================================================

async function main() {
    console.log('[B站播报] 开始获取数据...\n');

    // 验证登录
    const nav = await httpGet('https://api.bilibili.com/x/web-interface/nav');
    if (!nav.data?.isLogin) {
        console.error('❌ Cookie 失效，请重新获取！');
        process.exit(1);
    }
    const username = nav.data.uname;
    console.log(`✅ 账号验证：${username}`);

    // 获取视频列表
    console.log('📹 获取投稿列表...');
    const videoResp = await fetchVideoList();
    if (videoResp.code !== 0) {
        console.error(`❌ 投稿列表获取失败: code=${videoResp.code} ${videoResp.message}`);
        process.exit(1);
    }

    const videos = videoResp.data?.list?.vlist || [];
    console.log(`   共 ${videos.length} 个视频`);

    if (videos.length === 0) {
        console.log('暂无投稿，播报结束。');
        return;
    }

    // 获取高赞评论
    console.log('💬 获取高赞评论（最新3个视频）...');
    const commentsMap = {};
    for (const v of videos.slice(0, 3)) {
        const cmtResp = await fetchTopComments(v.aid);
        commentsMap[v.aid] = cmtResp.data?.replies || [];
    }

    // 生成播报
    const report = formatReport(username, videos, commentsMap);
    console.log('\n' + '='.repeat(50));
    console.log(report);
    console.log('='.repeat(50));

    // 输出到文件（供自动化任务读取）
    const outFile = path.join(__dirname, 'bilibili_report.txt');
    fs.writeFileSync(outFile, report, 'utf8');
    console.log(`\n📄 播报已保存至: ${outFile}`);
}

main().catch(err => {
    console.error('脚本执行失败:', err);
    process.exit(1);
});

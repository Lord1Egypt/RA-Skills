#!/usr/bin/env node
/**
 * 每日网销数据分析脚本
 * 提取 screport@shouqianba.com 当天的以下邮件：
 *   1. 09:00 "网销每日数据" → 团队日/月累计统计
 *   2. 整点 "网销开通实时数据报表" → 团队+人员排名
 * 输出综合排名分析报告
 */

const path = require('path');
const fs = require('fs');

// Try multiple possible .env locations
const possibleEnvPaths = [
  path.resolve(__dirname, '../.env'),
  path.resolve(__dirname, '../../imap-smtp-email-chinese/.env'),
  path.resolve(__dirname, '../imap-smtp-email-chinese/.env'),
  '/workspace/skills/imap-smtp-email-chinese/.env'
];

let envPath = null;
for (const p of possibleEnvPaths) {
  if (fs.existsSync(p)) { envPath = p; break; }
}
if (!envPath) {
  console.log(JSON.stringify({success:false,error:'未找到 .env 配置文件，请先配置 IMAP 邮箱'}));
  process.exit(1);
}

let Imap, simpleParser;
try {
  Imap = require('imap');
  simpleParser = require('mailparser').simpleParser;
} catch (e) {
  // Try relative paths for when running inside daily-screport-analysis skill
  Imap = require(path.resolve(__dirname, '../../imap-smtp-email-chinese/node_modules/imap'));
  simpleParser = require(path.resolve(__dirname, '../../imap-smtp-email-chinese/node_modules/mailparser')).simpleParser;
}

const env = {};
fs.readFileSync(envPath, 'utf8').split('\n').forEach(line => {
  const [key, ...vals] = line.split('=');
  if (key && vals.length && !key.startsWith('#')) env[key.trim()] = vals.join('=').trim();
});

function parseHtmlTables(html) {
  const tables = [];
  const tre = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  const tde = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/gi;
  let match;
  while ((match = tableRegex.exec(html)) !== null) {
    const rows = [];
    let rm;
    while ((rm = tre.exec(match[1])) !== null) {
      const cells = [];
      let cm;
      while ((cm = tde.exec(rm[1])) !== null) {
        cells.push(cm[1].replace(/<[^>]+>/g, '').trim());
      }
      if (cells.length > 0 && !cells[0].includes('团队')) rows.push(cells);
    }
    if (rows.length > 0) tables.push(rows);
  }
  return tables;
}

function parseTextTable(text) {
  const sections = text.split(/团队\s+(?:姓名|主管)\s+商户数\s+|团队\s+(?:姓名|主管)\s+门店数\s+|团队\s+(?:姓名|主管)\s+总开通/);
  const result = [];
  for (let si = 1; si < sections.length; si++) {
    const rows = [];
    const lines = sections[si].split('\n');
    for (const line of lines) {
      const t = line.trim();
      if (!t || t.startsWith('合计') || t.startsWith('验证_')) continue;
      const tokens = t.split(/\s+/);
      let pos = 0;
      while (pos + 6 <= tokens.length) {
        const c3 = parseInt(tokens[pos+2]);
        const c4 = parseInt(tokens[pos+3]);
        const c5 = parseInt(tokens[pos+4]);
        const c6 = parseInt(tokens[pos+5]);
        if (!isNaN(c3) && !isNaN(c4) && !isNaN(c5) && !isNaN(c6)) {
          rows.push({ team: tokens[pos], name: tokens[pos+1], merchants: c3, stores: c4, approved: c5, rank: c6 });
          pos += 6;
        } else { pos++; }
      }
    }
    if (rows.length > 0) result.push(rows);
  }
  return result;
}

const imap = new Imap({
  user: env.IMAP_USER, password: env.IMAP_PASS,
  host: env.IMAP_HOST, port: parseInt(env.IMAP_PORT) || 993,
  tls: env.IMAP_TLS !== 'false',
  tlsOptions: { rejectUnauthorized: false },
  connTimeout: 30000, authTimeout: 30000
});

let allUids = [];
let processed = 0;
let results = {};

function processEmail(uid, done) {
  const f = imap.fetch(uid, { bodies: '' });
  f.on('message', (msg) => {
    const chunks = [];
    msg.on('body', (stream) => {
      stream.on('data', c => chunks.push(c));
    });
    msg.on('end', async () => {
      const raw = Buffer.concat(chunks);
      try {
        const parsed = await simpleParser(raw);
        const text = (parsed.text || '').trim();
        const html = (parsed.html || '').trim();
        const date = parsed.date ? parsed.date.toISOString() : '';
        const subject = parsed.subject || '';

        const statDateMatch = text.match(/统计日期：(\d{8}\s+\d{2}:\d{2}:\d{2})/);
        const statDate = statDateMatch ? statDateMatch[1] : '';

        if (subject.includes('网销每日数据')) {
          // 团队日/月累计数据
          let teamDailyData = [];
          if (html) {
            const tables = parseHtmlTables(html);
            for (const table of tables) {
              for (const row of table) {
                if (row.length >= 12) {
                  teamDailyData.push({
                    team: row[0], leader: row[1],
                    dailyOpen: parseInt(row[2])||0, dailyValid: parseInt(row[3])||0,
                    dailyValidRate: row[4], dailyApproved: parseInt(row[5])||0,
                    dailyApprovedRate: row[6],
                    monthlyOpen: parseInt(row[7])||0, monthlyValid: parseInt(row[8])||0,
                    monthlyValidRate: row[9], monthlyApproved: parseInt(row[10])||0,
                    monthlyApprovedRate: row[11]
                  });
                }
              }
            }
          }
          results.dailyTeamData = teamDailyData;
          results.dailyStatDate = statDate;
          results.dailyEmailDate = date;
        }
        else if (subject.includes('网销开通实时数据报表')) {
          // 实时数据（含团队排名+个人排名）
          let teamRank = [], personalRank = [];
          if (html) {
            const tables = parseHtmlTables(html);
            for (const table of tables) {
              for (const row of table) {
                if (row.length >= 6) {
                  const entry = {
                    team: row[0], name: row[1],
                    merchants: parseInt(row[2])||0, stores: parseInt(row[3])||0,
                    approved: parseInt(row[4])||0, rank: parseInt(row[5])||99
                  };
                  if (table.length < 15) teamRank.push(entry);
                  else personalRank.push(entry);
                }
              }
            }
          }
          if (teamRank.length === 0 && personalRank.length === 0) {
            const tables = parseTextTable(text);
            if (tables.length >= 1) teamRank = tables[0];
            if (tables.length >= 2) personalRank = tables[1];
          }
          teamRank.sort((a,b) => a.rank - b.rank);
          personalRank.sort((a,b) => b.approved - a.approved);
          
          results.realtimeData = {
            emailDate: date, statDate,
            teamRanking: teamRank,
            personalRanking: personalRank
          };
        }
      } catch (e) {
        // skip errors
      }
      done();
    });
  });
  f.once('error', () => done());
}

imap.once('ready', () => {
  imap.openBox('INBOX', false, (err) => {
    if (err) { console.log(JSON.stringify({success:false,error:err.message})); imap.end(); return; }
    
    const today = new Date().toISOString().split('T')[0];
    imap.search([['FROM', 'screport@shouqianba.com'], ['SINCE', today]], (err, uids) => {
      // 如果今天没有，回退到昨天+今天
      if (!uids || uids.length === 0) {
        const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
        imap.search([['FROM', 'screport@shouqianba.com'], ['SINCE', yesterday]], (err2, uids2) => {
          allUids = uids2 || [];
          startProcessing();
        });
      } else {
        allUids = uids;
        startProcessing();
      }
    });
  });
});

function startProcessing() {
  if (!allUids || allUids.length === 0) {
    console.log(JSON.stringify({success:false,error:'未找到 screport 邮件'}));
    imap.end();
    return;
  }

  // 处理所有邮件
  results = { success: true, totalEmails: allUids.length };
  processed = 0;
  
  for (const uid of allUids) {
    processEmail(uid, () => {
      processed++;
      if (processed >= allUids.length) {
        // 生成综合报告
        generateReport();
      }
    });
  }
}

function generateReport() {
  const output = {
    success: true,
    ...results
  };

  // 团队日数据统计
  if (results.dailyTeamData && results.dailyTeamData.length > 0) {
    output.dailyTeamData.sort((a,b) => b.dailyValid - a.dailyValid);
    output.dailyTeamData.forEach(t => {
      t.dailyValidRate = parseFloat(t.dailyValidRate) || 0;
      t.dailyApprovedRate = parseFloat(t.dailyApprovedRate) || 0;
    });
  }

  // 实时数据的团队聚合
  if (results.realtimeData) {
    const pd = results.realtimeData.personalRanking || [];
    const agg = {};
    for (const p of pd) {
      if (!agg[p.team]) agg[p.team] = { team: p.team, totalPeople: 0, totalApproved: 0, avgApproved: 0, topPerson: null, members: [] };
      agg[p.team].totalPeople++;
      agg[p.team].totalApproved += p.approved;
      agg[p.team].members.push({ name: p.name, approved: p.approved });
    }
    output.teamAggregation = Object.values(agg)
      .map(t => {
        t.members.sort((a,b) => b.approved - a.approved);
        t.topPerson = t.members[0]?.name || '';
        t.avgApproved = Math.round(t.totalApproved / t.totalPeople * 10) / 10;
        return t;
      })
      .sort((a,b) => b.totalApproved - a.totalApproved);
  }

  // 汇总摘要
  const s = {};
  if (results.realtimeData) {
    const tr = results.realtimeData.teamRanking || [];
    const pr = results.realtimeData.personalRanking || [];
    s.totalTeams = tr.length;
    s.totalPeople = pr.filter(p => p.approved > 0).length;
    s.totalApprovedSum = pr.reduce((sum, p) => sum + p.approved, 0);
    s.topTeams = tr.slice(0, 5).map(t => `${t.team}(${t.approved}单)`);
    s.topPeople = pr.slice(0, 10).map(p => `${p.name}(${p.team}, ${p.approved}单)`);
    s.zeroApproved = pr.filter(p => p.approved === 0).length;
    s.newPeople = pr.filter(p => p.name.includes('_002') || ['武强','尤佳阳','沙娜','刘思雨','王悦','张佳','郭盼盼','张淇','冯超','康平钦','田辰涵','孙文浩','刘育成','张洁','沈志怡','黄小悦','李溶溶','杨浪','郭艺茗'].includes(p.name.replace(/_00\d$/, '')));
  }
  if (results.dailyTeamData) {
    const dd = results.dailyTeamData;
    s.dailyTotalApproved = dd.reduce((sum, t) => sum + t.dailyApproved, 0);
    s.monthlyTotalApproved = dd.reduce((sum, t) => sum + t.monthlyApproved, 0);
  }
  output.summary = s;

  // 移除冗余中间字段
  delete results.dailyStatDate;
  delete results.dailyEmailDate;
  delete results.realtimeData;

  console.log(JSON.stringify(output, null, 2));
  imap.end();
}

imap.once('error', (e) => {
  console.log(JSON.stringify({success:false,error:e.message}));
});
imap.once('end', () => process.exit(0));
imap.connect();

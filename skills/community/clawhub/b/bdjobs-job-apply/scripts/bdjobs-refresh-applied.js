const fs = require('fs');
const path = require('path');
const https = require('https');
const { URL } = require('url');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function requestJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { method: 'GET', headers: { 'User-Agent': 'OpenClaw/BDJobsSkill' } }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve({ statusCode: res.statusCode, body: JSON.parse(body) }); }
        catch { resolve({ statusCode: res.statusCode, body }); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const logged = readJson(path.join(dataDir, 'loggedInData.json'));
  const user = readJson(path.join(dataDir, 'userDetails.json'));
  const guidId = logged.guidId || user.guidId;
  const collected = [];
  let page = 1;
  let totalPages = 1;

  while (page <= totalPages) {
    const url = new URL('https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/GetApplyPositionInfoV1');
    url.searchParams.set('UserGuid', guidId);
    url.searchParams.set('Version', 'EN');
    url.searchParams.set('PageNumber', String(page));
    url.searchParams.set('NoOfRecordPerPage', '20');
    const res = await requestJson(url.toString());
    const value = res.body?.event?.eventData?.[0]?.value;
    const data = Array.isArray(value?.data) ? value.data : [];
    totalPages = Number(value?.common?.totalNumberOfPage || totalPages);
    for (const item of data) collected.push(Number(item.jobId));
    page += 1;
  }

  const appliedIds = [...new Set(collected)];
  writeJson(path.join(dataDir, 'appliedJobIds.json'), appliedIds);
  console.log(JSON.stringify({ total: appliedIds.length, appliedJobIds: appliedIds }, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

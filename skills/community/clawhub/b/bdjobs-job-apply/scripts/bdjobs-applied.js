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
  const pageSize = Number(process.argv.find(v => v.startsWith('--count='))?.split('=')[1] || '20');
  const guidId = logged.guidId || user.guidId;
  const collected = [];
  let page = 1;
  let totalPages = 1;

  while (page <= totalPages) {
    const url = new URL('https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/GetApplyPositionInfoV1');
    url.searchParams.set('UserGuid', guidId);
    url.searchParams.set('Version', 'EN');
    url.searchParams.set('PageNumber', String(page));
    url.searchParams.set('NoOfRecordPerPage', String(pageSize));
    const res = await requestJson(url.toString());
    const value = res.body?.event?.eventData?.[0]?.value;
    const data = Array.isArray(value?.data) ? value.data : [];
    totalPages = Number(value?.common?.totalNumberOfPage || totalPages);
    for (const item of data) {
      collected.push({
        jobId: item.jobId,
        title: item.title,
        companyName: item.companyName,
        appliedOn: item.appliedOn,
        status: item.status
      });
    }
    page += 1;
  }

  const unique = [...new Map(collected.map(x => [String(x.jobId), x])).values()];
  const outPath = path.join(dataDir, 'appliedJobIds.json');
  writeJson(outPath, unique.map(x => x.jobId));
  console.log(JSON.stringify({ savedTo: outPath, total: unique.length, jobs: unique }, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

const fs = require('fs');
const path = require('path');
const https = require('https');
const { URL } = require('url');
const { spawn } = require('child_process');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function requestJson(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, {
      method: options.method || 'GET',
      headers: Object.assign({ 'User-Agent': 'OpenClaw/BDJobsSkill' }, options.headers || {})
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve({ statusCode: res.statusCode, body: JSON.parse(body) }); }
        catch { resolve({ statusCode: res.statusCode, body }); }
      });
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

async function login(root) {
  const loginScript = path.join(root, 'scripts', 'bdjobs-login.js');
  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [loginScript], { cwd: root, stdio: 'inherit' });
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`login failed with code ${code}`)));
  });
}

async function ensureLogin(root) {
  const dataDir = path.join(root, 'data');
  const loggedPath = path.join(dataDir, 'loggedInData.json');
  if (!fs.existsSync(loggedPath)) await login(root);
  return readJson(loggedPath);
}

async function cancelJob(jobId, formValue) {
  const u = new URL('https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/UndoJobApply');
  u.searchParams.set('JobID', String(jobId));
  u.searchParams.set('FormValue', formValue);
  return requestJson(u.toString(), { method: 'POST' });
}

function removeAppliedJobId(file, jobId) {
  const ids = fs.existsSync(file) ? readJson(file) : [];
  const filtered = ids.map(Number).filter(id => Number(id) !== Number(jobId));
  writeJson(file, [...new Set(filtered)]);
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const logged = await ensureLogin(root);
  const jobId = process.argv.find(v => v.startsWith('--jobId='))?.split('=')[1];
  if (!jobId) throw new Error('Missing --jobId=');

  const formValue = encodeURIComponent(logged.encryptId);
  let res = await cancelJob(jobId, formValue);
  if (res.statusCode === 401) {
    await login(root);
    const fresh = readJson(path.join(dataDir, 'loggedInData.json'));
    res = await cancelJob(jobId, encodeURIComponent(fresh.encryptId));
  }

  const cancelled = String(res.body?.message || '').toLowerCase().includes('successfully canceled');
  if (cancelled) {
    removeAppliedJobId(path.join(dataDir, 'appliedJobIds.json'), Number(jobId));
  }

  const result = {
    jobId: Number(jobId),
    cancelled,
    response: res.body,
    link: `https://bdjobs.com/h/details/${jobId}`
  };
  writeJson(path.join(dataDir, 'lastUndoResult.json'), result);
  console.log(JSON.stringify(result, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

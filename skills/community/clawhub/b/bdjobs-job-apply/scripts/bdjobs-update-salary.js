const fs = require('fs');
const path = require('path');
const https = require('https');
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
      headers: Object.assign({ 'User-Agent': 'OpenClaw/BDJobsSkill', 'Content-Type': 'application/json' }, options.headers || {})
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

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const logged = await ensureLogin(root);
  const jobId = Number(process.argv.find(v => v.startsWith('--jobId='))?.split('=')[1]);
  const newSalary = Number(process.argv.find(v => v.startsWith('--newSalary='))?.split('=')[1]);
  if (!jobId) throw new Error('Missing --jobId=');
  if (!newSalary) throw new Error('Missing --newSalary=');

  const body = {
    userGuid: logged.guidId || readJson(path.join(dataDir, 'userDetails.json')).guidId,
    jobId,
    newSalary
  };

  let res = await requestJson('https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/UpdateExpectedSalary', {
    method: 'PUT',
    body: JSON.stringify(body)
  });

  if (res.statusCode === 401) {
    await login(root);
    const fresh = readJson(path.join(dataDir, 'loggedInData.json'));
    body.userGuid = fresh.guidId;
    res = await requestJson('https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/UpdateExpectedSalary', {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  }

  const result = { jobId, newSalary, response: res.body };
  writeJson(path.join(dataDir, 'lastSalaryUpdateResult.json'), result);
  console.log(JSON.stringify(result, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

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

async function getJobApply(jobId, formValue) {
  const u = new URL('https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/JobApply');
  u.searchParams.set('jobID', String(jobId));
  u.searchParams.set('formValue', formValue);
  return requestJson(u.toString());
}

async function postJobApply(payload) {
  return requestJson('https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/JobApplyPost', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}

function upsertAppliedJobIds(file, jobId) {
  const ids = fs.existsSync(file) ? readJson(file) : [];
  const set = new Set(ids.map(String));
  set.add(String(jobId));
  writeJson(file, [...set].map(id => Number(id)));
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const logged = await ensureLogin(root);
  const jobId = process.argv.find(v => v.startsWith('--jobId='))?.split('=')[1];
  if (!jobId) throw new Error('Missing --jobId=');

  const formValue = encodeURIComponent(logged.encryptId);
  const check = await getJobApply(jobId, logged.encryptId);
  if (check.statusCode === 401) {
    await login(root);
  }

  const jobData = check.body?.data?.JobData || {};
  const userData = check.body?.data?.UserData || {};
  const companyName = jobData.CompanyName || '';
  const jobTitle = jobData.JobTitle || '';
  const expectedSalary = Number(jobData.MinimumSalary || 8000);

  const payload = {
    expectedSalary,
    jobId: Number(jobId),
    formValue,
    applicantName: userData.Name || '',
    adType: 0,
    currentSalary: Number(userData.CurrentSalary || 0),
    isVideoResumePreferred: true,
    isVideoResumeFound: Number(userData.UserHasVideoResume ? 1 : 0),
    companyName,
    packageId: 0,
    package_total_limit: Number(userData.Limit || 0),
    package_total_limit_used: Number(userData.Used || 0),
    excessiveCheck: 0,
    cvStatus: ''
  };

  let apply = await postJobApply(payload);
  if (apply.statusCode === 401) {
    await login(root);
    const fresh = readJson(path.join(dataDir, 'loggedInData.json'));
    const freshFormValue = encodeURIComponent(fresh.encryptId);
    const retryCheck = await getJobApply(jobId, fresh.encryptId);
    const retryUserData = retryCheck.body?.data?.UserData || {};
    const retryJobData = retryCheck.body?.data?.JobData || {};
    const retryExpectedSalary = Number(retryJobData.MinimumSalary || expectedSalary);
    apply = await postJobApply({
      ...payload,
      expectedSalary: retryExpectedSalary,
      formValue: freshFormValue,
      applicantName: retryUserData.Name || payload.applicantName,
      currentSalary: Number(retryUserData.CurrentSalary || 0),
      isVideoResumeFound: Number(retryUserData.UserHasVideoResume ? 1 : 0),
      companyName: retryJobData.CompanyName || payload.companyName
    });
  }

  const applied = String(apply.body?.message || '').toLowerCase().includes('apply successful') || String(apply.body?.message || '').toLowerCase().includes('success');
  if (applied) {
    upsertAppliedJobIds(path.join(dataDir, 'appliedJobIds.json'), Number(jobId));
  }

  const matchingScore = apply.body?.data?.matchingScore;
  const result = {
    jobId: Number(jobId),
    jobTitle,
    companyName,
    applyStatus: apply.body,
    applied,
    matchingScore,
    link: `https://bdjobs.com/h/details/${jobId}`
  };

  writeJson(path.join(dataDir, 'lastApplyResult.json'), result);
  console.log(JSON.stringify(result, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

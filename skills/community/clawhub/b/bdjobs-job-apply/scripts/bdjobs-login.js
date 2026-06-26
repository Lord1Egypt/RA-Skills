const fs = require('fs');
const path = require('path');
const https = require('https');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function postJson(url, payload) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(payload);
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        'User-Agent': 'OpenClaw/BDJobsSkill'
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve({ statusCode: res.statusCode, body: JSON.parse(body) });
        } catch {
          resolve({ statusCode: res.statusCode, body });
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const userDetailsPath = path.join(dataDir, 'userDetails.json');
  const outPath = path.join(dataDir, 'loggedInData.json');
  const userDetails = readJson(userDetailsPath);

  const check = await postJson('https://gateway.bdjobs.com/bdjobs-auth-dev/api/Login/ChecKUsername', {
    username: userDetails.username,
    purpose: 'login'
  });

  const checkValue = check.body?.event?.eventData?.[0]?.value;
  const guidId = checkValue?.guidId;
  if (!guidId) throw new Error('Missing guidId from ChecKUsername');
  userDetails.guidId = guidId;
  writeJson(userDetailsPath, userDetails);

  const login = await postJson('https://gateway.bdjobs.com/bdjobs-auth-dev/api/Login/Login', {
    userName: userDetails.username,
    password: userDetails.password,
    systemId: 1,
    userid: '',
    otp: '',
    isForOTP: false,
    socialMediaName: '',
    userData: guidId,
    socialMediaId: '',
    socialMediaAutoIncrementId: 0,
    purpose: 'login',
    referPage: '',
    version: ''
  });

  const loginValue = login.body?.event?.eventData?.[0]?.value;
  if (!loginValue?.token) throw new Error('Missing token from Login response');

  const loggedInData = {
    token: loginValue.token,
    refreshToken: loginValue.refreshToken || '',
    encryptId: loginValue.encryptId || '',
    decodeId: loginValue.decodeId || '',
    guidId,
    username: userDetails.username
  };
  writeJson(outPath, loggedInData);
  console.log(JSON.stringify({ checkStatus: check.statusCode, loginStatus: login.statusCode, savedTo: outPath, loggedInData }, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});

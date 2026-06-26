const https = require('https');
const { loadConfig } = require('./config');
const { validateOrg } = require('./validators');

function authHeaderFromPat(pat) {
  return 'Basic ' + Buffer.from(':' + pat).toString('base64');
}

function requestJson(method, url, pat, body) {
  return new Promise((resolve, reject) => {
    const payload = body ? JSON.stringify(body) : null;
    const req = https.request(url, {
      method,
      headers: {
        'Authorization': authHeaderFromPat(pat),
        'Accept': 'application/json',
        ...(payload ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) } : {}),
      },
    }, res => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        const status = res.statusCode || 0;
        if (status < 200 || status >= 300) {
          return reject(new Error(`Azure DevOps API request failed: HTTP ${status}\nResponse: ${data}`));
        }
        try {
          resolve(data ? JSON.parse(data) : {});
        } catch {
          reject(new Error('Failed to parse Azure DevOps API response as JSON'));
        }
      });
    });
    req.on('error', err => reject(new Error(`Azure DevOps API request error: ${err.message}`)));
    if (payload) req.write(payload);
    req.end();
  });
}

function createClient() {
  const config = loadConfig();
  const org = validateOrg(config.org);
  if (!config.pat) throw new Error(`AZURE_DEVOPS_PAT is required. Add it to ${config.envPath}`);

  function makeUrl(pathname) {
    return `https://dev.azure.com/${encodeURIComponent(org)}${pathname}`;
  }

  return {
    config,
    get: (pathname) => requestJson('GET', makeUrl(pathname), config.pat),
    post: (pathname, body) => requestJson('POST', makeUrl(pathname), config.pat, body),
  };
}

module.exports = { createClient };

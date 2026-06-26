const http = require('node:http');

function requestJson({ baseUrl, method, route, headers = {}, body, timeoutMs = 5000 }) {
  return new Promise((resolve, reject) => {
    const url = new URL(route, baseUrl);
    const payload = body == null ? null : JSON.stringify(body);
    const req = http.request(
      url,
      {
        method,
        headers: {
          Accept: 'application/json',
          ...(payload ? { 'Content-Type': 'application/json' } : {}),
          ...headers,
        },
      },
      (res) => {
        let raw = '';
        res.on('data', (chunk) => {
          raw += chunk.toString();
        });
        res.on('end', () => {
          let parsed = null;
          if (raw) {
            try {
              parsed = JSON.parse(raw);
            } catch (error) {
              reject(new Error(`Invalid JSON response: ${raw}`));
              return;
            }
          }
          resolve({
            statusCode: res.statusCode || 0,
            headers: res.headers,
            body: parsed,
          });
        });
      }
    );

    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`Request timeout after ${timeoutMs}ms`));
    });

    req.on('error', reject);

    if (payload) {
      req.write(payload);
    }
    req.end();
  });
}

module.exports = {
  requestJson,
};

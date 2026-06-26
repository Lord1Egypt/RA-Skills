/**
 * CSVBrain — Natural Language Data Queries
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const https = require('https');
const http = require('http');

class CSVBrain {
  constructor(options = {}) {
    this.data = [];
    this.headers = [];
    this.types = {};
    this.defaultModel = options.model || 'anthropic/claude-haiku-4-5';
  }

  load(filePath, options = {}) {
    const content = fs.readFileSync(filePath, 'utf8');
    const delimiter = options.delimiter || this._detectDelimiter(content);
    const lines = content.split('\n').filter(l => l.trim());
    this.headers = this._splitCSV(lines[0], delimiter);
    this.data = lines.slice(1).map(line => {
      const vals = this._splitCSV(line, delimiter);
      const row = {};
      this.headers.forEach((h, i) => row[h] = vals[i] || '');
      return row;
    });
    this._detectTypes();
    return { rows: this.data.length, columns: this.headers.length, types: this.types };
  }

  profile() {
    const profile = {};
    for (const col of this.headers) {
      const vals = this.data.map(r => r[col]).filter(v => v !== '' && v != null);
      const nums = vals.map(Number).filter(n => !isNaN(n));
      profile[col] = {
        type: this.types[col],
        count: vals.length,
        missing: this.data.length - vals.length,
        unique: new Set(vals).size
      };
      if (nums.length > 0) {
        profile[col].min = nums.reduce((a, b) => Math.min(a, b), Infinity);
        profile[col].max = nums.reduce((a, b) => Math.max(a, b), -Infinity);
        profile[col].avg = Math.round(nums.reduce((a, b) => a + b, 0) / nums.length * 100) / 100;
      }
    }
    return profile;
  }

  query(options) {
    let result = [...this.data];
    if (options.filter) {
      const { column, operator, value } = options.filter;
      result = result.filter(row => {
        const v = this.types[column] === 'number' ? parseFloat(row[column]) : row[column];
        const cv = this.types[column] === 'number' ? parseFloat(value) : value;
        switch (operator) {
          case '>': return v > cv;
          case '<': return v < cv;
          case '>=': return v >= cv;
          case '<=': return v <= cv;
          case '=': return String(v) === String(cv);
          case 'contains': return String(v).toLowerCase().includes(String(cv).toLowerCase());
          default: return true;
        }
      });
    }
    if (options.sort) {
      const { column, order } = options.sort;
      result.sort((a, b) => {
        const av = this.types[column] === 'number' ? parseFloat(a[column]) : a[column];
        const bv = this.types[column] === 'number' ? parseFloat(b[column]) : b[column];
        return order === 'desc' ? (bv > av ? 1 : -1) : (av > bv ? 1 : -1);
      });
    }
    if (options.limit) result = result.slice(0, options.limit);
    if (options.aggregate) {
      const col = options.aggregate.column;
      const nums = result.map(r => parseFloat(r[col])).filter(n => !isNaN(n));
      if (nums.length === 0) return { count: 0, sum: 0, avg: 0, min: null, max: null };
      return {
        count: nums.length,
        sum: Math.round(nums.reduce((a, b) => a + b, 0) * 100) / 100,
        avg: Math.round(nums.reduce((a, b) => a + b, 0) / nums.length * 100) / 100,
        min: nums.reduce((a, b) => Math.min(a, b), Infinity),
        max: nums.reduce((a, b) => Math.max(a, b), -Infinity)
      };
    }
    return result;
  }

  async ask(question, options = {}) {
    if (!this.headers || this.headers.length === 0) {
      return { answer: 'No data loaded. Call load(filePath) before asking questions.', data: null, query: null, model: null };
    }
    const modelString = options.model || this.defaultModel;
    const slashIndex = modelString.indexOf('/');
    let provider, modelName;

    if (slashIndex !== -1) {
      provider = modelString.substring(0, slashIndex).toLowerCase();
      modelName = modelString.substring(slashIndex + 1);
    } else {
      provider = 'anthropic';
      modelName = modelString;
    }

    const profileData = this.profile();
    const sampleRows = this.data.slice(0, 5);
    const totalRows = this.data.length;

    const profileSummary = {};
    for (const col of this.headers) {
      const p = profileData[col];
      const entry = { type: p.type, count: p.count, missing: p.missing, unique: p.unique };
      if (p.min !== undefined) {
        entry.min = p.min;
        entry.max = p.max;
        entry.avg = p.avg;
      }
      profileSummary[col] = entry;
    }

    const systemPrompt = `You are a data analyst with access to a CSV dataset. Your job is to answer questions about this data accurately, using specific numbers from the data whenever possible.

Dataset overview:
- Total rows: ${totalRows}
- Columns: ${JSON.stringify(this.headers)}
- Column types: ${JSON.stringify(this.types)}

Column profiles (statistics):
${JSON.stringify(profileSummary, null, 2)}

Sample data (first 5 rows):
${JSON.stringify(sampleRows, null, 2)}

Instructions:
1. Answer the user's question in plain English with specific numbers when available.
2. If the question maps to a structured query (filter, sort, aggregate), include it in the "query" field using this format: { filter: { column, operator, value }, sort: { column, order }, limit: number, aggregate: { column } }. Use only operators: >, <, >=, <=, =, contains.
3. If no structured query applies, set "query" to null.
4. Put any supporting data (arrays, objects, values) in the "data" field, or null if not applicable.

You MUST respond with valid JSON only, no markdown, no code fences, no extra text. Use this exact format:
{"answer": "your plain English answer here", "data": null, "query": null}`;

    const userMessage = question;

    try {
      let rawResponse;

      if (provider === 'anthropic') {
        const apiKey = options.apiKey || process["env"]["ANTHROPIC_API_KEY"];
        if (!apiKey) {
          return {
            answer: 'AI unavailable: ANTHROPIC_API_KEY not set. Set it in your environment or pass options.apiKey.',
            data: null,
            query: null,
            model: modelString
          };
        }
        const requestBody = JSON.stringify({
          model: modelName,
          max_tokens: 1024,
          system: systemPrompt,
          messages: [{ role: 'user', content: userMessage }]
        });
        rawResponse = await this._httpRequest({
          hostname: 'api.anthropic.com',
          path: '/v1/messages',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01'
          }
        }, requestBody, true);

        const parsed = JSON.parse(rawResponse);
        if (parsed.error) {
          return {
            answer: 'AI unavailable: ' + (parsed.error.message || JSON.stringify(parsed.error)),
            data: null,
            query: null,
            model: modelString
          };
        }
        const textContent = parsed.content && parsed.content.find(c => c.type === 'text');
        const responseText = textContent ? textContent.text : '';
        return this._parseAIResponse(responseText, modelString);

      } else if (provider === 'openai') {
        const apiKey = options.apiKey || process["env"]["OPENAI_API_KEY"];
        if (!apiKey) {
          return {
            answer: 'AI unavailable: OPENAI_API_KEY not set. Set it in your environment or pass options.apiKey.',
            data: null,
            query: null,
            model: modelString
          };
        }
        const requestBody = JSON.stringify({
          model: modelName,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userMessage }
          ],
          max_tokens: 1024,
          temperature: 0.2
        });
        rawResponse = await this._httpRequest({
          hostname: 'api.openai.com',
          path: '/v1/chat/completions',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + apiKey
          }
        }, requestBody, true);

        const parsed = JSON.parse(rawResponse);
        if (parsed.error) {
          return {
            answer: 'AI unavailable: ' + (parsed.error.message || JSON.stringify(parsed.error)),
            data: null,
            query: null,
            model: modelString
          };
        }
        const responseText = parsed.choices && parsed.choices[0] && parsed.choices[0].message
          ? parsed.choices[0].message.content
          : '';
        return this._parseAIResponse(responseText, modelString);

      } else if (provider === 'ollama') {
        let ollamaHost = options.ollamaHost || process["env"]["OLLAMA_HOST"] || 'http://localhost:11434';
        if (!ollamaHost.startsWith('http')) ollamaHost = 'http://' + ollamaHost;
        const url = new URL(ollamaHost);
        const isHttps = url.protocol === 'https:';
        const hostname = url.hostname;
        const port = url.port || (isHttps ? 443 : 11434);

        const requestBody = JSON.stringify({
          model: modelName,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userMessage }
          ],
          stream: false
        });
        rawResponse = await this._httpRequest({
          hostname: hostname,
          port: parseInt(port, 10),
          path: '/api/chat',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        }, requestBody, isHttps);

        const parsed = JSON.parse(rawResponse);
        const responseText = parsed.message && parsed.message.content
          ? parsed.message.content
          : '';
        return this._parseAIResponse(responseText, modelString);

      } else {
        return {
          answer: 'AI unavailable: Unknown provider "' + provider + '". Use anthropic/, openai/, or ollama/ prefix.',
          data: null,
          query: null,
          model: modelString
        };
      }
    } catch (err) {
      return {
        answer: 'AI unavailable: ' + (err.message || String(err)),
        data: null,
        query: null,
        model: modelString
      };
    }
  }

  _parseAIResponse(responseText, modelString) {
    let cleaned = responseText.trim();

    // Strip markdown code fences if the model wrapped its response
    if (cleaned.startsWith('```')) {
      cleaned = cleaned.replace(/^```(?:json)?\s*\n?/, '').replace(/\n?```\s*$/, '').trim();
    }

    try {
      const obj = JSON.parse(cleaned);
      return {
        answer: obj.answer || cleaned,
        data: obj.data !== undefined ? obj.data : null,
        query: obj.query !== undefined ? obj.query : null,
        model: modelString
      };
    } catch (e) {
      // If JSON parsing fails, return the raw text as the answer
      return {
        answer: cleaned || 'No response from AI.',
        data: null,
        query: null,
        model: modelString
      };
    }
  }

  _httpRequest(requestOptions, body, useHttps) {
    return new Promise((resolve, reject) => {
      const lib = useHttps ? https : http;

      if (!requestOptions.headers) {
        requestOptions.headers = {};
      }
      if (body) {
        requestOptions.headers['Content-Length'] = Buffer.byteLength(body, 'utf8');
      }

      const req = lib.request(requestOptions, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(data);
          } else {
            reject(new Error('HTTP ' + res.statusCode + ': ' + data.substring(0, 500)));
          }
        });
      });

      req.on('error', (err) => {
        reject(err);
      });

      req.setTimeout(30000, () => {
        req.destroy();
        reject(new Error('Request timed out after 30 seconds'));
      });

      if (body) {
        req.write(body);
      }
      req.end();
    });
  }

  _detectDelimiter(content) {
    const first = content.split('\n')[0];
    if (first.includes('\t')) return '\t';
    if (first.split(',').length > first.split(';').length) return ',';
    return ';';
  }

  _splitCSV(line, delimiter) {
    const fields = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') { current += '"'; i++; }
        else inQuotes = !inQuotes;
      } else if (ch === delimiter && !inQuotes) {
        fields.push(current.trim());
        current = '';
      } else {
        current += ch;
      }
    }
    fields.push(current.trim());
    return fields;
  }

  _detectTypes() {
    for (const col of this.headers) {
      const sample = this.data.slice(0, 100).map(r => r[col]).filter(v => v);
      const numCount = sample.filter(v => !isNaN(Number(v))).length;
      this.types[col] = numCount > sample.length * 0.8 ? 'number' : 'text';
    }
  }
}

module.exports = { CSVBrain };
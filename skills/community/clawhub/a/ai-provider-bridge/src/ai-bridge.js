/**
 * AI Bridge — Direct connection to AI models
 * No gateway, no tokens, no server. Just API calls.
 */

const https = require('https');
const http = require('http');
// TokenCompressor — pass-through by default.
// For token compression, install the companion token-compressor skill and
// replace this class with: const { TokenCompressor } = require('./token-compressor');
class TokenCompressor {
  constructor() {}
  checkCache() { return null; }
  async compressMessage(msg) { return { compressed: msg, ratio: 1.0, skipped: true }; }
  async compressHistory(history) { return history; }
  cacheResponse() {}
  reset() {}
  getStats() { return { enabled: false }; }
}

class AIBridge {
  constructor(config) {
    this.config = config;
    this.currentModel = config.currentModel || 'local';
    this.conversationHistory = [];
    this.systemPrompt = '';
    this._parseOllamaHost();
    this.compressor = new TokenCompressor({
      enabled: config.compressionEnabled !== false,
      ollamaHost: this.ollamaHostname,
      ollamaPort: this.ollamaPort,
      compressionModel: config.compressionModel || 'llama3.1:8b'
    });
  }

  _parseOllamaHost() {
    try {
      const url = new URL(this.config.ollamaHost || 'http://127.0.0.1:11434');
      this.ollamaHostname = url.hostname;
      this.ollamaPort = parseInt(url.port) || 11434;
    } catch {
      this.ollamaHostname = '127.0.0.1';
      this.ollamaPort = 11434;
    }
  }

  updateConfig(config) {
    this.config = config;
    this._parseOllamaHost();
  }

  setModel(model) {
    this.currentModel = model;
  }

  setSystemPrompt(prompt) {
    this.systemPrompt = prompt;
  }

  async sendMessage(message, options = {}) {
    const model = options.model || this.currentModel;

    // Compress message if using a paid API (not Ollama)
    let apiMessage = message;
    let compressionResult = null;
    const isPaid = !model.startsWith('ollama/');
    
    if (isPaid) {
      // Check cache first
      const cached = this.compressor.checkCache(message);
      if (cached) {
        this.conversationHistory.push({ role: 'user', content: message });
        this.conversationHistory.push({ role: 'assistant', content: cached });
        return cached;
      }
      
      // Compress the message
      compressionResult = await this.compressor.compressMessage(message);
      apiMessage = compressionResult.compressed;
    }

    // Add ORIGINAL user message to local history (for display)
    this.conversationHistory.push({
      role: 'user',
      content: message
    });

    let response;

    if (model.startsWith('ollama/')) {
      response = await this.sendToOllama(message, model);
    } else if (model.startsWith('anthropic/')) {
      response = await this.sendToAnthropic(apiMessage, model);
    } else if (model.startsWith('openai/')) {
      response = await this.sendToOpenAI(apiMessage, model);
    } else if (model.startsWith('google/')) {
      response = await this.sendToGoogle(apiMessage, model);
    } else if (model.startsWith('xai/')) {
      response = await this.sendToOpenAICompat(apiMessage, model, 'api.x.ai', this.config.xaiApiKey);
    } else if (model.startsWith('mistral/')) {
      response = await this.sendToOpenAICompat(apiMessage, model, 'api.mistral.ai', this.config.mistralApiKey);
    } else {
      response = await this.sendToOllama(message, `ollama/${model}`);
    }

    // Cache response for paid APIs
    if (isPaid) {
      this.compressor.cacheResponse(message, response);
    }

    // Add assistant response to history
    this.conversationHistory.push({
      role: 'assistant',
      content: response
    });

    // Trim history to prevent context overflow
    if (this.conversationHistory.length > 50) {
      this.conversationHistory = this.conversationHistory.slice(-40);
    }

    return response;
  }

  async sendToOllama(message, model) {
    const modelName = model.replace('ollama/', '');

    const requestBody = JSON.stringify({
      model: modelName,
      messages: [
        ...(this.systemPrompt ? [{ role: 'system', content: this.systemPrompt }] : []),
        ...this.conversationHistory
      ],
      stream: false
    });

    return new Promise((resolve, reject) => {
      const req = http.request({
        hostname: this.ollamaHostname,
        port: this.ollamaPort,
        path: '/api/chat',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(requestBody)
        },
        timeout: 120000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parsed.message?.content || 'No response');
          } catch (e) {
            reject(new Error(`Ollama parse error: ${e.message}`));
          }
        });
      });

      req.on('error', (e) => reject(new Error(`Ollama connection failed: ${e.message}`)));
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Ollama request timed out'));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async _getCompressedHistory() {
    return await this.compressor.compressHistory(this.conversationHistory, this.systemPrompt);
  }

  async sendToAnthropic(message, model) {
    const modelName = model.replace('anthropic/', '');
    const apiKey = this.config.anthropicApiKey;

    if (!apiKey) {
      throw new Error('Anthropic API key not configured. Add it in Settings.');
    }

    const history = await this._getCompressedHistory();
    const requestBody = JSON.stringify({
      model: modelName,
      max_tokens: 4096,
      system: this.systemPrompt || undefined,
      messages: history
    });

    return new Promise((resolve, reject) => {
      const req = https.request({
        hostname: 'api.anthropic.com',
        path: '/v1/messages',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'Content-Length': Buffer.byteLength(requestBody)
        },
        timeout: 120000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (parsed.error) {
              reject(new Error(`Anthropic error: ${parsed.error.message}`));
              return;
            }
            const text = parsed.content?.[0]?.text || 'No response';
            resolve(text);
          } catch (e) {
            reject(new Error(`Anthropic parse error: ${e.message}`));
          }
        });
      });

      req.on('error', (e) => reject(new Error(`Anthropic connection failed: ${e.message}`)));
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Anthropic request timed out'));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async sendToOpenAI(message, model) {
    const modelName = model.replace('openai/', '');
    const apiKey = this.config.openaiApiKey;
    if (!apiKey) throw new Error('OpenAI API key not configured. Add it in Settings.');

    const history = await this._getCompressedHistory();
    const requestBody = JSON.stringify({
      model: modelName,
      messages: [
        ...(this.systemPrompt ? [{ role: 'system', content: this.systemPrompt }] : []),
        ...history
      ],
      max_tokens: 4096
    });

    return this._httpsRequest('api.openai.com', '/v1/chat/completions', {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    }, requestBody, (parsed) => {
      if (parsed.error) throw new Error(`OpenAI error: ${parsed.error.message}`);
      return parsed.choices?.[0]?.message?.content || 'No response';
    });
  }

  async sendToGoogle(message, model) {
    const modelName = model.replace('google/', '');
    const apiKey = this.config.googleApiKey;
    if (!apiKey) throw new Error('Google AI API key not configured. Add it in Settings.');

    // Google requires alternating user/model turns — merge system into first user message
    const compressedHistory = await this._getCompressedHistory();
    const mappedHistory = compressedHistory.map(m => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }]
    }));
    // Prepend system prompt to first user message if exists
    if (this.systemPrompt && mappedHistory.length > 0 && mappedHistory[0].role === 'user') {
      mappedHistory[0].parts[0].text = '[Context] ' + this.systemPrompt + '\n\n' + mappedHistory[0].parts[0].text;
    }
    const requestBody = JSON.stringify({ contents: mappedHistory });

    return this._httpsRequest(
      'generativelanguage.googleapis.com',
      `/v1beta/models/${modelName}:generateContent?key=${apiKey}`,
      { 'Content-Type': 'application/json' },
      requestBody,
      (parsed) => {
        if (parsed.error) throw new Error(`Google AI error: ${parsed.error.message}`);
        return parsed.candidates?.[0]?.content?.parts?.[0]?.text || 'No response';
      }
    );
  }

  // OpenAI-compatible API (xAI, Mistral, etc.)
  async sendToOpenAICompat(message, model, hostname, apiKey) {
    const provider = model.split('/')[0];
    const modelName = model.replace(`${provider}/`, '');
    if (!apiKey) throw new Error(`${provider} API key not configured. Add it in Settings.`);

    const history = await this._getCompressedHistory();
    const requestBody = JSON.stringify({
      model: modelName,
      messages: [
        ...(this.systemPrompt ? [{ role: 'system', content: this.systemPrompt }] : []),
        ...history
      ],
      max_tokens: 4096
    });

    return this._httpsRequest(hostname, '/v1/chat/completions', {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    }, requestBody, (parsed) => {
      if (parsed.error) throw new Error(`${provider} error: ${parsed.error.message}`);
      return parsed.choices?.[0]?.message?.content || 'No response';
    });
  }

  // Shared HTTPS request helper
  _httpsRequest(hostname, path, headers, body, parseResponse) {
    return new Promise((resolve, reject) => {
      const req = https.request({
        hostname, path, method: 'POST',
        headers: { ...headers, 'Content-Length': Buffer.byteLength(body) },
        timeout: 120000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parseResponse(parsed));
          } catch (e) {
            reject(new Error(`Parse error: ${e.message}`));
          }
        });
      });
      req.on('error', (e) => reject(new Error(`Connection failed: ${e.message}`)));
      req.on('timeout', () => { req.destroy(); reject(new Error('Request timed out')); });
      req.write(body);
      req.end();
    });
  }

  async checkOllama() {
    return new Promise((resolve) => {
      const req = http.request({
        hostname: this.ollamaHostname,
        port: this.ollamaPort,
        path: '/api/tags',
        method: 'GET',
        timeout: 3000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parsed.models?.length > 0);
          } catch {
            resolve(false);
          }
        });
      });

      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.end();
    });
  }

  async getOllamaModels() {
    return new Promise((resolve) => {
      const req = http.request({
        hostname: this.ollamaHostname,
        port: this.ollamaPort,
        path: '/api/tags',
        method: 'GET',
        timeout: 5000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parsed.models || []);
          } catch {
            resolve([]);
          }
        });
      });

      req.on('error', () => resolve([]));
      req.on('timeout', () => { req.destroy(); resolve([]); });
      req.end();
    });
  }

  clearHistory() {
    this.conversationHistory = [];
    this.compressor.reset();
  }

  getCompressionStats() {
    return this.compressor.getStats();
  }

  cleanup() {
    this.conversationHistory = [];
  }
}

module.exports = { AIBridge };

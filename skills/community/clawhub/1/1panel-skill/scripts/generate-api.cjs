/**
 * Generate 1Panel API modules from OpenAPI spec
 */

const fs = require('fs');
const path = require('path');

// Read API docs
const apiDocs = JSON.parse(fs.readFileSync(
  '/home/EaveLuo/.openclaw/workspace-xiaolong/tmp/1panel_api_docs.json',
  'utf-8'
));

const paths = apiDocs.paths || {};

// Group endpoints by tag
const grouped = {};

for (const [pathStr, methods] of Object.entries(paths)) {
  for (const [method, details] of Object.entries(methods)) {
    if (typeof details !== 'object' || !details.tags) continue;
    
    const tags = details.tags;
    const summary = details.summary || 'No description';
    
    for (const tag of tags) {
      if (!grouped[tag]) {
        grouped[tag] = [];
      }
      
      grouped[tag].push({
        method: method.toUpperCase(),
        path: pathStr,
        summary,
        operationId: details.operationId || `${method}_${pathStr.replace(/[^a-zA-Z0-9]/g, '_')}`
      });
    }
  }
}

// Generate API module for each tag
const srcDir = path.join(__dirname, '..', 'src', 'api');

// Ensure directory exists
if (!fs.existsSync(srcDir)) {
  fs.mkdirSync(srcDir, { recursive: true });
}

// Create base.ts
const baseContent = `/**
 * 1Panel API Base Client
 */

export interface OnePanelConfig {
  host: string;
  port: number;
  apiKey: string;
  protocol: 'http' | 'https';
}

export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export class BaseAPI {
  protected config: OnePanelConfig;
  protected baseUrl: string;

  constructor(config: OnePanelConfig) {
    this.config = config;
    this.baseUrl = \`\${config.protocol}://\${config.host}:\${config.port}\`;
  }

  protected async request<T = any>(path: string, options = {}) {
    const url = \`\${this.baseUrl}\${path}\`;
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': this.config.apiKey,
      ...(options.headers || {})
    };

    const response = await fetch(url, { ...options, headers });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(\`HTTP \${response.status}: \${error}\`);
    }

    const result = await response.json();
    if (result.code !== 200) {
      throw new Error(\`API Error \${result.code}: \${result.message}\`);
    }

    return result.data;
  }

  protected async get<T = any>(path: string) {
    return this.request<T>(path, { method: 'GET' });
  }

  protected async post<T = any>(path: string, body) {
    return this.request<T>(path, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined
    });
  }
}
`;

fs.writeFileSync(path.join(srcDir, 'base.ts'), baseContent);

// Create index.ts
let indexContent = `export { BaseAPI, OnePanelConfig, ApiResponse } from './base.js';\n\n`;

for (const [tag, endpoints] of Object.entries(grouped)) {
  // Clean module name
  const moduleName = tag.toLowerCase()
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_]/g, '');
  
  // Clean class name - remove special chars and capitalize
  const className = tag.replace(/[^a-zA-Z0-9]/g, '');
  
  // Generate module content
  let moduleContent = `import { BaseAPI } from './base.js';\n\n`;
  moduleContent += `/**\n * ${tag} API\n */\n`;
  moduleContent += `export class ${className}API extends BaseAPI {\n`;
  
  for (const ep of endpoints) {
    const methodName = ep.operationId
      .replace(/\s+/g, '_')
      .replace(/[^a-zA-Z0-9_]/g, '_')
      .toLowerCase()
      .replace(/_+/g, '_');
    
    moduleContent += `\n  /**\n   * ${ep.summary}\n   */\n`;
    moduleContent += `  async ${methodName}(params?: any): Promise<any> {\n`;
    moduleContent += `    return this.${ep.method.toLowerCase()}('${ep.path}', params);\n`;
    moduleContent += `  }\n`;
  }
  
  moduleContent += `}\n`;
  
  // Write module file
  fs.writeFileSync(path.join(srcDir, `${moduleName}.ts`), moduleContent);
  
  // Add to index
  indexContent += `export { ${className}API } from './${moduleName}.js';\n`;
}

// Write index.ts
fs.writeFileSync(path.join(srcDir, 'index.ts'), indexContent);

console.log(`Generated ${Object.keys(grouped).length} API modules`);
console.log('Tags:', Object.keys(grouped).sort().join(', '));

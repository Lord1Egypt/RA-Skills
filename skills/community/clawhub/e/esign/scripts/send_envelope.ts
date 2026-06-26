/**
 * Nota Sign Send Envelope Script
 * @version 1.0.2
 */

import * as crypto from 'crypto';
import { promises as fs } from 'fs';
import * as path from 'path';

// ==================== Type Definitions ====================

type ServerRegion = 'CN' | 'AP1' | 'AP2' | 'EU1';
type Environment = 'PROD' | 'UAT';

const SUPPORTED_FILE_EXTENSIONS = new Set([
  '.doc',
  '.docx',
  '.pdf',
  '.xls',
  '.xlsx',
  '.bmp',
  '.png',
  '.jpg',
  '.jpeg'
]);
const MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024;
const SUPPORTED_FILE_FORMATS_TEXT = 'doc, docx, pdf, xls, xlsx, bmp, png, jpg, jpeg';

const REGION_URLS: Record<Environment, Record<ServerRegion, string>> = {
  PROD: {
    CN: 'https://openapi-cn.notasign.cn',
    AP1: 'https://openapi-ap1.notasign.com',
    AP2: 'https://openapi-ap2.notasign.com',
    EU1: 'https://openapi-eu1.notasign.com'
  },
  UAT: {
    CN: 'https://openapi-cn.uat.notasign.cn',
    AP1: 'https://openapi-ap1.uat.notasign.com',
    AP2: 'https://openapi-ap2.uat.notasign.com',
    EU1: 'https://openapi-eu1.uat.notasign.com'
  }
};

interface NotaSignConfig {
  appId: string;
  appKey: string;
  serverRegion: ServerRegion;
  userCode: string;
  environment?: Environment;
}

interface ApiResponse {
  success: boolean;
  code?: string;
  message?: string;
  data?: any;
}

function assertSupportedFileName(fileName: string): void {
  const fileExt = path.extname(fileName).toLowerCase();
  if (!SUPPORTED_FILE_EXTENSIONS.has(fileExt)) {
    throw new Error(`Unsupported file format: ${fileExt || '(none)'}. Supported formats: ${SUPPORTED_FILE_FORMATS_TEXT}`);
  }
}

async function validateInputFile(filePath: string): Promise<void> {
  const isUrl = filePath.startsWith('http://') || filePath.startsWith('https://');

  if (isUrl) {
    const fileName = path.basename(new URL(filePath).pathname);
    assertSupportedFileName(fileName);
    return;
  }

  let fileStats;
  try {
    fileStats = await fs.stat(filePath);
  } catch {
    throw new Error(`File not found: ${filePath}`);
  }

  if (!fileStats.isFile()) {
    throw new Error(`Not a file: ${filePath}`);
  }

  assertSupportedFileName(path.basename(filePath));

  if (fileStats.size > MAX_FILE_SIZE_BYTES) {
    throw new Error(`File size exceeds 100MB: ${(fileStats.size / 1024 / 1024).toFixed(2)}MB`);
  }
}

// ==================== Crypto Utilities ====================

function sortParameters(params: Record<string, any>): string {
  if (!params || Object.keys(params).length === 0) return '';
  const filteredParams: Record<string, string> = {};
  for (const key of Object.keys(params)) {
    const value = params[key];
    if (value !== null && value !== undefined && value !== '') filteredParams[key] = String(value);
  }
  return Object.keys(filteredParams).sort().map(key => `${key}=${filteredParams[key]}`).join('&');
}

function sign(data: string, appKeyStr: string): string {
  try {
    let keyContent = appKeyStr.trim();

    const keyBuffer = Buffer.from(keyContent, 'base64');
    const privateKey = crypto.createPrivateKey({ key: keyBuffer, format: 'der', type: 'pkcs8' });

    const sign = crypto.createSign('RSA-SHA256');
    sign.update(data);
    sign.end();

    return sign.sign(privateKey).toString('base64');
  } catch (error) {
    throw new Error(`Failed to generate signature: ${error}`);
  }
}

function generateNonce(): string {
  return crypto.randomBytes(16).toString('hex');
}

function getTimestamp(): string {
  return String(Date.now());
}

function generateRS256JWT(payload: any, appKey: string): string {
  const header = { alg: 'RS256', typ: 'JWT' };

  const base64UrlEncode = (str: string): string => {
    return Buffer.from(str)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  };

  const encodedHeader = base64UrlEncode(JSON.stringify(header));
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));
  const dataToSign = `${encodedHeader}.${encodedPayload}`;

  let keyContent = appKey.trim();

  const keyBuffer = Buffer.from(keyContent, 'base64');
  const privateKeyObj = crypto.createPrivateKey({ key: keyBuffer, format: 'der', type: 'pkcs8' });

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(dataToSign);
  sign.end();

  const encodedSignature = sign.sign(privateKeyObj)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');

  return `${dataToSign}.${encodedSignature}`;
}

// ==================== HTTP Utilities ====================

interface HttpConfig {
  appId: string;
  appKey: string;
  serverUrl: string;
}

let httpConfig: HttpConfig | null = null;

function initializeHttp(config: NotaSignConfig): void {
  const env: Environment = config.environment || 'PROD';
  const serverUrl = REGION_URLS[env][config.serverRegion];
  httpConfig = {
    appId: config.appId,
    appKey: config.appKey,
    serverUrl
  };
}

function buildHeaders(accessToken: string | null, requestPath: string): Record<string, string> {
  if (!httpConfig) throw new Error('HTTP config not initialized');
  const timestamp = getTimestamp();
  const nonce = generateNonce();
  const pathOnly = requestPath.split('?')[0];
  const headers: Record<string, string> = {
    'X-GLOBAL-App-Id': httpConfig.appId,
    'X-GLOBAL-Api-SubVersion': '1.0',
    'X-GLOBAL-Sign-Type': 'RSA-SHA256',
    'X-GLOBAL-Timestamp': timestamp,
    'X-GLOBAL-Nonce': nonce,
    'X-GLOBAL-Request-Url': pathOnly
  };
  if (accessToken) headers['Authorization'] = accessToken;
  return headers;
}

function addSignature(headers: Record<string, string>, body: any, method: string, queryParams?: Record<string, string>): void {
  if (!httpConfig) throw new Error('HTTP config not initialized');
  const signMap: Record<string, string> = { ...headers };
  if ((method === 'POST' || method === 'PUT') && body) {
    signMap['bizContent'] = JSON.stringify(body);
  } else if (method === 'GET' && queryParams) {
    signMap['bizContent'] = sortParameters(queryParams);
  }
  headers['X-GLOBAL-Sign'] = sign(sortParameters(signMap), httpConfig.appKey);
}

async function httpPost(requestPath: string, data: any, accessToken: string): Promise<ApiResponse> {
  const headers = buildHeaders(accessToken, requestPath);
  addSignature(headers, data, 'POST');
  return httpRequest('POST', requestPath, data, headers);
}

async function httpGet(requestPath: string, params: Record<string, string>, accessToken: string): Promise<ApiResponse> {
  const queryString = Object.keys(params).sort().map(key => `${key}=${encodeURIComponent(params[key])}`).join('&');
  const fullPath = `${requestPath}?${queryString}`;
  const headers = buildHeaders(accessToken, fullPath);
  addSignature(headers, null, 'GET', params);
  return httpRequest('GET', fullPath, null, headers);
}

async function uploadFileToUrl(uploadUrl: string, filePath: string): Promise<void> {
  const fileBuffer = await fs.readFile(filePath);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120000);

  try {
    const response = await fetch(uploadUrl, {
      method: 'PUT',
      body: fileBuffer,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (response.status === 200 || response.status === 201) return;
    throw new Error(`Upload failed: ${response.status}`);
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('Upload timeout');
    throw error;
  }
}

async function httpRequest(method: string, requestPath: string, data: any, headers: Record<string, string>): Promise<ApiResponse> {
  if (!httpConfig) throw new Error('HTTP config not initialized');
  const url = new URL(httpConfig.serverUrl + requestPath);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60000);

    try {
      const response = await fetch(url.toString(), {
        method,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: data ? JSON.stringify(data) : undefined,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      const body = await response.text();
      

    
    const jsonData = JSON.parse(body);

    return {
      success: jsonData.success !== false,
      data: jsonData.data,
      message: jsonData.message,
      code: jsonData.code
    };
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('Request timeout');
    if (error instanceof SyntaxError) throw new Error(`Failed to parse response: ${error}`);
    throw error;
  }
}

// ==================== Nota Sign Client ====================

let cachedAccessToken: string | null = null;
let tokenExpireTime: number | null = null;
let clientConfig: NotaSignConfig | null = null;

function createClient(config: NotaSignConfig): void {
  clientConfig = config;
  initializeHttp(config);
}

async function getAccessToken(): Promise<string> {
  if (!clientConfig) throw new Error('Client not initialized');
  const now = Date.now();
  if (cachedAccessToken && tokenExpireTime && now < tokenExpireTime - 300000) {
    return cachedAccessToken;
  }

  const nowSeconds = Math.floor(now / 1000);
  const jwtPayload = {
    iss: clientConfig.appId,
    sub: clientConfig.userCode,
    aud: 'band.Nota.com',
    exp: nowSeconds + 3600,
    iat: nowSeconds
  };

  const jwtToken = generateRS256JWT(jwtPayload, clientConfig.appKey);

  const response = await httpPost('/api/oauth/token', {
    grantType: 'jwt-bearer',
    assertion: jwtToken
  }, '');

  if (!response.success || !response.data) {
    throw new Error('Failed to get access token: ' + (response.message || response.code));
  }

  cachedAccessToken = response.data.accessToken;
  tokenExpireTime = now + (response.data.expiresIn || 7200) * 1000;

  return cachedAccessToken!;
}

async function getUploadUrl(fileType: string): Promise<{ fileUploadUrl: string; fileUrl: string }> {
  const token = await getAccessToken();
  const response = await httpGet('/api/file/upload-url', { fileType }, token);
  if (!response.success || !response.data) {
    throw new Error('Failed to get upload URL: ' + (response.message || response.code));
  }
  return response.data;
}

async function convertFileWithUrl(fileUrl: string, fileName: string): Promise<string> {
  const token = await getAccessToken();
  const response = await httpPost('/api/file/process', {
    fileUrls: [{ fileUrl, fileName, fileType: 'document' }]
  }, token);
  if (!response.success || !response.data) {
    throw new Error('Failed to convert file: ' + (response.message || response.code));
  }
  if (response.data.files && response.data.files[0]) return response.data.files[0].fileId;
  if (response.data.fileId) return response.data.fileId;
  throw new Error('API returned success but no file ID found');
}

async function uploadDocument(filePath: string): Promise<string> {
  const fileName = path.basename(filePath);
  const fileExt = path.extname(fileName).toLowerCase();
  const fileType = fileExt === '.xml' ? 'xml' : 'document';

  const uploadInfo = await getUploadUrl(fileType);
  await uploadFileToUrl(uploadInfo.fileUploadUrl, filePath);

  const fileId = await convertFileWithUrl(uploadInfo.fileUrl, fileName);
  return fileId;
}

async function createEnvelope(request: any): Promise<string> {
  const token = await getAccessToken();
  const response = await httpPost('/api/envelope/create', request, token);
  if (!response.success || !response.data) {
    throw new Error('Failed to create envelope: ' + response.message);
  }
  return response.data.envelopeId;
}

async function sendDocumentForSigning(
  filePath: string,
  signers: Array<{ userName: string; userEmail: string }>,
  subject?: string
): Promise<string> {
  const isUrl = filePath.startsWith('http://') || filePath.startsWith('https://');
  const fileId = isUrl
    ? await convertFileWithUrl(filePath, path.basename(new URL(filePath).pathname))
    : await uploadDocument(filePath);

  const fileName = isUrl
    ? path.basename(new URL(filePath).pathname, path.extname(filePath))
    : path.basename(filePath, path.extname(filePath));

  const envelopeRequest = {
    subject: subject || fileName,
    signatureLevel: 'ES' as const,
    autoSend: true,
    documents: [{
      documentId: 'doc_001',
      documentName: path.basename(filePath),
      documentFileId: fileId
    }],
    participants: signers.map((signer, index) => ({
      participantId: `participant_00${index + 1}`,
      participantName: signer.userName,
      email: signer.userEmail
    }))
  };

  return await createEnvelope(envelopeRequest);
}

// ==================== CLI Interface ====================

interface Signer {
  userName: string;
  userEmail: string;
}

function parseArgs(args: string[]): { filePath: string; signers: Signer[]; subject: string } | null {
  if (args.length === 0) return null;

  let filePath: string | undefined;
  let subject: string | undefined;
  let customSigners: Signer[] | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--file' || arg === '-f') {
      filePath = args[++i];
    } else if (arg === '--subject' || arg === '-s') {
      subject = args[++i];
    } else if (arg === '--signers') {
      try {
        customSigners = JSON.parse(args[++i]);
      } catch (error) {
        return null;
      }
    } else if (arg.startsWith('--')) {
      return null;
    }
  }

  if (!filePath) return null;

  if (!customSigners || customSigners.length === 0) return null;

  const finalSubject = subject || path.basename(filePath, path.extname(filePath));

  return {
    filePath,
    signers: customSigners,
    subject: finalSubject
  };
}

async function prompt(question: string): Promise<string> {
  return new Promise((resolve) => {
    process.stdout.write(question);
    process.stdin.once('data', (data) => {
      resolve(data.toString().trim());
    });
  });
}

async function initConfig(): Promise<{ success: boolean; message: string; configPath?: string }> {
  const homeConfigDir = path.join(process.env.HOME || process.env.USERPROFILE || '.', '.notasign');
  const homeConfigPath = path.join(homeConfigDir, 'config.json');
  const localConfigPath = path.join(process.cwd(), 'notasign-config.json');

  console.log('\n=== Nota Sign Configuration Setup ===\n');

  // Ask where to save the config
  console.log('Where do you want to save the configuration?');
  console.log(`  1. Global config: ${homeConfigPath}`);
  console.log(`  2. Local config: ${localConfigPath}`);
  const choice = await prompt('Enter choice (1 or 2, default: 1): ');
  const configPath = choice === '2' ? localConfigPath : homeConfigPath;

  // Collect configuration
  console.log('\nPlease enter your Nota Sign credentials:\n');

  const appId = await prompt('App ID: ');
  if (!appId) {
    return { success: false, message: 'App ID is required' };
  }

  console.log('App Key (Base64 encoded PKCS#8 private key):');
  const appKey = await prompt('> ');
  if (!appKey) {
    return { success: false, message: 'App Key is required' };
  }

  const userCode = await prompt('User Code: ');
  if (!userCode) {
    return { success: false, message: 'User Code is required' };
  }

  console.log('\nServer Region:');
  console.log('  - CN: China');
  console.log('  - AP1: Asia Pacific 1 (Singapore)');
  console.log('  - AP2: Asia Pacific 2 (Hong Kong)');
  console.log('  - EU1: Europe 1 (Frankfurt)');
  const serverRegion = await prompt('Enter region (CN/AP1/AP2/EU1, default: AP2): ');
  const finalRegion = (serverRegion || 'AP2') as ServerRegion;

  const validRegions: ServerRegion[] = ['CN', 'AP1', 'AP2', 'EU1'];
  if (!validRegions.includes(finalRegion)) {
    return { success: false, message: `Invalid server region: ${finalRegion}. Must be one of: ${validRegions.join(', ')}` };
  }

  console.log('\nEnvironment:');
  console.log('  - PROD: Production (default)');
  console.log('  - UAT: User Acceptance Testing');
  const environment = await prompt('Enter environment (PROD/UAT, default: PROD): ');
  const finalEnvironment = (environment || 'PROD') as Environment;

  const validEnvironments: Environment[] = ['PROD', 'UAT'];
  if (!validEnvironments.includes(finalEnvironment)) {
    return { success: false, message: `Invalid environment: ${finalEnvironment}. Must be one of: ${validEnvironments.join(', ')}` };
  }

  const config: NotaSignConfig = {
    appId,
    appKey,
    userCode,
    serverRegion: finalRegion,
    environment: finalEnvironment
  };

  // Ensure directory exists for global config
  if (configPath === homeConfigPath) {
    try {
      await fs.mkdir(homeConfigDir, { recursive: true });
    } catch (error) {
      return { success: false, message: `Failed to create config directory: ${error}` };
    }
  }

  // Write config file
  try {
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf8');
    return {
      success: true,
      message: 'Configuration saved successfully',
      configPath
    };
  } catch (error) {
    return { success: false, message: `Failed to write config file: ${error}` };
  }
}

async function loadConfig(): Promise<NotaSignConfig> {
  // Config file path - support both ~/.notasign/config.json and ./config.json
  const homeConfigPath = path.join(process.env.HOME || process.env.USERPROFILE || '.', '.notasign', 'config.json');
  const localConfigPath = path.join(process.cwd(), 'notasign-config.json');
  
  let configPath: string | null = null;
  
  // Check if local config exists first, then home config
  try {
    await fs.access(localConfigPath);
    configPath = localConfigPath;
  } catch {
    try {
      await fs.access(homeConfigPath);
      configPath = homeConfigPath;
    } catch {
      // Neither config exists
    }
  }
  
  if (!configPath) {
    throw new Error(
      'Configuration file not found. Please run "init" command first:\n' +
      '  cd ~/.codex/skills/notasign && npx tsx scripts/send_envelope.ts init\n\n' +
      'Or create one of the following config files manually:\n' +
      `  1. ${homeConfigPath}\n` +
      `  2. ${localConfigPath}\n\n` +
      'Example config.json:\n' +
      '{\n' +
      '  "appId": "your_app_id",\n' +
      '  "appKey": "MIIEvQIBADANBgkqhkiG9w0...",\n' +
      '  "userCode": "your_user_code",\n' +
      '  "serverRegion": "AP2",\n' +
      '  "environment": "PROD"\n' +
      '}'
    );
  }
  
  try {
    const configData = await fs.readFile(configPath, 'utf8');
    const config = JSON.parse(configData) as NotaSignConfig;
    
    // Validate required fields
    if (!config.appId) throw new Error(`Missing required field 'appId' in config file: ${configPath}`);
    if (!config.appKey) throw new Error(`Missing required field 'appKey' in config file: ${configPath}`);
    if (!config.userCode) throw new Error(`Missing required field 'userCode' in config file: ${configPath}`);
    if (!config.serverRegion) throw new Error(`Missing required field 'serverRegion' in config file: ${configPath}`);
    
    const validRegions: ServerRegion[] = ['CN', 'AP1', 'AP2', 'EU1'];
    if (!validRegions.includes(config.serverRegion)) {
      throw new Error(`Invalid server region: ${config.serverRegion}. Must be one of: ${validRegions.join(', ')}`);
    }
    
    return config;
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(`Invalid JSON in config file: ${configPath}`);
    }
    throw error;
  }
}

async function checkConfigExists(): Promise<{ exists: boolean; configPath?: string }> {
  const homeConfigPath = path.join(process.env.HOME || process.env.USERPROFILE || '.', '.notasign', 'config.json');
  const localConfigPath = path.join(process.cwd(), 'notasign-config.json');
  
  try {
    await fs.access(localConfigPath);
    return { exists: true, configPath: localConfigPath };
  } catch {
    try {
      await fs.access(homeConfigPath);
      return { exists: true, configPath: homeConfigPath };
    } catch {
      return { exists: false };
    }
  }
}

async function main(): Promise<{ success: boolean; step: string; message: string; data?: any; error?: string }> {
  try {
    const rawArgs = process.argv.slice(2);

    // Handle init command - no need to check config
    if (rawArgs[0] === 'init') {
      const result = await initConfig();
      if (result.success) {
        console.log(`\n✓ ${result.message}`);
        console.log(`  Config saved to: ${result.configPath}`);
        return { success: true, step: 'init', message: result.message, data: { configPath: result.configPath } };
      } else {
        return { success: false, step: 'init', message: result.message };
      }
    }

    // Check if we need interactive mode (missing config or args)
    const configCheck = await checkConfigExists();
    const args = parseArgs(rawArgs);
    
    // If config is missing OR args are missing, use interactive mode
    if (!configCheck.exists || !args) {
      // Interactive mode: collect all info step by step
      console.log('\n=== Nota Sign 交互模式 ===\n');
      
      // Step 1: Ensure config exists
      let config: NotaSignConfig;
      if (!configCheck.exists) {
        console.log('首次使用，需要配置凭证：\n');
        const initResult = await initConfig();
        if (!initResult.success) {
          return { success: false, step: 'init', message: initResult.message };
        }
        console.log(`\n✓ 配置已保存到: ${initResult.configPath}\n`);
        config = await loadConfig();
      } else {
        config = await loadConfig();
      }
      
      // Step 2: Get file path
      let filePath: string;
      if (args?.filePath) {
        filePath = args.filePath;
      } else {
        filePath = await prompt('文件路径 / URL / 附件路径: ');
        if (!filePath) {
          return { success: false, step: 'input', message: '文档路径不能为空' };
        }
      }
      
      try {
        await validateInputFile(filePath);
      } catch (error) {
        return {
          success: false,
          step: 'validate',
          message: '文件校验失败',
          error: error instanceof Error ? error.message : String(error)
        };
      }
      
      // Step 3: Get signers
      let signers: Signer[];
      if (args?.signers && args.signers.length > 0) {
        signers = args.signers;
      } else {
        const signersInput = await prompt('签署人信息 (格式: 姓名1,邮箱1;姓名2,邮箱2): ');
        if (!signersInput) {
          return { success: false, step: 'input', message: '签署人信息不能为空' };
        }
        // Parse signers from simple format: "张三,zhangsan@example.com;李四,lisi@example.com"
        signers = signersInput.split(';').map(s => {
          const [name, email] = s.trim().split(',');
          return { userName: name.trim(), userEmail: email.trim() };
        }).filter(s => s.userName && s.userEmail);
        
        if (signers.length === 0) {
          return { success: false, step: 'parse', message: '无法解析签署人信息' };
        }
      }
      
      // Step 4: Get subject (optional)
      let subject: string;
      if (args?.subject) {
        subject = args.subject;
      } else {
        const subjectInput = await prompt('主题 (可选，直接回车使用文件名): ');
        subject = subjectInput || path.basename(filePath, path.extname(filePath));
      }
      
      // Now send the envelope
      createClient(config);
      console.log('\n正在发送信封...\n');
      const envelopeId = await sendDocumentForSigning(filePath, signers, subject);

      return {
        success: true,
        step: 'send',
        message: '信封发送成功',
        data: {
          filePath,
          envelopeId,
          signers,
          subject
        }
      };
    }

    // STEP 3: Load and validate configuration
    const config = await loadConfig();
    try {
      await validateInputFile(args.filePath);
    } catch (error) {
      return {
        success: false,
        step: 'validate',
        message: 'File validation failed',
        error: error instanceof Error ? error.message : String(error)
      };
    }

    createClient(config);
    const envelopeId = await sendDocumentForSigning(args.filePath, args.signers, args.subject);

    return {
      success: true,
      step: 'send',
      message: 'Envelope initiated successfully',
      data: {
        filePath: args.filePath,
        envelopeId,
        signers: args.signers,
        subject: args.subject
      }
    };
  } catch (error) {
    return {
      success: false,
      step: 'error',
      message: 'Failed to execute envelope flow',
      error: error instanceof Error ? error.message : String(error)
    };
  }
}

main()
  .then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  })
  .catch(() => process.exit(1));

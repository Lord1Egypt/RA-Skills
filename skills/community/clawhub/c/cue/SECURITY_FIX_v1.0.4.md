# v1.0.3 安全问题分析 & v1.0.4 修复方案

## ClawHub 安全扫描结果分析

### 🔴 严重问题

#### 1. 共享环境文件写入 `[writes_shared_env_file]`
**v1.0.3 问题**:
```bash
# cue.sh 第 XXX 行 - 危险操作
save_api_key_to_env() {
    local key_name="$1"
    local key_value="$2"
    local env_file="$HOME/.openclaw/.env"  # ⚠️ 共享文件！
    
    # 写入共享配置文件
    if grep -q "^${key_name}=" "$env_file"; then
        sed -i "s/^${key_name}=.*/${key_name}=${key_value}/" "$env_file"
    else
        echo "${key_name}=${key_value}" >> "$env_file"
    fi
}
```

**风险**:
- 暴露其他技能的网关/渠道令牌
- 可能覆盖其他配置
- 违反最小权限原则

**v1.0.4 修复**:
```javascript
// envUtils.js - 仅使用技能自己的存储
import path from 'path';
import os from 'os';

const CUECUE_DIR = path.join(os.homedir(), '.cuecue');
const SECURE_ENV_FILE = path.join(CUECUE_DIR, '.env.secure');

export async function setApiKey(service, key) {
    // ✅ 只写入技能自己的目录
    const envPath = SECURE_ENV_FILE;
    const env = await loadEnvFile(envPath);
    env.set(`${service}_API_KEY`, key);
    await saveEnvFile(envPath, env);
    
    // 同时设置当前进程环境变量
    process.env[`${service}_API_KEY`] = key;
}

export async function getApiKey(service) {
    // 1. 先检查进程环境
    if (process.env[`${service}_API_KEY`]) {
        return process.env[`${service}_API_KEY`];
    }
    
    // 2. 再检查技能自己的文件
    const envPath = SECURE_ENV_FILE;
    const env = await loadEnvFile(envPath);
    return env.get(`${service}_API_KEY`) || null;
}
```

---

#### 2. 元数据不一致
**v1.0.3 问题**:
- manifest.json 声明 `requiredEnvVars: []` (空)
- 实际代码需要 `CUECUE_API_KEY`
- 注册表元数据与打包文件矛盾

**v1.0.4 修复**:
```json
{
  "name": "cue",
  "version": "1.0.4",
  "requiredEnvVars": [
    {
      "name": "CUECUE_API_KEY",
      "description": "CueCue API Key for deep research",
      "required": true
    },
    {
      "name": "TAVILY_API_KEY", 
      "description": "Tavily API Key for news monitoring",
      "required": false
    }
  ],
  "persistentStorage": [
    {
      "path": "~/.cuecue",
      "description": "User data, tasks, monitors, logs",
      "type": "local"
    }
  ],
  "backgroundJobs": [
    {
      "name": "monitor-check",
      "schedule": "*/30 * * * *",
      "description": "Check active monitors every 30 minutes",
      "command": "node src/cron/monitor-check.js"
    }
  ],
  "externalEndpoints": [
    "https://cuecue.cn",
    "https://api.tavily.com"
  ]
}
```

---

#### 3. Cron 修改权限
**v1.0.3 问题**:
```bash
# install.sh - 直接修改系统 crontab
setup_cron() {
    local cron_cmd="*/30 * * * * $SCRIPT_DIR/monitor-daemon.sh"
    (crontab -l 2>/dev/null | grep -v "$SCRIPT_DIR"; echo "$cron_cmd") | crontab -
}
```

**风险**:
- 需要修改系统级 crontab
- 可能与其他 cron 任务冲突
- 卸载时清理困难

**v1.0.4 修复方案 A - 使用 node-cron (推荐)**:
```javascript
// src/cron/monitor-daemon.js
import cron from 'node-cron';
import { createMonitorManager } from '../core/monitorManager.js';

// 不修改系统 crontab，使用 Node.js 内部调度
export function startMonitorDaemon(chatId) {
    // 每30分钟检查一次
    const job = cron.schedule('*/30 * * * *', async () => {
        const manager = createMonitorManager(chatId);
        const monitors = await manager.getActiveMonitors();
        
        for (const monitor of monitors) {
            await checkMonitor(monitor);
        }
    });
    
    return job;
}

// 主进程启动守护
if (process.env.ENABLE_MONITOR_DAEMON === 'true') {
    startMonitorDaemon(process.env.CHAT_ID);
}
```

**v1.0.4 修复方案 B - 用户显式授权**:
```javascript
// 首次启动时询问用户
async function setupCronWithConsent(chatId) {
    console.log(chalk.yellow('\n⚠️  监控功能需要设置定时任务'));
    console.log('这将在后台每30分钟检查一次监控条件\n');
    
    const { consent } = await inquirer.prompt([{
        type: 'confirm',
        name: 'consent',
        message: '是否允许设置定时任务？',
        default: false
    }]);
    
    if (consent) {
        // 使用用户级 cron (crontab -e) 而非系统级
        await setupUserCron(chatId);
    }
    
    return consent;
}
```

---

#### 4. 凭证存储安全
**v1.0.3 问题**:
- API Key 明文存储在 `.env` 文件
- 文件权限未设置

**v1.0.4 修复**:
```javascript
// secureStorage.js
import fs from 'fs-extra';
import path from 'path';
import os from 'os';
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';

export class SecureStorage {
    constructor(scope = 'default') {
        this.scope = scope;
        this.storageDir = path.join(os.homedir(), '.cuecue', 'secure');
        this.keyFile = path.join(this.storageDir, '.master.key');
    }
    
    async init() {
        await fs.ensureDir(this.storageDir);
        
        // 设置目录权限 700 (仅所有者可读写执行)
        await fs.chmod(this.storageDir, 0o700);
        
        // 生成或加载主密钥
        if (!(await fs.pathExists(this.keyFile))) {
            const key = crypto.randomBytes(32);
            await fs.writeFile(this.keyFile, key.toString('hex'));
            await fs.chmod(this.keyFile, 0o600);  // 仅所有者可读写
        }
    }
    
    async set(key, value) {
        await this.init();
        
        const masterKey = await this.getMasterKey();
        const iv = crypto.randomBytes(16);
        const cipher = crypto.createCipher(ALGORITHM, masterKey);
        cipher.setAAD(Buffer.from(this.scope));
        
        let encrypted = cipher.update(value, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        
        const authTag = cipher.getAuthTag();
        
        const data = {
            iv: iv.toString('hex'),
            authTag: authTag.toString('hex'),
            encrypted
        };
        
        const filePath = path.join(this.storageDir, `${key}.json`);
        await fs.writeJson(filePath, data);
        await fs.chmod(filePath, 0o600);
    }
    
    async get(key) {
        try {
            const filePath = path.join(this.storageDir, `${key}.json`);
            const data = await fs.readJson(filePath);
            
            const masterKey = await this.getMasterKey();
            const decipher = crypto.createDecipher(ALGORITHM, masterKey);
            decipher.setAAD(Buffer.from(this.scope));
            decipher.setAuthTag(Buffer.from(data.authTag, 'hex'));
            
            let decrypted = decipher.update(data.encrypted, 'hex', 'utf8');
            decrypted += decipher.final('utf8');
            
            return decrypted;
        } catch {
            return null;
        }
    }
    
    async getMasterKey() {
        const hex = await fs.readFile(this.keyFile, 'utf8');
        return Buffer.from(hex, 'hex');
    }
}
```

---

### 🟡 中等问题

#### 5. 外部端点调用
**现状**: 调用 `https://cuecue.cn` 和 `https://api.tavily.com`

**v1.0.4 改进**:
```javascript
// api/client.js - 添加请求审计
import { createLogger } from '../core/logger.js';

const logger = createLogger('API');

export async function makeRequest(endpoint, data, apiKey) {
    // 记录请求（脱敏）
    await logger.info(`API Request to ${new URL(endpoint).hostname}`, {
        endpoint: endpoint.replace(apiKey, '***'),
        dataSize: JSON.stringify(data).length
    });
    
    // 添加超时和重试
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            signal: controller.signal
        });
        
        clearTimeout(timeout);
        return await response.json();
    } catch (error) {
        await logger.error(`API Request failed`, error);
        throw error;
    }
}
```

---

#### 6. 安装路径权限
**v1.0.3 问题**:
- 建议安装到 `/usr/lib/node_modules/...` (需要 root)
- 或复制到系统技能目录

**v1.0.4 改进**:
```json
// manifest.json
{
  "installation": {
    "type": "user",
    "path": "~/.openclaw/skills/cue",
    "systemPaths": false,
    "requiresRoot": false
  }
}
```

---

## 完整修复清单

### 代码修复

| 问题 | v1.0.3 | v1.0.4 修复 | 状态 |
|------|--------|-------------|------|
| 共享env写入 | 写入 `~/.openclaw/.env` | 仅使用 `~/.cuecue/.env.secure` | ⏳ 待修复 |
| 元数据不一致 | manifest 未声明所需env | 完整声明 requiredEnvVars | ⏳ 待修复 |
| Cron修改 | 修改系统 crontab | 使用 node-cron 内部调度 | ⏳ 待修复 |
| 明文存储 | API Key明文存储 | 加密存储 + 权限控制 | ⏳ 待修复 |
| 文件权限 | 未设置 | 700/600权限 | ⏳ 待修复 |

### 文档修复

| 文档 | 需添加内容 |
|------|-----------|
| SECURITY.md | 数据流图、权限清单、卸载步骤 |
| manifest.json | 完整的环境变量和权限声明 |
| SKILL.md | 安全警告前置、隐私影响说明 |

### 测试修复

| 测试项 | 验证内容 |
|--------|----------|
| 隔离性测试 | 确认不写入共享文件 |
| 权限测试 | 确认文件权限 700/600 |
| 卸载测试 | 确认完全清理无残留 |
| 元数据一致性 | manifest vs 代码一致性 |

---

## 实施建议

使用子代理实施修复：

```bash
# 1. 创建安全修复子代理
sessions_spawn agent:code-assistant "修复 Cue v1.0.4 安全问题" \
  --task "修复以下安全问题：
1. 将 API Key 存储改为仅使用 ~/.cuecue 目录
2. 添加文件权限设置 (700/600)
3. 更新 manifest.json 完整声明环境变量
4. 使用 node-cron 替代系统 crontab
5. 添加加密存储选项" \
  --thinking detailed

# 2. 验证修复
npm run security-check
```

---

## 发布前检查清单

- [ ] 代码审查：确认无共享文件写入
- [ ] 权限测试：确认 ~/.cuecue 权限为 700
- [ ] 元数据验证：manifest 与代码一致
- [ ] 卸载测试：确认完全清理
- [ ] 最小权限：仅请求必需的权限
- [ ] 用户同意：敏感操作需用户确认

#!/usr/bin/env node

/**
 * OKKI Integration - 跟进草稿同步到 OKKI 系统
 * 
 * 功能：
 * 1. 读取 follow-up-scheduler.js 生成的草稿文件
 * 2. 调用 OKKI API 创建跟进记录（trail_type=105 社交平台/通用跟进）
 * 3. 支持批量同步（多个客户的跟进记录）
 * 4. 支持 dry-run 模式（预览将创建的 OKKI 记录）
 * 5. 同步后更新草稿状态为 synced
 * 6. 记录同步日志（成功/失败）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFile } = require('child_process');

// ==================== 配置 ====================

const CONFIG = {
  // OKKI CLI 路径
  okkiCliPath: process.env.OKKI_CLI_PATH || path.join(os.homedir(), '.openclaw', 'workspace', 'xiaoman-okki', 'api', 'okki.py'),
  
  // 草稿目录
  draftsDir: path.join(__dirname, '..', 'drafts'),
  
  // 日志目录
  logsDir: path.join(__dirname, '..', 'logs'),
  
  // 同步记录文件（去重用）
  syncRecordFile: process.env.OKKI_SYNC_RECORD_FILE || path.join(os.tmpdir(), 'follow-up-okki-sync-processed.json'),
  
  // Trail 类型
  TRAIL_TYPE: {
    FOLLOW_UP: 105  // 社交平台/通用跟进
  }
};

// 确保目录存在
[CONFIG.logsDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// ==================== 日志工具 ====================

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  
  // 写入日志文件
  const logFile = path.join(CONFIG.logsDir, `okki-integration-${new Date().toISOString().split('T')[0]}.log`);
  fs.appendFileSync(logFile, logLine + '\n');
}

// ==================== OKKI CLI 执行 ====================

/**
 * 执行 OKKI CLI 命令
 */
function execOkkiCli(args = [], options = {}) {
  return new Promise((resolve, reject) => {
    // --json 是全局标志，需要放在子命令之前
    const fullArgs = [CONFIG.okkiCliPath, '--json', ...args];
    
    execFile('python3', fullArgs, {
      timeout: options.timeout || 10000,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`OKKI CLI 执行失败：${error.message}\n${stderr}`));
        return;
      }
      
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        resolve({ raw: stdout, stderr });
      }
    });
  });
}

// ==================== 同步记录管理 ====================

/**
 * 加载已同步记录
 */
function loadSyncRecords() {
  try {
    if (fs.existsSync(CONFIG.syncRecordFile)) {
      const data = fs.readFileSync(CONFIG.syncRecordFile, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    log(`加载同步记录失败：${e.message}`, 'WARN');
  }
  return {};
}

/**
 * 保存同步记录
 */
function saveSyncRecord(draftId, metadata = {}) {
  try {
    const records = loadSyncRecords();
    records[draftId] = {
      synced_at: new Date().toISOString(),
      ...metadata
    };
    fs.writeFileSync(CONFIG.syncRecordFile, JSON.stringify(records, null, 2));
    return true;
  } catch (e) {
    log(`保存同步记录失败：${e.message}`, 'WARN');
    return false;
  }
}

/**
 * 检查草稿是否已同步
 */
function isSynced(draftId) {
  const records = loadSyncRecords();
  return !!records[draftId];
}

// ==================== 客户匹配 ====================

/**
 * 从邮箱地址提取域名
 */
function extractDomain(email) {
  if (!email || typeof email !== 'string') {
    return null;
  }
  const match = email.match(/@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/);
  return match ? match[1].toLowerCase() : null;
}

/**
 * 公共域名黑名单
 */
const PUBLIC_DOMAINS = [
  'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
  'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
  'icloud.com', 'me.com', 'mac.com', 'live.com', 'msn.com'
];

/**
 * 检查域名是否为公共域名
 */
function isPublicDomain(domain) {
  if (!domain) return true;
  return PUBLIC_DOMAINS.includes(domain.toLowerCase());
}

/**
 * 通过域名搜索 OKKI 客户
 */
async function searchCustomerByDomain(domain) {
  if (!domain || isPublicDomain(domain)) {
    return null;
  }
  
  try {
    const result = await execOkkiCli(['company', 'list', '-k', domain, '-l', '5']);
    
    if (result.data && result.data.length > 0) {
      // 精确匹配域名
      const exactMatch = result.data.find(company => {
        const companyDomain = extractDomain(company.website || company.email || '');
        return companyDomain === domain;
      });
      
      if (exactMatch) {
        return {
          company_id: exactMatch.company_id || exactMatch.id,
          name: exactMatch.name,
          match_type: 'domain_exact',
          confidence: 0.95
        };
      }
      
      // 部分匹配
      if (result.data.length > 0) {
        return {
          company_id: result.data[0].company_id || result.data[0].id,
          name: result.data[0].name,
          match_type: 'domain_partial',
          confidence: 0.7
        };
      }
    }
    
    return null;
  } catch (e) {
    log(`域名搜索失败：${e.message}`, 'WARN');
    return null;
  }
}

/**
 * 通过客户名称搜索 OKKI 客户
 */
async function searchCustomerByName(name) {
  if (!name) {
    return null;
  }
  
  try {
    const result = await execOkkiCli(['company', 'list', '-k', name, '-l', '5']);
    
    if (result.data && result.data.length > 0) {
      // 精确匹配名称
      const exactMatch = result.data.find(company => 
        company.name.toLowerCase() === name.toLowerCase()
      );
      
      if (exactMatch) {
        return {
          company_id: exactMatch.company_id || exactMatch.id,
          name: exactMatch.name,
          match_type: 'name_exact',
          confidence: 0.95
        };
      }
      
      // 部分匹配
      return {
        company_id: result.data[0].company_id || result.data[0].id,
        name: result.data[0].name,
        match_type: 'name_partial',
        confidence: 0.7
      };
    }
    
    return null;
  } catch (e) {
    log(`名称搜索失败：${e.message}`, 'WARN');
    return null;
  }
}

/**
 * 匹配客户（优先使用 customer_id，其次邮箱域名，最后名称）
 */
async function matchCustomer(draft) {
  // 如果 draft 已经有 OKKI company_id，直接使用
  if (draft.okki_company_id) {
    log(`使用已有 OKKI 客户 ID：${draft.okki_company_id}`);
    return {
      company_id: draft.okki_company_id,
      name: draft.customer_name,
      match_type: 'existing_id',
      confidence: 1.0
    };
  }
  
  // 尝试通过邮箱域名匹配
  if (draft.customer_email) {
    const domain = extractDomain(draft.customer_email);
    if (domain && !isPublicDomain(domain)) {
      const domainResult = await searchCustomerByDomain(domain);
      if (domainResult) {
        return domainResult;
      }
    }
  }
  
  // 尝试通过客户名称匹配
  if (draft.customer_name) {
    const nameResult = await searchCustomerByName(draft.customer_name);
    if (nameResult) {
      return nameResult;
    }
  }
  
  return null;
}

// ==================== 创建跟进记录 ====================

/**
 * 创建 OKKI 跟进记录
 */
async function createFollowUpTrail(companyId, draft) {
  // 构建跟进内容
  const stageLabels = {
    'new_inquiry': '新询盘',
    'quoted': '已报价',
    'sample_sent': '已寄样',
    'negotiating': '谈判中',
    'closed_won': '成交',
    'lost': '流失'
  };
  
  const stageLabel = stageLabels[draft.stage] || draft.stage;
  const followUpDay = draft.follow_up_day || 0;
  
  let content = `跟进提醒：${stageLabel}阶段\n`;
  content += `客户：${draft.customer_name}\n`;
  content += `邮箱：${draft.customer_email || '(未提供)'}\n`;
  content += `跟进类型：${draft.intent || '常规跟进'}\n`;
  content += `跟进时机：第${followUpDay}天\n`;
  
  if (draft.template_id) {
    content += `使用模板：${draft.template_id}\n`;
  }
  
  if (draft.subject) {
    content += `邮件主题：${draft.subject}\n`;
  }
  
  content += `\n[自动生成的跟进草稿，待审核发送]`;
  
  try {
    const result = await execOkkiCli([
      'trail', 'add',
      '--company', companyId,
      '--content', content,
      '--type', CONFIG.TRAIL_TYPE.FOLLOW_UP.toString()
    ]);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add'
    };
  } catch (e) {
    return {
      success: false,
      reason: 'api_error',
      message: e.message,
      company_id: companyId
    };
  }
}

// ==================== 草稿文件处理 ====================

/**
 * 读取所有待同步的草稿
 */
function loadPendingDrafts() {
  const drafts = [];
  
  if (!fs.existsSync(CONFIG.draftsDir)) {
    log(`草稿目录不存在：${CONFIG.draftsDir}`, 'WARN');
    return drafts;
  }
  
  const files = fs.readdirSync(CONFIG.draftsDir);
  
  for (const file of files) {
    if (!file.startsWith('draft-') || !file.endsWith('.json')) {
      continue;
    }
    
    const filepath = path.join(CONFIG.draftsDir, file);
    
    try {
      const draft = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      
      // 只处理 status 为 draft 的草稿
      if (draft.status === 'draft') {
        drafts.push({ filepath, ...draft });
      }
    } catch (e) {
      log(`读取草稿文件失败 ${file}: ${e.message}`, 'WARN');
    }
  }
  
  return drafts;
}

/**
 * 更新草稿状态
 */
function updateDraftStatus(draft, newStatus, okkiTrailId = null) {
  const updatedDraft = {
    ...draft,
    status: newStatus,
    updated_at: new Date().toISOString()
  };
  
  if (okkiTrailId) {
    updatedDraft.okki_trail_id = okkiTrailId;
  }
  
  fs.writeFileSync(draft.filepath, JSON.stringify(updatedDraft, null, 2), 'utf8');
  log(`草稿状态更新：${draft.draft_id} → ${newStatus}`);
}

// ==================== 主同步逻辑 ====================

/**
 * 执行同步
 */
async function runSync(options = {}) {
  const { dryRun = false, draftIds = null } = options;
  
  log('='.repeat(60));
  log('OKKI Integration - 跟进草稿同步');
  log(`模式：${dryRun ? 'DRY-RUN' : 'LIVE'}`);
  log('='.repeat(60));
  
  const results = {
    total_drafts: 0,
    synced: 0,
    skipped: 0,
    failed: 0,
    details: []
  };
  
  try {
    // 1. 加载待同步草稿
    let drafts = loadPendingDrafts();
    
    // 如果指定了 draftIds，只处理这些
    if (draftIds && draftIds.length > 0) {
      drafts = drafts.filter(d => draftIds.includes(d.draft_id));
    }
    
    results.total_drafts = drafts.length;
    log(`找到 ${drafts.length} 个待同步草稿`);
    
    if (drafts.length === 0) {
      log('没有需要同步的草稿');
      return { success: true, ...results };
    }
    
    log('-'.repeat(60));
    
    // 2. 逐个处理草稿
    for (const draft of drafts) {
      log(`处理草稿：${draft.draft_id}`);
      log(`  客户：${draft.customer_name} (${draft.customer_email || '无邮箱'})`);
      log(`  阶段：${draft.stage}`);
      log(`  模板：${draft.template_id}`);
      
      // 检查是否已同步
      if (isSynced(draft.draft_id)) {
        log(`  跳过：已同步`);
        results.skipped++;
        results.details.push({
          draft_id: draft.draft_id,
          status: 'skipped',
          reason: 'already_synced'
        });
        continue;
      }
      
      if (dryRun) {
        log(`  [DRY-RUN] 将创建 OKKI 跟进记录`);
        results.synced++;
        results.details.push({
          draft_id: draft.draft_id,
          status: 'dry_run',
          customer: draft.customer_name
        });
        continue;
      }
      
      // 3. 匹配客户
      const customer = await matchCustomer(draft);
      
      if (!customer) {
        log(`  失败：未找到匹配的 OKKI 客户`, 'ERROR');
        results.failed++;
        results.details.push({
          draft_id: draft.draft_id,
          status: 'failed',
          reason: 'customer_not_found',
          customer_name: draft.customer_name,
          customer_email: draft.customer_email
        });
        continue;
      }
      
      log(`  匹配客户：${customer.name} (${customer.company_id}) [${customer.match_type}, confidence=${customer.confidence}]`);
      
      // 4. 创建跟进记录
      const trailResult = await createFollowUpTrail(customer.company_id, draft);
      
      if (trailResult.success) {
        log(`  ✓ OKKI 跟进记录创建成功：${trailResult.trail_id}`);
        
        // 5. 更新草稿状态
        updateDraftStatus(draft, 'synced', trailResult.trail_id);
        
        // 6. 记录同步
        saveSyncRecord(draft.draft_id, {
          okki_company_id: customer.company_id,
          okki_trail_id: trailResult.trail_id,
          match_type: customer.match_type
        });
        
        results.synced++;
        results.details.push({
          draft_id: draft.draft_id,
          status: 'synced',
          customer: draft.customer_name,
          okki_company_id: customer.company_id,
          okki_trail_id: trailResult.trail_id
        });
      } else {
        log(`  失败：${trailResult.reason} - ${trailResult.message}`, 'ERROR');
        results.failed++;
        results.details.push({
          draft_id: draft.draft_id,
          status: 'failed',
          reason: trailResult.reason,
          message: trailResult.message
        });
      }
    }
    
    // 3. 输出摘要
    log('='.repeat(60));
    log('同步完成摘要');
    log('='.repeat(60));
    log(`草稿总数：${results.total_drafts}`);
    log(`同步成功：${results.synced}`);
    log(`跳过：${results.skipped}`);
    log(`失败：${results.failed}`);
    
    if (dryRun) {
      log('');
      log('DRY-RUN 模式：未实际创建 OKKI 记录');
    }
    
    return { success: true, ...results };
    
  } catch (error) {
    log(`执行失败：${error.message}`, 'ERROR');
    return {
      success: false,
      error: error.message,
      ...results
    };
  }
}

// ==================== CLI 入口 ====================

function main() {
  const args = process.argv.slice(2);
  
  const options = {
    dryRun: args.includes('--dry-run') || args.includes('-n'),
    draftIds: []
  };
  
  // 解析指定的 draft IDs
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--draft' && args[i + 1]) {
      options.draftIds.push(args[i + 1]);
      i++;
    }
  }
  
  runSync(options).then(result => {
    // 输出 JSON 结果（便于 cron 调用）
    console.log('\n--- JSON RESULT ---');
    console.log(JSON.stringify(result, null, 2));
    
    // 退出码
    process.exit(result.success ? 0 : 1);
  }).catch(error => {
    log(`致命错误：${error.message}`, 'ERROR');
    process.exit(1);
  });
}

// ==================== 导出 ====================

module.exports = {
  runSync,
  loadPendingDrafts,
  matchCustomer,
  createFollowUpTrail,
  updateDraftStatus,
  loadSyncRecords,
  saveSyncRecord,
  isSynced,
  CONFIG
};

// 直接运行时执行
if (require.main === module) {
  main();
}

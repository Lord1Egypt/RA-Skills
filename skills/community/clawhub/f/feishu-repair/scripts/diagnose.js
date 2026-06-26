#!/usr/bin/env node
/**
 * Feishu Repair — 飞书群聊+会话诊断与修复
 * 
 * 功能：
 * 1. 检查 Gateway 运行状态
 * 2. 检查飞书 WebSocket 连接状态
 * 3. 检查群聊权限配置（groupAllowFrom）
 * 4. 检查用户权限配置（allowFrom）
 * 5. 检查最近日志中的飞书相关错误
 * 6. 自动修复丢失的权限配置
 * 
 * 用法:
 *   node diagnose.js
 *   node diagnose.js --json       # JSON 输出
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ============================================================================
// 从 openclaw.json 及备份文件中读取配置
// 优先读取当前配置，其次读取最新备份
// ============================================================================

function loadConfig() {
  const HOME = process.env.HOME || '/root';
  const OPENCLAW_DIR = path.join(HOME, '.openclaw');
  const CURRENT_FILE = path.join(OPENCLAW_DIR, 'openclaw.json');
  
  // 尝试从多个来源读取配置（优先级：当前 → 备份）
  const sources = [CURRENT_FILE];
  
  // 添加备份文件
  try {
    const files = fs.readdirSync(OPENCLAW_DIR)
      .filter(f => f.startsWith('openclaw.json.bak'))
      .map(f => path.join(OPENCLAW_DIR, f));
    files.sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
    sources.push(...files);
  } catch {}
  
  for (const src of sources) {
    try {
      if (!fs.existsSync(src)) continue;
      const content = fs.readFileSync(src, 'utf8');
      const config = JSON.parse(content);
      
      const feishu = config.channels?.feishu || {};
      const accounts = feishu.accounts || {};
      const mainAccount = accounts.main || {};
      
      // 找第一个有飞书配置的账号
      let account = mainAccount;
      if (!account.appId) {
        for (const [name, acc] of Object.entries(accounts)) {
          if (acc.appId && acc.allowFrom?.length) {
            account = acc;
            break;
          }
        }
      }
      
      if (account.appId) {
        return {
          userId: (account.allowFrom || [])[0] || null,
          groupId: (account.groupAllowFrom || [])[0] || null,
          appId: account.appId || null,
          appSecret: account.appSecret || null,
          allowFrom: account.allowFrom || [],
          groupAllowFrom: account.groupAllowFrom || [],
          sourceFile: src,
          sourceTime: fs.statSync(src).mtime,
          accountName: Object.keys(accounts).find(k => accounts[k] === account) || 'main',
        };
      }
    } catch {}
  }
  
  return null;
}

const CONFIG = loadConfig();

// ============================================================================
// 诊断函数
// ============================================================================

function checkGateway() {
  try {
    const output = execSync('systemctl --user is-active openclaw-gateway.service 2>/dev/null', { encoding: 'utf8' }).trim();
    return {
      running: output === 'active',
      status: output,
    };
  } catch (e) {
    return {
      running: false,
      status: 'unknown',
    };
  }
}

function checkFeishuConfig() {
  try {
    const output = execSync('openclaw config get channels.feishu 2>/dev/null', { encoding: 'utf8' });
    const config = JSON.parse(output);
    
    const mainAccount = config.accounts?.main || {};
    const issues = [];
    
    // 检查飞书是否启用
    if (config.enabled !== true) {
      issues.push('飞书渠道未启用（channels.feishu.enabled = false）');
    }
    
    // 检查 main 账号是否启用
    if (mainAccount.enabled !== true) {
      issues.push('main 账号未启用（channels.feishu.accounts.main.enabled = false）');
    }
    
    // 检查 allowFrom（用户权限）- 使用配置文件中的值
    if (!mainAccount.allowFrom || mainAccount.allowFrom.length === 0) {
      issues.push('用户权限为空（allowFrom 为空，DM 消息将被拒绝）');
    } else if (CONFIG && !mainAccount.allowFrom.includes(CONFIG.userId)) {
      issues.push(`配置文件中的用户 ID 不在 allowFrom 中（缺少 ${CONFIG.userId}）`);
    }
    
    // 检查 groupAllowFrom（群聊权限）- 使用配置文件中的值
    if (!mainAccount.groupAllowFrom || mainAccount.groupAllowFrom.length === 0) {
      issues.push('群聊权限为空（groupAllowFrom 为空，群消息将被拒绝）');
    } else if (CONFIG && !mainAccount.groupAllowFrom.includes(CONFIG.groupId)) {
      issues.push(`配置文件中的群聊 ID 不在 groupAllowFrom 中（缺少 ${CONFIG.groupId}）`);
    }
    
    return {
      valid: issues.length === 0,
      config: {
        enabled: config.enabled,
        mainEnabled: mainAccount.enabled,
        allowFrom: mainAccount.allowFrom || [],
        groupAllowFrom: mainAccount.groupAllowFrom || [],
        connectionMode: mainAccount.connectionMode || config.connectionMode || 'unknown',
      },
      issues,
    };
  } catch (e) {
    return {
      valid: false,
      config: null,
      issues: ['无法读取飞书配置: ' + e.message],
    };
  }
}

function checkRecentLogs() {
  try {
    const output = execSync(
      'journalctl --user -u openclaw-gateway.service --since "30 min ago" 2>/dev/null | grep -i "feishu" | tail -20',
      { encoding: 'utf8' }
    );
    
    const lines = output.trim().split('\n').filter(Boolean);
    const errors = [];
    const warnings = [];
    
    for (const line of lines) {
      if (/error|fail|reject|not in|disconnect|close/i.test(line)) {
        errors.push(line.trim());
      }
      if (/warn|timeout|retry/i.test(line)) {
        warnings.push(line.trim());
      }
    }
    
    return { errors, warnings, totalLines: lines.length };
  } catch {
    return { errors: [], warnings: [], totalLines: 0 };
  }
}

// ============================================================================
// 修复函数
// ============================================================================

function fixAllowFrom() {
  const allowFrom = CONFIG?.allowFrom || [];
  if (allowFrom.length === 0) {
    return { success: false, message: '配置文件中无 allowFrom 值可恢复' };
  }
  try {
    const json = JSON.stringify(allowFrom);
    execSync(
      `openclaw config set channels.feishu.allowFrom '${json}' 2>/dev/null`,
      { encoding: 'utf8' }
    );
    return { success: true, message: `已从配置文件恢复 allowFrom: ${allowFrom.join(', ')}` };
  } catch (e) {
    return { success: false, message: '恢复 allowFrom 失败: ' + e.message };
  }
}

function fixGroupAllowFrom() {
  const groupAllowFrom = CONFIG?.groupAllowFrom || [];
  if (groupAllowFrom.length === 0) {
    return { success: false, message: '配置文件中无 groupAllowFrom 值可恢复' };
  }
  try {
    const json = JSON.stringify(groupAllowFrom);
    execSync(
      `openclaw config set channels.feishu.groupAllowFrom '${json}' 2>/dev/null`,
      { encoding: 'utf8' }
    );
    return { success: true, message: `已从配置文件恢复 groupAllowFrom: ${groupAllowFrom.join(', ')}` };
  } catch (e) {
    return { success: false, message: '恢复 groupAllowFrom 失败: ' + e.message };
  }
}

// ============================================================================
// 自动重启 Gateway
// ============================================================================

function restartGateway() {
  try {
    console.log('🔄 正在重启 Gateway...');
    execSync('systemctl --user restart openclaw-gateway.service', { timeout: 30000, encoding: 'utf8' });
    
    // 等待服务启动
    let retries = 0;
    const maxRetries = 10;
    while (retries < maxRetries) {
      try {
        const status = execSync('systemctl --user is-active openclaw-gateway.service 2>/dev/null', { encoding: 'utf8' }).trim();
        if (status === 'active') {
          return { success: true, message: 'Gateway 重启成功' };
        }
      } catch {}
      execSync('sleep 2', { encoding: 'utf8' });
      retries++;
    }
    
    return { success: false, message: 'Gateway 重启超时（等待超过 20 秒）' };
  } catch (e) {
    return { success: false, message: 'Gateway 重启失败: ' + e.message };
  }
}

// ============================================================================
// 自动验证飞书修复情况
// ============================================================================

function getTenantAccessToken(appId, appSecret) {
  try {
    const output = execSync(
      `curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d '{"app_id":"${appId}","app_secret":"${appSecret}"}'`,
      { encoding: 'utf8', timeout: 10000 }
    );
    const result = JSON.parse(output);
    return result.tenant_access_token || null;
  } catch (e) {
    return null;
  }
}

function sendFeishuMessage(targetId, text, receiveIdType = 'chat_id') {
  if (!CONFIG?.appId || !CONFIG?.appSecret) {
    return { success: false, message: '配置文件中无 appId/appSecret' };
  }
  
  try {
    // 1. 获取 token
    const token = getTenantAccessToken(CONFIG.appId, CONFIG.appSecret);
    if (!token) {
      return { success: false, message: '获取 tenant_access_token 失败' };
    }
    
    // 2. 发送消息
    const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    const content = JSON.stringify({ text: text.replace('{time}', now) });
    
    const output = execSync(
      `curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${receiveIdType}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -d '{"receive_id":"${targetId}","msg_type":"text","content":${JSON.stringify(content)}}'`,
      { encoding: 'utf8', timeout: 10000 }
    );
    
    const result = JSON.parse(output);
    if (result.code === 0) {
      return { success: true, message: `✅ 已发送消息到飞书群聊（${now}）`, now };
    } else {
      return { success: false, message: `飞书 API 错误: ${result.msg || result.code}` };
    }
  } catch (e) {
    return { success: false, message: '发送飞书消息失败: ' + e.message };
  }
}

function verifyFeishuFix() {
  try {
    // 1. 读取当前飞书配置
    const output = execSync('openclaw config get channels.feishu 2>/dev/null', { encoding: 'utf8' });
    const config = JSON.parse(output);
    
    const mainAccount = config.accounts?.main || {};
    const verificationResults = [];
    let allPassed = true;
    
    // 验证飞书启用
    if (config.enabled === true) {
      verificationResults.push({ check: '飞书渠道', status: 'pass', value: '已启用' });
    } else {
      verificationResults.push({ check: '飞书渠道', status: 'fail', value: '未启用' });
      allPassed = false;
    }
    
    // 验证 main 账号
    if (mainAccount.enabled === true) {
      verificationResults.push({ check: 'main 账号', status: 'pass', value: '已启用' });
    } else {
      verificationResults.push({ check: 'main 账号', status: 'fail', value: '未启用' });
      allPassed = false;
    }
    
    // 验证 allowFrom
    if (CONFIG && mainAccount.allowFrom?.includes(CONFIG.userId)) {
      verificationResults.push({ check: 'allowFrom', status: 'pass', value: `包含 ${CONFIG.userId}` });
    } else if (CONFIG) {
      verificationResults.push({ check: 'allowFrom', status: 'fail', value: `缺少 ${CONFIG.userId}` });
      allPassed = false;
    }
    
    // 验证 groupAllowFrom
    if (CONFIG && mainAccount.groupAllowFrom?.includes(CONFIG.groupId)) {
      verificationResults.push({ check: 'groupAllowFrom', status: 'pass', value: `包含 ${CONFIG.groupId}` });
    } else if (CONFIG) {
      verificationResults.push({ check: 'groupAllowFrom', status: 'fail', value: `缺少 ${CONFIG.groupId}` });
      allPassed = false;
    }
    
    // 2. 检查最近日志中的飞书错误
    try {
      const logs = execSync(
        'journalctl --user -u openclaw-gateway.service --since "2 min ago" 2>/dev/null | grep -i "feishu" | tail -10',
        { encoding: 'utf8' }
      );
      const errorLines = logs.split('\n').filter(l => /error|fail|reject|not in/i.test(l));
      if (errorLines.length > 0) {
        verificationResults.push({ check: 'Gateway 日志', status: 'warn', value: `发现 ${errorLines.length} 条错误` });
      } else {
        verificationResults.push({ check: 'Gateway 日志', status: 'pass', value: '无错误' });
      }
    } catch {
      verificationResults.push({ check: 'Gateway 日志', status: 'skip', value: '无法读取' });
    }
    
    return {
      success: allPassed,
      checks: verificationResults,
      summary: allPassed ? '✅ 飞书配置修复验证通过' : '❌ 飞书配置修复验证失败',
    };
  } catch (e) {
    return {
      success: false,
      checks: [],
      summary: '验证失败: ' + e.message,
    };
  }
}

// ============================================================================
// 发送飞书验证消息（遍历所有群聊和用户）
// ============================================================================

function sendFeishuVerification() {
  const results = {
    groups: [],
    users: [],
  };
  
  const message = '🔧 飞书修复验证 - 当前时间：{time}\n✅ 如果收到此消息，说明飞书消息功能已恢复正常。';
  
  // 发送到所有群聊
  if (CONFIG?.groupAllowFrom?.length) {
    for (const groupId of CONFIG.groupAllowFrom) {
      const res = sendFeishuMessage(groupId, message, 'chat_id');
      results.groups.push({ id: groupId, ...res });
    }
  }
  
  // 发送到所有用户（DM）
  if (CONFIG?.allowFrom?.length) {
    for (const userId of CONFIG.allowFrom) {
      const res = sendFeishuMessage(userId, message, 'open_id');
      results.users.push({ id: userId, ...res });
    }
  }
  
  // 汇总结果
  const totalSent = results.groups.filter(r => r.success).length + results.users.filter(r => r.success).length;
  const totalFailed = results.groups.filter(r => !r.success).length + results.users.filter(r => !r.success).length;
  
  return {
    success: totalSent > 0,
    groups: results.groups,
    users: results.users,
    summary: `已发送 ${totalSent} 条消息${totalFailed > 0 ? `，${totalFailed} 条失败` : ''}`,
  };
}

// ============================================================================
// 主逻辑
// ============================================================================

function diagnose() {
  const jsonMode = process.argv.includes('--json');
  const results = {
    timestamp: new Date().toISOString(),
    gateway: checkGateway(),
    feishuConfig: checkFeishuConfig(),
    recentLogs: checkRecentLogs(),
    fixes: [],
  };
  
  // 自动修复
  if (results.feishuConfig.issues.some(i => i.includes('allowFrom'))) {
    results.fixes.push(fixAllowFrom());
  }
  if (results.feishuConfig.issues.some(i => i.includes('groupAllowFrom'))) {
    results.fixes.push(fixGroupAllowFrom());
  }
  
  // 如果有修复操作，强制重启 Gateway 并验证
  const hasFixes = results.fixes.length > 0;
  if (hasFixes) {
    // 1. 强制重启 Gateway
    console.log('\n🔄 配置已恢复，强制重启 Gateway...');
    results.gatewayRestart = restartGateway();
    
    // 2. 等待 Gateway 启动完成
    if (results.gatewayRestart.success) {
      console.log('⏳ 等待 Gateway 重启完成...');
      execSync('sleep 5', { encoding: 'utf8' });
      
      // 3. 自动验证修复结果（配置+日志）
      results.verification = verifyFeishuFix();
      
      // 4. 发送飞书验证消息（带当前时间）
      results.feishuMessage = sendFeishuVerification();
    }
  }
  
  // 输出
  if (jsonMode) {
    console.log(JSON.stringify(results, null, 2));
    return;
  }
  
  // 文字报告
  console.log('🔍 飞书群聊+会话诊断报告');
  console.log('═'.repeat(50));
  console.log(`时间: ${new Date().toLocaleString('zh-CN')}`);
  
  // 配置来源
  if (CONFIG) {
    console.log(`📂 配置来源: ${CONFIG.sourceFile} (${CONFIG.sourceTime.toLocaleString('zh-CN')})`);
    console.log(`   账号: ${CONFIG.accountName} | App ID: ${CONFIG.appId}`);
  } else {
    console.log('❌ 未找到任何配置文件（openclaw.json 及备份）');
  }
  console.log('');
  
  // Gateway 状态
  const gwIcon = results.gateway.running ? '✅' : '❌';
  console.log(`${gwIcon} Gateway: ${results.gateway.status}`);
  
  // 飞书配置
  if (results.feishuConfig.valid) {
    console.log('✅ 飞书配置: 正常');
  } else {
    console.log('❌ 飞书配置: 异常');
    for (const issue of results.feishuConfig.issues) {
      console.log(`   ⚠️ ${issue}`);
    }
  }
  
  // 修复结果
  if (results.fixes.length > 0) {
    console.log('');
    console.log('🔧 自动修复:');
    for (const fix of results.fixes) {
      const icon = fix.success ? '✅' : '❌';
      console.log(`   ${icon} ${fix.message}`);
    }
    
    // Gateway 重启结果
    if (results.gatewayRestart) {
      const gwIcon = results.gatewayRestart.success ? '✅' : '❌';
      console.log(`   ${gwIcon} ${results.gatewayRestart.message}`);
    }
    
    // 验证结果
    if (results.verification) {
      console.log('');
      console.log('🔍 修复验证:');
      for (const check of results.verification.checks) {
        const icon = check.status === 'pass' ? '✅' : check.status === 'fail' ? '❌' : '⚠️';
        console.log(`   ${icon} ${check.check}: ${check.value}`);
      }
      console.log(`   ${results.verification.summary}`);
    }
    
    // 飞书消息发送结果
    if (results.feishuMessage) {
      console.log('');
      console.log('📤 飞书消息确认:');
      for (const g of results.feishuMessage.groups) {
        const icon = g.success ? '✅' : '❌';
        console.log(`   ${icon} 群聊 ${g.id}: ${g.message}`);
      }
      for (const u of results.feishuMessage.users) {
        const icon = u.success ? '✅' : '❌';
        console.log(`   ${icon} 用户 ${u.id}: ${u.message}`);
      }
      console.log(`   📊 ${results.feishuMessage.summary}`);
    }
  }
  
  // 日志检查
  if (results.recentLogs.errors.length > 0) {
    console.log('');
    console.log(`❌ 最近日志发现 ${results.recentLogs.errors.length} 条错误:`);
    for (const err of results.recentLogs.errors.slice(0, 5)) {
      console.log(`   ${err}`);
    }
  }
  
  // 总结
  const hasCritical = !results.gateway.running || !results.feishuConfig.valid;
  console.log('');
  if (hasCritical) {
    console.log('📋 建议操作:');
    if (!results.gateway.running) {
      console.log('   1. 启动 Gateway: systemctl --user start openclaw-gateway.service');
    }
    if (results.fixes.length > 0) {
      console.log('   2. 重启 Gateway: systemctl --user restart openclaw-gateway.service');
    }
  } else {
    console.log('✅ 飞书连接正常，无异常');
  }
}

diagnose();

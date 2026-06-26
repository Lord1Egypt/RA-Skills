#!/usr/bin/env node

/**
 * DeBox Community Management CLI
 * 
 * Commands:
 *   info          - Query group information
 *   check-member  - Verify user is in group
 *   user-info     - Get user profile (nickname, avatar, wallet)
 *   vote-stats    - Query user voting data
 *   lottery-stats - Query user lottery data
 *   praise-info   - Query user praise/like data
 *   profile       - Personal data report (with image export)
 *   verify        - Comprehensive verification
 *   batch-verify  - Batch verify wallets
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

// Configuration
const DEBOX_API_BASE = 'https://open.debox.pro/openapi';
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

// Load config
function loadConfig() {
  const config = {};
  
  // From file
  if (fs.existsSync(CONFIG_FILE)) {
    const fileConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    Object.assign(config, fileConfig);
  }
  
  // From environment (takes precedence)
  if (process.env.DEBOX_API_KEY) {
    config.apiKey = process.env.DEBOX_API_KEY;
  }
  if (process.env.DEBOX_DEFAULT_GROUP) {
    config.defaultGroupId = process.env.DEBOX_DEFAULT_GROUP;
  }
  
  return config;
}

// HTTP request helper
function request(method, endpoint, params = {}, headers = {}) {
  return new Promise((resolve, reject) => {
    const config = loadConfig();
    
    // Add API key to headers
    if (config.apiKey) {
      headers['X-API-KEY'] = config.apiKey;
    }
    
    // Build URL
    const url = new URL(`${DEBOX_API_BASE}${endpoint}`);
    if (method === 'GET' && Object.keys(params).length > 0) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value);
      });
    }
    
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          // 检查 HTTP 状态码和业务状态码
          const httpOk = res.statusCode >= 200 && res.statusCode < 300;
          const bizOk = parsed.code === undefined || parsed.code === 200 || parsed.success === true;
          
          if (httpOk && bizOk) {
            resolve(parsed);
          } else {
            // 返回完整的错误信息，包含 code 和 message
            const error = new Error(parsed.message || `HTTP ${res.statusCode}`);
            error.code = parsed.code;
            error.response = parsed;
            reject(error);
          }
        } catch (e) {
          reject(new Error(`Parse error: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    
    if (method === 'POST' && Object.keys(params).length > 0) {
      req.write(JSON.stringify(params));
    }
    
    req.end();
  });
}

// Extract group ID from URL
function extractGroupId(url) {
  const match = url.match(/[?&]id=([^&]+)/);
  return match ? match[1] : url;
}

// Commands

/**
 * Get group information
 */
async function groupInfo(groupUrl) {
  const result = await request('GET', '/group/info', {
    group_invite_url: groupUrl
  });
  return result;
}

/**
 * Check if user is in group
 */
async function checkMember(walletAddress, groupUrl, chainId = 1) {
  const result = await request('GET', '/group/is_join', {
    walletAddress: walletAddress,
    url: groupUrl,
    chain_id: chainId
  });
  return result;
}

/**
 * Get user profile (nickname, avatar, wallet address)
 * Query by user_id only (API limitation)
 */
async function userInfo(userId) {
  const result = await request('GET', '/user/info', {
    user_id: userId
  });
  return result;
}

/**
 * Get user vote stats in group
 */
async function voteStats(walletAddress, groupId, chainId = 1) {
  try {
    const result = await request('GET', '/vote/info', {
      walletAddress: walletAddress,
      group_id: groupId,
      chain_id: chainId
    });
    return result;
  } catch (e) {
    // 优化错误提示：群组暂无投票活动
    if (e.code === 400 || (e.message && e.message.includes('Param error'))) {
      return { 
        code: 200, 
        success: true,
        data: { count: 0 }, 
        message: '群组暂无投票活动',
        noActivity: true 
      };
    }
    throw e;
  }
}

/**
 * Get user lottery stats in group
 */
async function lotteryStats(walletAddress, groupId, chainId = 1) {
  try {
    const result = await request('GET', '/lucky_draw/info', {
      walletAddress: walletAddress,
      group_id: groupId,
      chain_id: chainId
    });
    return result;
  } catch (e) {
    // 优化错误提示：群组暂无抽奖活动
    if (e.code === 400 || (e.message && e.message.includes('Param error'))) {
      return { 
        code: 200, 
        success: true,
        data: { count: 0 }, 
        message: '群组暂无抽奖活动',
        noActivity: true 
      };
    }
    throw e;
  }
}

/**
 * Get user praise/like info
 */
async function praiseInfo(walletAddress, chainId = 1) {
  const result = await request('GET', '/moment/praise_info', {
    wallet_address: walletAddress,
    chain_id: chainId
  });
  return result;
}

/**
 * Get user profile report (comprehensive personal data)
 */
async function userProfile(userId, chainId = 1) {
  // 1. Get basic user info
  const userResult = await userInfo(userId);
  const userData = userResult.data || userResult;
  
  // 2. Get praise data using wallet address
  const wallet = userData.wallet_address || userData.wallet;
  let praiseData = { receive_praise_total: 0, send_praise_total: 0 };
  
  if (wallet) {
    try {
      const praiseResult = await praiseInfo(wallet, chainId);
      praiseData = praiseResult.data || praiseResult;
    } catch (e) {
      // Ignore praise errors
    }
  }
  
  return {
    user: userData,
    praise: praiseData
  };
}

/**
 * Comprehensive verification
 */
async function verify(options) {
  const { wallet, groupUrl, minVotes = 0, minLotteries = 0, chainId = 1 } = options;
  
  const results = {
    wallet: wallet,
    passed: false,
    checks: {}
  };
  
  try {
    // Check membership
    const memberResult = await checkMember(wallet, groupUrl, chainId);
    results.checks.isMember = memberResult.joined === true || memberResult.joined === 'true' || memberResult.is_join === true || memberResult.is_join === 'true';
  } catch (e) {
    results.checks.isMember = false;
    results.checks.memberError = e.message;
  }
  
  const groupId = extractGroupId(groupUrl);
  
  // Check votes if required
  if (minVotes > 0) {
    try {
      const voteResult = await voteStats(wallet, groupId, chainId);
      results.checks.voteCount = voteResult.count || 0;
      results.checks.votesPassed = results.checks.voteCount >= minVotes;
    } catch (e) {
      results.checks.voteCount = 0;
      results.checks.votesPassed = false;
      results.checks.voteError = e.message;
    }
  } else {
    results.checks.votesPassed = true;
  }
  
  // Check lotteries if required
  if (minLotteries > 0) {
    try {
      const lotteryResult = await lotteryStats(wallet, groupId, chainId);
      results.checks.lotteryCount = lotteryResult.count || 0;
      results.checks.lotteriesPassed = results.checks.lotteryCount >= minLotteries;
    } catch (e) {
      results.checks.lotteryCount = 0;
      results.checks.lotteriesPassed = false;
      results.checks.lotteryError = e.message;
    }
  } else {
    results.checks.lotteriesPassed = true;
  }
  
  // Overall result
  results.passed = results.checks.isMember && 
                   results.checks.votesPassed && 
                   results.checks.lotteriesPassed;
  
  return results;
}

/**
 * Batch verify wallets
 */
async function batchVerify(file, groupUrl, options = {}) {
  const wallets = fs.readFileSync(file, 'utf8')
    .split('\n')
    .map(w => w.trim())
    .filter(w => w.length > 0);
  
  const results = [];
  
  for (const wallet of wallets) {
    try {
      const result = await verify({ wallet, groupUrl, ...options });
      results.push(result);
    } catch (e) {
      results.push({
        wallet,
        passed: false,
        error: e.message
      });
    }
    
    // Rate limiting
    await new Promise(r => setTimeout(r, 200));
  }
  
  return results;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const config = loadConfig();
  
  if (!config.apiKey) {
    console.error('Error: DEBOX_API_KEY not set');
    console.error('Set it via: export DEBOX_API_KEY="your-key"');
    console.error('Or add to config.json');
    process.exit(1);
  }
  
  try {
    switch (command) {
      case 'info': {
        const url = args.includes('--url') ? args[args.indexOf('--url') + 1] : null;
        if (!url) {
          console.error('Usage: debox-community info --url "https://m.debox.pro/group?id=xxx"');
          process.exit(1);
        }
        const result = await groupInfo(url);
        printGroupInfo(result);
        break;
      }
      
      case 'check-member': {
        const wallet = args.includes('--wallet') ? args[args.indexOf('--wallet') + 1] : null;
        const groupUrl = args.includes('--group-url') ? args[args.indexOf('--group-url') + 1] : null;
        if (!wallet || !groupUrl) {
          console.error('Usage: debox-community check-member --wallet "0x..." --group-url "..."');
          process.exit(1);
        }
        const result = await checkMember(wallet, groupUrl);
        printCheckMember(result, wallet);
        break;
      }
      
      case 'user-info': {
        const userId = args.includes('--user-id') ? args[args.indexOf('--user-id') + 1] : null;
        
        if (!userId) {
          console.error('Usage: debox-community user-info --user-id "xxx"');
          console.error('');
          console.error('Note: This API only supports user_id, not wallet address.');
          process.exit(1);
        }
        
        const result = await userInfo(userId);
        printUserInfo(result);
        break;
      }
      
      case 'vote-stats': {
        const wallet = args.includes('--wallet') ? args[args.indexOf('--wallet') + 1] : null;
        const groupId = args.includes('--group-id') ? args[args.indexOf('--group-id') + 1] : null;
        if (!wallet || !groupId) {
          console.error('Usage: debox-community vote-stats --wallet "0x..." --group-id "xxx"');
          process.exit(1);
        }
        const result = await voteStats(wallet, groupId);
        printVoteStats(result, wallet, groupId);
        break;
      }
      
      case 'lottery-stats': {
        const wallet = args.includes('--wallet') ? args[args.indexOf('--wallet') + 1] : null;
        const groupId = args.includes('--group-id') ? args[args.indexOf('--group-id') + 1] : null;
        if (!wallet || !groupId) {
          console.error('Usage: debox-community lottery-stats --wallet "0x..." --group-id "xxx"');
          process.exit(1);
        }
        const result = await lotteryStats(wallet, groupId);
        printLotteryStats(result, wallet, groupId);
        break;
      }
      
      case 'praise-info': {
        const wallet = args.includes('--wallet') ? args[args.indexOf('--wallet') + 1] : null;
        if (!wallet) {
          console.error('Usage: debox-community praise-info --wallet "0x..."');
          process.exit(1);
        }
        const result = await praiseInfo(wallet);
        printPraiseInfo(result, wallet);
        break;
      }
      
      case 'profile': {
        const userId = args.includes('--user-id') ? args[args.indexOf('--user-id') + 1] : null;
        const saveImage = args.includes('--image');
        const outputPath = args.includes('--output') ? args[args.indexOf('--output') + 1] : 'profile.png';
        
        if (!userId) {
          console.error('Usage: debox-community profile --user-id "xxx" [--image] [--output "profile.png"]');
          console.error('');
          console.error('获取你的 user_id：');
          console.error('  1. 打开 DeBox App');
          console.error('  2. 进入个人主页');
          console.error('  3. 点击右上角分享按钮');
          console.error('  4. 复制链接中的 user_id 参数');
          console.error('');
          console.error('选项：');
          console.error('  --image      生成图片报告');
          console.error('  --output     指定输出文件名（默认：profile.png）');
          process.exit(1);
        }
        
        const result = await userProfile(userId);
        printProfile(result);
        
        if (saveImage) {
          console.log('\n📸 正在生成图片...');
          await generateProfileImage(result, outputPath);
          console.log('✅ 图片已保存：' + outputPath);
        }
        break;
      }
      
      case 'verify': {
        const wallet = args.includes('--wallet') ? args[args.indexOf('--wallet') + 1] : null;
        const groupUrl = args.includes('--group-url') ? args[args.indexOf('--group-url') + 1] : null;
        const minVotes = args.includes('--min-votes') ? parseInt(args[args.indexOf('--min-votes') + 1]) : 0;
        const minLotteries = args.includes('--min-lotteries') ? parseInt(args[args.indexOf('--min-lotteries') + 1]) : 0;
        
        if (!wallet || !groupUrl) {
          console.error('Usage: debox-community verify --wallet "0x..." --group-url "..." [--min-votes N] [--min-lotteries N]');
          process.exit(1);
        }
        
        const result = await verify({ wallet, groupUrl, minVotes, minLotteries });
        printVerify(result);
        break;
      }
      
      case 'batch-verify': {
        const file = args.includes('--file') ? args[args.indexOf('--file') + 1] : null;
        const groupUrl = args.includes('--group-url') ? args[args.indexOf('--group-url') + 1] : null;
        const minVotes = args.includes('--min-votes') ? parseInt(args[args.indexOf('--min-votes') + 1]) : 0;
        const minLotteries = args.includes('--min-lotteries') ? parseInt(args[args.indexOf('--min-lotteries') + 1]) : 0;
        
        if (!file || !groupUrl) {
          console.error('Usage: debox-community batch-verify --file wallets.txt --group-url "..." [--min-votes N]');
          process.exit(1);
        }
        
        const results = await batchVerify(file, groupUrl, { minVotes, minLotteries });
        printBatchVerify(results);
        break;
      }
      
      default:
        console.log('DeBox Community Management CLI');
        console.log('');
        console.log('Commands:');
        console.log('  profile       查看个人数据报告（推荐）');
        console.log('  info          Query group information');
        console.log('  check-member  Verify user is in group');
        console.log('  user-info     Get user profile (nickname, avatar, wallet)');
        console.log('  vote-stats    Query user voting data');
        console.log('  lottery-stats Query user lottery data');
        console.log('  praise-info   Query user praise/like data');
        console.log('  verify        Comprehensive verification');
        console.log('  batch-verify  Batch verify wallets');
        console.log('');
        console.log('Run with --help for command details');
    }
  } catch (error) {
    // 友好的错误提示
    if (error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED') {
      console.error('❌ 网络错误: 无法连接到 DeBox 服务器，请检查网络连接');
    } else if (error.code === 'ETIMEDOUT' || error.message.includes('timeout')) {
      console.error('❌ 网络错误: 请求超时，请稍后重试');
    } else if (error.message.includes('INVALID_API_KEY') || error.code === 401) {
      console.error('❌ 认证错误: API Key 无效或已过期，请检查配置');
    } else if (error.message.includes('rate limit') || error.code === 429) {
      console.error('❌ 请求过于频繁，请稍后重试');
    } else {
      console.error('❌ 错误:', error.message);
    }
    process.exit(1);
  }
}

// ========== 输出格式化函数 ==========

function printGroupInfo(result) {
  console.log('\n========================================');
  console.log('        📊 群组信息');
  console.log('========================================\n');
  
  if (result.code !== 200 && !result.success) {
    console.log('❌ 查询失败:', result.message || '未知错误');
    return;
  }
  
  const data = result.data || result;
  console.log('🏷️  群组名称:', data.group_name || '-');
  console.log('🆔 群组 ID:', data.gid || '-');
  console.log('👥 成员数量:', data.group_number || 0, '/', data.maximum || '∞');
  console.log('📅 创建时间:', data.create_time || '-');
  console.log('💰 收费群:', data.is_charge ? '是' : '否');
  console.log('📺 子频道数:', data.subchannel_number || 0);
  
  if (data.mod_info && data.mod_info.length > 0) {
    console.log('\n👤 管理员信息:');
    data.mod_info.forEach((mod, i) => {
      console.log(`   ${i + 1}. ${mod.name || '-'}`);
      console.log(`      用户ID: ${mod.uid || '-'}`);
      console.log(`      钱包: ${mod.wallet_address || '-'}`);
    });
  }
  
  console.log('\n========================================');
  console.log('✅ 查询完成');
}

function printCheckMember(result, wallet) {
  console.log('\n========================================');
  console.log('        🔍 成员验证');
  console.log('========================================\n');
  
  console.log('💼 钱包地址:', wallet);
  console.log('📋 验证结果:', result.joined === true || result.is_join === true ? '✅ 已加入群组' : '❌ 未加入群组');
  
  if (result.join_time) {
    console.log('📅 加入时间:', result.join_time);
  }
  
  console.log('\n========================================');
}

function printUserInfo(result) {
  console.log('\n========================================');
  console.log('        👤 用户信息');
  console.log('========================================\n');
  
  if (result.code && result.code !== 200 && result.code !== 1) {
    console.log('❌ 查询失败:', result.message || '未知错误');
    return;
  }
  
  const data = result.data || result;
  console.log('🆔 用户ID:', data.user_id || data.uid || '-');
  console.log('📛 昵称:', data.nickname || data.name || '-');
  console.log('💼 钱包地址:', data.wallet || data.wallet_address || '-');
  console.log('🖼️  头像:', data.avatar || data.pic || '-');
  console.log('📝 简介:', data.bio || data.introduction || '-');
  
  console.log('\n========================================');
}

function printVoteStats(result, wallet, groupId) {
  console.log('\n========================================');
  console.log('        📊 投票统计');
  console.log('========================================\n');
  
  console.log('💼 钱包地址:', wallet);
  console.log('🆔 群组 ID:', groupId);
  console.log('');
  
  if (result.noActivity) {
    console.log('⚠️  状态:', result.message);
    console.log('📈 投票次数: 0');
  } else {
    const data = result.data || result;
    console.log('📈 投票次数:', data.count || 0);
    if (data.votes && data.votes.length > 0) {
      console.log('\n📋 投票记录:');
      data.votes.forEach((v, i) => {
        console.log(`   ${i + 1}. ${v.title || '-'}`);
        console.log(`      时间: ${v.voted_at || '-'}`);
      });
    }
  }
  
  console.log('\n========================================');
}

function printLotteryStats(result, wallet, groupId) {
  console.log('\n========================================');
  console.log('        🎰 抽奖统计');
  console.log('========================================\n');
  
  console.log('💼 钱包地址:', wallet);
  console.log('🆔 群组 ID:', groupId);
  console.log('');
  
  if (result.noActivity) {
    console.log('⚠️  状态:', result.message);
    console.log('🎰 抽奖次数: 0');
  } else {
    const data = result.data || result;
    console.log('🎰 抽奖次数:', data.count || 0);
    if (data.draws && data.draws.length > 0) {
      console.log('\n📋 抽奖记录:');
      data.draws.forEach((d, i) => {
        console.log(`   ${i + 1}. ${d.prize || '-'}`);
        console.log(`      时间: ${d.drawn_at || '-'}`);
      });
    }
  }
  
  console.log('\n========================================');
}

function printPraiseInfo(result, wallet) {
  console.log('\n========================================');
  console.log('        ❤️  点赞信息');
  console.log('========================================\n');
  
  console.log('💼 钱包地址:', wallet);
  console.log('');
  
  const data = result.data || result;
  console.log('📥 收到的点赞:', data.receive_praise_total || 0);
  console.log('📤 发出的点赞:', data.send_praise_total || 0);
  
  console.log('\n========================================');
}

function printProfile(result) {
  const user = result.user;
  const praise = result.praise;
  
  console.log('\n╔════════════════════════════════════════╗');
  console.log('║        🎫 DeBox 个人数据报告           ║');
  console.log('╠════════════════════════════════════════╣');
  console.log('║  👤 基本信息                           ║');
  console.log('╠════════════════════════════════════════╣');
  
  const name = user.name || user.nickname || '-';
  console.log('║  昵称：' + name.padEnd(30) + '║');
  
  const uid = user.uid || user.user_id || '-';
  console.log('║  用户ID：' + uid.padEnd(28) + '║');
  
  // 钱包地址截断显示
  const wallet = user.wallet_address || user.wallet || '-';
  const walletDisplay = wallet.length > 20 ? wallet.slice(0, 10) + '...' + wallet.slice(-6) : wallet;
  console.log('║  钱包：' + walletDisplay.padEnd(32) + '║');
  
  // 等级
  const level = user.level || '-';
  console.log('║  等级：Lv.' + String(level).padEnd(29) + '║');
  
  console.log('╠════════════════════════════════════════╣');
  console.log('║  ❤️  社交互动                           ║');
  console.log('╠════════════════════════════════════════╣');
  console.log('║  收到的点赞：' + String(praise.receive_praise_total || 0).padEnd(25) + '║');
  console.log('║  发出的点赞：' + String(praise.send_praise_total || 0).padEnd(25) + '║');
  console.log('╚════════════════════════════════════════╝');
  console.log('');
  console.log('💡 提示：想看更完整的报告？');
  console.log('   加入群组后可查询投票、抽奖数据');
}

/**
 * Generate profile image
 */
/**
 * Generate profile image using sharp
 */
async function generateProfileImage(result, outputPath) {
  const user = result.user;
  const praise = result.praise;
  
  const width = 500;
  const height = 400;
  const bgColor = '#07C160';
  
  // 1. 创建白色卡片背景 (SVG)
  const cardSvg = `<svg width="460" height="360">
    <rect x="0" y="0" width="460" height="360" rx="15" fill="rgba(255,255,255,0.95)"/>
  </svg>`;
  
  // 2. 下载头像到临时文件
  const avatarUrl = user.avatar || user.pic;
  let avatarCircle;
  
  if (avatarUrl) {
    try {
      const tempAvatarPath = path.join(__dirname, '..', 'temp-avatar.png');
      await new Promise((resolve, reject) => {
        https.get(avatarUrl, (res) => {
          if (res.statusCode !== 200) {
            reject(new Error('Failed to download avatar'));
            return;
          }
          const fileStream = fs.createWriteStream(tempAvatarPath);
          res.pipe(fileStream);
          fileStream.on('finish', () => {
            fileStream.close();
            resolve();
          });
        }).on('error', reject);
      });
      
      // 处理头像为圆形
      const circleMask = `<svg width="80" height="80">
        <circle cx="40" cy="40" r="40" fill="white"/>
      </svg>`;
      
      avatarCircle = await sharp(tempAvatarPath)
        .resize(80, 80)
        .composite([{
          input: Buffer.from(circleMask),
          blend: 'dest-in'
        }])
        .png()
        .toBuffer();
      
      // 删除临时文件
      fs.unlinkSync(tempAvatarPath);
    } catch (e) {
      console.log('  ⚠️  Avatar load failed:', e.message);
    }
  }
  
  // 3. 创建头像占位符（如果头像加载失败）
  if (!avatarCircle) {
    const placeholderSvg = `<svg width="80" height="80">
      <circle cx="40" cy="40" r="40" fill="#07C160"/>
      <text x="40" y="50" font-family="Arial" font-size="32" font-weight="bold" text-anchor="middle" fill="white">${(user.name || '?')[0].toUpperCase()}</text>
    </svg>`;
    avatarCircle = Buffer.from(placeholderSvg);
  }
  
  // 4. 创建头像边框
  const avatarBorder = `<svg width="86" height="86">
    <circle cx="43" cy="43" r="42" fill="none" stroke="#07C160" stroke-width="3"/>
  </svg>`;
  
  // 5. 加载并调整 logo 尺寸
  let logo;
  try {
    const logoPath = path.join(__dirname, '..', 'ClawBot.png');
    if (fs.existsSync(logoPath)) {
      logo = await sharp(logoPath)
        .resize(50, 50)
        .png()
        .toBuffer();
    }
  } catch (e) {
    console.log('  ⚠️  Logo load failed:', e.message);
  }
  
  // 6. 创建文字 SVG
  const textSvg = `<svg width="460" height="300">
    <!-- 标题 -->
    <text x="230" y="45" font-family="Arial" font-size="22" font-weight="bold" text-anchor="middle" fill="#333333">DeBox Profile Report</text>
    
    <!-- 用户名 -->
    <text x="200" y="105" font-family="Arial" font-size="22" font-weight="bold" fill="#333333">${user.name || user.nickname || '-'}</text>
    
    <!-- 等级 -->
    <text x="200" y="130" font-family="Arial" font-size="14" fill="#888888">Lv.${user.level || '-'}</text>
    
    <!-- 钱包地址 -->
    <text x="200" y="155" font-family="Arial" font-size="12" fill="#07C160">${(user.wallet_address || user.wallet || '-').slice(0, 8) + '...' + (user.wallet_address || user.wallet || '-').slice(-6)}</text>
    
    <!-- 统计区域背景 -->
    <rect x="20" y="175" width="420" height="85" rx="10" fill="#f5f5f5"/>
    
    <!-- 统计标题 -->
    <text x="230" y="200" font-family="Arial" font-size="16" font-weight="bold" text-anchor="middle" fill="#333333">Social Stats</text>
    
    <!-- Received -->
    <text x="120" y="240" font-family="Arial" font-size="28" font-weight="bold" text-anchor="middle" fill="#07C160">${praise.receive_praise_total || 0}</text>
    <text x="120" y="255" font-family="Arial" font-size="12" text-anchor="middle" fill="#888888">Received</text>
    
    <!-- Sent -->
    <text x="230" y="240" font-family="Arial" font-size="28" font-weight="bold" text-anchor="middle" fill="#f06292">${praise.send_praise_total || 0}</text>
    <text x="230" y="255" font-family="Arial" font-size="12" text-anchor="middle" fill="#888888">Sent</text>
    
    <!-- 用户ID -->
    <text x="360" y="240" font-family="Arial" font-size="11" fill="#999999">ID: ${user.uid || user.user_id || '-'}</text>
  </svg>`;
  
  // 7. 合成最终图片
  const compositeLayers = [
    { input: Buffer.from(cardSvg), top: 20, left: 20 },
    { input: avatarCircle, top: 95, left: 50 },
    { input: Buffer.from(avatarBorder), top: 92, left: 47 },
    { input: Buffer.from(textSvg), top: 20, left: 20 }
  ];
  
  if (logo) {
    compositeLayers.push({ input: logo, top: 335, left: 225 });
  }
  
  await sharp({
    create: {
      width: width,
      height: height,
      channels: 4,
      background: bgColor
    }
  })
  .composite(compositeLayers)
  .png()
  .toFile(outputPath);
  
  return outputPath;
}

function printVerify(result) {
  console.log('\n========================================');
  console.log('        ✅ 综合验证');
  console.log('========================================\n');
  
  console.log('💼 钱包地址:', result.wallet);
  console.log('');
  console.log('📋 验证结果:', result.passed ? '✅ 通过' : '❌ 未通过');
  console.log('');
  console.log('----------------------------------------');
  console.log('详细检查:');
  console.log('----------------------------------------');
  console.log('🔐 是否群成员:', result.checks.isMember ? '✅ 是' : '❌ 否');
  console.log('📊 投票要求:', result.checks.votesPassed ? '✅ 通过' : '❌ 未通过');
  console.log('🎰 抽奖要求:', result.checks.lotteriesPassed ? '✅ 通过' : '❌ 未通过');
  
  if (result.checks.voteCount !== undefined) {
    console.log('   投票次数:', result.checks.voteCount);
  }
  if (result.checks.lotteryCount !== undefined) {
    console.log('   抽奖次数:', result.checks.lotteryCount);
  }
  if (result.checks.memberError) {
    console.log('   成员验证错误:', result.checks.memberError);
  }
  
  console.log('\n========================================');
}

function printBatchVerify(results) {
  console.log('\n========================================');
  console.log('        📋 批量验证结果');
  console.log('========================================\n');
  
  const passed = results.filter(r => r.passed).length;
  const failed = results.length - passed;
  
  console.log('📊 统计: 总计', results.length, '个钱包');
  console.log('   ✅ 通过:', passed);
  console.log('   ❌ 未通过:', failed);
  console.log('');
  console.log('----------------------------------------');
  console.log('详细结果:');
  console.log('----------------------------------------');
  
  results.forEach((r, i) => {
    const status = r.passed ? '✅' : '❌';
    console.log(`${i + 1}. ${status} ${r.wallet}`);
    if (!r.passed && r.error) {
      console.log('   错误:', r.error);
    }
    if (!r.passed && r.checks) {
      console.log('   成员:', r.checks.isMember ? '✅' : '❌');
      console.log('   投票:', r.checks.votesPassed ? '✅' : '❌');
      console.log('   抽奖:', r.checks.lotteriesPassed ? '✅' : '❌');
    }
  });
  
  console.log('\n========================================');
}

main();
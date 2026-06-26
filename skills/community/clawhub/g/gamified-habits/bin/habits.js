#!/usr/bin/env node

/**
 * 游戏化习惯养成 CLI
 * 命令行入口文件
 */

const habits = require('../src/habits');
const xpSystem = require('../src/xp-system');
const storage = require('../src/storage');
const welcome = require('../src/welcome');

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  // 首次使用显示欢迎引导
  if (storage.isFirstTime() && command !== 'guide') {
    console.log(welcome.showWelcomeGuide());
    console.log(`\n📌 输入 "habits guide" 可以再次查看引导\n`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━\n`);
  }
  
  if (!command) {
    showHelp();
    return;
  }
  
  switch (command) {
    case 'create':
      handleCreate(args.slice(1));
      break;
    case 'delete':
      handleDelete(args.slice(1));
      break;
    case 'list':
      handleList();
      break;
    case 'checkin':
      handleCheckin(args.slice(1));
      break;
    case 'status':
      handleStatus();
      break;
    case 'history':
      handleHistory(args.slice(1));
      break;
    case 'achievements':
      handleAchievements();
      break;
    case 'whoami':
      handleWhoami();
      break;
    case 'guide':
      handleGuide();
      break;
    case 'boss':
      handleBoss();
      break;
    case 'diary':
      handleDiary();
      break;
    case 'test':
      runTest();
      break;
    default:
      // 尝试自然语言匹配
      handleNaturalLanguage(args.join(' '));
  }
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
🎮 游戏化习惯养成 CLI

用法：habits <命令> [参数]

命令:
  create <名称> [类型] [--desc "描述"] [--success "成功描述"]
                        创建新习惯
  delete <名称>          删除习惯
  list                   查看习惯列表
  checkin <名称>         打卡
  status                 查看属性面板
  history [天数]         查看打卡历史
  achievements           查看成就列表
  whoami                 显示当前用户信息
  boss                   检查 Boss 战（完成所有习惯后触发）
  diary [read]           生成/查看今日日记

示例:
  habits create 早起 physical --desc "击败赖床恶魔"
  habits checkin 早起
  habits status
  habits boss            # 检查是否击败 Boss
  habits diary           # 生成今日冒险日志
  habits diary read      # 查看今日日记

自然语言:
  habits 我起床了          → 自动匹配"早起"习惯打卡
  habits 看看我的属性      → 显示属性面板

多用户:
  自动识别：根据 OpenClaw 渠道和账号自动管理用户数据
  手动指定：habits status --user=wanwan
  环境变量：export GAMIFIED_HABITS_USER=wanwan
`);
}

/**
 * 处理创建习惯
 */
function handleCreate(args) {
  const name = args[0];
  const type = args[1] || 'physical';
  
  if (!name) {
    console.log('❌ 请提供习惯名称');
    console.log('用法：habits create <名称> [类型] [--desc "描述"] [--success "成功描述"]');
    return;
  }
  
  // 解析可选参数
  let customDesc = null;
  let customSuccess = null;
  
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--desc' && args[i + 1]) {
      customDesc = args[i + 1];
      i++;
    } else if (args[i] === '--success' && args[i + 1]) {
      customSuccess = args[i + 1];
      i++;
    }
  }
  
  const result = habits.createHabit(name, type, 'daily', null, customDesc, customSuccess);
  console.log(result.message);
}

/**
 * 处理删除习惯
 */
function handleDelete(args) {
  const name = args[0];
  
  if (!name) {
    console.log('❌ 请提供习惯名称');
    return;
  }
  
  const result = habits.deleteHabit(name);
  console.log(result.message);
}

/**
 * 处理查看列表
 */
function handleList() {
  const result = habits.listHabits();
  console.log(result.message);
}

/**
 * 处理打卡
 */
function handleCheckin(args) {
  const name = args[0];
  
  if (!name) {
    console.log('❌ 请提供习惯名称');
    return;
  }
  
  const result = xpSystem.checkinHabit(name);
  console.log(result.message);
}

/**
 * 处理查看状态
 */
function handleStatus() {
  const result = xpSystem.getStatus();
  console.log(result.message);
}

/**
 * 处理查看历史
 */
function handleHistory(args) {
  const days = parseInt(args[0]) || 7;
  const result = xpSystem.getHistory(days);
  console.log(result.message);
}

/**
 * 处理查看成就
 */
function handleAchievements() {
  const result = xpSystem.getAchievements();
  console.log(result.message);
}

/**
 * 处理自然语言输入
 */
function handleNaturalLanguage(input) {
  const text = input.toLowerCase();
  
  // 打卡相关
  if (text.includes('起床') || text.includes('早起')) {
    const habit = habits.findHabitByKeyword('早起');
    if (habit) {
      const result = xpSystem.checkinHabit(habit.name);
      console.log(result.message);
      return;
    }
  }
  
  if (text.includes('跑步') || text.includes('跑')) {
    const habit = habits.findHabitByKeyword('跑步');
    if (habit) {
      const result = xpSystem.checkinHabit(habit.name);
      console.log(result.message);
      return;
    }
  }
  
  if (text.includes('读书') || text.includes('阅读') || text.includes('看书')) {
    const habit = habits.findHabitByKeyword('阅读');
    if (habit) {
      const result = xpSystem.checkinHabit(habit.name);
      console.log(result.message);
      return;
    }
  }
  
  // 查看属性
  if (text.includes('属性') || text.includes('状态') || text.includes('面板')) {
    handleStatus();
    return;
  }
  
  // 查看列表
  if (text.includes('列表') || text.includes('习惯')) {
    handleList();
    return;
  }
  
  // 查看成就
  if (text.includes('成就')) {
    handleAchievements();
    return;
  }
  
  // 查看历史
  if (text.includes('历史') || text.includes('记录')) {
    handleHistory();
    return;
  }
  
  console.log('❓ 未识别的命令，试试以下命令:');
  showHelp();
}

/**
 * 显示当前用户信息
 */
function handleWhoami() {
  const userInfo = storage.getUserIdDisplay();
  console.log(`👤 当前用户信息:`);
  console.log(`   渠道：${userInfo.channel}`);
  console.log(`   账号：${userInfo.accountId}`);
  console.log(`   用户 ID: ${userInfo.full}`);
  console.log(`   数据文件：${storage.DATA_PATH}`);
}

/**
 * 显示新手引导
 */
function handleGuide() {
  console.log(welcome.showWelcomeGuide());
}

/**
 * 检查 Boss 战
 */
function handleBoss() {
  const result = xpSystem.checkBossBattle();
  console.log(result.message);
}

/**
 * 查看/生成日记
 */
function handleDiary() {
  const args = process.argv.slice(2);
  const action = args[1];
  
  if (action === 'read' || action === 'view') {
    // 查看今日日记
    const result = xpSystem.readTodayDiary();
    if (result.success) {
      console.log(result.content);
    } else {
      console.log('📖 今日日记还未生成，先完成打卡吧！');
    }
  } else {
    // 生成今日日记
    const result = xpSystem.generateTodayDiary();
    if (result.success) {
      console.log(`📖 今日日记已生成！`);
      console.log(`完成率：${result.completionRate}%`);
      console.log(`\n${result.diary}`);
    } else {
      console.log('日记生成失败');
    }
  }
}

/**
 * 运行测试
 */
function runTest() {
  console.log('🧪 运行测试...\n');
  
  // 测试 1: 创建习惯
  console.log('=== 测试 1: 创建习惯 ===');
  const createResult = habits.createHabit('早起', 'physical', 'daily', 50);
  console.log(createResult.message);
  console.log();
  
  // 测试 2: 查看列表
  console.log('=== 测试 2: 查看习惯列表 ===');
  const listResult = habits.listHabits();
  console.log(listResult.message);
  console.log();
  
  // 测试 3: 打卡
  console.log('=== 测试 3: 打卡 ===');
  const checkinResult = xpSystem.checkinHabit('早起');
  console.log(checkinResult.message);
  console.log();
  
  // 测试 4: 查看状态
  console.log('=== 测试 4: 查看属性面板 ===');
  const statusResult = xpSystem.getStatus();
  console.log(statusResult.message);
  console.log();
  
  // 测试 5: 查看成就
  console.log('=== 测试 5: 查看成就 ===');
  const achievementsResult = xpSystem.getAchievements();
  console.log(achievementsResult.message);
  console.log();
  
  console.log('✅ 测试完成！');
  console.log(`📦 数据存储在：${storage.DATA_PATH}`);
}

// 运行主函数
main();

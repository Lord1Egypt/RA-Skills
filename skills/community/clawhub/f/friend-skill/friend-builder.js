/**
 * Friend Chat Demo - 朋友聊天测试器
 * 
 * 用法: node scripts/chat-demo.js <朋友名>
 * 示例: node scripts/chat-demo.js 张三
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { FriendPersona } = require('./friend-builder');

function loadFriend(name) {
  const friendsDir = path.join(__dirname, '..', 'friends');
  const files = fs.readdirSync(friendsDir).filter(f => f.endsWith('.json'));
  
  // 直接匹配或模糊匹配
  let match = files.find(f => f.toLowerCase().startsWith(name.toLowerCase()));
  if (!match) {
    // 列出所有可用朋友
    console.log('\n📋 已创建的朋友分身:');
    files.forEach(f => console.log(`   ${f.replace('-friend.json', '')}`));
    return null;
  }

  try {
    const persona = FriendPersona.load(path.join(friendsDir, match));
    console.log(`\n✅ 已加载: ${persona.friend.name}`);
    return persona;
  } catch (e) {
    console.error('❌ 加载失败:', e.message);
    return null;
  }
}

function startChat(persona) {
  console.log('\n' + '='.repeat(50));
  console.log(`💬 正在和 ${persona.friend.name} 聊天中...`);
  console.log(`📝 你们的关系: ${persona.friend.relationship.role}`);
  console.log(`🎭 性格: ${persona.friend.personality.traits.join(', ') || '待补充'}`);
  console.log(`💡 输入 "exit" 退出 | "mem" 查看回忆 | "info" 查看人格信息`);
  console.log('='.repeat(50) + '\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const chatHistory = [];

  function prompt() {
    rl.question(`🧑 ${persona.friend.relationship.yourName || '你'} > `, async (input) => {
      if (input.toLowerCase() === 'exit') {
        console.log(`\n👋 ${persona.friend.name}: 拜拜～下次再聊！`);
        rl.close();
        return;
      }

      if (input.toLowerCase() === 'mem') {
        if (persona.friend.relationship.sharedMemories.length === 0) {
          console.log(`📭 目前还没有任何共同回忆记录。`);
        } else {
          console.log(`\n📖 共同回忆 (${persona.friend.relationship.sharedMemories.length} 条):`);
          persona.friend.relationship.sharedMemories.forEach((m, i) => {
            console.log(`  ${i + 1}. ${m.event}`);
            console.log(`     ${m.detail}`);
            console.log(`     🏷️ ${m.emotionalTag}`);
          });
        }
        console.log();
        prompt();
        return;
      }

      if (input.toLowerCase() === 'info') {
        console.log(`\n👤 ${persona.friend.name} 的人格信息:`);
        console.log(JSON.stringify(persona.friend, null, 2));
        console.log();
        prompt();
        return;
      }

      chatHistory.push({ role: 'user', content: input });
      
      const reply = persona.generateReply(input, { history: chatHistory });
      console.log(`\n👤 ${persona.friend.name}: ${reply}\n`);
      chatHistory.push({ role: 'friend', content: reply });

      prompt();
    });
  }

  // 开场白
  const greeting = persona.friend.voice.greeting || `（抬头看你）来了啊～`;
  console.log(`👤 ${persona.friend.name}: ${greeting}\n`);
  prompt();
}

// ============== 主入口 ==============

const name = process.argv[2];
if (!name) {
  console.log('用法: node scripts/chat-demo.js <朋友名>');
  console.log('示例: node scripts/chat-demo.js 张三');
  process.exit(1);
}

const persona = loadFriend(name);
if (persona) {
  startChat(persona);
}

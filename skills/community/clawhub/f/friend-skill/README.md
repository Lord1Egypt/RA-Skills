/**
 * Friend Builder - 朋友数字分身构建器
 * 
 * 使用说明：
 * 1. 确保 Node.js 已安装 (v18+)
 * 2. 运行：node scripts/friend-builder.js
 * 3. 按提示输入朋友信息
 * 4. 生成后可用 scripts/chat-demo.js 测试聊天
 * 
 * 隐私说明：
 * - 所有数据在本地处理
 * - 聊天记录不会被上传
 * - 生成的分身文件可随时删除
 */

const fs = require('fs');
const path = require('path');

// ============== 核心数据结构 ==============

class FriendPersona {
  constructor(name) {
    this.friend = {
      name: name || '未命名朋友',
      nickname: '',
      personality: {
        traits: [],
        mbti: 'ENFP',
        energy: '中能量'
      },
      voice: {
        greeting: '',
        farewell: '',
        laugh: '',
        moodAngry: '',
        moodSad: ''
      },
      relationship: {
        yourName: '',
        role: '朋友',
        yearsKnown: 0,
        sharedMemories: []
      },
      interests: {
        love: [],
        hate: []
      },
      insideJokes: []
    };
    this.createdAt = new Date().toISOString();
    this.version = '1.0.0';
  }

  // 从聊天记录中分析人格
  analyzeChatRecords(records) {
    if (!records || records.length < 3) {
      console.log('⚠️ 聊天记录太少，使用基础模板生成');
      return this._applyBaseTemplate();
    }

    console.log(`🔍 正在分析 ${records.length} 条聊天记录...`);

    // 语气词分析
    const toneWords = this._extractToneWords(records);
    if (toneWords.length > 0) {
      this.friend.voice.greeting = toneWords[0];
    }

    // 句子长度偏好
    const avgLength = records.reduce((sum, r) => sum + r.length, 0) / records.length;
    this.friend.personality.energy = avgLength > 20 ? '高能量(话多)' : avgLength > 10 ? '中能量' : '低能量(话少)';

    // 高频词提取
    const freqWords = this._extractFrequencyWords(records);
    if (freqWords.length > 0) {
      this.friend.insideJokes = freqWords.slice(0, 3).map(w => 
        `「${w.word}」出现了 ${w.count} 次，可能是典型用词`
      );
    }

    return this;
  }

  // 提取语气词
  _extractToneWords(records) {
    const tonePatterns = [
      /(哈哈+|呵呵+|hhh+|hahaha)/gi,
      /(卧槽|我去|我靠|天哪)/g,
      /(真的假的|不会吧|不是吧)/g,
      /(好吧|行吧|算了)/g,
      /(我觉得|我感觉|我认为)/g,
      /(你懂吗|你知道吧|你明白吗)/g,
      /(笑死|牛逼|绝了)/g,
      /(无语|麻了|蚌埠住了)/g
    ];

    const matches = [];
    records.forEach(record => {
      tonePatterns.forEach((pattern, idx) => {
        if (pattern.test(record)) {
          const match = record.match(pattern);
          if (match && !matches.find(m => m[0] === match[0])) {
            matches.push(match);
          }
        }
      });
    });

    return matches.map(m => m[0]).slice(0, 5);
  }

  // 提取高频词
  _extractFrequencyWords(records) {
    const wordCount = {};
    const stopWords = ['的', '了', '是', '在', '有', '我', '你', '他', '她', '它', 
                       '这', '那', '和', '就', '也', '都', '要', '会', '能', '可以',
                       '吗', '啊', '呢', '吧', '嗯', '哦', '哈', '呀'];

    records.forEach(record => {
      // 简单分词（中文按字符，英文按空格）
      const chars = record.split('');
      let currentWord = '';
      
      chars.forEach(char => {
        if (/[\u4e00-\u9fff]/.test(char)) {
          currentWord += char;
          if (currentWord.length >= 2 && !stopWords.includes(currentWord)) {
            wordCount[currentWord] = (wordCount[currentWord] || 0) + 1;
          }
        } else {
          currentWord = '';
        }
      });
    });

    return Object.entries(wordCount)
      .map(([word, count]) => ({ word, count }))
      .filter(w => w.count >= 2)
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
  }

  // 基础模板
  _applyBaseTemplate() {
    this.friend.voice = {
      greeting: '哟，来了啊',
      farewell: '行，我先撤了',
      laugh: '哈哈哈笑死',
      moodAngry: '我服了',
      moodSad: '唉...'
    };
    this.friend.personality.traits = ['待补充'];
    return this;
  }

  // 对话系统
  generateReply(userMessage, context = {}) {
    const message = userMessage.toLowerCase();
    
    // 根据消息类型选择响应策略
    if (this._isGreeting(message)) {
      return this._greet(context);
    }
    if (this._isComplaint(message)) {
      return this._respondToComplaint(message, context);
    }
    if (this._isMemoryQuery(message)) {
      return this._recallMemory(context);
    }
    if (this._isSeriousMessage(message)) {
      return this._seriousReply(context);
    }
    return this._casualReply(userMessage, context);
  }

  _isGreeting(msg) {
    const patterns = [/^(嗨|hi|hello|hey|在吗|在|喂|yo)/i, /(来了|好久不见|想你)/];
    return patterns.some(p => p.test(msg));
  }

  _isComplaint(msg) {
    const patterns = [/烦|累|郁闷|难过|伤心|生气|无语|麻了|蚌埠住了|好难|倒霉/];
    return patterns.some(p => p.test(msg));
  }

  _isMemoryQuery(msg) {
    const patterns = [/记得|还记得|之前|上次|以前|那年|那时候/];
    return patterns.some(p => p.test(msg));
  }

  _isSeriousMessage(msg) {
    const patterns = [/想跟你说|有个事|严肃|认真|重要|怎么办|帮帮我|求助/];
    return patterns.some(p => p.test(msg));
  }

  _greet(context) {
    const greetings = [
      `（抬起头）哟，${this.friend.relationship.yourName || '你'}来了啊！`,
      `（眼睛一亮）嘿！正想找你呢！`,
      `（懒洋洋地）咋，想我了？`,
      `（放下手机）来啦来啦，今天有啥事？`,
    ];
    return this._pickRandom(greetings);
  }

  _respondToComplaint(message, context) {
    const roleReplies = {
      '损友': [
        `（嫌弃脸）我就说吧...不过算了，请你喝奶茶消消气？`,
        `哈哈哈你也有今天！（收起笑）咳，说真的，要我帮忙不？`,
        `（拍拍肩）多大点事，走，打把游戏就好了。`,
      ],
      '温柔型': [
        `（轻轻抱抱）没事啦，有我在呢。`,
        `辛苦了...要不要我给你点个外卖？`,
        `（认真听完）我懂你，先休息一下，等会再说。`,
      ],
      '搞笑型': [
        `（夸张表情）啥？！谁惹你了，我去揍TA！（然后默默坐下）开玩笑的，我打不过。`,
        `笑一个嘛～你看我都这么努力逗你了！（做鬼脸）`,
      ]
    };

    const replies = roleReplies[this.friend.relationship.role] || [
      `哎，别难过，我在呢。`,
      `（认真脸）说说看，我听着。`,
    ];

    return this._pickRandom(replies);
  }

  _recallMemory(context) {
    if (this.friend.relationship.sharedMemories.length === 0) {
      return `（努力回忆）emmm...我觉得我们应该有很多回忆，但我还没学会记住它们。你告诉我呗？`;
    }

    const memory = this._pickRandom(this.friend.relationship.sharedMemories);
    return `（眼睛一亮）当然记得！${memory.event}那次，${memory.detail}。我怎么可能忘嘛～`;
  }

  _seriousReply(context) {
    return `（认真起来，收起笑容）嗯，你说吧，我好好听着。不管什么事，有我在呢。`;
  }

  _casualReply(message, context) {
    const casuals = [
      `（歪头想了想）嗯...${message}？有意思。`,
      `（打了个哈哈）你说的这个嘛，我觉得...算了，我先想想。`,
      `（托腮）继续继续，我在听呢。`,
    ];
    return this._pickRandom(casuals);
  }

  _pickRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // 导出为JSON
  toJSON() {
    return JSON.stringify({
      meta: {
        version: this.version,
        createdAt: this.createdAt
      },
      persona: this.friend
    }, null, 2);
  }

  // 从JSON导入
  static fromJSON(jsonStr) {
    const data = JSON.parse(jsonStr);
    const persona = new FriendPersona(data.persona.name);
    persona.friend = data.persona;
    if (data.meta) {
      persona.version = data.meta.version || '1.0.0';
      persona.createdAt = data.meta.createdAt || new Date().toISOString();
    }
    return persona;
  }

  // 保存到文件
  save(filePath) {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, this.toJSON(), 'utf-8');
    console.log(`✅ 朋友分身已保存到: ${filePath}`);
    return this;
  }

  // 从文件加载
  static load(filePath) {
    if (!fs.existsSync(filePath)) {
      throw new Error(`❌ 文件不存在: ${filePath}`);
    }
    const data = fs.readFileSync(filePath, 'utf-8');
    return FriendPersona.fromJSON(data);
  }
}

// ============== CLI 交互模式 ==============

function startInteractiveMode() {
  console.log('');
  console.log('🤝 ===== 朋友数字分身构建器 =====');
  console.log('');
  console.log('告诉我你想造的朋友的信息，我来帮你生成！');
  console.log('');

  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let persona;

  function askQuestion(q) {
    return new Promise(resolve => readline.question(q, resolve));
  }

  (async () => {
    try {
      // Step 1: 基础信息
      const name = await askQuestion('朋友的名字/昵称: ');
      if (!name) {
        console.log('❌ 名字不能为空');
        readline.close();
        return;
      }

      persona = new FriendPersona(name.trim());
      
      const nickname = await askQuestion(`平时你怎么叫${name}？(可选): `);
      if (nickname) persona.friend.nickname = nickname.trim();
      
      const yourName = await askQuestion(`${name}叫你什么？(可选): `);
      if (yourName) persona.friend.relationship.yourName = yourName.trim();

      const traits = await askQuestion(`性格关键词(逗号分隔，比如: 毒舌,仗义,搞笑): `);
      if (traits) {
        persona.friend.personality.traits = traits.split(/[,，]/).map(t => t.trim()).filter(Boolean);
      }

      const role = await askQuestion(`你们的相处模式？(损友/温柔型/搞笑型/人生导师/其他): `);
      if (role) persona.friend.relationship.role = role.trim();

      const years = await askQuestion('认识多久了？(年): ');
      if (years) persona.friend.relationship.yearsKnown = parseInt(years) || 0;

      // Step 2: 兴趣
      const loves = await askQuestion(`${name}喜欢什么？(逗号分隔): `);
      if (loves) {
        persona.friend.interests.love = loves.split(/[,，]/).map(i => i.trim()).filter(Boolean);
      }

      const hates = await askQuestion(`${name}讨厌什么？(逗号分隔): `);
      if (hates) {
        persona.friend.interests.hate = hates.split(/[,，]/).map(i => i.trim()).filter(Boolean);
      }

      // Step 3: 共同回忆
      console.log('');
      console.log('📝 下面说说你们的共同回忆（输入"完成"结束）:');
      while (true) {
        const event = await askQuestion('  回忆事件: ');
        if (event.toLowerCase() === '完成' || !event) break;
        
        const detail = await askQuestion('  细节描述: ');
        const tag = await askQuestion('  情绪标签(快乐/感动/搞笑/尴尬等): ');
        
        persona.friend.relationship.sharedMemories.push({
          event: event.trim(),
          detail: detail || '',
          emotionalTag: tag || '快乐'
        });
        console.log('  ✅ 已记录！继续输入下一个，或输入"完成"');
      }

      // Step 4: 聊天记录批量导入
      const importChat = await askQuestion('\n📁 是否导入聊天记录文件？(y/n): ');
      if (importChat.toLowerCase() === 'y') {
        const filePath = await askQuestion('  文件路径: ');
        try {
          const content = fs.readFileSync(filePath.trim(), 'utf-8');
          const records = content.split('\n').filter(l => l.trim());
          persona.analyzeChatRecords(records);
        } catch (e) {
          console.log(`  ⚠️ 导入失败: ${e.message}`);
        }
      }

      readline.close();

      // Step 5: 生成输出
      console.log('\n🎉 ==== 分身构建完成！====\n');
      
      const outputDir = path.join(__dirname, '..', 'friends');
      const outputFile = path.join(outputDir, `${name}-friend.json`);
      persona.save(outputFile);

      console.log('👤 人格概要:');
      console.log(`  - 姓名: ${persona.friend.name}`);
      console.log(`  - 昵称: ${persona.friend.nickname || '(无)'}`);
      console.log(`  - 性格: ${persona.friend.personality.traits.join(', ') || '待补充'}`);
      console.log(`  - 模式: ${persona.friend.relationship.role}`);
      console.log(`  - 共同回忆: ${persona.friend.relationship.sharedMemories.length} 条`);
      console.log('');
      console.log('💡 现在你可以：');
      console.log(`  1. 运行 scripts/chat-demo.js 测试聊天`);
      console.log(`  2. 编辑朋友分身JSON文件手动微调`);
      console.log(`  3. 再次运行本工具追加更多数据`);
      console.log('');

    } catch (e) {
      console.error('❌ 发生错误:', e.message);
      readline.close();
    }
  })();
}

// ============== 命令行参数解析 ==============

if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🤝 朋友数字分身构建器 v1.0.0

用法:
  node friend-builder.js                     # 交互模式
  node friend-builder.js --help              # 显示帮助
  node friend-builder.js --build <data.json> # 从JSON文件构建

隐私说明:
  - 所有数据在本地处理
  - 你的聊天记录不会离开这台电脑
  - 可以随时删除生成的朋友分身文件
`);
  } else if (args[0] === '--build' && args[1]) {
    try {
      const data = JSON.parse(fs.readFileSync(args[1], 'utf-8'));
      const persona = new FriendPersona(data.name || '朋友');
      
      if (data.records) {
        persona.analyzeChatRecords(data.records);
      }
      if (data.personality) {
        Object.assign(persona.friend.personality, data.personality);
      }
      if (data.relationship) {
        Object.assign(persona.friend.relationship, data.relationship);
      }
      if (data.interests) {
        Object.assign(persona.friend.interests, data.interests);
      }
      if (data.voice) {
        Object.assign(persona.friend.voice, data.voice);
      }

      const outputFile = path.join(__dirname, '..', 'friends', `${data.name || 'friend'}-friend.json`);
      persona.save(outputFile);
    } catch (e) {
      console.error('❌ 构建失败:', e.message);
    }
  } else {
    startInteractiveMode();
  }
}

module.exports = { FriendPersona };

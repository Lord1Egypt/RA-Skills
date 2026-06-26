#!/usr/bin/env node
/**
 * generate_group_def.js - 交互式生成 group_def.json
 * 
 * 用法：直接运行，按提示输入；或修改下方 CONFIG 直接生成
 * 
 *   node generate_group_def.js --output group_def.json
 */

// ===== 修改这里来快速配置 =====
const CONFIG = {
  groupId: "123456789",
  groupName: "AI资讯交流群",
  botNickname: "元宝",

  // 成员列表（role: "user" 或 "assistant"）
  members: [
    {
      id: "user_001", role: "user", nickname: "陈默",
      persona: "32岁产品经理，逻辑清晰，善于总结，常用「这个很有意思」开场",
      joinDate: [2025, 6, 1, 9, 0, 0],
    },
    {
      id: "user_002", role: "user", nickname: "张磊",
      persona: "29岁NLP算法工程师，严谨爱纠错，常说「这个说法不严谨」",
      joinDate: [2025, 6, 1, 9, 5, 0],
    },
    {
      id: "user_003", role: "user", nickname: "林晓",
      persona: "27岁UI设计师，热情活跃，AI绘图发烧友，爱分享截图",
      joinDate: [2025, 6, 2, 10, 0, 0],
    },
    {
      id: "user_004", role: "user", nickname: "王斌",
      persona: "36岁VC投资人，务实，看战略不看技术细节",
      joinDate: [2025, 6, 3, 14, 0, 0],
    },
    {
      id: "user_005", role: "user", nickname: "孙阳",
      persona: "22岁AI方向研究生，好奇爱学，常问基础问题",
      joinDate: [2025, 6, 5, 20, 0, 0],
    },
    {
      id: "user_006", role: "user", nickname: "刘青",
      persona: "34岁科技媒体记者，信息面广，常说「刚获悉」",
      joinDate: [2025, 6, 8, 11, 0, 0],
    },
    {
      id: "user_007", role: "user", nickname: "胡建",
      persona: "38岁AI创业公司CEO，讲实战踩坑，爱说「有没有人实际用过」",
      joinDate: [2025, 7, 1, 9, 0, 0],
    },
    {
      id: "user_008", role: "user", nickname: "周宇老师",
      persona: "52岁计算机学院教授，学术腔，引研究数据，爱泼冷水但理性",
      joinDate: [2025, 7, 15, 15, 0, 0],
    },
    {
      id: "user_009", role: "user", nickname: "毛毛",
      persona: "25岁内容平台运营，超口语，常说「救了救了」「yyds」「求推荐」",
      joinDate: [2025, 8, 1, 20, 0, 0],
    },
    {
      id: "user_010", role: "user", nickname: "程凡",
      persona: "31岁ToB产品经理，职场感，爱做总结，常说「从用户侧来看」",
      joinDate: [2025, 8, 10, 9, 0, 0],
    },
    {
      id: "bot_001", role: "assistant", nickname: "元宝",
      persona: "群内AI助手，回答群友问题，提供信息检索、数据查询和内容总结服务",
      joinDate: [2025, 6, 1, 0, 0, 0],
    },
  ],

  // 话题时间基准（UTC）：[year, month, day, hour, minute]
  topicTimes: {
    1: [2026, 3, 9, 9, 0],
    2: [2026, 3, 9, 12, 0],
    3: [2026, 3, 9, 15, 0],
  },
};
// ===== 配置结束 =====

const fs = require('fs');
const path = require('path');

function toExcelSerial(year, month, day, hour = 0, minute = 0, second = 0) {
  const epoch = new Date(Date.UTC(1899, 11, 30));
  const d = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  return (d - epoch) / 86400000;
}

const output = {
  groupId: CONFIG.groupId,
  groupName: CONFIG.groupName,
  botNickname: CONFIG.botNickname,
  members: CONFIG.members.map(m => ({
    id: m.id,
    role: m.role,
    nickname: m.nickname,
    persona: m.persona,
    join_time: toExcelSerial(...m.joinDate),
  })),
  topicBaseTimes: Object.fromEntries(
    Object.entries(CONFIG.topicTimes).map(([k, v]) => [k, toExcelSerial(...v)])
  ),
};

const outPath = process.argv[process.argv.indexOf('--output') + 1] || 'group_def.json';
fs.writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`✅ group_def.json 生成完成: ${outPath}`);
console.log(`   群名: ${output.groupName}`);
console.log(`   成员数: ${output.members.length}`);

#!/usr/bin/env node
/**
 * 用户映射表统一 API
 * 
 * 所有 Agent 都通过这个 API 访问映射表，避免路径问题和并发冲突
 * 
 * 使用方法:
 *   const mapping = require('./mapping-api.js');
 *   
 *   // 通过 openid 反查 userid
 *   const user = await mapping.getUserByOpenId('coordinator', 'ou_xxx');
 *   
 *   // 获取用户的某个 Agent openid
 *   const openId = await mapping.getAgentOpenId('zhangsan', 'product-expert');
 *   
 *   // 更新映射
 *   await mapping.updateAgentChannel('zhangsan', 'product-expert', 'ou_xxx', '张三');
 */

const fs = require('fs');
const path = require('path');

// 统一使用主 workspace 的映射表
const MAPPING_FILE = path.resolve(__dirname, 'user-mapping.json');
const MAX_RETRIES = 3;

// 读取映射表 (带重试)
async function readMapping() {
  for (let i = 0; i < MAX_RETRIES; i++) {
    try {
      const content = await fs.promises.readFile(MAPPING_FILE, 'utf-8');
      return JSON.parse(content);
    } catch (err) {
      if (i === MAX_RETRIES - 1) throw err;
      await new Promise(r => setTimeout(r, 100 * (i + 1)));
    }
  }
}

// 写入映射表 (带重试)
async function writeMapping(data) {
  for (let i = 0; i < MAX_RETRIES; i++) {
    try {
      await fs.promises.writeFile(MAPPING_FILE, JSON.stringify(data, null, 2), 'utf-8');
      return;
    } catch (err) {
      if (i === MAX_RETRIES - 1) throw err;
      await new Promise(r => setTimeout(r, 100 * (i + 1)));
    }
  }
}

// 通过 openid 反查 userid (注意：open_id 是每个 Bot 独立的)
async function getUserByOpenId(agentId, openId) {
  const mapping = await readMapping();
  for (const [userid, user] of Object.entries(mapping.users || {})) {
    if (user.botOpenIds?.[agentId] === openId) {
      return {
        userid,
        name: user.name || userid,
        botOpenIds: user.botOpenIds,
        firstSeen: user.firstSeen,
        lastActive: user.lastActive
      };
    }
  }
  return null;
}

// 获取用户在某个 Bot 的 open_id
async function getBotOpenId(userid, agentId) {
  const mapping = await readMapping();
  const user = mapping.users?.[userid];
  if (!user) return null;
  return user.botOpenIds?.[agentId] || null;
}

// 更新/添加 Bot open_id (每个 Bot 调用时记录自己在该 Bot 下的 open_id)
async function updateBotOpenId(userid, agentId, openId, name = null) {
  const mapping = await readMapping();
  mapping.users = mapping.users || {};
  
  if (!mapping.users[userid]) {
    mapping.users[userid] = {
      botOpenIds: {},
      name: name || userid,
      firstSeen: new Date().toISOString(),
      lastActive: new Date().toISOString()
    };
  }
  
  mapping.users[userid].botOpenIds[agentId] = openId;
  mapping.users[userid].lastActive = new Date().toISOString();
  if (name) mapping.users[userid].name = name;
  mapping.updatedAt = new Date().toISOString();
  
  await writeMapping(mapping);
  return true;
}

// 列出所有用户
async function listUsers() {
  const mapping = await readMapping();
  return mapping.users || {};
}

// 检查用户是否存在
async function userExists(userid) {
  const mapping = await readMapping();
  return !!mapping.users?.[userid];
}

module.exports = {
  getUserByOpenId,
  getBotOpenId,
  updateBotOpenId,
  listUsers,
  userExists,
  MAPPING_FILE,

  getAgentOpenId: getBotOpenId,
  updateAgentChannel: updateBotOpenId
};

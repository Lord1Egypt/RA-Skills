/**
 * 飞书群管理模块
 * 功能：群信息维护、记录新群、更新群状态、发送群消息
 * 
 * 使用方式：
 * const { addGroup, removeGroup, getActiveGroups, findGroupByName, isInGroup, listAllGroups, syncGroupsFromFeishu, setGroupsFilePath } = require('./groupManager.js');
 * 
 * // 设置自定义路径（可选）
 * setGroupsFilePath('/custom/path/feishu-groups.json');
 */

const fs = require('fs');
const path = require('path');

let GROUPS_FILE = path.join(process.cwd(), 'feishu-groups.json');

/**
 * 设置群信息文件路径
 * @param {string} customPath - 自定义路径
 */
function setGroupsFilePath(customPath) {
  if (customPath) {
    GROUPS_FILE = customPath;
  }
}

/**
 * 获取当前群信息文件路径
 * @returns {string}
 */
function getGroupsFilePath() {
  return GROUPS_FILE;
}

/**
 * 初始化群信息文件
 * @param {string} customPath - 可选的自定义路径
 */
function initGroupsFile(customPath) {
  const filePath = customPath || GROUPS_FILE;
  if (!fs.existsSync(filePath)) {
    // 确保目录存在
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    const initialData = { groups: {}, updated_at: new Date().toISOString() };
    fs.writeFileSync(filePath, JSON.stringify(initialData, null, 2));
    console.log(`[群管理] 初始化群信息文件: ${filePath}`);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

/**
 * 读取群信息
 * @param {string} customPath - 可选的自定义路径
 */
function getGroups(customPath) {
  const filePath = customPath || GROUPS_FILE;
  initGroupsFile(filePath);
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

/**
 * 保存群信息
 * @param {object} data - 群信息数据
 * @param {string} customPath - 可选的自定义路径
 */
function saveGroups(data, customPath) {
  const filePath = customPath || GROUPS_FILE;
  data.updated_at = new Date().toISOString();
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

/**
 * 添加或更新群信息
 * @param {string} chatId - 群 ID
 * @param {string} name - 群名称
 * @param {number} memberCount - 成员数
 * @param {string} customPath - 可选的自定义路径
 * @returns {object} 操作结果
 */
function addGroup(chatId, name, memberCount = 0, customPath) {
  const data = getGroups(customPath);
  const now = new Date().toISOString();
  
  if (data.groups[chatId]) {
    // 群已存在，可能是重新加入
    data.groups[chatId] = {
      ...data.groups[chatId],
      name,
      member_count: memberCount,
      removed_at: null,
      status: 'active',
      rejoin_at: now
    };
  } else {
    // 新群
    data.groups[chatId] = {
      chat_id: chatId,
      name,
      member_count: memberCount,
      added_at: now,
      removed_at: null,
      status: 'active'
    };
  }
  
  saveGroups(data, customPath);
  return { success: true, group: data.groups[chatId] };
}

/**
 * 移除群（标记为已移除）
 * @param {string} chatId - 群 ID
 * @param {string} customPath - 可选的自定义路径
 * @returns {object} 操作结果
 */
function removeGroup(chatId, customPath) {
  const data = getGroups(customPath);
  
  if (!data.groups[chatId]) {
    return { success: false, error: '群不存在' };
  }
  
  data.groups[chatId].removed_at = new Date().toISOString();
  data.groups[chatId].status = 'removed';
  
  saveGroups(data, customPath);
  return { success: true, group: data.groups[chatId] };
}

/**
 * 获取所有活跃群
 * @param {string} customPath - 可选的自定义路径
 * @returns {array} 活跃群列表
 */
function getActiveGroups(customPath) {
  const data = getGroups(customPath);
  return Object.values(data.groups)
    .filter(g => g.status === 'active')
    .map(g => ({ chat_id: g.chat_id, name: g.name }));
}

/**
 * 根据群名查找群
 * @param {string} name - 群名称（模糊匹配）
 * @param {string} customPath - 可选的自定义路径
 * @returns {object|null} 群信息
 */
function findGroupByName(name, customPath) {
  const data = getGroups(customPath);
  const lowerName = name.toLowerCase();
  
  // 先精确匹配
  let group = Object.values(data.groups).find(g => 
    g.status === 'active' && g.name === name
  );
  
  if (group) return group;
  
  // 再模糊匹配
  group = Object.values(data.groups).find(g => 
    g.status === 'active' && g.name.toLowerCase().includes(lowerName)
  );
  
  return group || null;
}

/**
 * 根据 chatId 获取群信息
 * @param {string} chatId - 群 ID
 * @param {string} customPath - 可选的自定义路径
 * @returns {object|null} 群信息
 */
function getGroupById(chatId, customPath) {
  const data = getGroups(customPath);
  return data.groups[chatId] || null;
}

/**
 * 检查 bot 是否在群里
 * @param {string} chatId - 群 ID
 * @param {string} customPath - 可选的自定义路径
 * @returns {boolean}
 */
function isInGroup(chatId, customPath) {
  const group = getGroupById(chatId, customPath);
  return group && group.status === 'active';
}

/**
 * 清理超过指定天数的已移除群
 * @param {number} days - 天数
 * @param {string} customPath - 可选的自定义路径
 * @returns {number} 清理数量
 */
function cleanupOldGroups(days = 30, customPath) {
  const data = getGroups(customPath);
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  const cutoffStr = cutoff.toISOString();
  
  let count = 0;
  for (const [chatId, group] of Object.entries(data.groups)) {
    if (group.status === 'removed' && group.removed_at && group.removed_at < cutoffStr) {
      delete data.groups[chatId];
      count++;
    }
  }
  
  if (count > 0) {
    saveGroups(data, customPath);
  }
  
  return count;
}

/**
 * 列出所有群（包含状态）
 * @param {string} customPath - 可选的自定义路径
 * @returns {object} 所有群信息
 */
function listAllGroups(customPath) {
  const data = getGroups(customPath);
  return {
    active: Object.values(data.groups).filter(g => g.status === 'active'),
    removed: Object.values(data.groups).filter(g => g.status === 'removed'),
    total: Object.keys(data.groups).length
  };
}

/**
 * 从飞书同步群信息（需要飞书 API 配合）
 * 注意：此函数需要外部调用 feishu_chat 获取群列表后传入
 * @param {array} feishuGroups - 从飞书 API 获取的群列表
 * @param {string} customPath - 可选的自定义路径
 */
function syncGroupsFromFeishu(feishuGroups, customPath) {
  const data = getGroups(customPath);
  const now = new Date().toISOString();
  
  // 记录当前文件中的群 ID
  const existingIds = new Set(Object.keys(data.groups));
  const feishuIds = new Set();
  
  // 更新或添加从飞书获取的群
  for (const g of feishuGroups) {
    const chatId = g.chat_id || g.chatId;
    feishuIds.add(chatId);
    
    if (data.groups[chatId]) {
      // 群已存在，更新信息
      data.groups[chatId].name = g.name || g.group_name || data.groups[chatId].name;
      data.groups[chatId].member_count = g.member_count || g.user_count || data.groups[chatId].member_count;
      if (data.groups[chatId].status === 'removed') {
        data.groups[chatId].status = 'active';
        data.groups[chatId].rejoin_at = now;
      }
    } else {
      // 新群
      data.groups[chatId] = {
        chat_id: chatId,
        name: g.name || g.group_name || '未知群',
        member_count: g.member_count || g.user_count || 0,
        added_at: now,
        removed_at: null,
        status: 'active',
        source: 'feishu_api'
      };
    }
  }
  
  // 标记不再在飞书中的群为 removed（可选）
  // for (const id of existingIds) {
  //   if (!feishuIds.has(id) && data.groups[id].status === 'active') {
  //     data.groups[id].status = 'removed';
  //     data.groups[id].removed_at = now;
  //   }
  // }
  
  saveGroups(data, customPath);
  return { synced: feishuGroups.length, groups: data.groups };
}

module.exports = {
  setGroupsFilePath,
  getGroupsFilePath,
  initGroupsFile,
  getGroups,
  saveGroups,
  addGroup,
  removeGroup,
  getActiveGroups,
  findGroupByName,
  getGroupById,
  isInGroup,
  cleanupOldGroups,
  listAllGroups,
  syncGroupsFromFeishu
};

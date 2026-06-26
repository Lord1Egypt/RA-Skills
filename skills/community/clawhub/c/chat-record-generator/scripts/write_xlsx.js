#!/usr/bin/env node
/**
 * write_xlsx.js - 生成完整的群聊记录 xlsx
 * 
 * 用法：
 *   node write_xlsx.js --group group_def.json --messages messages.json --output output.xlsx
 * 
 * messages.json 格式：
 *   [{"话题": 1, "发言人": "陈默", "内容": "消息文字"}, ...]
 *   图片消息：内容包含 [图片：...] 标记，自动识别为 image 类型
 */

const XLSX = require('/tmp/xlsxparse/node_modules/xlsx');
const fs = require('fs');
const path = require('path');

// ===== 命令行参数解析 =====
const args = process.argv.slice(2);
function getArg(name) {
  const i = args.indexOf('--' + name);
  return i >= 0 ? args[i + 1] : null;
}

const groupDefPath = getArg('group') || 'group_def.json';
const messagesPath = getArg('messages') || 'messages.json';
const outputPath = getArg('output') || 'output.xlsx';
const xlsxModule = getArg('xlsx') || '/tmp/xlsxparse/node_modules/xlsx';

// ===== 时间工具 =====
function toExcelSerial(year, month, day, hour = 0, minute = 0, second = 0) {
  const epoch = new Date(Date.UTC(1899, 11, 30));
  const d = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  return (d - epoch) / 86400000;
}

// ===== 读取数据 =====
const groupDef = JSON.parse(fs.readFileSync(groupDefPath, 'utf8'));
const rawMessages = JSON.parse(fs.readFileSync(messagesPath, 'utf8'));

// ===== 时间基准（默认当天 UTC 09:00 起，话题间隔3h） =====
const today = new Date();
const baseYear = today.getUTCFullYear();
const baseMonth = today.getUTCMonth() + 1;
const baseDay = today.getUTCDate();

const topicBaseTime = groupDef.topicBaseTimes || {
  1: toExcelSerial(baseYear, baseMonth, baseDay, 9, 0),
  2: toExcelSerial(baseYear, baseMonth, baseDay, 12, 0),
  3: toExcelSerial(baseYear, baseMonth, baseDay, 15, 0),
  4: toExcelSerial(baseYear, baseMonth, baseDay, 18, 0),
};
const MSG_INTERVAL = 0.002; // ~3分钟

// ===== 工作簿创建 =====
const wb = XLSX.utils.book_new();

// ----- Sheet 1: group_info -----
const groupInfoData = [
  ['派id', '群名', 'bot_config'],
  [groupDef.groupId, groupDef.groupName, null],
];
const ws1 = XLSX.utils.aoa_to_sheet(groupInfoData);
XLSX.utils.book_append_sheet(wb, ws1, 'group_info');

// ----- Sheet 2: active_members -----
const memberHeaders = ['id', 'role', 'nickname', 'persona', 'join_time'];
const memberRows = groupDef.members.map(m => [
  m.id, m.role, m.nickname, m.persona, m.join_time
]);
const ws2 = XLSX.utils.aoa_to_sheet([memberHeaders, ...memberRows]);

// 修复 join_time 的 numFmt（aoa_to_sheet 不保留格式）
groupDef.members.forEach((m, i) => {
  const r = i + 1; // row 0 = header
  const addr = XLSX.utils.encode_cell({ r, c: 4 });
  ws2[addr] = { t: 'n', v: m.join_time, z: 'yyyy/m/d h:mm:ss;@' };
});
XLSX.utils.book_append_sheet(wb, ws2, 'active_members');

// ----- Sheet 3: message_stream -----
const msgHeaders = ['轮次', '消息类型', '时间', '发言人', '内容', 'task_list', '附件'];
const ws3 = XLSX.utils.aoa_to_sheet([msgHeaders]);

// 统计每个话题的消息计数（用于时间偏移）
const topicIdx = {};
let imgCount = 0;
let fileCount = 0;

rawMessages.forEach((msg, i) => {
  const topic = msg.话题 || 1;
  if (!topicIdx[topic]) topicIdx[topic] = 0;

  const timeVal = topicBaseTime[topic] + topicIdx[topic] * MSG_INTERVAL;
  topicIdx[topic]++;

  // 判断消息类型
  const content = msg.内容 || '';
  let msgType, cellContent, attachment;

  if (content.includes('[图片：') || content.includes('[图片:')) {
    msgType = 'image';
    cellContent = null;
    attachment = 'image_' + (++imgCount);
  } else if (content.includes('[文件：') || content.includes('[文件:')) {
    msgType = 'file';
    cellContent = null;
    attachment = 'file_' + (++fileCount);
  } else {
    msgType = 'text';
    cellContent = content;
    attachment = null;
  }

  const r = i + 1;

  function setCell(c, v, fmt) {
    const addr = XLSX.utils.encode_cell({ r, c });
    if (v === null || v === undefined) {
      ws3[addr] = { t: 'z', v: null };
      return;
    }
    if (fmt) {
      ws3[addr] = { t: 'n', v, z: fmt };
    } else {
      ws3[addr] = { t: typeof v === 'number' ? 'n' : 's', v };
    }
  }

  setCell(0, i + 1);
  setCell(1, msgType);
  setCell(2, timeVal, 'yyyy/m/d h:mm;@');
  setCell(3, msg.发言人);
  setCell(4, cellContent);
  setCell(5, null);
  setCell(6, attachment);
});

ws3['!ref'] = `A1:G${rawMessages.length + 1}`;
XLSX.utils.book_append_sheet(wb, ws3, 'message_stream');

// ===== 写入文件 =====
XLSX.writeFile(wb, outputPath);

console.log(`✅ 写入完成: ${outputPath}`);
console.log(`   消息总数: ${rawMessages.length}`);
console.log(`   图片消息: ${imgCount}`);
console.log(`   文件消息: ${fileCount}`);
console.log(`   成员数: ${groupDef.members.length}`);

// 验证：读回第一行
const wb2 = XLSX.readFile(outputPath);
const check = wb2.Sheets['message_stream'];
console.log(`   时间格式验证 C2: ${check['C2'] ? check['C2'].w : '(空)'}`);

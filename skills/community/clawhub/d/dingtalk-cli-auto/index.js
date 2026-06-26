/**
 * 钉钉 CLI 自动化 - 统一入口
 * 支持直接导入使用或命令行调用
 * 
 * Usage:
 *   const { MessageClient, CalendarClient, TodoClient, ContactClient } = require('./');
 *   
 *   const msgClient = new MessageClient();
 *   await msgClient.sendText(userId, null, 'Hello');
 */

const MessageClient = require('./lib/message');
const CalendarClient = require('./lib/calendar');
const TodoClient = require('./lib/todo');
const ContactClient = require('./lib/contact');
const { DWSClient, DWSError, parseTime, formatISO, formatDisplay } = require('./lib/dws');

module.exports = {
  // 客户端
  MessageClient,
  CalendarClient,
  TodoClient,
  ContactClient,
  DWSClient,
  
  // 工具函数
  DWSError,
  parseTime,
  formatISO,
  formatDisplay
};
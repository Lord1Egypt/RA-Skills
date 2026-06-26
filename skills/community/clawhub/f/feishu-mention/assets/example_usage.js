/**
 * FeishuMention Resolver (v2.0) - 使用示例
 * 
 * 本示例展示如何使用 Account ID 和自动配置功能。
 * 前提：确保 ~/.openclaw/openclaw.json 中已配置相关账号。
 */

import { resolve } from '../index.js';

console.log('===== FeishuMention Resolver v2.0 使用示例 =====\n');

async function runExamples() {
  // 模拟上下文
  const chatId = 'oc_acc4410336517a2ff73413fac977c39a';
  const myAccount = 'elves'; // 假设当前执行者是 'elves'

  // =====================
  // 场景 1: 基础使用 (自动 Bot 发现)
  // =====================
  console.log('📌 场景 1: 基础使用 (自动 Bot 发现)');
  const text1 = '你好 @product，请确认需求';
  
  console.log(`输入: "${text1}"`);
  console.log(`身份: ${myAccount}`);
  
  // 系统会自动在配置中查找 "product" 账号对应的 OpenID
  const res1 = await resolve(text1, myAccount, chatId);
  console.log(`输出: ${res1}\n`);


  // =====================
  // 场景 2: 支持别名
  // =====================
  console.log('📌 场景 2: 支持别名');
  const text2 = '呼叫 @老张';
  const aliases = [
    { name: '张三', alias: ['老张', 'zhangsan'] }
  ];
  
  console.log(`输入: "${text2}"`);
  console.log(`别名配置: 张三 <- [老张]`);
  
  // "老张" -> "张三" -> 查找群成员 -> 获取 OpenID
  const res2 = await resolve(text2, myAccount, chatId, { aliases });
  console.log(`输出: ${res2}\n`);


  // =====================
  // 场景 3: 混合使用
  // =====================
  console.log('📌 场景 3: 混合使用');
  const text3 = '@product @backend 请配合 @老张 测试';
  
  console.log(`输入: "${text3}"`);
  
  const res3 = await resolve(text3, myAccount, chatId, { aliases });
  console.log(`输出: ${res3}\n`);
}

runExamples().catch(console.error);

#!/usr/bin/env node
/**
 * SMTP 连接测试脚本
 */

const nodemailer = require('nodemailer');

const configs = [
  {
    name: '端口 465 (SSL)',
    host: 'smtp.mxhichina.com',
    port: 465,
    secure: true,
    tls: { rejectUnauthorized: false },
  },
  {
    name: '端口 587 (STARTTLS)',
    host: 'smtp.mxhichina.com',
    port: 587,
    secure: false,
    requireTLS: true,
    tls: { rejectUnauthorized: false },
  },
  {
    name: '端口 25 (非加密)',
    host: 'smtp.mxhichina.com',
    port: 25,
    secure: false,
  },
];

const user = '8@batype.com';
const pass = '960515@ss.com';

async function testConfig(config) {
  console.log(`\n${'='.repeat(50)}`);
  console.log(`测试：${config.name}`);
  console.log(`${'='.repeat(50)}`);
  
  const transporter = nodemailer.createTransport({
    host: config.host,
    port: config.port,
    secure: config.secure,
    requireTLS: config.requireTLS,
    tls: config.tls,
    auth: { user, pass },
    debug: true,
    logger: true,
  });
  
  try {
    console.log('正在验证连接...');
    await transporter.verify();
    console.log(`✅ ${config.name} - 连接成功！`);
    
    // 尝试发送测试邮件
    console.log('正在发送测试邮件...');
    await transporter.sendMail({
      from: user,
      to: user,
      subject: 'SMTP 测试邮件',
      text: '这是一封测试邮件，用于验证 SMTP 配置是否正确。',
    });
    console.log(`✅ ${config.name} - 邮件发送成功！`);
    return true;
  } catch (error) {
    console.error(`❌ ${config.name} - 失败：${error.message}`);
    if (error.response) {
      console.error(`   服务器响应：${error.response}`);
    }
    return false;
  } finally {
    await transporter.close();
  }
}

async function main() {
  console.log('📧 SMTP 连接测试');
  console.log(`用户：${user}`);
  console.log(`密码：${'*'.repeat(pass.length)}`);
  
  let success = false;
  for (const config of configs) {
    const result = await testConfig(config);
    if (result) {
      success = true;
      console.log(`\n✅ 推荐配置：使用 ${config.name}`);
      break;
    }
  }
  
  if (!success) {
    console.log('\n❌ 所有配置都失败了');
    console.log('\n可能原因：');
    console.log('  1. 密码错误（需要使用客户端授权码，不是登录密码）');
    console.log('  2. SMTP 服务未开启');
    console.log('  3. 账号被限制');
    console.log('\n解决方案：');
    console.log('  1. 登录 https://qiye.aliyun.com/alimail/');
    console.log('  2. 设置 → 安全设置 → 生成客户端授权码');
    console.log('  3. 使用授权码替换密码');
  }
}

main().catch(console.error);

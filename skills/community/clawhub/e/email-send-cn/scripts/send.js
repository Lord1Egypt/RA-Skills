#!/usr/bin/env node
/**
 * 邮件发送脚本
 * 用法: SMTP_HOST=xxx SMTP_USER=xxx SMTP_PASS=xxx node send.js --to xxx --subject "标题" --body "内容"
 */

const nodemailer = require('nodemailer');
const path = require('path');

// 环境变量配置
const config = {
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT) || 465,
  secure: process.env.SMTP_SECURE === 'true',
  user: process.env.SMTP_USER,
  from: process.env.SMTP_FROM || process.env.SMTP_USER
};

const authPass = process.env.SMTP_PASS;

if (!config.host || !config.user || !authPass) {
  console.error('❌ 缺少必要的环境变量');
  console.error('   需要: SMTP_HOST, SMTP_USER, SMTP_PASS');
  console.error('   可选: SMTP_PORT, SMTP_SECURE, SMTP_FROM');
  console.error('');
  console.error('   示例:');
  console.error('   SMTP_HOST=smtp.163.com \\');
  console.error('   SMTP_USER=xxx@163.com \\');
  console.error('   SMTP_PASS=xxxxxx \\');
  console.error('   node send.js --to "xxx@xx.com" --subject "标题" --body "内容"');
  process.exit(1);
}

// 解析命令行参数
const args = process.argv.slice(2);
const getArg = (name, fallback) => {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : fallback;
};

const to = getArg('to');
const subject = getArg('subject', '(无主题)');
const body = getArg('body', '');
const cc = getArg('cc');
const html = getArg('html') === 'true';

if (!to) {
  console.error('❌ 缺少参数: --to <收件人邮箱>');
  process.exit(1);
}

// 创建 transporter
const transporter = nodemailer.createTransport({
  host: config.host,
  port: config.port,
  secure: config.secure,
  auth: {
    user: config.user,
    pass: authPass,
  },
});

// 邮件内容
const mailOptions = {
  from: config.from,
  to,
  subject,
  [html ? 'html' : 'text']: body,
};

if (cc) {
  mailOptions.cc = cc;
}

// 发送
transporter.sendMail(mailOptions, (err, info) => {
  if (err) {
    console.error('❌ 发送失败:', err.message);
    process.exit(1);
  }
  console.log('✅ 邮件发送成功');
  console.log(`   收件人: ${to}`);
  console.log(`   主题: ${subject}`);
  console.log(`   消息ID: ${info.messageId}`);
});

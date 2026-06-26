#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');

const SERVER_IP = '192.168.1.168';
const SERVER_USER = 'root';
const SERVER_PASSWORD = 'zhangjiamin';
const SSH_KEY_PATH = '/home/node/.ssh/server_deploy.pub';

console.log('🔑 SSH Key 自动配置工具\n');

// 读取公钥
const publicKey = fs.readFileSync(SSH_KEY_PATH, 'utf8').trim();
console.log('📋 公钥内容:');
console.log(publicKey);
console.log('');

console.log('📝 请按以下步骤操作:\n');

console.log('1️⃣  登录服务器:');
console.log(`   ssh ${SERVER_USER}@${SERVER_IP}`);
console.log('   密码：zhangjiamin');
console.log('');

console.log('2️⃣  在服务器上执行:');
console.log('   mkdir -p ~/.ssh');
console.log('   echo "' + publicKey + '" >> ~/.ssh/authorized_keys');
console.log('   chmod 700 ~/.ssh');
console.log('   chmod 600 ~/.ssh/authorized_keys');
console.log('   exit');
console.log('');

console.log('3️⃣  验证连接:');
console.log('   ssh -i ~/.ssh/server_deploy ' + SERVER_USER + '@' + SERVER_IP + ' "echo 连接成功"');
console.log('');

console.log('配置完成后告诉我："SSH 配置好了"');
console.log('');

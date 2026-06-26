const skill = require('./index.js');

const email = `Dear Friend,

I hope this email finds you well. I wanted to share some exciting information about a powerful tool I've been using recently.

---

# OpenClaw

Any OS gateway for AI agents across WhatsApp, Telegram, Discord, iMessage, and more.

## What is OpenClaw?

OpenClaw is a self-hosted gateway that connects your favorite chat apps (WhatsApp, Telegram, Discord, iMessage, and more) to AI coding agents. You run a single Gateway process on your own machine (or a server), and it becomes the bridge between your messaging apps and an always-available AI assistant.

## Who is it for?

Developers and power users who want a personal AI assistant they can message from anywhere - without giving up control of their data or relying on a hosted service.

## What makes it different?

- Self-hosted: runs on your hardware, your rules
- Multi-channel: one Gateway serves WhatsApp, Telegram, Discord, and more simultaneously
- Agent-native: built for AI assistants, not just message routing
- Extensible: plugins add Mattermost and more

## Key Features

1. Gateway Daemon - Central hub for all messaging channels
2. Control UI - Browser dashboard for chat, config, and sessions
3. Skills System - Extensible capabilities
4. Multi-Platform - WhatsApp, Telegram, Discord, iMessage, Signal, and more

## Quick Start

1. Install: npm install -g openclaw
2. Run wizard: openclaw onboard
3. Start gateway: openclaw gateway

---

I think this could be really useful for our projects. Let me know what you think!

Best regards,
zong.yz@163.com

---
This email was sent via OpenClaw 163 Mail Skill
`;

skill.utils.sendEmail('zongxuliang@163.com', '好好看下这篇文章', email).then(result => {
    console.log('✅ 邮件发送成功');
    console.log('消息 ID:', result.messageId);
    console.log('收件人:', result.accepted[0]);
}).catch(err => {
    console.error('❌ 发送失败:', err.message);
});

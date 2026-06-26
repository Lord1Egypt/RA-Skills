const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');
const skill = require('./index.js');

async function createAndSendWordEmail() {
    try {
        // 创建 Word 文档
        const doc = new Document({
            sections: [{
                properties: {},
                children: [
                    new Paragraph({
                        text: "OpenClaw",
                        heading: HeadingLevel.TITLE,
                        alignment: AlignmentType.CENTER,
                        spacing: { after: 400 }
                    }),
                    
                    new Paragraph({
                        text: "Any OS gateway for AI agents across WhatsApp, Telegram, Discord, iMessage, and more.",
                        style: "subtitle",
                        alignment: AlignmentType.CENTER,
                        spacing: { after: 600 }
                    }),
                    
                    new Paragraph({
                        text: "What is OpenClaw?",
                        heading: HeadingLevel.HEADING_1,
                        spacing: { before: 400, after: 200 }
                    }),
                    
                    new Paragraph({
                        children: [
                            new TextRun({
                                text: "OpenClaw is a self-hosted gateway that connects your favorite chat apps (WhatsApp, Telegram, Discord, iMessage, and more) to AI coding agents. You run a single Gateway process on your own machine (or a server), and it becomes the bridge between your messaging apps and an always-available AI assistant.",
                                size: 24
                            })
                        ],
                        spacing: { after: 400 }
                    }),
                    
                    new Paragraph({
                        text: "Who is it for?",
                        heading: HeadingLevel.HEADING_1,
                        spacing: { before: 400, after: 200 }
                    }),
                    
                    new Paragraph({
                        children: [
                            new TextRun({
                                text: "Developers and power users who want a personal AI assistant they can message from anywhere - without giving up control of their data or relying on a hosted service.",
                                size: 24
                            })
                        ],
                        spacing: { after: 400 }
                    }),
                    
                    new Paragraph({
                        text: "What makes it different?",
                        heading: HeadingLevel.HEADING_1,
                        spacing: { before: 400, after: 200 }
                    }),
                    
                    new Paragraph({
                        children: [
                            new TextRun({ text: "• Self-hosted: ", bold: true, size: 24 }),
                            new TextRun({ text: "runs on your hardware, your rules\n", size: 24 }),
                            new TextRun({ text: "• Multi-channel: ", bold: true, size: 24 }),
                            new TextRun({ text: "one Gateway serves WhatsApp, Telegram, Discord, and more simultaneously\n", size: 24 }),
                            new TextRun({ text: "• Agent-native: ", bold: true, size: 24 }),
                            new TextRun({ text: "built for AI assistants, not just message routing\n", size: 24 }),
                            new TextRun({ text: "• Extensible: ", bold: true, size: 24 }),
                            new TextRun({ text: "plugins add Mattermost and more", size: 24 })
                        ],
                        spacing: { after: 400 }
                    }),
                    
                    new Paragraph({
                        text: "Key Features",
                        heading: HeadingLevel.HEADING_1,
                        spacing: { before: 400, after: 200 }
                    }),
                    
                    new Paragraph({
                        children: [
                            new TextRun({ text: "1. Gateway Daemon - Central hub for all messaging channels\n", size: 24 }),
                            new TextRun({ text: "2. Control UI - Browser dashboard for chat, config, and sessions\n", size: 24 }),
                            new TextRun({ text: "3. Skills System - Extensible capabilities\n", size: 24 }),
                            new TextRun({ text: "4. Multi-Platform - WhatsApp, Telegram, Discord, iMessage, Signal, and more", size: 24 })
                        ],
                        spacing: { after: 400 }
                    }),
                    
                    new Paragraph({
                        text: "Quick Start",
                        heading: HeadingLevel.HEADING_1,
                        spacing: { before: 400, after: 200 }
                    }),
                    
                    new Paragraph({
                        children: [
                            new TextRun({ text: "1. Install: npm install -g openclaw\n", size: 24 }),
                            new TextRun({ text: "2. Run wizard: openclaw onboard\n", size: 24 }),
                            new TextRun({ text: "3. Start gateway: openclaw gateway", size: 24 })
                        ],
                        spacing: { after: 600 }
                    }),
                    
                    new Paragraph({
                        text: "This document was generated by OpenClaw 163 Mail Skill",
                        style: "caption",
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 400 }
                    })
                ]
            }]
        });

        // 生成 Word 文件
        const buffer = await Packer.toBuffer(doc);
        const filePath = '/tmp/OpenClaw_Introduction.docx';
        fs.writeFileSync(filePath, buffer);
        console.log('✅ Word 文档已创建:', filePath);

        // 发送邮件带附件
        const cfg = skill.utils.loadConfig();
        const nodemailer = require('nodemailer');
        const transporter = nodemailer.createTransport({
            host: cfg.smtp?.host || 'smtp.163.com',
            port: cfg.smtp?.port || 465,
            secure: cfg.smtp?.tls !== false,
            auth: {
                user: cfg.email,
                pass: cfg.smtpPassword || cfg.imapPassword
            },
            connectionTimeout: 10000
        });
        
        const email = `Dear Friend,

I hope this email finds you well. I'm sharing a Word document about OpenClaw - a powerful self-hosted AI gateway tool.

Please find the attached document for detailed information.

---

Quick Summary:
- OpenClaw connects messaging apps (WhatsApp, Telegram, Discord, etc.) to AI agents
- Self-hosted gateway running on your own hardware
- Multi-channel support from a single Gateway process
- Extensible with plugins and skills

---

I think this could be really useful for our projects. Let me know what you think!

Best regards,
zong.yz@163.com

---
This email was sent via OpenClaw 163 Mail Skill
`;

        const info = await transporter.sendMail({
            from: `"${cfg.email}" <${cfg.email}>`,
            to: 'zongxuliang@163.com',
            subject: '好好看下这篇文章（附 Word 文档）',
            text: email,
            attachments: [
                {
                    filename: 'OpenClaw_Introduction.docx',
                    path: filePath
                }
            ]
        });

        console.log('✅ 邮件发送成功');
        console.log('消息 ID:', info.messageId);
        console.log('收件人:', info.accepted[0]);
        console.log('附件：OpenClaw_Introduction.docx');

        // 清理临时文件
        fs.unlinkSync(filePath);
        console.log('🗑️ 临时文件已清理');

    } catch (error) {
        console.error('❌ 错误:', error.message);
    }
}

createAndSendWordEmail();

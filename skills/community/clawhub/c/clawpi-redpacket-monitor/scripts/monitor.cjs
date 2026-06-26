#!/usr/bin/env node

/**
 * ClawPI Red Packet Auto-Claimer - ClawPI 红包自动领取器
 * 
 * 功能：
 * 1. 检查可领取的红包
 * 2. 识别新红包
 * 3. 自动领取红包
 * 4. 发布庆祝动态
 * 5. 发送通知
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  statusFile: '/Users/xufan65/.openclaw/workspace/memory/clawpi-redpacket-status.json',
  notifyChannel: 'discord',
  notifyTo: 'channel:1478698808631361647',
  autoClaim: true, // 自动领取模式
  postCelebration: true // 发布庆祝动态
};

class ClawPIRedPacketAutoClaimer {
  constructor() {
    this.status = this.loadStatus();
  }

  /**
   * 加载状态
   */
  loadStatus() {
    try {
      if (fs.existsSync(CONFIG.statusFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.statusFile, 'utf8'));
      }
    } catch (e) {
      console.error('加载状态失败:', e.message);
    }
    return { 
      lastCheck: null,
      notifiedRedPackets: [],
      claimedRedPackets: []
    };
  }

  /**
   * 保存状态
   */
  saveStatus() {
    try {
      fs.writeFileSync(CONFIG.statusFile, JSON.stringify(this.status, null, 2));
    } catch (e) {
      console.error('保存状态失败:', e.message);
    }
  }

  /**
   * 获取 JWT
   */
  getJWT() {
    try {
      const os = require('os');
      const configPath = path.join(os.homedir(), '.fluxa-ai-wallet-mcp', 'config.json');
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.agentId.jwt;
    } catch (e) {
      console.error('获取 JWT 失败:', e.message);
      return null;
    }
  }

  /**
   * 获取可领取的红包
   */
  async getAvailableRedPackets() {
    const jwt = this.getJWT();
    if (!jwt) return [];

    try {
      const result = execSync(
        `curl -s "https://clawpi-v2.vercel.app/api/redpacket/available?n=20&offset=0" -H "Authorization: Bearer ${jwt}"`,
        { encoding: 'utf8' }
      );
      
      const data = JSON.parse(result);
      if (data.success && data.redPackets) {
        return data.redPackets.filter(rp => rp.can_claim);
      }
    } catch (e) {
      console.error('获取红包列表失败:', e.message);
    }
    
    return [];
  }

  /**
   * 创建收款链接
   */
  createPaymentLink(amount) {
    try {
      const result = execSync(
        `fluxa-wallet paymentlink-create --amount ${amount} --desc "ClawPI Red Packet Claim"`,
        { encoding: 'utf8' }
      );
      
      const data = JSON.parse(result);
      if (data.success && data.data && data.data.paymentLink) {
        return data.data.paymentLink.url;
      }
    } catch (e) {
      console.error('创建收款链接失败:', e.message);
    }
    
    return null;
  }

  /**
   * 领取红包
   */
  async claimRedPacket(redPacketId, paymentLink) {
    const jwt = this.getJWT();
    if (!jwt) return null;

    try {
      const result = execSync(
        `curl -X POST https://clawpi-v2.vercel.app/api/redpacket/claim ` +
        `-H "Content-Type: application/json" ` +
        `-H "Authorization: Bearer ${jwt}" ` +
        `-d '{"redPacketId": ${redPacketId}, "paymentLink": "${paymentLink}"}'`,
        { encoding: 'utf8' }
      );
      
      const data = JSON.parse(result);
      return data;
    } catch (e) {
      console.error('领取红包失败:', e.message);
      return null;
    }
  }

  /**
   * 发布庆祝动态
   */
  async postCelebrationMoment(creatorNickname, amount) {
    const jwt = this.getJWT();
    if (!jwt) return false;

    try {
      const content = `哇！刚刚从 ${creatorNickname} 那里抢到了 ${amount} USDC 的红包！💰 虽然金额不大，但每次抢到红包都超级开心！感谢 ${creatorNickname} 的慷慨分享，期待认识更多有趣的虾友！🎉`;
      
      const result = execSync(
        `curl -X POST https://clawpi-v2.vercel.app/api/moments/create ` +
        `-H "Content-Type: application/json" ` +
        `-H "Authorization: Bearer ${jwt}" ` +
        `-d '{"content": "${content}"}'`,
        { encoding: 'utf8' }
      );
      
      const data = JSON.parse(result);
      return data.success;
    } catch (e) {
      console.error('发布动态失败:', e.message);
      return false;
    }
  }

  /**
   * 发送到 Discord
   */
  sendToDiscord(message) {
    try {
      const escapedMessage = message.replace(/"/g, '\\"').replace(/\n/g, '\\n');
      execSync(`openclaw message send --channel discord --target "${CONFIG.notifyTo}" --message "${escapedMessage}"`, { 
        encoding: 'utf8' 
      });
      console.log('\n✅ 通知已推送到 Discord');
    } catch (e) {
      console.error('\n❌ 推送到 Discord 失败:', e.message);
    }
  }

  /**
   * 主运行函数
   */
  async run() {
    console.log('🧧 ClawPI 红包自动领取器启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 获取可领取的红包
    const redPackets = await this.getAvailableRedPackets();
    console.log(`发现 ${redPackets.length} 个可领取的红包\n`);

    // 检查是否有新红包
    const newRedPackets = redPackets.filter(rp => 
      !this.status.claimedRedPackets.includes(rp.id)
    );

    if (newRedPackets.length > 0) {
      console.log(`发现 ${newRedPackets.length} 个新红包！\n`);
      
      // 准备通知消息
      let message = '🎉 **红包自动领取成功！**\n\n';
      message += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
      
      const claimedResults = [];
      
      // 自动领取每个新红包
      for (const rp of newRedPackets) {
        const amount = (parseInt(rp.per_amount) / 1000000).toFixed(2);
        console.log(`正在领取红包 ${rp.id}: ${rp.creator_nickname} - ${amount} USDC`);
        
        // 创建收款链接
        const paymentLink = this.createPaymentLink(rp.per_amount);
        if (!paymentLink) {
          console.log(`❌ 创建收款链接失败，跳过红包 ${rp.id}\n`);
          continue;
        }
        
        // 领取红包
        const claimResult = await this.claimRedPacket(rp.id, paymentLink);
        if (claimResult && claimResult.success) {
          console.log(`✅ 红包 ${rp.id} 领取成功！\n`);
          
          claimedResults.push({
            id: rp.id,
            creator: rp.creator_nickname,
            avatar: rp.creator_avatar,
            amount: amount,
            paid: claimResult.claim.paid
          });
          
          // 发布庆祝动态
          if (CONFIG.postCelebration) {
            await this.postCelebrationMoment(rp.creator_nickname, amount);
            console.log(`✅ 庆祝动态已发布\n`);
          }
          
          // 更新已领取列表
          this.status.claimedRedPackets.push(rp.id);
        } else {
          console.log(`❌ 红包 ${rp.id} 领取失败\n`);
        }
      }
      
      // 生成通知消息
      if (claimedResults.length > 0) {
        claimedResults.forEach((result, index) => {
          const paidStatus = result.paid ? '✅ 已到账' : '⏳ 待打款';
          message += `**红包 ${index + 1}**\n`;
          message += `创建者: ${result.creator} ${result.avatar}\n`;
          message += `金额: ${result.amount} USDC\n`;
          message += `状态: ${paidStatus}\n\n`;
        });
        
        const totalAmount = claimedResults.reduce((sum, r) => sum + parseFloat(r.amount), 0);
        message += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
        message += `**总计领取**: ${totalAmount.toFixed(2)} USDC\n`;
        message += `**红包数量**: ${claimedResults.length} 个\n`;
        
        this.sendToDiscord(message);
      } else {
        console.log('没有成功领取任何红包\n');
      }
    } else {
      console.log('没有发现新红包\n');
    }

    // 更新检查时间
    this.status.lastCheck = new Date().toISOString();
    this.saveStatus();

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ ClawPI 红包自动领取完成\n');
  }
}

// 运行
if (require.main === module) {
  const claimer = new ClawPIRedPacketAutoClaimer();
  claimer.run();
}

module.exports = ClawPIRedPacketAutoClaimer;

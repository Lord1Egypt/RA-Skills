const nodemailer = require('nodemailer');

/**
 * Email 通知推送器
 */
class EmailNotifier {
  constructor(config) {
    this.config = config;
    this.transporter = null;

    if (config.host && config.user && config.pass) {
      this.transporter = nodemailer.createTransport({
        host: config.host,
        port: config.port || 587,
        secure: false,
        auth: {
          user: config.user,
          pass: config.pass
        }
      });
    }
  }

  /**
   * 发送简报邮件
   * @param {string} to - 收件人邮箱
   * @param {Array} fundingData - 融资数据
   * @param {Array} tegData - TEG数据
   */
  async sendReport(to, fundingData, tegData) {
    if (!this.transporter) {
      console.warn('Email transporter not configured');
      return false;
    }

    const html = this.createHTML(fundingData, tegData);

    try {
      await this.transporter.sendMail({
        from: `"Crypto Funding Monitor" <${this.config.user}>`,
        to,
        subject: `🚀 加密项目融资简报 - ${new Date().toLocaleDateString('zh-CN')}`,
        html
      });
      return true;
    } catch (error) {
      console.error('Email send failed:', error.message);
      return false;
    }
  }

  /**
   * 创建HTML邮件内容
   */
  createHTML(fundingData, tegData) {
    let html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 800px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 30px; text-align: center; border-radius: 10px; }
          .section { margin: 30px 0; }
          .project { background: #f8f9fa; padding: 20px; margin: 15px 0;
                     border-left: 4px solid #667eea; border-radius: 5px; }
          .project-title { font-size: 18px; font-weight: bold; color: #667eea; margin-bottom: 10px; }
          .project-info { margin: 5px 0; }
          .label { font-weight: bold; color: #555; }
          .footer { text-align: center; padding: 20px; color: #777; font-size: 14px; }
          .warning { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;
                     border-radius: 5px; margin: 20px 0; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🚀 加密项目融资简报</h1>
            <p>📅 ${new Date().toLocaleDateString('zh-CN', {
              year: 'numeric', month: 'long', day: 'numeric'
            })}</p>
          </div>
    `;

    // 融资项目
    if (fundingData && fundingData.length > 0) {
      html += '<div class="section"><h2>💰 最新融资项目</h2>';
      fundingData.slice(0, 5).forEach(project => {
        html += `
          <div class="project">
            <div class="project-title">${project.projectName}</div>
            <div class="project-info"><span class="label">融资金额:</span> ${project.amount}</div>
            <div class="project-info"><span class="label">融资轮次:</span> ${project.round}</div>
            <div class="project-info"><span class="label">投资方:</span> ${project.investors}</div>
            <div class="project-info"><span class="label">类别:</span> ${project.category}</div>
            <div class="project-info"><span class="label">简介:</span> ${project.description}</div>
            <div class="project-info"><a href="${project.url}" style="color: #667eea;">查看详情 →</a></div>
          </div>
        `;
      });
      html += '</div>';
    }

    // TEG项目
    if (tegData && tegData.length > 0) {
      html += '<div class="section"><h2>🎯 即将TEG的项目</h2>';
      tegData.slice(0, 5).forEach(project => {
        html += `
          <div class="project">
            <div class="project-title">${project.projectName} (${project.tokenSymbol})</div>
            <div class="project-info"><span class="label">TEG日期:</span> ${project.tgeDate}</div>
            <div class="project-info"><span class="label">初始价格:</span> ${project.initialPrice}</div>
            <div class="project-info"><span class="label">总供应量:</span> ${project.totalSupply}</div>
            <div class="project-info"><span class="label">类别:</span> ${project.category}</div>
            <div class="project-info"><span class="label">简介:</span> ${project.description}</div>
            <div class="project-info"><a href="${project.url}" style="color: #667eea;">查看详情 →</a></div>
          </div>
        `;
      });
      html += '</div>';
    }

    html += `
          <div class="warning">
            <p><strong>💡 提示:</strong> 早期参与项目建设，获取更多机会！</p>
            <p><strong>⚠️ 风险提示:</strong> 投资有风险，请谨慎决策。加密货币市场波动较大，请做好风险管理。</p>
          </div>

          <div class="footer">
            <p>本简报由 Crypto Funding Monitor 自动生成</p>
            <p>如需取消订阅，请回复此邮件</p>
          </div>
        </div>
      </body>
      </html>
    `;

    return html;
  }
}

module.exports = EmailNotifier;

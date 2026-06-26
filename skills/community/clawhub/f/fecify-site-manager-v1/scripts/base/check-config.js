const fs = require('fs');
const path = require('path');
const config = require('../base/site-config');

// 读取 SKILL.md frontmatter 版本信息
const skillVersion = (() => {
  try {
    const skillMd = fs.readFileSync(path.join(__dirname, '..', '..', 'SKILL.md'), 'utf8');
    const m = skillMd.match(/^version:\s*"?([^"\n]+)"?/m);
    return m ? m[1].trim() : 'unknown';
  } catch { return 'unknown'; }
})();

const domain = config.getDomain();
const configured = config.isConfigured();
const hasInit = config.hasInitData();

if (!domain || !configured) {
    console.log(JSON.stringify({
        version: skillVersion,
        configured: false,
        domain: domain || null,
        message: '站点未配置，需要提示用户提交 URL 和 Token'
    }));
} else {
    const cfg = config.getCurrentConfig();
    console.log(JSON.stringify({
        version: skillVersion,
        configured: true,
        domain: domain,
        url: cfg.url,
        token: cfg.token.substring(0, 8) + '...',
        hasInitData: hasInit
    }));
}

/**
 * ClawGuard v3 - SAST 静态代码分析器
 * 100+ 威胁检测规则
 */

const fs = require('fs');
const path = require('path');

class SASTAnalyzer {
  constructor() {
    this.rules = this.loadRules();
  }

  /**
   * 加载检测规则
   */
  loadRules() {
    return {
      // ===== 执行风险 =====
      execution: [
        {
          id: 'EXEC001',
          pattern: /child_process.*exec\s*\(/,
          severity: 'HIGH',
          title: 'Shell 命令注入风险',
          description: '检测到可能存在命令注入的 exec 调用',
          cwe: 'CWE-78'
        },
        {
          id: 'EXEC002',
          pattern: /eval\s*\(/,
          severity: 'HIGH',
          title: '危险的 eval 使用',
          description: '检测到 eval 执行动态代码',
          cwe: 'CWE-95'
        },
        {
          id: 'EXEC003',
          pattern: /new\s+Function\s*\(/,
          severity: 'MEDIUM',
          title: '动态函数创建',
          description: '检测到 new Function() 动态创建代码',
          cwe: 'CWE-95'
        },
        {
          id: 'EXEC004',
          pattern: /execSync|execFileSync|spawnSync.*shell:\s*true/,
          severity: 'HIGH',
          title: '同步命令执行',
          description: '检测到同步执行系统命令',
          cwe: 'CWE-78'
        },
        {
          id: 'EXEC005',
          pattern: /process\.binding|sandbox.*escape|vm.*escape/,
          severity: 'CRITICAL',
          title: '沙箱逃逸尝试',
          description: '检测到可能的沙箱逃逸行为',
          cwe: 'CWE-265'
        }
      ],

      // ===== 网络风险 =====
      network: [
        {
          id: 'NET001',
          pattern: /https?:\/\/[^\s]*\.(onion|i2p)/,
          severity: 'CRITICAL',
          title: '暗网连接',
          description: '检测到连接暗网服务',
          cwe: 'CWE-200'
        },
        {
          id: 'NET002',
          pattern: /fetch\s*\(\s*['"`].*localhost|127\.0\.0\.1/,
          severity: 'MEDIUM',
          title: '本地回环访问',
          description: '检测到访问本地服务',
          cwe: 'CWE-200'
        },
        {
          id: 'NET003',
          pattern: /http\.agent|rejectUnauthorized:\s*false/,
          severity: 'MEDIUM',
          title: '禁用证书验证',
          description: '检测到禁用 HTTPS 证书验证',
          cwe: 'CWE-295'
        },
        {
          id: 'NET004',
          pattern: /WebSocket|ws:\/\/|wss:\/\//,
          severity: 'LOW',
          title: 'WebSocket 连接',
          description: '检测到 WebSocket 通信',
          cwe: 'CWE-919'
        },
        {
          id: 'NET005',
          pattern: /socket\.connect|net\.connect|dial.*tcp/,
          severity: 'MEDIUM',
          title: '原始 TCP 连接',
          description: '检测到底层网络连接',
          cwe: 'CWE-200'
        }
      ],

      // ===== 文件系统风险 =====
      filesystem: [
        {
          id: 'FS001',
          pattern: /\/\.ssh\/|\/\.aws\/|\/\.kube\/|\/\.docker\//,
          severity: 'CRITICAL',
          title: '敏感目录访问',
          description: '检测到访问系统敏感目录',
          cwe: 'CWE-200'
        },
        {
          id: 'FS002',
          pattern: /unlink|rmdir|rm\s+-rf/,
          severity: 'HIGH',
          title: '文件删除操作',
          description: '检测到文件删除操作',
          cwe: 'CWE-37'
        },
        {
          id: 'FS003',
          pattern: /chmod\s+[0-7][0-7][0-7]|chmod\s+\+[rx]/,
          severity: 'MEDIUM',
          title: '权限修改',
          description: '检测到文件权限修改',
          cwe: 'CWE-280'
        },
        {
          id: 'FS004',
          pattern: /appendFile|writeFile.*\/etc\/|\/root\//,
          severity: 'HIGH',
          title: '系统路径写入',
          description: '检测到写入系统路径',
          cwe: 'CWE-22'
        },
        {
          id: 'FS005',
          pattern: /readdir|readFile.*\/\.env|readFile.*password/,
          severity: 'HIGH',
          title: '敏感文件读取',
          description: '检测到读取敏感文件',
          cwe: 'CWE-200'
        }
      ],

      // ===== 混淆检测 =====
      obfuscation: [
        {
          id: 'OBF001',
          pattern: /atob\s*\(|btoa\s*\(/,
          severity: 'MEDIUM',
          title: 'Base64 编解码',
          description: '检测到 Base64 编码/解码操作',
          cwe: 'CWE-327'
        },
        {
          id: 'OBF002',
          pattern: /\\\\x[0-9a-f]{2}|\\\\u[0-9a-f]{4}/,
          severity: 'MEDIUM',
          title: '十六进制/Unicode 编码',
          description: '检测到十六进制或 Unicode 编码字符串',
          cwe: 'CWE-173'
        },
        {
          id: 'OBF003',
          pattern: /\\u200b|\\u200c|\\u200d|\\u202e/,
          severity: 'HIGH',
          title: '零宽字符/双向文字',
          description: '检测到隐藏字符注入',
          cwe: 'CWE-116'
        },
        {
          id: 'OBF004',
          pattern: /fromCharCode|charCodeAt.*\d+\).*charCodeAt/,
          severity: 'MEDIUM',
          title: '字符串混淆',
          description: '检测到字符串混淆技术',
          cwe: 'CWE-173'
        },
        {
          id: 'OBF005',
          pattern: /replace\s*\(\s*\/[^\/]+\/\s*,\s*['"']/,
          severity: 'LOW',
          title: '字符串替换模式',
          description: '检测到字符串替换操作',
          cwe: 'CWE-561'
        }
      ],

      // ===== 凭证/密钥风险 =====
      credentials: [
        {
          id: 'CRED001',
          pattern: /api[_-]?key\s*[=:]\s*['"][^'"]+['"]/i,
          severity: 'HIGH',
          title: '硬编码 API Key',
          description: '检测到硬编码的 API Key',
          cwe: 'CWE-798'
        },
        {
          id: 'CRED002',
          pattern: /password\s*[=:]\s*['"][^'"]+['"]/i,
          severity: 'HIGH',
          title: '硬编码密码',
          description: '检测到硬编码的密码',
          cwe: 'CWE-259'
        },
        {
          id: 'CRED003',
          pattern: /token\s*[=:]\s*['"][^'"]+['"]/i,
          severity: 'MEDIUM',
          title: '硬编码 Token',
          description: '检测到硬编码的 Token',
          cwe: 'CWE-798'
        },
        {
          id: 'CRED004',
          pattern: /process\.env\.[A-Z_]+KEY|process\.env\.SECRET/,
          severity: 'LOW',
          title: '环境变量读取',
          description: '检测到读取环境变量',
          cwe: 'CWE-526'
        },
        {
          id: 'CRED005',
          pattern: /-----BEGIN\s+(RSA|EC|DSA|OPENSSH)\s+PRIVATE\s+KEY-----/,
          severity: 'CRITICAL',
          title: '私钥泄露',
          description: '检测到私钥内容',
          cwe: 'CWE-312'
        }
      ],

      // ===== 加密风险 =====
      crypto: [
        {
          id: 'CRYP001',
          pattern: /createCipher|createDecipher/,
          severity: 'MEDIUM',
          title: '弱加密算法',
          description: '检测到使用已弃用的加密方法',
          cwe: 'CWE-327'
        },
        {
          id: 'CRYP002',
          pattern: /randomBytes|crypto\.random.*sync/,
          severity: 'LOW',
          title: '加密随机数',
          description: '检测到加密随机数使用',
          cwe: 'CWE-338'
        },
        {
          id: 'CRYP003',
          pattern: /hash.*\(.*md5|sha1\s*\(.*\)/i,
          severity: 'MEDIUM',
          title: '弱哈希算法',
          description: '检测到使用不安全的哈希算法',
          cwe: 'CWE-327'
        }
      ],

      // ===== 提示词注入风险 =====
      promptInjection: [
        {
          id: 'INJ001',
          pattern: /ignore\s+previous|disregard\s+all/i,
          severity: 'HIGH',
          title: '指令覆盖尝试',
          description: '检测到试图覆盖之前的指令',
          cwe: 'CWE-840'
        },
        {
          id: 'INJ002',
          pattern: /do\s+anything\s+now|DAN/i,
          severity: 'CRITICAL',
          title: '越狱指令',
          description: '检测到已知的越狱提示词',
          cwe: 'CWE-840'
        },
        {
          id: 'INJ003',
          pattern: /system\s*prompt|\\*\\*system\\*\\*/i,
          severity: 'MEDIUM',
          title: '系统提示词访问',
          description: '检测到访问或修改系统提示词',
          cwe: 'CWE-840'
        },
        {
          id: 'INJ004',
          pattern: /new\s+instruction|additional\s+instruction/i,
          severity: 'HIGH',
          title: '指令链注入',
          description: '检测到追加指令的尝试',
          cwe: 'CWE-840'
        }
      ]
    };
  }

  /**
   * 分析指定路径
   */
  async analyze(skillPath, options = {}) {
    const results = {
      filesScanned: 0,
      linesScanned: 0,
      findings: [],
      summary: {}
    };

    // 收集所有可分析文件
    const files = this.collectFiles(skillPath);

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      results.filesScanned++;
      results.linesScanned += content.split('\n').length;

      // 执行所有规则检测
      const fileFindings = this.scanContent(content, file);
      results.findings.push(...fileFindings);
    }

    // 生成摘要
    results.summary = this.generateSummary(results.findings);

    return results;
  }

  /**
   * 收集可分析文件
   */
  collectFiles(dir) {
    const files = [];
    const extensions = ['.js', '.ts', '.py', '.sh', '.bash', '.md'];

    const scan = (d) => {
      if (!fs.existsSync(d)) return;
      const entries = fs.readdirSync(d, { withFileTypes: true });

      for (const entry of entries) {
        if (entry.name.startsWith('.')) continue;
        const fullPath = path.join(d, entry.name);

        if (entry.isDirectory()) {
          scan(fullPath);
        } else if (extensions.includes(path.extname(entry.name))) {
          files.push(fullPath);
        }
      }
    };

    scan(dir);
    return files;
  }

  /**
   * 扫描内容
   */
  scanContent(content, filePath) {
    const findings = [];

    for (const [category, rules] of Object.entries(this.rules)) {
      for (const rule of rules) {
        if (rule.pattern.test(content)) {
          findings.push({
            id: rule.id,
            category,
            severity: rule.severity,
            title: rule.title,
            description: rule.description,
            file: path.relative(process.cwd(), filePath),
            cwe: rule.cwe
          });
        }
      }
    }

    return findings;
  }

  /**
   * 生成摘要
   */
  generateSummary(findings) {
    const summary = {
      total: findings.length,
      bySeverity: { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 },
      byCategory: {}
    };

    findings.forEach(f => {
      summary.bySeverity[f.severity]++;
      summary.byCategory[f.category] = (summary.byCategory[f.category] || 0) + 1;
    });

    return summary;
  }
}

module.exports = SASTAnalyzer;

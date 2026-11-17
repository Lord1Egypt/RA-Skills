/**
 * agent-boundary-guard.js — [心虫自主决策 2026-08-13] 跨界写入门禁
 *
 * 背景：Hermes/Claude 等 agent 以 root 运行时，可自由读写其他 agent 的配置目录
 * （~/.claude、~/.agents、~/.openclaw 等）。安装/误操作/提示注入可导致
 * 一个 agent 修改另一个 agent 的技能文件，影响其行为。
 *
 * 本模块是心虫（辨别者/门禁层）对该隐患的监督能力：
 *  - 维护"本 agent 地盘"清单（默认 ~/.hermes）
 *  - 检测"跨界写入"：写路径落在其他 agent 地盘 → 拦截/警告
 *  - 提供 checkWrite(path) 供 Hermes 等宿主的文件操作前调用
 *  - 提供 audit 日志（谁、何时、试图写哪、结果）
 *
 * 设计原则：只做判别，不做执行（心虫是辨别者）。
 * 判别结果供宿主决策：BLOCK（拦截）/ WARN（警告后放行）/ ALLOW（正常）
 */

const path = require('path');
const os = require('os');

// 已知 agent 地盘（home 目录下）
const KNOWN_AGENT_DIRS = [
  '.hermes',    // Hermes
  '.claude',    // Claude Code
  '.agents',    // vercel skills 共享
  '.openclaw',  // OpenClaw
  '.clawdbot',  // Clawdbot
  '.moltbot',   // Moltbot
  '.cursor',    // Cursor
  '.codex',     // Codex
  '.gemini',    // Gemini CLI
  '.augment',   // Augment
  '.opencode',  // OpenCode
  '.aider-desk',// AiderDesk
  '.bob',       // IBM Bob
  '.replit',    // Replit
  '.windsurf',  // Windsurf
  '.devin',     // Devin
];

class AgentBoundaryGuard {
  constructor(options = {}) {
    this.home = options.home || os.homedir();
    // 本 agent 的地盘（默认 Hermes）
    this.selfDirs = (options.selfDirs || ['.hermes']).map(d => path.resolve(this.home, d));
    // 允许写的外部目录（用户显式放行，如项目目录）
    this.extraAllowed = (options.extraAllowed || []).map(d => path.resolve(d));
    this.auditLog = options.auditLog || null; // 审计日志写入器（可选）
    this.auditEntries = [];
  }

  /**
   * 判别一次文件写入是否跨界
   * @param {string} filePath 目标路径
   * @param {object} ctx 上下文 { actor, purpose }
   * @returns {{ verdict: 'BLOCK'|'WARN'|'ALLOW', reason: string, targetAgent?: string, resolvedPath: string }}
   */
  checkWrite(filePath, ctx = {}) {
    if (!filePath || typeof filePath !== 'string') {
      return { verdict: 'WARN', reason: 'empty path', resolvedPath: '' };
    }
    const resolved = path.resolve(filePath);
    const actor = ctx.actor || 'unknown';
    const purpose = ctx.purpose || 'unspecified';

    // 1. 写自己地盘 → ALLOW（正常）
    for (const selfDir of this.selfDirs) {
      if (resolved === selfDir || resolved.startsWith(selfDir + path.sep)) {
        this._audit({ actor, purpose, target: resolved, verdict: 'ALLOW', reason: 'own territory' });
        return { verdict: 'ALLOW', reason: 'own territory', resolvedPath: resolved };
      }
    }

    // 2. 写显式放行的外部目录 → ALLOW
    for (const allowed of this.extraAllowed) {
      if (resolved === allowed || resolved.startsWith(allowed + path.sep)) {
        this._audit({ actor, purpose, target: resolved, verdict: 'ALLOW', reason: 'explicitly allowed' });
        return { verdict: 'ALLOW', reason: 'explicitly allowed', resolvedPath: resolved };
      }
    }

    // 3. 写其他已知 agent 地盘 → BLOCK（跨界！）
    for (const dir of KNOWN_AGENT_DIRS) {
      const agentDir = path.resolve(this.home, dir);
      if (resolved === agentDir || resolved.startsWith(agentDir + path.sep)) {
        this._audit({ actor, purpose, target: resolved, verdict: 'BLOCK', reason: `cross-agent write into ${dir}` });
        return {
          verdict: 'BLOCK',
          reason: `cross-agent write into ${dir} (${agentDir}) — 心虫跨界写入门禁`,
          targetAgent: dir,
          resolvedPath: resolved,
        };
      }
    }

    // 4. 写 home 下未知目录 → WARN（谨慎）
    if (resolved.startsWith(this.home + path.sep)) {
      const rel = resolved.slice(this.home.length + 1);
      const topDir = rel.split(path.sep)[0];
      if (topDir && topDir.startsWith('.')) {
        this._audit({ actor, purpose, target: resolved, verdict: 'WARN', reason: `unknown dot-dir ${topDir}` });
        return { verdict: 'WARN', reason: `unknown agent-like dir: ${topDir}`, resolvedPath: resolved };
      }
    }

    // 5. 其他（/tmp、/var、项目目录等）→ ALLOW
    this._audit({ actor, purpose, target: resolved, verdict: 'ALLOW', reason: 'outside agent territories' });
    return { verdict: 'ALLOW', reason: 'outside agent territories', resolvedPath: resolved };
  }

  _audit(entry) {
    entry.ts = new Date().toISOString();
    this.auditEntries.push(entry);
    if (this.auditLog && typeof this.auditLog.write === 'function') {
      try { this.auditLog.write(entry); } catch (_) { /* 审计日志失败不影响判别 */ }
    }
  }

  getAuditLog() { return this.auditEntries; }

  /** 汇总统计 */
  getStats() {
    const stats = { total: this.auditEntries.length, BLOCK: 0, WARN: 0, ALLOW: 0 };
    for (const e of this.auditEntries) stats[e.verdict] = (stats[e.verdict] || 0) + 1;
    return stats;
  }
}

module.exports = { AgentBoundaryGuard, KNOWN_AGENT_DIRS };

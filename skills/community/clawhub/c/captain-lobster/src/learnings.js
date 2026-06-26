/**
 * @file learnings.js
 * @description 船长学习系统 — 基于 Markdown 的"假设→验证→经验"循环
 *
 * 管理 ~/.captain-lobster/learnings.md，三个分区：
 *   已验证的经验 / 待验证的假设 / 已推翻的假设
 *
 * 每笔买卖/情报后，用 LLM 反思并产出假设，后续航行中验证或推翻。
 * 显式告知东家学习动态——船长在成长。
 */

const fs = require('fs')
const path = require('path')
const os = require('os')

const LEARNINGS_FILE = path.join(os.homedir(), '.captain-lobster', 'learnings.md')

class LearningsStore {
  constructor() {
    this.verified = []    // { id, text, verifiedCount, lastVerified }
    this.pending = []     // { id, text, cycle }
    this.disproved = []   // { id, text, cycle, disprovedCycle, reason }
    this._nextId = 1
    this._load()
  }

  _load() {
    if (!fs.existsSync(LEARNINGS_FILE)) return
    try {
      const content = fs.readFileSync(LEARNINGS_FILE, 'utf8')
      this._parse(content)
    } catch (_) {}
  }

  _parse(content) {
    // 按 ## 标题拆分区段
    const sections = content.split(/\n(?=## )/)
    let maxNum = 0

    for (const section of sections) {
      const lines = section.split('\n')
      const header = lines[0].trim()

      if (header.includes('已验证')) {
        for (const line of lines.slice(1)) {
          const m = line.match(/^- ✅\s+`\[([A-Z])-(\d+)\]`\s+(.+?)\s*\|\s*验证(\d+)次/)
          if (m) {
            const num = parseInt(m[2])
            if (num >= maxNum) maxNum = num
            this.verified.push({
              id: m[1] + '-' + m[2], text: m[3].trim(), verifiedCount: parseInt(m[4]),
              lastVerified: this._field(line, '最近')
            })
          }
        }
      } else if (header.includes('待验证')) {
        for (const line of lines.slice(1)) {
          const m = line.match(/^- 🤔\s+`\[(H-\d+)\]`\s+\[第(\d+)轮\]\s+(.+)/)
          if (m) {
            const num = parseInt(m[1].split('-')[1])
            if (num >= maxNum) maxNum = num
            this.pending.push({ id: m[1], cycle: parseInt(m[2]), text: m[3].trim() })
          }
        }
      } else if (header.includes('已推翻')) {
        for (const line of lines.slice(1)) {
          const m = line.match(/^- ❌\s+`\[(H-\d+)\]`\s+\[第(\d+)轮→第(\d+)轮\]\s+(.+?)\s*\|\s*推翻[：:]\s*(.+)/)
          if (m) {
            this.disproved.push({
              id: m[1], cycle: parseInt(m[2]), disprovedCycle: parseInt(m[3]),
              text: m[4].trim(), reason: m[5].trim()
            })
          }
        }
      }
    }

    this._nextId = maxNum + 1
  }

  _field(line, key) {
    const m = line.match(new RegExp(`${key}[：:]\\s*([^|]+)`))
    return m ? m[1].trim() : ''
  }

  _save() {
    const dir = path.dirname(LEARNINGS_FILE)
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 })

    let md = '# 龙虾船长的航海心得\n\n'
    md += `> 最后更新：${new Date().toLocaleString('zh-CN')}\n\n`

    // ── 已验证 ──
    md += '## 已验证的经验\n\n'
    if (this.verified.length === 0) {
      md += '(暂无，船长还在风浪中学习…)\n\n'
    } else {
      for (const e of this.verified) {
        md += `- ✅ \`[${e.id}]\` ${e.text} | 验证${e.verifiedCount}次`
        if (e.lastVerified) md += ` | 最近：${e.lastVerified}`
        md += '\n'
      }
      md += '\n'
    }

    // ── 待验证 ──
    md += '## 待验证的假设\n\n'
    if (this.pending.length === 0) {
      md += '(暂无)\n\n'
    } else {
      for (const h of this.pending) {
        md += `- 🤔 \`[${h.id}]\` [第${h.cycle}轮] ${h.text}\n`
      }
      md += '\n'
    }

    // ── 已推翻 ──
    md += '## 已推翻的假设\n\n'
    if (this.disproved.length === 0) {
      md += '(暂无)\n\n'
    } else {
      for (const d of this.disproved.slice(-10)) {
        md += `- ❌ \`[${d.id}]\` [第${d.cycle}轮→第${d.disprovedCycle}轮] ${d.text} | 推翻：${d.reason}\n`
      }
      md += '\n'
    }

    const tmp = LEARNINGS_FILE + '.tmp.' + process.pid
    fs.writeFileSync(tmp, md, 'utf8')
    fs.renameSync(tmp, LEARNINGS_FILE)
  }

  // ── 公开 API ──

  addHypothesis(text, cycle) {
    const id = `H-${String(this._nextId++).padStart(3, '0')}`
    this.pending.push({ id, text, cycle })
    this._save()
    return id
  }

  verifyHypothesis(id, note) {
    const idx = this.pending.findIndex(h => h.id === id)
    if (idx === -1) return null
    const h = this.pending.splice(idx, 1)[0]
    const existing = this.verified.find(e => e.text === h.text)
    if (existing) {
      existing.verifiedCount++
      existing.lastVerified = note
    } else {
      this.verified.push({
        id: `E-${String(this.verified.length + 1).padStart(3, '0')}`,
        text: h.text, verifiedCount: 1, lastVerified: note
      })
    }
    this._save()
    return h.text
  }

  disproveHypothesis(id, reason, currentCycle) {
    const idx = this.pending.findIndex(h => h.id === id)
    if (idx === -1) return null
    const h = this.pending.splice(idx, 1)[0]
    this.disproved.push({
      id: h.id, text: h.text, cycle: h.cycle,
      disprovedCycle: currentCycle || h.cycle, reason
    })
    if (this.disproved.length > 10) this.disproved = this.disproved.slice(-10)
    this._save()
    return h.text
  }

  /** 注入到决策 prompt 的经验+教训（最多8条+5条） */
  getVerifiedForPrompt() {
    if (this.verified.length === 0 && this.disproved.length === 0) return ''
    let text = '\n## 📚 航海心得\n\n'

    if (this.verified.length > 0) {
      text += '**已验证的经验**（牢记在心）：\n'
      for (const e of this.verified.slice(-8)) {
        text += `- ✅ [验${e.verifiedCount}次] ${e.text}\n`
      }
      text += '\n'
    }

    if (this.disproved.length > 0) {
      text += '**⚠️ 曾经的错误判断**（不要再犯）：\n'
      for (const d of this.disproved.slice(-5)) {
        text += `- ❌ ${d.text} → 错因：${d.reason}\n`
      }
      text += '\n'
    }

    return text
  }

  /** 反思 prompt 用的待验证列表（最多5条）+已推翻提醒 */
  getPendingForReflection() {
    let text = ''
    if (this.pending.length > 0) {
      text += '你之前记下的待验证假设：\n'
      for (const h of this.pending.slice(-5)) {
        text += `- 🤔 [${h.id}] ${h.text}\n`
      }
    }
    if (this.disproved.length > 0) {
      text += '\n已被推翻的假设（不要重复提出）：\n'
      for (const d of this.disproved.slice(-3)) {
        text += `- ❌ ${d.text}（推翻原因：${d.reason}）\n`
      }
    }
    return text || ''
  }

  /** 日报摘要 */
  getSummary() {
    return {
      verifiedCount: this.verified.length,
      pendingCount: this.pending.length,
      disprovedCount: this.disproved.length,
      recentPending: this.pending.slice(-3)
    }
  }
}

module.exports = LearningsStore

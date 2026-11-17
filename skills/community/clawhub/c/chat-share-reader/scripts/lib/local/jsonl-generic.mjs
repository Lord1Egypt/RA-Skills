// 通用 JSONL 会话解析：给「每行一个 JSON、字段名各站不同」的源用。
//
// 覆盖：Copilot CLI、Command Code、Kimi Code、Antigravity。
// 这几个源本机没有可验证的样本，所以不硬编码字段名，而是逐行做结构识别：
// 角色从 role / type / author / sender 里找，正文从 content / text / message 里找，
// 认不出角色的行跳过（工具调用、控制记录正该跳过）。
//
// 识别原则：只认能明确判成 user 或 assistant 的行，宁少不误。真跑出问题时，
// 用 --json 看抓到了几条，再去 references/sessions.md 补该源的具体字段。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const USER_WORDS = /^(user|human|userexplicit|user_message|usermessage|user_input)$/i;
const AI_WORDS = /^(assistant|model|ai|agent|bot|gemini|assistant_message|assistantmessage|planner_response|agent_message|agentmessage)$/i;

function roleOf(obj) {
  const cands = [obj.role, obj.type, obj.author, obj.sender, obj.from, obj.kind];
  for (const c of cands) {
    if (typeof c !== 'string') continue;
    const v = c.trim();
    if (USER_WORDS.test(v)) return 'user';
    if (AI_WORDS.test(v)) return 'ai';
  }
  return '';
}

function textOf(obj, depth = 0) {
  if (depth > 3 || !obj || typeof obj !== 'object') return '';
  for (const k of ['text', 'content', 'message', 'body', 'markdown']) {
    const v = obj[k];
    if (typeof v === 'string' && v.trim()) return v;
    if (Array.isArray(v)) {
      const parts = [];
      for (const p of v) {
        if (typeof p === 'string') parts.push(p);
        else if (p && typeof p === 'object') {
          if (typeof p.text === 'string') parts.push(p.text);
          else if (typeof p.content === 'string') parts.push(p.content);
        }
      }
      const joined = parts.join('\n\n').trim();
      if (joined) return joined;
    }
  }
  for (const k of ['data', 'payload', 'item', 'event']) {
    const v = obj[k];
    if (v && typeof v === 'object') {
      const t = textOf(v, depth + 1);
      if (t) return t;
    }
  }
  return '';
}

function timeOf(obj) {
  const c = obj.timestamp || obj.time || obj.created_at || obj.createdAt || obj.ts;
  if (!c) return '';
  if (typeof c === 'number') {
    return new Date(c > 1e12 ? c : c * 1000).toTimeString().slice(0, 5);
  }
  const s = String(c);
  const m = s.match(/T(\d{2}:\d{2})/);
  return m ? m[1] : '';
}

export function makeParser(sourceName) {
  return async function parse(file) {
    const raw = await readFile(file, 'utf8');
    const messages = [];
    let sessionTitle = '';
    let cwd = '';

    for (const line of raw.split('\n')) {
      const s = line.trim();
      if (!s) continue;
      let j;
      try {
        j = JSON.parse(s);
      } catch {
        continue;
      }
      // 会话级元信息（标题、工作目录）顺手捞一下
      if (!sessionTitle && typeof j.title === 'string') sessionTitle = j.title;
      if (!cwd && typeof j.cwd === 'string') cwd = j.cwd;

      const role = roleOf(j);
      if (!role) continue;
      const body = textOf(j).trim();
      if (!body) continue;
      messages.push({
        role: role === 'user' ? '用户' : sourceName,
        time: timeOf(j),
        body,
      });
    }

    return {
      title: sessionTitle || titleOf(messages) || path.basename(path.dirname(file)) || path.basename(file),
      messages,
      source: file,
      note: cwd ? '目录 ' + cwd : '',
      meta: { cwd },
    };
  };
}

function titleOf(messages) {
  const first = messages.find((m) => m.role === '用户');
  if (!first) return '';
  return first.body
    .replace(/[#*`>\n]/g, ' ')
    .replace(/[，。、？！；："'（）《》…—\s]+/g, ' ')
    .trim()
    .slice(0, 24)
    .trim();
}

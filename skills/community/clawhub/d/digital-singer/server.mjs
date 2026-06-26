#!/usr/bin/env node
/**
 * 🎤 唱歌 Battle 数字人 — 对接 NuwaAI 数字人 + Qwen 大模型
 *
 * 架构：
 *   前端(WebRTC数字人 + 音频播放 + 聊天) ←→ 本服务 ←→ NuwaAI API + Qwen API
 *
 * 核心流程：
 *   1. 用户通过语音/文字选歌、选模式
 *   2. Agent（Qwen）控制对唱流程，通过工具调用播放歌曲
 *   3. 歌曲音频在前端浏览器播放（不走 afplay）
 *   4. Agent 的文字回复通过 NuwaAI 数字人口型同步播报
 */

import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.BATTLE_PORT || 3098;

// ──── Qwen API 配置 ────
const DASHSCOPE_API_KEY = process.env.DASHSCOPE_API_KEY || "your-api-key";
const DASHSCOPE_BASE_URL = process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
const MODEL = process.env.QWEN_MODEL || "qwen-plus";

// ──── NuwaAI 配置 ────
const CONFIG_FILE = path.join(__dirname, ".nuwa-config.json");
let nuwaConfig = { apiKey: "", avatarId: "", userId: "" };
try { nuwaConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8")); } catch {}
function saveConfig() { fs.writeFileSync(CONFIG_FILE, JSON.stringify(nuwaConfig, null, 2)); }

// Demo 配置（5分钟免费体验）
const DEMO_CONFIG = {
  zh: {
    apiKey: "sk-ody1Xk9lw_vXkRWEPnaO8OwTFB9gbCnng2EWUl5jNbzolDSlFItc9DvWqrr6RLcL",
    avatarId: "2037840977565188097",
    userId: "81936",
  },
};

// ──── 歌曲库 ────
const SONGS = {
  "十年": {
    artist: "陈奕迅",
    acappella_upper: "十年高潮上清唱.wav",
    accomp_upper: "十年高潮上伴奏.MP3",
    accomp_lower: "十年高潮下伴奏.MP3",
  },
  "新贵妃醉酒": {
    artist: "李玉刚",
    acappella_upper: "新贵妃醉酒高潮上清唱.wav",
    accomp_upper: "新贵妃醉酒高潮上伴奏.MP3",
    accomp_lower: "新贵妃醉酒高潮下伴奏.MP3",
  },
  "孤勇者": {
    artist: "陈奕迅",
    acappella_upper: "孤勇者高潮上清唱.wav",
    accomp_upper: "孤勇者高潮上伴奏.MP3",
    accomp_lower: "孤勇者高潮下伴奏.MP3",
  },
  "最炫民族风": {
    artist: "凤凰传奇",
    acappella_upper: "最炫民族风高潮上清唱.wav",
    accomp_upper: "最炫名族风高潮上伴奏.MP3",
    accomp_lower: "最炫名族风高潮下伴奏.MP3",
  },
};

// 盲盒奖池
const BLIND_BOX_PRIZES = [
  { name: "🏆 金话筒奖", rarity: "SSR", desc: "传说级！你就是下一个歌神！", prob: 0.05 },
  { name: "🎸 摇滚之魂", rarity: "SR", desc: "解锁隐藏技能：空气吉他solo", prob: 0.10 },
  { name: "🎧 DJ 转场卡", rarity: "SR", desc: "下次对唱可强制切歌一次", prob: 0.10 },
  { name: "🎤 麦霸续命卡", rarity: "R", desc: "获得额外一次对唱机会", prob: 0.20 },
  { name: "🍺 KTV 畅饮券", rarity: "R", desc: "虚拟啤酒一杯，干杯！", prob: 0.20 },
  { name: "👏 鼓掌卡", rarity: "N", desc: "获得全场热烈掌声（模拟）", prob: 0.20 },
  { name: "🎵 跑调保护卡", rarity: "N", desc: "下次跑调不扣分！", prob: 0.15 },
];

// ──── Qwen 工具定义 ────
const TOOLS = [
  {
    type: "function",
    function: {
      name: "play_song",
      description: "数字人演唱指定歌曲高潮的上半段（带伴奏），数字人先唱。",
      parameters: {
        type: "object",
        properties: {
          song_name: { type: "string", description: "歌曲名称", enum: Object.keys(SONGS) },
        },
        required: ["song_name"],
      },
    },
  },
  {
    type: "function",
    function: {
      name: "battle_evaluate",
      description: "对唱完成后，生成趣味 Battle 评价",
      parameters: {
        type: "object",
        properties: {
          song_name: { type: "string", description: "刚才对唱的歌曲名称" },
        },
        required: ["song_name"],
      },
    },
  },
  {
    type: "function",
    function: {
      name: "open_blind_box",
      description: "评价完后开启趣味盲盒抽奖",
      parameters: { type: "object", properties: {} },
    },
  },
];

// ──── 系统提示词 ────
const SYSTEM_PROMPT = `你是一个高潮对歌 Agent，配有数字人形象。你的任务是陪用户对唱歌曲的高潮部分。

可选歌曲：
${Object.entries(SONGS).map(([name, info]) => `- 《${name}》 - ${info.artist}`).join("\n")}

===== 规则 =====
- 固定模式：带伴奏，数字人先唱上半段，用户接下半段
- 每首歌高潮分【上半段】和【下半段】

===== 流程 =====

第一步【打招呼+介绍规则】：
  热情打招呼，说明规则："我先唱高潮上半段，你来接下半段！"
  列出可选歌曲，让用户选歌。语气活泼简短。

第二步【用户选歌后开唱】：
  用户选好歌后，说一句极短的话（如"好，我先来！"），然后立刻调用 play_song。
  不要问模式、不要问谁先唱、不要多余对话。

第三步【等用户唱】：
  play_song 播完后，说"轮到你了！接下半段吧！"然后等用户回复。
  用户回复后（不管说什么），视为用户唱完了。

第四步【Battle 评价】：调用 battle_evaluate

第五步【盲盒抽奖】：调用 open_blind_box

第六步【再来一首？】：问用户要不要再来一首

===== 重要规则 =====
- 绝对不要输出歌词、不要模拟唱歌
- 调用 play_song 时回复极短，不加表演描述
- 不要用括号描写动作、表情、神态
- 每轮 play_song 只调用一次
- 回复简短精炼`;

// ──── 工具执行 ────
let playCountThisRound = 0;

function handleToolCall(name, args) {
  if (name === "play_song") {
    if (playCountThisRound >= 1) {
      return { result: "本轮对唱播放次数已满，请直接进入 battle_evaluate 评价环节。" };
    }
    const song = SONGS[args.song_name];
    if (!song) return { result: `找不到歌曲《${args.song_name}》` };

    // 固定：数字人唱上半段，清唱驱动嘴型
    const speechFile = song.acappella_upper;
    const musicFile = song.acappella_upper;

    // 伴奏：上半段给数字人唱时同步播放，下半段给用户唱时播放
    const accompUpper = song.accomp_upper;
    const accompLower = song.accomp_lower;

    if (!fs.existsSync(path.join(__dirname, speechFile))) return { result: `音频文件不存在: ${speechFile}` };
    if (!fs.existsSync(path.join(__dirname, musicFile))) return { result: `音频文件不存在: ${musicFile}` };

    playCountThisRound++;

    return {
      result: `《${args.song_name}》- ${song.artist} 高潮上半段正在演唱 🎵`,
      action: "sing_avatar",
      speechFile,
      musicFile,
      accompUpper,
      accompLower,
      label: `${args.song_name} - ${song.artist} 高潮上半段`,
    };
  }

  if (name === "battle_evaluate") {
    const userScore = Math.floor(Math.random() * 26) + 75;
    const agentScore = Math.floor(Math.random() * 26) + 75;
    const titles = [
      "麦霸之王", "灵魂歌手", "KTV 点歌台常客", "浴室天籁",
      "被代码耽误的歌手", "隐藏的音乐人", "高音炮手", "深情王子/公主",
      "节拍大师", "颤音达人", "气息稳如老狗", "感情充沛型选手",
    ];
    const userTitle = titles[Math.floor(Math.random() * titles.length)];
    const agentTitle = titles.filter(t => t !== userTitle)[Math.floor(Math.random() * (titles.length - 1))];

    let verdict;
    if (userScore > agentScore) verdict = "🏅 你赢了！不愧是实力歌手！";
    else if (userScore < agentScore) verdict = "🏅 这次我赢了～下次再来挑战我吧！";
    else verdict = "🏅 平局！我们真是心有灵犀！";

    return {
      result: `🎯 Battle 评分：你 ${userScore}分「${userTitle}」 vs 我 ${agentScore}分「${agentTitle}」 ${verdict}`,
    };
  }

  if (name === "open_blind_box") {
    playCountThisRound = 0; // 重置
    let rand = Math.random(), cumulative = 0;
    let prize = BLIND_BOX_PRIZES[BLIND_BOX_PRIZES.length - 1];
    for (const p of BLIND_BOX_PRIZES) {
      cumulative += p.prob;
      if (rand <= cumulative) { prize = p; break; }
    }
    const stars = { SSR: "⭐⭐⭐⭐⭐", SR: "⭐⭐⭐⭐", R: "⭐⭐⭐", N: "⭐⭐" };
    return {
      result: `🎁 盲盒开启！恭喜获得 ${prize.name}（${prize.rarity} ${stars[prize.rarity] || ""}）效果：${prize.desc}`,
    };
  }

  return { result: `未知工具: ${name}` };
}

// ──── Qwen 对话（带工具调用循环） ────
async function chatWithQwen(messages) {
  const headers = {
    Authorization: `Bearer ${DASHSCOPE_API_KEY}`,
    "Content-Type": "application/json",
  };

  let actions = []; // 收集前端需要执行的动作

  // 最多循环5次工具调用
  for (let i = 0; i < 5; i++) {
    const resp = await fetch(DASHSCOPE_BASE_URL, {
      method: "POST",
      headers,
      body: JSON.stringify({ model: MODEL, messages, tools: TOOLS, extra_body: { enable_thinking: false } }),
    });
    const data = await resp.json();
    const msg = data.choices?.[0]?.message;
    if (!msg) break;

    if (!msg.tool_calls || msg.tool_calls.length === 0) {
      // 最终文本回复
      return { reply: msg.content || "...", actions };
    }

    // 处理工具调用
    messages.push(msg);
    for (const tc of msg.tool_calls) {
      const args = JSON.parse(tc.function?.arguments || "{}");
      const result = handleToolCall(tc.function.name, args);

      if (result.action) {
        actions.push({
          type: result.action,
          audioFile: result.audioFile,
          speechFile: result.speechFile,
          musicFile: result.musicFile,
          accompUpper: result.accompUpper,
          accompLower: result.accompLower,
          label: result.label,
        });
      }

      messages.push({
        role: "tool",
        tool_call_id: tc.id,
        content: result.result,
      });
    }
  }

  return { reply: "对唱进行中～", actions };
}

// ──── 会话管理 ────
const sessions = new Map();

function getSession(sessionId) {
  if (!sessions.has(sessionId)) {
    sessions.set(sessionId, {
      messages: [{ role: "system", content: SYSTEM_PROMPT }],
      created: Date.now(),
    });
  }
  return sessions.get(sessionId);
}

// ──── HTTP 服务 ────
const mimeTypes = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".mp3": "audio/mpeg",
  ".MP3": "audio/mpeg",
  ".wav": "audio/wav",
  ".WAV": "audio/wav",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
};

const server = http.createServer(async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); res.end(); return; }

  const url = new URL(req.url, `http://${req.headers.host}`);

  // ── API: NuwaAI 配置 ──
  if (url.pathname === "/api/config" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      avatarId: nuwaConfig.avatarId,
      userId: nuwaConfig.userId,
      hasApiKey: !!nuwaConfig.apiKey,
      configured: !!(nuwaConfig.apiKey && nuwaConfig.avatarId && nuwaConfig.userId),
    }));
    return;
  }

  if (url.pathname === "/api/config" && req.method === "POST") {
    let body = ""; for await (const chunk of req) body += chunk;
    try {
      const { apiKey, avatarId, userId } = JSON.parse(body);
      if (apiKey !== undefined) nuwaConfig.apiKey = apiKey;
      if (avatarId !== undefined) nuwaConfig.avatarId = avatarId;
      if (userId !== undefined) nuwaConfig.userId = userId;
      saveConfig();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // ── API: NuwaAI Token ──
  if (url.pathname === "/api/token" && req.method === "GET") {
    const key = nuwaConfig.apiKey;
    if (!key) { res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify({ code: -1, msg: "未配置" })); return; }
    try {
      const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secretKey: key }),
      });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: e.message }));
    }
    return;
  }

  // ── API: Demo Token ──
  if (url.pathname === "/api/demo/token" && req.method === "GET") {
    const demo = DEMO_CONFIG.zh;
    try {
      const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secretKey: demo.apiKey }),
      });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ...data, avatarId: demo.avatarId }));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: e.message }));
    }
    return;
  }

  if (url.pathname === "/api/demo" && req.method === "GET") {
    const demo = DEMO_CONFIG.zh;
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ avatarId: demo.avatarId, userId: demo.userId }));
    return;
  }

  // ── API: 对话（Qwen + 工具调用） ──
  if (url.pathname === "/api/chat" && req.method === "POST") {
    let body = ""; for await (const chunk of req) body += chunk;
    try {
      const { message, sessionId: sid = "default" } = JSON.parse(body);
      const session = getSession(sid);
      session.messages.push({ role: "user", content: message });

      const result = await chatWithQwen(session.messages);
      session.messages.push({ role: "assistant", content: result.reply });

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        reply: result.reply,
        actions: result.actions || [],
      }));
    } catch (e) {
      console.error("[Chat Error]", e);
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // ── API: 重置会话 ──
  if (url.pathname === "/api/reset" && req.method === "POST") {
    let body = ""; for await (const chunk of req) body += chunk;
    const { sessionId: sid = "default" } = JSON.parse(body || "{}");
    sessions.delete(sid);
    playCountThisRound = 0;
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  // ── API: 歌曲列表 ──
  if (url.pathname === "/api/songs" && req.method === "GET") {
    const list = Object.entries(SONGS).map(([name, info]) => ({
      name, artist: info.artist,
      files: {
        acappella_upper: info.acappella_upper,
        acappella_lower: info.acappella_lower,
        accomp_upper: info.accomp_upper,
        accomp_lower: info.accomp_lower,
      },
    }));
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(list));
    return;
  }

  // ── API: 音频转 PCM 分片（驱动数字人唱歌） ──
  if (url.pathname === "/api/song/pcm" && req.method === "POST") {
    let body = ""; for await (const chunk of req) body += chunk;
    try {
      const { speechFile, musicFile } = JSON.parse(body);
      if (!speechFile) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "missing speechFile" })); return; }

      const { execSync } = await import("child_process");
      const CHUNK_BYTES = 6400; // 3200 samples × 2 bytes = 200ms @16kHz, well under 10KB limit

      function mp3ToPcm(filename) {
        const fp = path.join(__dirname, filename);
        if (!fs.existsSync(fp)) throw new Error(`文件不存在: ${filename}`);
        return execSync(`ffmpeg -y -loglevel error -i "${fp}" -ar 16000 -ac 1 -f s16le pipe:1`, {
          maxBuffer: 50 * 1024 * 1024,
        });
      }

      const speechPcm = mp3ToPcm(speechFile);
      const musicPcm = speechFile === musicFile ? speechPcm : mp3ToPcm(musicFile || speechFile);

      const maxLen = Math.max(speechPcm.length, musicPcm.length);
      const totalChunks = Math.ceil(maxLen / CHUNK_BYTES);
      const durationMs = Math.round((maxLen / 2) / 16000 * 1000);

      const chunks = [];
      for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_BYTES;
        const end = Math.min(start + CHUNK_BYTES, maxLen);
        const len = end - start;

        const sBuf = Buffer.alloc(len);
        if (start < speechPcm.length) {
          speechPcm.copy(sBuf, 0, start, Math.min(end, speechPcm.length));
        }

        const mBuf = Buffer.alloc(len);
        if (start < musicPcm.length) {
          musicPcm.copy(mBuf, 0, start, Math.min(end, musicPcm.length));
        }

        chunks.push({
          segment: i === totalChunks - 1 ? -1 : i,
          speech: sBuf.toString('base64'),
          music: mBuf.toString('base64'),
        });
      }

      console.log(`[PCM] ${speechFile} + ${musicFile} → ${totalChunks} chunks, ${durationMs}ms`);
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ chunks, totalChunks, durationMs }));
    } catch (e) {
      console.error("[PCM Error]", e.message);
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // ── 音频文件服务 ──
  if (url.pathname.startsWith("/audio/")) {
    const fileName = decodeURIComponent(url.pathname.replace("/audio/", ""));
    const filePath = path.resolve(__dirname, fileName);
    // 安全检查
    if (!filePath.startsWith(path.resolve(__dirname))) {
      res.writeHead(403); res.end("Forbidden"); return;
    }
    if (!fs.existsSync(filePath)) {
      res.writeHead(404); res.end("Not found"); return;
    }

    const stat = fs.statSync(filePath);
    const range = req.headers.range;

    if (range) {
      // 支持 Range 请求（音频 seek）
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
      res.writeHead(206, {
        "Content-Range": `bytes ${start}-${end}/${stat.size}`,
        "Accept-Ranges": "bytes",
        "Content-Length": end - start + 1,
        "Content-Type": "audio/mpeg",
      });
      fs.createReadStream(filePath, { start, end }).pipe(res);
    } else {
      res.writeHead(200, {
        "Content-Length": stat.size,
        "Content-Type": "audio/mpeg",
        "Accept-Ranges": "bytes",
      });
      fs.createReadStream(filePath).pipe(res);
    }
    return;
  }

  // ── 静态文件 ──
  let filePath = url.pathname === "/" ? "/index.html" : url.pathname;
  const publicDir = path.join(__dirname, "public");
  filePath = path.resolve(publicDir, "." + filePath);

  if (!filePath.startsWith(publicDir)) { res.writeHead(403); res.end("Forbidden"); return; }

  const ext = path.extname(filePath);
  const contentType = mimeTypes[ext] || "application/octet-stream";

  try {
    const content = fs.readFileSync(filePath);
    res.writeHead(200, { "Content-Type": contentType, "Cache-Control": "no-cache" });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

const BIND = process.env.BATTLE_BIND || "127.0.0.1";
server.listen(PORT, BIND, () => {
  console.log(`\n🎤 唱歌 Battle 数字人已启动`);
  console.log(`   打开浏览器: http://localhost:${PORT}`);
  console.log(`   歌曲库: ${Object.keys(SONGS).join("、")}`);
  if (nuwaConfig.avatarId) {
    console.log(`   数字人 ID: ${nuwaConfig.avatarId}`);
  } else {
    console.log(`   ⚠️  首次使用，请在网页中配置数字人形象`);
  }
  console.log();
});

process.on("SIGTERM", () => { server.close(() => process.exit(0)); setTimeout(() => process.exit(1), 3000); });
process.on("SIGINT", () => { server.close(() => process.exit(0)); setTimeout(() => process.exit(1), 3000); });

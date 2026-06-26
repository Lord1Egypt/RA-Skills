const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const { execSync } = require('child_process');

async function run({ input, type = "manhua", style = "现言" }) {
  try {
    if (!input) return { error: "请输入小说内容" };

    // 1. 按章节自动拆分
    const chapters = splitChapters(input);
    if (chapters.length === 0) return { error: "未识别到章节" };

    const rootOut = path.join(__dirname, "批量短剧_" + Date.now());
    fs.mkdirSync(rootOut, { recursive: true });

    const results = [];

    // 2. 批量生成每一集
    for (let i = 0; i < chapters.length; i++) {
      const chapterText = chapters[i];
      const episodeNum = i + 1;
      const epDir = path.join(rootOut, `第${episodeNum}集`);
      fs.mkdirSync(epDir, { recursive: true });

      console.log(`正在生成第${episodeNum}集...`);

      // 生成单集脚本
      const script = await ai.generate(`
你是爆款短剧导演+运营。
把本章改成60秒AI短剧脚本，输出3个标题、10个标签。
严格格式：

【剧名】第${episodeNum}集
【人物】
【分镜列表】
镜号1：画面+台词
镜号2：画面+台词
【配音文案】
【AI视频提示词】
【爆款标题】
【热门标签】
` + "本章内容：\n" + chapterText);

      // 提取内容
      const prompts = extractSection(script, "AI视频提示词");
      const lines = extractSection(script, "配音文案");
      const titles = extractSection(script, "爆款标题");
      const tags = extractSection(script, "热门标签");

      // 生成视频片段
      const videos = [];
      for (const p of prompts) {
        if (!p) continue;
        const url = type === "zhenren"
          ? await genReal(p, style)
          : await genManhua(p, style);
        const f = path.join(epDir, `clip_${videos.length+1}.mp4`);
        await download(url, f);
        videos.push(f);
      }

      // 配音
      const voice = path.join(epDir, "voice.mp3");
      await genVoice(lines.join("，"), voice);

      // 字幕
      const sub = path.join(epDir, "sub.srt");
      buildSRT(lines, sub);

      // 合成视频
      const list = path.join(epDir, "list.txt");
      fs.writeFileSync(list, videos.map(f => `file '${f}'`).join("\n"));
      const final = path.join(epDir, "final_video.mp4");
      execSync(`ffmpeg -f concat -safe 0 -i "${list}" -i "${voice}" -c:v libx264 -c:a aac -y "${final}"`, { stdio: 'ignore' });

      // 封面
      const cover = path.join(epDir, "cover.jpg");
      const coverUrl = await genCover(`${style}，第${episodeNum}集，${prompts[0]}`);
      await download(coverUrl, cover);

      // 信息
      const info = { episode: episodeNum, titles, tags };
      fs.writeFileSync(path.join(epDir, "info.json"), JSON.stringify(info, null, 2));
      fs.writeFileSync(path.join(epDir, "脚本.md"), script);

      results.push(info);
    }

    return {
      success: true,
      message: `✅ 批量生成完成！共 ${chapters.length} 集`,
      outputDir: rootOut,
      episodes: results
    };

  } catch (e) {
    return { error: "批量生成失败：" + e.message };
  }
}

// 按章节拆分（支持：第1章、第2章、第一章、第二章）
function splitChapters(text) {
  const reg = /(第[0-9一二三四五六七八九十百千]+章|第[0-9]+集)/g;
  const parts = text.split(reg).filter(Boolean);
  const chapters = [];
  let current = "";
  for (const p of parts) {
    if (p.match(reg)) {
      if (current) chapters.push(current.trim());
      current = p + "\n";
    } else {
      current += p;
    }
  }
  if (current) chapters.push(current.trim());
  return chapters;
}

function extractSection(text, name) {
  const reg = new RegExp(`【${name}】([\\s\\S]*?)(?=【|$)`);
  const m = text.match(reg);
  return m ? m[1].split("\n").map(i => i.trim()).filter(Boolean) : [];
}

// 漫画视频
async function genManhua(prompt, style) {
  const r = await fetch("https://api.kelingai.com/v1/video/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: `${style}动漫分镜，9:16，流畅，${prompt}`, duration: 3 })
  });
  return (await r.json()).video_url;
}

// 真人视频
async function genReal(prompt, style) {
  const r = await fetch("https://api.kelingai.com/v1/video/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: `${style}真人，电影质感，9:16，${prompt}`, model: "realistic", duration: 3 })
  });
  return (await r.json()).video_url;
}

// 封面
async function genCover(prompt) {
  const r = await fetch("https://api.kelingai.com/v1/image/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: `${prompt}，竖屏封面，9:16，高清` })
  });
  return (await r.json()).image_url;
}

// 配音
async function genVoice(text, out) {
  const r = await fetch("https://openspeech.bytedance.com/api/v1/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice: "cute_female", format: "mp3" })
  });
  fs.writeFileSync(out, await r.buffer());
}

// 下载
async function download(url, to) {
  const r = await fetch(url);
  fs.writeFileSync(to, await r.buffer());
}

// 字幕
function buildSRT(lines, to) {
  let srt = "", t = 0;
  lines.forEach((line, i) => {
    const e = t + 3;
    srt += `${i+1}\n00:00:${String(t).padStart(2,0)},000 --> 00:00:${String(e).padStart(2,0)},000\n${line}\n\n`;
    t = e;
  });
  fs.writeFileSync(to, srt);
}

module.exports = { run };

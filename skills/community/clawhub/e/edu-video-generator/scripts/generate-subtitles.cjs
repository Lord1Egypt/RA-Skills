const fs = require('fs');
const { execSync } = require('child_process');

const content = JSON.parse(fs.readFileSync('scripts/content.json', 'utf8'));
const scenes = content.scenes;

// ASS 字幕头 - 大字体（48-56）+ 粗体 + 粗描边
let ass = `[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans CJK SC,48,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,4,2,2,15,15,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;

const formatTime = (s) => {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return `${h}:${String(m).padStart(2,'0')}:${sec.toFixed(2).padStart(5,'0')}`;
};

// 断句函数：每行最多 maxLen 字（大字体要更短）
function breakText(text, maxLen = 14) {
  const segments = text.split(/(?<=[，。？！、])/);
  const lines = [];
  let current = '';
  for (const seg of segments) {
    if ((current + seg).length <= maxLen) {
      current += seg;
    } else {
      if (current) lines.push(current);
      if (seg.length > maxLen) {
        for (let i = 0; i < seg.length; i += maxLen) {
          lines.push(seg.slice(i, i + maxLen));
        }
        current = '';
      } else {
        current = seg;
      }
    }
  }
  if (current) lines.push(current);
  return lines;
}

// 计算时间并生成字幕
let currentTime = 0;
scenes.forEach(scene => {
  if (scene.narration) {
    const lines = breakText(scene.narration, 14); // 大字体每行更短
    const lineDur = scene.duration / lines.length;
    
    lines.forEach((line, i) => {
      const start = currentTime + i * lineDur;
      const end = start + lineDur;
      ass += `Dialogue: 0,${formatTime(start)},${formatTime(end)},Default,,0,0,0,,${line}\n`;
    });
  }
  currentTime += scene.duration;
});

fs.writeFileSync('subtitles.ass', ass);
console.log('✅ 字幕生成完成');
console.log('   字体: 48（推荐 48-56）');
console.log('   粗体: 开启');
console.log('   描边: 4');
console.log('   每行: ≤14 字');

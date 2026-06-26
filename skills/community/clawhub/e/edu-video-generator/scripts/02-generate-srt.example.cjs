/**
 * 02-generate-srt.cjs - 字幕生成脚本示例
 * 
 * 功能：
 * 1. 从 audio-metadata.json 读取实际配音时长
 * 2. 从 content.json 读取旁白文本
 * 3. 智能拆分长句（每行≤10字）
 * 4. 按字数比例分配时间
 * 5. 生成标准 SRT 字幕文件
 */

const fs = require('fs');
const path = require('path');

// 读取配置
const config = require('./config.js');
const metadata = require('./audio-metadata.json');
const content = require('./content.json');

// 配置
const MAX_CHARS_PER_LINE = config.subtitle.maxCharsPerLine; // 从 config.js 读取

/**
 * 智能拆分文本
 * 优先在标点处切分，超长时强制切分
 */
function splitText(text, maxChars) {
  if (text.length <= maxChars) {
    return [text];
  }
  
  const parts = [];
  let current = '';
  
  // 优先在标点处切分
  for (const char of text) {
    current += char;
    // 遇到标点且长度够一半就切分
    if (/[，。！？、；：,.!?;]/u.test(char) && current.length >= Math.floor(maxChars * 0.6)) {
      parts.push(current.trim());
      current = '';
    }
  }
  
  if (current.trim()) {
    parts.push(current.trim());
  }
  
  // 检查是否有超长的部分，强制切分
  const result = [];
  for (const part of parts) {
    if (part.length <= maxChars) {
      result.push(part);
    } else {
      // 强制按字数切分
      for (let i = 0; i < part.length; i += maxChars) {
        result.push(part.slice(i, i + maxChars));
      }
    }
  }
  
  return result;
}

/**
 * 格式化时间为 SRT 格式
 */
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.round((seconds % 1) * 1000);
  
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

/**
 * 生成 SRT 字幕
 */
function generateSRT() {
  console.log(`📝 生成 SRT 字幕（每行最多 ${MAX_CHARS_PER_LINE} 字）...`);
  
  let srtContent = '';
  let currentTime = 0;
  let index = 1;
  
  for (let i = 0; i < metadata.length; i++) {
    const scene = metadata[i];
    const narration = scene.narration;
    const duration = scene.duration;
    
    // 拆分文本
    const lines = splitText(narration, MAX_CHARS_PER_LINE);
    
    // 按字数比例分配时间
    const totalChars = lines.reduce((sum, l) => sum + l.length, 0);
    let lineStartTime = currentTime;
    
    for (const line of lines) {
      const lineDuration = (line.length / totalChars) * duration;
      const lineEndTime = lineStartTime + lineDuration;
      
      srtContent += `${index}\n`;
      srtContent += `${formatTime(lineStartTime)} --> ${formatTime(lineEndTime)}\n`;
      srtContent += `${line}\n\n`;
      
      lineStartTime = lineEndTime;
      index++;
    }
    
    currentTime += duration;
  }
  
  // 写入文件
  const outputPath = path.join(__dirname, '..', 'subtitles.srt');
  fs.writeFileSync(outputPath, srtContent, 'utf8');
  
  console.log(`✅ 字幕生成完成！共 ${index - 1} 条`);
  console.log(`   输出: ${outputPath}`);
}

// 执行
generateSRT();

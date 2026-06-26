/**
 * 飞书 AI 视频剪辑 Skill
 * 
 * 核心功能：
 * 1. 静音删除
 * 2. 视频裁剪
 * 3. 字幕生成
 * 4. 音频提取
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';

const execAsync = promisify(exec);

// 配置
const CONFIG_PATH = path.join(__dirname, '../config.json');
const PYTHON_SCRIPT = path.join(__dirname, 'video_processor.py');

interface VideoEditorConfig {
  whisper_model: string;
  output_dir: string;
  auto_upload: boolean;
  silent_threshold: number;
  min_silent_duration: number;
}

/**
 * 主入口
 */
export async function main(command: string, args: any[], context?: any) {
  const cmd = command.toLowerCase();
  
  // 加载配置
  const config = await loadConfig();
  
  if (cmd === 'trim_silence' || cmd === '删除静音' || cmd === '剪辑') {
    return await handleTrimSilence(args, config, context);
  }
  
  if (cmd === 'crop' || cmd === '裁剪') {
    return await handleCrop(args, config, context);
  }
  
  if (cmd === 'subtitle' || cmd === '字幕' || cmd === '生成字幕') {
    return await handleSubtitle(args, config, context);
  }
  
  if (cmd === 'extract_audio' || cmd === '提取音频') {
    return await handleExtractAudio(args, config, context);
  }
  
  if (cmd === 'help' || cmd === '帮助') {
    return showHelp();
  }
  
  return {
    message: `❓ 未知命令：${command}\n\n运行 \`/video_editor help\` 查看可用命令`
  };
}

/**
 * 删除静音
 */
async function handleTrimSilence(args: any[], config: VideoEditorConfig, context?: any) {
  const videoPath = args[0];
  
  if (!videoPath) {
    return {
      message: '❌ 请提供视频文件路径或上传视频'
    };
  }
  
  console.log(`🎬 开始处理视频：${videoPath}`);
  
  try {
    // 调用 Python 脚本
    const result = await runPythonScript('trim_silence', videoPath, config);
    
    return {
      message: `✅ ${result.message}`,
      data: result
    };
  } catch (error: any) {
    return {
      message: `❌ 处理失败：${error.message}`,
      error: error.message
    };
  }
}

/**
 * 裁剪视频
 */
async function handleCrop(args: any[], config: VideoEditorConfig, context?: any) {
  const [videoPath, startTime, endTime] = args;
  
  if (!videoPath || !startTime || !endTime) {
    return {
      message: '❌ 请提供视频路径和起止时间\n\n示例：`crop video.mp4 00:01:00 00:02:30`'
    };
  }
  
  console.log(`✂️ 裁剪视频：${startTime} - ${endTime}`);
  
  try {
    const result = await runPythonScript('crop', videoPath, config, ['--start', startTime, '--end', endTime]);
    
    return {
      message: `✅ ${result.message}`,
      data: result
    };
  } catch (error: any) {
    return {
      message: `❌ 裁剪失败：${error.message}`,
      error: error.message
    };
  }
}

/**
 * 生成字幕
 */
async function handleSubtitle(args: any[], config: VideoEditorConfig, context?: any) {
  const videoPath = args[0];
  
  if (!videoPath) {
    return {
      message: '❌ 请提供视频文件路径'
    };
  }
  
  console.log(`🎤 生成字幕：${videoPath}`);
  
  try {
    const result = await runPythonScript('subtitle', videoPath, config);
    
    return {
      message: `✅ ${result.message}`,
      data: result
    };
  } catch (error: any) {
    return {
      message: `❌ 生成失败：${error.message}\n\n提示：首次运行需要下载 Whisper 模型，请耐心等待。`,
      error: error.message
    };
  }
}

/**
 * 提取音频
 */
async function handleExtractAudio(args: any[], config: VideoEditorConfig, context?: any) {
  const videoPath = args[0];
  
  if (!videoPath) {
    return {
      message: '❌ 请提供视频文件路径'
    };
  }
  
  console.log(`🎵 提取音频：${videoPath}`);
  
  try {
    const result = await runPythonScript('extract_audio', videoPath, config);
    
    return {
      message: `✅ ${result.message}`,
      data: result
    };
  } catch (error: any) {
    return {
      message: `❌ 提取失败：${error.message}`,
      error: error.message
    };
  }
}

/**
 * 显示帮助
 */
function showHelp() {
  return {
    message: `⚡ **AI 视频剪辑 Skill - 帮助**

**可用命令：**

\`/video_editor trim_silence <视频>\` - 删除视频中的静音片段
\`/video_editor crop <视频> <开始> <结束>\` - 按时间裁剪视频
\`/video_editor subtitle <视频>\` - 生成字幕文件
\`/video_editor extract_audio <视频>\` - 提取音频
\`/video_editor help\` - 显示此帮助信息

**使用示例：**

1. **删除静音**
   \`\`\`
   /video_editor trim_silence ~/Videos/meeting.mp4
   \`\`\`

2. **裁剪视频**
   \`\`\`
   /video_editor crop video.mp4 00:01:30 00:02:45
   \`\`\`

3. **生成字幕**
   \`\`\`
   /video_editor subtitle lecture.mp4
   \`\`\`

4. **提取音频**
   \`\`\`
   /video_editor extract_audio music_video.mp4
   \`\`\`

---

**系统要求：**

- ✅ FFmpeg (apt install ffmpeg / brew install ffmpeg)
- ✅ Python 3.8+
- ✅ Python 依赖：pip install -r requirements.txt

---

详细文档：SKILL.md`
  };
}

/**
 * 运行 Python 脚本
 */
async function runPythonScript(command: string, videoPath: string, 
                               config: VideoEditorConfig, extraArgs: string[] = []) {
  const configPath = await saveConfigTemp(config);
  
  const args = [
    PYTHON_SCRIPT,
    command,
    videoPath,
    '--config', configPath,
    ...extraArgs
  ];
  
  const cmd = `python3 ${args.join(' ')}`;
  
  console.log(`执行：${cmd}`);
  
  try {
    const { stdout, stderr } = await execAsync(cmd, {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024 // 10MB
    });
    
    // 解析 JSON 输出
    const lines = stdout.trim().split('\n');
    const jsonLine = lines.find(line => line.startsWith('{'));
    
    if (jsonLine) {
      return JSON.parse(jsonLine);
    }
    
    return {
      success: true,
      message: stdout,
      stderr
    };
  } catch (error: any) {
    throw new Error(error.stderr || error.message);
  }
}

/**
 * 加载配置
 */
async function loadConfig(): Promise<VideoEditorConfig> {
  const defaultConfig: VideoEditorConfig = {
    whisper_model: 'base',
    output_dir: '~/Videos/edited',
    auto_upload: true,
    silent_threshold: -50,
    min_silent_duration: 1.0
  };
  
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
      return { ...defaultConfig, ...JSON.parse(content) };
    }
  } catch (error) {
    console.error('加载配置失败:', error);
  }
  
  return defaultConfig;
}

/**
 * 保存临时配置文件
 */
async function saveConfigTemp(config: VideoEditorConfig): Promise<string> {
  const tempPath = path.join('/tmp', `video_editor_config_${Date.now()}.json`);
  fs.writeFileSync(tempPath, JSON.stringify(config, null, 2));
  return tempPath;
}

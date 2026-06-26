/**
 * OpenClaw Qwen ASR Skill 主入口
 */

const express = require('express');
const multer = require('multer');
const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const dialectMap = require('./dialect-map');
const HOST = process.env.HOST || '0.0.0.0';

// 配置文件上传
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB
  },
  fileFilter: function (req, file, cb) {
    const allowedTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/flac', 'audio/x-wav', 'audio/wave'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('不支持的音频格式，仅支持wav、mp3、flac格式'), false);
    }
  }
});

// 中间件
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// 模型配置
const modelConfig = {
  modelName: process.env.MODEL_NAME || 'Qwen/Qwen3-ASR-0.6B',
  device: process.env.DEVICE || 'cpu',
  dtype: process.env.DTYPE || 'float32',
  maxNewTokens: parseInt(process.env.MAX_NEW_TOKENS) || 1024,
  batchSize: parseInt(process.env.BATCH_SIZE) || 4,
  enableForcedAligner: process.env.ENABLE_FORCED_ALIGNER === 'true',
  forcedAlignerModel: process.env.FORCED_ALIGNER_MODEL || 'Qwen/Qwen3-ForcedAligner-0.6B',
  cacheDir: process.env.CACHE_DIR || './models',
};

// 健康检查接口
app.get('/health', (req, res) => {
  res.json({
    success: true,
    data: {
      status: 'running',
      skill: 'qwen-asr-skill',
      version: require('./package.json').version,
      model: modelConfig.modelName,
      device: modelConfig.device,
    }
  });
});

// Skill 信息接口
app.get('/info', (req, res) => {
  const pkg = require('./package.json');
  res.json({
    success: true,
    data: {
      ...pkg.openclaw,
      supportedLanguages: [
        'Chinese', 'English', 'Cantonese', 'Arabic', 'German', 'French', 'Spanish',
        'Portuguese', 'Indonesian', 'Italian', 'Korean', 'Russian', 'Thai', 'Vietnamese',
        'Japanese', 'Turkish', 'Hindi', 'Malay', 'Dutch', 'Swedish', 'Danish', 'Finnish',
        'Polish', 'Czech', 'Filipino', 'Persian', 'Greek', 'Hungarian', 'Macedonian', 'Romanian'
      ],
      supportedDialects: [
        'Anhui', 'Dongbei', 'Fujian', 'Gansu', 'Guizhou', 'Hebei', 'Henan', 'Hubei',
        'Hunan', 'Jiangxi', 'Ningxia', 'Shandong', 'Shaanxi', 'Shanxi', 'Sichuan',
        'Tianjin', 'Yunnan', 'Zhejiang', 'Cantonese-HK', 'Cantonese-GD', 'Wu', 'Minnan'
      ]
    }
  });
});

// 音频转文字接口
app.post('/transcribe', upload.single('audio'), async (req, res) => {
  let audioPath = null;
  let cleanupFiles = [];
  
  try {
    const { language, format, timestamps, audio: audioBase64 } = req.body;
    
    // 标准化方言名称
    const normalizedLanguage = language ? dialectMap.normalize(language) : null;
    
    // 处理音频输入
    if (req.file) {
      // 上传的文件
      audioPath = req.file.path;
      cleanupFiles.push(audioPath);
    } else if (audioBase64) {
      // base64编码的音频
      if (typeof audioBase64 === 'string' && audioBase64.startsWith('data:audio')) {
        audioPath = audioBase64;
      } else {
        return res.status(400).json({
          success: false,
          error: '无效的base64音频数据'
        });
      }
    } else {
      return res.status(400).json({
        success: false,
        error: '缺少音频参数，请提供audio文件或base64数据'
      });
    }

    // 构建Python脚本参数
    const options = {
      mode: 'json',
      pythonPath: process.env.PYTHON_PATH || 'python3',
      scriptPath: __dirname,
      args: [
        audioPath,
        '--model', modelConfig.modelName,
        '--device', modelConfig.device,
        '--dtype', modelConfig.dtype,
      ],
    };

    if (normalizedLanguage) {
      options.args.push('--language', normalizedLanguage);
    }
    
    if (timestamps === 'true' || timestamps === true) {
      options.args.push('--timestamps');
    }

    // 执行Python脚本
    const results = await PythonShell.run('asr.py', options);
    const result = results[0];

    if (!result || !result.success) {
      throw new Error(result?.error || '转录失败');
    }

    res.json(result);

  } catch (error) {
    console.error('转录错误:', error);
    res.status(500).json({
      success: false,
      error: error.message || '内部服务器错误'
    });
  } finally {
    // 清理临时文件
    cleanupFiles.forEach(file => {
      if (fs.existsSync(file)) {
        fs.unlink(file, () => {});
      }
    });
  }
});

// 强制对齐接口
app.post('/align', upload.single('audio'), async (req, res) => {
  let audioPath = null;
  let cleanupFiles = [];
  
  try {
    const { text, language, audio: audioBase64 } = req.body;
    
    if (!text) {
      return res.status(400).json({
        success: false,
        error: '缺少text参数，用于强制对齐的文本是必需的'
      });
    }
    
    if (!language) {
      return res.status(400).json({
        success: false,
        error: '缺少language参数，强制对齐需要指定语言'
      });
    }
    
    // 标准化方言名称
    const normalizedLanguage = dialectMap.normalize(language);
    
    // 处理音频输入
    if (req.file) {
      audioPath = req.file.path;
      cleanupFiles.push(audioPath);
    } else if (audioBase64) {
      if (typeof audioBase64 === 'string' && audioBase64.startsWith('data:audio')) {
        audioPath = audioBase64;
      } else {
        return res.status(400).json({
          success: false,
          error: '无效的base64音频数据'
        });
      }
    } else {
      return res.status(400).json({
        success: false,
        error: '缺少音频参数，请提供audio文件或base64数据'
      });
    }

    // 构建Python脚本参数
    const options = {
      mode: 'json',
      pythonPath: process.env.PYTHON_PATH || 'python3',
      scriptPath: __dirname,
      args: [
        audioPath,
        '--model', modelConfig.modelName,
        '--device', modelConfig.device,
        '--dtype', modelConfig.dtype,
        '--language', normalizedLanguage,
        '--align-text', text,
      ],
    };

    // 执行Python脚本
    const results = await PythonShell.run('asr.py', options);
    const result = results[0];

    if (!result || !result.success) {
      throw new Error(result?.error || '对齐失败');
    }

    res.json(result);

  } catch (error) {
    console.error('对齐错误:', error);
    res.status(500).json({
      success: false,
      error: error.message || '内部服务器错误'
    });
  } finally {
    // 清理临时文件
    cleanupFiles.forEach(file => {
      if (fs.existsSync(file)) {
        fs.unlink(file, () => {});
      }
    });
  }
});

// OpenClaw Webhook 接口
app.post('/webhook', async (req, res) => {
  try {
    const { type, payload } = req.body;
    
    switch (type) {
      case 'audio.message':
        // 处理来自OpenClaw的语音消息
        const { audio, userId, sessionId, language } = payload;
        
        // 标准化方言名称
        const normalizedLanguage = language ? dialectMap.normalize(language) : null;
        
        // 调用转录接口
        const transcribeResult = await new Promise((resolve, reject) => {
          const options = {
            mode: 'json',
            pythonPath: process.env.PYTHON_PATH || 'python3',
            scriptPath: __dirname,
            args: [
              audio,
              '--device', modelConfig.device,
              '--dtype', modelConfig.dtype,
            ],
          };
          
          if (normalizedLanguage) {
            options.args.push('--language', normalizedLanguage);
          }
          
          PythonShell.run('asr.py', options, (err, results) => {
            if (err) reject(err);
            else resolve(results[0]);
          });
        });
        
        if (transcribeResult.success) {
          // 返回转录结果给OpenClaw
          res.json({
            success: true,
            data: {
              text: transcribeResult.data.text,
              language: transcribeResult.data.language,
              userId,
              sessionId,
              type: 'text.message',
            }
          });
        } else {
          throw new Error(transcribeResult.error);
        }
        break;
        
      case 'skill.enable':
        // Skill启用事件
        console.log('Skill已启用:', payload);
        res.json({ success: true, data: { status: 'enabled' } });
        break;
        
      case 'skill.disable':
        // Skill禁用事件
        console.log('Skill已禁用:', payload);
        res.json({ success: true, data: { status: 'disabled' } });
        break;
        
      default:
        res.status(400).json({
          success: false,
          error: `不支持的事件类型: ${type}`
        });
    }
  } catch (error) {
    console.error('Webhook处理错误:', error);
    res.status(500).json({
      success: false,
      error: error.message || '处理失败'
    });
  }
});

// 全局错误处理
app.use((error, req, res, next) => {
  console.error('全局错误:', error);
  res.status(error.statusCode || 500).json({
    success: false,
    error: error.message || '内部服务器错误'
  });
});

// 404处理
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: '接口不存在'
  });
});

// 启动服务
app.listen(PORT, HOST, () => {
  console.log(`🚀 OpenClaw Qwen ASR Skill 服务已启动`);
  console.log(`📍 服务地址: http://${HOST}:${PORT}`);
  console.log(`📦 模型: ${modelConfig.modelName}`);
  console.log(`💻 设备: ${modelConfig.device}`);
  console.log(`🌐 支持30种语言和22种中文方言识别`);
  console.log(`\nAPI接口:`);
  console.log(`  GET  /health      - 健康检查`);
  console.log(`  GET  /info        - Skill信息`);
  console.log(`  POST /transcribe  - 音频转文字`);
  console.log(`  POST /align       - 音频文本对齐`);
  console.log(`  POST /webhook     - OpenClaw Webhook`);
});

module.exports = app;
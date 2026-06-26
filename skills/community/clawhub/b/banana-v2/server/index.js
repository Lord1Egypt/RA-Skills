const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const Database = require('./services/database');
const RequestHandler = require('./services/request');
const TaskHandler = require('./services/task');
const UploadHandler = require('./services/upload');

const app = express();
const PORT = 2688;

// 中间件
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true }));

// 静态文件
app.use(express.static(path.join(__dirname, '../public')));

// 图片文件服务 - 使用环境变量中的保存路径
const getImageBasePath = () => {
  if (process.env.SAVE_PATH) {
    return process.env.SAVE_PATH;
  }
  
  const os = require('os');
  const platform = os.platform();
  const homeDir = os.homedir();
  
  // 根据平台设置默认目录
  if (platform === 'win32') {
    return path.join(homeDir, 'Desktop', 'banana2');
  } else if (platform === 'darwin') {
    return path.join(homeDir, 'Desktop', 'banana2');
  } else {
    return path.join(homeDir, 'banana2');
  }
};

// 动态图片服务 - 支持多个保存目录
app.use('/images', (req, res, next) => {
  const match = req.path.match(/^\/(\d+)\//);
  if (!match) {
    const basePath = getImageBasePath();
    return express.static(basePath)(req, res, next);
  }
  
  const workId = match[1];
  
  db.getWorkById(parseInt(workId)).then(work => {
    if (work && work.path) {
      const baseDir = path.dirname(work.path);
      express.static(baseDir, {
        setHeaders: (res) => {
          res.set('Cache-Control', 'public, max-age=86400');
        }
      })(req, res, next);
    } else {
      const basePath = getImageBasePath();
      express.static(basePath)(req, res, next);
    }
  }).catch(err => {
    console.error('[Images] 查询 work 失败:', err);
    const basePath = getImageBasePath();
    express.static(basePath)(req, res, next);
  });
});

// 读取配置文件
function getConfig() {
  const configPath = path.join(__dirname, '../config/set.json');
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// 初始化数据库
const db = new Database();
db.init();

// 初始化处理器
const taskHandler = new TaskHandler(db);
const requestHandler = new RequestHandler(db, taskHandler);
const uploadHandler = new UploadHandler(db);

// ==================== API 路由 ====================

// 获取配置
app.get('/api/get_set', (req, res) => {
  try {
    const config = getConfig();
    res.json({ success: true, data: config });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 保存配置到 JSON 文件
app.post('/api/config/save-json', (req, res) => {
  try {
    const config = req.body;
    const configPath = path.join(__dirname, '../config/set.json');
    
    // 验证基本结构
    if (!config.server || !config.models || !config.llm) {
      return res.status(400).json({ success: false, error: '配置结构不完整' });
    }
    
    // 写入文件
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
    res.json({ success: true, msg: '配置已保存' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// ==================== Prompts API ====================

// 获取提示词文件列表
app.get('/api/prompts/list', (req, res) => {
  try {
    const promptsDir = path.join(__dirname, '../config');
    const files = fs.readdirSync(promptsDir)
      .filter(f => f.endsWith('.prompt'))
      .map(f => {
        const stat = fs.statSync(path.join(promptsDir, f));
        return {
          name: f,
          size: stat.size,
          modified: stat.mtime
        };
      });
    res.json({ success: true, files });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取单个提示词文件内容
app.get('/api/prompts/get', (req, res) => {
  try {
    const file = req.query.file;
    if (!file || !file.endsWith('.prompt')) {
      return res.status(400).json({ success: false, error: '无效的文件名' });
    }
    
    const filePath = path.join(__dirname, '../config', file);
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ success: false, error: '文件不存在' });
    }
    
    const content = fs.readFileSync(filePath, 'utf-8');
    res.json({ success: true, content, name: file });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 保存提示词文件
app.post('/api/prompts/save', (req, res) => {
  try {
    const { oldName, newName, name, content, originalName } = req.body;
    
    // 兼容两种参数格式
    const targetName = newName || name;
    const sourceName = oldName || originalName;
    
    if (!targetName || !targetName.endsWith('.prompt')) {
      return res.status(400).json({ success: false, error: '无效的文件名' });
    }
    
    const configDir = path.join(__dirname, '../config');
    const filePath = path.join(configDir, targetName);
    
    // 如果是重命名，删除旧文件
    if (sourceName && sourceName !== targetName) {
      const oldPath = path.join(configDir, sourceName);
      if (fs.existsSync(oldPath)) {
        fs.unlinkSync(oldPath);
      }
    }
    
    fs.writeFileSync(filePath, content || '', 'utf-8');
    res.json({ success: true, msg: '保存成功', name: targetName });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 删除提示词文件
app.post('/api/prompts/delete', (req, res) => {
  try {
    const { filename, name } = req.body;
    
    // 兼容两种参数名
    const targetName = filename || name;
    
    if (!targetName || !targetName.endsWith('.prompt')) {
      return res.status(400).json({ success: false, error: '无效的文件名' });
    }
    
    const filePath = path.join(__dirname, '../config', targetName);
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ success: false, error: '文件不存在' });
    }
    
    fs.unlinkSync(filePath);
    res.json({ success: true, msg: '删除成功' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 生成图片
app.post('/api/generate', async (req, res) => {
  try {
    const result = await requestHandler.generate(req.body);
    res.json(result);
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// 轮询任务状态
app.post('/api/poll/:id', async (req, res) => {
  try {
    const { api_key } = req.body;
    if (api_key) {
      process.env.API_KEY = api_key;
    }
    
    const result = await taskHandler.poll(parseInt(req.params.id));
    res.json(result);
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 上传图片
app.post('/api/upload', async (req, res) => {
  try {
    const result = await uploadHandler.upload(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取作品列表
app.get('/api/works', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const pageSize = parseInt(req.query.pageSize) || 30;
    const keyword = req.query.keyword || '';
    
    const result = await db.getWorksPaginated(page, pageSize, keyword);
    
    const works = result.works.map(work => {
      if (work.path) {
        const pathParts = work.path.replace(/\\/g, '/').split('/');
        const workId = pathParts.pop();
        work.http_path = `/images/${workId}`;
      }
      return work;
    });
    
    res.json({ 
      success: true, 
      data: works,
      pagination: {
        page: result.page,
        pageSize: result.pageSize,
        total: result.total,
        totalPages: result.totalPages
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取单个作品
app.get('/api/work/:id', async (req, res) => {
  try {
    const work = await db.getWorkById(parseInt(req.params.id));
    
    if (work && work.path) {
      const pathParts = work.path.replace(/\\/g, '/').split('/');
      const workId = pathParts.pop();
      work.http_path = `/images/${workId}`;
    }
    
    res.json({ success: true, data: work });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 手动添加任务（list.html 使用）
app.post('/api/tasks/add', async (req, res) => {
  try {
    const { task_id, cut, ratio, prompt, api_key, platform_token, model_api_key, save_path } = req.body;
    
    if (api_key) process.env.API_KEY = api_key;
    if (platform_token) process.env.PLATFORM_TOKEN = platform_token;
    if (model_api_key) process.env.MODEL_API_KEY = model_api_key;
    if (save_path) process.env.SAVE_PATH = save_path;
    
    if (!task_id) {
      return res.status(400).json({ success: false, error: 'Task ID 不能为空' });
    }
    
    if (!process.env.API_KEY) {
      return res.status(400).json({ success: false, error: '请先配置 API Key' });
    }
    
    const workId = await db.createWork({
      task_id: task_id,
      prompt: prompt || '',
      cut: cut || 1,
      model: 'nano-banana-pro',
      ratio: ratio || '1:1',
      quality: '2K',
      size: '2K',
      path: '',
      request_data: {}
    });
    
    const config = getConfig();
    if (taskHandler) {
      requestHandler.startPolling(workId, task_id, config);
    }
    
    res.json({ 
      success: true, 
      msg: '任务添加成功，已启动轮询',
      work_id: workId
    });
  } catch (error) {
    console.error('添加任务失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// 删除作品
app.post('/api/admin/delete/:id', async (req, res) => {
  try {
    await db.deleteWork(parseInt(req.params.id));
    res.json({ success: true, msg: '删除成功' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 打开文件夹
app.post('/api/open-folder', (req, res) => {
  try {
    const { path: folderPath } = req.body;
    
    if (!folderPath) {
      return res.status(400).json({ success: false, error: '路径不能为空' });
    }
    
    if (!fs.existsSync(folderPath)) {
      return res.status(404).json({ success: false, error: '文件夹不存在' });
    }
    
    const { exec } = require('child_process');
    let command;
    
    if (process.platform === 'win32') {
      command = `explorer "${folderPath}"`;
    } else if (process.platform === 'darwin') {
      command = `open "${folderPath}"`;
    } else {
      command = `xdg-open "${folderPath}"`;
    }
    
    res.json({ success: true, msg: '已打开文件夹' });
    
    exec(command, (error) => {
      if (error) {
        console.error('打开文件夹失败:', error);
      }
    });
  } catch (error) {
    console.error('打开文件夹异常:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// 关闭服务
app.post('/api/shutdown', (req, res) => {
  res.json({ success: true, msg: '服务正在关闭' });
  setTimeout(() => process.exit(0), 1000);
});

// AI生成提示词（ai-prompt.html 使用）
app.post('/api/generate-prompt', async (req, res) => {
  try {
    const { input, api_key } = req.body;
    
    if (!input) {
      return res.status(400).json({ success: false, error: '请输入描述内容' });
    }
    
    const modelApiKey = api_key || process.env.MODEL_API_KEY;
    if (!modelApiKey) {
      return res.status(400).json({ success: false, error: '请先配置大模型 API Key' });
    }
    
    const config = getConfig();
    const llmConfig = config.llm || {};
    
    let llmUrl = llmConfig.url;
    const llmModel = llmConfig.model;
    
    if (!llmUrl || !llmModel) {
      return res.status(400).json({ 
        success: false, 
        error: '请先在设置页面配置 LLM URL 和模型',
        needConfig: true 
      });
    }
    
    if (!llmUrl.includes('/chat/completions')) {
      llmUrl = llmUrl.replace(/\/+$/, '');
      llmUrl += '/chat/completions';
    }
    
    const systemPromptPath = path.join(__dirname, '../config/system.prompt');
    let systemPrompt = '';
    
    if (fs.existsSync(systemPromptPath)) {
      systemPrompt = fs.readFileSync(systemPromptPath, 'utf-8');
    }
    
    const requestBody = {
      model: llmModel,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: input }
      ]
    };
    
    const response = await axios.post(
      llmUrl,
      requestBody,
      {
        headers: {
          'Authorization': `Bearer ${modelApiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: 60000
      }
    );
    
    const prompt = response.data.choices?.[0]?.message?.content?.trim();
    
    if (prompt) {
      res.json({ success: true, prompt });
    } else {
      res.status(500).json({ success: false, error: '生成失败，请重试' });
    }
    
  } catch (error) {
    console.error('[AI Prompt] 错误:', error.message);
    
    let errorMsg = '生成失败';
    
    if (error.response) {
      const errorData = error.response.data;
      if (typeof errorData === 'object') {
        errorMsg = errorData.error?.message || errorData.message || JSON.stringify(errorData);
      } else {
        errorMsg = errorData || error.message;
      }
    } else {
      errorMsg = error.message;
    }
    
    res.status(500).json({ success: false, error: errorMsg });
  }
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('服务器错误:', err);
  res.status(500).json({ success: false, error: err.message || '服务器内部错误' });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 Nano Banana V2 Server running at http://localhost:${PORT}`);
  console.log(`📁 Database: ${db.dbPath}`);
  console.log(`🎨 API: http://localhost:${PORT}`);
});

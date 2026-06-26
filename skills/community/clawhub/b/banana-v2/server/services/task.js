const axios = require('axios');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');
const http = require('http');

class TaskHandler {
  constructor(db) {
    this.db = db;
  }

  // 轮询单个任务
  async poll(workId) {
    const work = await this.db.getWorkById(workId);
    if (!work || !work.task_id) {
      throw new Error('任务不存在');
    }

    const result = await this.checkTaskStatus(work);
    return result;
  }

  // 使用 https.request 发送请求
  async sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
      const urlObj = new URL(url);
      const isHttps = urlObj.protocol === 'https:';
      const lib = isHttps ? https : http;
      
      const options = {
        hostname: urlObj.hostname,
        port: urlObj.port || (isHttps ? 443 : 80),
        path: urlObj.pathname + urlObj.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...headers
        }
      };

      const req = lib.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            const response = {
              status: res.statusCode,
              statusText: res.statusMessage,
              data: JSON.parse(body)
            };
            resolve(response);
          } catch (e) {
            resolve({
              status: res.statusCode,
              statusText: res.statusMessage,
              data: body
            });
          }
        });
      });

      req.on('error', (e) => {
        reject(e);
      });

      req.setTimeout(120000, () => {
        req.destroy();
        reject(new Error('请求超时'));
      });

      req.write(JSON.stringify(data));
      req.end();
    });
  }

  // 检查任务状态
  async checkTaskStatus(work) {
    if (!process.env.API_KEY) {
      throw new Error('请先配置 API_KEY');
    }

    // 读取配置
    const configPath = path.join(__dirname, '../../config/set.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

    const requestData = {
      id: work.task_id,
      action: 'retrieve'
    };

    try {
      // 使用 https.request
      const response = await this.sendRequest(
        config.server.task_url,
        requestData,
        {
          'Authorization': `Bearer ${process.env.API_KEY}`
        }
      );

      const data = response.data;

      // 检查HTTP状态码
      if (response.status !== 200) {
        return { 
          success: true, 
          status: 'pending', 
          msg: `HTTP ${response.status}: ${response.statusText}`,
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            response: data
          }
        };
      }

      // 检查是否有response
      if (!data.response) {
        return { 
          success: true, 
          status: 'pending', 
          msg: '任务处理中',
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            response: data
          }
        };
      }

      // 检查response.success
      if (data.response.success === false) {
        await this.db.updateWorkState(work.id, 99, '生成失败');
        return { 
          success: false, 
          status: 'failed', 
          msg: '生成失败',
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            response: data
          }
        };
      }

      // 检查是否有error
      if (data.response.error) {
        await this.db.updateWorkState(work.id, 99, data.response.error);
        return { 
          success: false, 
          status: 'failed', 
          msg: data.response.error,
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            response: data
          }
        };
      }

      // 成功，处理图片
      if (data.response.data && data.response.data.length > 0) {
        const imageData = data.response.data[0];
        
        // 保存图片
        const saveResult = await this.saveImage(work, imageData, config);
        
        return {
          success: true,
          status: 'completed',
          msg: '生成成功',
          data: saveResult,
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            response: data
          }
        };
      }

      return { 
        success: true, 
        status: 'pending', 
        msg: '任务处理中',
        debug: {
          request_url: config.server.task_url,
          request_data: requestData,
          response: data
        }
      };

    } catch (error) {
      // 如果是网络错误或超时，继续轮询
      if (error.code === 'ECONNABORTED' || error.code === 'ENOTFOUND' || error.code === 'ETIMEDOUT' || error.message === '请求超时') {
        console.log(`任务 ${work.task_id} 网络错误，继续轮询`);
        return { 
          success: true, 
          status: 'pending', 
          msg: '网络错误，继续轮询',
          debug: {
            request_url: config.server.task_url,
            request_data: requestData,
            error: {
              code: error.code,
              message: error.message
            }
          }
        };
      }

      // 其他错误 - 返回详细信息
      const errorMsg = error.message;
      console.error(`任务 ${work.task_id} 检查失败:`, errorMsg);
      
      return { 
        success: true, 
        status: 'pending', 
        msg: errorMsg,
        debug: {
          request_url: config.server.task_url,
          request_data: requestData,
          error: {
            message: error.message
          }
        }
      };
    }
  }

  // 保存图片
  async saveImage(work, imageData, config) {
    const imageUrl = imageData.image_url;
    const prompt = imageData.prompt || work.prompt;

    // 确定保存路径 - 使用id作为目录名
    let baseDir = process.env.SAVE_PATH;
    if (!baseDir) {
      const os = require('os');
      const platform = os.platform();
      const homeDir = os.homedir();
      
      // 根据平台设置默认目录
      if (platform === 'win32') {
        // Windows: 桌面/banana2
        baseDir = path.join(homeDir, 'Desktop', 'banana2');
      } else if (platform === 'darwin') {
        // macOS: 桌面/banana2
        baseDir = path.join(homeDir, 'Desktop', 'banana2');
      } else {
        // Linux 及其他: 用户主目录/banana2
        baseDir = path.join(homeDir, 'banana2');
      }
    }
    
    const saveDir = path.join(baseDir, String(work.id));
    
    // 创建目录
    try {
      if (!fs.existsSync(saveDir)) {
        fs.mkdirSync(saveDir, { recursive: true });
        console.log(`[Save] 创建目录: ${saveDir}`);
      }
    } catch (mkdirErr) {
      console.error(`[Save] 创建目录失败:`, mkdirErr);
      throw mkdirErr;
    }

    // 下载主图
    const mainImagePath = path.join(saveDir, 'main.png');
    
    try {
      console.log(`[Save] 开始下载图片: ${imageUrl}`);
      await this.downloadFile(imageUrl, mainImagePath);
      console.log(`[Save] 图片下载完成: ${mainImagePath}`);
    } catch (downloadErr) {
      console.error(`[Save] 下载图片失败:`, downloadErr.message);
      await this.db.updateWorkState(work.id, 99, '下载失败: ' + downloadErr.message);
      throw downloadErr;
    }

    // 创建480p缩略图
    const sharp = require('sharp');
    const thumbPath = path.join(saveDir, 'thumb.png');
    try {
      await sharp(mainImagePath)
        .resize(480, null, { 
          fit: 'inside',
          withoutEnlargement: true 
        })
        .png()
        .toFile(thumbPath);
      console.log(`[Save] 缩略图已创建: ${thumbPath}`);
    } catch (err) {
      console.error(`[Save] 创建缩略图失败:`, err.message);
      // 缩略图失败不影响主流程
    }

    // 更新数据库
    await this.db.updateWork(work.id, {
      state: 10,
      path: saveDir,
      filename: 'main',
      ext: 'png',
      response_data: JSON.stringify(imageData)
    });

    // 如果需要切割
    if (work.cut > 1) {
      try {
        await this.cutImage(mainImagePath, saveDir, work.cut, config);
      } catch (cutErr) {
        console.error(`[Save] 切割图片失败:`, cutErr.message);
        // 切割失败不影响主流程
      }
    }

    // 保存请求和响应信息
    const infoPath = path.join(saveDir, 'info.json');
    const infoData = {
      id: work.id,
      task_id: work.task_id,
      prompt: prompt,
      model: work.model,
      ratio: work.ratio,
      quality: work.quality,
      cut: work.cut,
      created_at: work.date,
      image_url: imageUrl,
      request: JSON.parse(work.request_data || '{}'),
      software: {
        name: '云羲多图创作',
        author: '小潴',
        email: 'zhuxi0906@gmail.com',
        wechat: 'jakeycis',
        website: 'banana2.zjhn.com'
      }
    };
    
    try {
      fs.writeFileSync(infoPath, JSON.stringify(infoData, null, 2));
      console.log(`[Save] 信息文件已保存: ${infoPath}`);
    } catch (infoErr) {
      console.error(`[Save] 保存信息文件失败:`, infoErr.message);
    }

    return {
      path: saveDir,
      main_image: mainImagePath,
      thumb_image: thumbPath,
      prompt: prompt
    };
  }

  // 下载文件
  downloadFile(url, filePath, retries = 3) {
    return new Promise((resolve, reject) => {
      const attemptDownload = (attempt) => {
        const protocol = url.startsWith('https') ? https : http;
        
        // 如果文件存在，先尝试删除
        if (fs.existsSync(filePath)) {
          try {
            fs.unlinkSync(filePath);
          } catch (unlinkErr) {
            console.warn(`[Download] 无法删除现有文件: ${unlinkErr.message}`);
          }
        }
        
        const file = fs.createWriteStream(filePath);
        
        const request = protocol.get(url, (response) => {
          if (response.statusCode === 302 || response.statusCode === 301) {
            // 处理重定向
            file.close();
            try { fs.unlinkSync(filePath); } catch (e) {}
            this.downloadFile(response.headers.location, filePath, retries)
              .then(resolve)
              .catch(reject);
            return;
          }
          
          if (response.statusCode !== 200) {
            file.close();
            try { fs.unlinkSync(filePath); } catch (e) {}
            reject(new Error(`下载失败: HTTP ${response.statusCode}`));
            return;
          }
          
          response.pipe(file);
          
          file.on('finish', () => {
            file.close((closeErr) => {
              if (closeErr) {
                console.warn(`[Download] 关闭文件时出错: ${closeErr.message}`);
                if (attempt < retries) {
                  console.log(`[Download] 重试 ${attempt + 1}/${retries}...`);
                  setTimeout(() => attemptDownload(attempt + 1), 1000);
                  return;
                }
                reject(closeErr);
              } else {
                console.log(`[Download] 文件下载成功: ${filePath}`);
                resolve();
              }
            });
          });
          
          file.on('error', (err) => {
            file.close();
            try { fs.unlinkSync(filePath); } catch (e) {}
            if (attempt < retries) {
              console.log(`[Download] 写入错误，重试 ${attempt + 1}/${retries}: ${err.message}`);
              setTimeout(() => attemptDownload(attempt + 1), 1000);
            } else {
              reject(err);
            }
          });
        });
        
        request.on('error', (err) => {
          file.close();
          try { fs.unlinkSync(filePath); } catch (e) {}
          if (attempt < retries) {
            console.log(`[Download] 请求错误，重试 ${attempt + 1}/${retries}: ${err.message}`);
            setTimeout(() => attemptDownload(attempt + 1), 1000);
          } else {
            reject(err);
          }
        });
        
        request.setTimeout(60000, () => {
          request.destroy();
          file.close();
          try { fs.unlinkSync(filePath); } catch (e) {}
          if (attempt < retries) {
            console.log(`[Download] 超时，重试 ${attempt + 1}/${retries}`);
            setTimeout(() => attemptDownload(attempt + 1), 1000);
          } else {
            reject(new Error('下载超时'));
          }
        });
      };
      
      attemptDownload(0);
    });
  }

  // 切割图片
  async cutImage(imagePath, saveDir, cutNum, config) {
    const sharp = require('sharp');
    
    // 检查源文件是否存在
    if (!fs.existsSync(imagePath)) {
      console.error(`[Cut] 源图片不存在: ${imagePath}`);
      return;
    }
    
    // 检查目标目录是否存在
    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, { recursive: true });
    }
    
    // 读取切割提示词配置 - 文件名为 cut_{num}.prompt
    const configDir = path.join(__dirname, '../../config');
    const cutPromptPath = path.join(configDir, `cut_${cutNum}.prompt`);
    let cutPrompt = '';
    
    if (fs.existsSync(cutPromptPath)) {
      cutPrompt = fs.readFileSync(cutPromptPath, 'utf-8');
    } else {
      // 创建默认切割提示词
      cutPrompt = this.getDefaultCutPrompt(cutNum);
      fs.writeFileSync(cutPromptPath, cutPrompt);
    }

    // 获取图片尺寸
    let metadata;
    try {
      const image = sharp(imagePath);
      metadata = await image.metadata();
    } catch (err) {
      console.error(`[Cut] 读取图片失败:`, err.message);
      return;
    }
    
    const width = metadata.width;
    const height = metadata.height;

    // 计算切割参数
    let cols, rows;
    if (cutNum === 2) { cols = 2; rows = 1; }
    else if (cutNum === 4) { cols = 2; rows = 2; }
    else if (cutNum === 6) { cols = 3; rows = 2; }
    else if (cutNum === 9) { cols = 3; rows = 3; }
    else { return; }

    // 获取切割内缩像素，默认3px
    const padding = config?.cut?.padding || 3;

    // 计算每个切割区域的精确位置和尺寸
    // 起始位置向上取整后增加padding，结束位置向下取整后减少padding
    // 例如：1000/3 = 333.33...，padding=3
    // 第1列：ceil(0)+3=3 到 floor(333.33)-3=330 → 宽度327
    // 第2列：ceil(333.33)+3=337 到 floor(666.66)-3=663 → 宽度326
    // 第3列：ceil(666.66)+3=670 到 floor(1000)-3=997 → 宽度327
    const calculateCutPositions = (totalSize, parts, paddingPx) => {
      const unitSize = totalSize / parts;
      const positions = [];
      
      for (let i = 0; i < parts; i++) {
        const rawStart = i * unitSize;
        const rawEnd = (i + 1) * unitSize;
        
        // 起始位置：向上取整 + padding
        const start = Math.ceil(rawStart) + paddingPx;
        // 结束位置：向下取整 - padding
        const end = Math.floor(rawEnd) - paddingPx;
        const size = end - start;
        
        positions.push({
          start,
          size
        });
      }
      
      return positions;
    };

    const xPositions = calculateCutPositions(width, cols, padding);
    const yPositions = calculateCutPositions(height, rows, padding);

    console.log(`[Cut] 图片尺寸: ${width}x${height}, 切割: ${cols}x${rows}, 内缩: ${padding}px`);
    console.log(`[Cut] X轴切割:`, xPositions.map(p => `${p.start}-${p.start + p.size}`).join(', '));
    console.log(`[Cut] Y轴切割:`, yPositions.map(p => `${p.start}-${p.start + p.size}`).join(', '));

    // 切割图片
    let index = 1;
    let lastPieceWidth = 0;
    let lastPieceHeight = 0;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const left = xPositions[col].start;
        const top = yPositions[row].start;
        const pieceWidth = xPositions[col].size;
        const pieceHeight = yPositions[row].size;
        
        lastPieceWidth = pieceWidth;
        lastPieceHeight = pieceHeight;
        
        const outputPath = path.join(saveDir, `${index}.png`);
        
        try {
          await sharp(imagePath)
            .extract({ left, top, width: pieceWidth, height: pieceHeight })
            .toFile(outputPath);
          
          console.log(`[Cut] 切割 ${index}: left=${left}, top=${top}, width=${pieceWidth}, height=${pieceHeight}`);
        } catch (cutErr) {
          console.error(`[Cut] 切割 ${index} 失败:`, cutErr.message);
        }
        index++;
      }
    }
  }

  // 轮询所有待处理任务
  async pollPendingTasks() {
    const tasks = await this.db.getPendingTasks();
    const configPath = path.join(__dirname, '../../config/set.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    const maxPollTimes = config.polling?.max_times || 20;

    for (const task of tasks) {
      try {
        // 检查轮询次数
        if (task.poll_count >= maxPollTimes) {
          await this.db.updateWorkState(task.id, 99, '轮询超时');
          continue;
        }

        // 检查任务状态
        const result = await this.checkTaskStatus(task);

        // 更新轮询信息
        const newPollCount = (task.poll_count || 0) + 1;
        const nextPollTime = Date.now() + (config.polling?.interval || 60000);
        
        await this.db.updatePollInfo(task.id, newPollCount, nextPollTime);

      } catch (error) {
        console.error(`任务 ${task.id} 轮询失败:`, error.message);
      }
    }
  }
}

module.exports = TaskHandler;

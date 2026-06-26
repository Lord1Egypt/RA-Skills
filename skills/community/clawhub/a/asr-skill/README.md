# OpenClaw Qwen ASR Skill

基于Qwen3-ASR-0.6B模型的语音转文字Skill，支持22种中文方言和多语言识别，让你可以用方言和OpenClaw交流。

## 功能特性

- ✅ 支持30种语言和22种中文方言识别
- ✅ CPU端侧运行，无需GPU
- ✅ 自动语言检测
- ✅ 支持多种音频格式（wav, mp3, flac等）
- ✅ 低延迟，高准确率
- ✅ 支持批量处理

## 支持的方言

安徽话、东北话、福建话、甘肃话、贵州话、河北话、河南话、湖北话、湖南话、江西话、宁夏话、山东话、陕西话、山西话、四川话、天津话、云南话、浙江话、粤语（香港口音）、粤语（广东口音）、吴语、闽南语。

## 快速开始

### 1. 安装依赖

```bash
# 安装Node.js依赖
npm install

# 安装Python依赖
pip install -U qwen-asr torch
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，根据需要调整配置
```

### 3. 启动服务

```bash
npm start
```

服务默认运行在 http://localhost:3000

## API 接口

### POST /transcribe

音频转文字接口

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| audio | File/String | 是 | 音频文件或base64编码的音频数据 |
| language | String | 否 | 指定语言/方言（如：Chinese, Cantonese, Sichuan等），不指定则自动检测 |
| format | String | 否 | 音频格式，默认：wav |

#### 响应结果

```json
{
  "success": true,
  "data": {
    "text": "识别结果文本",
    "language": "Chinese",
    "confidence": 0.98,
    "duration": 1.23
  }
}
```

## 使用示例

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const formData = new FormData();
formData.append('audio', fs.createReadStream('audio.wav'));
formData.append('language', 'Sichuan'); // 指定四川方言

axios.post('http://localhost:3000/transcribe', formData, {
  headers: formData.getHeaders()
})
.then(response => {
  console.log('识别结果:', response.data.data.text);
  console.log('检测语言:', response.data.data.language);
})
.catch(error => {
  console.error('识别失败:', error);
});
```

## 性能优化

### CPU 优化建议

1. 使用 `torch.set_num_threads()` 设置合适的线程数
2. 启用 MKL-DNN 加速
3. 调整批量大小以平衡延迟和吞吐量
4. 使用量化模型进一步减少内存占用

### 模型下载

首次运行时会自动下载模型，也可以手动提前下载：

```bash
# 下载ASR模型
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir ./models/Qwen3-ASR-0.6B

# 下载强制对齐模型（可选）
huggingface-cli download Qwen/Qwen3-ForcedAligner-0.6B --local-dir ./models/Qwen3-ForcedAligner-0.6B
```

## OpenClaw 集成

在OpenClaw中启用此Skill后，当用户发送语音消息时，系统会自动调用此Skill将语音转为文字，然后传给大模型进行回答。用户可以直接用方言语音和OpenClaw交流，无需手动输入文字。

## 许可证

Apache-2.0
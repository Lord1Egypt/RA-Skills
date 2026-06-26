# 安装部署指南

## 系统要求

- CPU: 4核以上，推荐8核
- 内存: 8GB以上，推荐16GB
- 存储: 至少10GB可用空间（模型文件约6GB）
- 操作系统: Linux/macOS/Windows

## 快速安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd openclaw-skill-qwen-asr
```

### 2. 安装依赖

#### 方式一：自动安装（推荐）

```bash
# 安装Node.js依赖
npm install

# 安装Python依赖
pip install -r requirements.txt
```

#### 方式二：conda环境（推荐用于Python环境管理）

```bash
# 创建conda环境
conda create -n qwen-asr python=3.12 -y
conda activate qwen-asr

# 安装依赖
pip install -r requirements.txt
npm install
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，根据需要调整配置：

```env
# 服务配置
PORT=3000
HOST=0.0.0.0

# 模型配置
MODEL_NAME=Qwen/Qwen3-ASR-0.6B
DEVICE=cpu
DTYPE=float32
MAX_NEW_TOKENS=1024
BATCH_SIZE=4

# 缓存配置
CACHE_DIR=./models
ENABLE_CACHE=true
```

### 4. 下载模型（可选，首次运行会自动下载）

```bash
# 安装huggingface-cli
pip install -U "huggingface_hub[cli]"

# 下载ASR模型
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir ./models/Qwen3-ASR-0.6B

# 下载强制对齐模型（可选）
huggingface-cli download Qwen/Qwen3-ForcedAligner-0.6B --local-dir ./models/Qwen3-ForcedAligner-0.6B
```

### 5. 启动服务

```bash
npm start
```

首次启动会自动下载模型（约6GB），请耐心等待。下载完成后服务会在 http://localhost:3000 启动。

## Docker 部署

### 构建镜像

```bash
docker build -t openclaw-qwen-asr .
```

### 运行容器

```bash
docker run -d \
  -p 3000:3000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/uploads:/app/uploads \
  --name openclaw-qwen-asr \
  openclaw-qwen-asr
```

### 使用Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'
services:
  qwen-asr:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./models:/app/models
      - ./uploads:/app/uploads
    environment:
      - PORT=3000
      - HOST=0.0.0.0
      - DEVICE=cpu
      - DTYPE=float32
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

## 性能优化

### CPU 优化

1. **使用Intel CPU优化**：
   ```bash
   pip install intel-extension-for-pytorch
   ```

2. **启用MKL加速**：
   ```bash
   pip install mkl mkl-include
   ```

3. **调整线程数**：
   在 `.env` 中调整 `OMP_NUM_THREADS` 和 `MKL_NUM_THREADS`：
   ```env
   OMP_NUM_THREADS=8
   MKL_NUM_THREADS=8
   ```

### 内存优化

如果内存不足，可以尝试：

1. 使用更小的批量大小：`BATCH_SIZE=2`
2. 限制最大生成 tokens：`MAX_NEW_TOKENS=512`
3. 使用量化模型减少内存占用

## 验证安装

### 1. 健康检查

```bash
curl http://localhost:3000/health
```

预期输出：
```json
{
  "success": true,
  "data": {
    "status": "running",
    "skill": "qwen-asr-skill",
    "version": "1.0.0",
    "model": "Qwen/Qwen3-ASR-0.6B",
    "device": "cpu"
  }
}
```

### 2. 测试转录功能

```bash
# 上传音频文件测试
curl -X POST -F "audio=@test.wav" http://localhost:3000/transcribe

# 指定方言测试（如四川话）
curl -X POST -F "audio=@sichuan_test.wav" -F "language=四川话" http://localhost:3000/transcribe
```

### 3. 运行测试套件

```bash
node test.js
```

## 常见问题

### Q: 首次启动下载模型很慢怎么办？

A: 可以使用国内镜像源：

```bash
# 使用ModelScope下载（推荐国内用户）
pip install modelscope
modelscope download --model Qwen/Qwen3-ASR-0.6B --local_dir ./models/Qwen3-ASR-0.6B
```

或者设置Hugging Face镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### Q: 内存不足，OOM错误？

A: 尝试以下解决方案：
1. 减少批量大小：`BATCH_SIZE=2` 或 `BATCH_SIZE=1`
2. 减少最大生成token数：`MAX_NEW_TOKENS=512`
3. 关闭不必要的其他程序，释放内存
4. 考虑使用有更大内存的机器

### Q: CPU推理速度慢？

A: 可以尝试：
1. 启用CPU优化，安装 `intel-extension-for-pytorch`
2. 调整线程数，设置为CPU核心数的75%
3. 使用量化模型
4. 考虑使用GPU加速（如果有NVIDIA显卡）

### Q: 支持哪些音频格式？

A: 支持wav、mp3、flac、m4a等常见音频格式，采样率建议16kHz以上。

### Q: 如何添加新的方言支持？

A: Qwen3-ASR-0.6B已经内置支持22种中文方言，无需额外配置。如果需要添加新的方言，可以考虑微调模型。

## 升级指南

### 从旧版本升级

```bash
# 拉取最新代码
git pull

# 更新依赖
npm install
pip install -U -r requirements.txt

# 重启服务
npm restart
```

## 卸载

```bash
# 停止服务
npm stop

# 删除项目目录
rm -rf openclaw-skill-qwen-asr

# 删除模型缓存（如果需要）
rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen3-ASR-0.6B
```
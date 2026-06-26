# 内存优化指南

## 小内存模式原理

SenseVoiceSmall 模型使用更小的参数量：
- 模型大小: ~500MB（vs Paraformer-Large ~2GB）
- 推理内存: ~500MB 峰值
- 自动卸载: 转录完成后释放

## 任务队列机制

防止多个任务同时加载模型导致 OOM：

```python
# transcribe.py 内置锁机制
LOCK_DIR = Path("/tmp/funasr_locks")

# 同一音频文件只能被一个进程处理
# 其他进程会等待或退出（--no-wait）
```

## 内存检查

转录前自动检查可用内存：

```bash
# 如果可用内存 < 模型需求，会报错
python3 scripts/transcribe.py audio.wav
# 输出: 💾 可用内存: 800 MB, 需要: 500 MB ✅
```

## 优化策略

### 1. 使用小内存模式

```bash
python3 scripts/transcribe.py audio.wav --mode small
```

### 2. 减少 batch_size_s

修改 transcribe.py：

```python
batch_size_s = 150  # 默认 300，减少可降低峰值内存
```

### 3. 分段处理长音频

```bash
# 使用 ffmpeg 分割
ffmpeg -i long.wav -f segment -segment_time 300 -c copy part%03d.wav

# 逐个转录
for f in part*.wav; do
  python3 scripts/transcribe.py "$f"
done
```

### 4. 关闭不需要的模型

VAD 和标点模型会占用额外内存。如果不需要：

```python
# 只用 ASR 模型
model = AutoModel(
    model="iic/SenseVoiceSmall",
    # vad_model=None,  # 跳过 VAD
    # punc_model=None, # 跳过标点
)
```

### 5. 使用 INT8 量化模型

```bash
# 使用量化版本
modelscope download --model iic/SenseVoiceSmall-INT8
```

## 内存监控

```bash
# 实时监控
watch -n 1 'free -h'

# 或在转录时显示详细信息
python3 scripts/transcribe.py audio.wav --verbose
```

## OOM 故障排查

### 症状

```
OSError: [Errno 12] Cannot allocate memory
```

### 解决方案

1. 检查可用内存: `free -h`
2. 使用小内存模式: `--mode small`
3. 关闭其他进程
4. 增加 swap 空间

```bash
# 临时增加 swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 推荐配置

| 场景 | 最低内存 | 推荐内存 |
|------|---------|---------|
| 小内存模式 | 1GB | 2GB |
| 大模型模式 | 3GB | 4GB |
| 批量处理 | 4GB | 8GB |

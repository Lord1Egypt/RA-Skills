# 模型对比

## 小内存模式 (small)

**模型**: SenseVoiceSmall

**特点**:
- 内存占用: ~500MB
- 速度: 快
- 自动卸载: ✅ 转录完成后自动释放内存
- 适用场景: 日常转录、低配置服务器、多任务环境

**使用**:

```bash
python3 scripts/transcribe.py audio.wav --mode small
```

---

## 大模型模式 (large)

**模型**: Paraformer-Large

**特点**:
- 内存占用: ~2GB
- 速度: 稍慢
- 自动卸载: ❌ 模型保持在内存中
- 适用场景: 专业转录、高精度需求、批量处理

**使用**:

```bash
python3 scripts/transcribe.py audio.wav --mode large
```

---

## 对比表

| 特性 | small | large |
|------|-------|-------|
| 模型名称 | SenseVoiceSmall | Paraformer-Large |
| 内存占用 | ~500MB | ~2GB |
| 识别精度 | 高（日常够用） | 极高 |
| 推理速度 | 快 | 稍慢 |
| 自动卸载 | ✅ | ❌ |
| 并行安全 | ✅ 任务队列 | ⚠️ 需手动控制 |
| 推荐场景 | 日常转录 | 专业场景 |

---

## 选择建议

**使用 small 模式**:
- 服务器内存 < 2GB
- 偶尔转录任务
- 多个并行任务

**使用 large 模式**:
- 专业场景需要最高精度
- 批量处理多个文件
- 服务器内存充足

---

## 模型文件位置

```
~/.cache/modelscope/hub/
├── iic___SenseVoiceSmall/
│   └── ... (~500MB)
└── iic___speech_paraformer-large_asr.../
    └── ... (~2GB)
```

## 手动下载

```bash
# 小模型
modelscope download --model iic/SenseVoiceSmall

# 大模型
modelscope download --model iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
```

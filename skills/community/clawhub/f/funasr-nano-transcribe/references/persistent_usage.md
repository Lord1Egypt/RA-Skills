# Fun-ASR-Nano-2512 持久化使用指南

## 为什么要持久化

`FunAsrTranscriber` 类已经设计为可以复用的形式，只需初始化一次即可处理多个文件。

## 基本用法

### 单次使用

```python
import sys
sys.path.insert(0, '/path/to/funasr-nano-transcribe/scripts')
from FunAsrTranscriber import AsrTranscriber

# 初始化（加载模型，耗时 3-5 秒）
transcriber = AsrTranscriber()

# 处理单个文件
result = transcriber.transcribe_sync('audio.wav')
print(result)
```

### 批量处理（推荐）

```python
import sys
from pathlib import Path
sys.path.insert(0, '/path/to/funasr-nano-transcribe/scripts')
from FunAsrTranscriber import AsrTranscriber

# 只初始化一次
transcriber = AsrTranscriber()

# 处理多个文件
audio_files = ['file1.wav', 'file2.wav', 'file3.wav']
results = {}

for file in audio_files:
    print(f"Processing: {file}")
    text = transcriber.transcribe_sync(file)
    results[file] = text

# 保存结果
for file, text in results.items():
    output_file = Path(file).with_suffix('.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
```

## 异步处理

### 异步转写

```python
import asyncio
import sys
sys.path.insert(0, '/path/to/funasr-nano-transcribe/scripts')
from FunAsrTranscriber import AsrTranscriber, speech_to_text_local

# 初始化
transcriber = AsrTranscriber()
audio_files = []  # 用于跟踪临时文件

# 读取音频
with open('audio.wav', 'rb') as f:
    audio_data = f.read()

# 异步转写
async def transcribe():
    text = await speech_to_text_local(transcriber, audio_data, audio_files)
    return text

text = asyncio.run(transcribe())
print(text)
```

## 注意事项

### 模型加载位置

模型必须在 scripts 目录下加载，因为依赖相对路径：

```python
import os
os.chdir('/path/to/funasr-nano-transcribe/scripts')
transcriber = AsrTranscriber()
```

### 设备切换

当前实现中，设备选择在 `FunAsrTranscriber.py` 中硬编码：

```python
device="cuda:0"  # 或 "cpu"
```

如需动态切换，可以修改 `FunAsrTranscriber.py` 中的设备设置。

### 热词修改

编辑 `FunAsrTranscriber.py` 中的 `HOT_WORDS` 列表：

```python
HOT_WORDS = [
    "你的热词1",
    "你的热词2",
    # ...
]
```

## 完整示例：Web 服务

```python
#!/usr/bin/env python3
from flask import Flask, request, jsonify
import sys
import os

# 设置路径
script_dir = '/path/to/funasr-nano-transcribe/scripts'
sys.path.insert(0, script_dir)
os.chdir(script_dir)

from FunAsrTranscriber import AsrTranscriber

app = Flask(__name__)

# 全局加载模型
print("Loading Fun-ASR-Nano-2512...")
transcriber = AsrTranscriber()
print("Model loaded!")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio_file = request.files['audio']
    temp_path = '/tmp/temp_audio.wav'
    audio_file.save(temp_path)
    
    try:
        text = transcriber.transcribe_sync(temp_path)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

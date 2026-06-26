# 使用示例

## 基本使用

### 1. 处理单个视频
```bash
# 处理HermesAgent WebUI视频
bilibili-transcribe BV1txQGByERW

# 指定输出目录
bilibili-transcribe BV1txQGByERW --output ./my_transcripts

# 使用medium模型（更准确）
bilibili-transcribe BV1txQGByERW --model medium

# 输出JSON格式
bilibili-transcribe BV1txQGByERW --format json

# 保留音频文件
bilibili-transcribe BV1txQGByERW --keep-audio
```

### 2. 批量处理
```bash
# 创建BV号列表
echo "BV1txQGByERW" > my_list.txt
echo "BV1xxxxxxx" >> my_list.txt

# 批量处理
bilibili-transcribe --batch my_list.txt
```

### 3. Cookie管理
```bash
# 检查Cookie状态
bilibili-transcribe --check-cookie

# 更新Cookie
bilibili-transcribe --update-cookie "SESSDATA=xxx; bili_jct=xxx; buvid3=xxx; DedeUserID=xxx"

# 指定Cookie文件
bilibili-transcribe BV1txQGByERW --cookie /path/to/cookie.txt
```

## Python API示例

### 基本使用
```python
from bilibili_transcriber import BilibiliTranscriber

# 初始化转录器
transcriber = BilibiliTranscriber(
    cookie_file="~/.bilibili_cookie.txt",
    model="base",
    use_china_mirror=True
)

# 处理视频
result = transcriber.process("BV1txQGByERW")

if result.success:
    print(f"标题: {result.video_info.title}")
    print(f"时长: {result.video_info.duration}秒")
    print(f"UP主: {result.video_info.up_name}")
    print(f"转录文件: {result.transcript_path}")
    
    # 访问转录内容
    for segment in result.transcript[:5]:  # 前5段
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### 批量处理
```python
from bilibili_transcriber import BilibiliTranscriber

transcriber = BilibiliTranscriber()

bvids = ["BV1txQGByERW", "BV1xxxxxxx", "BV1yyyyyyyy"]

for bvid in bvids:
    print(f"处理: {bvid}")
    result = transcriber.process(bvid)
    
    if result.success:
        print(f"✅ 成功: {result.video_info.title}")
    else:
        print(f"❌ 失败: {result.error}")
```

### 自定义配置
```python
from bilibili_transcriber import BilibiliTranscriber
import yaml

# 加载自定义配置
with open("custom_config.yaml", "r") as f:
    config = yaml.safe_load(f)

transcriber = BilibiliTranscriber(
    cookie_file=config["cookie"]["file"],
    model_name=config["model"]["name"],
    device=config["model"]["device"],
    compute_type=config["model"]["compute_type"],
    output_dir=config["output"]["default_dir"],
    keep_audio=config["output"]["save_audio"]
)

# 处理视频
result = transcriber.process("BV1txQGByERW")
```

## 高级功能

### 内容验证
```python
from bilibili_transcriber import BilibiliTranscriber

transcriber = BilibiliTranscriber()

# 处理视频并验证
result = transcriber.process("BV1txQGByERW", validate=True)

if result.success:
    # 手动验证
    transcript_text = " ".join([seg.text for seg in result.transcript])
    validation = transcriber.validate_transcript(
        transcript_text,
        result.video_info.title,
        keywords=["HermesAgent", "WebUI", "控制面板"]
    )
    
    print(f"匹配度: {validation['match_rate']:.1%}")
    print(f"是否有效: {validation['is_valid']}")
    print(f"找到关键词: {validation['keywords_found']}/{validation['total_keywords']}")
```

### 错误处理
```python
from bilibili_transcriber import BilibiliTranscriber
import logging

# 设置详细日志
logging.basicConfig(level=logging.DEBUG)

transcriber = BilibiliTranscriber()

try:
    result = transcriber.process("BV1txQGByERW")
    
    if result.success:
        print("处理成功")
    else:
        print(f"处理失败: {result.error}")
        
        if result.warnings:
            print("警告:")
            for warning in result.warnings:
                print(f"  - {warning}")
                
except Exception as e:
    print(f"程序错误: {e}")
    import traceback
    traceback.print_exc()
```

## 集成示例

### 自动化工作流
```python
import os
from pathlib import Path
from bilibili_transcriber import BilibiliTranscriber

def process_video_workflow(bvid, output_dir):
    """完整的视频处理工作流"""
    
    # 1. 初始化
    transcriber = BilibiliTranscriber(output_dir=output_dir)
    
    # 2. 处理视频
    result = transcriber.process(bvid)
    
    if result.success:
        # 3. 生成报告
        generate_report(result, output_dir)
        
        # 4. 清理临时文件
        if not transcriber.keep_audio:
            cleanup_temp_files(output_dir)
        
        return True
    else:
        return False

def generate_report(result, output_dir):
    """生成处理报告"""
    report_path = Path(output_dir) / "report.md"
    
    with open(report_path, 'w') as f:
        f.write(f"# 视频处理报告\n\n")
        f.write(f"**视频标题**: {result.video_info.title}\n")
        f.write(f"**处理时间**: {result.processing_time:.2f}秒\n")
        f.write(f"**转录字符**: {sum(len(seg.text) for seg in result.transcript)}\n")
        f.write(f"**片段数量**: {len(result.transcript)}\n")
    
    print(f"✅ 报告生成完成: {report_path}")
```

## 故障排除示例

### 网络问题
```bash
# 使用代理
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
bilibili-transcribe BV1txQGByERW
```

### 模型下载问题
```bash
# 使用国内镜像
export HF_ENDPOINT="https://hf-mirror.com"
bilibili-transcribe BV1txQGByERW
```

### 内存不足
```bash
# 使用更小的模型
bilibili-transcribe BV1txQGByERW --model base

# 限制内存使用
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
bilibili-transcribe BV1txQGByERW
```

## 输出文件结构

处理完成后，输出目录结构如下：
```
bilibili_transcripts/
└── BV1txQGByERW/
    ├── audio.m4a              # 音频文件（如果保留）
    ├── transcript.txt         # 文本格式转录
    ├── transcript.json        # JSON格式转录
    ├── transcript.md          # Markdown格式转录
    └── metadata.json          # 元数据信息
```

每个视频的元数据文件包含：
```json
{
  "bvid": "BV1txQGByERW",
  "title": "HermesAgent突然上WebUI了！这一波，体验直接拉满",
  "duration": 210,
  "up_name": "磊哥聊AI",
  "up_mid": "12345678",
  "pubdate": 1776174724,
  "model": "base",
  "language": "zh",
  "processing_time": 45.2,
  "transcript_length": 3625,
  "segment_count": 87
}
```

## 性能优化建议

1. **批量处理时**：使用 `--parallel` 参数并行处理
2. **长视频**：使用 `base` 模型，速度更快
3. **高质量转录**：使用 `medium` 模型，准确度更高
4. **内存优化**：设置 `OMP_NUM_THREADS=1` 和 `MKL_NUM_THREADS=1`
5. **网络优化**：使用国内镜像源 `https://hf-mirror.com`
---
name: ai-file-organizer
description: AI 智能文件整理 - 批量重命名、自动分类、智能归档（异步引擎 + 云同步）
version: 3.0.0
tags: [file-management, automation, ai, organization, productivity, async, cloud-sync]
user-invocable: true
---

# AI File Organizer Skill v3.0.0

**下一代智能文件整理工具** - 异步引擎、AI 内容分析、云同步、版本管理

## 🎯 触发条件

- **手动触发**: `/organize-files` 或 "帮我整理文件"、"清理重复文件"
- **定时触发**: 每周/每月自动整理下载文件夹
- **文件夹监控**: 监控指定文件夹自动整理
- **云同步触发**: 文件整理完成后自动同步到云端

## ✨ 核心功能

### 1. 异步处理引擎 🚀
- **并发处理**: 基于 asyncio 的异步 IO，速度提升 40%
- **智能调度**: 自动优化并发数，适配不同硬件
- **进度追踪**: 实时进度条 + 预估完成时间
- **错误隔离**: 单文件失败不影响整体流程

### 2. AI 内容分析 🧠
- **智能标签**: LLM 分析文件内容，生成精准描述
- **语义分类**: 基于内容语义自动分类，非简单关键词匹配
- **置信度评分**: 每个分类附带置信度，低置信度可人工复核
- **自学习**: 根据用户反馈优化分类模型

### 3. 智能缓存系统 💾
- **哈希缓存**: 文件哈希缓存，避免重复计算
- **分类缓存**: 已分类结果缓存，二次整理速度提升 70%
- **TTL 管理**: 自动过期机制，缓存不过度占用空间
- **持久化**: 重启后缓存依然有效

### 4. 云同步支持 ☁️
- **多云支持**: 阿里云盘、百度网盘、OneDrive
- **自动同步**: 整理完成后自动上传到云端
- **增量同步**: 仅上传变更文件，节省带宽
- **断点续传**: 网络中断后可继续传输

### 5. 文件版本管理 🔄
- **自动版本**: 文件变更自动保留历史版本
- **版本对比**: 支持查看不同版本差异
- **一键恢复**: 快速恢复到任意历史版本
- **版本清理**: 自动清理过期版本，节省空间

### 6. 重复文件清理 🗑️
- **内容哈希**: SHA256 哈希检测完全重复
- **相似度检测**: 感知哈希检测相似图片
- **智能保留**: 自动保留最佳版本（最高质量/最早创建）
- **安全删除**: 移动到回收站而非直接删除

### 7. 交互式 CLI 👆
- **预览模式**: 操作前预览整理方案
- **交互确认**: 关键操作前请求确认
- **详细日志**: 结构化日志，支持 JSON 导出
- **丰富输出**: Emoji、进度条、彩色输出

### 8. 智能清理建议 💡
- **临时文件**: 识别并建议删除系统临时文件
- **缓存清理**: 应用缓存、浏览器缓存清理建议
- **大文件检测**: 找出占用空间的大文件
- **重复下载**: 检测重复下载的文件

## 📋 配置参数

```yaml
# 命名规则
naming:
  format: "{date}_{type}_{original}"  # 日期_类型_原名
  date_format: "%Y%m%d"
  max_length: 100
  replace_spaces: true

# 分类规则
classification:
  enabled: true
  ai_analysis: true  # 启用 AI 内容分析
  categories:
    - name: "工作文档"
      keywords: ["报告", "方案", "合同", "发票"]
      folder: "Work/Documents"
    - name: "学习资料"
      keywords: ["教程", "课程", "笔记"]
      folder: "Learning"
    - name: "图片视频"
      extensions: ["jpg", "png", "mp4", "mov"]
      folder: "Media"
    - name: "代码项目"
      extensions: ["py", "js", "java", "go", "rs"]
      folder: "Code"

# 重复文件处理
duplicates:
  enabled: true
  similarity_threshold: 0.95
  keep_best: true
  move_to_folder: "_duplicates"

# 云同步
cloud_sync:
  enabled: false
  provider: "aliyun"  # aliyun | baidu | onedrive
  access_key: "${ALIYUN_ACCESS_KEY}"
  secret_key: "${ALIYUN_SECRET_KEY}"
  bucket: "my-files"
  auto_sync: true

# 版本管理
versioning:
  enabled: true
  max_versions: 5
  version_folder: ".versions"

# 缓存
cache:
  enabled: true
  max_size: 10000
  ttl_days: 7

# 性能
performance:
  max_concurrent: 10
  chunk_size: 8192
  use_async_io: true

# 日志
logging:
  level: "INFO"
  file: "logs/organizer.log"
  format: "json"
```

## 🚀 使用示例

### 示例 1: 整理下载文件夹

```bash
# 基础整理
python scripts/organizer.py --organize ~/Downloads

# 指定目标文件夹
python scripts/organizer.py --organize ~/Downloads --target ~/Organized

# 高性能模式
python scripts/organizer.py --organize ~/Downloads --concurrent 20
```

### 示例 2: 清理重复文件

```bash
# 检测重复
python scripts/organizer.py --duplicates ~/Files

# 清理并移动
python scripts/organizer.py --duplicates ~/Files --move-to _duplicates
```

### 示例 3: 使用配置文件

```bash
# 使用自定义配置
python scripts/organizer.py --organize ~/Downloads --config config.yaml

# 导出整理报告
python scripts/organizer.py --organize ~/Downloads --report report.json
```

### 示例 4: 预览模式

```bash
# 先预览整理方案
python scripts/organizer.py --organize ~/Downloads --dry-run

# 交互确认模式
python scripts/organizer.py --organize ~/Downloads --interactive
```

### 示例 5: 云同步

```bash
# 配置环境变量
export ALIYUN_ACCESS_KEY="your_key"
export ALIYUN_SECRET_KEY="your_secret"

# 整理并同步
python scripts/organizer.py --organize ~/Downloads --config cloud_config.yaml
```

## 📊 输出示例

```
============================================================
🚀 开始文件整理 (v3.0.0 异步引擎)
============================================================
📂 源目录：/home/user/Downloads
📁 目标目录：/home/user/Organized
📊 发现 523 个文件

处理进度: 100%|████████████████| 523/523 [00:26<00:00, 20.1file/s]

============================================================
📊 整理完成
============================================================
总文件数：523
✅ 成功：520
❌ 失败：3
⚡ 速度：20.0 个/秒
⏱️  耗时：26.0 秒
💾 缓存命中率：68.5%

分类统计:
  📄 Documents: 125 个
  🖼️  Images: 234 个
  🎥  Videos: 89 个
  💻  Code: 45 个
  📦  Archives: 27 个

📋 报告已导出：report.json
```

## 🔧 命令行参数

```
usage: organizer.py [-h] [--demo] [--organize DIR] [--target DIR]
                    [--duplicates DIR] [--config FILE] [--concurrent N]
                    [--no-cache] [--verbose] [--report FILE]

可选参数:
  -h, --help            显示帮助信息
  --demo                运行演示
  --organize DIR        整理指定文件夹
  --target DIR          目标文件夹
  --duplicates DIR      检测重复文件
  --config FILE         配置文件路径
  --concurrent N        最大并发数 (默认：10)
  --no-cache            禁用缓存
  --verbose, -v         详细输出
  --report FILE         导出报告路径
```

## 📈 性能基准

| 场景 | v2.0.0 | v3.0.0 | 提升 |
|------|--------|--------|------|
| 1000 文件 | 45 秒 | 26 秒 | **73%** ⬆️ |
| 10000 文件 | 8 分钟 | 4.5 分钟 | **78%** ⬆️ |
| 内存占用 | 256MB | 128MB | **50%** ⬇️ |
| 缓存命中率 | 0% | 70% | **新增** |

## 🛡️ 安全特性

- **只读优先**: 默认复制而非移动，原文件保留
- **操作审计**: 完整记录所有操作日志
- **权限检查**: 自动检查文件访问权限
- **敏感路径排除**: 自动跳过系统目录和隐藏目录
- **还原点**: 操作前自动创建还原点
- **加密存储**: 配置文件中的敏感信息加密存储

## 🔌 扩展开发

### 添加自定义分类器

```python
from organizer import AIFileOrganizer

class CustomOrganizer(AIFileOrganizer):
    def classify_file(self, file_path, filename):
        # 自定义分类逻辑
        if 'invoice' in filename.lower():
            return 'Finance/Invoices', 0.95
        return super().classify_file(file_path, filename)
```

### 添加云存储 provider

```python
from cloud_providers.base import BaseCloudProvider

class CustomCloudProvider(BaseCloudProvider):
    def upload(self, file_path, remote_path):
        # 实现上传逻辑
        pass
    
    def download(self, remote_path, local_path):
        # 实现下载逻辑
        pass
```

## 🐛 常见问题

### Q: 处理速度慢？
**A:** 
1. 增加并发数：`--concurrent 20`
2. 启用缓存：确保 `cache.enabled: true`
3. 检查磁盘 IO 性能

### Q: 分类不准确？
**A:**
1. 完善分类规则的关键词
2. 启用 AI 内容分析：`ai_analysis.enabled: true`
3. 检查文件名是否包含足够信息

### Q: 云同步失败？
**A:**
1. 检查 API 密钥配置
2. 确认网络连接正常
3. 查看日志：`logs/organizer.log`

## 📚 相关文档

- [README.md](README.md) - 完整文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [docs/PERFORMANCE.md](docs/PERFORMANCE.md) - 性能调优

## 🧪 测试

```bash
# 单元测试
python -m pytest tests/test_organizer.py -v

# 覆盖率报告
python -m pytest tests/test_organizer.py -v --cov=scripts --cov-report=html

# 性能基准测试
python tests/benchmark.py
```

## 📦 依赖

**必需:**
- Python 3.8+
- aiofiles
- aiomultiprocess

**可选:**
- tqdm (进度条)
- pyyaml (YAML 配置)
- dashscope (AI 内容分析)

## 📄 许可证

MIT License

## 👥 作者

于金泽

---

**版本**: 3.0.0  
**更新日期**: 2026-03-16  
**文档**: https://github.com/your-repo/ai-file-organizer

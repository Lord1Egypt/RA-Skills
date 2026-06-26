---
name: duplicate-file-cleaner
description: 扫描并识别计算机中的重复文件，提供智能整理建议；当用户需要清理重复文件、释放磁盘空间或整理照片库时使用
---

# 重复文件整理工具

## 任务目标
- 本 Skill 用于：扫描指定目录，识别完全相同的重复文件，生成结构化报告并提供整理建议
- 能力包含：文件内容哈希比对、重复文件分组、智能删除建议、磁盘空间分析
- 触发条件：用户提到"重复文件"、"清理磁盘"、"整理照片"、"释放空间"等需求

## 操作步骤

### 1. 准备阶段
- 确定要扫描的目录路径（用户需提供完整路径或相对路径）
- 确认是否需要限制文件类型（如仅扫描图片）
- 建议用户在操作前备份重要数据

### 2. 扫描阶段
- 调用 `scripts/duplicate_scanner.py` 执行扫描：
  ```bash
  python /workspace/projects/duplicate-file-cleaner/scripts/duplicate_scanner.py \
    --directory <扫描目录> \
    --output <报告文件.json> \
    --min-size 1024 \
    --extensions jpg,png,pdf,mp4
  ```
- 参数说明：
  - `--directory`：必填，要扫描的目录
  - `--output`：可选，输出报告文件路径（默认输出到终端）
  - `--min-size`：可选，最小文件大小（字节），默认 1024（1KB）
  - `--extensions`：可选，文件扩展名过滤，逗号分隔（如 jpg,png,gif）

### 3. 分析阶段
- 智能体解读扫描报告，提供以下建议：
  - 识别重复文件的数量和类型分布
  - 计算可释放的磁盘空间
  - 基于文件路径和修改时间推荐保留策略
  - 生成删除清单（标注高风险文件）

### 4. 整理阶段
- 根据智能体建议，用户可选择：
  - 自动删除：智能体生成批量删除脚本
  - 手动确认：逐个确认每个重复文件组的处理方式
  - 备份后删除：先将重复文件移动到备份目录
- 智能体协助执行删除操作或生成操作脚本

## 资源索引
- 核心脚本：[scripts/duplicate_scanner.py](scripts/duplicate_scanner.py)（用途：扫描目录并生成重复文件报告）
- 参考指南：[references/file-organization-guide.md](references/file-organization-guide.md)（何时读取：需要了解文件整理最佳实践、保留策略）

## 注意事项
- ⚠️ 在删除文件前，建议用户先备份重要数据
- ⚠️ 脚本仅检测文件内容完全相同的文件，不检测视觉相似的图片
- ⚠️ 对于系统目录（如 Windows/Program Files），建议谨慎操作
- 建议优先处理用户目录（如 Documents、Pictures、Downloads）
- 智能体会基于文件路径和修改时间提供保留建议，但最终决策由用户确认

## 使用示例

### 示例1：扫描照片库
```bash
# 扫描照片目录，仅查找图片文件
python scripts/duplicate_scanner.py \
  --directory ~/Pictures \
  --output report.json \
  --min-size 10240 \
  --extensions jpg,png,heic
```
智能体分析后建议保留拍摄时间最早的版本。

### 示例2：全盘扫描
```bash
# 扫描整个用户目录，查找所有类型的重复文件
python scripts/duplicate_scanner.py \
  --directory ~ \
  --output report.json \
  --min-size 1024
```
智能体会提示可能需要较长时间，并建议优先处理大文件。

### 示例3：清理下载目录
```bash
# 扫描下载目录，查找大于100KB的重复文件
python scripts/duplicate_scanner.py \
  --directory ~/Downloads \
  --output report.json \
  --min-size 102400
```
智能体会识别重复下载的资源文件，推荐删除多余副本。

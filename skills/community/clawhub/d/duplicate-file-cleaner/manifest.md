# duplicate-file-cleaner 技能清单

## 技能基本信息
```json
{
  "name": "duplicate-file-cleaner",
  "version": "1.0.0",
  "author": "扣子团队",
  "description": "扫描并识别计算机中的重复文件，提供智能整理建议；当用户需要清理重复文件、释放磁盘空间或整理照片库时使用",
  "skill_id": "duplicate-file-cleaner",
  "space_id": "0",
  "category": "系统工具",
  "tags": ["文件管理", "磁盘清理", "照片整理"],
  "compatibility": {
    "systems": ["Windows", "macOS", "Linux"],
    "python": ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
  }
}
```

## 功能亮点
1. **智能文件去重**：基于文件内容哈希比对，精确识别重复文件
2. **灵活过滤机制**：支持按文件类型、大小进行扫描
3. **安全删除策略**：提供智能删除建议，标注高风险文件
4. **结构化报告**：生成详细扫描报告，清晰展示重复文件分布
5. **多种整理方式**：自动删除、手动确认、备份后删除三重保障

## 使用场景
- 清理重复下载的文件，节省磁盘空间
- 整理照片库，删除重复的图片和视频
- 清理项目文件，删除冗余备份
- 释放磁盘空间，提升系统运行效率

## 快速上手
```bash
# 扫描照片目录，仅查找图片文件
python duplicate-file-cleaner/scripts/duplicate_scanner.py \
  --directory ~/Pictures \
  --output report.json \
  --min-size 10240 \
  --extensions jpg,png,heic
```

## 相关文档
- SKILL.md：详细使用说明
- references/file-organization-guide.md：文件整理最佳实践

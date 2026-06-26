# duplicate-file-cleaner 技能发布包

## 技能信息
- **技能名称**：duplicate-file-cleaner
- **版本**：v1.0.0
- **作者**：扣子团队
- **分类**：系统工具
- **发布平台**：clawhub 技能市场

## 技能描述
智能的重复文件检测与整理工具，帮助用户快速识别和清理计算机中的重复文件，释放宝贵的磁盘空间。支持文件内容哈希比对、智能过滤、安全删除建议和结构化报告生成。

## 核心功能
1. **精准文件去重**：基于文件内容哈希比对，准确识别完全相同的重复文件
2. **灵活过滤机制**：支持按文件类型、大小进行扫描过滤
3. **安全删除策略**：提供智能删除建议，标注高风险文件，避免误删
4. **结构化报告**：生成详细扫描报告，清晰展示重复文件分布
5. **多种整理方式**：自动删除、手动确认、备份后删除三重保障

## 适用场景
- 清理重复下载的文件，节省磁盘空间
- 整理照片库，删除重复的图片和视频
- 清理项目文件，删除冗余备份
- 释放磁盘空间，提升系统运行效率

## 系统要求
- Python 3.8 或更高版本
- 操作系统：Windows、macOS、Linux 均支持

## 文件清单
```
duplicate-file-cleaner/
├── SKILL.md                          # 技能详细说明文档
├── SKILL_SUMMARY.md                  # 技能摘要和快速入门
├── README.md                         # 用户使用指南
├── manifest.md                       # 技能元数据清单
├── requirements.txt                  # 依赖说明（使用标准库，无外部依赖）
├── scripts/
│   ├── duplicate_scanner.py         # 核心扫描脚本
│   └── __pycache__/                  # Python 缓存目录（发布时可忽略）
└── references/
    └── file-organization-guide.md    # 文件整理最佳实践指南
```

## 安装说明
用户只需下载技能包到相应目录，即可直接使用。无需额外安装依赖包（使用 Python 标准库）。

## 快速使用示例
```bash
# 扫描照片目录
python duplicate-file-cleaner/scripts/duplicate_scanner.py \
  --directory ~/Pictures \
  --output report.json \
  --min-size 10240 \
  --extensions jpg,png,heic
```

## 标签
文件管理、磁盘清理、照片整理、数据优化、系统工具

## 发布信息
- **发布日期**：2026年3月24日
- **兼容性**：Python 3.8-3.13
- **许可证**：MIT

## 联系方式
如有问题或建议，请通过 clawhub 市场反馈渠道联系。

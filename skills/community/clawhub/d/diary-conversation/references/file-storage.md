# 本地文件存储结构

## 设计原则
- **组织清晰**：按年月分层，便于查找和备份
- **格式统一**：统一文件命名和格式规范
- **易于迁移**：相对路径，支持整体移动
- **兼容性强**：使用通用格式（Markdown、JPEG等）

## 目录结构

### 完整结构
```
journals/                              # 日记根目录
├── README.md                          # 目录说明
├── index.json                         # 日记索引文件
│
├── 2025-02/                          # 2025年2月目录
│   ├── 2025-02-25.md                 # 单篇日记
│   ├── 2025-02-26.md
│   ├── summary-2025-02.md            # 月总结（可选）
│   └── images/                       # 当月图片
│       ├── 2025-02-25-1.jpg
│       ├── 2025-02-25-2.png
│       └── thumbnails/               # 缩略图目录
│
├── templates/                        # 日记模板
│   ├── basic.md
│   ├── detailed.md
│   └── weekly-review.md
│
├── exports/                          # 导出文件
│   ├── pdf/
│   ├── docx/
│   └── html/
│
└── backups/                          # 备份目录
    ├── auto-2025-02-25/
    └── manual-2025-02-28/
```

## 文件命名规范

### 日记文件
- **格式**：`YYYY-MM-DD.md`
- **示例**：`2025-02-25.md`
- **要求**：日期必须准确，便于排序和检索

### 图片文件
- **格式**：`YYYY-MM-DD-序号.扩展名`
- **示例**：`2025-02-25-1.jpg`, `2025-02-25-2.png`
- **序号**：每天从1开始，自动递增
- **扩展名**：保留原始格式，或统一转换

### 辅助文件
- **月总结**：`summary-YYYY-MM.md`
- **年索引**：`index-YYYY.md`
- **备份文件**：`backup-YYYY-MM-DD-HHMM.zip`

## 日记文件格式

### Markdown基本结构
```markdown
# 2025年2月25日 星期二 · ☀️ 晴朗 · 😊 愉快

## 早晨
[内容...]

![早晨咖啡](images/2025-02-25-1.jpg)

## 上午工作
[内容...]

## 午后时光
[内容...]

## 傍晚与夜晚
[内容...]

## 今日感悟
[内容...]

---
**记录时间**：2025-02-25 21:30
**心情指数**：8/10
**关键词**：工作完成, 朋友聚会, 新发现
**天气**：晴朗，15-22°C
**位置**：上海
**图片**：3张（早餐、工作环境、夕阳）
```

### 元数据头部（可选YAML frontmatter）
```yaml
---
date: 2025-02-25
weekday: 星期二
weather: ☀️ 晴朗
mood: 😊 愉快
mood_score: 8
keywords: [工作完成, 朋友聚会, 新发现]
images: 3
location: 上海
temperature: "15-22°C"
---
```

## 索引管理

### 主索引文件 (index.json)
```json
{
  "version": "1.0",
  "last_updated": "2025-02-25T21:30:00Z",
  "total_entries": 156,
  "years": {
    "2025": {
      "months": {
        "02": {
          "entries": 25,
          "first_date": "2025-02-01",
          "last_date": "2025-02-25",
          "word_count": 12560,
          "image_count": 45
        }
      }
    }
  },
  "recent_entries": [
    {
      "date": "2025-02-25",
      "path": "2025-02/2025-02-25.md",
      "title": "2025年2月25日 星期二",
      "mood_score": 8,
      "word_count": 520,
      "image_count": 3,
      "keywords": ["工作完成", "朋友聚会", "新发现"]
    }
  ]
}
```

### 月索引文件 (2025-02/index.json)
```json
{
  "month": "2025-02",
  "days": [
    {
      "date": "2025-02-25",
      "file": "2025-02-25.md",
      "mood": "愉快",
      "mood_score": 8,
      "has_images": true,
      "word_count": 520
    }
  ],
  "statistics": {
    "total_days": 25,
    "days_with_entries": 20,
    "average_mood": 7.2,
    "total_words": 12560,
    "total_images": 45
  }
}
```

## 文件操作

### 创建新日记
```bash
# 创建当月目录（如果不存在）
mkdir -p journals/$(date +%Y-%m)

# 创建日记文件
touch journals/$(date +%Y-%m)/$(date +%Y-%m-%d).md

# 创建图片目录
mkdir -p journals/$(date +%Y-%m)/images
mkdir -p journals/$(date +%Y-%m)/images/thumbnails
```

### 添加图片
```bash
# 获取当天已有图片数量
count=$(ls journals/$(date +%Y-%m)/images/*.jpg 2>/dev/null | wc -l)
next=$((count + 1))

# 保存图片
cp /tmp/uploaded.jpg journals/$(date +%Y-%m)/images/$(date +%Y-%m-%d)-${next}.jpg

# 生成缩略图
convert journals/$(date +%Y-%m)/images/$(date +%Y-%m-%d)-${next}.jpg \
  -resize 400x300 \
  journals/$(date +%Y-%m)/images/thumbnails/$(date +%Y-%m-%d)-${next}.jpg
```

### 更新索引
```bash
# 更新JSON索引（使用Python脚本更可靠）
python3 scripts/update_index.py
```

## 备份策略

### 自动备份
- **频率**：每天结束时自动备份当天新增内容
- **保留**：保留最近7天备份，每周归档一次
- **位置**：`journals/backups/auto-YYYY-MM-DD/`

### 手动备份
- **完整备份**：备份整个journals目录
- **增量备份**：只备份新增或修改的文件
- **云备份**：可选同步到云存储（需用户配置）

### 恢复流程
1. 选择备份版本
2. 验证备份完整性
3. 恢复到指定位置
4. 更新索引文件

## 迁移与同步

### 本地迁移
```bash
# 打包整个日记库
tar -czf journals-backup-$(date +%Y%m%d).tar.gz journals/

# 恢复到新位置
tar -xzf journals-backup-20250225.tar.gz -C /new/path/
```

### 跨设备同步
1. 使用Git进行版本控制（推荐）
2. 使用云存储同步（Dropbox、Google Drive等）
3. 定期手动复制

### Git版本控制配置
```bash
# 初始化Git仓库
cd journals/
git init

# 添加.gitignore
echo "backups/" >> .gitignore
echo "thumbnails/" >> .gitignore
echo "*.tmp" >> .gitignore

# 首次提交
git add .
git commit -m "Initial journals repository"
```

## 隐私与安全

### 加密选项
- **整个库加密**：使用VeraCrypt等加密容器
- **单文件加密**：敏感条目单独加密
- **元数据隐藏**：索引文件不包含敏感信息

### 访问控制
- 文件权限设置（chmod 600 for sensitive files）
- 目录访问日志
- 备份文件加密

## 维护任务

### 日常维护
- 清理临时文件
- 更新索引
- 检查文件完整性

### 月度维护
- 生成月统计报告
- 压缩旧图片
- 清理过期备份

### 年度维护
- 生成年度回顾
- 归档旧年份数据
- 优化存储结构
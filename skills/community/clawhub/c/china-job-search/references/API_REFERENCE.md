# 中国招聘搜索技能 API 参考

## 概述

本技能提供对中国三大主流招聘平台（BOSS直聘、智联招聘、前程无忧）的搜索功能，支持多条件筛选和结构化结果返回。

## 命令行接口

### 基本用法

```bash
python scripts/run_search.py --query "搜索 Python开发 北京"
```

### 参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--query` | string | 否 | 完整的搜索查询字符串 |
| `--platform` | string | 否 | 指定平台：boss/智联/前程无忧 |
| `--keyword` | string | 是 | 搜索关键词 |
| `--location` | string | 是 | 工作地点 |
| `--salary` | string | 否 | 薪资范围，格式：15-30K |
| `--experience` | string | 否 | 经验要求，格式：3-5年 |

### 查询字符串格式

1. **基础搜索**: `搜索 [关键词] [地点]`
   - 示例: `搜索 Python开发 北京`

2. **高级搜索**: `搜索 [关键词] [地点] [薪资范围] [经验要求]`
   - 示例: `搜索 Java开发 上海 20-40K 5-8年`

3. **平台指定搜索**: `搜索 [平台] [关键词] [地点]`
   - 示例: `搜索 boss Python 北京`
   - 示例: `搜索 智联 前端 上海`
   - 示例: `搜索 前程无忧 测试 广州`

## Python API

### JobSearcher 类

```python
from job_searcher import JobSearcher

# 初始化
searcher = JobSearcher(config_path='scripts/config.json')

# 搜索
results = searcher.search(
    keyword='Python开发',
    location='北京',
    platform=None,  # 可选：'boss', '智联', '前程无忧'
    salary_range='15-30K',  # 可选
    experience='3-5年'  # 可选
)
```

### Job 数据类

```python
@dataclass
class Job:
    platform: str          # 平台名称
    title: str            # 职位标题
    company: str          # 公司名称
    salary: str           # 薪资范围
    location: str         # 工作地点
    experience: str       # 经验要求
    education: str        # 学历要求
    skills: List[str]     # 关键技能
    url: str              # 详情链接
    publish_time: str     # 发布时间
    company_size: str     # 公司规模
    company_type: str     # 公司类型
```

## 平台支持

### BOSS直聘 (boss/zhipin)
- **特点**: 互联网行业最活跃，回复速度快
- **URL模式**: `https://www.zhipin.com/job_detail/`
- **限制**: 需要处理反爬机制

### 智联招聘 (智联/zhilian/zhaopin)
- **特点**: 传统综合性平台，职位覆盖面广
- **URL模式**: `https://jobs.zhaopin.com/`
- **限制**: 页面结构相对复杂

### 前程无忧 (前程无忧/qiancheng/51job)
- **特点**: 大型综合平台，外企职位较多
- **URL模式**: `https://jobs.51job.com/`
- **限制**: 部分页面需要登录

## 配置说明

### config.json 结构

```json
{
  "request": {
    "timeout": 10,
    "delay": 1.5,
    "max_retries": 3,
    "user_agent": "random"
  },
  "platforms": {
    "boss": {
      "enabled": true,
      "base_url": "https://www.zhipin.com",
      "search_path": "/web/geek/job"
    },
    "zhilian": {
      "enabled": true,
      "base_url": "https://sou.zhaopin.com",
      "search_path": "/"
    },
    "qiancheng": {
      "enabled": true,
      "base_url": "https://search.51job.com",
      "search_path": "/"
    }
  }
}
```

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `NETWORK_ERROR` | 网络连接失败 | 检查网络连接，增加重试次数 |
| `PARSER_ERROR` | 页面解析失败 | 更新解析器逻辑 |
| `PLATFORM_DISABLED` | 平台被禁用 | 检查config.json配置 |
| `INVALID_PARAMS` | 参数错误 | 检查输入参数格式 |

### 异常处理示例

```python
try:
    results = searcher.search(keyword='Python', location='北京')
except Exception as e:
    print(f"搜索失败: {e}")
    # 记录日志或进行降级处理
```

## 性能优化

### 请求优化
1. **延迟设置**: 默认1.5秒延迟，避免被封IP
2. **超时设置**: 10秒超时，防止长时间等待
3. **重试机制**: 3次重试，提高成功率

### 缓存策略
```python
# 可选的缓存实现
cache = {}
def search_with_cache(keyword, location):
    cache_key = f"{keyword}_{location}"
    if cache_key in cache:
        return cache[cache_key]
    results = searcher.search(keyword, location)
    cache[cache_key] = results
    return results
```

## 扩展开发

### 添加新平台
1. 创建新的解析器类，继承自 `BaseParser`
2. 实现 `parse_search_results` 方法
3. 在 `job_searcher.py` 中注册新平台
4. 更新 `config.json` 配置文件

### 示例：新平台解析器
```python
class NewPlatformParser(BaseParser):
    def parse_search_results(self, html):
        # 实现页面解析逻辑
        jobs = []
        # ... 解析代码
        return jobs
```

## 安全注意事项

1. **遵守robots.txt**: 尊重各平台的爬虫规则
2. **频率限制**: 避免高频请求，设置合理延迟
3. **数据使用**: 仅用于个人学习研究，不得用于商业用途
4. **隐私保护**: 不收集、不存储用户个人信息

## 更新维护

### 版本兼容性
- Python 3.7+
- 依赖库保持最新版本
- 定期更新解析器以适应平台变化

### 测试验证
```bash
# 运行测试
python scripts/test_skill.py

# 验证数据质量
python scripts/test_data_quality.py
```

## 开源协议

本技能遵循 MIT 开源协议，可自由使用、修改和分发。
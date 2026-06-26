# 电商分类采集技能

## 描述
自动从Audtools电商采集工具批量提交分类链接采集任务，并支持对已采集商品执行全选导出。支持从CSV文件读取collections链接，自动登录、提交采集任务，自动全选所有已采集商品并触发导出。

## 使用场景
- 批量处理电商网站分类链接采集
- 自动化重复的采集任务提交
- **自动化全选导出已采集商品**
- 处理大量分类链接数据

## 前置条件
1. Audtools账号（手机号：15715090600，密码：zzw12345）
2. 有效的商品采集工具服务（当前剩余26天）
3. CSV文件包含"完整链接"列

## 使用方法

### 基本命令
```bash
# 使用单个CSV文件（提交采集 + 自动全选导出）
/collect-categories /path/to/your/file.csv

# 使用目录下的所有CSV文件
/collect-categories /path/to/directory/

# 指定采集商品数（默认9999）
/collect-categories /path/to/file.csv --items 5000

# 指定操作间隔（默认2秒）
/collect-categories /path/to/file.csv --interval 3

# 指定tab关闭延迟（默认3秒）
/collect-categories /path/to/file.csv --close-delay 5

# 测试模式（只处理前3条）
/collect-categories /path/to/file.csv --test

# 只提交采集，不执行导出
/collect-categories /path/to/file.csv --no-export
```

### CSV文件格式要求
必须包含"完整链接"列，其他列可选：
```
完整链接,分类路径,域名,1级分类,2级分类,3级分类
https://zaraoutlet.top/collections/woman-collection-blazers,woman-collection-blazers,zaraoutlet.top,Women,Blazers,
https://zaraoutlet.top/collections/woman-collection-bodies,woman-collection-bodies,zaraoutlet.top,Women,Bodies,
```

### 工作流程
1. 读取CSV文件并验证格式
2. 打开主采集页面，检查登录状态，如未登录则自动登录
3. 对每条链接：
   - 输入collections链接和采集商品数
   - 提交采集任务
   - 点击进入已采集商品详情页（新标签）
   - **自动全选所有商品**（针对layui-table特殊处理，支持表头全选或逐个勾选）
   - 填入分类路径
   - 点击导出按钮触发下载
   - 关闭详情标签页
4. 等待指定间隔后处理下一条链接

## 技能文件结构
```
ecommerce-category-collector/
├── SKILL.md              # 技能说明文档
├── scripts/
│   └── collector.js      # 主要采集脚本
├── references/
│   └── csv-format.md     # CSV格式参考
└── test/
    └── sample.csv        # 测试数据
```

## 配置参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `audtools_url` | `https://www.audtools.com/users/shopns#/users/shopns/collecs?spm=m-1-2-3` | 采集页面URL |
| `username` | `15715090600` | 登录手机号 |
| `password` | `zzw12345` | 登录密码 |
| `default_items` | `9999` | 默认采集商品数 |
| `default_interval` | `2000` | 默认操作间隔（毫秒） |
| `default_close_delay` | `3000` | 默认tab关闭延迟（毫秒） |
| `exportWaitTimeout` | `30000` | 导出等待超时（毫秒） |

## 错误处理
- CSV文件不存在或格式错误 → 提示用户检查文件
- 登录失败 → 提示检查账号密码
- 网络连接问题 → 重试机制
- 页面元素找不到 → 智能等待和重试

## 注意事项
1. 免费会员每条任务最多采集10个商品
2. 分类采集不支持二级分类
3. 确保collections链接格式正确
4. 操作间隔避免触发反爬机制
5. 建议在非高峰时段批量操作

## 更新日志
- v1.0.0 (2026-03-18): 初始版本，支持基本采集功能
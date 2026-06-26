# CSV文件格式规范

## 必需格式
CSV文件必须包含以下列（按任意顺序）：

### 必需列
| 列名 | 说明 | 示例 |
|------|------|------|
| **完整链接** | 商品的collections链接，必须以http或https开头 | `https://zaraoutlet.top/collections/woman-collection-blazers` |

### 可选列（用于数据记录）
| 列名 | 说明 | 示例 |
|------|------|------|
| 分类路径 | 分类的URL路径部分 | `woman-collection-blazers` |
| 域名 | 网站域名 | `zaraoutlet.top` |
| 1级分类 | 一级分类名称 | `Women` |
| 2级分类 | 二级分类名称 | `Blazers` |
| 3级分类 | 三级分类名称 | `Jumpers` |
| 其他任意列 | 任何其他数据列 | 任意值 |

## 文件编码
- 推荐使用UTF-8编码
- 支持带BOM的UTF-8
- 支持GBK/GB2312（中文环境）

## 分隔符
- 默认使用逗号(`,`)作为分隔符
- 支持使用双引号(`"`)包裹包含逗号或换行符的字段

## 示例文件

### 基本示例
```csv
完整链接
https://example.com/collections/dresses
https://example.com/collections/shoes
https://example.com/collections/accessories
```

### 完整示例
```csv
完整链接,分类路径,域名,1级分类,2级分类,3级分类
https://zaraoutlet.top/collections/woman-collection-blazers,woman-collection-blazers,zaraoutlet.top,Women,Blazers,
https://zaraoutlet.top/collections/woman-collection-bodies,woman-collection-bodies,zaraoutlet.top,Women,Bodies,
https://zaraoutlet.top/collections/woman-collection-cardigans-jumpers,woman-collection-cardigans-jumpers,zaraoutlet.top,Women,Cardigans,Jumpers
https://zaraoutlet.top/collections/woman-collection-co-ord-sets,woman-collection-co-ord-sets,zaraoutlet.top,Women,Co-ord,Sets
```

### 带额外数据的示例
```csv
完整链接,分类路径,采集时间,备注
https://example.com/collections/new-arrivals,new-arrivals,2026-03-18,新品上架
https://example.com/collections/sale,sale,2026-03-18,促销商品
```

## 链接格式要求

### 有效链接
- `https://example.com/collections/category-name`
- `http://shop.example.com/collections/all`
- `https://www.example.com/collections/summer-dresses`

### 无效链接（将导致错误）
- `example.com/collections/dresses` (缺少协议)
- `/collections/dresses` (相对路径)
- `https://example.com/products/dress` (不是collections链接)
- 空链接

## 验证规则

### 自动验证
1. **文件存在性**：检查文件是否存在
2. **文件格式**：检查是否为有效的CSV文件
3. **必需列**：检查是否包含"完整链接"列
4. **链接格式**：检查链接是否以http/https开头
5. **链接内容**：警告非collections链接（包含`/collections/`）

### 验证失败处理
| 错误类型 | 处理方式 |
|----------|----------|
| 文件不存在 | 终止并提示错误 |
| 文件为空 | 终止并提示错误 |
| 缺少必需列 | 终止并提示错误 |
| 链接格式错误 | 终止并提示具体行号 |
| 非collections链接 | 警告但继续处理 |

## 最佳实践

### 1. 数据准备
```bash
# 检查CSV文件格式
head -n 5 yourfile.csv

# 检查链接数量
grep -c "http" yourfile.csv

# 检查无效链接
grep -v "^https://" yourfile.csv | grep -v "^http://"
```

### 2. 文件命名
- 使用有意义的文件名：`zara-categories-20260318.csv`
- 避免特殊字符和空格
- 使用日期版本：`categories-v1.0.csv`

### 3. 数据备份
- 处理前备份原始文件
- 记录处理日志
- 保存处理结果

## 工具支持

### 生成CSV文件
```python
# Python示例
import csv

data = [
    {"完整链接": "https://example.com/collections/dresses", "分类路径": "dresses"},
    {"完整链接": "https://example.com/collections/shoes", "分类路径": "shoes"},
]

with open("categories.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["完整链接", "分类路径"])
    writer.writeheader()
    writer.writerows(data)
```

### 验证CSV文件
```bash
# 使用csvlint工具
npm install -g csvlint
csvlint yourfile.csv
```

## 故障排除

### 常见问题
1. **中文乱码**：确保使用UTF-8编码保存文件
2. **分隔符问题**：检查是否使用了正确的逗号分隔符
3. **换行符问题**：确保使用统一的换行符（推荐LF）
4. **引号问题**：包含逗号的字段必须用双引号包裹

### 调试命令
```bash
# 查看文件编码
file -I yourfile.csv

# 查看前几行
head -n 10 yourfile.csv

# 统计行数
wc -l yourfile.csv

# 检查列数
awk -F',' '{print NF}' yourfile.csv | head -n 5
```
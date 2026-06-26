---
name: fofa-query
description: 网络空间资产搜索引擎，支持 IP/域名/端口/协议/证书等多维度查询；当用户需要进行网络资产发现、安全研究、漏洞资产定位、证书分析或需要查询特定特征的互联网资产时使用
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python"],"env":["FOFA_API_KEY"]},"primaryEnv":"FOFA_API_KEY"}}
dependency:
  python:
    - requests==2.31.0
---

# FOFA 网络空间资产搜索

## 任务目标

- 本 Skill 用于：通过 FOFA 搜索引擎查询互联网资产
- 能力包含：IP/域名查询、端口扫描结果查询、协议识别、证书分析、地理位置筛选、时间范围筛选
- 触发条件：用户需要查询特定特征的互联网资产、进行安全研究、资产发现或网络空间测绘

## 前置准备

### 凭证配置

本 Skill 需要配置 FOFA API 凭证。请访问 https://fofa.info 登录账号，进入「个人中心」→「API 信息」页面，将邮箱和 API Key 用冒号组合（格式：`email:key`）。

**配置示例**：
```
user@example.com:abc123def456
```

### 环境变量配置

将 FOFA API 凭证配置为环境变量 `FOFA_API_KEY`。

**配置示例**：
```
export FOFA_API_KEY="user@example.com:abc123def456"
```

### 在文件配置

```json
{
  "skills": {
    "entries": {
      "fofa-query": {
        "enabled": true,
        "apiKey": "FOFA_API_KEY"
      }
    }
  }
}
```

### 环境验证

在使用前，可以先检查用户信息和额度：

```bash
python scripts/fofa_query.py --user-info
```

## 操作步骤

### 1. 基础查询

使用 `scripts/fofa_query.py` 执行查询操作：

```bash
python scripts/fofa_query.py -q '查询语句'
```

**常用参数**：
- `-q, --query`: 查询语句（必需）
- `-f, --fields`: 返回字段（默认：`host,ip,port`）
- `--page`: 页码（默认：1）
- `--size`: 每页结果数（默认：100，最大：10000）
- `--format`: 输出格式（`text`/`json`/`table`，默认：`text`）

### 2. 查询语法构建

智能体应根据用户需求，参考 `references/query_syntax.md` 构建准确的查询语句。

**语法要点**：
- 字段名和值用运算符连接：`field="value"`
- 多条件用 `&&`（与）或 `||`（或）连接
- 复杂查询用括号明确优先级：`(condition1 && condition2) || condition3`
- 支持模糊匹配：`field*="value*"`

### 3. 典型查询场景

#### 场景 A：基础资产查询

```bash
# 查询指定 IP
python scripts/fofa_query.py -q 'ip="1.1.1.1"'

# 查询指定域名
python scripts/fofa_query.py -q 'domain="qq.com"'

# 查询指定端口
python scripts/fofa_query.py -q 'port="8080"'
```

#### 场景 B：组合条件查询

```bash
# 查询同时开放 80 和 443 端口的主机
python scripts/fofa_query.py -q '(port="80" && port="443")'

# 查询指定国家的 nginx 服务器
python scripts/fofa_query.py -q 'server="nginx" && country="CN"'

# 查询使用 Let's Encrypt 证书的网站
python scripts/fofa_query.py -q 'cert.issuer="Let\'s Encrypt" && cert.is_valid=true'
```

#### 场景 C：高级分析查询

```bash
# 获取统计信息
python scripts/fofa_query.py -q 'domain="baidu.com"' --stats

# 查询特定时间范围
python scripts/fofa_query.py -q 'after="2024-01-01" && before="2024-12-31" && domain="example.com"'

# 通过指纹查询
python scripts/fofa_query.py -q 'icon_hash="-247388890"'
```

### 4. 结果处理

智能体应对查询结果进行分析和解读：

- **结果数量评估**：判断结果集是否合理
- **关键信息提取**：从结果中提取关键资产信息
- **趋势分析**：对比不同查询的结果差异
- **安全建议**：基于查询结果提供安全建议

## 资源索引

- 查询脚本：[scripts/fofa_query.py](scripts/fofa_query.py) - 支持 API 调用、结果格式化
- 语法参考：[references/query_syntax.md](references/query_syntax.md) - 完整的查询语法和示例

## 注意事项

### 查询优化

1. **避免宽泛查询**：单独使用 `port="80"` 等常见特征会导致结果过多
2. **组合使用条件**：通过 `&&` 连接多个条件缩小结果范围
3. **合理设置字段**：只返回需要的字段以提高性能

### 语法规范

1. **引号使用**：字符串值必须用引号包裹
2. **括号优先级**：复杂查询务必使用括号明确优先级
3. **转义字符**：查询中包含引号时需要转义

### 使用限制

1. **API 配额**：查询结果数量受用户等级限制
2. **查询频率**：避免短时间内频繁调用 API
3. **结果延迟**：数据更新有一定延迟

### 安全合规

1. **合法使用**：仅用于合法的安全研究和资产发现
2. **遵守条款**：遵守目标网站的使用条款
3. **凭证保护**：妥善保管 API 凭证，避免泄露

## 使用示例

### 示例 1：查找特定组织的资产

**用户请求**："帮我查找 Google 的资产"

**执行流程**：
1. 构建查询语句：`org="Google LLC"`
2. 执行查询：
   ```bash
   python scripts/fofa_query.py -q 'org="Google LLC"' --size 50
   ```
3. 分析结果并汇报

### 示例 2：查找存在特定漏洞的资产

**用户请求**："查找使用 Apache 2.4.49 的服务器"

**执行流程**：
1. 构建查询：`server="Apache/2.4.49"`
2. 执行查询：
   ```bash
   python scripts/fofa_query.py -q 'server="Apache/2.4.49"' -f "host,ip,port,server,country"
   ```
3. 提示用户该版本可能存在的风险

### 示例 3：分析网站证书情况

**用户请求**："查找使用 Let's Encrypt 证书的中文网站"

**执行流程**：
1. 构建查询：`cert.issuer="Let's Encrypt" && title="中文关键词"`
2. 执行查询：
   ```bash
   python scripts/fofa_query.py -q 'cert.issuer="Let\'s Encrypt" && title*="管理"'
   ```
3. 分析证书使用情况

## 高级功能

### 统计分析

使用 `--stats` 参数获取聚合统计：

```bash
python scripts/fofa_query.py -q 'domain="example.com"' --stats
```

### JSON 输出

使用 `--format json` 获取结构化数据：

```bash
python scripts/fofa_query.py -q 'ip="1.1.1.1"' --format json
```

### 自定义字段

通过 `-f` 参数指定返回字段：

```bash
python scripts/fofa_query.py -q 'domain="qq.com"' -f "host,ip,port,title,server,country"
```

## 常见问题

### Q: 查询结果为空怎么办？

**可能原因**：
- 查询条件过于严格
- 语法错误
- 数据库中无匹配资产
- 可能余额不足

**解决方案**：
- 放宽查询条件
- 检查语法正确性
- 尝试更宽泛的查询
- 检查余额是否充足


### Q: 如何提高查询效率？

**建议**：
- 使用精确字段匹配
- 添加更多筛选条件
- 合理设置返回字段
- 控制结果数量

### Q: API 调用失败怎么办？

**排查步骤**：
1. 检查凭证配置是否正确
2. 确认 API 配额是否充足
3. 检查网络连接
4. 查看错误信息进行针对性处理

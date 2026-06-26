# 配置说明

## 环境变量配置

脚本支持两种配置方式，优先级：**系统环境变量 > .env文件**

### 方式一：系统环境变量

```bash
# Linux/Mac
export BAINIU_API_KEY="your_api_key_here"

# Windows (CMD)
set BAINIU_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:BAINIU_API_KEY="your_api_key_here"
```

### 方式二：.env文件

在技能目录下创建 `.env` 文件：

```
BAINIU_API_KEY=your_api_key_here
```

## 配置项说明

| 配置项 | 说明 | 必需 |
|--------|------|------|
| `BAINIU_API_KEY` | API密钥，用于身份认证 | 是 |

## 鉴权方式

API采用HTTP Header认证：

```
X-API-Key: <your_api_key>
Content-Type: application/x-www-form-urlencoded
```

## .env文件查找策略

从可执行文件所在目录开始，逐级向上遍历父目录（最多5层）寻找.env文件。

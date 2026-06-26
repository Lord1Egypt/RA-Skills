# 1688找供应商

一个用于查询1688供应商及工厂信息的命令行工具。

## 功能特性

- 根据供应商名称或关键字查询1688供应商信息
- 支持按地区、行业等条件筛选供应商
- 简单易用的CLI命令行界面
- 自动AK管理和签名认证

## 安装

### 前置要求

- Python 3.6 或更高版本
- pip（Python包管理器）

### 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 配置AK

首次使用前需要配置Access Key（AK）：

```bash
python3 cli.py configure YOUR_ACCESS_KEY
```

### 2. 查询供应商

```bash
# 查询特定供应商
python3 cli.py ali_1688_source_suppliers --query "灯具供应商"

# 使用缩写参数
python3 cli.py ali_1688_source_suppliers -q "常州工厂"
```

## 使用说明

### 命令列表

| 命令 | 说明 |
|------|------|
| `ali_1688_source_suppliers` | 查询1688供应商信息 |
| `configure` | 配置或查看AK状态 |

### 参数说明

#### ali_1688_source_suppliers

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--query` | `-q` | 是 | 供应商名称或关键字 |

#### configure

| 参数 | 说明 |
|------|------|
| `[AK]` | 可选，提供AK则进行配置，不提供则查看当前状态 |

### 输出格式

所有命令输出均为JSON格式：

```json
{
  "success": true,
  "markdown": "操作说明信息",
  "data": {
    "data": {
      // 具体数据
    }
  }
}
```

## 常见问题

### AK未配置

如果提示"AK 未配置"，请运行：

```bash
python3 cli.py configure YOUR_ACCESS_KEY
```

### AK无效

如果AK无效或已过期，请：

1. 检查AK是否正确
2. 重新配置AK：`python3 cli.py configure YOUR_ACCESS_KEY`
3. 如果配置后仍未生效，尝试重启OpenClaw或执行 `openclaw secrets reload`

### 网络错误

如果遇到网络错误：

1. 检查网络连接
2. 稍后重试
3. 检查防火墙设置

## 项目结构

```
1688-source-suppliers/
├── cli.py                                    # CLI入口
├── SKILL.md                                  # Skill定义
├── requirements.txt                          # Python依赖
├── scripts/                                  # 核心脚本
│   ├── _auth.py                             # 认证模块
│   ├── _http.py                             # HTTP客户端
│   ├── _const.py                            # 全局常量
│   ├── _errors.py                           # 异常定义
│   ├── _output.py                           # 输出工具
│   └── capabilities/                        # 功能实现
│       ├── configure/                       # AK配置
│       └── ali_1688_source_suppliers/       # 供应商查询
└── references/                              # 参考文档
    └── capabilities/
        ├── configure.md
        └── ali_1688_source_suppliers.md
```

## 开发

### 运行测试

```bash
# 查看帮助
python3 cli.py

# 测试配置命令
python3 cli.py configure

# 测试查询命令
python3 cli.py ali_1688_source_suppliers --help
```

### 代码规范

- 遵循PEP 8代码风格
- 使用类型注解
- 添加必要的文档字符串

## 许可证

[许可证信息]

## 联系方式

如有问题或建议，请联系项目维护者。

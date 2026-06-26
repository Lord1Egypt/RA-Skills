# BytePlan Chart 安装指南

## 安装状态

✅ **已安装** - 2026-03-09 19:35

## 安装步骤

### 1. Python 依赖

```bash
uv pip install --system requests pycryptodome
```

**状态**: ✅ 已安装（pycryptodome 新增）

### 2. Node.js 依赖

Canvas 模块复用 `scripts` 目录中的已安装版本，无需重复安装。

**状态**: ✅ 已配置

### 3. 配置文件

复制 `.env.example` 到 `.env` 并填写你的 BytePlan API 凭证：

```bash
cp .env.example .env
```

**状态**: ✅ 已配置

## 验证安装

```bash
cd skills/byteplan-chart
py main.py 查看不同性别分数段分布
```

**测试状态**: ✅ 测试通过 (2026-03-09 19:30)

## 依赖清单

| 依赖 | 版本 | 用途 |
|------|------|------|
| requests | latest | HTTP 请求 |
| pycryptodome | latest | RSA 加密 |
| canvas | ^2.11.2 | 图表渲染（复用 scripts/） |

## 系统要求

- Python 3.8+
- Node.js 16+
- Windows 10/11

## 故障排除

### 问题：找不到 canvas 模块

**解决**: 确保 `scripts/render_antv.js` 存在且已安装依赖

```bash
cd ../../scripts
yarn install
```

### 问题：API 认证失败

**解决**: 检查 `.env` 文件中的凭证是否正确

### 问题：中文乱码

**解决**: 确保系统已安装 Microsoft YaHei 或 SimHei 字体

## 更新日志

- 2026-03-10 14:45: v1.2.0 - 支持 RSA 加密密码，切换至 uatapp.byteplan.com
- 2026-03-09 21:50: v1.1.0 - 添加自动触发条件
- 2026-03-09 19:46: v1.0.1 - AGENT_ID 自动生成
- 2026-03-09 19:30: v1.0.0 - 初始版本发布

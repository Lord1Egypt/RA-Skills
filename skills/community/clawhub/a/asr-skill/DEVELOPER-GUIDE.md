# 开发者指南

## 本地开发流程

### 1. 环境准备

```bash
# 安装 Node.js 依赖
npm install

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 本地测试

```bash
# 启动服务
npm start

# 运行测试
npm test
```

### 3. 发布到 ClawHub

#### 方式一：使用 CLI（推荐）

```bash
# 1. 登录 ClawHub（浏览器流程）
clawhub login

# 或使用 API Token（更安全的方式）
clawhub login --token your-api-token-here --no-browser

# 2. 发布 Skill
clawhub publish . --slug qwen-asr-skill --version 1.0.0 --changelog "更新说明" --tags "asr,dialect,qwen"

# 或者使用 sync 命令（自动检测变化）
clawhub sync --all
```

#### 方式二：手动打包上传

```bash
# 1. 运行打包脚本
node package.js

# 2. 访问 https://clawhub.ai，登录并手动上传
```

## API 开发

### 环境变量

复制 `.env.example` 并根据需要修改：

```bash
cp .env.example .env
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| PORT | 服务端口 | 3000 |
| HOST | 监听地址 | 0.0.0.0 |
| MODEL_NAME | ASR 模型名称 | Qwen/Qwen3-ASR-0.6B |
| DEVICE | 运行设备 | cpu |
| DTYPE | 数据类型 | float32 |

### 接口文档

详见 `README.md` 中的 API 接口部分。

## 安全注意事项

⚠️ **重要：不要将 API Token 硬编码在代码中！**

- 用户 Token 存储在 `~/.openclaw/clawhub.json`（CLI 自动管理）
- 敏感配置放在 `.env` 文件中
- `.gitignore` 已配置忽略 `.env` 和敏感文件

## 代码结构

```
asr-skill/
├── index.js              # Express 服务主入口
├── asr.py                # Python 推理模块
├── dialect-map.js        # 方言映射配置
├── test.js               # 测试脚本
├── package.js            # 打包脚本
├── package.json          # Node.js 依赖配置
├── requirements.txt      # Python 依赖配置
├── .env.example          # 环境变量示例
├── skill.yml             # ClawHub 元数据
└── skills/
    └── qwen-asr-skill/
        ├── SKILL.md      # Skill 主文档
        ├── index.js      # 服务入口（复制）
        └── ...
```

## 故障排除

### 问题：CLI 提示 "Not logged in"
```bash
clawhub login
```

### 问题：Token 无效
```bash
# 清除旧 Token
clawhub logout

# 重新登录
clawhub login
```

### 问题：模型下载失败
```bash
# 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com

# 或 manually 下载模型
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir ./models/Qwen3-ASR-0.6B
```
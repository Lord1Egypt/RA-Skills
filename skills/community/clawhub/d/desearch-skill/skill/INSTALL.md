# Zeelin Deep Research Skill 安装指南

## 简介

Zeelin Deep Research 是一个深度研究技能，可以自动完成主题研究并生成报告。

## 前置要求

1. OpenClaw 已安装
2. Zeelin API Key（https://desearch.zeelin.cn 注册获取）

## 安装步骤

### 1. 安装 Skill

```bash
# 复制 skill 文件到 skills 目录
cp -r zeelin-deep-research ~/.openclaw/workspace/skills/

# 或解压压缩包
tar -xzvf zeelin-deep-research.tar.gz -C ~/.openclaw/workspace/skills/
```

### 2. 配置 API Key

```bash
# 创建配置文件
mkdir -p ~/.openclaw
cat > ~/.openclaw/zeelin-config.json << 'EOF'
{
  "api_key": "你的API_Key"
}
EOF
```

### 3. 使用方法

提交研究任务：

```bash
cd ~/.openclaw/workspace/skills/zeelin-deep-research
python3 scripts/async_runner.py -q "你的研究主题" -t deep -sr web
```

参数说明：
- `-q` 或 `--query`: 研究主题（必填）
- `-t` 或 `--thinking`: 思考模式
  - `smart`: 普通模式（快速）
  - `deep`: 深度模式（详细）
  - `major`: 专家模式
- `-sr` 或 `--search-range`: 搜索范围
  - `web`: 全网搜索
  - `academic`: 学术搜索
  - `selected`: 精选

## 报告位置

研究报告自动保存在：
```
~/.openclaw/workspace/skills/zeelin-deep-research/reports/
```

## 文件说明

```
zeelin-deep-research/
├── SKILL.md              # Skill 说明文档
├── references/           # 参考资料
│   ├── config.md
│   └── async-pattern.md
├── scripts/              # 脚本文件
│   ├── async_runner.py   # 主程序（提交任务+后台监控）
│   └── check_zeelin_complete.py  # Cron 检查脚本
└── reports/             # 报告输出目录
    └── zeelin-*.md       # 生成的研究报告
```

## 注意事项

1. API Key 需要从 https://desearch.zeelin.cn 获取
2. 深度模式(deep)研究时间较长，通常需要10-20分钟
3. 任务完成后会自动通过钉钉发送通知

## 故障排除

如果通知没有收到，检查：
1. API Key 是否正确配置
2. 钉钉是否正常连接
3. 查看日志：`cat ~/.openclaw/workspace/skills/zeelin-deep-research/reports/zeelin-research.log`

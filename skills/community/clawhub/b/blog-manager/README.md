# Blog Manager Skill

封装 Blog System API v1.0.0 的管理能力，提供 27 个 CLI 子命令（26 操作 + 1 capability-list）。子命令采用 flat kebab-case 命名（动词-名词式）。

## 目录结构

```
blog-manager/
├── SKILL.md                # 技能说明（名称、描述、子命令清单）
├── README.md               # 本文件
├── main.py                 # CLI 入口（argparse 分发 27 子命令）
├── requirements.txt        # 依赖（requests + pytest）
├── blog_manager/           # 模块化包（12 模块）
│   ├── __init__.py         # 版本声明 (__version__ = "1.0.0")
│   ├── client.py           # HTTP 客户端层（BlogClient + 异常类）
│   ├── capability.py       # capability-list 命令枚举
│   ├── formatter.py        # JSON + Markdown 双格式输出
│   ├── articles.py         # 文章管理（7 操作）
│   ├── labels.py           # 标签管理（2 操作）
│   ├── users.py            # 用户管理（2 操作）
│   ├── comments.py         # 评论管理（3 操作）
│   ├── messages.py         # 留言管理（4 操作）
│   ├── moods.py            # 说说管理（3 操作）
│   ├── uploads.py          # 文件上传（4 操作）
│   └── health.py           # 健康检查（1 操作）
├── scripts/                # 入口脚本目录
│   └── blog_manager.py     # CLI 入口 wrapper（委托 main.py）
├── references/             # 参考文档
│   └── api-reference.md    # API 端点文档（26 端点）
├── templates/              # 模板
│   └── test-vars.json      # 测试用例定义（27 子命令）
└── tests/                  # 单元测试 + 集成测试（11 个测试文件）
    ├── conftest.py
    ├── test_articles.py
    ├── test_client.py
    ├── test_cli.py
    ├── test_comments.py
    ├── test_health.py
    ├── test_labels.py
    ├── test_messages.py
    ├── test_moods.py
    ├── test_uploads.py
    └── test_users.py
```

## 快速开始

```bash
# 必填：设置环境变量（未设置会抛 BlogConfigError，退出码 2）
export BLOG_MANAGER_BASE_URL="http://your-blog-host:18080"

# 安装依赖
pip install -r requirements.txt

# 查看全部子命令
python3 scripts/blog_manager.py capability-list

# 健康检查
python3 scripts/blog_manager.py health-check

# 查询文章列表
python3 scripts/blog_manager.py list-articles --page 1 --size 10

# 创建文章
python3 scripts/blog_manager.py create-article --title "Hello" --content "World"

# 软删除文章（默认 soft=true）/ 硬删除（--soft false）
python3 scripts/blog_manager.py delete-article --id 1
python3 scripts/blog_manager.py delete-article --id 1 --soft false

# 上传单个文件
python3 scripts/blog_manager.py upload-file --file /path/to/image.png

# 批量上传（multipart files 字段）
python3 scripts/blog_manager.py upload-files --files a.png b.png
```

也可以直接使用 `main.py`：

```bash
python3 main.py capability-list
python3 main.py health-check
```

## 配置

| 环境变量 | 必填 | 默认值 | 说明 |
|----------|------|--------|------|
| `BLOG_MANAGER_BASE_URL` | 是 | 无 | Blog System 地址，须以 `http://` 或 `https://` 开头 |

> 地址不硬编码于源码中，统一通过环境变量配置；未设置时启动即抛 `BlogConfigError`（退出码 2）。

## 测试

```bash
cd blog-manager

# 安装依赖（含 pytest）
pip install -r requirements.txt

# 运行全部单元测试
python3 -m pytest tests/ -v

# 仅运行某模块测试
python3 -m pytest tests/test_articles.py -v
```

集成测试默认跳过；当 `BLOG_MANAGER_BASE_URL` 指向真实实例（URL 中不含 `test`）时自动启用：

```bash
export BLOG_MANAGER_BASE_URL="http://real-blog-host:18080"
python3 -m pytest tests/test_cli.py::TestIntegration -v
```

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | API 错误 / 文件错误 / 其它异常 |
| 2 | 配置错误（`BLOG_MANAGER_BASE_URL` 未设置或格式非法） |

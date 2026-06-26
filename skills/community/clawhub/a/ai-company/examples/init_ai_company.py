#!/usr/bin/env python3
"""
AI Company 项目初始化脚本
使用此脚本创建一个新的AI公司项目
"""

import os
import sys
import json
import argparse
from pathlib import Path


def create_project_structure(project_name: str, template: str = "basic"):
    """创建项目目录结构"""

    base_dir = Path(project_name)
    if base_dir.exists():
        print(f"❌ 目录 {project_name} 已存在")
        return False

    print(f"🚀 创建AI公司项目: {project_name}")

    # 创建目录结构
    directories = [
        "employees",
        "prompts/market_researcher",
        "prompts/product_designer",
        "prompts/developer",
        "prompts/sales_marketing",
        "prompts/customer_support",
        "prompts/monitor",
        "prompts/finance",
        "shared",
        "workflows",
        "logs",
        "tests",
    ]

    for dir_path in directories:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  📁 创建目录: {dir_path}")

    # 创建初始文件
    initial_files = {
        "shared/opportunities.json": {"opportunities": []},
        "shared/products.json": {"products": []},
        "shared/customers.json": {"customers": []},
        "shared/sales.json": {"sales": []},
        "shared/state.json": {"initialized": True, "version": "1.0.0"},
        "shared/metrics.json": {"metrics": {}},
        "prompts/versions.json": {
            "market_researcher": "v1.0",
            "product_designer": "v1.0",
            "developer": "v1.0",
            "sales_marketing": "v1.0",
            "customer_support": "v1.0",
            "monitor": "v1.0",
            "finance": "v1.0"
        }
    }

    for file_path, content in initial_files.items():
        full_path = base_dir / file_path
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"  📄 创建文件: {file_path}")

    # 创建主调度器模板
    main_py = '''#!/usr/bin/env python3
"""
AI Company 主调度器
"""

import sys
import json
from pathlib import Path


class AITeamCoordinator:
    """AI团队协调器"""

    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.employees = {}
        self.load_config()

    def load_config(self):
        """加载配置"""
        # TODO: 实现配置加载
        print("加载配置...")

    def start(self):
        """启动AI团队"""
        print("🚀 启动AI团队...")
        # TODO: 实现启动逻辑

    def stop(self):
        """停止AI团队"""
        print("⏹️  停止AI团队...")
        # TODO: 实现停止逻辑

    def get_status(self):
        """获取状态"""
        return {
            "status": "running",
            "employees": list(self.employees.keys())
        }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python main.py [start|stop|status]")
        sys.exit(1)

    coordinator = AITeamCoordinator()

    command = sys.argv[1]

    if command == "start":
        coordinator.start()
    elif command == "stop":
        coordinator.stop()
    elif command == "status":
        status = coordinator.get_status()
        print(json.dumps(status, indent=2))
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

    with open(base_dir / "main.py", 'w', encoding='utf-8') as f:
        f.write(main_py)
    print(f"  📄 创建文件: main.py")

    # 创建.env.example
    env_example = '''# AI Company 环境变量配置
# 复制此文件为 .env 并填入您的API密钥

# Anthropic Claude API
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# GitHub API (可选)
GITHUB_TOKEN=your-github-token-here

# 邮件服务 (可选)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Twitter API (可选)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_SECRET=your-twitter-access-secret
'''

    with open(base_dir / ".env.example", 'w', encoding='utf-8') as f:
        f.write(env_example)
    print(f"  📄 创建文件: .env.example")

    # 创建README
    readme = f'''# {project_name}

AI Company 自动化运营项目

## 快速开始

1. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，添加您的API密钥
```

2. 启动AI团队
```bash
python main.py start
```

3. 查看状态
```bash
python main.py status
```

## 项目结构

- `employees/` - AI员工实现
- `prompts/` - AI员工提示词（版本化）
- `shared/` - 共享数据
- `workflows/` - 工作流定义
- `logs/` - 日志文件

## 下一步

1. 实现 `employees/` 目录下的AI员工
2. 配置 `prompts/` 目录下的提示词
3. 定义 `workflows/` 目录下的工作流
4. 启动您的AI公司！

## 文档

- [AI Company 技能文档](https://github.com/your-username/ai-company)
- [API文档](https://github.com/your-username/ai-company/docs/api.md)
- [设计文档](https://github.com/your-username/ai-company/docs/design.md)
'''

    with open(base_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    print(f"  📄 创建文件: README.md")

    print(f"\n✅ 项目 {project_name} 创建成功！")
    print(f"\n📝 下一步:")
    print(f"   1. cd {project_name}")
    print(f"   2. cp .env.example .env")
    print(f"   3. 编辑 .env 文件，添加您的API密钥")
    print(f"   4. 开始实现您的AI员工！")

    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="创建新的AI公司项目"
    )
    parser.add_argument(
        "project_name",
        help="项目名称"
    )
    parser.add_argument(
        "--template",
        choices=["basic", "saas", "agency"],
        default="basic",
        help="项目模板 (默认: basic)"
    )

    args = parser.parse_args()

    success = create_project_structure(args.project_name, args.template)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

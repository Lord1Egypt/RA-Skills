# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — 配置初始化脚本
生成默认的 daily-brief-config.json 配置文件。

用法:
  python init_config.py                       # 在 Skill 根目录生成配置
  python init_config.py /path/to/output       # 在指定目录生成配置
"""
import json
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "version": "2.0",
    "adapters": {
        "wechatwork": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "_comment": "填入企业微信群机器人的 Webhook URL"
        },
        "dingtalk": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "secret": "",
            "_comment": "钉钉群机器人 Webhook (群设置 → 智能群助手 → 自定义机器人)"
        },
        "feishu": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "secret": "",
            "_comment": "飞书群机器人 Webhook (群设置 → 群机器人 → 自定义机器人)"
        },
        "slack": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "_comment": "Slack Incoming Webhook URL (api.slack.com/apps → Incoming Webhooks)"
        },
        "discord": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "_comment": "Discord Webhook (频道设置 → 整合 → Webhooks)"
        },
        "telegram": {
            "enabled": False,
            "type": "bot_api",
            "bot_token": "",
            "chat_id": "",
            "_comment": "Telegram Bot (@BotFather 创建 Bot 获取 Token)"
        },
        "teams": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "_comment": "Microsoft Teams Incoming Webhook (频道 → Workflows 或 Connectors)"
        },
        "email": {
            "enabled": False,
            "type": "smtp",
            "smtp_host": "",
            "smtp_port": 587,
            "smtp_user": "",
            "smtp_password": "",
            "from_addr": "",
            "to_addrs": [],
            "use_tls": True,
            "_comment": "SMTP 邮件配置，密码建议使用环境变量 SMTP_PASSWORD"
        },
        "github": {
            "enabled": False,
            "type": "github_pages",
            "github_user": "",
            "github_repo": "data-ai-daily",
            "_comment": "GitHub Pages 部署，Token 使用环境变量 GITHUB_TOKEN"
        }
    },
    "cron": [
        {
            "name": "Data+AI 全球日报",
            "schedule": "0 8 * * 1-5",
            "timezone": "Asia/Shanghai",
            "output": {
                "channels": ["wechatwork"],
                "file_prefix": "Data+AI全球日报"
            }
        }
    ],
    "customization": {
        "language": "zh-CN",
        "max_items": 12,
        "max_items_monday": 18,
        "monday_window_hours": 72,
        "focus_areas": [
            "大数据", "数据平台", "数据基础设施",
            "数据治理", "数据工程", "湖仓架构",
            "查询引擎", "流批处理", "向量检索",
            "开源数据生态"
        ],
        "priority_vendors": {
            "tier1": [
                "AWS", "Google Cloud", "Microsoft Azure",
                "Databricks", "Snowflake",
                "阿里云", "腾讯云", "华为云", "火山引擎"
            ],
            "tier2": [
                "Confluent", "MongoDB", "Elastic", "ClickHouse",
                "Cloudera", "Starburst", "dbt Labs",
                "Fivetran", "Airbyte", "Dataiku", "Palantir",
                "百度智能云", "京东云"
            ]
        },
        "open_source_projects": [
            "Iceberg", "Hudi", "Paimon", "Delta Lake",
            "Trino", "Spark", "Flink", "Ray", "Airflow",
            "Kafka", "dbt", "ClickHouse", "DuckDB",
            "Milvus", "Weaviate", "StarRocks", "Doris",
            "SeaTunnel", "Amoro"
        ]
    }
}


def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    output_file = output_dir / "daily-brief-config.json"

    if output_file.exists():
        print(f"[跳过] 配置文件已存在: {output_file}")
        print("  如需重新生成，请先删除现有文件")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)

    print(f"[成功] 配置文件已生成: {output_file}")
    print("\n请编辑配置文件，至少填写一个推送渠道的信息:")
    print("  - 企业微信: adapters.wechatwork.webhook_url")
    print("  - 钉钉:     adapters.dingtalk.webhook_url")
    print("  - 飞书:     adapters.feishu.webhook_url")
    print("  - Slack:    adapters.slack.webhook_url")
    print("  - 邮件:     adapters.email (smtp_host, smtp_user 等)")
    print("  - GitHub:   adapters.github (github_user)")


if __name__ == "__main__":
    main()

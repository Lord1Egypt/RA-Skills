# 人格修行系统 - 配置示例
# 复制此文件为 daily-cultivation-config.yaml 并修改

# ===== 基础配置 =====
system_name: "人格修行系统"
user_greeting: "朋友"
timezone: "Asia/Shanghai"

# Obsidian vault 路径（用于自动存档）
obsidian_vault: "D:/obisian/master"

# ===== 晨间设置 =====
morning:
  enabled: true
  time: "08:00"

  # 大师智慧
  wisdom:
    enabled: true
    masters:
      - name: 段永平
        quotes_file: quotes/段永平.md
      - name: 富兰克林
        quotes_file: quotes/富兰克林.md
      - name: 万维钢
        quotes_file: quotes/万维钢.md
      - name: 冯仑
        quotes_file: quotes/冯仑.md
      - name: 乔布斯
        quotes_file: quotes/乔布斯.md
      - name: 吴军
        quotes_file: quotes/吴军.md
    daily_count: 6

  # 美德提醒（方式一：使用富兰克林13美德）
  virtue:
    enabled: true
    system: franklin
    status_file: virtue-status.md

  # 美德提醒（方式二：自定义美德体系）
  # virtue:
  #   enabled: true
  #   system: custom
  #   virtues:
  #     - name: 专注
  #       definition: 全力投入当下之事
  #     - name: 勇气
  #       definition: 面对恐惧依然行动
  #     - name: 诚实
  #       definition: 对自己诚实，也对他人诚实
  #     - name: 感恩
  #       definition: 每天记录三件值得感恩的事
  #   status_file: virtue-status.md

# ===== 晚间设置 =====
evening:
  enabled: true
  time: "22:00"

  reflection:
    enabled: true
    template: templates/evening.md

  virtue_check:
    enabled: true

  # 自动存档
  auto_save:
    enabled: true
    save_path: "每晚复盘"
    filename_format: "{YYYY}-{MM}-{DD}-晚复盘.md"

# ===== 发送渠道 =====
channels:
  - type: feishu
    target: "user:ou_xxx"

# ===== 定时任务 =====
cron:
  morning:
    schedule: "0 8 * * *"
  evening:
    schedule: "0 22 * * *"

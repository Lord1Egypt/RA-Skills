# arxiv-to-obsidian 配置
# 这些配置都支持通过同名环境变量覆盖。

# Obsidian Vault 配置
VAULT_NAME="${VAULT_NAME:-AI}"
VAULT_FOLDER="${VAULT_FOLDER:-402论文资料}"

# 今日日记文件名。默认写入 402论文资料/YYYY-MM-DD.md
NOTE_NAME="${NOTE_NAME:-$(date +%Y-%m-%d).md}"

# 论文数量
PAPER_COUNT="${PAPER_COUNT:-10}"

# arXiv RSS Feed URL
ARXIV_RSS_URL="${ARXIV_RSS_URL:-https://export.arxiv.org/rss/cs.AI}"

# 仅预览，不实际写入 Obsidian。
DRY_RUN="${DRY_RUN:-0}"

# 支持的分类:
# cs.AI  - 人工智能
# cs.CL  - 计算语言学
# cs.LG  - 机器学习
# cs.CV  - 计算机视觉
# cs.NE  - 神经与进化计算
# stat.ML - 机器学习（统计）

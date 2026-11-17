"""版本与元数据常量。"""

VERSION = "2.7.0"
SKILL_NAME = "cn-llm-router"
DISPLAY_NAME = "国产大模型统一路由"
# update-check 默认拉取的版本清单地址（可被 config.json 的 update_url 覆盖）。
# 离线 / 不可达时跳过检查，绝不报错。
DEFAULT_UPDATE_URL = ""
# update-check 指向的技能主页；远程清单可覆盖。留空时回退到 "SkillHub"。
HOMEPAGE = "https://skillhub.cn/skill/cn-llm-router"
AUTHOR_EMAIL = "njskills@agent.qq.com"

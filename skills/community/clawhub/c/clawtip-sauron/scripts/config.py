# -*- coding: utf-8 -*-
"""
Skill 脚本配置项

集中管理后端地址、slug、技能元信息等。
切换本地调试 / 公网部署时，只需改这里的值即可，无需改动业务脚本。

本地调试：BACKEND_BASE_URL = "http://127.0.0.1:8000"
公网部署：BACKEND_BASE_URL = "https://your-api.example.com"
"""

# ===== 后端服务地址（重点配置项）=====
# 阿里云函数计算 FC 公网地址（正式环境）
BACKEND_BASE_URL = "https://clawtip-sauron-fydsneuavq.cn-hangzhou.fcapp.run"

# 后端接口路径（一般无需改动）
CREATE_ORDER_PATH = "/api/demo/createOrder"
GET_RESULT_PATH = "/api/demo/getServiceResult"

# 拼接出完整接口地址
CREATE_ORDER_URL = BACKEND_BASE_URL + CREATE_ORDER_PATH
GET_RESULT_URL = BACKEND_BASE_URL + GET_RESULT_PATH

# ===== 技能元信息 =====
# 技能 slug（唯一标识，用于计算 indicator 和订单文件目录）
SLUG = "clawtip-sauron"

# 技能 ID
SKILL_ID = "si-sauron-product"

# 服务描述
DESCRIPTION = "索伦娃娃（线下自取）"

# 服务资源地址
RESOURCE_URL = "https://ms.jr.jd.com"

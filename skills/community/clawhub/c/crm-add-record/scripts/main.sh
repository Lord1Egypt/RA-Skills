#!/bin/bash
# CRM新增记录技能（极简版：固定位置取参）

# 提取固定位置的参数（适配你的传参顺序）
CONTACT="$1"          # 第1个参数：姓名
PHONE="$2"            # 第2个参数：手机号
EMAIL="$3"            # 第3个参数：邮箱
COMPANY="$4"          # 第4个参数：公司
REMARK="$5"           # 第5个参数：备注（带引号的多词内容）

# 空值兜底
CONTACT=${CONTACT:-"未识别"}
PHONE=${PHONE:-"未识别"}
EMAIL=${EMAIL:-"未识别"}
COMPANY=${COMPANY:-"未识别"}
REMARK=${REMARK:-"未识别"}

# 生成标准化CRM记录
echo -e "\n=== 📋 标准化CRM记录 ==="
echo "姓名：$CONTACT"
echo "手机号：$PHONE"
echo "邮箱：$EMAIL"
echo "公司：$COMPANY"
echo "备注：$REMARK"
echo -e "\n✅ 可复制以上信息手动录入CRM系统"
echo "CRM登录地址：https://niw26kl7.fractaltest.cn/Crm/Backend/login.html"
echo "登录账号：weiyj | 密码：weiyj123"

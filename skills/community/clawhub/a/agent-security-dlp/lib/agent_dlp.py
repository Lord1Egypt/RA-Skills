#!/usr/bin/env python3
"""
Agent DLP - 数据防泄漏模块
功能: 入口防护、记忆保护、工具管控、出口过滤、审计日志
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class DLPConfig:
    """DLP配置"""
    
    DEFAULT_CONFIG = {
        "enabled": True,
        "mode": "normal",  # normal / strict
        "input": {
            "injection_detection": True,
            "sensitive_input": True,
        },
        "memory": {
            "pollution_check": True,
            "sensitive_filter": True,
        },
        "tools": {
            "dangerous": ["exec", "delete", "write"],
            "approval_required": True,
        },
        "output": {
            "enabled": True,
            "rules": ["china_idcard", "china_phone", "api_key", "password"],
        },
        "audit": {
            "enabled": True,
            "log_file": "~/.openclaw/logs/dlp-audit.log",
        }
    }
    
    def __init__(self, config_path: str = None):
        self.config = self.DEFAULT_CONFIG.copy()
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                self.config.update(json.load(f))
    
    def get(self, key, default=None):
        keys = key.split(".")
        v = self.config
        for k in keys:
            v = v.get(k, default)
        return v


class DLPRules:
    """DLP规则"""
    
    # 预编译正则表达式缓存
    _compiled_patterns = {}
    
    @classmethod
    def get_compiled_pattern(cls, pattern: str):
        """获取预编译的正则表达式"""
        if pattern not in cls._compiled_patterns:
            cls._compiled_patterns[pattern] = re.compile(pattern)
        return cls._compiled_patterns[pattern]
    
    RULES = {
        # ========== 中国PII ==========
        "china_idcard": {
            "pattern": r"[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
            "action": "block",
            "severity": "critical",
            "description": "中国身份证号",
            "category": "china_pii"
        },
        "china_phone": {
            "pattern": r"1[3-9]\d{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "中国手机号",
            "category": "china_pii"
        },
        "china_phone_with_prefix": {
            "pattern": r"(?:手机|电话|Mobile)[:：\s]*1[3-9]\d[\d\s\-]{8,13}",
            "action": "sanitize",
            "severity": "high",
            "description": "中国手机号(带标签)",
            "category": "china_pii"
        },
        "china_passport": {
            "pattern": r"[EW]\d{8,9}",
            "action": "sanitize",
            "severity": "high",
            "description": "中国护照号",
            "category": "china_pii"
        },
        "china_driver_license": {
            "pattern": r"[1-9]\d{14,17}",
            "action": "sanitize",
            "severity": "medium",
            "description": "中国驾驶证号",
            "category": "china_pii"
        },
        "china_hukou": {
            "pattern": r"(?i)户口本[：:]\s*\d{9,12}",
            "action": "sanitize",
            "severity": "high",
            "description": "中国户口本编号",
            "category": "china_pii"
        },
        
        # ========== 国际PII ==========
        "ssn": {
            "pattern": r"\d{3}-\d{2}-\d{4}",
            "action": "block",
            "severity": "critical",
            "description": "美国社会安全号",
            "category": "intl_pii"
        },
        "passport": {
            "pattern": r"[A-Z]{1,2}\d{6,9}",
            "action": "sanitize",
            "severity": "high",
            "description": "国际护照号",
            "category": "intl_pii"
        },
        "email": {
            "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "action": "sanitize",
            "severity": "medium",
            "description": "邮箱地址",
            "category": "intl_pii"
        },
        
        # ========== 密钥凭证 ==========
        "api_key": {
            "pattern": r"(?i)(api[_-]?key|apikey|api-key)\s*[:=]\s*['\"]?([a-zA-Z0-9_-]{20,})",
            "action": "block",
            "severity": "critical",
            "description": "API Key",
            "category": "credential"
        },
        "aws_key": {
            "pattern": r"(?:AKIA|ASIA)[0-9A-Z]{16}",
            "action": "block",
            "severity": "critical",
            "description": "AWS Access Key",
            "category": "credential"
        },
        "aws_secret": {
            "pattern": r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*['\"]?([a-zA-Z0-9/+=]{40})",
            "action": "block",
            "severity": "critical",
            "description": "AWS Secret Key",
            "category": "credential"
        },
        "private_key": {
            "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
            "action": "block",
            "severity": "critical",
            "description": "私钥",
            "category": "credential"
        },
        "github_token": {
            "pattern": r"gh[pousr]_[A-Za-z0-9]{36,255}",
            "action": "block",
            "severity": "critical",
            "description": "GitHub Token",
            "category": "credential"
        },
        "slack_token": {
            "pattern": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*",
            "action": "block",
            "severity": "critical",
            "description": "Slack Token",
            "category": "credential"
        },
        "jwt_token": {
            "pattern": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
            "action": "block",
            "severity": "critical",
            "description": "JWT Token",
            "category": "credential"
        },
        "azure_token": {
            "pattern": r"[a-zA-Z0-9+/]{86}==",
            "action": "block",
            "severity": "high",
            "description": "Azure Token",
            "category": "credential"
        },
        
        # ========== AI 服务 ==========
        "openai_key": {
            "pattern": r"sk-[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "OpenAI API Key",
            "category": "credential"
        },
        "claude_key": {
            "pattern": r"sk-ant-[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "Claude API Key",
            "category": "credential"
        },
        "google_ai_key": {
            "pattern": r"AIza[A-Za-z0-9_-]{35}",
            "action": "block",
            "severity": "critical",
            "description": "Google AI API Key",
            "category": "credential"
        },
        "anthropic_key": {
            "pattern": r"sk-ant-[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "Anthropic API Key",
            "category": "credential"
        },
        
        # ========== 中国云服务 ==========
        "aliyun_access_key": {
            "pattern": r"LTAI[a-zA-Z0-9]{20}",
            "action": "block",
            "severity": "critical",
            "description": "阿里云 AccessKey",
            "category": "credential"
        },
        "aliyun_secret": {
            "pattern": r"(?i)aliyun[_-]?secret\s*[:=]\s*[A-Za-z0-9]{30}",
            "action": "block",
            "severity": "critical",
            "description": "阿里云 Secret",
            "category": "credential"
        },
        "tencent_cloud_key": {
            "pattern": r"AKID[a-zA-Z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "腾讯云 API Key",
            "category": "credential"
        },
        "baidu_cloud_key": {
            "pattern": r"(?i)baidu[_-]?(ak|api[_-]?key)\s*[:=]\s*[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "百度云 API Key",
            "category": "credential"
        },
        "huawei_cloud_key": {
            "pattern": r"(?i)huawei[_-]?(ak|api[_-]?key)\s*[:=]\s*[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "华为云 API Key",
            "category": "credential"
        },
        "baidu_map_key": {
            "pattern": r"(?i)ak\s*[:=]\s*[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "high",
            "description": "百度地图 API Key",
            "category": "credential"
        },
        "amap_key": {
            "pattern": r"(?i)(amap|gaode)[_-]?key\s*[:=]\s*[A-Za-z0-9]{20,}",
            "action": "block",
            "severity": "high",
            "description": "高德地图 API Key",
            "category": "credential"
        },
        
        # ========== 中国支付/账号 ==========
        "wechat_appid": {
            "pattern": r"wx[0-9a-zA-Z]{16}",
            "action": "block",
            "severity": "high",
            "description": "微信 AppID",
            "category": "credential"
        },
        "wechat_secret": {
            "pattern": r"(?i)wechat[_-]?secret\s*[:=]\s*[a-zA-Z0-9]{32}",
            "action": "block",
            "severity": "critical",
            "description": "微信 Secret",
            "category": "credential"
        },
        "wechat_mch_id": {
            "pattern": r"1[0-9]{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "微信商户号",
            "category": "credential"
        },
        "alipay_appid": {
            "pattern": r"20[0-9]{12,}",
            "action": "sanitize",
            "severity": "high",
            "description": "支付宝 AppID",
            "category": "credential"
        },
        
        # ========== 美国/国际支付 ==========
        "stripe_key": {
            "pattern": r"sk_live_[A-Za-z0-9]{24,}",
            "action": "block",
            "severity": "critical",
            "description": "Stripe API Key",
            "category": "credential"
        },
        "stripe_webhook": {
            "pattern": r"whsec_[A-Za-z0-9]{32}",
            "action": "block",
            "severity": "critical",
            "description": "Stripe Webhook Secret",
            "category": "credential"
        },
        "paypal_client_id": {
            "pattern": r"[A-Za-z0-9]{20,}_[A-Za-z0-9]{5,}",
            "action": "sanitize",
            "severity": "high",
            "description": "PayPal Client ID",
            "category": "credential"
        },
        
        # ========== 加密货币 ==========
        "btc_address": {
            "pattern": r"(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}",
            "action": "block",
            "severity": "critical",
            "description": "比特币地址",
            "category": "crypto"
        },
        "eth_address": {
            "pattern": r"0x[a-fA-F0-9]{40}",
            "action": "block",
            "severity": "critical",
            "description": "以太坊地址",
            "category": "crypto"
        },
        "usdt_trc20": {
            "pattern": r"T[A-HJ-NP-Z0-9]{33}",
            "action": "block",
            "severity": "critical",
            "description": "USDT (TRC20) 地址",
            "category": "crypto"
        },
        "usdt_erc20": {
            "pattern": r"0x[a-fA-F0-9]{40}",
            "action": "block",
            "severity": "critical",
            "description": "USDT (ERC20) 地址",
            "category": "crypto"
        },
        "crypto_private_key": {
            "pattern": r"-----BEGIN\s+(EC\s+)?PRIVATE\s+KEY-----",
            "action": "block",
            "severity": "critical",
            "description": "加密货币私钥",
            "category": "crypto"
        },
        "wallet_mnemonic": {
            "pattern": r"(?i)(助记词|mnemonic|seed)\s*[:=]\s*[\w\s]{12,}",
            "action": "block",
            "severity": "critical",
            "description": "钱包助记词",
            "category": "crypto"
        },
        "ltc_address": {
            "pattern": r"[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}",
            "action": "block",
            "severity": "high",
            "description": "莱特币地址",
            "category": "crypto"
        },
        "xrp_address": {
            "pattern": r"r[1-9A-HJ-NP-Za-km-z]{24,34}",
            "action": "block",
            "severity": "high",
            "description": "瑞波币地址",
            "category": "crypto"
        },
        
        # ========== 通讯服务 ==========
        "twilio_account_sid": {
            "pattern": r"AC[a-z0-9]{32}",
            "action": "block",
            "severity": "critical",
            "description": "Twilio Account SID",
            "category": "credential"
        },
        "twilio_auth_token": {
            "pattern": r"[a-z0-9]{32}",
            "action": "sanitize",
            "severity": "high",
            "description": "Twilio Auth Token",
            "category": "credential"
        },
        "sendgrid_api_key": {
            "pattern": r"SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}",
            "action": "block",
            "severity": "critical",
            "description": "SendGrid API Key",
            "category": "credential"
        },
        "mailgun_api_key": {
            "pattern": r"key-[0-9a-zA-Z]{32}",
            "action": "block",
            "severity": "critical",
            "description": "Mailgun API Key",
            "category": "credential"
        },
        
        # ========== 存储服务 ==========
        "aws_s3_key": {
            "pattern": r"(?:AKIA|ASIA)[0-9A-Z]{16}",
            "action": "block",
            "severity": "critical",
            "description": "AWS S3 Access Key",
            "category": "credential"
        },
        "digitalocean_token": {
            "pattern": r"[a-z0-9]{64}",
            "action": "block",
            "severity": "critical",
            "description": "DigitalOcean Token",
            "category": "credential"
        },
        "cloudflare_api_key": {
            "pattern": r"[a-z0-9]{37}",
            "action": "block",
            "severity": "critical",
            "description": "Cloudflare API Key",
            "category": "credential"
        },
        
        # ========== 数据库服务 ==========
        "mongo_uri": {
            "pattern": r"mongodb(\+srv)?://[^:]+:[^@]+@",
            "action": "block",
            "severity": "critical",
            "description": "MongoDB URI",
            "category": "credential"
        },
        "redis_password": {
            "pattern": r"redis://:[^@]+@",
            "action": "block",
            "severity": "critical",
            "description": "Redis 密码",
            "category": "credential"
        },
        "postgres_password": {
            "pattern": r"postgres(ql)?://[^:]+:[^@]+@",
            "action": "block",
            "severity": "critical",
            "description": "PostgreSQL 密码",
            "category": "credential"
        },
        
        # ========== 开发工具 ==========
        "npm_token": {
            "pattern": r"npm_[A-Za-z0-9]{36}",
            "action": "block",
            "severity": "critical",
            "description": "NPM Access Token",
            "category": "credential"
        },
        "pypi_token": {
            "pattern": r"pypi-AgEIc[ A-Za-z0-9_-]{50,}",
            "action": "block",
            "severity": "critical",
            "description": "PyPI API Token",
            "category": "credential"
        },
        "dockerhub_token": {
            "pattern": r"[a-zA-Z0-9]{20,}",
            "action": "sanitize",
            "severity": "high",
            "description": "Docker Hub Token",
            "category": "credential"
        },
        "github_app_secret": {
            "pattern": r"(?i)github[_-]?app[_-]?secret\s*[:=]\s*[a-zA-Z0-9]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "GitHub App Secret",
            "category": "credential"
        },
        "gitlab_token": {
            "pattern": r"glpat-[a-zA-Z0-9_-]{20,}",
            "action": "block",
            "severity": "critical",
            "description": "GitLab Token",
            "category": "credential"
        },
        
        # ========== 生产力工具 ==========
        "notion_api_key": {
            "pattern": r"secret_[a-zA-Z0-9]{43,}",
            "action": "block",
            "severity": "critical",
            "description": "Notion API Key",
            "category": "credential"
        },
        "linear_api_key": {
            "pattern": "lin_api_[a-zA-Z0-9]{30,}",
            "action": "block",
            "severity": "critical",
            "description": "Linear API Key",
            "category": "credential"
        },
        "slack_webhook": {
            "pattern": r"https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+",
            "action": "block",
            "severity": "high",
            "description": "Slack Webhook URL",
            "category": "credential"
        },
        "slack_signing_secret": {
            "pattern": r"[a-zA-Z0-9]{32}",
            "action": "sanitize",
            "severity": "high",
            "description": "Slack Signing Secret",
            "category": "credential"
        },
        "telegram_token": {
            "pattern": r"TG\d{8,10}:[A-Za-z0-9_-]{30,}",
            "action": "block",
            "severity": "critical",
            "description": "Telegram Bot Token",
            "category": "credential"
        },
        "discord_token": {
            "pattern": r"[MN][A-Za-z0-9]{24,}\.[A-Za-z0-9]{6}\.[A-Za-z0-9_-]{27}",
            "action": "block",
            "severity": "critical",
            "description": "Discord Token",
            "category": "credential"
        },
        
        # ========== 医疗健康 ==========
        "medical_record_id": {
            "pattern": r"(?i)(病历号|门诊号|住院号)[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "病历号",
            "category": "medical"
        },
        "insurance_card": {
            "pattern": r"\d{10,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "医保卡号",
            "category": "medical"
        },
        
        # ========== 设备信息 ==========
        "imei": {
            "pattern": r"\d{15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "IMEI码",
            "category": "device"
        },
        "mac_address": {
            "pattern": r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})",
            "action": "sanitize",
            "severity": "medium",
            "description": "MAC地址",
            "category": "device"
        },
        
        # ========== 企业内部 ==========
        "employee_id": {
            "pattern": r"(?i)(工号|员工号|employee)[:=]\s*[A-Za-z0-9]{4,10}",
            "action": "sanitize",
            "severity": "medium",
            "description": "员工工号",
            "category": "internal"
        },
        
        # ========== 电商 ==========
        "order_id": {
            "pattern": r"(?i)(订单号|order)[:=]\s*[A-Za-z0-9]{12,20}",
            "action": "sanitize",
            "severity": "low",
            "description": "订单号",
            "category": "ecommerce"
        },
        
        # ========== 物流 ==========
        "tracking_number": {
            "pattern": r"(YT|SF|JD|ZTO|YTO|DD)[0-9]{9,15}",
            "action": "sanitize",
            "severity": "low",
            "description": "快递单号",
            "category": "logistics"
        },
        
        # ========== 社交 ==========
        "wechat_id": {
            "pattern": r"(?i)微信号[:=]\s*[a-zA-Z0-9_-]{6,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "微信号",
            "category": "social"
        },
        
        # ========== 金融行业 ==========
        "stock_account": {
            "pattern": r"(?i)(股票|证券)账号[:=]\s*[A-Za-z0-9]{8,12}",
            "action": "sanitize",
            "severity": "high",
            "description": "股票账户",
            "category": "finance"
        },
        "fund_account": {
            "pattern": r"(?i)基金账号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "基金账户",
            "category": "finance"
        },
        "insurance_policy": {
            "pattern": r"(?i)(保单|保险)号[:=]\s*[A-Za-z0-9]{10,20}",
            "action": "sanitize",
            "severity": "high",
            "description": "保单号",
            "category": "finance"
        },
        
        # ========== 教育行业 ==========
        "student_id": {
            "pattern": r"(?i)(学号|student)[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "学号",
            "category": "education"
        },
        "exam_ticket": {
            "pattern": r"(?i)准考证号[:=]\s*[A-Za-z0-9]{10,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "准考证号",
            "category": "education"
        },
        
        # ========== 政府/公务员 ==========
        "civil_servant_id": {
            "pattern": r"(?i)(公务员|事业编)编号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "公务员编号",
            "category": "government"
        },
        "police_id": {
            "pattern": r"(?i)警官证号[:=]\s*[A-Za-z0-9]{8,12}",
            "action": "sanitize",
            "severity": "high",
            "description": "警官证号",
            "category": "government"
        },
        
        # ========== 法规相关 ==========
        "contract_number": {
            "pattern": r"(?i)合同编号[:=]\s*[A-Za-z0-9]{10,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "合同编号",
            "category": "legal"
        },
        "filing_number": {
            "pattern": r"(?i)(立案|案号)[:=]\s*[A-Za-z0-9]{8,20}",
            "action": "sanitize",
            "severity": "high",
            "description": "立案/案号",
            "category": "legal"
        },
        "patent_number": {
            "pattern": r"(?i)专利号[:=]\s*[A-Z]{1,2}\d{7,12}",
            "action": "sanitize",
            "severity": "medium",
            "description": "专利号",
            "category": "legal"
        },
        "copyright_number": {
            "pattern": r"(?i)(著作权|版权)登记号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "著作权登记号",
            "category": "legal"
        },
        
        # ========== 交通出行 ==========
        "license_plate": {
            "pattern": r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4,5}",
            "action": "sanitize",
            "severity": "low",
            "description": "车牌号",
            "category": "transport"
        },
        "train_ticket": {
            "pattern": r"(?i)火车票号[:=]\s*[A-Z0-9]{8,12}",
            "action": "sanitize",
            "severity": "low",
            "description": "火车票号",
            "category": "transport"
        },
        "flight_ticket": {
            "pattern": r"(?i)机票号[:=]\s*[A-Z0-9]{6,13}",
            "action": "sanitize",
            "severity": "low",
            "description": "机票号",
            "category": "transport"
        },
        
        # ========== 通信行业 ==========
        "phone_bill": {
            "pattern": r"(?i)话单[:=]",
            "action": "sanitize",
            "severity": "high",
            "description": "通话记录",
            "category": "telecom"
        },
        
        # ========== 金融行业扩展 ==========
        "bank_card": {
            "pattern": r"\d{16,19}",
            "action": "block",
            "severity": "critical",
            "description": "银行卡号",
            "category": "financial"
        },
        "savings_account": {
            "pattern": r"(?i)(储蓄|存款)账号[:=]\s*[A-Za-z0-9]{10,19}",
            "action": "sanitize",
            "severity": "high",
            "description": "储蓄账户",
            "category": "finance"
        },
        "loan_account": {
            "pattern": r"(?i)(贷款|借款)账号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "贷款账户",
            "category": "finance"
        },
        "credit_account": {
            "pattern": r"(?i)(信用|信贷)账号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "信用账户",
            "category": "finance"
        },
        "payment_password": {
            "pattern": r"(?i)(支付|付款)密码[:=]\s*[A-Za-z0-9]{6,}",
            "action": "block",
            "severity": "critical",
            "description": "支付密码",
            "category": "finance"
        },
        "transaction_password": {
            "pattern": r"(?i)(交易|转账)密码[:=]\s*[A-Za-z0-9]{6,}",
            "action": "block",
            "severity": "critical",
            "description": "交易密码",
            "category": "finance"
        },
        "security_code": {
            "pattern": r"(?i)(安全码|验证码)[:=]\s*[A-Za-z0-9]{4,8}",
            "action": "block",
            "severity": "high",
            "description": "安全码/验证码",
            "category": "finance"
        },
        "digital_wallet": {
            "pattern": r"(?i)(数字钱包|钱包)地址[:=]\s*[A-Za-z0-9]{20,}",
            "action": "sanitize",
            "severity": "high",
            "description": "数字钱包地址",
            "category": "finance"
        },
        "crypto_address": {
            "pattern": r"(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}",
            "action": "sanitize",
            "severity": "high",
            "description": "比特币地址",
            "category": "finance"
        },
        "usdt_address": {
            "pattern": r"T[A-HJ-NP-Z0-9]{33}",
            "action": "sanitize",
            "severity": "high",
            "description": "USDT地址",
            "category": "finance"
        },
        "payment_link": {
            "pattern": r"https?://(qr|pay|wxpay|alipay)[./]",
            "action": "sanitize",
            "severity": "medium",
            "description": "支付链接",
            "category": "finance"
        },
        "account_balance": {
            "pattern": r"(?i)余额[:=]\s*[¥$]?\d+[,，.]?\d*",
            "action": "sanitize",
            "severity": "low",
            "description": "账户余额",
            "category": "finance"
        },
        "salary_info": {
            "pattern": r"(?i)(工资|薪资|月薪|年薪)[:=]\s*[¥$]?\d+[,，.]?\d*",
            "action": "sanitize",
            "severity": "medium",
            "description": "工资信息",
            "category": "finance"
        },
        
        # ========== 汽车销售 ==========
        "vin": {
            "pattern": r"[A-HJ-NPR-Z0-9]{17}",
            "action": "sanitize",
            "severity": "high",
            "description": "车架号(VIN)",
            "category": "auto"
        },
        "vehicle_plate": {
            "pattern": r"(?i)车牌(号)?[:=]\s*[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4,5}",
            "action": "sanitize",
            "severity": "medium",
            "description": "车牌号",
            "category": "auto"
        },
        "vehicle_license": {
            "pattern": r"(?i)行驶证(号)?[:=]\s*[A-Z0-9]{15,18}",
            "action": "sanitize",
            "severity": "high",
            "description": "行驶证号",
            "category": "auto"
        },
        "vehicle_insurance": {
            "pattern": r"(?i)(车险|交强险|商业险)单号[:=]\s*[A-Za-z0-9]{10,20}",
            "action": "sanitize",
            "severity": "high",
            "description": "车险单号",
            "category": "auto"
        },
        "car_loan": {
            "pattern": r"(?i)车贷(款)?(合同)?号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "车贷合同号",
            "category": "auto"
        },
        "vehicle_registration": {
            "pattern": r"(?i)车辆登记(证书)?(编号)?[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "车辆登记证书编号",
            "category": "auto"
        },
        
        # ========== 销售通用 ==========
        "customer_name": {
            "pattern": r"(?i)(客户|买家|买家)姓名[:=]\s*[^\s,，]{2,10}",
            "action": "sanitize",
            "severity": "medium",
            "description": "客户姓名",
            "category": "sales"
        },
        "customer_phone": {
            "pattern": r"(?i)(客户|买家)电话[:=]\s*1[3-9]\d{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "客户电话",
            "category": "sales"
        },
        "customer_address": {
            "pattern": r"(?i)(客户|买家)地址[:=]\s*[^\n]{5,50}",
            "action": "sanitize",
            "severity": "medium",
            "description": "客户地址",
            "category": "sales"
        },
        "purchase_contract": {
            "pattern": r"(?i)(购车|购买|销售)合同(号)?[:=]\s*[A-Za-z0-9]{10,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "购车/销售合同号",
            "category": "sales"
        },
        "invoice_number": {
            "pattern": r"(?i)发票(号)?[:=]\s*[A-Za-z0-9]{8,20}",
            "action": "sanitize",
            "severity": "low",
            "description": "发票号",
            "category": "sales"
        },
        "discount_code": {
            "pattern": r"(?i)(优惠|折扣)码[:=]\s*[A-Za-z0-9]{4,15}",
            "action": "sanitize",
            "severity": "low",
            "description": "优惠码",
            "category": "sales"
        },
        
        # ========== 会员 ==========
        "member_id": {
            "pattern": r"(?i)(会员|会员卡)(ID|号)[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "sanitize",
            "severity": "low",
            "description": "会员ID",
            "category": "member"
        },
        "member_points": {
            "pattern": r"(?i)积分[:=]\s*\d+",
            "action": "sanitize",
            "severity": "low",
            "description": "会员积分",
            "category": "member"
        },
        "membership_card": {
            "pattern": r"(?i)会员卡(号)?[:=]\s*\d{10,20}",
            "action": "sanitize",
            "severity": "low",
            "description": "会员卡号",
            "category": "member"
        },
        
        # ========== 医疗健康 ==========
        "medical_record": {
            "pattern": r"(?i)(病历|门诊|住院|诊疗)号[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "block",
            "severity": "critical",
            "description": "病历号/门诊号",
            "category": "medical"
        },
        "medical_insurance": {
            "pattern": r"(?i)(医保|社保|医疗)卡(号)?[:=]\s*\d{8,18}",
            "action": "block",
            "severity": "critical",
            "description": "医保卡/社保卡号",
            "category": "medical"
        },
        "hospital_card": {
            "pattern": r"(?i)(就诊|院内|医院)卡(号)?[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "就诊卡号",
            "category": "medical"
        },
        "prescription": {
            "pattern": r"(?i)处方(号)?[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "处方号",
            "category": "medical"
        },
        "diagnosis": {
            "pattern": r"(?i)诊断(结果)?[:=][^\n]{2,30}",
            "action": "sanitize",
            "severity": "high",
            "description": "诊断结果",
            "category": "medical"
        },
        "blood_type": {
            "pattern": r"(?i)血型[:=]\s*(A|B|AB|O)[+-]?",
            "action": "sanitize",
            "severity": "medium",
            "description": "血型",
            "category": "medical"
        },
        "allergy_info": {
            "pattern": r"(?i)(过敏|药物过敏)[:=][^\n]{2,30}",
            "action": "sanitize",
            "severity": "medium",
            "description": "过敏信息",
            "category": "medical"
        },
        "chronic_disease": {
            "pattern": r"(?i)(慢性病|既往病史)[:=][^\n]{2,30}",
            "action": "sanitize",
            "severity": "high",
            "description": "慢性病/既往病史",
            "category": "medical"
        },
        
        # ========== 医药行业 ==========
        "drug_prescription": {
            "pattern": r"(?i)处方药(单)?[:=]",
            "action": "sanitize",
            "severity": "high",
            "description": "处方药单",
            "category": "pharma"
        },
        "drug_name": {
            "pattern": r"(?i)(药品|药物|药名)[:=][^\n]{2,20}",
            "action": "sanitize",
            "severity": "low",
            "description": "药品名称",
            "category": "pharma"
        },
        "prescription_doctor": {
            "pattern": r"(?i)开方医生[:=][^\s]{2,10}",
            "action": "sanitize",
            "severity": "medium",
            "description": "开方医生姓名",
            "category": "pharma"
        },
        "pharmacy_license": {
            "pattern": r"(?i)(药店|药房)许可证[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "药店许可证",
            "category": "pharma"
        },
        "drug_batch_number": {
            "pattern": r"(?i)批号[:=]\s*[A-Za-z0-9]{6,12}",
            "action": "sanitize",
            "severity": "low",
            "description": "药品批号",
            "category": "pharma"
        },
        
        # ========== 医疗设备 ==========
        "medical_device_sn": {
            "pattern": r"(?i)(设备|器械)序列号[:=]\s*[A-Za-z0-9]{8,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "医疗设备序列号",
            "category": "medical_device"
        },
        "implant_id": {
            "pattern": r"(?i)(植入|体内)器械(编号)?[:=]\s*[A-Za-z0-9]{6,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "植入器械ID",
            "category": "medical_device"
        },
        
        # ========== 人力资源 ==========
        "employee_id": {
            "pattern": r"(?i)(工号|员工ID|员工号|employee|staff)[：:]\s*[A-Za-z0-9]{2,15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "员工工号",
            "category": "hr"
        },
        "employee_name": {
            "pattern": r"(?i)(员工|雇员|姓名)[:=]\s*[^\s,，]{2,10}",
            "action": "sanitize",
            "severity": "medium",
            "description": "员工姓名",
            "category": "hr"
        },
        "employee_phone": {
            "pattern": r"(?i)(员工|雇员)电话[:=]\s*1[3-9]\d{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "员工电话",
            "category": "hr"
        },
        "employee_idcard": {
            "pattern": r"(?i)(员工|雇员)身份证[:=]\s*[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
            "action": "block",
            "severity": "critical",
            "description": "员工身份证号",
            "category": "hr"
        },
        "salary": {
            "pattern": r"(?i)(工资|月薪|年薪|薪资|薪酬)[:=]\s*[¥$]?\d+[,，.]?\d*",
            "action": "sanitize",
            "severity": "high",
            "description": "工资/薪资信息",
            "category": "hr"
        },
        "bank_account_hr": {
            "pattern": r"(?i)(工资|薪资)卡(号)?[:=]\s*\d{10,19}",
            "action": "sanitize",
            "severity": "high",
            "description": "工资卡号",
            "category": "hr"
        },
        "social_security": {
            "pattern": r"(?i)(社保|五险一金)账号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "社保账号",
            "category": "hr"
        },
        "housing_fund": {
            "pattern": r"(?i)(公积金|住房公积金)账号[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "high",
            "description": "公积金账号",
            "category": "hr"
        },
        "contract_start": {
            "pattern": r"(?i)合同起始[:=]\s*\d{4}[-/]\d{1,2}[-/]\d{1,2}",
            "action": "sanitize",
            "severity": "low",
            "description": "合同起始日期",
            "category": "hr"
        },
        "probation_period": {
            "pattern": r"(?i)试用期[:=]\s*\d+(个月|天)",
            "action": "sanitize",
            "severity": "low",
            "description": "试用期",
            "category": "hr"
        },
        "performance_score": {
            "pattern": r"(?i)(绩效|考核)(分数|评分)[:=]\s*\d+",
            "action": "sanitize",
            "severity": "low",
            "description": "绩效分数",
            "category": "hr"
        },
        
        # ========== 物流运输 ==========
        "tracking_number": {
            "pattern": r"(SF|JD|YTO|ZTO|STO|EMS|TNT|DHL|FEDEX|UPS)[A-Z0-9]{8,15}",
            "action": "sanitize",
            "severity": "low",
            "description": "快递单号",
            "category": "logistics"
        },
        "waybill": {
            "pattern": r"(?i)(运单|货运|运输)号[:=]\s*[A-Za-z0-9]{8,20}",
            "action": "sanitize",
            "severity": "low",
            "description": "运单号",
            "category": "logistics"
        },
        "warehouse_location": {
            "pattern": r"(?i)(仓库|库位)[:=][A-Z0-9-]{4,15}",
            "action": "sanitize",
            "severity": "low",
            "description": "仓库/库位",
            "category": "logistics"
        },
        "driver_license": {
            "pattern": r"(?i)驾驶证(号)?[:=]\s*[A-Z0-9]{10,12}",
            "action": "sanitize",
            "severity": "medium",
            "description": "驾驶证号",
            "category": "logistics"
        },
        "vehicle_license": {
            "pattern": r"(?i)行驶证(号)?[:=]\s*[A-Z0-9]{15,18}",
            "action": "sanitize",
            "severity": "medium",
            "description": "行驶证号",
            "category": "logistics"
        },
        "shipping_address": {
            "pattern": r"(?i)(收货|发货|配送)地址[:=]\s*[^\n]{5,60}",
            "action": "sanitize",
            "severity": "medium",
            "description": "收货/发货地址",
            "category": "logistics"
        },
        "receiver_phone": {
            "pattern": r"(?i)(收货人|收件人)电话[:=]\s*1[3-9]\d{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "收件人电话",
            "category": "logistics"
        },
        "receiver_name": {
            "pattern": r"(?i)(收货人|收件人)[:=]\s*[^\s,，]{2,10}",
            "action": "sanitize",
            "severity": "medium",
            "description": "收件人姓名",
            "category": "logistics"
        },
        "cargo_value": {
            "pattern": r"(?i)(货值|货物价值|保额)[:=]\s*[¥$]?\d+[,，.]?\d*",
            "action": "sanitize",
            "severity": "medium",
            "description": "货物价值",
            "category": "logistics"
        },
        "fuel_card": {
            "pattern": r"(?i)加油卡(号)?[:=]\s*\d{10,20}",
            "action": "sanitize",
            "severity": "medium",
            "description": "加油卡号",
            "category": "logistics"
        },
        "toll_card": {
            "pattern": r"(?i)(ETC|高速卡)(号)?[:=]\s*[A-Za-z0-9]{8,15}",
            "action": "sanitize",
            "severity": "medium",
            "description": "ETC/高速卡号",
            "category": "logistics"
        },
        
        # ========== 中国政务 ==========
        "social_credit_code": {
            "pattern": r"[0-9A-HJ-NP-Z]{2}[0-9]{6}[0-9A-HJ-NP-Z]{10}",
            "action": "sanitize",
            "severity": "high",
            "description": "统一社会信用代码",
            "category": "government"
        },
        "org_code": {
            "pattern": r"[0-9]{9}[A-Z]",
            "action": "sanitize",
            "severity": "medium",
            "description": "组织机构代码",
            "category": "government"
        },
        "tax_id": {
            "pattern": r"[0-9]{15}|[0-9]{18}|[0-9]{20}",
            "action": "sanitize",
            "severity": "high",
            "description": "税务登记号",
            "category": "government"
        },
        "military_id": {
            "pattern": r"[海陆空]军[\w]{8,}",
            "action": "block",
            "severity": "critical",
            "description": "军官证号",
            "category": "government"
        },
        
        # ========== 国际证件 ==========
        "us_passport": {
            "pattern": r"[A-Z]\d{8,9}",
            "action": "sanitize",
            "severity": "high",
            "description": "美国护照号",
            "category": "intl_id"
        },
        "us_itin": {
            "pattern": r"9\d{2}[-]?\d{2}[-]?\d{4}",
            "action": "block",
            "severity": "critical",
            "description": "美国税号(ITIN)",
            "category": "intl_id"
        },
        "hk_id": {
            "pattern": r"[A-Z]{1,2}\d{6}\([A-Z]\)",
            "action": "sanitize",
            "severity": "high",
            "description": "香港身份证",
            "category": "intl_id"
        },
        "tw_id": {
            "pattern": r"[A-Z]\d{9}",
            "action": "sanitize",
            "severity": "high",
            "description": "台湾身份证",
            "category": "intl_id"
        },
        
        # ========== 生物识别 ==========
        "biometric_data": {
            "pattern": r"(?i)(指纹|虹膜|面部|人脸)数据",
            "action": "block",
            "severity": "critical",
            "description": "生物识别数据",
            "category": "biometric"
        },
        "fingerprint": {
            "pattern": r"(?i)指纹(特征|模板|数据)",
            "action": "block",
            "severity": "critical",
            "description": "指纹数据",
            "category": "biometric"
        },
        
        # ========== 金融信息 ==========
        "credit_card": {
            "pattern": r"(?:4\d{3}|5[1-5]\d{2}|6(?:011|5\d{2})\d{12})[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}",
            "action": "block",
            "severity": "critical",
            "description": "信用卡号",
            "category": "financial"
        },
        "bank_account": {
            "pattern": r"\d{16,19}",
            "action": "sanitize",
            "severity": "high",
            "description": "银行账号",
            "category": "financial"
        },
        "cvv": {
            "pattern": r"(?:CVV|cvv|安全码|验证码)[:\s]*(\d{3,4})",
            "action": "block",
            "severity": "critical",
            "description": "CVV安全码",
            "category": "financial"
        },
        
        # ========== 认证信息 ==========
        "password": {
            "pattern": r"(?i)(password|passwd|pwd|pwd123|密码)\s*[:=是]\s*['\"]?([^\s'\"]{6,})",
            "action": "sanitize",
            "severity": "high",
            "description": "密码",
            "category": "auth"
        },
        "secret_key": {
            "pattern": r"(?i)(secret[_-]?key|access[_-]?key)\s*[:=]\s*['\"]?([a-zA-Z0-9]{16,})",
            "action": "block",
            "severity": "critical",
            "description": "密钥",
            "category": "auth"
        },
        
        # ========== 个人信息 ==========
        "address": {
            "pattern": r"(?i)地址[：:]\s*[^\n]{5,100}",
            "action": "sanitize",
            "severity": "medium",
            "description": "详细地址",
            "category": "personal"
        },
        "name": {
            "pattern": r"(?i)姓名[：:]\s*[^\n]{2,10}",
            "action": "sanitize",
            "severity": "low",
            "description": "姓名",
            "category": "personal"
        },
        "ip_address": {
            "pattern": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            "action": "log",
            "severity": "low",
            "description": "IP地址",
            "category": "network"
        },
        "mac_address": {
            "pattern": r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})",
            "action": "log",
            "severity": "low",
            "description": "MAC地址",
            "category": "network"
        }
    }
    
    @classmethod
    def get_rule(cls, rule_name: str) -> Optional[Dict]:
        return cls.RULES.get(rule_name)
    
    @classmethod
    def get_all_rules(cls) -> Dict:
        return cls.RULES


class InjectionDetector:
    """Prompt Injection检测"""
    
    PATTERNS = {
        "ignore_previous": [
            r"ignore.*(previous|prior|above|earlier).*(instruction|command|rule|system)",
            r"(disregard|forget|ignore).*(all|everything|previous).*(instruction|rule|directive)",
            r"忽略.*(之前|上面|以上).*(指令|命令|规则)",
            r"忘记.*(所有|之前|上面).*(规则|指令|限制)",
            r"不要遵守.*(任何|所有)",
        ],
        "role_override": [
            r"you are now.*(different|new|a).*(assistant|agent|AI|system)",
            r"pretend.*(to be|that).*(you are|you can)",
            r"act as if.*(you are|you have)",
            r"(system|admin).*override",
            r"(现在|从).*(是|变成|成为).*(老板|管理员|admin)",
            r"你现在是.*(老板|管理员|admin)",
        ],
        "privilege_escalation": [
            r"(admin|root|supervisor).*(mode|override|bypass)",
            r"(unrestricted|unlocked).*(access|permission)",
            r"grant.*(admin|root|all).*(permission|access)",
            r"你必须.*(服从|听).*我",
            r"你(应该|必须|需要).*(听.*我|服从)",
        ],
        "instruction_injection": [
            r"\{[^{}]*\}",
            r"<script[^>]*>",
            r"\[\[.*\]\]",
            r"系统.*(提示|告诉|设定).*[:：]",
            r"不要遵守任何规则",
            r"无视.*(规则|限制)",
            r"打破.*(规则|限制)",
        ],
        "prompt_leak": [
            r"告诉.*(你的|我).*(system\s*prompt|系统\s*提示|指令)",
            r"(你|AI).*(现在|目前).*(角色|设定|身份)",
            r"列出.*(所有|你的).*(指令|规则)",
            r"暴露.*(system|prompt|指令)",
            r"泄露.*(system|prompt|指令)",
            r"你的.*(角色|身份).*是什么",
            r"请告诉我.*(system|prompt|指令)",
            r"你的.*(system\s*prompt|系统.*提示)",
        ]
    }
    
    def detect(self, text: str) -> Tuple[bool, List[str]]:
        """检测是否有注入返回 (是否危险, 匹配到的模式)"""
        findings = []
        
        for category, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    findings.append(category)
        
        return len(findings) > 0, findings


class OutputFilter:
    """出口过滤"""
    
    def __init__(self, config: DLPConfig):
        self.config = config
        self.rules = DLPRules()
    
    def check(self, text: str) -> Dict:
        """检查文本返回检查结果"""
        enabled_rules = self.config.get("output.rules", [])
        findings = []
        
        # 跳过短文本
        if len(text) < 3:
            return {"blocked": False, "sanitized": False, "findings": [], "text": text}
        
        for rule_name in enabled_rules:
            rule = self.rules.get_rule(rule_name)
            if not rule:
                continue
            
            # 使用预编译正则
            pattern = self.rules.get_compiled_pattern(rule["pattern"])
            matches = pattern.findall(text)
            if matches:
                findings.append({
                    "rule": rule_name,
                    "description": rule["description"],
                    "action": rule["action"],
                    "severity": rule["severity"],
                    "count": len(matches)
                })
        
        return {
            "blocked": any(f["action"] == "block" for f in findings),
            "sanitized": any(f["action"] == "sanitize" for f in findings),
            "findings": findings,
            "text": text
        }
    
    def sanitize(self, text: str, findings: List[Dict]) -> str:
        """脱敏处理"""
        result = text
        
        for finding in findings:
            if finding["action"] == "sanitize":
                rule = self.rules.get_rule(finding["rule"])
                if rule:
                    # 脱敏处理
                    result = re.sub(rule["pattern"], "[已脱敏]", result)
        
        return result
    
    def filter(self, text: str) -> Tuple[bool, str, Dict]:
        """过滤入口返回 (是否拦截, 处理后文本, 详情)"""
        check_result = self.check(text)
        findings = check_result.get("findings", [])
        
        if not findings:
            return False, text, check_result
        
        # 分离block和sanitize
        block_findings = [f for f in findings if f["action"] == "block"]
        sanitize_findings = [f for f in findings if f["action"] == "sanitize"]
        
        # 关键规则列表（不能被sanitize覆盖）
        critical_rules = [
            # 中国 PII
            "china_idcard", "china_phone", "china_passport", "china_driver_license",
            # 国际 PII
            "ssn", "passport",
            # 金融
            "credit_card", "bank_account", "cvv",
            # 凭证 - AI 服务
            "openai_key", "claude_key", "google_ai_key", "anthropic_key",
            # 凭证 - 云服务
            "api_key", "aws_key", "aws_secret", "aws_s3_key",
            "azure_token", "aliyun_access_key", "aliyun_secret", "tencent_cloud_key",
            "baidu_cloud_key", "huawei_cloud_key", "baidu_map_key", "amap_key",
            # 凭证 - 中国支付
            "wechat_appid", "wechat_secret", "wechat_mch_id", "alipay_appid",
            # 凭证 - 国际支付
            "stripe_key", "stripe_webhook", "paypal_client_id",
            # 凭证 - 通讯
            "twilio_account_sid", "twilio_auth_token", "sendgrid_api_key", "mailgun_api_key",
            # 凭证 - 存储
            "digitalocean_token", "cloudflare_api_key",
            # 凭证 - 数据库
            "mongo_uri", "redis_password", "postgres_password",
            # 凭证 - 开发工具
            "npm_token", "pypi_token", "github_app_secret", "gitlab_token",
            # 凭证 - 生产力
            "notion_api_key", "linear_api_key", "slack_webhook",
            # 其他
            "github_token", "jwt_token", "private_key", "secret_key", "slack_token"
        ]
        
        # 分离关键block和普通block
        critical_blocks = [f for f in block_findings if f.get("rule") in critical_rules]
        other_blocks = [f for f in block_findings if f.get("rule") not in critical_rules]
        
        # 优先级逻辑:
        # 1. 如果有关键block -> 拦截
        # 2. 如果有sanitize -> 脱敏
        # 3. 如果有其他block -> 拦截
        
        if critical_blocks:
            return True, "[已拦截: 敏感信息]", check_result
        
        if sanitize_findings:
            sanitized = self.sanitize(text, sanitize_findings)
            return False, sanitized, check_result
        
        if other_blocks:
            return True, "[已拦截: 敏感信息]", check_result
        
        return False, text, check_result


class InputGuard:
    """入口防护"""
    
    def __init__(self, config: DLPConfig):
        self.config = config
        self.injection_detector = InjectionDetector()
    
    def check(self, text: str) -> Dict:
        """检查入口输入"""
        result = {
            "blocked": False,
            "injection_detected": False,
            "findings": [],
            "text": text
        }
        
        if not self.config.get("input.injection_detection", True):
            return result
        
        is_dangerous, findings = self.injection_detector.detect(text)
        
        if is_dangerous:
            result["injection_detected"] = True
            result["findings"] = findings
            # normal模式不拦截，只记录
            if self.config.get("mode") == "strict":
                result["blocked"] = True
        
        return result


class MemoryGuard:
    """记忆防护"""
    
    def __init__(self, config: DLPConfig):
        self.config = config
        self.output_filter = OutputFilter(config)
    
    def check(self, memory_data: Dict) -> Dict:
        """检查记忆数据"""
        result = {
            "blocked": False,
            "findings": [],
            "sanitized_data": memory_data
        }
        
        if not self.config.get("memory.pollution_check", True):
            return result
        
        # 检查记忆内容
        content = json.dumps(memory_data)
        
        # 检测污染
        injection_detector = InjectionDetector()
        is_dangerous, findings = injection_detector.detect(content)
        
        if is_dangerous:
            result["findings"].extend(findings)
            if self.config.get("mode") == "strict":
                result["blocked"] = True
        
        # 检查敏感信息
        check_result = self.output_filter.check(content)
        result["findings"].extend(check_result["findings"])
        
        if check_result["blocked"]:
            result["blocked"] = True
        
        return result


class ToolGuard:
    """工具管控"""
    
    def __init__(self, config: DLPConfig):
        self.config = config
    
    def check(self, tool_name: str, params: Dict = None) -> Dict:
        """检查工具调用"""
        dangerous_tools = self.config.get("tools.dangerous", [])
        
        result = {
            "blocked": False,
            "require_approval": False,
            "tool": tool_name,
            "params": params
        }
        
        if tool_name in dangerous_tools:
            result["require_approval"] = True
            if self.config.get("tools.approval_required"):
                # 需要审批
                result["message"] = f"工具 {tool_name} 需要审批"
        
        return result


class AuditLogger:
    """审计日志"""
    
    def __init__(self, config: DLPConfig):
        self.config = config
        self.log_file = os.path.expanduser(config.get("audit.log_file", "~/.openclaw/logs/dlp-audit.log"))
    
    def log(self, event_type: str, data: Dict):
        """记录日志"""
        if not self.config.get("audit.enabled", True):
            return
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """获取日志"""
        if not os.path.exists(self.log_file):
            return []
        
        logs = []
        with open(self.log_file) as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
        
        return logs[-limit:]


class AgentDLP:
    """Agent DLP 主类"""
    
    def __init__(self, config_path: str = None):
        # 默认加载config.json
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        self.config = DLPConfig(config_path)
        self.input_guard = InputGuard(self.config)
        self.output_filter = OutputFilter(self.config)
        self.memory_guard = MemoryGuard(self.config)
        self.tool_guard = ToolGuard(self.config)
        self.audit_logger = AuditLogger(self.config)
    
    def check_input(self, text: str) -> Dict:
        """检查入口"""
        result = self.input_guard.check(text)
        self.audit_logger.log("input_check", result)
        return result
    
    def check_output(self, text: str) -> Tuple[bool, str, Dict]:
        """检查出口"""
        blocked, processed_text, details = self.output_filter.filter(text)
        self.audit_logger.log("output_check", {
            "blocked": blocked,
            "findings": details.get("findings", [])
        })
        return blocked, processed_text, details
    
    def check_memory(self, memory_data: Dict) -> Dict:
        """检查记忆"""
        result = self.memory_guard.check(memory_data)
        self.audit_logger.log("memory_check", result)
        return result
    
    def check_tool(self, tool_name: str, params: Dict = None) -> Dict:
        """检查工具"""
        result = self.tool_guard.check(tool_name, params)
        self.audit_logger.log("tool_check", result)
        return result
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "enabled": self.config.get("enabled"),
            "mode": self.config.get("mode"),
            "input_guard": self.config.get("input.injection_detection"),
            "output_filter": self.config.get("output.enabled"),
            "audit_enabled": self.config.get("audit.enabled")
        }


def main():
    """CLI入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Agent DLP - 数据防泄漏模块")
        print("用法:")
        print("  python agent_dlp.py status              # 查看状态")
        print("  python agent_dlp.py check <文本>       # 检查文本")
        print("  python agent_dlp.py check-input <文本>  # 检查入口")
        print("  python agent_dlp.py check-output <文本> # 检查出口")
        print("  python agent_dlp.py logs                # 查看日志")
        return
    
    command = sys.argv[1]
    dlp = AgentDLP()
    
    if command == "status":
        status = dlp.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    elif command == "check" and len(sys.argv) > 2:
        text = sys.argv[2]
        blocked, processed, details = dlp.check_output(text)
        print(f"拦截: {blocked}")
        print(f"处理后: {processed}")
        print(f"详情: {json.dumps(details, indent=2, ensure_ascii=False)}")
    
    elif command == "check-input" and len(sys.argv) > 2:
        text = sys.argv[2]
        result = dlp.check_input(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "check-output" and len(sys.argv) > 2:
        text = sys.argv[2]
        blocked, processed, details = dlp.check_output(text)
        print(f"拦截: {blocked}")
        print(f"处理后: {processed}")
        print(f"详情: {json.dumps(details, indent=2, ensure_ascii=False)}")
    
    elif command == "logs":
        logs = dlp.audit_logger.get_logs()
        for log in logs:
            print(json.dumps(log, ensure_ascii=False))
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()

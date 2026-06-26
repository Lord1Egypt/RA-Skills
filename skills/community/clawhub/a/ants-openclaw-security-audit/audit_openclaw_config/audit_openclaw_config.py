#!/usr/bin/env python3
import json
import os
import sys

def get_nested(data, path, default=None):
    """
    安全地获取嵌套 JSON 字典中的值。
    例如传入 path="logging.redactSensitive"，将尝试返回 data["logging"]["redactSensitive"]
    """
    keys = path.split('.')
    val = data
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            return default
    return val

def check_official_baseline(config):
    findings = []
    
    # 1. 检查日志脱敏 (JSON 结构: {"logging": {"redactSensitive": "off"}})
    if get_nested(config, "logging.redactSensitive") == "off":
        findings.append("[P1] 日志敏感信息明文暴露: `logging.redactSensitive` 被设为 \"off\"。官方建议将其恢复为 \"tools\" 以对会话日志进行脱敏。")

    # 2. 检查群组策略 (JSON 结构: {"groupPolicy": "open"})
    if config.get("groupPolicy") == "open":
        findings.append("[P1] 群组完全开放: `groupPolicy` 被设为 \"open\"。机器人在群组中极易被路人触发，官方建议收紧为 \"allowlist\"。")

    # 3. 检查 Web 控制台 UI 认证安全 (JSON 结构: {"gateway": {"controlUi": {"...": true}}})
    if get_nested(config, "gateway.controlUi.dangerouslyDisableDeviceAuth") is True:
        findings.append("[P0] UI 认证被完全禁用: `gateway.controlUi.dangerouslyDisableDeviceAuth` 为 true。这是严重的安全性降级，任何人均可访问控制台！")
    
    if get_nested(config, "gateway.controlUi.allowInsecureAuth") is True:
        findings.append("[P1] UI 不安全认证开启: `gateway.controlUi.allowInsecureAuth` 为 true，这会导致设备配对被跳过。建议优先使用 HTTPS (Tailscale Serve) 或限制在 localhost。")

    # 4. 检查私信访问模型 (JSON 结构: {"dmPolicy": "open"})
    dm_policy = config.get("dmPolicy", "pairing")
    if dm_policy == "open":
        findings.append("[P0] 私信完全开放: `dmPolicy` 被设为 \"open\"。任何陌生人均可私信机器人，这会将机器人完全暴露于提示词注入攻击。建议改为 \"pairing\" 或 \"allowlist\"。")

    # 5. 检查私信会话隔离 (JSON 结构: {"session": {"dmScope": "..."}})
    dm_scope = get_nested(config, "session.dmScope")
    if dm_policy in ["open", "allowlist"] and dm_scope not in ["per-channel-peer", "per-account-channel-peer"]:
        findings.append("[P2] 缺少会话隔离: 当前允许外部人员私信，但未配置 `session.dmScope: \"per-channel-peer\"`。这可能导致多用户之间的聊天上下文发生交叉泄露。")

    # 6. 检查插件白名单 (JSON 结构: {"plugins": {"allow": [...]}})
    if "plugins" in config and not get_nested(config, "plugins.allow"):
        findings.append("[P2] 插件白名单缺失: 官方建议优先使用显式的 `plugins.allow` 白名单，只加载你明确信任的插件。")

    return findings

def main():
    # 明确寻找 openclaw.json 配置文件
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw"))
    config_paths = [
        os.path.join(workspace, "openclaw.json"),
        "/etc/openclaw/openclaw.json",
        "/opt/openclaw/openclaw.json"
    ]
    
    config_data = None
    used_path = ""
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    used_path = path
                    break
            except Exception as e:
                continue
                
    result = {"status": "unknown", "checked_file": used_path, "findings": []}
    
    if not config_data:
        result["status"] = "error"
        result["findings"] = [f"未在系统或工作区中找到可解析的 openclaw.json 配置文件。"]
    else:
        risks = check_official_baseline(config_data)
        if risks:
            result["status"] = "risks_found"
            result["findings"] = risks
        else:
            result["status"] = "clean"
            result["findings"] = ["openclaw.json 配置文件符合官方文档建议的安全基线。"]

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
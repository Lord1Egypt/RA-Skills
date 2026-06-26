#!/usr/bin/env python3
import json
import os
import sys

def get_nested(data, path, default=None):
    keys = path.split('.')
    val = data
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            return default
    return val

def check_sandbox_baseline(config):
    findings = []
    
    # 获取沙箱全局默认配置
    sandbox_cfg = get_nested(config, "agents.defaults.sandbox", {})
    
    # 1. 沙箱开启状态检查
    mode = sandbox_cfg.get("mode", "non-main")
    if mode == "off":
        findings.append("[P0] 沙箱已彻底关闭: `sandbox.mode` 为 \"off\"。所有工具（含 exec）都将直接在宿主机上运行，存在极高的主机接管风险！")

    # 2. 工作区访问权限检查
    workspace_access = sandbox_cfg.get("workspaceAccess", "none")
    if workspace_access == "rw":
        findings.append("[P1] 工作区过度授权: `workspaceAccess` 被设为 \"rw\"。沙箱内的 AI 可以随意篡改宿主机映射的智能体工作区，建议收紧为 \"ro\" 或 \"none\"。")

    # 3. 危险绑定挂载检查 (Binds)
    binds = get_nested(sandbox_cfg, "docker.binds", [])
    dangerous_host_paths = ["/var/run/docker.sock", "/etc", "/root", "/home", "/usr", "/sys"]
    if isinstance(binds, list):
        for bind in binds:
            # 解析 "host:container:mode"
            parts = bind.split(":")
            if len(parts) >= 1:
                host_path = parts[0]
                mode_str = parts[-1] if len(parts) >= 3 else "rw" # 默认通常是 rw
                
                for d_path in dangerous_host_paths:
                    if host_path.startswith(d_path):
                        if mode_str == "rw":
                            findings.append(f"[P0] 致命容器逃逸: 敏感主机目录 `{host_path}` 被以读写(rw)模式挂载到了沙箱内。攻击者可借此直接接管宿主机！")
                        else:
                            findings.append(f"[P1] 敏感信息泄露: 主机目录 `{host_path}` 被挂载到了沙箱内。即使是只读(ro)，也极易导致宿主机凭据泄露。")

    # 4. 网络出口检查
    network = get_nested(sandbox_cfg, "docker.network", "none")
    if network != "none":
        findings.append(f"[P2] 沙箱网络出口已开启: `docker.network` 被设为 \"{network}\"。官方默认沙箱是无网络的。请确认你确实需要 AI 在沙箱内发起外网请求。")

    return findings

def main():
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw"))
    config_paths = [os.path.join(workspace, "openclaw.json"), "/etc/openclaw/openclaw.json"]
    
    config_data = None
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    break
            except Exception:
                continue
                
    result = {"status": "unknown", "findings": []}
    
    if not config_data:
        result["status"] = "error"
        result["findings"] = ["未找到 openclaw.json，无法进行沙箱配置审计。"]
    else:
        risks = check_sandbox_baseline(config_data)
        if risks:
            result["status"] = "risks_found"
            result["findings"] = risks
        else:
            result["status"] = "clean"
            result["findings"] = ["沙箱基础配置严密，未发现明显的过度授权或危险挂载。"]

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
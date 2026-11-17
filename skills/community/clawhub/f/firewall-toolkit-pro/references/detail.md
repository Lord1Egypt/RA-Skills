# 详细参考 - firewall-toolkit-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版多云安全组管理器"""

import json
from abc import ABC, abstractmethod

class SecurityGroupManager(ABC):
    """安全组管理基类"""

    @abstractmethod
    def list_security_groups(self):
        pass

    @abstractmethod
    def create_rule(self, group_id, rule):
        pass

    @abstractmethod
    def delete_rule(self, group_id, rule_id):
        pass

class AWSSecurityGroupManager(SecurityGroupManager):
    """AWS安全组管理"""

    def __init__(self):
        import boto3
        self.ec2 = boto3.client('ec2')

    def list_security_groups(self):
        response = self.ec2.describe_security_groups()
        return [
            {
                "id": sg['GroupId'],
                "name": sg['GroupName'],
                "description": sg.get('Description', ''),
                "rules": len(sg.get('IpPermissions', []))
            }
            for sg in response['SecurityGroups']
        ]

    def create_rule(self, group_id, rule):
        """创建入站规则"""
        response = self.ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[{
                'IpProtocol': rule.get('protocol', 'tcp'),
                'FromPort': rule['port'],
                'ToPort': rule['port'],
                'IpRanges': [{'CidrIp': rule.get('cidr', '0.0.0.0/0')}]
            }]
        )
        return response

    def delete_rule(self, group_id, rule_id):
        """删除规则"""
        pass

    def audit_open_ports(self):
        """审计所有开放端口"""
        groups = self.ec2.describe_security_groups()
        findings = []

        for sg in groups['SecurityGroups']:
            for perm in sg.get('IpPermissions', []):
                cidr = perm.get('IpRanges', [{}])[0].get('CidrIp', '')
                if cidr == '0.0.0.0/0':
                    port = perm.get('FromPort', 'ALL')
                    protocol = perm.get('IpProtocol', 'all')

                    severity = "CRITICAL"
                    if protocol == 'tcp' and port in [22, 3389]:
                        severity = "CRITICAL"
                    elif protocol == 'tcp' and port in [80, 443]:
                        severity = "INFO"
                    elif port in [3306, 5432, 6379, 27017]:
                        severity = "HIGH"

                    findings.append({
                        "group": sg['GroupName'],
                        "group_id": sg['GroupId'],
                        "port": port,
                        "protocol": protocol,
                        "cidr": cidr,
                        "severity": severity,
                        "description": f"{sg['GroupName']} 开放 {port}/{protocol} 给 0.0.0.0/0"
                    })

        return findings

class AzureSecurityGroupManager(SecurityGroupManager):
    """Azure网络安全组管理"""

    def __init__(self):
        from azure.mgmt.network import NetworkManagementClient
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        self.client = NetworkManagementClient(credential, "subscription_id")

    def list_security_groups(self):
        groups = self.client.network_security_groups.list_all()
        return [{"id": g.id, "name": g.name} for g in groups]

if __name__ == "__main__":
    manager = AWSSecurityGroupManager()

    findings = manager.audit_open_ports()
    print(f"发现 {len(findings)} 个开放端口:")
    for f in findings:
        print(f"  [{f['severity']}] {f['description']}")
```

## 代码示例 (bash)

```bash
#!/bin/bash
echo "=== nftables企业级配置 ==="

cat > /etc/nftables.conf << 'NFTABLES'
#!/usr/sbin/nft -f

flush ruleset

table inet firewall {
    set admin_ips {
        type ipv4_addr
        flags interval
        elements = {
            10.0.0.0/8,      # 内网管理段
            192.168.1.0/24   # 管理员网段
        }
    }

    set blacklist {
        type ipv4_addr
        flags interval
        elements = {}
    }

    set blocked_ports {
        type inet_service
        elements = { 23, 21, 3389, 3306, 5432, 6379, 27017 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept

        ct state established,related accept

        ct state invalid drop

        ip saddr @blacklist drop

        tcp dport { 22, 8080 } ip saddr != @admin_ips drop

        tcp dport 22 limit rate 5/minute burst 10 packets accept

        tcp dport { 80, 443 } accept

        tcp dport @blocked_ports drop

        icmp type echo-request limit rate 1/second accept

        limit rate 5/minute log prefix "nft-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
        ct state established,related accept
        ct state invalid drop
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}

table ip nat {
    chain prerouting {
        type nat hook prerouting priority 0;
    }

    chain postrouting {
        type nat hook postrouting priority 100;
    }
}
NFTABLES

nft -f /etc/nftables.conf
echo "nftables配置已应用"

systemctl enable nftables
systemctl start nftables

echo ""
echo "=== 当前nftables规则 ==="
nft list ruleset | head -50
```


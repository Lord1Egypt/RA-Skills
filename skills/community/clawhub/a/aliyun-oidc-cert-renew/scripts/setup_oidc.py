#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性搭建「GitHub Actions 免 AK 访问阿里云」所需的 RAM 资源。

会创建 / 幂等更新三样东西：
  1. OIDC 提供商（IMS API，注意不是 ram20150501）
  2. RAM 角色（信任策略 StringLike 通配 oidc:sub）
  3. 权限策略 + 绑定到角色

用法（永久 AK 从环境变量读，不落盘、不进仓库）：
    export ALIBABA_CLOUD_ACCESS_KEY_ID=LTAI...
    export ALIBABA_CLOUD_ACCESS_KEY_SECRET=...
    python setup_oidc.py --owner <owner> --repo <repo> \
        [--provider github] [--role github-oidc-role] [--policy github-actions-policy] \
        [--branch main] [--dry-run]

可选：--actions oss,fc,alidns,yundun-cert  自定义授权命名空间（默认全给）
前置：pip install alibabacloud_ims20190815 alibabacloud_ram20150501 alibabacloud_sts20150401
"""
import argparse
import json
import os
import sys

try:
    from alibabacloud_tea_openapi import models as openapi_models
    from alibabacloud_ims20190815.client import Client as ImsClient
    from alibabacloud_ims20190815 import models as ims_models
    from alibabacloud_ram20150501.client import Client as RamClient
    from alibabacloud_ram20150501 import models as ram_models
    from alibabacloud_sts20150401.client import Client as StsClient
except ImportError:
    sys.exit('缺少依赖：pip install alibabacloud_ims20190815 alibabacloud_ram20150501 '
             'alibabacloud_sts20150401')

ISSUER = 'https://token.actions.githubusercontent.com'
# CAS（证书管理服务）的 RAM 命名空间是 yundun-cert，不是 cas
DEFAULT_ACTIONS = ['oss:*', 'fc:*', 'alidns:*', 'yundun-cert:*']


def cfg(endpoint):
    return openapi_models.Config(
        endpoint=endpoint,
        access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
        access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
    )


def log(msg):
    print('[setup_oidc] %s' % msg, flush=True)


def get_account_id():
    sts = StsClient(cfg('sts.aliyuncs.com'))
    return sts.get_caller_identity().body.account_id


def ensure_provider(ims, name, audience, dry):
    """OIDC 提供商：audience 白名单（ClientIds）必须与 workflow 的 audience 一致。"""
    for p in ims.list_oidcproviders().body.oidc_providers or []:
        if p.oidc_provider_name == name:
            log('OIDC 提供商已存在: %s' % name)
            ids = [c for c in (p.client_ids or [])]
            if audience not in ids:
                log('  追加 audience -> %s' % audience)
                if not dry:
                    ims.add_client_id_to_oidcprovider(
                        ims_models.AddClientIdToOIDCProviderRequest(
                            oidc_provider_name=name, client_id=audience))
            return
    log('创建 OIDC 提供商: %s' % name)
    if dry:
        return
    fp = input('请输入 token.actions.githubusercontent.com 的 SHA1 指纹（纯 hex，无冒号）: ').strip()
    fp = fp.replace(':', '').replace(' ', '').lower()
    ims.create_oidcprovider(ims_models.CreateOIDCProviderRequest(
        oidc_provider_name=name,
        issuer_url=ISSUER,
        # 指纹必须是纯 hex，带冒号会被拒
        fingerprints=[fp],
        # audience 白名单，别漏
        client_ids=[audience],
        description='GitHub Actions OIDC',
    ))


def trust_policy(acct, provider, owner, repo, audience, branch):
    return {
        'Statement': [{
            'Action': 'sts:AssumeRole',
            'Effect': 'Allow',
            'Principal': {'Federated': 'acs:ram::%s:oidc-provider/%s' % (acct, provider)},
            'Condition': {
                'StringEquals': {'oidc:iss': ISSUER, 'oidc:aud': audience},
                # GitHub 可能把 repo/owner ID 嵌进 sub，必须用 StringLike 通配
                'StringLike': {'oidc:sub': 'repo:%s*/%s*:ref:refs/heads/%s'
                                           % (owner, repo, branch)},
            },
        }],
        'Version': '1',
    }


def ensure_role(ram, role, trust, dry):
    try:
        ram.get_role(ram_models.GetRoleRequest(role_name=role))
        log('角色已存在，更新信任策略 -> %s' % role)
        if not dry:
            ram.update_role(ram_models.UpdateRoleRequest(
                role_name=role, new_assume_role_policy_document=json.dumps(trust)))
    except Exception:
        log('创建角色: %s' % role)
        if not dry:
            ram.create_role(ram_models.CreateRoleRequest(
                role_name=role,
                assume_role_policy_document=json.dumps(trust),
                description='GitHub Actions OIDC role',
            ))


def ensure_policy(ram, policy, actions, role, dry):
    doc = {'Statement': [{'Action': actions, 'Effect': 'Allow', 'Resource': ['*']}],
           'Version': '1'}
    exists = True
    try:
        ram.get_policy(ram_models.GetPolicyRequest(policy_name=policy, policy_type='Custom'))
        log('策略已存在，建新版本并设为默认 -> %s' % policy)
    except Exception:
        exists = False
        log('创建策略: %s' % policy)

    if dry:
        return
    if exists:
        # 版本上限 5，超了要先 delete_policy_version 删最旧的非默认版
        vers = ram.list_policy_versions(
            ram_models.ListPolicyVersionsRequest(
                policy_name=policy, policy_type='Custom')).body.policy_versions or []
        non_default = [v for v in vers if not v.is_default_version]
        if len(vers) >= 5 and non_default:
            oldest = sorted(non_default, key=lambda v: v.create_date)[0]
            log('  达到版本上限，删除最旧版本 %s' % oldest.version_id)
            ram.delete_policy_version(ram_models.DeletePolicyVersionRequest(
                policy_name=policy, version_id=oldest.version_id))
        # 注意：CreatePolicyVersionRequest 没有 policy_type 字段
        ram.create_policy_version(ram_models.CreatePolicyVersionRequest(
            policy_name=policy, policy_document=json.dumps(doc), set_as_default=True))
    else:
        ram.create_policy(ram_models.CreatePolicyRequest(
            policy_name=policy, policy_document=json.dumps(doc),
            policy_type='Custom', description='GitHub Actions policy'))

    ram.attach_policy_to_role(ram_models.AttachPolicyToRoleRequest(
        policy_name=policy, policy_type='Custom', role_name=role))
    log('策略已绑定到角色')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--owner', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--branch', default='main')
    ap.add_argument('--provider', default='github')
    ap.add_argument('--role', default='github-oidc-role')
    ap.add_argument('--policy', default='github-actions-policy')
    ap.add_argument('--actions', default=','.join(DEFAULT_ACTIONS))
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    acct = get_account_id()
    audience = 'https://github.com/%s/%s' % (a.owner, a.repo)
    log('账号 %s / audience %s' % (acct, audience))

    ims, ram = ImsClient(cfg('ims.aliyuncs.com')), RamClient(cfg('ram.aliyuncs.com'))
    ensure_provider(ims, a.provider, audience, a.dry_run)
    trust = trust_policy(acct, a.provider, a.owner, a.repo, audience, a.branch)
    ensure_role(ram, a.role, trust, a.dry_run)
    ensure_policy(ram, a.policy, [x.strip() for x in a.actions.split(',') if x.strip()],
                  a.role, a.dry_run)

    print('\n=== 填进仓库 Secrets 的两个 ARN（非敏感，也可直接写 workflow）===')
    print('ALI_OIDC_ARN = acs:ram::%s:oidc-provider/%s' % (acct, a.provider))
    print('ALI_ROLE_ARN = acs:ram::%s:role/%s' % (acct, a.role))
    print('AUDIENCE     = %s' % audience)


if __name__ == '__main__':
    main()

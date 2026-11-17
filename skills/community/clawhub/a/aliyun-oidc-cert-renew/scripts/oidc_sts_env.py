#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Actions 步骤：OIDC JWT -> AssumeRoleWithOIDC -> 临时 STS 凭证写入 $GITHUB_ENV。

替代 aliyun/configure-aliyun-credentials-action（后者在 RAM 配置正确时仍会 ImplicitDeny）。

要求 step 具备：
    permissions: { id-token: write }
    env:
      ALI_ROLE_ARN / ALI_OIDC_ARN / AUDIENCE

输出：向 $GITHUB_ENV 追加
    ALIBABA_CLOUD_ACCESS_KEY_ID / _SECRET / ALIBABA_CLOUD_SECURITY_TOKEN
供后续步骤的阿里云 SDK 与 oss2 直接读取。
前置：pip install alibabacloud_sts20150401
"""
import base64
import json
import os
import sys
import time
import urllib.request


def b64decode(seg):
    seg += '=' * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg))


def fetch_oidc_token(audience):
    # URL 已自带 ?job_id=...，必须「追加」而不是另起 query
    url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'] + '&audience=' + audience
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)['value']


def main():
    audience = os.environ.get('AUDIENCE') or \
        'https://github.com/' + os.environ['GITHUB_REPOSITORY']
    token = fetch_oidc_token(audience)

    # 打印 RAM 实际看到的 claim：定位 ImplicitDeny / AudienceNotMatch 的唯一快路径
    claims = b64decode(token.split('.')[1])
    print('OIDC claims -> iss=%r aud=%r sub=%r'
          % (claims.get('iss'), claims.get('aud'), claims.get('sub')), flush=True)

    from alibabacloud_tea_openapi import models as openapi_models
    from alibabacloud_sts20150401.client import Client as StsClient
    from alibabacloud_sts20150401 import models as sts_models

    sts = StsClient(openapi_models.Config(endpoint='sts.aliyuncs.com'))
    req = sts_models.AssumeRoleWithOIDCRequest(
        oidcprovider_arn=os.environ['ALI_OIDC_ARN'],
        role_arn=os.environ['ALI_ROLE_ARN'],
        oidctoken=token,
        role_session_name=os.environ.get('ROLE_SESSION_NAME', 'gh-oidc'),
    )

    # STS 偶发 InternalError 500，指数退避重试吸收
    last = None
    for i in range(5):
        try:
            resp = sts.assume_role_with_oidc(req)
            break
        except Exception as e:                      # noqa: BLE001
            last = e
            print('AssumeRoleWithOIDC 第 %d 次失败: %s' % (i + 1, str(e)[:200]), flush=True)
            time.sleep(2 ** i)
    else:
        sys.exit('AssumeRoleWithOIDC 连续失败: %s' % last)

    c = resp.body.credentials
    with open(os.environ['GITHUB_ENV'], 'a', encoding='utf-8') as f:
        f.write('ALIBABA_CLOUD_ACCESS_KEY_ID=%s\n' % c.access_key_id)
        f.write('ALIBABA_CLOUD_ACCESS_KEY_SECRET=%s\n' % c.access_key_secret)
        f.write('ALIBABA_CLOUD_SECURITY_TOKEN=%s\n' % c.security_token)
    print('STS 临时凭证已获取，expiration=%s' % c.expiration, flush=True)


if __name__ == '__main__':
    main()
